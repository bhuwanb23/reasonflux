"""Skill-related metrics (SU) for SCT evaluation (Phase 11D-2)."""

from __future__ import annotations

from core.skill import Skill
from skills.config import SkillConfig
from skills.utility import compute_su as _compute_su
from skills.utility import score_skill_utility
from skills.utility_components import SkillUtilityBreakdown


def compute_su(skill: Skill, config: SkillConfig | None = None) -> float:
    """Compute Skill Utility: (RCG+TV+CP+RV) − (CC+MC+NR)."""
    return _compute_su(skill, config)


def skill_utility_breakdown(
    skill: Skill, config: SkillConfig | None = None
) -> SkillUtilityBreakdown:
    """Return the full SU component breakdown."""
    return score_skill_utility(skill, config)
