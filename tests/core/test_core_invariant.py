"""Tests for Invariant knowledge object."""

import pytest

from core import InvalidStateTransitionError, Invariant, InvariantState


def test_invariant_strength_computed():
    inv = Invariant(
        invariant_id="INV-1",
        pattern_signature=["detect", "reflect", "verify"],
        frequency=10,
        consistency=0.8,
        generality=0.5,
    )
    assert inv.strength == pytest.approx(4.0)


def test_invariant_validation_bounds():
    with pytest.raises(ValueError, match="consistency"):
        Invariant(
            invariant_id="INV-1",
            pattern_signature=["a"],
            consistency=1.5,
        )
    with pytest.raises(ValueError, match="frequency"):
        Invariant(invariant_id="INV-1", pattern_signature=["a"], frequency=-1)


def test_invariant_state_transitions():
    inv = Invariant(invariant_id="INV-1", pattern_signature=["reflect"])
    inv.transition_to(InvariantState.VALIDATED)
    inv.transition_to(InvariantState.STRONG)
    assert inv.state == InvariantState.STRONG
    with pytest.raises(InvalidStateTransitionError):
        inv.transition_to(InvariantState.DETECTED)


def test_invariant_dict_round_trip():
    inv = Invariant(
        invariant_id="INV-2",
        pattern_signature=["find_symmetry", "apply_reflection"],
        frequency=5,
        consistency=1.0,
        generality=0.6,
        transfer_contribution=0.2,
        associated_concepts=["reflection"],
        source_trace_ids=["tr1", "tr2"],
        state=InvariantState.VALIDATED,
    )
    restored = Invariant.from_dict(inv.to_dict())
    assert restored.invariant_id == inv.invariant_id
    assert restored.strength == pytest.approx(inv.strength)
    assert restored.state == InvariantState.VALIDATED
    assert restored.pattern_signature == inv.pattern_signature
