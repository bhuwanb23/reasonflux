"""Skill Creation Trigger — SCV gate (Phase 11D-1).

SCV = Reuse × AG × TS − CreationCost
Create if SCV > skill_creation_threshold.
"""

from __future__ import annotations

from core.skill import SkillCandidate, compute_scv
from skills.config import SkillConfig


class SkillCreationTrigger:
    """Decide whether a skill candidate should be promoted."""

    def __init__(self, config: SkillConfig | None = None) -> None:
        self.config = config or SkillConfig()

    def compute_scv(self, candidate: SkillCandidate) -> float:
        """Compute SCV for a candidate (delegates to core formula)."""
        reuse = candidate.reuse if candidate.reuse else candidate.expected_reuse
        ts = (
            candidate.transfer_score
            if candidate.transfer_score
            else candidate.expected_transfer
        )
        return compute_scv(
            reuse, candidate.abstraction_gain, ts, candidate.creation_cost
        )

    def should_create(
        self, candidate: SkillCandidate, *, strict: bool = False
    ) -> bool:
        """True when SCV exceeds the configured creation threshold."""
        scv = self.compute_scv(candidate)
        threshold = (
            self.config.skill_creation_threshold_strict
            if strict
            else self.config.skill_creation_threshold
        )
        return scv > threshold

    def threshold(self, *, strict: bool = False) -> float:
        if strict:
            return self.config.skill_creation_threshold_strict
        return self.config.skill_creation_threshold
