"""Transfer promotion gate — ITS / NTR / attempts / lifecycle."""

import pytest

from core import Invariant, InvariantEvidence, InvariantState
from invariants.validation import ValidationScores
from transfer import (
    TransferConfig,
    TransferMemory,
    TransferRecord,
    TransferScores,
    TransferType,
    confirm_transfer,
    evaluate_transfer_gate,
)


def _invariant(state=InvariantState.VALIDATED):
    return Invariant(
        invariant_id="INV-r",
        pattern_signature=["apply_reflection"],
        frequency=10,
        consistency=0.9,
        generality=0.5,
        state=state,
        evidence=InvariantEvidence(observations=10),
    )


def _validation_ok():
    return ValidationScores(
        frequency=0.8,
        consistency=0.9,
        generality=0.5,
        transfer=0.7,
        reasoning_value=0.6,
        pass_frequency=True,
        pass_consistency=True,
        pass_generality=True,
        pass_transfer=True,
        pass_reasoning=True,
    )


def test_gate_requires_its_attempts_and_blocks_ntr():
    cfg = TransferConfig(min_its=0.5, min_transfer_attempts=2, ntr_limit=0.3)
    inv = _invariant()
    validation = _validation_ok()

    low_its = TransferScores(its=0.2, ntr=0.0, tu=0.5, attempts=3, weighted=0.1)
    result = evaluate_transfer_gate(inv, validation, low_its, cfg)
    assert result.rejected
    assert "its_below_threshold" in result.reasons

    few = TransferScores(its=0.8, ntr=0.0, tu=0.5, attempts=1, weighted=0.4)
    result = evaluate_transfer_gate(inv, validation, few, cfg)
    assert "insufficient_transfer_attempts" in result.reasons

    # Reflection applied to pure counting → high failure rate
    ntr = TransferScores(its=0.6, ntr=0.5, tu=0.2, attempts=4, weighted=0.12)
    result = evaluate_transfer_gate(inv, validation, ntr, cfg)
    assert result.rejected
    assert "negative_transfer" in result.reasons


def test_confirm_transfer_advances_lifecycle():
    mem = TransferMemory()
    for family, benefit in (("count", 0.8), ("group", 0.8), ("rotate", 0.7)):
        mem.record(
            TransferRecord(
                invariant_id="INV-r",
                source_family="reflect",
                target_family=family,
                success=True,
                benefit=benefit,
                reasoning_reduction=0.7,
                transfer_type=TransferType.MODERATE,
            )
        )
    inv = _invariant(InvariantState.VALIDATED)
    result = confirm_transfer(
        inv,
        mem,
        TransferConfig(),
        validation_scores=_validation_ok(),
        total_families=3,
    )
    assert result.promotable
    assert inv.state is InvariantState.TRANSFER_VERIFIED
    assert inv.transfer_contribution == pytest.approx(result.scores.its)
    assert inv.evidence.transfer_events >= 3


def test_confirm_blocks_negative_transfer_to_counting():
    mem = TransferMemory()
    for _ in range(3):
        mem.record(
            TransferRecord(
                invariant_id="INV-r",
                source_family="reflect",
                target_family="pure_count",
                success=False,
                benefit=0.0,
                reasoning_reduction=0.0,
                transfer_type=TransferType.MODERATE,
            )
        )
    inv = _invariant()
    result = confirm_transfer(
        inv, mem, TransferConfig(ntr_limit=0.3), validation_scores=_validation_ok()
    )
    assert result.rejected
    assert "negative_transfer" in result.reasons
    assert inv.state is InvariantState.VALIDATED
