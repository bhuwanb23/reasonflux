"""Monitoring events refresh Skill.utility."""

from core import Skill, SkillState
from skills import record_reuse, record_transfer, refresh_skill_utility


def test_record_reuse_updates_utility():
    skill = Skill(
        skill_id="sk",
        abstraction_gain=0.5,
        creation_cost=0.05,
        reuse_count=0,
        state=SkillState.ACTIVE,
        metadata={"mvp_category": "reflection", "composition_potential": 0.4},
    )
    refresh_skill_utility(skill)
    before = skill.utility
    for i in range(5):
        record_reuse(skill, task_id=f"t{i}")
        record_transfer(
            skill,
            source_family="reflect",
            target_family=f"fam{i}",
            success=True,
            benefit=0.8,
        )
    assert skill.reuse_count == 5
    assert skill.utility >= before
    assert skill.metadata.get("utility_breakdown") is not None
