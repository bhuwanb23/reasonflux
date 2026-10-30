"""Scenario fixtures produce growth signals."""

from evaluation.harness.runner import run_benchmark
from evaluation.harness.scenarios import build_scenario


def test_l1_to_l4_scenarios_build():
    for level in ("skill", "transfer", "capability", "arc"):
        steps = build_scenario(level)
        assert len(steps) >= 2
        assert len(steps[-1].skills) >= 1


def test_capability_scenario_positive_cgr():
    result = run_benchmark("capability")
    assert len(result.snapshots) >= 2
    # Later CGR should be non-negative on growth path
    assert result.snapshots[-1].capability_score >= result.snapshots[0].capability_score
    cgrs = [s.cgr for s in result.snapshots[1:]]
    assert any(c > 0 for c in cgrs) or result.snapshots[-1].ig >= result.snapshots[0].ig
