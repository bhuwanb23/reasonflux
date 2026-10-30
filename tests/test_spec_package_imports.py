"""Specification package keeps stable import paths after the 11C-3 split."""

from invariants import InvariantPolicy, apply_rejection_criteria, qualify_invariant
from invariants.specification import (
    InvariantIdentity,
    classify_invariant_type,
    summarize_specification,
)


def test_specification_package_reexports():
    policy = InvariantPolicy()
    assert policy.min_frequency == 3
    assert callable(qualify_invariant)
    assert callable(apply_rejection_criteria)
    assert callable(classify_invariant_type)
    assert "definition" in summarize_specification()
    identity = InvariantIdentity(origin="t", pattern_signature=("a", "b"))
    assert identity.invariant_id.startswith("INV-")
