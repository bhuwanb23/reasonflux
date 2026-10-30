"""SF4 negative transfer skills (Phase 11D-5)."""

from __future__ import annotations

from dataclasses import dataclass

from core.skill import Skill
from core.states import SkillState
from invariants.robustness.escalation import FailureLevel
from skills.lifecycle.biography import append_biography_event
from skills.library import SkillLibrary
from skills.robustness.config import SkillRobustnessConfig
from skills.robustness.metrics import skill_ntr


@dataclass(slots=True)
class TransferHealth:
    """NTR assessment and recommended action."""

    level: FailureLevel
    ntr: float
    action: str  # none | demote_retrieval | dormant | retire

    def to_dict(self) -> dict:
        return {
            "level": self.level.value,
            "ntr": self.ntr,
            "action": self.action,
        }


def assess_negative_transfer(
    skill: Skill, config: SkillRobustnessConfig | None = None
) -> TransferHealth:
    config = config or SkillRobustnessConfig()
    ntr = skill_ntr(skill)
    if ntr >= config.ntr_retire:
        return TransferHealth(FailureLevel.REJECTED, ntr, "retire")
    if ntr >= config.ntr_restrict:
        return TransferHealth(FailureLevel.RESTRICTED, ntr, "dormant")
    if ntr >= config.ntr_warn:
        return TransferHealth(FailureLevel.WARNING, ntr, "demote_retrieval")
    return TransferHealth(FailureLevel.OK, ntr, "none")


def apply_transfer_health(
    skill: Skill,
    health: TransferHealth,
    library: SkillLibrary | None = None,
) -> Skill:
    """Apply NTR ladder: demote retrieval priority → dormant → retire."""
    del library
    meta = dict(skill.metadata or {})
    meta["ntr"] = health.ntr
    meta["transfer_health"] = health.to_dict()
    if health.action == "demote_retrieval":
        meta["retrieval_boost"] = min(
            0.0, float(meta.get("retrieval_boost", 0.0) or 0.0) - 0.2
        )
        skill.metadata = meta
        append_biography_event(skill, "failure", {"kind": "ntr_warn", "ntr": health.ntr})
        return skill
    if health.action == "dormant":
        skill.metadata = meta
        if skill.state in (
            SkillState.ACTIVE,
            SkillState.GROWING,
            SkillState.CORE,
        ):
            skill.transition_to(SkillState.DORMANT)
            append_biography_event(
                skill, "dormant", {"reason": "ntr_restrict", "ntr": health.ntr}
            )
        return skill
    if health.action == "retire":
        skill.metadata = meta
        if skill.state not in (SkillState.RETIRED, SkillState.ARCHIVED):
            if skill.state is SkillState.CANDIDATE:
                skill.transition_to(SkillState.RETIRED)
            elif skill.state is SkillState.PROMOTED:
                skill.transition_to(SkillState.RETIRED)
            else:
                skill.transition_to(SkillState.RETIRED)
            append_biography_event(
                skill, "retired", {"reason": "ntr_retire", "ntr": health.ntr}
            )
        return skill
    skill.metadata = meta
    return skill
