"""Growth evidence model and failure detectors."""

from evaluation import (
    GrowthConfig,
    audit_growth,
    build_growth_evidence,
    detect_coverage_inflation,
    detect_growth_without_utility,
    detect_metric_gaming,
    detect_skill_count_illusion,
    detect_transfer_illusion,
)


def test_five_failure_modes_detected():
    cfg = GrowthConfig()
    assert detect_skill_count_illusion(skill_delta=5, cgr=0.0, config=cfg) is not None
    assert detect_transfer_illusion(tg=0.1, utility_delta=0.0, config=cfg) is not None
    assert detect_coverage_inflation(ccg=0.1, transfer_delta=0.0, config=cfg) is not None
    assert detect_growth_without_utility(cgr=0.05, ug=0.0, config=cfg) is not None
    empty = build_growth_evidence()
    assert detect_metric_gaming(cgr=0.1, evidence=empty, config=cfg) is not None


def test_audit_growth_ok_with_evidence():
    ev = build_growth_evidence(
        new_skills=1,
        transfer_events=2,
        coverage_expansion=0.1,
        utility_improvement=0.05,
    )
    result = audit_growth(
        cgr=0.1,
        tg=0.2,
        ug=0.05,
        ccg=0.1,
        skill_delta=1,
        transfer_delta=2.0,
        evidence=ev,
    )
    assert result.ok
    assert result.evidence is not None
    assert result.evidence.has_support()


def test_audit_rejects_unsupported_positive_cgr():
    result = audit_growth(cgr=0.1, evidence=build_growth_evidence())
    assert not result.ok
    kinds = {f.kind for f in result.failures}
    assert "metric_gaming" in kinds or "unsupported_growth" in kinds
