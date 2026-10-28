"""Validation orchestrator — candidates → ranked / promotable (Phase 11C-3)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence

from core.invariant import Invariant
from core.states import InvariantState
from invariants.promotion import apply_promotion, meets_promotion_criteria
from invariants.ranking import RankedInvariant, rank_invariants
from invariants.specification.policy import InvariantPolicy
from invariants.validation.scores import ValidationConfig


@dataclass(slots=True)
class ValidationStatistics:
    """Counts from a validation run."""

    candidates_in: int = 0
    ranked: int = 0
    validated: int = 0
    transfer_verified: int = 0
    promotable: int = 0
    rejected: int = 0

    def to_dict(self) -> dict:
        return {
            "candidates_in": self.candidates_in,
            "ranked": self.ranked,
            "validated": self.validated,
            "transfer_verified": self.transfer_verified,
            "promotable": self.promotable,
            "rejected": self.rejected,
        }


@dataclass(slots=True)
class ValidationResult:
    """Outputs of ``validate_and_rank``."""

    ranked: list[RankedInvariant] = field(default_factory=list)
    validated: list[Invariant] = field(default_factory=list)
    transfer_verified: list[Invariant] = field(default_factory=list)
    promotable: list[Invariant] = field(default_factory=list)
    rejected: list[tuple[Invariant, list[str]]] = field(default_factory=list)
    statistics: ValidationStatistics = field(default_factory=ValidationStatistics)

    def to_dict(self) -> dict:
        return {
            "ranked": [r.to_dict() for r in self.ranked],
            "validated": [i.to_dict() for i in self.validated],
            "transfer_verified": [i.to_dict() for i in self.transfer_verified],
            "promotable": [i.to_dict() for i in self.promotable],
            "rejected": [
                {"invariant": inv.to_dict(), "reasons": list(reasons)}
                for inv, reasons in self.rejected
            ],
            "statistics": self.statistics.to_dict(),
        }


def _ensure_detected(inv: Invariant) -> None:
    if inv.state is InvariantState.CANDIDATE:
        inv.transition_to(InvariantState.DETECTED)


def _annotate(inv: Invariant, item: RankedInvariant) -> None:
    inv.metadata = dict(inv.metadata or {})
    inv.metadata["validation"] = {**item.scores.to_dict(), "rank": item.rank}
    inv.transfer_contribution = item.scores.transfer


def validate_and_rank(
    candidates: Sequence[Invariant],
    *,
    config: ValidationConfig | None = None,
    transfer_scores: Mapping[str, float] | None = None,
    policy: InvariantPolicy | None = None,
) -> ValidationResult:
    """Score, rank, and promote candidate invariants (gatekeeper for SCT)."""
    config = config or ValidationConfig()
    ranked = rank_invariants(
        list(candidates), config, transfer_scores=transfer_scores, policy=policy
    )

    validated: list[Invariant] = []
    transfer_verified: list[Invariant] = []
    promotable: list[Invariant] = []
    rejected: list[tuple[Invariant, list[str]]] = []

    for item in ranked:
        scores = item.scores
        inv = item.invariant

        if meets_promotion_criteria(scores, config):
            promoted = apply_promotion(item, config)
            if promoted is None:
                rejected.append((inv, list(scores.reasons) or ["promotion"]))
                continue
            promotable.append(promoted)
            validated.append(promoted)
            transfer_verified.append(promoted)
            continue

        # Survived F (or rescue) + C + G → validated tier (not yet SCT).
        structural_ok = (
            scores.pass_frequency
            and scores.pass_consistency
            and scores.pass_generality
            and "task_specific_literal" not in scores.reasons
            and "failed_variation_survival" not in scores.reasons
        )
        if structural_ok:
            _ensure_detected(inv)
            if inv.state is InvariantState.DETECTED:
                inv.transition_to(InvariantState.VALIDATED)
            _annotate(inv, item)
            validated.append(inv)
            if scores.pass_transfer:
                if inv.state is InvariantState.VALIDATED:
                    inv.transition_to(InvariantState.TRANSFER_VERIFIED)
                transfer_verified.append(inv)
            else:
                rejected.append((inv, list(scores.reasons)))
        else:
            rejected.append((inv, list(scores.reasons) or ["filtered"]))

    stats = ValidationStatistics(
        candidates_in=len(candidates),
        ranked=len(ranked),
        validated=len(validated),
        transfer_verified=len(transfer_verified),
        promotable=len(promotable),
        rejected=len(rejected),
    )
    return ValidationResult(
        ranked=ranked,
        validated=validated,
        transfer_verified=transfer_verified,
        promotable=promotable,
        rejected=rejected,
        statistics=stats,
    )
