"""Lifecycle metrics SA / SU / UG / RF / TS / HS (Phase 11D-3)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.skill import Skill
from skills.config import SkillConfig
from skills.lifecycle.aging import last_used_index, recency_weight, tasks_since_use
from skills.lifecycle.health import HealthScore, apply_recency, compute_health
from skills.utility import compute_su


@dataclass(slots=True)
class LifecycleMetrics:
    """Per-skill lifecycle snapshot."""

    sa: float = 0.0  # skill age (task ticks)
    su: float = 0.0
    ug: float = 0.0  # utility growth
    rf: float = 0.0  # reuse frequency = reuse / age
    ts: float = 0.0
    hs: float = 0.0
    health: HealthScore | None = None

    def to_dict(self) -> dict[str, Any]:
        out: dict[str, Any] = {
            "sa": self.sa,
            "su": self.su,
            "ug": self.ug,
            "rf": self.rf,
            "ts": self.ts,
            "hs": self.hs,
        }
        if self.health is not None:
            out["health"] = self.health.to_dict()
        return out


def compute_lifecycle_metrics(
    skill: Skill,
    *,
    task_clock: int = 0,
    config: SkillConfig | None = None,
    previous_su: float | None = None,
) -> LifecycleMetrics:
    """Compute SA/SU/UG/RF/TS/HS for a skill at task_clock."""
    config = config or SkillConfig()
    meta = skill.metadata or {}
    life = dict(meta.get("lifecycle") or {})
    # Prefer explicit lifecycle age; only derive from clock when birth_task set.
    if "age_tasks" in life:
        sa = max(0.0, float(life["age_tasks"]))
    elif "birth_task" in meta:
        try:
            birth_i = int(meta["birth_task"])
        except (TypeError, ValueError):
            birth_i = 0
        sa = max(0.0, float(task_clock) - float(birth_i))
    else:
        sa = float(max(0, last_used_index(skill)))

    su = float(
        skill.utility
        if meta.get("utility_breakdown")
        else compute_su(skill, config)
    )
    if previous_su is None:
        prev = (meta.get("utility_breakdown") or {}).get("su")
        if prev is not None and float(prev) != su:
            previous_su = float(prev)
        else:
            life = dict(meta.get("lifecycle") or {})
            if "previous_su" in life:
                previous_su = float(life["previous_su"])
            else:
                previous_su = su
    ug = su - float(previous_su)
    age_for_rf = sa if sa > 0 else 1.0
    rf = float(skill.reuse_count or 0) / age_for_rf
    ts = float(skill.transfer_score or 0.0)

    health = compute_health(skill, config)
    t_idle = tasks_since_use(skill, task_clock)
    rw = recency_weight(t_idle, config)
    health = apply_recency(health, rw)

    return LifecycleMetrics(
        sa=sa, su=su, ug=ug, rf=rf, ts=ts, hs=health.value, health=health
    )
