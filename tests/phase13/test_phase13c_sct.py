"""Phase 13C protocol/metric contracts; never execute the multi-seed runner here."""
from __future__ import annotations

import pytest

from core.invariant import Invariant
from skills.config import SkillConfig
from solver.tasks import make_task_batch
from experiments.phase13c_sct import (
    _candidate_score,
    _enforce_opportunity_horizon,
    _gate_config,
    _opportunities,
    _quantile,
    load_config,
    run_confirmation,
)


def test_scv10_uses_frozen_lifecycle_cost_formula_and_logs_clipping():
    inv = Invariant(
        invariant_id="INV-test-reflection",
        pattern_signature=["apply_reflection"],
        frequency=6,
        consistency=1.0,
        generality=0.75,
        task_families=["reflection"],
        metadata={
            "expected_reuse": 1.2,
            "abstraction_gain": 1.1,
            "expected_transfer": 0.8,
            "creation_cost": 0.1,
            "mvp_category": "reflection",
        },
    )
    candidate, score = _candidate_score(inv, SkillConfig())

    assert score["p_reuse"] == 1.0
    assert score["AG"] == 1.0
    assert score["TS"] == 0.8
    assert score["CC"] == 0.1
    assert score["MC"] == pytest.approx(0.06)
    assert score["SCV10"] == pytest.approx(7.3)
    assert candidate.scv == score["SCV10"]
    assert score["p_reuse_raw"] == 1.2
    assert score["AG_raw"] == 1.1


def test_phase13c_gate_bypasses_only_legacy_scv_threshold():
    base = SkillConfig(skill_creation_threshold=0.0, min_frequency=5)
    bypass = _gate_config(base)
    assert bypass.skill_creation_threshold == -1.0e9
    assert bypass.min_frequency == base.min_frequency
    assert bypass.base_maintenance == base.base_maintenance


def test_candidate_opportunities_are_deduplicated_and_bounded_to_ten():
    inv = Invariant(
        invariant_id="INV-test-reflection",
        pattern_signature=["apply_reflection"],
        frequency=6,
        consistency=1.0,
        generality=0.75,
        task_families=["reflection"],
        metadata={"mvp_category": "reflection"},
    )
    tasks = make_task_batch(per_family=10, seed=2020, difficulty=0.3)
    opportunities = _opportunities(inv, tasks, 10)
    assert len(opportunities) == 10
    assert len({task.task_id for task in opportunities}) == 10


def test_quantile_interpolation_is_deterministic():
    assert _quantile([0.0, 1.0, 2.0, 3.0], 0.25) == 0.75
    assert _quantile([0.0, 1.0, 2.0, 3.0], 0.50) == 1.5
    assert _quantile([], 0.5) == 0.0


def test_candidates_without_full_horizon_are_reported_not_shortened():
    inv = Invariant(
        invariant_id="INV-test-reflection",
        pattern_signature=["apply_reflection"],
        frequency=6,
        consistency=1.0,
        generality=0.75,
        task_families=["reflection"],
        metadata={"mvp_category": "reflection"},
    )
    tasks = make_task_batch(per_family=1, seed=2020, difficulty=0.3)
    kept, rejected = _enforce_opportunity_horizon(
        [{"invariant": inv, "score": {"SCV10": 1.0}}], [], tasks, 10
    )
    assert kept == []
    assert rejected[0]["available_opportunities"] < 10
    assert rejected[0]["reasons"] == ["insufficient_distinct_heldout_opportunities"]


def test_confirmation_gate_requires_saved_frozen_calibration(monkeypatch, tmp_path):
    monkeypatch.setattr("experiments.phase13c.reporting.OUT_DIR", tmp_path)
    monkeypatch.setattr("experiments.phase13c_sct.OUT_DIR", tmp_path)
    with pytest.raises(FileNotFoundError, match="Run Phase 13C calibration"):
        run_confirmation(write=False)


def test_confirmation_cli_reports_confirmatory_seeds_without_running_stage(monkeypatch, capsys):
    import sys
    from experiments.phase13c import cli

    monkeypatch.setattr(sys, "argv", ["phase13c_sct", "confirm", "--no-write"])
    monkeypatch.setattr(
        cli,
        "run_confirmation",
        lambda write: {"calibration_seeds": [15, 16, 17, 18, 19], "seeds": list(range(20, 30))},
    )
    import json
    cli.main()
    payload = json.loads(capsys.readouterr().out)
    assert payload["seeds"] == list(range(20, 30))


def test_frozen_seed_offsets_keep_all_task_streams_separate():
    tasks = load_config()["tasks"]
    spans = {
        "discovery": range(tasks["discovery_seed_offset"], tasks["discovery_seed_offset"] + 1),
        "evaluation": range(tasks["evaluation_seed_offset"], tasks["evaluation_seed_offset"] + 1),
        "composition_training": range(tasks["composition_training_seed_offset"], tasks["composition_training_seed_offset"] + 10),
        "composition_validation": range(tasks["composition_validation_seed_offset"], tasks["composition_validation_seed_offset"] + 1),
        "composition_reuse": range(tasks["composition_reuse_seed_offset"], tasks["composition_reuse_seed_offset"] + 1),
        "lifecycle_probe": range(tasks["lifecycle_probe_seed_offset"], tasks["lifecycle_probe_seed_offset"] + 2),
    }
    names = list(spans)
    for i, left in enumerate(names):
        for right in names[i + 1:]:
            assert set(spans[left]).isdisjoint(spans[right]), (left, right)
