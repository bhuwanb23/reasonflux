"""Skill retrieval by trigger conditions with SU ranking (Phase 11D-2)."""

from __future__ import annotations

from typing import Sequence

from core.skill import Skill
from core.states import SkillState
from skills.config import SkillConfig
from skills.library import SkillLibrary
from skills.utility import compute_su


def retrieve_skills(
    library: SkillLibrary,
    conditions: Sequence[str] | None = None,
    *,
    state: SkillState | None = SkillState.ACTIVE,
    rank_by: str = "utility",
    config: SkillConfig | None = None,
) -> list[Skill]:
    """Return matching skills ranked by utility (default) or confidence."""
    config = config or SkillConfig()
    skills = library.list_skills(state=state) if state else library.list_skills()
    if conditions:
        wanted = {str(c).lower() for c in conditions if str(c).strip()}
        hits: list[Skill] = []
        for skill in skills:
            triggers = {str(t).lower() for t in skill.trigger_conditions}
            if wanted & triggers:
                hits.append(skill)
        skills = hits
    else:
        skills = list(skills)

    if rank_by == "confidence":
        skills.sort(
            key=lambda s: (
                -float((s.metadata or {}).get("confidence", 0.0) or 0.0),
                s.skill_id,
            )
        )
    else:
        skills.sort(
            key=lambda s: (
                -float(
                    s.utility
                    if (s.metadata or {}).get("utility_breakdown")
                    else compute_su(s, config)
                ),
                -float((s.metadata or {}).get("confidence", 0.0) or 0.0),
                s.skill_id,
            )
        )
    return skills
