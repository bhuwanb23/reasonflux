"""Unified hard promotion gate before SCT (Phase 11C-5)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.invariant import Invariant
from core.states import InvariantState
from invariants.robustness.config import RobustnessConfig
from invariants.robustness.diversity import meets_multi_family
from invariants.robustness.escalation import (
    EscalationResult,
    FailureLevel,
    apply_escalation_metadata,
    evaluate_escalation,
    record_ntr_violation,
)
from invariants.robustness.explosion import should_restrict_promotion
from invariants.robustness.vst import passes_vst, vst_for_invariant
from invariants.validation.scores import ValidationScores
from transfer.gate import evaluate_transfer_gate
from transfer.memory import TransferMemory
from transfer.metrics import TransferConfig, TransferScores, compute_transfer_score


@dataclass(slots=True)
class HardGateResult:
    promotable: bool
    level: FailureLevel
    reasons: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    transfer: TransferScores | None = None

    def to_dict(self) -> dict:
        return {
            "promotable": self.promotable,
            "level": self.level.value,
            "reasons": list(self.reasons),
            "metrics": dict(self.metrics),
            "transfer": self.transfer.to_dict() if self.transfer else None,
        }


def evaluate_hard_gate(
    invariant: Invariant,
    validation_scores: ValidationScores | None,
    *,
    memory: TransferMemory | None = None,
    robustness_config: RobustnessConfig | None = None,
    transfer_config: TransferConfig | None = None,
    ier: float | None = None,
    compatibility_ok: bool = True,
    total_families: int = 1,
) -> HardGateResult:
    """All doc checks: F/C/G/T/R, transfer gate, VST, E_min, families, NTR."""
    robustness_config = robustness_config or RobustnessConfig()
    transfer_config = transfer_config or TransferConfig()
    reasons: list[str] = []

    meta_level = (invariant.metadata or {}).get("failure_level")
    if meta_level == FailureLevel.BLACKLISTED.value:
        return HardGateResult(
            False,
            FailureLevel.BLACKLISTED,
            ["blacklisted"],
            {"vst": vst_for_invariant(invariant)},
        )

    transfer_scores = TransferScores()
    if memory is not None:
        transfer_scores = compute_transfer_score(
            memory,
            invariant.invariant_id,
            transfer_config,
            total_families=total_families,
        )

    tg = evaluate_transfer_gate(
        invariant, validation_scores, transfer_scores, transfer_config
    )
    if not tg.promotable:
        reasons.extend(tg.reasons)
        if transfer_scores.ntr > transfer_config.ntr_limit:
            record_ntr_violation(invariant)

    if validation_scores is not None:
        if not validation_scores.pass_reasoning:
            reasons.append("reasoning_value")
        if not validation_scores.pass_transfer and "transfer" not in reasons:
            reasons.append("transfer")

    vst = vst_for_invariant(invariant)
    if not passes_vst(invariant, robustness_config):
        reasons.append("vst_below_threshold")

    obs = invariant.evidence.observations if invariant.evidence else 0
    if obs < robustness_config.min_evidence:
        reasons.append("insufficient_evidence")

    if not meets_multi_family(invariant, robustness_config):
        reasons.append("multi_family")

    if not compatibility_ok:
        reasons.append("incompatible")

    if ier is not None and should_restrict_promotion(ier, robustness_config):
        reasons.append("ier_restrict")

    escalation = evaluate_escalation(
        invariant,
        transfer_scores=transfer_scores,
        ier=ier,
        config=robustness_config,
        transfer_ntr_limit=transfer_config.ntr_limit,
    )
    apply_escalation_metadata(invariant, escalation)

    if escalation.level is FailureLevel.BLACKLISTED:
        reasons.append("blacklisted")
    elif escalation.level is FailureLevel.REJECTED and not reasons:
        reasons.extend(escalation.reasons)

    level = escalation.level
    if reasons and level is FailureLevel.OK:
        level = FailureLevel.REJECTED

    promotable = not reasons and level in (FailureLevel.OK, FailureLevel.WARNING)

    metrics = {
        "vst": vst,
        "evidence": obs,
        "ier": ier,
        "task_families": len(set(invariant.task_families or [])),
    }
    return HardGateResult(
        promotable=promotable,
        level=level,
        reasons=sorted(set(reasons)),
        metrics=metrics,
        transfer=transfer_scores,
    )


def confirm_hard_gate(
    invariant: Invariant,
    validation_scores: ValidationScores | None,
    *,
    memory: TransferMemory | None = None,
    robustness_config: RobustnessConfig | None = None,
    transfer_config: TransferConfig | None = None,
    ier: float | None = None,
    compatibility_ok: bool = True,
    total_families: int = 1,
) -> HardGateResult:
    """Advance to TRANSFER_VERIFIED only when hard gate passes."""
    result = evaluate_hard_gate(
        invariant,
        validation_scores,
        memory=memory,
        robustness_config=robustness_config,
        transfer_config=transfer_config,
        ier=ier,
        compatibility_ok=compatibility_ok,
        total_families=total_families,
    )
    if not result.promotable:
        return result

    if invariant.state is InvariantState.CANDIDATE:
        invariant.transition_to(InvariantState.DETECTED)
    if invariant.state is InvariantState.DETECTED:
        invariant.transition_to(InvariantState.VALIDATED)
    if invariant.state in (
        InvariantState.VALIDATED,
        InvariantState.STRONG,
    ):
        invariant.transition_to(InvariantState.TRANSFER_VERIFIED)

    if result.transfer is not None:
        invariant.transfer_contribution = result.transfer.its
        if result.transfer.attempts > 0:
            invariant.evidence.transfer_events = max(
                invariant.evidence.transfer_events, result.transfer.attempts
            )
    invariant.metadata = dict(invariant.metadata or {})
    invariant.metadata["hard_gate"] = result.to_dict()
    return result
