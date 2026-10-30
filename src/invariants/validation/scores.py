"""ValidationScores and shared normalization helpers (Phase 11C-3)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


def clamp01(value: float) -> float:
    """Clamp a float into [0, 1]."""
    return max(0.0, min(1.0, float(value)))


def normalize_count(count: float, norm: float) -> float:
    """Map a non-negative count to [0, 1] via ``min(1, count / norm)``."""
    if norm <= 0:
        raise ValueError("norm must be > 0")
    if count < 0:
        raise ValueError("count must be >= 0")
    return clamp01(count / norm)


@dataclass(slots=True)
class ValidationConfig:
    """Thresholds for Phase 11C-3 ranking and promotion."""

    freq_norm: float = 10.0
    transfer_norm: float = 3.0
    min_f: float = 0.3
    min_c: float = 0.6
    min_g: float = 0.3
    min_t: float = 0.1
    min_r: float = 0.1
    min_invariant_score: float = 0.01
    transfer_rescue_min_t: float = 0.7
    transfer_rescue_min_frequency: int = 2

    def __post_init__(self) -> None:
        if self.freq_norm <= 0 or self.transfer_norm <= 0:
            raise ValueError("freq_norm and transfer_norm must be > 0")
        for name in ("min_f", "min_c", "min_g", "min_t", "min_r", "min_invariant_score"):
            value = getattr(self, name)
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0, 1]")
        if self.transfer_rescue_min_frequency < 1:
            raise ValueError("transfer_rescue_min_frequency must be >= 1")

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> ValidationConfig:
        known = {f for f in cls.__dataclass_fields__}
        payload = {k: v for k, v in (data or {}).items() if k in known}
        return cls(**payload)


@dataclass(slots=True)
class ValidationScores:
    """Per-candidate F, C, G, T, R scores and product InvariantScore."""

    frequency: float = 0.0
    consistency: float = 0.0
    generality: float = 0.0
    transfer: float = 0.0
    reasoning_value: float = 0.0
    pass_frequency: bool = False
    pass_consistency: bool = False
    pass_generality: bool = False
    pass_transfer: bool = False
    pass_reasoning: bool = False
    rescued_by_transfer: bool = False
    reasons: list[str] = field(default_factory=list)

    @property
    def score(self) -> float:
        """InvariantScore = F × C × G × T × R."""
        return (
            self.frequency
            * self.consistency
            * self.generality
            * self.transfer
            * self.reasoning_value
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "frequency": self.frequency,
            "consistency": self.consistency,
            "generality": self.generality,
            "transfer": self.transfer,
            "reasoning_value": self.reasoning_value,
            "score": self.score,
            "pass_frequency": self.pass_frequency,
            "pass_consistency": self.pass_consistency,
            "pass_generality": self.pass_generality,
            "pass_transfer": self.pass_transfer,
            "pass_reasoning": self.pass_reasoning,
            "rescued_by_transfer": self.rescued_by_transfer,
            "reasons": list(self.reasons),
        }
