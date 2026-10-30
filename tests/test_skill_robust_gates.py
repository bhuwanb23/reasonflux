"""Robust promotion and retirement gates."""

from core import Skill, SkillState
from skills import SkillLibrary, SkillRobustnessConfig
from skills.robustness.gates import (
    evaluate_skill_promotion_gate,
    evaluate_skill_retirement_gate,
)


def _strong() -> Skill:
    return Skill(
        skill_id="strong",
        state=SkillState.ACTIVE,
        trigger_conditions=["reflect"],
        transfer_score=0.8,
        utility=0.6,
        reuse_count=4,
        metadata={
            "confidence": 0.9,
            "evidence": {
                "discovery": [{}, {}, {}],
                "utility": [{}, {}, {}],
                "transfer": [{}, {}, {}],
            },
        },
    )


def test_promotion_gate_passes_strong_skill():
    gate = evaluate_skill_promotion_gate(
        _strong(), library=SkillLibrary(), config=SkillRobustnessConfig(), ser=0.1
    )
    assert gate.promotable
    assert gate.reasons == []
    assert gate.level.value == "ok"


def test_promotion_gate_blocks_all_six_checks():
    cfg = SkillRobustnessConfig(
        min_evidence_promote=5,
        min_confidence_promote=0.9,
        min_utility_promote=0.8,
        ntr_warn=0.05,
        ntr_restrict=0.1,
        ntr_retire=0.6,
        ser_restrict=0.5,
        tfd_min_promote=0.9,
    )
    lib = SkillLibrary()
    lib.add(
        Skill(
            skill_id="dup",
            state=SkillState.ACTIVE,
            trigger_conditions=["reflect"],
        )
    )
    weak = Skill(
        skill_id="weak2",
        state=SkillState.ACTIVE,
        trigger_conditions=["reflect"],
        transfer_score=0.0,
        utility=0.0,
        metadata={"confidence": 0.1, "evidence": {"discovery": []}},
    )
    gate = evaluate_skill_promotion_gate(
        weak,
        library=lib,
        config=cfg,
        ser=0.9,
        families=["reflect"] * 10,
        tasks=10,
        ntr=0.5,
    )
    assert not gate.promotable
    for reason in ("evidence", "confidence", "utility", "ntr", "duplicate", "ser_restrict", "low_tfd"):
        assert reason in gate.reasons


def test_retirement_gate_blocks_premature_delete():
    cfg = SkillRobustnessConfig()
    useful = _strong()
    gate = evaluate_skill_retirement_gate(useful, config=cfg)
    assert not gate.promotable
    assert "utility_not_low" in gate.reasons


def test_retirement_gate_allows_weak_skill():
    cfg = SkillRobustnessConfig()
    weak = Skill(
        skill_id="w",
        state=SkillState.ACTIVE,
        utility=0.0,
        transfer_score=0.0,
        reuse_count=0,
    )
    gate = evaluate_skill_retirement_gate(weak, config=cfg)
    assert gate.promotable
