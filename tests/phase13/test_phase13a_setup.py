"""Phase 13A governance, statistics, and reproducibility checks."""

from pathlib import Path

import pytest

from evaluation.metrics_registry import metric_definition
from evaluation.stats import summarize_metric
from experiments._common import write_experiment_record
from experiments.exp01_invariants.run import main_multi as exp01_multi


def test_metric_registry_defines_paper_fields():
    definition = metric_definition("TS")
    assert definition["formula"] == "performance_after - performance_before"
    assert definition["failure_condition"] == "<= 0"


def test_multi_seed_summary_contains_uncertainty():
    result = exp01_multi(seeds=(0, 1), write=False)
    summary = result["statistics"]["IS"]
    assert summary["n"] == pytest.approx(2.0)
    assert {"mean", "std", "variance", "ci_low", "ci_high"} <= set(summary)


def test_stats_reject_invalid_confidence():
    with pytest.raises(ValueError):
        summarize_metric([1.0, 2.0], confidence=1.0)


def test_experiment_record_is_written_with_schema(tmp_path: Path):
    artifacts = write_experiment_record(
        "test_record",
        {"experiment_id": "TEST", "results": {"ok": True}},
        root=tmp_path,
    )
    record = Path(artifacts["json"]).read_text(encoding="utf-8")
    assert '"record_schema": "phase-13a-v1"' in record
    assert Path(artifacts["md"]).exists()
