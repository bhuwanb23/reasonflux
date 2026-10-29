"""SF1 premature skill creation and demotion."""

from core import Skill, SkillState
from skills import SkillRobustnessConfig, demote_skill
from skills.robustness.sf_creation import detect_premature_skill


def test_detect_premature_skill():
    cfg = SkillRobustnessConfig(min_evidence_promote=3, min_confidence_promote=0.4)
    weak = Skill(
        skill_id="p1",
        state=SkillState.ACTIVE,
        metadata={"confidence": 0.1, "evidence": {"discovery": []}},
    )
    assert detect_premature_skill(weak, cfg)

    strong = Skill(
        skill_id="p2",
        state=SkillState.ACTIVE,
        transfer_score=0.5,
        metadata={
            "confidence": 0.9,
            "evidence": {"discovery": [{}, {}, {}]},
        },
    )
    assert not detect_premature_skill(strong, cfg)


def test_demote_walks_two_hops_to_candidate():
    skill = Skill(skill_id="p3", state=SkillState.ACTIVE)
    demote_skill(skill)
    assert skill.state is SkillState.CANDIDATE
    assert skill.metadata["demoted"] is True
    assert skill.metadata["biography"]["failures"]
