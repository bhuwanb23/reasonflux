"""Tests for invariant identity and lifecycle advancement (11C-1)."""

import pytest

from core import (
    InvalidStateTransitionError,
    Invariant,
    InvariantEvidence,
    InvariantState,
    InvariantType,
)
from invariants import (
    InvariantIdentity,
    can_become_skill_candidate,
    qualify_invariant,
)


def _verified_invariant(invariant_id="INV-1"):
    return Invariant(
        invariant_id=invariant_id,
        pattern_signature=["find_symmetry", "apply_reflection"],
        frequency=5,
        consistency=0.9,
        generality=0.7,
        task_families=["reflection", "counting"],
        evidence=InvariantEvidence(
            observations=5, task_families=["reflection", "counting"], transfer_events=2
        ),
        invariant_type=InvariantType.PROCEDURAL,
        origin="synthetic",
    )


def test_identity_fingerprint_is_deterministic():
    inv = _verified_invariant()
    a = InvariantIdentity.from_invariant(inv)
    b = InvariantIdentity.from_invariant(inv)
    assert a.fingerprint == b.fingerprint
    assert a.invariant_id == b.invariant_id
    assert a.invariant_id.startswith("INV-")


def test_identity_normalizes_case_and_whitespace():
    a = InvariantIdentity(origin="Synthetic", pattern_signature=("Find_Symmetry", "apply"))
    b = InvariantIdentity(origin=" synthetic ", pattern_signature=("find_symmetry", "APPLY"))
    assert a.fingerprint == b.fingerprint


def test_identity_differs_by_origin():
    a = InvariantIdentity(origin="synthetic", pattern_signature=("a", "b"))
    b = InvariantIdentity(origin="arc", pattern_signature=("a", "b"))
    assert a.fingerprint != b.fingerprint


def test_identity_requires_origin_and_pattern():
    with pytest.raises(ValueError, match="origin"):
        InvariantIdentity(origin="", pattern_signature=("a",))
    with pytest.raises(ValueError, match="pattern_signature"):
        InvariantIdentity(origin="synthetic", pattern_signature=())


def test_identity_to_dict_exposes_ids():
    payload = InvariantIdentity(
        origin="synthetic", pattern_signature=("a", "b"), task_families=("f1",)
    ).to_dict()
    assert payload["fingerprint"] in payload["invariant_id"]
    assert payload["task_families"] == ["f1"]


def test_full_lifecycle_path_to_skill_candidate():
    inv = _verified_invariant()
    assert inv.state is InvariantState.DETECTED
    inv.transition_to(InvariantState.VALIDATED)
    inv.transition_to(InvariantState.STRONG)
    inv.transition_to(InvariantState.TRANSFER_VERIFIED)
    inv.transition_to(InvariantState.SKILL_CANDIDATE)
    assert inv.state is InvariantState.SKILL_CANDIDATE


def test_candidate_to_detected_path():
    inv = Invariant(
        invariant_id="INV-2",
        pattern_signature=["a"],
        state=InvariantState.CANDIDATE,
    )
    inv.transition_to(InvariantState.DETECTED)
    assert inv.state is InvariantState.DETECTED


def test_archived_is_terminal():
    inv = _verified_invariant()
    inv.transition_to(InvariantState.ARCHIVED)
    with pytest.raises(InvalidStateTransitionError):
        inv.transition_to(InvariantState.VALIDATED)


def test_cannot_skip_to_transfer_verified_from_detected():
    inv = _verified_invariant()
    with pytest.raises(InvalidStateTransitionError):
        inv.transition_to(InvariantState.TRANSFER_VERIFIED)


def test_can_become_skill_candidate_requires_transfer_verified():
    inv = _verified_invariant()
    assert can_become_skill_candidate(inv) is False
    inv.transition_to(InvariantState.VALIDATED)
    inv.transition_to(InvariantState.TRANSFER_VERIFIED)
    assert qualify_invariant(inv) == []
    assert can_become_skill_candidate(inv) is True


def test_can_become_skill_candidate_rejects_unqualified():
    inv = _verified_invariant()
    inv.transition_to(InvariantState.VALIDATED)
    inv.transition_to(InvariantState.TRANSFER_VERIFIED)
    inv.evidence.transfer_events = 0
    assert can_become_skill_candidate(inv) is False


def test_invariant_state_round_trip_preserves_new_stages():
    inv = _verified_invariant()
    inv.transition_to(InvariantState.VALIDATED)
    inv.transition_to(InvariantState.TRANSFER_VERIFIED)
    restored = Invariant.from_dict(inv.to_dict())
    assert restored.state is InvariantState.TRANSFER_VERIFIED
