"""Evidence buckets and confidence."""

import pytest

from skills import SkillEvidence, compute_skill_confidence, seed_evidence_from_invariant


def test_seed_and_confidence():
    ev = seed_evidence_from_invariant(
        invariant_id="INV-r",
        frequency=10,
        consistency=0.9,
        transfer_score=0.8,
        transfer_events=3,
    )
    assert len(ev.discovery) == 1
    assert len(ev.transfer) >= 1
    conf = compute_skill_confidence(ev)
    assert 0.0 < conf <= 1.0


def test_negative_evidence_lowers_confidence():
    base = SkillEvidence(
        discovery=[{"x": 1}, {"x": 2}, {"x": 3}],
        transfer=[{"t": 1}, {"t": 2}, {"t": 3}],
        consistency=1.0,
    )
    high = compute_skill_confidence(base)
    base.negative = [{"n": i} for i in range(5)]
    low = compute_skill_confidence(base)
    assert low < high
