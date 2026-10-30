"""False-negative handling — transfer can rescue rare invariants (11C-3)."""

from __future__ import annotations

from core.invariant import Invariant
from invariants.validation.scores import ValidationConfig


def can_rescue_by_transfer(
    invariant: Invariant,
    transfer_score: float,
    *,
    frequency_passed: bool,
    config: ValidationConfig | None = None,
) -> bool:
    """True when high transfer should rescue a rare-but-important invariant.

    Principle: transfer can rescue rare but important invariants when
    frequency alone would discard them.
    """
    if frequency_passed:
        return False
    config = config or ValidationConfig()
    return (
        transfer_score >= config.transfer_rescue_min_t
        and invariant.frequency >= config.transfer_rescue_min_frequency
    )
