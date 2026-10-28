"""Tests for invariant evidence and confidence models."""

import pytest

from core import Invariant, InvariantConfidence, InvariantEvidence
from invariants import compute_confidence, confidence_from_evidence


def test_evidence_counters_validate():
    with pytest.raises(ValueError):
        InvariantEvidence(observations=-1)
    with pytest.raises(ValueError):
        InvariantEvidence(transfer_events=-1)


def test_evidence_recording():
    ev = InvariantEvidence()
    ev.record_observation("reflection")
    ev.record_observation("reflection")
    ev.record_observation("counting")
    ev.record_transfer(2)
    ev.record_reuse()
    assert ev.observations == 3
    assert ev.task_family_count == 2
    assert ev.transfer_events == 2
    assert ev.reuse_events == 1


def test_evidence_round_trip():
    ev = InvariantEvidence(
        observations=4, task_families=["a"], transfer_events=1, reuse_events=2
    )
    assert InvariantEvidence.from_dict(ev.to_dict()) == ev


def test_weak_confidence_for_thin_evidence():
    ev = InvariantEvidence(observations=1, task_families=["a"])
    assert confidence_from_evidence(ev, consistency=0.1) is InvariantConfidence.WEAK


def test_moderate_confidence_mid_evidence():
    ev = InvariantEvidence(observations=4, task_families=["a", "b"], transfer_events=1)
    assert confidence_from_evidence(ev, consistency=0.6) is InvariantConfidence.MODERATE


def test_strong_confidence_for_rich_evidence():
    ev = InvariantEvidence(observations=9, task_families=["a", "b", "c"], transfer_events=3)
    assert confidence_from_evidence(ev, consistency=0.95) is InvariantConfidence.STRONG


def test_invariant_observation_updates_frequency_and_evidence():
    inv = Invariant(invariant_id="I1", pattern_signature=["a"], frequency=0)
    inv.record_observation("reflection")
    inv.record_observation("counting")
    assert inv.frequency == 2
    assert inv.evidence.observations == 2
    assert inv.evidence.task_family_count == 2
    assert set(inv.task_families) == {"reflection", "counting"}


def test_compute_confidence_uses_invariant_evidence():
    inv = Invariant(
        invariant_id="I1",
        pattern_signature=["a", "b"],
        consistency=0.95,
        evidence=InvariantEvidence(
            observations=9, task_families=["a", "b", "c"], transfer_events=3
        ),
    )
    assert compute_confidence(inv) is InvariantConfidence.STRONG


def test_invariant_evidence_round_trip_through_invariant():
    inv = Invariant(
        invariant_id="I1",
        pattern_signature=["a"],
        evidence=InvariantEvidence(observations=3, task_families=["x"], transfer_events=1),
    )
    restored = Invariant.from_dict(inv.to_dict())
    assert restored.evidence.observations == 3
    assert restored.evidence.transfer_events == 1
