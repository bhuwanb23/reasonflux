"""E1-E5 edge case hardening."""

import pytest

from core import Invariant, InvariantEvidence, InvariantState
from invariants.robustness import (
    diminishing_transfer_utility,
    jaccard_similarity,
    should_merge_signatures,
)
from invariants.validation import can_rescue_by_transfer, ValidationConfig


def test_e3_similarity_merge_hint():
    a = ["reflect", "find_symmetry", "align", "verify_core", "step5", "step6"]
    b = a + ["extra"]
    assert jaccard_similarity(a, b) >= 0.85
    assert should_merge_signatures(a, b)


def test_e4_saturation():
    base = 0.8
    assert diminishing_transfer_utility(3, base) == pytest.approx(base)
    assert diminishing_transfer_utility(10, base) < base


def test_e2_transfer_rescue():
    inv = Invariant(
        invariant_id="r",
        pattern_signature=["reflect"],
        frequency=2,
        evidence=InvariantEvidence(observations=3),
        metadata={"variations": ["color", "shape", "position", "count"]},
    )
    cfg = ValidationConfig()
    assert can_rescue_by_transfer(inv, 0.8, frequency_passed=False, config=cfg)
