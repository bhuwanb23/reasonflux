"""Unit tests for Intelligence metric helpers."""

from evaluation import (
    classify_intelligence_stage,
    compute_elasticity,
    compute_ia,
    compute_ie,
    compute_igr,
    intelligence_score,
)


def test_intelligence_score_weights_and_zero():
    ig = intelligence_score(ag=0.1, su=0.2, ts=0.3, cgr=0.4, cp=0.05, ad=0.02)
    expected = 0.15 * 0.1 + 0.15 * 0.2 + 0.20 * 0.3 + 0.25 * 0.4 + 0.15 * 0.05 + 0.10 * 0.02
    assert abs(ig - expected) < 1e-9
    assert intelligence_score(0, 0, 0, 0, 0, 0) == 0.0


def test_igr_ia_ie_elasticity():
    assert abs(compute_igr(0.5, 0.2, dt=1.0) - 0.3) < 1e-9
    assert abs(compute_ia(0.3, 0.1, dt=1.0) - 0.2) < 1e-9
    assert abs(compute_ie(0.4, 4) - 0.1) < 1e-9
    assert abs(compute_elasticity(0.2, 2, dt=1.0) - 0.1) < 1e-9
    assert compute_ie(0.5, 0) == 0.0
    assert compute_elasticity(0.2, 0) == 0.0


def test_maturity_stages():
    assert classify_intelligence_stage() == "emerging"
    assert (
        classify_intelligence_stage(skill_count=3, transfer_events=1, igr=0.1)
        == "developing"
    )
    assert (
        classify_intelligence_stage(cross_family=True, transfer_events=3)
        == "generalizing"
    )
    assert (
        classify_intelligence_stage(
            cross_family=True, composition_ok=True, transfer_events=3
        )
        == "compositional"
    )
    assert (
        classify_intelligence_stage(adaptation_ok=True, igr=0.1) == "adaptive"
    )
