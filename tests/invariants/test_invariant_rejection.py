"""Tests for invariant rejection criteria (what is NOT an invariant)."""

from core import Invariant, InvariantEvidence
from invariants import RejectionReason, apply_rejection_criteria


def _inv(**overrides):
    params = dict(
        invariant_id="INV-1",
        pattern_signature=["find_symmetry", "apply_reflection"],
        frequency=5,
        consistency=0.9,
        generality=0.5,
        task_families=["reflection", "counting"],
        evidence=InvariantEvidence(observations=5, transfer_events=1),
    )
    params.update(overrides)
    return Invariant(**params)


def test_clean_invariant_is_not_rejected():
    assert apply_rejection_criteria(_inv()) == []


def test_rare_event_rejected():
    assert RejectionReason.RARE_EVENT in apply_rejection_criteria(_inv(frequency=1))


def test_task_specific_detail_rejected():
    inv = _inv(pattern_signature=["reflect:red_triangle", "verify"])
    assert RejectionReason.TASK_SPECIFIC in apply_rejection_criteria(inv)


def test_task_specific_shape_token_rejected():
    inv = _inv(pattern_signature=["detect_triangle", "apply_reflection"])
    assert RejectionReason.TASK_SPECIFIC in apply_rejection_criteria(inv)


def test_universal_noise_rejected():
    inv = _inv(generality=1.0, task_families=["a", "b", "c"])
    assert RejectionReason.UNIVERSAL_NOISE in apply_rejection_criteria(inv)


def test_accidental_correlation_rejected_for_metadata_only():
    inv = _inv(pattern_signature=["meta:blue_present", "meta:task_group"])
    assert RejectionReason.ACCIDENTAL_CORRELATION in apply_rejection_criteria(inv)


def test_accidental_correlation_rejected_for_empty_pattern():
    inv = _inv(pattern_signature=[])
    assert RejectionReason.ACCIDENTAL_CORRELATION in apply_rejection_criteria(inv)
