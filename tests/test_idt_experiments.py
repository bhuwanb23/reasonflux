"""Phase 13B IDT experiment contracts."""

import pytest

from experiments.check_phase13b_gates import baseline_comparison_passes
from experiments.idt_experiments import (
    baselines,
    discover_family,
    quality,
    robustness,
    transfer,
)


@pytest.mark.parametrize("family", ["reflection", "rotation", "counting", "grouping"])
def test_family_discovery_finds_expected_invariant(family: str):
    result = discover_family(family, seed=0)
    assert result["expected_found"] is True
    assert result["metrics"]["IS"] > 0


def test_idt_quality_meets_mvp_targets():
    result = quality(seed=0)
    assert result["metrics"]["IP"] >= 0.70
    assert result["metrics"]["IR"] >= 0.75


def test_idt_transfer_is_positive_and_predictive():
    result = transfer(seed=0)
    assert result["metrics"]["TS"] > 0
    assert result["metrics"]["TU"] > 0
    assert result["metrics"]["PEARSON"] > 0


def test_idt_robustness_survives_variation_and_noise():
    result = robustness(seed=0)
    assert result["metrics"]["VST"] >= 0.60
    assert result["metrics"]["RANK_STABILITY"] >= 0.60


def test_idt_baselines_are_not_worse_than_controls():
    result = baselines(seed=0)
    assert result["metrics"]["ASFT"] > result["metrics"]["random_pattern"]
    assert result["metrics"]["ASFT"] >= result["metrics"]["frequency_only"]
    assert result["metrics"]["ASFT"] >= result["metrics"]["no_transfer"]


def test_baseline_report_exposes_paired_deltas_and_ranking_diagnostics():
    result = baselines(seed=0)
    metrics = result["metrics"]
    diagnostics = result["ranking_diagnostics"]

    assert metrics["ASFT_advantage"] == pytest.approx(
        metrics["ASFT"] - metrics["frequency_only"]
    )
    assert metrics["ASFT_minus_no_transfer"] == pytest.approx(
        metrics["ASFT"] - metrics["no_transfer"]
    )
    assert diagnostics["asft_order"]
    assert diagnostics["frequency_order"]
    assert diagnostics["no_transfer_order"]
    assert diagnostics["mean_transfer_utility_at_k"]
    assert diagnostics["distinct_semantic_candidates"] >= 1


def test_phase13b_baseline_gate_rejects_ties_and_requires_all_controls_beaten():
    tied = [
        {
            "metrics": {
                "ASFT": 0.5,
                "frequency_only": 0.5,
                "no_transfer": 0.4,
                "random_pattern": 0.1,
            }
        }
    ]
    wins = [
        {
            "metrics": {
                "ASFT": 0.51,
                "frequency_only": 0.5,
                "no_transfer": 0.4,
                "random_pattern": 0.1,
            }
        }
    ]
    assert baseline_comparison_passes([]) is False
    assert baseline_comparison_passes(tied) is False
    assert baseline_comparison_passes(wins) is True
