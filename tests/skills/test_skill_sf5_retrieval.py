"""SF5 retrieval failure diagnosis and boost."""

from core import Skill, SkillState
from skills import SkillLibrary, SkillRobustnessConfig, retrieve_skills
from skills.robustness.sf_retrieval import (
    boost_retrieval,
    diagnose_retrieval_failure,
)


def test_low_recall_diagnosed_and_boost_raises_rank():
    cfg = SkillRobustnessConfig(rr_min=0.6, retrieval_boost=0.2)
    lib = SkillLibrary()
    missed = Skill(
        skill_id="missed",
        state=SkillState.ACTIVE,
        trigger_conditions=["reflect"],
        utility=0.1,
        metadata={"composition_potential": 0.3},
    )
    found = Skill(
        skill_id="found",
        state=SkillState.ACTIVE,
        trigger_conditions=["count"],
        utility=0.2,
        metadata={"composition_potential": 0.3},
    )
    lib.add(missed)
    lib.add(found)

    diag = diagnose_retrieval_failure(
        ["reflect", "count"], lib, [found], cfg
    )
    assert diag.recall == 0.5
    assert diag.missed_ids == ["missed"]
    assert "boost_missed" in diag.actions

    boost_retrieval(missed, cfg.retrieval_boost)
    ranked = retrieve_skills(lib, ["reflect", "count"])
    assert ranked[0].skill_id == "missed"
