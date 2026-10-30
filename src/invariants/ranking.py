"""Invariant ranking — InvariantScore = F × C × G × T × R (Phase 11C-3)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Mapping

from core.invariant import Invariant
from invariants.validation import (
    ValidationConfig,
    ValidationScores,
    can_rescue_by_transfer,
    is_false_positive,
    passes_consistency,
    passes_frequency,
    passes_generality,
    passes_reasoning_value,
    passes_transfer,
    score_consistency,
    score_frequency,
    score_generality,
    score_reasoning_value,
    score_transfer,
)
from invariants.specification.policy import InvariantPolicy


@dataclass(slots=True)
class RankedInvariant:
    """An invariant paired with validation scores and 1-based rank."""

    invariant: Invariant
    scores: ValidationScores
    rank: int = 0

    def to_dict(self) -> dict:
        return {
            "invariant": self.invariant.to_dict(),
            "scores": self.scores.to_dict(),
            "rank": self.rank,
        }


def compute_validation_scores(
    invariant: Invariant,
    config: ValidationConfig | None = None,
    *,
    transfer_override: float | None = None,
    policy: InvariantPolicy | None = None,
) -> ValidationScores:
    """Run the five validation tests and assemble ``ValidationScores``."""
    config = config or ValidationConfig()
    f = score_frequency(invariant, config)
    c = score_consistency(invariant)
    g = score_generality(invariant)
    t = score_transfer(invariant, config, override=transfer_override)
    r = score_reasoning_value(invariant)

    freq_ok = passes_frequency(f, config)
    rescued = can_rescue_by_transfer(
        invariant, t, frequency_passed=freq_ok, config=config
    )
    if rescued:
        freq_ok = True

    scores = ValidationScores(
        frequency=f,
        consistency=c,
        generality=g,
        transfer=t,
        reasoning_value=r,
        pass_frequency=freq_ok,
        pass_consistency=passes_consistency(c, config),
        pass_generality=passes_generality(g, config),
        pass_transfer=passes_transfer(t, config),
        pass_reasoning=passes_reasoning_value(r, config),
        rescued_by_transfer=rescued,
    )

    fp_reasons = is_false_positive(invariant, policy)
    if fp_reasons:
        scores.reasons.extend(fp_reasons)
    if not scores.pass_frequency:
        scores.reasons.append("frequency")
    if not scores.pass_consistency:
        scores.reasons.append("consistency")
    if not scores.pass_generality:
        scores.reasons.append("generality")
    if not scores.pass_transfer:
        scores.reasons.append("transfer")
    if not scores.pass_reasoning:
        scores.reasons.append("reasoning_value")
    return scores


def rank_invariants(
    candidates: list[Invariant],
    config: ValidationConfig | None = None,
    *,
    transfer_scores: Mapping[str, float] | None = None,
    policy: InvariantPolicy | None = None,
) -> list[RankedInvariant]:
    """Score and rank candidates by InvariantScore (desc).

    Candidates with score below ``min_invariant_score`` and no transfer rescue
    are still ranked but callers typically filter them via promotion.
    """
    config = config or ValidationConfig()
    transfer_scores = transfer_scores or {}
    ranked: list[RankedInvariant] = []
    for inv in candidates:
        override = transfer_scores.get(inv.invariant_id)
        scores = compute_validation_scores(
            inv, config, transfer_override=override, policy=policy
        )
        ranked.append(RankedInvariant(invariant=inv, scores=scores))

    ranked.sort(key=lambda item: (-item.scores.score, item.invariant.invariant_id))
    for index, item in enumerate(ranked, start=1):
        item.rank = index
    return ranked
