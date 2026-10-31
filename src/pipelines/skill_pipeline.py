"""Skill pipeline — promotable invariants → skills (Phase 11, Phase C).

Thin orchestration over :func:`create_skills_from_invariants` (11D-1), adding
config loading and a pipeline-shaped result so Phase C is one call.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from core.invariant import Invariant
from core.skill import Skill
from skills.config import SkillConfig
from skills.library import SkillLibrary
from skills.pipeline import SkillCreationResult, create_skills_from_invariants

__all__ = ["SkillPipelineResult", "run_skill_pipeline"]


@dataclass(slots=True)
class SkillPipelineResult:
    """Promotion outcome plus the resulting library."""

    creation: SkillCreationResult | None = None
    library: SkillLibrary = field(default_factory=SkillLibrary)

    @property
    def promoted(self) -> list[Skill]:
        return list(self.creation.promoted) if self.creation else []

    @property
    def rejected(self) -> list[tuple[Invariant, list[str]]]:
        return list(self.creation.rejected) if self.creation else []

    def to_dict(self) -> dict[str, Any]:
        return {
            "n_promoted": len(self.promoted),
            "n_rejected": len(self.rejected),
            "promoted": [s.to_dict() for s in self.promoted],
            "rejected": [
                {"invariant_id": inv.invariant_id, "reasons": list(reasons)}
                for inv, reasons in self.rejected
            ],
            "library_size": len(self.library),
        }


def run_skill_pipeline(
    promotable: Sequence[Invariant],
    *,
    library: SkillLibrary | None = None,
    config: SkillConfig | None = None,
    ntr_by_invariant: dict[str, float] | None = None,
) -> SkillPipelineResult:
    """Promote each promotable invariant into a skill when SCV justifies it."""
    lib = library or SkillLibrary()
    creation = create_skills_from_invariants(
        list(promotable),
        library=lib,
        config=config or SkillConfig(),
        ntr_by_invariant=ntr_by_invariant,
    )
    return SkillPipelineResult(creation=creation, library=lib)
