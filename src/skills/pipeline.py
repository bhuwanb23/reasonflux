"""End-to-end SCT pipeline: promotable invariants → skills (11D-1)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from core.invariant import Invariant
from core.skill import Skill
from skills.birth import SkillBirthRecord
from skills.candidate import from_invariant
from skills.config import SkillConfig
from skills.intake import intake_invariant
from skills.library import SkillLibrary
from skills.promotion import promote_skill


@dataclass(slots=True)
class SkillCreationStatistics:
    candidates_in: int = 0
    promoted: int = 0
    rejected: int = 0

    def to_dict(self) -> dict:
        return {
            "candidates_in": self.candidates_in,
            "promoted": self.promoted,
            "rejected": self.rejected,
        }


@dataclass(slots=True)
class SkillCreationResult:
    promoted: list[Skill] = field(default_factory=list)
    rejected: list[tuple[Invariant, list[str]]] = field(default_factory=list)
    birth_records: list[SkillBirthRecord] = field(default_factory=list)
    library: SkillLibrary | None = None
    statistics: SkillCreationStatistics = field(
        default_factory=SkillCreationStatistics
    )

    def to_dict(self) -> dict:
        return {
            "promoted": [s.to_dict() for s in self.promoted],
            "rejected": [
                {"invariant": inv.to_dict(), "reasons": list(reasons)}
                for inv, reasons in self.rejected
            ],
            "birth_records": [b.to_dict() for b in self.birth_records],
            "statistics": self.statistics.to_dict(),
        }


def create_skills_from_invariants(
    promotable: Sequence[Invariant],
    *,
    library: SkillLibrary | None = None,
    config: SkillConfig | None = None,
    ntr_by_invariant: dict[str, float] | None = None,
    allow_prior_evidence: bool = False,
) -> SkillCreationResult:
    """Run intake → candidate → qualify → promote for each invariant."""
    config = config or SkillConfig()
    if library is None:
        library = SkillLibrary()
    ntr_by_invariant = ntr_by_invariant or {}

    promoted: list[Skill] = []
    rejected: list[tuple[Invariant, list[str]]] = []
    births: list[SkillBirthRecord] = []

    for inv in promotable:
        intake = intake_invariant(inv, config, allow_prior_evidence=allow_prior_evidence)
        if not intake.accepted:
            rejected.append((inv, list(intake.reasons)))
            continue
        candidate = from_invariant(
            inv, config=config, allow_prior_transfer=allow_prior_evidence
        )
        result = promote_skill(
            candidate,
            invariant=inv,
            library=library,
            config=config,
            ntr=float(ntr_by_invariant.get(inv.invariant_id, 0.0)),
            allow_prior_evidence=allow_prior_evidence,
        )
        if result.promoted and result.skill is not None:
            promoted.append(result.skill)
            if result.birth is not None:
                births.append(result.birth)
        else:
            rejected.append((inv, list(result.reasons)))

    stats = SkillCreationStatistics(
        candidates_in=len(promotable),
        promoted=len(promoted),
        rejected=len(rejected),
    )
    return SkillCreationResult(
        promoted=promoted,
        rejected=rejected,
        birth_records=births,
        library=library,
        statistics=stats,
    )
