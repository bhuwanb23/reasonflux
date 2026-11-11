"""Evidence-gated revival and zombie guard (Phase 11D-3)."""

from core import Skill, SkillState
from skills import SkillConfig, reactivate_skill, refresh_skill_utility


def test_reactivate_with_evidence():
    skill = Skill(
        skill_id="x1",
        state=SkillState.RETIRED,
        utility=0.0,
        metadata={"reactivations": 0},
    )
    refresh_skill_utility(skill)
    cfg = SkillConfig(reactivate_min_evidence=2, reactivate_min_expected_su=0.0)
    result = reactivate_skill(
        skill, evidence_count=2, expected_su=0.5, config=cfg, task_clock=10
    )
    assert result.success
    assert skill.state is SkillState.ACTIVE
    assert skill.metadata["reactivations"] == 1
    assert skill.metadata["biography"]["reactivations"]


def test_zombie_guard_blocks_repeat_revival():
    skill = Skill(
        skill_id="x2",
        state=SkillState.ARCHIVED,
        utility=0.1,
        metadata={
            "reactivations": 2,
            "last_reactivation": {"raised_utility": False},
        },
    )
    cfg = SkillConfig(
        reactivate_min_evidence=1,
        reactivate_min_expected_su=0.0,
        reactivate_max_attempts=2,
    )
    result = reactivate_skill(
        skill, evidence_count=5, expected_su=1.0, config=cfg
    )
    assert not result.success
    assert result.blocked_zombie
    assert skill.state is SkillState.ARCHIVED
