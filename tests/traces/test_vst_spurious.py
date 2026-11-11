"""F1 spurious vs mechanism VST."""

import pytest

from core import Invariant, InvariantEvidence
from invariants.robustness import passes_vst, vst_for_invariant
from invariants.validation import is_false_positive


def test_spurious_blue_fails_vst_and_fp():
    inv = Invariant(
        invariant_id="INV-blue",
        pattern_signature=["select_blue", "apply_reflection"],
        frequency=20,
        consistency=0.9,
        generality=0.5,
        evidence=InvariantEvidence(observations=20),
        metadata={"failed_variations": ["color", "shape"]},
    )
    assert vst_for_invariant(inv) == pytest.approx(0.5)
    assert not passes_vst(inv)
    assert "low_vst" in is_false_positive(inv)


def test_reflection_survives_variations():
    inv = Invariant(
        invariant_id="INV-ref",
        pattern_signature=["find_symmetry", "apply_reflection"],
        frequency=20,
        consistency=0.9,
        generality=0.8,
        evidence=InvariantEvidence(observations=20),
        metadata={"variations": ["color", "shape", "position", "count"]},
    )
    assert vst_for_invariant(inv) == 1.0
    assert passes_vst(inv)
    assert is_false_positive(inv) == []
