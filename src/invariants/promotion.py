"""Promotion criteria and lifecycle advancement (Phase 11C-3)."""

from __future__ import annotations

from core.invariant import Invariant
from core.states import INVARIANT_TRANSITIONS, InvariantState, can_transition
from invariants.ranking import RankedInvariant
from invariants.specification.confidence import compute_confidence
from invariants.validation.scores import ValidationConfig, ValidationScores

_FP_TAGS = frozenset(
    {"task_specific_literal", "failed_variation_survival", "low_vst"}
)

# Preferred forward path to Promotable (SKILL_CANDIDATE).
_PROMOTION_PATH: tuple[InvariantState, ...] = (
    InvariantState.DETECTED,
    InvariantState.VALIDATED,
    InvariantState.TRANSFER_VERIFIED,
    InvariantState.SKILL_CANDIDATE,
)


def meets_promotion_criteria(
    scores: ValidationScores, config: ValidationConfig | None = None
) -> bool:
    """True when F,C,G,T,R gates all pass and no false-positive reasons remain."""
    config = config or ValidationConfig()
    if scores.score < config.min_invariant_score and not scores.rescued_by_transfer:
        return False
    if not (
        scores.pass_frequency
        and scores.pass_consistency
        and scores.pass_generality
        and scores.pass_transfer
        and scores.pass_reasoning
    ):
        return False
    if any(r in _FP_TAGS for r in scores.reasons):
        return False
    return True


def advance_to_promotable(invariant: Invariant) -> Invariant:
    """Advance lifecycle toward ``SKILL_CANDIDATE`` (doc: Promotable)."""
    for target in _PROMOTION_PATH:
        if invariant.state is InvariantState.SKILL_CANDIDATE:
            break
        if invariant.state is target:
            continue
        if can_transition(invariant.state, target, INVARIANT_TRANSITIONS):
            invariant.transition_to(target)
            continue
        # Insert the next legal hop toward target when a direct jump is illegal.
        for hop in _PROMOTION_PATH:
            if hop is target:
                break
            if can_transition(invariant.state, hop, INVARIANT_TRANSITIONS):
                invariant.transition_to(hop)
        if can_transition(invariant.state, target, INVARIANT_TRANSITIONS):
            invariant.transition_to(target)
    if invariant.state is not InvariantState.SKILL_CANDIDATE:
        raise ValueError(
            f"Could not advance {invariant.invariant_id!r} to skill_candidate "
            f"(stuck at {invariant.state.value!r})"
        )
    return invariant


def apply_promotion(
    ranked: RankedInvariant, config: ValidationConfig | None = None
) -> Invariant | None:
    """If criteria pass, annotate + advance the invariant; else return None."""
    config = config or ValidationConfig()
    if not meets_promotion_criteria(ranked.scores, config):
        return None

    inv = ranked.invariant
    scores = ranked.scores
    inv.transfer_contribution = scores.transfer
    inv.confidence = compute_confidence(inv)
    inv.metadata = dict(inv.metadata or {})
    inv.metadata["validation"] = {**scores.to_dict(), "rank": ranked.rank}
    if scores.transfer > 0 and inv.evidence.transfer_events == 0:
        inv.evidence.transfer_events = max(1, int(round(scores.transfer * 3)))
    advance_to_promotable(inv)
    return inv
