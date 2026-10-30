"""False-positive handling — color/shape/position rejection."""

from core import Invariant, InvariantState
from invariants.validation.false_positives import is_false_positive


def test_color_literal_is_false_positive():
    inv = Invariant(
        invariant_id="INV-blue",
        pattern_signature=["reflect:blue_triangle"],
        state=InvariantState.CANDIDATE,
    )
    reasons = is_false_positive(inv)
    assert "task_specific_literal" in reasons


def test_failed_variation_survival():
    inv = Invariant(
        invariant_id="INV-v",
        pattern_signature=["find_symmetry", "apply_reflection"],
        state=InvariantState.CANDIDATE,
        metadata={"failed_variations": ["color", "shape"]},
    )
    reasons = is_false_positive(inv)
    assert "failed_variation_survival" in reasons


def test_clean_invariant_not_false_positive():
    inv = Invariant(
        invariant_id="INV-clean",
        pattern_signature=["find_symmetry", "apply_reflection"],
        state=InvariantState.CANDIDATE,
    )
    assert is_false_positive(inv) == []
