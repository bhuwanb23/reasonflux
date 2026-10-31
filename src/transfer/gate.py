"""Transfer promotion gate — ITS / NTR / attempts before SCT (Phase 11C-4)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from core.invariant import Invariant
from core.states import InvariantState
from transfer.memory import TransferMemory
from transfer.metrics import TransferConfig, TransferScores, compute_transfer_score

if TYPE_CHECKING:  # pragma: no cover - import only for type checkers
    # Imported under TYPE_CHECKING to break the cycle
    # transfer.gate → invariants.validation → invariants → robustness.hard_gate
    # → transfer.gate. ValidationScores is used in annotations only.
    from invariants.validation.scores import ValidationScores


@dataclass(slots=True)
class TransferGateResult:
    """Outcome of the transfer-aware promotion gate."""

    promotable: bool
    rejected: bool
    reasons: list[str] = field(default_factory=list)
    scores: TransferScores | None = None

    def to_dict(self) -> dict:
        return {
            "promotable": self.promotable,
            "rejected": self.rejected,
            "reasons": list(self.reasons),
            "scores": self.scores.to_dict() if self.scores else None,
        }


def evaluate_transfer_gate(
    invariant: Invariant,
    validation_scores: ValidationScores | None,
    transfer_scores: TransferScores,
    config: TransferConfig | None = None,
) -> TransferGateResult:
    """Enforce transfer evidence requirements before SCT eligibility.

    Requires: F/C/G from validation (when provided), ITS >= min_its,
    attempts >= min_transfer_attempts, NTR <= ntr_limit.
    """
    config = config or TransferConfig()
    reasons: list[str] = []

    if validation_scores is not None:
        if not validation_scores.pass_frequency:
            reasons.append("frequency")
        if not validation_scores.pass_consistency:
            reasons.append("consistency")
        if not validation_scores.pass_generality:
            reasons.append("generality")

    if transfer_scores.attempts < config.min_transfer_attempts:
        reasons.append("insufficient_transfer_attempts")
    if transfer_scores.its < config.min_its:
        reasons.append("its_below_threshold")
    if transfer_scores.ntr > config.ntr_limit:
        reasons.append("negative_transfer")

    ok = not reasons
    return TransferGateResult(
        promotable=ok,
        rejected=not ok,
        reasons=reasons,
        scores=transfer_scores,
    )


def confirm_transfer(
    invariant: Invariant,
    memory: TransferMemory,
    config: TransferConfig | None = None,
    *,
    validation_scores: ValidationScores | None = None,
    total_families: int = 1,
) -> TransferGateResult:
    """Advance VALIDATED → TRANSFER_VERIFIED when the transfer gate passes."""
    config = config or TransferConfig()
    scores = compute_transfer_score(
        memory, invariant.invariant_id, config, total_families=total_families
    )
    result = evaluate_transfer_gate(invariant, validation_scores, scores, config)
    if not result.promotable:
        return result

    # Lifecycle: ensure we can reach TRANSFER_VERIFIED.
    if invariant.state is InvariantState.CANDIDATE:
        invariant.transition_to(InvariantState.DETECTED)
    if invariant.state is InvariantState.DETECTED:
        invariant.transition_to(InvariantState.VALIDATED)
    if invariant.state is InvariantState.VALIDATED:
        invariant.transition_to(InvariantState.TRANSFER_VERIFIED)
    elif invariant.state is InvariantState.STRONG:
        invariant.transition_to(InvariantState.TRANSFER_VERIFIED)

    invariant.transfer_contribution = scores.its
    if scores.attempts > 0:
        invariant.evidence.transfer_events = max(
            invariant.evidence.transfer_events, scores.attempts
        )
    invariant.metadata = dict(invariant.metadata or {})
    invariant.metadata["transfer"] = scores.to_dict()
    return result
