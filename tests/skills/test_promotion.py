"""Promotion criteria and lifecycle to SKILL_CANDIDATE."""

import pytest

from core import Invariant, InvariantEvidence, InvariantState, InvalidStateTransitionError
from invariants import (
    RankedInvariant,
    ValidationConfig,
    ValidationScores,
    advance_to_promotable,
    apply_promotion,
    compute_validation_scores,
    meets_promotion_criteria,
)


def _good_inv():
    return Invariant(
        invariant_id="INV-good",
        pattern_signature=["find_symmetry", "apply_reflection"],
        frequency=15,
        consistency=0.9,
        generality=0.7,
        transfer_contribution=0.8,
        evidence=InvariantEvidence(observations=15, transfer_events=3),
        state=InvariantState.CANDIDATE,
        metadata={"reasoning_value": 0.7},
    )


def test_meets_promotion_criteria():
    inv = _good_inv()
    scores = compute_validation_scores(inv)
    assert meets_promotion_criteria(scores)


def test_false_positive_blocks_promotion():
    scores = ValidationScores(
        frequency=1.0,
        consistency=1.0,
        generality=1.0,
        transfer=1.0,
        reasoning_value=1.0,
        pass_frequency=True,
        pass_consistency=True,
        pass_generality=True,
        pass_transfer=True,
        pass_reasoning=True,
        reasons=["task_specific_literal"],
    )
    assert not meets_promotion_criteria(scores)


def test_advance_to_promotable_from_candidate():
    inv = _good_inv()
    advance_to_promotable(inv)
    assert inv.state is InvariantState.SKILL_CANDIDATE


def test_apply_promotion_annotates_and_advances():
    inv = _good_inv()
    scores = compute_validation_scores(inv)
    ranked = RankedInvariant(invariant=inv, scores=scores, rank=1)
    promoted = apply_promotion(ranked)
    assert promoted is not None
    assert promoted.state is InvariantState.SKILL_CANDIDATE
    assert "validation" in promoted.metadata
    assert promoted.metadata["validation"]["rank"] == 1
    assert promoted.transfer_contribution == pytest.approx(scores.transfer)


def test_apply_promotion_rejects_weak():
    inv = Invariant(
        invariant_id="INV-weak",
        pattern_signature=["verify_output"],
        frequency=50,
        consistency=1.0,
        generality=1.0,
        state=InvariantState.CANDIDATE,
    )
    scores = compute_validation_scores(inv)
    ranked = RankedInvariant(invariant=inv, scores=scores, rank=1)
    assert apply_promotion(ranked) is None
