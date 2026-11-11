"""Composition trigger: compose only when SC < TR."""

from core import Skill, SkillState
from skills import SkillConfig, should_compose


def test_no_compose_when_single_skill_covers():
    skill = Skill(
        skill_id="reflect",
        state=SkillState.ACTIVE,
        trigger_conditions=["reflect", "count"],
    )
    result = should_compose(["reflect", "count"], [skill], SkillConfig())
    assert not result.should_compose
    assert "single_skill_covers" in result.reasons


def test_compose_when_no_single_skill_covers():
    a = Skill(
        skill_id="reflect",
        state=SkillState.ACTIVE,
        trigger_conditions=["reflect"],
    )
    b = Skill(
        skill_id="count",
        state=SkillState.ACTIVE,
        trigger_conditions=["count"],
    )
    result = should_compose(["reflect", "count"], [a, b], SkillConfig())
    assert result.should_compose
    assert "sc_lt_tr" in result.reasons
