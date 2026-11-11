"""SkillCandidate factory from invariants."""

import pytest

from core import Invariant, InvariantEvidence, InvariantState
from skills import classify_mvp_category, from_invariant, generate_candidates


def test_classify_mvp_category():
    assert classify_mvp_category(["find_symmetry", "apply_reflection"]) == "reflection"
    assert classify_mvp_category(["apply_rotation"]) == "rotation"
    assert classify_mvp_category(["count_objects"]) == "counting"


def test_from_invariant_builds_candidate_with_scv():
    inv = Invariant(
        invariant_id="INV-r",
        pattern_signature=["find_symmetry", "apply_reflection"],
        frequency=20,
        consistency=0.9,
        generality=0.8,
        transfer_contribution=0.8,
        state=InvariantState.SKILL_CANDIDATE,
        evidence=InvariantEvidence(observations=20, transfer_events=3),
        metadata={"reasoning_value": 0.7},
    )
    cand = from_invariant(inv)
    assert cand.source_invariant_id == "INV-r"
    assert cand.metadata["mvp_category"] == "reflection"
    assert cand.metadata["status"] == "under_evaluation"
    assert cand.scv is not None
    assert cand.scv > 0


def test_generate_candidates_filters_intake():
    good = Invariant(
        invariant_id="good",
        pattern_signature=["apply_reflection"],
        frequency=10,
        consistency=0.9,
        generality=0.5,
        transfer_contribution=0.7,
        state=InvariantState.SKILL_CANDIDATE,
        evidence=InvariantEvidence(observations=10),
        metadata={"reasoning_value": 0.5},
    )
    bad = Invariant(
        invariant_id="bad",
        pattern_signature=["apply_reflection"],
        frequency=10,
        consistency=0.9,
        generality=0.5,
        transfer_contribution=0.7,
        state=InvariantState.VALIDATED,
        evidence=InvariantEvidence(observations=10),
    )
    cands = generate_candidates([good, bad])
    assert len(cands) == 1
    assert cands[0].source_invariant_id == "good"
