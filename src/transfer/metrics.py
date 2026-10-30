"""Invariant Transfer Score (ITS), Transfer Utility (TU), NTR (Phase 11C-4)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Sequence

from transfer.memory import TransferMemory


@dataclass(slots=True)
class TransferConfig:
    """Thresholds for transfer-aware discovery and promotion."""

    min_transfer_attempts: int = 2
    min_its: float = 0.5
    ntr_limit: float = 0.3
    tu_reduction_norm: float = 1.0
    confidence_attempts_norm: float = 5.0

    def __post_init__(self) -> None:
        if self.min_transfer_attempts < 1:
            raise ValueError("min_transfer_attempts must be >= 1")
        if not 0.0 <= self.min_its <= 1.0:
            raise ValueError("min_its must be in [0, 1]")
        if not 0.0 <= self.ntr_limit <= 1.0:
            raise ValueError("ntr_limit must be in [0, 1]")
        if self.tu_reduction_norm <= 0:
            raise ValueError("tu_reduction_norm must be > 0")
        if self.confidence_attempts_norm <= 0:
            raise ValueError("confidence_attempts_norm must be > 0")

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> TransferConfig:
        known = {f for f in cls.__dataclass_fields__}
        payload = {k: v for k, v in (data or {}).items() if k in known}
        return cls(**payload)


@dataclass(slots=True)
class TransferScores:
    """ITS / NTR / TU bundle for one invariant."""

    its: float = 0.0
    ntr: float = 0.0
    tu: float = 0.0
    success_rate: float = 0.0
    coverage: float = 0.0
    attempts: int = 0
    confidence: float = 0.0
    weighted: float = 0.0  # refined T = ITS × TU

    def to_dict(self) -> dict[str, Any]:
        return {
            "its": self.its,
            "ntr": self.ntr,
            "tu": self.tu,
            "success_rate": self.success_rate,
            "coverage": self.coverage,
            "attempts": self.attempts,
            "confidence": self.confidence,
            "weighted": self.weighted,
        }


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def compute_its(attempts: int, benefits: Sequence[float]) -> float:
    """ITS = sum(TransferBenefits) / TransferAttempts."""
    if attempts <= 0:
        return 0.0
    return _clamp01(sum(float(b) for b in benefits) / attempts)


def compute_ntr(attempts: int, failures: int) -> float:
    """NTR = FailedTransferAttempts / TotalTransferAttempts."""
    if attempts <= 0:
        return 0.0
    if failures < 0:
        raise ValueError("failures must be >= 0")
    return _clamp01(failures / attempts)


def compute_tu(
    success_rate: float, reasoning_reduction: float, task_coverage: float
) -> float:
    """TU = TransferSuccess × ReasoningReduction × TaskCoverage."""
    return _clamp01(
        _clamp01(success_rate)
        * _clamp01(reasoning_reduction)
        * _clamp01(task_coverage)
    )


def compute_transfer_score(
    memory: TransferMemory,
    invariant_id: str,
    config: TransferConfig | None = None,
    *,
    total_families: int = 1,
) -> TransferScores:
    """Compute ITS, NTR, TU, confidence, and weighted T for an invariant."""
    config = config or TransferConfig()
    summary = memory.summary(invariant_id)
    attempts = summary.attempts
    if attempts == 0:
        return TransferScores()

    benefits = [r.benefit for r in memory.records_for(invariant_id)]
    its = compute_its(attempts, benefits)
    ntr = compute_ntr(attempts, summary.failures)
    success_rate = summary.successes / attempts
    mean_reduction = summary.total_reduction / attempts
    coverage = summary.coverage / max(total_families, 1)
    tu = compute_tu(success_rate, mean_reduction, coverage)
    confidence = _clamp01(attempts / config.confidence_attempts_norm) * success_rate
    return TransferScores(
        its=its,
        ntr=ntr,
        tu=tu,
        success_rate=success_rate,
        coverage=_clamp01(coverage),
        attempts=attempts,
        confidence=_clamp01(confidence),
        weighted=_clamp01(its * tu),
    )
