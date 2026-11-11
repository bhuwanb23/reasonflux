"""Baselines and ablations."""

from evaluation.harness.runner import run_benchmark


def test_baseline_a_flat_cgr_and_fails_success():
    growth = run_benchmark("capability")
    flat = run_benchmark("capability", baseline="A")
    # Baseline A freezes learning — final CGR near zero relative to growth path
    assert abs(flat.snapshots[-1].cgr) <= abs(growth.snapshots[-1].cgr) + 1e-9
    assert flat.success is False


def test_ablation_a5_weakens_cgm():
    full = run_benchmark("capability")
    ablated = run_benchmark("capability", ablation="A5")
    assert ablated.snapshots[-1].capability_score <= full.snapshots[-1].capability_score + 1e-9
    # Ablated mean utility should be capped low
    assert ablated.snapshots[-1].mean_su <= 0.15 + 1e-9
