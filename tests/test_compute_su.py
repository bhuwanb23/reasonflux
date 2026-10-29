"""compute_su and refresh_skill_utility."""

import pytest

from core import Skill, SkillState
from evaluation import compute_su
from skills import SkillConfig, refresh_skill_utility, score_skill_utility


def test_su_formula_and_refresh():
    skill = Skill(
        skill_id="sk",
        abstraction_gain=0.8,
        transfer_score=0.7,
        creation_cost=0.1,
        reuse_count=5,
        reuse_history=[{"impact": 1.0}] * 5,
        transfer_history=[
            {"success": True, "target_family": "a"},
            {"success": True, "target_family": "b"},
        ],
        state=SkillState.ACTIVE,
        metadata={"mvp_category": "reflection", "composition_potential": 0.5},
    )
    breakdown = score_skill_utility(skill, SkillConfig())
    assert breakdown.su == pytest.approx(
        (breakdown.rcg + breakdown.tv + breakdown.cp + breakdown.rv)
        - (breakdown.cc + breakdown.mc + breakdown.nr)
    )
    assert compute_su(skill) == pytest.approx(breakdown.su)

    refresh_skill_utility(skill)
    assert skill.utility == pytest.approx(breakdown.su)
    assert "utility_breakdown" in skill.metadata
    assert "economic_status" in skill.metadata
