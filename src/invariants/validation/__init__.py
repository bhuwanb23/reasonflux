"""Phase 11C-3 validation tests and score helpers."""

from invariants.validation.consistency import passes_consistency, score_consistency
from invariants.validation.false_negatives import can_rescue_by_transfer
from invariants.validation.false_positives import is_false_positive
from invariants.validation.frequency import passes_frequency, score_frequency
from invariants.validation.generality import passes_generality, score_generality
from invariants.validation.reasoning_value import (
    passes_reasoning_value,
    score_reasoning_value,
)
from invariants.validation.scores import ValidationConfig, ValidationScores, clamp01
from invariants.validation.transfer import passes_transfer, score_transfer

__all__ = [
    "ValidationConfig",
    "ValidationScores",
    "can_rescue_by_transfer",
    "clamp01",
    "is_false_positive",
    "passes_consistency",
    "passes_frequency",
    "passes_generality",
    "passes_reasoning_value",
    "passes_transfer",
    "score_consistency",
    "score_frequency",
    "score_generality",
    "score_reasoning_value",
    "score_transfer",
]
