"""EFU vs lifetime cost promotion economics."""

from core import SkillCandidate
from skills import (
    SkillConfig,
    evaluate_promotion_economics,
    expected_future_utility,
    lifetime_cost,
)


def test_strong_candidate_worthwhile():
    cand = SkillCandidate(
        candidate_id="sc1",
        source_invariant_id="inv1",
        expected_reuse=0.8,
        abstraction_gain=0.7,
        transfer_score=0.7,
        creation_cost=0.1,
        metadata={"composition_potential": 0.5},
    )
    proj = evaluate_promotion_economics(cand, SkillConfig())
    assert proj.worthwhile
    assert expected_future_utility(cand) > lifetime_cost(cand)


def test_expensive_low_value_not_worthwhile():
    cand = SkillCandidate(
        candidate_id="sc2",
        source_invariant_id="inv2",
        expected_reuse=0.0,
        abstraction_gain=0.0,
        transfer_score=0.0,
        creation_cost=2.0,
    )
    proj = evaluate_promotion_economics(cand)
    assert not proj.worthwhile
