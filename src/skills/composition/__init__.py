"""Sequential skill composition — Phase 11D-4."""

from skills.composition.compose import ComposeOutcome, ComposeResult, try_compose
from skills.composition.evaluate import (
    compute_composition_confidence,
    record_composition_outcome,
)
from skills.composition.graph import CompositionGraph
from skills.composition.lifecycle import advance_composition, promote_composition
from skills.composition.models import CompositionCandidate, CompositionState
from skills.composition.propose import propose_sequential
from skills.composition.trigger import ComposeTriggerResult, should_compose
from skills.composition.utility import CompositionUtilityBreakdown, compute_cu

__all__ = [
    "ComposeOutcome",
    "ComposeResult",
    "ComposeTriggerResult",
    "CompositionCandidate",
    "CompositionGraph",
    "CompositionState",
    "CompositionUtilityBreakdown",
    "advance_composition",
    "compute_composition_confidence",
    "compute_cu",
    "promote_composition",
    "propose_sequential",
    "record_composition_outcome",
    "should_compose",
    "try_compose",
]
