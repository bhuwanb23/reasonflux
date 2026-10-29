"""Active → Growing on positive UG; decline returns to Active."""

from core import Skill, SkillState
from skills import SkillConfig, apply_lifecycle, evaluate_lifecycle, refresh_skill_utility


def _useful(**kwargs) -> Skill:
    base = dict(
        skill_id="g1",
        abstraction_gain=0.7,
        transfer_score=0.6,
        creation_cost=0.05,
        reuse_count=4,
        reuse_history=[{"impact": 1.0}] * 4,
        state=SkillState.ACTIVE,
        metadata={"composition_potential": 0.5, "lifecycle": {}},
    )
    base.update(kwargs)
    skill = Skill(**base)
    refresh_skill_utility(skill)
    return skill


def test_active_to_growing_on_positive_ug():
    skill = _useful()
    cfg = SkillConfig(growing_ug=0.02)
    decision = evaluate_lifecycle(skill, previous_su=skill.utility - 0.1, config=cfg)
    assert decision.action == "grow"
    assert decision.target_state is SkillState.GROWING
    apply_lifecycle(skill, decision, config=cfg)
    assert skill.state is SkillState.GROWING


def test_growing_declines_to_active_on_negative_ug():
    skill = _useful(state=SkillState.GROWING, skill_id="g2")
    cfg = SkillConfig(growing_ug=0.02)
    decision = evaluate_lifecycle(skill, previous_su=skill.utility + 0.2, config=cfg)
    assert decision.action == "decline"
    apply_lifecycle(skill, decision, config=cfg)
    assert skill.state is SkillState.ACTIVE
