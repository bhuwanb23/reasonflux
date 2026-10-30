"""Transfer illusion weighting — WTS = TS × difficulty (F3)."""

from __future__ import annotations

from transfer.taxonomy import TransferType
from invariants.robustness.config import RobustnessConfig


def difficulty_factor(
    transfer_type: TransferType, config: RobustnessConfig | None = None
) -> float:
    """Map transfer taxonomy to difficulty weight (near discounted)."""
    config = config or RobustnessConfig()
    mapping = {
        TransferType.NEAR: config.difficulty_near,
        TransferType.MODERATE: config.difficulty_moderate,
        TransferType.COMPOSITIONAL: config.difficulty_compositional,
        TransferType.STRUCTURAL: config.difficulty_structural,
    }
    return mapping.get(transfer_type, config.difficulty_moderate)


def compute_wts(
    transfer_score: float,
    transfer_type: TransferType,
    config: RobustnessConfig | None = None,
) -> float:
    """Weighted transfer score for meaningful transfer (harder = higher)."""
    config = config or RobustnessConfig()
    ts = max(0.0, min(1.0, float(transfer_score)))
    return ts * difficulty_factor(transfer_type, config)


def meaningful_transfer_weight(
    benefit: float, transfer_type: TransferType, config: RobustnessConfig | None = None
) -> float:
    """Discount near-transfer benefits when aggregating promotion evidence."""
    return compute_wts(benefit, transfer_type, config)
