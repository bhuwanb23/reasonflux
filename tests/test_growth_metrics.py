"""Unit tests for CGR / CA / saturation / capability_score."""

from evaluation import (
    GrowthConfig,
    capability_score,
    classify_growth_state,
    compute_ca,
    compute_cgr,
    compute_portfolio_capability,
    compute_saturation_ratio,
)
from capability import Capability, CapabilityLibrary
from core import Skill, SkillState
from skills import SkillLibrary


def test_compute_cgr_pair_and_series():
    assert abs(compute_cgr(current_c=0.8, previous_c=0.5, dt=1.0) - 0.3) < 1e-9
    assert abs(compute_cgr([0.2, 0.5, 0.8], dt=1.0) - 0.3) < 1e-9
    assert compute_cgr([0.5]) == 0.0


def test_compute_ca_and_saturation():
    assert abs(compute_ca(0.3, 0.1, dt=1.0) - 0.2) < 1e-9
    assert abs(compute_saturation_ratio(0.1, 2.0) - 0.05) < 1e-9
    assert compute_saturation_ratio(0.0, 0.0) == 0.0
    assert compute_saturation_ratio(0.5, 0.0) == 1.0


def test_capability_score_and_portfolio():
    skills = SkillLibrary()
    skills.add(
        Skill(
            skill_id="s1",
            state=SkillState.ACTIVE,
            utility=0.8,
            transfer_score=0.6,
            transfer_history=[{"target_family": "geo", "success": True}],
            metadata={
                "mvp_category": "reflection",
                "utility_breakdown": {"su": 0.8},
                "composed_from": ["a"],
            },
        )
    )
    caps = CapabilityLibrary()
    cap = Capability(capability_id="c1", skill_ids=["s1"])
    caps.add(cap)
    score = capability_score(cap, library=skills, record_history=False)
    assert 0.0 < score <= 1.5
    port = compute_portfolio_capability(caps, skills)
    assert abs(port - score) < 1e-9


def test_classify_growth_state():
    assert classify_growth_state(0.1, has_history=False) == "emerging"
    assert classify_growth_state(-0.05) == "declining"
    assert classify_growth_state(0.1, ca=0.05) == "accelerating"
    assert classify_growth_state(0.1, ca=0.0) == "growing"
    cfg = GrowthConfig(saturation_low_csr=0.05, skill_count_illusion_max_cgr=0.01)
    assert classify_growth_state(0.0, csr=0.01, growth_config=cfg) == "saturated"
