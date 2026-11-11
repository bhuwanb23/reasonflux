"""False-negative handling — transfer rescues rare-but-important invariants."""

from core import Invariant, InvariantEvidence, InvariantState
from invariants import ValidationConfig, compute_validation_scores
from invariants.validation.false_negatives import can_rescue_by_transfer


def test_rare_high_transfer_is_rescued():
    inv = Invariant(
        invariant_id="INV-rare",
        pattern_signature=["find_symmetry", "apply_reflection"],
        frequency=2,  # F=0.2 < min_f=0.3
        consistency=0.9,
        generality=0.7,
        transfer_contribution=0.85,
        evidence=InvariantEvidence(observations=2, transfer_events=3),
        state=InvariantState.CANDIDATE,
        metadata={"reasoning_value": 0.6},
    )
    scores = compute_validation_scores(inv)
    assert scores.rescued_by_transfer is True
    assert scores.pass_frequency is True


def test_rare_low_transfer_not_rescued():
    inv = Invariant(
        invariant_id="INV-rare2",
        pattern_signature=["find_symmetry", "apply_reflection"],
        frequency=2,
        consistency=0.9,
        generality=0.7,
        transfer_contribution=0.2,
        state=InvariantState.CANDIDATE,
        metadata={"reasoning_value": 0.6},
    )
    scores = compute_validation_scores(inv)
    assert scores.rescued_by_transfer is False
    assert scores.pass_frequency is False


def test_can_rescue_helper_requires_min_frequency():
    inv = Invariant(
        invariant_id="INV-once",
        pattern_signature=["a"],
        frequency=1,
        state=InvariantState.CANDIDATE,
    )
    assert (
        can_rescue_by_transfer(
            inv, 0.9, frequency_passed=False, config=ValidationConfig()
        )
        is False
    )
