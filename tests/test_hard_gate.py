"""Hard gate and escalation L1-L4."""

import pytest

from core import Invariant, InvariantEvidence, InvariantState
from invariants.robustness import (
    FailureLevel,
    RobustnessConfig,
    confirm_hard_gate,
    evaluate_escalation,
    evaluate_hard_gate,
    record_ntr_violation,
)
from invariants.validation import ValidationScores
from transfer import TransferMemory, TransferRecord, TransferType


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


def _good_inv():
    return Invariant(
        invariant_id="INV-r",
        pattern_signature=["apply_reflection"],
        frequency=10,
        consistency=0.9,
        generality=0.5,
        state=InvariantState.VALIDATED,
        task_families=["reflect", "count"],
        evidence=InvariantEvidence(observations=10),
        metadata={"variations": ["color", "shape", "position", "count"]},
    )


def test_hard_gate_passes_with_transfer_memory():
    mem = TransferMemory()
    for fam in ("count", "group"):
        mem.record(
            TransferRecord(
                invariant_id="INV-r",
                source_family="reflect",
                target_family=fam,
                success=True,
                benefit=0.8,
                reasoning_reduction=0.7,
                transfer_type=TransferType.MODERATE,
            )
        )
    inv = _good_inv()
    result = evaluate_hard_gate(
        inv, _validation_ok(), memory=mem, total_families=2
    )
    assert result.promotable
    assert result.level in (FailureLevel.OK, FailureLevel.WARNING)


def test_ntr_blacklist_escalation():
    inv = _good_inv()
    inv.metadata = dict(inv.metadata or {})
    inv.metadata["ntr_violations"] = 2
    esc = evaluate_escalation(inv)
    assert esc.level is FailureLevel.BLACKLISTED


def test_confirm_hard_gate_lifecycle():
    mem = TransferMemory()
    for fam in ("count", "group"):
        mem.record(
            TransferRecord(
                invariant_id="INV-r",
                source_family="reflect",
                target_family=fam,
                success=True,
                benefit=0.8,
                reasoning_reduction=0.7,
                transfer_type=TransferType.MODERATE,
            )
        )
    inv = _good_inv()
    result = confirm_hard_gate(
        inv, _validation_ok(), memory=mem, total_families=2
    )
    assert result.promotable
    assert inv.state is InvariantState.TRANSFER_VERIFIED


def test_record_ntr_violation():
    inv = _good_inv()
    record_ntr_violation(inv)
    record_ntr_violation(inv)
    assert inv.metadata["ntr_violations"] == 2
