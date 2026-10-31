"""End-to-end: real tasks → traces → invariants → skills → reuse → CGR.

This is the load-bearing test for Phase 11. Unlike the harness suites, nothing
here is synthetic scenario data: every trace comes from the solver, every
invariant from those traces, and every growth number from accumulating
experience.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import pytest

from baselines.dreamcoder_like.run import run as dreamcoder_run
from baselines.no_learning.run import run as no_learning_run
from baselines.random_skill_creation.run import run as random_run
from baselines.skill_storage.run import run as storage_run
from pipelines.full_asft_pipeline import run_full_asft_pipeline

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture(scope="module")
def full_run():
    return run_full_asft_pipeline()


def test_pipeline_produces_every_stage(full_run):
    assert full_run.rounds
    assert full_run.traces
    assert full_run.invariants
    assert full_run.skills
    assert full_run.capabilities
    assert full_run.reuse


def test_traces_are_real_and_from_all_families(full_run):
    families = {t.metadata["task_family"] for t in full_run.traces}
    assert families == {"reflection", "rotation", "counting", "grouping"}
    for trace in full_run.traces:
        assert trace.steps, trace.trace_id
        assert trace.outcome is not None


def test_growth_curve_recovers_and_grows(full_run):
    scores = full_run.capability_scores
    assert len(scores) >= 3
    trough = min(scores)
    assert scores[-1] > trough, scores
    assert full_run.cgr > 0.0, full_run.cgr_series
    assert full_run.ig > 0.0, full_run.ig_series


def test_library_accumulates_skills(full_run):
    """Skills must persist across rounds, not be rebuilt from scratch."""
    counts = [r.n_skills for r in full_run.rounds]
    assert counts[-1] >= counts[0]
    assert full_run.summary["library_size"] >= counts[-1]


def test_transfer_is_measured_not_assumed(full_run):
    credited = [r for r in full_run.reuse if r.transfer_credit]
    assert credited
    for result in credited:
        # Credit requires an actual cost reduction on a correct run.
        assert result.success
        assert result.reused_cost < result.baseline_cost
        assert result.benefit > 0.0


def test_pipeline_success_flag(full_run):
    assert full_run.success is True
    summary = full_run.summary
    assert summary["cgr"] > 0.0
    assert summary["ig"] > 0.0
    assert summary["recovered_from_trough"] is True


def test_asft_beats_every_baseline(full_run):
    asft_capability = full_run.summary["final_capability"]
    baselines = [no_learning_run(), storage_run(), random_run(), dreamcoder_run()]
    for baseline in baselines:
        assert asft_capability > baseline["capability_score"], baseline["name"]
    # And no-learning must be the floor.
    assert no_learning_run()["capability_score"] == 0.0


def test_baselines_are_distinguishable():
    names = {
        no_learning_run()["name"],
        storage_run()["name"],
        random_run()["name"],
        dreamcoder_run()["name"],
    }
    assert names == {
        "no_learning",
        "skill_storage",
        "random_skill_creation",
        "dreamcoder_like",
    }


@pytest.mark.parametrize(
    "module",
    [
        "pipelines.full_asft_pipeline",
        "pipelines.trace_pipeline",
        "pipelines.invariant_pipeline",
        "pipelines.skill_pipeline",
        "transfer.reuse_engine",
        "transfer",
        "evaluation.invariant_metrics",
    ],
)
def test_modules_import_in_a_fresh_interpreter(module):
    """Import hygiene: these have had circular-import failures historically."""
    code = f"import {module}; print('ok')"
    proc = subprocess.run(
        [sys.executable, "-c", code],
        cwd=ROOT,
        capture_output=True,
        text=True,
        env={**_env(), "PYTHONPATH": str(ROOT / "src")},
    )
    assert proc.returncode == 0, proc.stderr
    assert "ok" in proc.stdout


def _env() -> dict[str, str]:
    import os

    return dict(os.environ)
