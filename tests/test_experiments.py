"""Experiment runners emit paper artifacts and report honest numbers."""

from __future__ import annotations

import pytest

from experiments.exp01_invariants.run import main as exp01
from experiments.exp02_skills.run import main as exp02
from experiments.exp03_transfer.run import main as exp03
from experiments.exp05_end_to_end.run import main as exp05


def test_exp01_discovers_reflection_and_rotation():
    out = exp01(write=False)
    assert out["n_validated"] > 0
    assert out["reflection_found"] is True
    assert out["rotation_found"] is True
    assert out["is_summary"]["mean"] > 0.0
    # Ranking must be sorted by IS descending.
    scores = [row["is"] for row in out["invariants"]]
    assert scores == sorted(scores, reverse=True)


def test_exp02_scv_gate_actually_gates():
    out = exp02(write=False)
    assert out["admitted"] > 0
    assert out["admitted_at_strict_threshold"] == 0
    assert out["scv_gate_effective"] is True


def test_exp03_reports_positive_and_cross_family_transfer():
    out = exp03(write=False)
    assert out["positive_transfer"] is True
    assert out["n_transfer_records"] > 0
    assert out["mean_benefit"] > 0.0
    # Transfer must not be confined to the originating family.
    assert out["n_cross_family"] > 0


def test_exp05_beats_all_baselines():
    out = exp05(write=False)
    assert out["beats_all_baselines"] is True
    assert out["success"] is True
    names = {b["name"] for b in out["baselines"]}
    assert len(names) == 4


def test_exp_artifacts_are_written(tmp_path):
    out = exp01(write=True)
    artifacts = out.get("artifacts") or {}
    assert "json" in artifacts and "md" in artifacts
    json_path = __import__("pathlib").Path(artifacts["json"])
    assert json_path.exists()
    assert json_path.stat().st_size > 0
