"""SF8 adversarial formation (low task-family diversity)."""

from core import Skill, SkillState
from skills import SkillLibrary, SkillRobustnessConfig, evaluate_skill_promotion_gate
from skills.robustness.sf_capability import detect_adversarial_formation


def test_low_tfd_blocks_promotion():
    cfg = SkillRobustnessConfig(tfd_min_promote=0.4)
    risk = detect_adversarial_formation(["reflect"] * 10, tasks=10, config=cfg)
    assert risk.blocked
    assert risk.tfd == 0.1

    skill = Skill(
        skill_id="adv",
        state=SkillState.ACTIVE,
        transfer_score=0.8,
        utility=0.5,
        metadata={
            "confidence": 0.9,
            "evidence": {"discovery": [{}, {}, {}], "transfer": [], "utility": []},
        },
    )
    gate = evaluate_skill_promotion_gate(
        skill,
        library=SkillLibrary(),
        config=cfg,
        families=["reflect"] * 10,
        tasks=10,
    )
    assert not gate.promotable
    assert "low_tfd" in gate.reasons


def test_diverse_families_pass():
    cfg = SkillRobustnessConfig(tfd_min_promote=0.4)
    risk = detect_adversarial_formation(
        ["reflect", "count", "group", "rotate"], tasks=4, config=cfg
    )
    assert not risk.blocked
