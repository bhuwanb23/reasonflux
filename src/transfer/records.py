"""Transfer evidence records (Phase 11C-4)."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from transfer.taxonomy import TransferType


@dataclass(slots=True)
class TransferRecord:
    """One transfer attempt of an invariant onto a target task family."""

    invariant_id: str
    source_family: str
    target_family: str
    success: bool
    benefit: float = 0.0
    reasoning_reduction: float = 0.0
    transfer_type: TransferType = TransferType.NEAR
    timestamp: float = 0.0

    def __post_init__(self) -> None:
        if not self.invariant_id or not str(self.invariant_id).strip():
            raise ValueError("invariant_id must be a non-empty string")
        if not self.source_family or not str(self.source_family).strip():
            raise ValueError("source_family must be a non-empty string")
        if not self.target_family or not str(self.target_family).strip():
            raise ValueError("target_family must be a non-empty string")
        if not 0.0 <= self.benefit <= 1.0:
            raise ValueError("benefit must be in [0, 1]")
        if not 0.0 <= self.reasoning_reduction <= 1.0:
            raise ValueError("reasoning_reduction must be in [0, 1]")
        if self.timestamp < 0:
            raise ValueError("timestamp must be >= 0")
        if not isinstance(self.transfer_type, TransferType):
            self.transfer_type = TransferType(self.transfer_type)

    def to_dict(self) -> dict[str, Any]:
        data = asdict(self)
        data["transfer_type"] = self.transfer_type.value
        return data

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> TransferRecord:
        return cls(
            invariant_id=data["invariant_id"],
            source_family=data["source_family"],
            target_family=data["target_family"],
            success=bool(data["success"]),
            benefit=float(data.get("benefit", 0.0)),
            reasoning_reduction=float(data.get("reasoning_reduction", 0.0)),
            transfer_type=TransferType(
                data.get("transfer_type", TransferType.NEAR.value)
            ),
            timestamp=float(data.get("timestamp", 0.0)),
        )


@dataclass(slots=True)
class TransferMemorySummary:
    """Aggregated transfer history for one invariant."""

    invariant_id: str
    attempts: int = 0
    successes: int = 0
    failures: int = 0
    total_benefit: float = 0.0
    total_reduction: float = 0.0
    target_families: list[str] = None  # type: ignore[assignment]

    def __post_init__(self) -> None:
        if self.target_families is None:
            self.target_families = []

    @property
    def coverage(self) -> int:
        return len(self.target_families)

    def to_dict(self) -> dict[str, Any]:
        return {
            "invariant_id": self.invariant_id,
            "attempts": self.attempts,
            "successes": self.successes,
            "failures": self.failures,
            "total_benefit": self.total_benefit,
            "total_reduction": self.total_reduction,
            "target_families": list(self.target_families),
            "coverage": self.coverage,
        }
