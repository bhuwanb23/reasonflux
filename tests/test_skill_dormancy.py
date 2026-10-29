"""Dormancy after unused tasks; stays in memory; not retrieved."""

from core import Skill, SkillState
from skills import (
    SkillConfig,
    SkillLibrary,
    apply_lifecycle,
    evaluate_lifecycle,
    refresh_skill_utility,
    retrieve_skills,
)


def test_dormant_after_unused_tasks_not_retrieved():
    skill = Skill(
        skill_id="d1",
        abstraction_gain=0.6,
        transfer_score=0.5,
        creation_cost=0.05,
        reuse_count=3,
        reuse_history=[{"impact": 1.0}] * 3,
        state=SkillState.ACTIVE,
        metadata={
            "composition_potential": 0.4,
            "lifecycle": {"tasks_since_use": 10, "age_tasks": 15},
        },
    )
    refresh_skill_utility(skill)
    cfg = SkillConfig(dormant_after_tasks=10, su_min=0.0, growing_ug=0.5)
    decision = evaluate_lifecycle(skill, task_clock=20, config=cfg)
    assert decision.action == "dormant"
    apply_lifecycle(skill, decision, config=cfg)
    assert skill.state is SkillState.DORMANT

    lib = SkillLibrary()
    lib.add(skill)
    assert lib.get("d1") is not None
    hits = retrieve_skills(lib)
    assert hits == []
    # state=None returns all skills (including dormant); default is active-tier.
    assert retrieve_skills(lib, state=None) == [skill]
    assert lib.list_skills(state=SkillState.DORMANT) == [skill]
