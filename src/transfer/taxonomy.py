"""Transfer taxonomy — near / moderate / compositional / structural (11C-4)."""

from __future__ import annotations

from enum import Enum
from typing import Sequence


class TransferType(str, Enum):
    """How far an invariant travels across task families."""

    NEAR = "near"
    MODERATE = "moderate"
    COMPOSITIONAL = "compositional"
    STRUCTURAL = "structural"


_BANDS: dict[TransferType, str] = {
    TransferType.NEAR: "very_high",
    TransferType.MODERATE: "medium",
    TransferType.COMPOSITIONAL: "medium_to_high",
    TransferType.STRUCTURAL: "high",
}


def expected_transfer_band(transfer_type: TransferType) -> str:
    """Return the expected transfer strength band for a transfer type."""
    return _BANDS[transfer_type]


def classify_transfer(
    source_family: str,
    target_family: str,
    *,
    source_ops: Sequence[str] | None = None,
    target_ops: Sequence[str] | None = None,
    structural: bool = False,
) -> TransferType:
    """Classify transfer between two task contexts.

    - same family or identical op sets → NEAR
    - shared core ops, different family → MODERATE
    - target contains source core plus extras → COMPOSITIONAL
    - structural=True or 2+ extra mechanisms → STRUCTURAL
    """
    src_family = (source_family or "").strip()
    tgt_family = (target_family or "").strip()
    src = {str(op).strip() for op in (source_ops or []) if str(op).strip()}
    tgt = {str(op).strip() for op in (target_ops or []) if str(op).strip()}

    if structural:
        return TransferType.STRUCTURAL

    if src_family and tgt_family and src_family == tgt_family:
        return TransferType.NEAR
    if src and tgt and src == tgt:
        return TransferType.NEAR

    if src and tgt:
        shared = src & tgt
        extra = tgt - src
        if shared and not extra:
            return TransferType.NEAR if src_family == tgt_family else TransferType.MODERATE
        if shared and len(extra) >= 2:
            return TransferType.STRUCTURAL
        if shared and extra:
            return TransferType.COMPOSITIONAL
        if shared:
            return TransferType.MODERATE

    # Different families with no op info → moderate by default.
    if src_family and tgt_family and src_family != tgt_family:
        return TransferType.MODERATE
    return TransferType.NEAR
