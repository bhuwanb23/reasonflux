"""Tests for intelligence-level failure detectors and audit."""

from evaluation import (
    audit_intelligence,
    build_growth_evidence,
    detect_adaptation_failure,
    detect_composition_failure,
    detect_fragmentation_persistence,
    detect_growth_illusion,
    detect_skill_hoarding,
    detect_transfer_collapse,
)


def test_intel_detectors():
    assert detect_skill_hoarding(skill_count=10, ig_delta=0.0) is not None
    assert detect_transfer_collapse(tg=0.1, previous_tg=0.5) is not None
    assert detect_fragmentation_persistence(fragmentation_score=0.6) is not None
    assert detect_composition_failure(composition_success_rate=0.05) is not None
    assert detect_adaptation_failure(new_families=2, elasticity=0.0) is not None
    empty = build_growth_evidence()
    assert (
        detect_growth_illusion(ig_delta=0.1, cgr=0.1, evidence=empty) is not None
    )


def test_audit_intelligence_ok_with_evidence():
    ev = build_growth_evidence(
        new_skills=1,
        transfer_events=2,
        coverage_expansion=0.1,
        utility_improvement=0.05,
        composition_growth=0.1,
    )
    res = audit_intelligence(
        ig=0.2,
        ig_delta=0.05,
        evidence=ev,
        extra_metrics={
            "skill_count": 2,
            "tg": 0.2,
            "ug": 0.05,
            "ccg": 0.1,
            "cgr": 0.05,
            "transfer_delta": 1.0,
            "composition_success_rate": 0.8,
            "new_families": 0,
            "elasticity": 0.1,
            "fragmentation": 0.1,
        },
    )
    assert res.ok
