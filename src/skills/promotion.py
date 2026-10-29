"""Stage 5–6 — promote SkillCandidate to Active Skill (Phase 11D-1)."""

from __future__ import annotations

from dataclasses import dataclass, field

from core.invariant import Invariant
from core.skill import Skill, SkillCandidate
from core.states import SkillState
from skills.birth import SkillBirthRecord, make_birth_record
from skills.config import SkillConfig
from skills.evidence import (
    SkillEvidence,
    compute_skill_confidence,
    seed_evidence_from_invariant,
)
from skills.intake import intake_invariant
from skills.library import SkillLibrary
from skills.qualification import QualificationResult, qualify_candidate
from skills.trigger import SkillCreationTrigger
from skills.utility import refresh_skill_utility


@dataclass(slots=True)
class PromotionResult:
    """Result of attempting skill promotion."""

    promoted: bool
    skill: Skill | None = None
    birth: SkillBirthRecord | None = None
    reasons: list[str] = field(default_factory=list)
    qualification: QualificationResult | None = None

    def to_dict(self) -> dict:
        return {
            "promoted": self.promoted,
            "skill": self.skill.to_dict() if self.skill else None,
            "birth": self.birth.to_dict() if self.birth else None,
            "reasons": list(self.reasons),
            "qualification": (
                self.qualification.to_dict() if self.qualification else None
            ),
        }


def promote_skill(
    candidate: SkillCandidate,
    *,
    invariant: Invariant,
    library: SkillLibrary | None = None,
    config: SkillConfig | None = None,
    ntr: float = 0.0,
    skill_id: str | None = None,
) -> PromotionResult:
    """Qualify, instantiate, emit birth event, and store in the library."""
    config = config or SkillConfig()
    if library is None:
        library = SkillLibrary()

    intake = intake_invariant(invariant, config)
    if not intake.accepted:
        return PromotionResult(promoted=False, reasons=list(intake.reasons))

    qualification = qualify_candidate(
        candidate,
        invariant=invariant,
        library=library,
        config=config,
        ntr=ntr,
    )
    if not qualification.qualified:
        return PromotionResult(
            promoted=False,
            reasons=list(qualification.reasons),
            qualification=qualification,
        )

    trigger = SkillCreationTrigger(config)
    scv = trigger.compute_scv(candidate)
    candidate.scv = scv

    skill = Skill.from_candidate(candidate, skill_id=skill_id)
    skill.reuse_count = 0  # expected reuse is economic; count starts at birth
    if skill.state is SkillState.PROMOTED:
        skill.transition_to(SkillState.ACTIVE)

    transfer_events = 0
    if invariant.evidence is not None:
        transfer_events = int(invariant.evidence.transfer_events or 0)
    evidence = seed_evidence_from_invariant(
        invariant_id=invariant.invariant_id,
        frequency=invariant.frequency,
        consistency=invariant.consistency,
        transfer_score=candidate.transfer_score or candidate.expected_transfer,
        transfer_events=transfer_events,
    )
    confidence = compute_skill_confidence(evidence)
    skill.metadata = dict(skill.metadata or {})
    skill.metadata["evidence"] = evidence.to_dict()
    skill.metadata["confidence"] = confidence
    skill.metadata["status"] = "active"
    skill.transfer_history = list(evidence.transfer)

    birth = make_birth_record(
        skill_id=skill.skill_id,
        source_invariant_id=invariant.invariant_id,
        scv=scv,
        transfer_score=skill.transfer_score,
        evidence=evidence.to_dict(),
        transfer_history=list(skill.transfer_history),
        reasons=["scv", "transfer", "evidence", "ntr"],
    )
    skill.metadata["birth"] = birth.to_dict()
    refresh_skill_utility(skill, config)

    library.add(skill)
    return PromotionResult(
        promoted=True,
        skill=skill,
        birth=birth,
        reasons=[],
        qualification=qualification,
    )
