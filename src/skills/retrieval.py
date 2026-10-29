"""Thin skill retrieval by trigger conditions (Phase 11D-1).

Full ranking / confidence-weighted retrieval expands in later 11D phases.
"""

from __future__ import annotations

from typing import Sequence

from core.skill import Skill
from core.states import SkillState
from skills.library import SkillLibrary


def retrieve_skills(
    library: SkillLibrary,
    conditions: Sequence[str] | None = None,
    *,
    state: SkillState | None = SkillState.ACTIVE,
) -> list[Skill]:
    """Return skills matching any trigger condition (simple overlap)."""
    skills = library.list_skills(state=state) if state else library.list_skills()
    if not conditions:
        return list(skills)
    wanted = {str(c).lower() for c in conditions if str(c).strip()}
    hits: list[Skill] = []
    for skill in skills:
        triggers = {str(t).lower() for t in skill.trigger_conditions}
        if wanted & triggers:
            hits.append(skill)
    hits.sort(
        key=lambda s: (
            -float((s.metadata or {}).get("confidence", 0.0) or 0.0),
            s.skill_id,
        )
    )
    return hits
