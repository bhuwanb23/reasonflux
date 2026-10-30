"""E2E: capability snapshots → C_t, CGR, CA, IG, robustness."""

from capability import (
    Capability,
    CapabilityLibrary,
    compute_system_capability_state,
    sync_capability_state,
)
from core import CapabilityState, Skill, SkillState
from evaluation import (
    audit_growth,
    build_growth_evidence,
    compute_ca,
    compute_cgr,
    compute_ig,
    component_snapshot,
    composition_growth,
    coverage_growth,
    transfer_growth,
    utility_growth,
)
from skills import SkillLibrary


def _skill(sid: str, *, utility: float, families: list[str], composed: bool = False) -> Skill:
    meta = {
        "mvp_category": "reflection" if "geo" in families else "rotation",
        "utility_breakdown": {"su": utility},
    }
    if composed:
        meta["composed_from"] = ["a", "b"]
    return Skill(
        skill_id=sid,
        state=SkillState.ACTIVE,
        utility=utility,
        transfer_score=utility,
        transfer_history=[{"target_family": f, "success": True} for f in families],
        metadata=meta,
    )


def test_positive_zero_negative_cgr_and_ig():
    skills_t0 = SkillLibrary()
    skills_t0.add(_skill("reflect", utility=0.4, families=["geo"]))
    caps = CapabilityLibrary()
    caps.add(Capability(capability_id="geo", skill_ids=["reflect"], utility=0.4))

    snap0 = compute_system_capability_state(caps, skills_t0)
    assert snap0.growth_state == "emerging"
    assert snap0.cgr == 0.0

    # t1: stronger utility + extra transfer family + composition
    skills_t1 = SkillLibrary()
    skills_t1.add(
        _skill("reflect", utility=0.8, families=["geo", "algebra"], composed=True)
    )
    skills_t1.add(_skill("rotate", utility=0.6, families=["geo"]))
    caps.get("geo").add_skill("rotate")
    caps.get("geo").utility = 0.7

    snap1 = compute_system_capability_state(
        caps, skills_t1, previous_score=snap0.capability_score
    )
    assert snap1.cgr > 0
    assert snap1.growth_state in ("growing", "accelerating")

    # Zero growth
    snap_flat = compute_system_capability_state(
        caps, skills_t1, previous_score=snap1.capability_score
    )
    assert abs(snap_flat.cgr) < 1e-9

    # Negative growth
    skills_t2 = SkillLibrary()
    skills_t2.add(_skill("reflect", utility=0.1, families=["geo"]))
    weak = CapabilityLibrary()
    weak.add(Capability(capability_id="geo", skill_ids=["reflect"], utility=0.1))
    snap_down = compute_system_capability_state(
        weak, skills_t2, previous_score=snap1.capability_score
    )
    assert snap_down.cgr < 0
    assert snap_down.growth_state == "declining"

    ca = compute_ca(snap1.cgr, 0.0)
    assert ca > 0

    cap = caps.get("geo")
    prev = {"transfer_support": 1.0, "coverage": 0.1, "composition_count": 0.0, "utility": 0.4}
    tg = transfer_growth(cap, prev, library=skills_t1)
    ccg = coverage_growth(cap, prev, library=skills_t1, total_families=5)
    compg = composition_growth(cap, prev, library=skills_t1)
    ug = utility_growth(cap, prev)
    ig = compute_ig(snap1.cgr, tg=tg, ug=ug, ccg=ccg, compg=compg)
    assert ig > 0

    ev = build_growth_evidence(
        new_skills=1,
        transfer_events=2,
        coverage_expansion=max(0.0, ccg),
        utility_improvement=max(0.0, ug),
        composition_growth=max(0.0, compg),
    )
    result = audit_growth(
        cgr=snap1.cgr,
        tg=tg,
        ug=ug,
        ccg=ccg,
        skill_delta=1,
        transfer_delta=tg,
        evidence=ev,
    )
    assert result.ok

    state = CapabilityState(state_id="sys")
    sync_capability_state(
        state,
        snap1.portfolio,
        ["geo"],
        growth=snap1,
        write_growth=True,
    )
    assert state.growth_metrics["cgr"] == snap1.cgr
    assert state.metadata["growth_state"] == snap1.growth_state
