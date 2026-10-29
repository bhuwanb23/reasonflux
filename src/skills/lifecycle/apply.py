"""Apply lifecycle decisions — single write path for biography (Phase 11D-3)."""

from __future__ import annotations

from core.skill import Skill
from core.states import SkillState
from skills.config import SkillConfig
from skills.lifecycle.biography import append_biography_event
from skills.lifecycle.policy import LifecycleDecision, decide_lifecycle
from skills.utility import refresh_skill_utility

_ACTION_KIND = {
    "grow": "growth",
    "core": "core",
    "decline": "decline",
    "dormant": "dormant",
    "retire": "retired",
    "archive": "archived",
}


def evaluate_lifecycle(
    skill: Skill,
    *,
    task_clock: int = 0,
    config: SkillConfig | None = None,
    previous_su: float | None = None,
    expected_su: float | None = None,
) -> LifecycleDecision:
    """Decide lifecycle action without mutating state (metrics patch only)."""
    return decide_lifecycle(
        skill,
        task_clock=task_clock,
        config=config,
        previous_su=previous_su,
        expected_su=expected_su,
    )


def apply_lifecycle(
    skill: Skill,
    decision: LifecycleDecision,
    *,
    config: SkillConfig | None = None,
) -> Skill:
    """Apply decision: transition, lifecycle metadata, biography, SU refresh."""
    config = config or SkillConfig()
    meta = dict(skill.metadata or {})
    life = dict(meta.get("lifecycle") or {})
    life.update(decision.lifecycle_patch or {})
    if decision.action == "core":
        meta["capability_anchor"] = True
        life["capability_anchor"] = True
    if decision.action == "retire":
        life["retired_tasks"] = int(life.get("retired_tasks", 0) or 0)
    meta["lifecycle"] = life
    if decision.metrics is not None:
        meta["lifecycle_metrics"] = decision.metrics.to_dict()
    if decision.health is not None:
        meta["health"] = decision.health.to_dict()
    skill.metadata = meta

    if (
        decision.target_state is not None
        and decision.target_state is not skill.state
    ):
        skill.transition_to(decision.target_state)
        kind = _ACTION_KIND.get(decision.action, decision.action)
        append_biography_event(
            skill,
            kind,
            {
                "action": decision.action,
                "state": decision.target_state.value,
                "reasons": list(decision.reasons),
            },
        )
    elif decision.action == "keep":
        # Still persist streak/age updates without a transition event.
        pass

    refresh_skill_utility(skill, config)
    return skill
