"""Skill competition — rank and soft-select by utility (Phase 11D-2)."""

from __future__ import annotations

from typing import Sequence

from core.skill import Skill
from skills.config import SkillConfig
from skills.utility import compute_su, refresh_skill_utility


def _utility_of(skill: Skill, config: SkillConfig) -> float:
    if (skill.metadata or {}).get("utility_breakdown") is not None:
        return float(skill.utility)
    return float(compute_su(skill, config))


def rank_by_utility(
    skills: Sequence[Skill],
    *,
    config: SkillConfig | None = None,
    refresh: bool = False,
) -> list[Skill]:
    """Return skills sorted by SU descending (ties by skill_id)."""
    config = config or SkillConfig()
    items = list(skills)
    if refresh:
        for skill in items:
            refresh_skill_utility(skill, config)
    items.sort(key=lambda s: (-_utility_of(s, config), s.skill_id))
    return items


def select_dominant(
    skills: Sequence[Skill],
    capacity: int | None = None,
    *,
    config: SkillConfig | None = None,
) -> list[Skill]:
    """Keep top-N skills by SU (soft capacity; no deletion)."""
    config = config or SkillConfig()
    cap = capacity if capacity is not None else config.library_capacity
    ranked = rank_by_utility(skills, config=config)
    return ranked[: max(0, int(cap))]
