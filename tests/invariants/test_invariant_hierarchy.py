"""Tests for operation → pattern → invariant hierarchy and IS strength."""

import pytest

from core import Invariant, InvariantType
from invariants import (
    HierarchyLevel,
    InvariantHierarchy,
    compute_invariant_strength,
    hierarchy_level_for,
    is_above_threshold,
    summarize_specification,
)
from invariants.strength import MINIMUM_INVARIANT_STRENGTH


def test_compute_invariant_strength():
    assert compute_invariant_strength(10, 0.8, 0.5) == pytest.approx(4.0)


def test_strength_rejects_out_of_range_inputs():
    with pytest.raises(ValueError):
        compute_invariant_strength(-1, 0.5, 0.5)
    with pytest.raises(ValueError):
        compute_invariant_strength(1, 1.5, 0.5)
    with pytest.raises(ValueError):
        compute_invariant_strength(1, 0.5, -0.1)


def test_strength_threshold_gate():
    strong = Invariant(
        invariant_id="I1", pattern_signature=["a", "b"], frequency=10,
        consistency=1.0, generality=1.0,
    )
    weak = Invariant(
        invariant_id="I2", pattern_signature=["a"], frequency=1,
        consistency=0.5, generality=0.5,
    )
    assert is_above_threshold(strong) is True
    assert is_above_threshold(weak) is False
    assert strong.strength >= MINIMUM_INVARIANT_STRENGTH


@pytest.mark.parametrize(
    ("pattern", "itype", "expected"),
    [
        (["find_symmetry"], InvariantType.OPERATIONAL, HierarchyLevel.OPERATION),
        (
            ["find_symmetry", "apply_reflection"],
            InvariantType.PROCEDURAL,
            HierarchyLevel.PATTERN,
        ),
        (
            ["detect", "transform", "verify"],
            InvariantType.PROCEDURAL,
            HierarchyLevel.INVARIANT,
        ),
    ],
)
def test_hierarchy_level_mapping(pattern, itype, expected):
    inv = Invariant(invariant_id="I1", pattern_signature=pattern, invariant_type=itype)
    assert hierarchy_level_for(inv) == expected


def test_hierarchy_builds_from_invariants():
    invs = [
        Invariant(invariant_id="op", pattern_signature=["a"], invariant_type=InvariantType.OPERATIONAL),
        Invariant(
            invariant_id="pat",
            pattern_signature=["a", "b"],
            invariant_type=InvariantType.PROCEDURAL,
        ),
        Invariant(
            invariant_id="inv",
            pattern_signature=["a", "b", "c"],
            invariant_type=InvariantType.PROCEDURAL,
        ),
    ]
    hierarchy = InvariantHierarchy.build(invs)
    assert hierarchy.members_at(HierarchyLevel.OPERATION) == ["op"]
    assert hierarchy.members_at(HierarchyLevel.PATTERN) == ["pat"]
    assert hierarchy.members_at(HierarchyLevel.INVARIANT) == ["inv"]
    assert len(hierarchy.to_dict()["nodes"]) == 3


def test_hierarchy_empty_level_returns_empty_list():
    hierarchy = InvariantHierarchy.build([])
    assert hierarchy.members_at(HierarchyLevel.OPERATION) == []


def test_specification_summary_is_machine_readable():
    spec = summarize_specification()
    assert set(spec["qualification_rules"]) == {
        "recurrence",
        "stability",
        "generality",
        "transfer_utility",
    }
    assert spec["mvp_supported_types"] == ["operational", "procedural"]
    assert {c["name"] for c in spec["rejection_criteria"]} == {
        "rare_event",
        "task_specific_detail",
        "universal_noise",
        "accidental_correlation",
    }
    assert "definition" in spec
