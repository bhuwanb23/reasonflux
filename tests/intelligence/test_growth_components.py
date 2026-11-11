"""Component growth deltas TG / CCG / CompG / UG."""

from capability import Capability, seed_from_skills
from core import Skill, SkillState
from evaluation import (
    component_snapshot,
    composition_growth,
    coverage_growth,
    transfer_growth,
    utility_growth,
)
from skills import SkillLibrary


def _lib_with(sid: str, *, families=None, composed=False, utility=0.4) -> SkillLibrary:
    lib = SkillLibrary()
    history = [{"target_family": f, "success": True} for f in (families or ["geo"])]
    meta = {
        "mvp_category": "reflection",
        "utility_breakdown": {"su": utility},
    }
    if composed:
        meta["composed_from"] = ["x", "y"]
    lib.add(
        Skill(
            skill_id=sid,
            state=SkillState.ACTIVE,
            utility=utility,
            transfer_score=0.5,
            transfer_history=history,
            metadata=meta,
        )
    )
    return lib


def test_transfer_coverage_comp_utility_growth():
    lib = _lib_with("s1", families=["geo"], composed=False, utility=0.4)
    cap = Capability(capability_id="c", skill_ids=["s1"], utility=0.4)
    seed_from_skills(cap, lib)
    prev = component_snapshot(cap, library=lib, total_families=5)

    # Expand transfer + coverage + composition + utility
    lib2 = SkillLibrary()
    lib2.add(
        Skill(
            skill_id="s1",
            state=SkillState.ACTIVE,
            utility=0.7,
            transfer_score=0.8,
            transfer_history=[
                {"target_family": "geo", "success": True},
                {"target_family": "algebra", "success": True},
            ],
            metadata={
                "mvp_category": "rotation",
                "utility_breakdown": {"su": 0.7},
                "composed_from": ["a"],
            },
        )
    )
    cap2 = Capability(
        capability_id="c",
        skill_ids=["s1"],
        utility=0.7,
        coverage=0.0,
    )
    # Fresh evidence from richer skill
    seed_from_skills(cap2, lib2)

    tg = transfer_growth(cap2, prev, library=lib2)
    ccg = coverage_growth(cap2, prev, library=lib2, total_families=5)
    compg = composition_growth(cap2, prev, library=lib2)
    ug = utility_growth(cap2, prev)

    assert tg > 0
    assert ccg > 0
    assert compg > 0
    assert ug > 0
