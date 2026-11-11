"""Tests for Phase 11C-1 invariant taxonomy and MVP scope."""

import pytest

from core import Invariant, InvariantType, MVP_INVARIANT_TYPES
from invariants import classify_invariant_type


def test_mvp_scope_is_operational_and_procedural():
    assert InvariantType.OPERATIONAL in MVP_INVARIANT_TYPES
    assert InvariantType.PROCEDURAL in MVP_INVARIANT_TYPES
    assert InvariantType.STRUCTURAL not in MVP_INVARIANT_TYPES
    assert InvariantType.TRANSFER not in MVP_INVARIANT_TYPES


@pytest.mark.parametrize(
    ("pattern", "families", "structural", "expected"),
    [
        (["find_symmetry"], 1, False, InvariantType.OPERATIONAL),
        (["find_symmetry", "apply_reflection"], 1, False, InvariantType.PROCEDURAL),
        (["detect", "transform", "verify"], 1, True, InvariantType.STRUCTURAL),
        (["find_symmetry", "apply_reflection"], 3, False, InvariantType.TRANSFER),
    ],
)
def test_classify_invariant_type(pattern, families, structural, expected):
    assert classify_invariant_type(pattern, families, structural) is expected


def test_single_step_across_families_stays_operational():
    assert classify_invariant_type(["find_symmetry"], 5) is InvariantType.OPERATIONAL


def test_invariant_type_serialization():
    inv = Invariant(
        invariant_id="INV-1",
        pattern_signature=["a", "b"],
        invariant_type=InvariantType.PROCEDURAL,
    )
    restored = Invariant.from_dict(inv.to_dict())
    assert restored.invariant_type is InvariantType.PROCEDURAL


def test_is_mvp_supported_flag():
    supported = Invariant(
        invariant_id="I1", pattern_signature=["a"], invariant_type=InvariantType.OPERATIONAL
    )
    unsupported = Invariant(
        invariant_id="I2", pattern_signature=["a"], invariant_type=InvariantType.STRUCTURAL
    )
    assert supported.is_mvp_supported is True
    assert unsupported.is_mvp_supported is False
