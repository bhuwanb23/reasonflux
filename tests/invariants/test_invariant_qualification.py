"""Tests for invariant qualification rules (the four 11C-1 conditions)."""

import pytest

from core import Invariant, InvariantEvidence, InvariantType
from invariants import (
    InvariantPolicy,
    qualify_invariant,
    require_qualification,
)


def _qualified(**overrides):
    params = dict(
        invariant_id="INV-ok",
        pattern_signature=["find_symmetry", "apply_reflection"],
        frequency=5,
        consistency=0.9,
        generality=0.7,
        task_families=["reflection", "counting"],
        evidence=InvariantEvidence(
            observations=5,
            task_families=["reflection", "counting"],
            transfer_events=2,
            reuse_events=3,
        ),
        invariant_type=InvariantType.PROCEDURAL,
        origin="synthetic",
    )
    params.update(overrides)
    return Invariant(**params)


def test_fully_qualified_invariant_has_no_violations():
    assert qualify_invariant(_qualified()) == []
    assert require_qualification(_qualified()).invariant_id == "INV-ok"


def test_rule_recurrence_rejects_one_off():
    inv = _qualified(frequency=1)
    violations = qualify_invariant(inv)
    assert [v.rule for v in violations] == ["recurrence"]


def test_rule_stability_rejects_inconsistent_structure():
    inv = _qualified(consistency=0.2)
    violations = qualify_invariant(inv)
    assert [v.rule for v in violations] == ["stability"]


def test_rule_generality_rejects_single_family():
    inv = _qualified(
        task_families=["reflection"],
        evidence=InvariantEvidence(
            observations=5, task_families=["reflection"], transfer_events=1
        ),
    )
    violations = qualify_invariant(inv)
    assert [v.rule for v in violations] == ["generality"]


def test_rule_transfer_utility_requires_transfer_evidence():
    inv = _qualified(evidence=InvariantEvidence(observations=5, transfer_events=0, task_families=["a", "b"]))
    violations = qualify_invariant(inv)
    assert [v.rule for v in violations] == ["transfer_utility"]


def test_transfer_requirement_can_be_disabled_by_policy():
    inv = _qualified(evidence=InvariantEvidence(observations=5, task_families=["a", "b"]))
    policy = InvariantPolicy(require_transfer_evidence=False)
    assert qualify_invariant(inv, policy) == []


def test_taxonomy_scope_enforced_unless_allowed():
    inv = _qualified(invariant_type=InvariantType.STRUCTURAL)
    assert [v.rule for v in qualify_invariant(inv)] == ["taxonomy_scope"]
    assert qualify_invariant(inv, allow_unsupported_type=True) == []


def test_multiple_violations_are_all_reported():
    inv = _qualified(frequency=1, consistency=0.1)
    rules = {v.rule for v in qualify_invariant(inv)}
    assert rules == {"recurrence", "stability"}


def test_require_qualification_raises_with_detail():
    with pytest.raises(ValueError, match="recurrence"):
        require_qualification(_qualified(frequency=0))


def test_policy_thresholds_are_configurable():
    inv = _qualified(frequency=3)
    strict = InvariantPolicy(min_frequency=5)
    assert [v.rule for v in qualify_invariant(inv, strict)] == ["recurrence"]


def test_policy_rejects_invalid_bounds():
    with pytest.raises(ValueError):
        InvariantPolicy(min_consistency=2.0)
    with pytest.raises(ValueError):
        InvariantPolicy(min_frequency=0)


def test_policy_from_dict_ignores_unknown_keys():
    policy = InvariantPolicy.from_dict({"min_frequency": 4, "unknown": True})
    assert policy.min_frequency == 4
