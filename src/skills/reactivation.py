"""Evidence-gated skill reactivation with zombie guard (Phase 11D-3)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.skill import Skill
from core.states import SkillState
from skills.config import SkillConfig
from skills.lifecycle.biography import append_biography_event
from skills.utility import refresh_skill_utility

ELIGIBLE = frozenset(
    {SkillState.RETIRED, SkillState.ARCHIVED, SkillState.DORMANT}
)


@dataclass(slots=True)
class ReactivationResult:
    """Outcome of a reactivation attempt."""

    success: bool
    skill: Skill
    reasons: list[str] = field(default_factory=list)
    blocked_zombie: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "success": self.success,
            "skill_id": self.skill.skill_id,
            "state": self.skill.state.value,
            "reasons": list(self.reasons),
            "blocked_zombie": self.blocked_zombie,
        }


def reactivate_skill(
    skill: Skill,
    *,
    evidence_count: int,
    expected_su: float,
    config: SkillConfig | None = None,
    task_clock: int = 0,
) -> ReactivationResult:
    """Revive RETIRED/ARCHIVED/DORMANT → ACTIVE when evidence gates pass."""
    config = config or SkillConfig()
    min_su = (
        config.reactivate_min_expected_su
        if config.reactivate_min_expected_su is not None
        else config.su_min
    )
    reasons: list[str] = []

    if skill.state not in ELIGIBLE:
        return ReactivationResult(
            success=False,
            skill=skill,
            reasons=[f"state_not_eligible:{skill.state.value}"],
        )

    if int(evidence_count) < int(config.reactivate_min_evidence):
        reasons.append("insufficient_evidence")
    if float(expected_su) < float(min_su):
        reasons.append("expected_su_too_low")

    meta = dict(skill.metadata or {})
    attempts = int(meta.get("reactivations", 0) or 0)
    last = dict(meta.get("last_reactivation") or {})
    raised = bool(last.get("raised_utility", False))
    zombie = (
        attempts >= int(config.reactivate_max_attempts) and not raised
    )
    if zombie:
        return ReactivationResult(
            success=False,
            skill=skill,
            reasons=["zombie_guard"],
            blocked_zombie=True,
        )

    if reasons:
        return ReactivationResult(success=False, skill=skill, reasons=reasons)

    prior_su = float(skill.utility or 0.0)
    skill.transition_to(SkillState.ACTIVE)
    attempts += 1
    meta["reactivations"] = attempts
    life = dict(meta.get("lifecycle") or {})
    life["tasks_since_use"] = 0
    life["low_su_streak"] = 0
    life["retired_tasks"] = 0
    life["reactivated_at"] = int(task_clock)
    meta["lifecycle"] = life
    meta["last_reactivation"] = {
        "task_clock": int(task_clock),
        "expected_su": float(expected_su),
        "evidence_count": int(evidence_count),
        "prior_su": prior_su,
        "raised_utility": False,  # set True by monitoring after proof
    }
    skill.metadata = meta
    append_biography_event(
        skill,
        "reactivated",
        {
            "task_clock": int(task_clock),
            "expected_su": float(expected_su),
            "evidence_count": int(evidence_count),
            "attempt": attempts,
        },
    )
    refresh_skill_utility(skill, config)
    # raised_utility stays False until monitoring proves SU improved;
    # zombie guard then blocks further revivals after max attempts.
    del prior_su  # retained in last_reactivation for later comparison

    return ReactivationResult(
        success=True, skill=skill, reasons=["reactivated"]
    )
