"""Sequential propose + explosion / redundant / specialization guards."""

from core import Skill, SkillState
from skills import SkillConfig, SkillLibrary, propose_sequential
from skills.composition.propose import is_overspecialized, is_redundant


def _lib(*skills: Skill) -> SkillLibrary:
    lib = SkillLibrary()
    for s in skills:
        lib.add(s)
    return lib


def test_propose_sequential_pair_covers_joint_requirements():
    a = Skill(
        skill_id="reflect",
        state=SkillState.ACTIVE,
        trigger_conditions=["reflect"],
        utility=0.5,
        metadata={"mvp_category": "reflection"},
    )
    b = Skill(
        skill_id="count",
        state=SkillState.ACTIVE,
        trigger_conditions=["count"],
        utility=0.4,
        metadata={"mvp_category": "counting"},
    )
    cands = propose_sequential(
        _lib(a, b), ["reflect", "count"], SkillConfig()
    )
    assert cands
    assert any(set(c.order) == {"reflect", "count"} for c in cands)


def test_redundant_and_overspecialized_rejected():
    cfg = SkillConfig(compose_reject_identical=True, compose_max_literal_triggers=2)
    same = Skill(
        skill_id="r1",
        state=SkillState.ACTIVE,
        trigger_conditions=["reflect"],
        metadata={"mvp_category": "reflection"},
    )
    same2 = Skill(
        skill_id="r1",
        state=SkillState.ACTIVE,
        trigger_conditions=["reflect"],
        metadata={"mvp_category": "reflection"},
    )
    assert is_redundant([same, same2], cfg) == "identical_skill_ids"

    lit_a = Skill(
        skill_id="a",
        state=SkillState.ACTIVE,
        trigger_conditions=["color:blue", "shape:triangle"],
        metadata={"mvp_category": "reflection"},
    )
    lit_b = Skill(
        skill_id="b",
        state=SkillState.ACTIVE,
        trigger_conditions=["size:small"],
        metadata={"mvp_category": "counting"},
    )
    assert is_overspecialized([lit_a, lit_b], cfg)

    # Explosion cap
    skills = []
    for i in range(6):
        skills.append(
            Skill(
                skill_id=f"s{i}",
                state=SkillState.ACTIVE,
                trigger_conditions=[f"t{i}", "shared"],
                utility=0.3,
                metadata={"mvp_category": "general"},
            )
        )
    cands = propose_sequential(
        _lib(*skills),
        [f"t{i}" for i in range(6)],
        SkillConfig(compose_max_candidates_per_task=3, compose_max_skills=2),
    )
    assert len(cands) <= 3
