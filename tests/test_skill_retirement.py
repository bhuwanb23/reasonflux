"""Retirement gates, premature guard, library retention (Phase 11D-3)."""

from core import Skill, SkillState
from skills import (
    SkillConfig,
    SkillLibrary,
    refresh_skill_utility,
    retire_skills,
    retrieve_skills,
)


def _weak(*, skill_id: str, age: int, streak: int, reuse: int = 0) -> Skill:
    skill = Skill(
        skill_id=skill_id,
        abstraction_gain=0.0,
        transfer_score=0.0,
        creation_cost=1.0,
        reuse_count=reuse,
        state=SkillState.ACTIVE,
        metadata={
            "composition_potential": 0.0,
            "lifecycle": {
                "age_tasks": age,
                "low_su_streak": streak,
                "tasks_since_use": 0,
            },
        },
    )
    refresh_skill_utility(skill)
    return skill


def test_retire_when_gates_met_keeps_in_library():
    skill = _weak(skill_id="r1", age=19, streak=2, reuse=0)
    cfg = SkillConfig(
        su_min=0.0,
        retire_low_su_periods=3,
        retire_max_reuse=1,
        retire_max_ts=0.1,
        retire_min_age_tasks=20,
        dormant_after_tasks=100,
    )
    lib = SkillLibrary()
    lib.add(skill)
    changed = retire_skills([skill], task_clock=30, config=cfg, library=lib)
    assert changed and skill.state is SkillState.RETIRED
    assert lib.get("r1") is skill
    assert retrieve_skills(lib) == []


def test_premature_retirement_blocked_for_young_skills():
    skill = _weak(skill_id="r2", age=5, streak=5, reuse=0)
    cfg = SkillConfig(
        su_min=0.0,
        retire_low_su_periods=3,
        retire_min_age_tasks=20,
        dormant_after_tasks=100,
    )
    # Large absolute clock must not bypass retire_min_age_tasks.
    changed = retire_skills([skill], task_clock=1000, config=cfg)
    assert changed == []
    assert skill.state is SkillState.ACTIVE
    age = int((skill.metadata or {}).get("lifecycle", {}).get("age_tasks", 0))
    assert age < 20
