"""Harness growth can pass; gamed/flat path fails hard gate."""

from evaluation.harness.config import HarnessConfig
from evaluation.harness.evidence import gate_run
from evaluation.harness.runner import run_benchmark
from pipelines.evaluation_pipeline import run_evaluation_pipeline


def test_growth_passes_hard_gate():
    run = run_benchmark("capability", config=HarnessConfig(hard_validation=True))
    ok, kinds = gate_run(run, HarnessConfig(hard_validation=True))
    assert ok is True, kinds
    assert run.success is True


def test_flat_fails_hard_gate():
    run = run_benchmark(
        "capability",
        baseline="A",
        config=HarnessConfig(hard_validation=True),
    )
    ok, kinds = gate_run(run, HarnessConfig(hard_validation=True))
    assert ok is False
    assert run.success is False
    assert kinds  # non-empty failure reasons


def test_pipeline_still_green(tmp_path):
    growth = run_evaluation_pipeline(
        level="capability",
        out_dir=tmp_path / "g",
        write=False,
        run_id="e5_growth",
    )
    flat = run_evaluation_pipeline(
        level="capability",
        baseline="A",
        out_dir=tmp_path / "f",
        write=False,
        run_id="e5_flat",
    )
    assert growth["success"] is True
    assert flat["success"] is False
