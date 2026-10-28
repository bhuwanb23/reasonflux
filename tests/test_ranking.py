"""Ranking by InvariantScore = F × C × G × T × R."""

import pytest

from core import Invariant, InvariantEvidence, InvariantState
from invariants import rank_invariants


def _inv(iid, *, freq, c, g, t, r, sig=None):
    return Invariant(
        invariant_id=iid,
        pattern_signature=sig or ["find_symmetry", "apply_reflection"],
        frequency=freq,
        consistency=c,
        generality=g,
        transfer_contribution=t,
        evidence=InvariantEvidence(observations=freq, transfer_events=int(t * 3)),
        state=InvariantState.CANDIDATE,
        metadata={"reasoning_value": r},
    )


def test_product_formula_and_ordering():
    reflection = _inv("INV-ref", freq=20, c=0.9, g=0.8, t=0.7, r=0.7)
    verify = _inv(
        "INV-ver",
        freq=50,
        c=1.0,
        g=1.0,
        t=0.0,
        r=0.0,
        sig=["verify_output"],
    )
    ranked = rank_invariants([verify, reflection])
    assert ranked[0].invariant.invariant_id == "INV-ref"
    assert ranked[0].rank == 1
    assert ranked[0].scores.score > ranked[1].scores.score
    assert ranked[1].scores.score == pytest.approx(0.0)


def test_rank_is_one_based_and_complete():
    items = [
        _inv(f"INV-{i}", freq=10 + i, c=0.8, g=0.5, t=0.5, r=0.5) for i in range(3)
    ]
    ranked = rank_invariants(items)
    assert [r.rank for r in ranked] == [1, 2, 3]
