"""Capability coverage (CCov) formula."""

from capability import Capability, CapabilityConfig, compute_coverage
from core import Skill, SkillState
from skills import SkillLibrary


def _skill(sid: str, *, families=None, category="reflection") -> Skill:
    history = [{"target_family": f, "success": True} for f in (families or [])]
    return Skill(
        skill_id=sid,
        state=SkillState.ACTIVE,
        transfer_history=history,
        metadata={"mvp_category": category, "utility_breakdown": {"su": 0.5}},
        utility=0.5,
    )


def test_ccov_formula_with_family_norm():
    lib = SkillLibrary()
    lib.add(_skill("a", families=["geo", "algebra"]))
    lib.add(_skill("b", families=["geo"], category="rotation"))
    cap = Capability(capability_id="c", skill_ids=["a", "b"])
    cfg = CapabilityConfig(ccov_family_norm=5)
    # families: geo, algebra, cat:reflection, cat:rotation → 4
    cov = compute_coverage(cap, library=lib, total_families=5, config=cfg)
    assert abs(cov - 4 / 5) < 1e-9
    assert abs(cap.coverage - cov) < 1e-9
