"""Edge cases EC1–EC4."""

from core import Skill, SkillState
from skills import SkillLibrary, SkillRobustnessConfig
from skills.robustness.edge_cases import (
    detect_cannibalization,
    enforce_zombie_archive,
    is_ancient_core,
    rare_high_value_override,
)
from skills.robustness.gates import evaluate_skill_retirement_gate


def test_ec1_rare_high_value_override():
    cfg = SkillRobustnessConfig(transfer_override_min=0.7)
    rare = Skill(skill_id="rare", state=SkillState.ACTIVE, transfer_score=0.85)
    assert rare_high_value_override(rare, cfg)
    weak = Skill(skill_id="weak", state=SkillState.ACTIVE, transfer_score=0.2)
    assert not rare_high_value_override(weak, cfg)


def test_ec2_ancient_core_protected_from_retirement():
    cfg = SkillRobustnessConfig(ancient_core_min_age=50)
    skill = Skill(
        skill_id="ancient",
        state=SkillState.CORE,
        utility=0.0,
        transfer_score=0.0,
        reuse_count=1,
        metadata={
            "lifecycle": {"age_tasks": 80},
            "biography": {"peak_utility": {"utility": 0.9, "reuse": 12}},
        },
    )
    assert is_ancient_core(skill, cfg)
    gate = evaluate_skill_retirement_gate(skill, config=cfg)
    assert not gate.promotable
    assert "ancient_core" in gate.reasons


def test_ec3_zombie_permanently_archived():
    cfg = SkillRobustnessConfig(zombie_permanent_archive_attempts=2)
    skill = Skill(
        skill_id="zombie",
        state=SkillState.RETIRED,
        metadata={
            "reactivations": 2,
            "last_reactivation": {"raised_utility": False},
        },
    )
    assert enforce_zombie_archive(skill, cfg)
    assert skill.state is SkillState.ARCHIVED
    assert skill.metadata["permanent_archive"] is True
    assert skill.metadata["zombie"] is True


def test_ec4_cannibalization_denied():
    cfg = SkillRobustnessConfig(cannibalization_ratio=0.5)
    core = Skill(
        skill_id="core",
        state=SkillState.CORE,
        utility=0.9,
        trigger_conditions=["reflect"],
    )
    weak = Skill(
        skill_id="weak",
        state=SkillState.ACTIVE,
        utility=0.2,
        trigger_conditions=["reflect"],
    )
    lib = SkillLibrary()
    lib.add(core)
    lib.add(weak)
    assert detect_cannibalization(weak, core, cfg)
    strong = Skill(
        skill_id="strong",
        state=SkillState.ACTIVE,
        utility=0.95,
        trigger_conditions=["reflect"],
    )
    assert not detect_cannibalization(strong, core, cfg)
