"""ITS / NTR / TU / confidence math."""

import pytest

from transfer import (
    TransferConfig,
    TransferMemory,
    TransferRecord,
    TransferType,
    compute_its,
    compute_ntr,
    compute_transfer_score,
    compute_tu,
)


def test_its_ntr_tu_basic():
    assert compute_its(2, [0.8, 0.6]) == pytest.approx(0.7)
    assert compute_ntr(4, 1) == pytest.approx(0.25)
    assert compute_tu(1.0, 0.5, 0.5) == pytest.approx(0.25)


def test_zero_attempt_edge_cases():
    assert compute_its(0, []) == 0.0
    assert compute_ntr(0, 0) == 0.0
    scores = compute_transfer_score(TransferMemory(), "missing")
    assert scores.its == 0.0
    assert scores.weighted == 0.0
    assert scores.attempts == 0


def test_confidence_scales_with_attempts():
    mem = TransferMemory()
    for benefit in (0.9, 0.9, 0.9, 0.9, 0.9):
        mem.record(
            TransferRecord(
                invariant_id="INV",
                source_family="a",
                target_family="b",
                success=True,
                benefit=benefit,
                reasoning_reduction=1.0,
                transfer_type=TransferType.NEAR,
            )
        )
    cfg = TransferConfig(confidence_attempts_norm=5)
    scores = compute_transfer_score(mem, "INV", cfg, total_families=1)
    assert scores.confidence == pytest.approx(1.0)
    assert scores.its == pytest.approx(0.9)
    assert scores.weighted == pytest.approx(scores.its * scores.tu)


def test_transfer_config_from_dict_and_validation():
    cfg = TransferConfig.from_dict({"min_its": 0.6, "ntr_limit": 0.2, "unknown": 1})
    assert cfg.min_its == pytest.approx(0.6)
    assert cfg.ntr_limit == pytest.approx(0.2)
    with pytest.raises(ValueError):
        TransferConfig(min_transfer_attempts=0)
