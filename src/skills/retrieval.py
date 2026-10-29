"""Skill retrieval by trigger conditions with SU ranking (Phase 11D-2/3)."""

from __future__ import annotations

from typing import Sequence

from core.skill import Skill
from core.states import SkillState
from skills.config import SkillConfig
from skills.library import SkillLibrary
from skills.utility import compute_su

# Active-tier states are eligible for default retrieval (not dormant/retired).
RETRIEVABLE_STATES = frozenset(
    {SkillState.ACTIVE, SkillState.GROWING, SkillState.CORE}
)
_DEFAULT = object()  # sentinel: default active-tier; None means all states


def retrieve_skills(
    library: SkillLibrary,
    conditions: Sequence[str] | None = None,
    *,
    state: SkillState | frozenset[SkillState] | None | object = _DEFAULT,
    rank_by: str = "utility",
    config: SkillConfig | None = None,
) -> list[Skill]:
    """Return matching skills ranked by utility (default) or confidence.

    Default ``state`` is the active tier (ACTIVE/GROWING/CORE). Pass
    ``state=None`` for all skills, an explicit ``SkillState``, or a set of
    states.
    """
    config = config or SkillConfig()
    if state is _DEFAULT:
        skills = [s for s in library.list_skills() if s.state in RETRIEVABLE_STATES]
    elif state is None:
        skills = library.list_skills()
    elif isinstance(state, (frozenset, set)):
        skills = [s for s in library.list_skills() if s.state in state]
    else:
        skills = library.list_skills(state=state)  # type: ignore[arg-type]
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
                -float((s.metadata or {}).get("retrieval_boost", 0.0) or 0.0),
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
                )
                - float((s.metadata or {}).get("retrieval_boost", 0.0) or 0.0),
                -float((s.metadata or {}).get("confidence", 0.0) or 0.0),
                s.skill_id,
            )
        )
    return skills
