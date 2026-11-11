"""Five validation tests — Reflection high; VerifyOutput low T/R."""

import pytest

from core import Invariant, InvariantEvidence, InvariantState
from invariants import ValidationConfig, compute_validation_scores


def _inv(**kwargs):
    params = dict(
        invariant_id="INV-x",
        pattern_signature=["find_symmetry", "apply_reflection"],
        frequency=10,
        consistency=0.9,
        generality=0.7,
        transfer_contribution=0.0,
        evidence=InvariantEvidence(observations=10, transfer_events=0),
        state=InvariantState.CANDIDATE,
        metadata={},
    )
    params.update(kwargs)
    return Invariant(**params)


def test_reflection_scores_high_on_all_axes():
    inv = _inv(
        transfer_contribution=0.8,
        metadata={"reasoning_value": 0.7},
        evidence=InvariantEvidence(
            observations=22, transfer_events=3, task_families=["a", "b"]
        ),
    )
    scores = compute_validation_scores(inv)
    assert scores.pass_frequency
    assert scores.pass_consistency
    assert scores.pass_generality
    assert scores.pass_transfer
    assert scores.pass_reasoning
    assert scores.score > 0.05


def test_verify_output_low_transfer_and_reasoning():
    inv = _inv(
        invariant_id="INV-verify",
        pattern_signature=["verify_output"],
        frequency=50,
        consistency=1.0,
        generality=1.0,
        transfer_contribution=0.0,
        evidence=InvariantEvidence(observations=50, transfer_events=0),
        metadata={},
    )
    scores = compute_validation_scores(inv)
    assert scores.pass_frequency
    assert scores.pass_consistency
    assert not scores.pass_transfer
    assert not scores.pass_reasoning
    assert scores.score == 0.0


def test_transfer_override_map():
    inv = _inv(transfer_contribution=0.0)
    scores = compute_validation_scores(inv, transfer_override=0.9)
    assert scores.transfer == pytest.approx(0.9)
    assert scores.pass_transfer


def test_frequency_gate_with_config():
    inv = _inv(frequency=2)
    scores = compute_validation_scores(inv, ValidationConfig(min_f=0.3))
    assert not scores.pass_frequency
    assert "frequency" in scores.reasons
