"""Skill retirement — evaluate and apply retire/archive decisions (Phase 11D-3).

Retired skills remain in the library (no deletion).
"""

from __future__ import annotations

from typing import Sequence

from core.skill import Skill
from core.states import SkillState
from skills.config import SkillConfig
from skills.lifecycle.apply import apply_lifecycle
from skills.lifecycle.policy import decide_lifecycle
from skills.library import SkillLibrary


def retire_skills(
    skills: Sequence[Skill],
    *,
    task_clock: int = 0,
    config: SkillConfig | None = None,
    library: SkillLibrary | None = None,
) -> list[Skill]:
    """Evaluate each skill; apply retirement/archive decisions; return changed.

    Skills that retire stay in ``library`` when provided (never deleted).
    """
    config = config or SkillConfig()
    changed: list[Skill] = []
    for skill in skills:
        decision = decide_lifecycle(
            skill, task_clock=task_clock, config=config
        )
        if decision.action not in ("retire", "archive"):
            # Still persist streak counters for retirement eligibility.
            if decision.lifecycle_patch:
                meta = dict(skill.metadata or {})
                life = dict(meta.get("lifecycle") or {})
                life.update(decision.lifecycle_patch)
                meta["lifecycle"] = life
                skill.metadata = meta
            continue
        before = skill.state
        apply_lifecycle(skill, decision, config=config)
        if skill.state is not before:
            changed.append(skill)
            if library is not None and library.get(skill.skill_id) is None:
                # Ensure presence; never remove on retire.
                try:
                    library.add(skill)
                except ValueError:
                    pass
    return changed


def is_retired_or_archived(skill: Skill) -> bool:
    return skill.state in (SkillState.RETIRED, SkillState.ARCHIVED)
