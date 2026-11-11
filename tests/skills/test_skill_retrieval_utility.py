"""Retrieval sorts by utility by default."""

from core import Skill, SkillState
from skills import SkillLibrary, refresh_skill_utility, retrieve_skills


def test_retrieve_sorts_by_utility():
    lib = SkillLibrary()
    low = Skill(
        skill_id="low",
        trigger_conditions=["apply_reflection"],
        abstraction_gain=0.1,
        creation_cost=0.1,
        state=SkillState.ACTIVE,
    )
    high = Skill(
        skill_id="high",
        trigger_conditions=["apply_reflection"],
        abstraction_gain=0.9,
        transfer_score=0.8,
        creation_cost=0.05,
        reuse_count=5,
        reuse_history=[{"impact": 1.0}] * 5,
        transfer_history=[{"success": True, "target_family": "a"}],
        state=SkillState.ACTIVE,
        metadata={"composition_potential": 0.6, "mvp_category": "reflection"},
    )
    refresh_skill_utility(low)
    refresh_skill_utility(high)
    lib.add(low)
    lib.add(high)
    hits = retrieve_skills(lib, ["apply_reflection"])
    assert hits[0].skill_id == "high"
