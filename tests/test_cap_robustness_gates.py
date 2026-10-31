"""Hard gate rejects skill-count-only growth."""

from capability.robustness.config import CapabilityRobustnessConfig
from capability.robustness.gates import validate_growth_claim
from evaluation.growth_checks import GrowthEvidence


def test_rejects_skill_count_only():
    ev = GrowthEvidence(new_skills=5)
    result = validate_growth_claim(
        transfer_delta=0.0,
        utility_delta=0.0,
        coverage_delta=0.0,
        evidence=ev,
        skill_delta=5,
        cgr=0.1,
    )
    assert result.accepted is False
    assert "skill_count_only_growth" in result.reasons


def test_accepts_multi_signal_growth():
    ev = GrowthEvidence(
        new_skills=1,
        transfer_events=2,
        coverage_expansion=0.1,
        utility_improvement=0.2,
    )
    result = validate_growth_claim(
        transfer_delta=0.1,
        utility_delta=0.2,
        coverage_delta=0.1,
        evidence=ev,
        skill_delta=1,
        cgr=0.05,
    )
    assert result.accepted is True
    assert result.reasons == []


def test_requires_evidence_when_configured():
    cfg = CapabilityRobustnessConfig(require_evidence=True)
    result = validate_growth_claim(
        transfer_delta=0.1,
        utility_delta=0.1,
        coverage_delta=0.1,
        evidence=None,
        config=cfg,
    )
    assert result.accepted is False
    assert "missing_growth_evidence" in result.reasons
