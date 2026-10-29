"""Lifecycle policy decisions (Phase 11D-3)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.skill import Skill
from core.states import SkillState
from skills.config import SkillConfig
from skills.lifecycle.aging import tasks_since_use
from skills.lifecycle.health import HealthScore, compute_health
from skills.lifecycle.metrics import LifecycleMetrics, compute_lifecycle_metrics
from skills.utility_components import compute_nr

ACTIVE_TIER = frozenset(
    {SkillState.ACTIVE, SkillState.GROWING, SkillState.CORE}
)


@dataclass(slots=True)
class LifecycleDecision:
    """Policy outcome for one skill evaluation."""

    action: str  # keep | grow | core | decline | dormant | retire | archive
    target_state: SkillState | None
    reasons: list[str] = field(default_factory=list)
    metrics: LifecycleMetrics | None = None
    health: HealthScore | None = None
    lifecycle_patch: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "target_state": (
                self.target_state.value if self.target_state else None
            ),
            "reasons": list(self.reasons),
            "metrics": self.metrics.to_dict() if self.metrics else None,
            "health": self.health.to_dict() if self.health else None,
            "lifecycle_patch": dict(self.lifecycle_patch),
        }


def _life(skill: Skill) -> dict[str, Any]:
    return dict((skill.metadata or {}).get("lifecycle") or {})


def decide_lifecycle(
    skill: Skill,
    *,
    task_clock: int = 0,
    config: SkillConfig | None = None,
    previous_su: float | None = None,
    expected_su: float | None = None,
) -> LifecycleDecision:
    """Decide next lifecycle action from current state and streaks."""
    del expected_su  # reserved for reactivation callers
    config = config or SkillConfig()
    metrics = compute_lifecycle_metrics(
        skill, task_clock=task_clock, config=config, previous_su=previous_su
    )
    health = metrics.health or compute_health(skill, config)
    life = _life(skill)
    state = skill.state
    su = metrics.su
    ug = metrics.ug
    tracked_age = int(life.get("age_tasks", 0) or 0) + 1
    # Never use absolute task_clock as age. Prefer tracked counter; allow
    # metrics.sa only when birth_task anchors relative age.
    if "birth_task" in (skill.metadata or {}):
        age_tasks = max(tracked_age, int(metrics.sa))
    else:
        age_tasks = tracked_age
    patch: dict[str, Any] = {
        "previous_su": su,
        "age_tasks": age_tasks,
    }

    # Update streaks
    low_su = int(life.get("low_su_streak", 0) or 0)
    pos_ug = int(life.get("positive_ug_streak", 0) or 0)
    if su < config.su_min:
        low_su += 1
    else:
        low_su = 0
    if ug > config.growing_ug:
        pos_ug += 1
    elif ug < -config.growing_ug:
        pos_ug = 0
    patch["low_su_streak"] = low_su
    patch["positive_ug_streak"] = pos_ug

    idle = tasks_since_use(skill, task_clock)
    if "tasks_since_use" not in life and task_clock:
        idle = tasks_since_use(skill, task_clock)
    patch.setdefault("tasks_since_use", idle)

    # Retired → Archived
    if state is SkillState.RETIRED:
        retired_tasks = int(life.get("retired_tasks", 0) or 0) + 1
        patch["retired_tasks"] = retired_tasks
        if retired_tasks >= config.archive_after_tasks:
            return LifecycleDecision(
                action="archive",
                target_state=SkillState.ARCHIVED,
                reasons=["archive_after_tasks"],
                metrics=metrics,
                health=health,
                lifecycle_patch=patch,
            )
        return LifecycleDecision(
            action="keep",
            target_state=None,
            reasons=["retired_waiting"],
            metrics=metrics,
            health=health,
            lifecycle_patch=patch,
        )

    if state is SkillState.ARCHIVED:
        return LifecycleDecision(
            action="keep",
            target_state=None,
            reasons=["archived"],
            metrics=metrics,
            health=health,
            lifecycle_patch=patch,
        )

    # Retirement (anti-premature + economic gates)
    age = int(patch["age_tasks"])
    reuse = int(skill.reuse_count or 0)
    ts = float(skill.transfer_score or 0.0)
    can_retire = (
        state in ACTIVE_TIER | {SkillState.DORMANT}
        and low_su >= config.retire_low_su_periods
        and reuse <= config.retire_max_reuse
        and ts <= config.retire_max_ts
        and age >= config.retire_min_age_tasks
    )
    if can_retire:
        return LifecycleDecision(
            action="retire",
            target_state=SkillState.RETIRED,
            reasons=["low_su_streak", "low_reuse", "low_ts", "age_ok"],
            metrics=metrics,
            health=health,
            lifecycle_patch=patch,
        )

    # Dormancy: unused but still useful
    if (
        state in ACTIVE_TIER
        and idle >= config.dormant_after_tasks
        and su >= config.su_min
    ):
        return LifecycleDecision(
            action="dormant",
            target_state=SkillState.DORMANT,
            reasons=["tasks_since_use"],
            metrics=metrics,
            health=health,
            lifecycle_patch=patch,
        )

    # Dormant wake is evidence-driven (reactivate_skill); keep here.
    if state is SkillState.DORMANT:
        return LifecycleDecision(
            action="keep",
            target_state=None,
            reasons=["dormant"],
            metrics=metrics,
            health=health,
            lifecycle_patch=patch,
        )

    # Core promotion
    nr = compute_nr(skill, config)
    transfer_ok = ts >= config.core_min_transfer
    if state is SkillState.GROWING and (
        su >= config.core_su
        and transfer_ok
        and reuse >= config.core_min_reuse
        and nr <= config.ntr_limit
        and pos_ug >= config.core_growth_periods
    ):
        patch["capability_anchor"] = True
        return LifecycleDecision(
            action="core",
            target_state=SkillState.CORE,
            reasons=["core_criteria"],
            metrics=metrics,
            health=health,
            lifecycle_patch=patch,
        )

    # Decline from Growing/Core → Active on negative UG
    if state in (SkillState.GROWING, SkillState.CORE) and ug < -config.growing_ug:
        return LifecycleDecision(
            action="decline",
            target_state=SkillState.ACTIVE,
            reasons=["negative_ug"],
            metrics=metrics,
            health=health,
            lifecycle_patch=patch,
        )

    # Active → Growing on positive UG
    if state is SkillState.ACTIVE and ug > config.growing_ug:
        return LifecycleDecision(
            action="grow",
            target_state=SkillState.GROWING,
            reasons=["positive_ug"],
            metrics=metrics,
            health=health,
            lifecycle_patch=patch,
        )

    return LifecycleDecision(
        action="keep",
        target_state=None,
        reasons=["stable"],
        metrics=metrics,
        health=health,
        lifecycle_patch=patch,
    )
