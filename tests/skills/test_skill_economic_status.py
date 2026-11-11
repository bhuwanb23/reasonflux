"""Economic status classification."""

from core import Skill, SkillState
from skills import SkillConfig, classify_economic_status, refresh_skill_utility
from skills.utility_components import SkillUtilityBreakdown


def test_core_and_retirement_candidate():
    skill = Skill(
        skill_id="core",
        abstraction_gain=0.9,
        transfer_score=0.8,
        creation_cost=0.05,
        reuse_count=5,
        reuse_history=[{"impact": 1.0}] * 5,
        transfer_history=[
            {"success": True, "target_family": f"f{i}"} for i in range(4)
        ],
        state=SkillState.ACTIVE,
        metadata={"mvp_category": "reflection", "composition_potential": 0.7},
    )
    refresh_skill_utility(skill, SkillConfig())
    assert skill.metadata["economic_status"] == "core"

    weak = Skill(
        skill_id="weak",
        abstraction_gain=0.0,
        transfer_score=0.0,
        creation_cost=0.5,
        reuse_count=0,
        transfer_history=[
            {"success": False, "target_family": "x"},
            {"success": False, "target_family": "y"},
        ],
        state=SkillState.ACTIVE,
    )
    refresh_skill_utility(weak, SkillConfig(su_min=0.0))
    # High NR + high CC → negative SU → retirement_candidate
    assert weak.metadata["economic_status"] == "retirement_candidate"
    assert weak.metadata["retirement_candidate"] is True


def test_unproven_for_new_skill():
    skill = Skill(
        skill_id="new",
        abstraction_gain=0.4,
        transfer_score=0.4,
        creation_cost=0.1,
        reuse_count=0,
        state=SkillState.ACTIVE,
    )
    bd = SkillUtilityBreakdown(su=0.2)
    status = classify_economic_status(skill, bd, SkillConfig(core_su=0.6))
    assert status == "unproven"
