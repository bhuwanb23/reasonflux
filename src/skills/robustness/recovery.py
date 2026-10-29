"""Detect → Diagnose → Recover → Monitor (Phase 11D-5)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.skill import Skill
from core.states import SkillState
from skills.library import SkillLibrary
from skills.robustness.config import SkillRobustnessConfig
from skills.robustness.sf_creation import demote_skill
from skills.robustness.sf_retrieval import boost_retrieval
from skills.robustness.sf_transfer import apply_transfer_health, assess_negative_transfer
from skills.robustness.taxonomy import FailureDiagnosis, SkillFailure


@dataclass(slots=True)
class RecoveryAction:
    action: str  # demote | dormant | retire | archive | merge | boost | monitor
    failure: SkillFailure
    target_state: str | None = None
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "action": self.action,
            "failure": self.failure.value,
            "target_state": self.target_state,
            "notes": list(self.notes),
        }


def plan_recovery(
    diagnosis: FailureDiagnosis,
    config: SkillRobustnessConfig | None = None,
) -> RecoveryAction:
    """Map a diagnosis to a recovery action."""
    del config
    f = diagnosis.failure
    if f is SkillFailure.SF1:
        return RecoveryAction("demote", f, SkillState.CANDIDATE.value, ["requalify"])
    if f is SkillFailure.SF2:
        return RecoveryAction("retire", f, SkillState.RETIRED.value, ["capacity"])
    if f is SkillFailure.SF3:
        return RecoveryAction("merge", f, None, ["consolidate"])
    if f is SkillFailure.SF4:
        action = "retire"
        if "ntr_warn" in diagnosis.reasons:
            action = "boost"  # actually demote_retrieval; handled in apply
            return RecoveryAction("demote_retrieval", f, None, diagnosis.reasons)
        if "ntr_restrict" in diagnosis.reasons:
            action = "dormant"
        return RecoveryAction(action, f, SkillState.DORMANT.value if action == "dormant" else SkillState.RETIRED.value, diagnosis.reasons)
    if f is SkillFailure.SF5:
        return RecoveryAction("boost", f, None, ["retrieval_boost"])
    if f is SkillFailure.SF6:
        return RecoveryAction("monitor", f, None, ["reject_composition"])
    if f is SkillFailure.SF7:
        return RecoveryAction("retire", f, SkillState.RETIRED.value, ["prune_harmful"])
    if f is SkillFailure.SF8:
        return RecoveryAction("monitor", f, None, ["require_diversity"])
    if f is SkillFailure.EC3:
        return RecoveryAction("archive", f, SkillState.ARCHIVED.value, ["zombie"])
    if f is SkillFailure.EC2:
        return RecoveryAction("monitor", f, None, ["protect_core"])
    if f is SkillFailure.EC4:
        return RecoveryAction("monitor", f, None, ["deny_slot"])
    return RecoveryAction("monitor", f, None, list(diagnosis.reasons))


def apply_recovery(
    skill: Skill,
    action: RecoveryAction,
    library: SkillLibrary | None = None,
    config: SkillRobustnessConfig | None = None,
) -> Skill:
    """Execute recovery action on skill."""
    config = config or SkillRobustnessConfig()
    if action.action == "demote":
        return demote_skill(skill, library)
    if action.action == "demote_retrieval":
        health = assess_negative_transfer(skill, config)
        return apply_transfer_health(skill, health, library)
    if action.action == "dormant":
        if skill.state in (SkillState.ACTIVE, SkillState.GROWING, SkillState.CORE):
            skill.transition_to(SkillState.DORMANT)
        return skill
    if action.action == "retire":
        if skill.state not in (SkillState.RETIRED, SkillState.ARCHIVED):
            if skill.state in (
                SkillState.ACTIVE,
                SkillState.GROWING,
                SkillState.CORE,
                SkillState.DORMANT,
                SkillState.PROMOTED,
                SkillState.CANDIDATE,
            ):
                skill.transition_to(SkillState.RETIRED)
        return skill
    if action.action == "archive":
        if skill.state is SkillState.CORE:
            # CORE is protected from archival; retire via normal lifecycle.
            return skill
        if skill.state is SkillState.ACTIVE:
            skill.transition_to(SkillState.RETIRED)
        elif skill.state is SkillState.GROWING:
            skill.transition_to(SkillState.RETIRED)
        elif skill.state is SkillState.DORMANT:
            skill.transition_to(SkillState.RETIRED)
        elif skill.state is SkillState.PROMOTED:
            skill.transition_to(SkillState.RETIRED)
        elif skill.state is SkillState.CANDIDATE:
            skill.transition_to(SkillState.RETIRED)
        if skill.state is SkillState.RETIRED:
            skill.transition_to(SkillState.ARCHIVED)
        return skill
    if action.action == "boost":
        boost_retrieval(skill, config.retrieval_boost)
        return skill
    return skill
