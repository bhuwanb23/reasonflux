"""Failure escalation L1–L4 (Phase 11C-5)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from core.invariant import Invariant
from invariants.robustness.config import RobustnessConfig
from invariants.robustness.explosion import ier_level
from invariants.robustness.vst import vst_for_invariant
from transfer.metrics import TransferScores


class FailureLevel(str, Enum):
    """Escalation severity (orthogonal to InvariantState)."""

    OK = "ok"
    WARNING = "warning"  # L1
    RESTRICTED = "restricted"  # L2
    REJECTED = "rejected"  # L3
    BLACKLISTED = "blacklisted"  # L4


@dataclass(slots=True)
class EscalationResult:
    level: FailureLevel
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"level": self.level.value, "reasons": list(self.reasons)}


def _metadata_int(inv: Invariant, key: str) -> int:
    meta = inv.metadata or {}
    return int(meta.get(key, 0) or 0)


def record_ntr_violation(invariant: Invariant) -> None:
    """Increment NTR violation counter for blacklist tracking."""
    invariant.metadata = dict(invariant.metadata or {})
    n = _metadata_int(invariant, "ntr_violations") + 1
    invariant.metadata["ntr_violations"] = n


def apply_escalation_metadata(invariant: Invariant, result: EscalationResult) -> None:
    invariant.metadata = dict(invariant.metadata or {})
    invariant.metadata["failure_level"] = result.level.value
    invariant.metadata["failure_reasons"] = list(result.reasons)


def evaluate_escalation(
    invariant: Invariant,
    *,
    transfer_scores: TransferScores | None = None,
    ier: float | None = None,
    config: RobustnessConfig | None = None,
    transfer_ntr_limit: float = 0.3,
) -> EscalationResult:
    """Map failure signals to L1–L4."""
    config = config or RobustnessConfig()
    reasons: list[str] = []
    level = FailureLevel.OK

    if (invariant.metadata or {}).get("failure_level") == FailureLevel.BLACKLISTED.value:
        return EscalationResult(FailureLevel.BLACKLISTED, ["blacklisted"])

    if _metadata_int(invariant, "ntr_violations") >= config.ntr_blacklist_violations:
        return EscalationResult(FailureLevel.BLACKLISTED, ["repeated_ntr"])

    if transfer_scores is not None and transfer_scores.ntr > transfer_ntr_limit:
        reasons.append("negative_transfer")
        level = FailureLevel.REJECTED

    vst = vst_for_invariant(invariant)
    if vst < config.min_vst:
        reasons.append("low_vst")
        if level.value == FailureLevel.OK.value:
            level = FailureLevel.REJECTED

    obs = invariant.evidence.observations if invariant.evidence else 0
    if obs < config.min_evidence:
        reasons.append("sparse_evidence")
        if level in (FailureLevel.OK, FailureLevel.WARNING):
            level = FailureLevel.WARNING

    if transfer_scores is not None and transfer_scores.weighted < 0.2:
        if transfer_scores.attempts >= 1:
            reasons.append("weak_transfer")
            if level is FailureLevel.OK:
                level = FailureLevel.RESTRICTED

    if ier is not None:
        sev = ier_level(ier, config)
        if sev == "restrict":
            reasons.append("invariant_explosion")
            if level in (FailureLevel.OK, FailureLevel.WARNING):
                level = FailureLevel.RESTRICTED
        elif sev == "warn":
            reasons.append("ier_warn")
            if level is FailureLevel.OK:
                level = FailureLevel.WARNING

    if invariant.frequency < 3 and level is FailureLevel.OK:
        reasons.append("low_frequency")
        level = FailureLevel.WARNING

    if not reasons:
        return EscalationResult(FailureLevel.OK, [])
    return EscalationResult(level, reasons)
