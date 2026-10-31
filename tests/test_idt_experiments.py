"""Phase 13B IDT experiment contracts."""

import pytest

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


def test_idt_baselines_show_transfer_aware_advantage():
    result = baselines(seed=0)
    assert result["metrics"]["ASFT"] > result["metrics"]["random_pattern"]
    assert result["metrics"]["ASFT"] > result["metrics"]["frequency_only"]
