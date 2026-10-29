"""Core criteria and capability_anchor flag (Phase 11D-3)."""

from core import Skill, SkillState
from skills import SkillConfig, apply_lifecycle, evaluate_lifecycle, refresh_skill_utility


def test_growing_to_core_sets_capability_anchor():
    skill = Skill(
        skill_id="c1",
        abstraction_gain=0.9,
        transfer_score=0.8,
        creation_cost=0.05,
        reuse_count=5,
        reuse_history=[{"impact": 1.0}] * 5,
        transfer_history=[
            {"success": True, "target_family": f"f{i}"} for i in range(3)
        ],
        state=SkillState.GROWING,
        metadata={
            "composition_potential": 0.6,
            "confidence": 0.8,
            "lifecycle": {"positive_ug_streak": 1},
        },
    )
    refresh_skill_utility(skill)
    cfg = SkillConfig(
        core_su=0.3,
        core_min_reuse=3,
        core_min_transfer=0.5,
        core_growth_periods=2,
        growing_ug=0.01,
    )
    # One more positive UG tick → streak reaches 2 and core criteria hold.
    decision = evaluate_lifecycle(
        skill, previous_su=skill.utility - 0.05, config=cfg
    )
    assert decision.action == "core"
    apply_lifecycle(skill, decision, config=cfg)
    assert skill.state is SkillState.CORE
    assert skill.metadata.get("capability_anchor") is True
