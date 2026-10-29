"""Skill robustness metrics re-export for evaluation (Phase 11D-5)."""

from __future__ import annotations

from core.skill import Skill
from skills.robustness.metrics import (
    capability_growth_rate,
    retrieval_recall,
    skill_explosion_ratio,
    skill_ntr,
    task_family_diversity,
)


def negative_transfer_rate(skill: Skill) -> float:
    """NTR of one skill."""
    return skill_ntr(skill)


__all__ = [
    "capability_growth_rate",
    "negative_transfer_rate",
    "retrieval_recall",
    "skill_explosion_ratio",
    "skill_ntr",
    "task_family_diversity",
]
