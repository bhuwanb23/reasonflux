"""SF2 skill explosion ratio and capacity enforcement."""

from core import Skill, SkillState
from skills import SkillLibrary, SkillRobustnessConfig
from skills.robustness.sf_creation import (
    enforce_library_capacity,
    ser_level,
    should_restrict_skill_promotion,
)


def test_ser_levels():
    cfg = SkillRobustnessConfig(ser_warn=0.5, ser_restrict=0.8)
    assert ser_level(1, 10, cfg) == "ok"
    assert ser_level(6, 10, cfg) == "warn"
    assert ser_level(9, 10, cfg) == "restrict"
    assert should_restrict_skill_promotion(0.9, cfg)


def test_capacity_enforcement_retires_weakest_keeps_core():
    cfg = SkillRobustnessConfig(library_capacity=2)
    lib = SkillLibrary()
    core = Skill(skill_id="core", state=SkillState.CORE, utility=1.0, reuse_count=9)
    weak = Skill(skill_id="weak", state=SkillState.ACTIVE, utility=0.0, reuse_count=0)
    mid = Skill(skill_id="mid", state=SkillState.ACTIVE, utility=0.3, reuse_count=1)
    for s in (core, weak, mid):
        lib.add(s)

    retired = enforce_library_capacity(lib, cfg)
    assert len(lib) == 3  # retired ≠ deleted
    assert core.state is SkillState.CORE
    assert weak.state is SkillState.RETIRED
    assert [s.skill_id for s in retired] == ["weak"]
