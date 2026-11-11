"""TransferRecord validation and TransferMemory counters."""

import pytest

from transfer import TransferMemory, TransferRecord, TransferType


def _rec(**kwargs):
    base = dict(
        invariant_id="INV-1",
        source_family="reflect",
        target_family="count",
        success=True,
        benefit=0.8,
        reasoning_reduction=0.5,
        transfer_type=TransferType.MODERATE,
    )
    base.update(kwargs)
    return TransferRecord(**base)


def test_record_rejects_empty_ids_and_out_of_range():
    with pytest.raises(ValueError):
        _rec(invariant_id="")
    with pytest.raises(ValueError):
        _rec(benefit=1.5)
    with pytest.raises(ValueError):
        _rec(reasoning_reduction=-0.1)


def test_memory_counters_coverage_summary():
    mem = TransferMemory()
    mem.record(_rec(target_family="count", success=True, benefit=0.8))
    mem.record(_rec(target_family="group", success=True, benefit=0.6))
    mem.record(_rec(target_family="count", success=False, benefit=0.0))

    assert mem.attempts("INV-1") == 3
    assert mem.successes("INV-1") == 2
    assert mem.failures("INV-1") == 1
    assert mem.coverage("INV-1") == 2

    summary = mem.summary("INV-1")
    assert summary.attempts == 3
    assert summary.coverage == 2
    assert set(summary.target_families) == {"count", "group"}
    assert summary.total_benefit == pytest.approx(1.4)


def test_memory_clear():
    mem = TransferMemory()
    mem.record(_rec())
    mem.clear()
    assert mem.attempts("INV-1") == 0
