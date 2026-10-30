"""Hard multi-signal growth validation (Phase 11E-5)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from capability.robustness.config import CapabilityRobustnessConfig
from evaluation.growth_checks import GrowthEvidence


@dataclass(slots=True)
class GrowthClaimResult:
    """Outcome of validate_growth_claim."""

    accepted: bool
    reasons: list[str] = field(default_factory=list)
    signals: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "accepted": self.accepted,
            "reasons": list(self.reasons),
            "signals": dict(self.signals),
        }


def validate_growth_claim(
    *,
    transfer_delta: float,
    utility_delta: float,
    coverage_delta: float,
    evidence: GrowthEvidence | None = None,
    skill_delta: int = 0,
    cgr: float | None = None,
    config: CapabilityRobustnessConfig | None = None,
) -> GrowthClaimResult:
    """Accept growth only if transfer, utility, coverage, and evidence support it.

    Skill-count-only growth is explicitly rejected.
    """
    config = config or CapabilityRobustnessConfig()
    reasons: list[str] = []
    signals = {
        "transfer_delta": float(transfer_delta),
        "utility_delta": float(utility_delta),
        "coverage_delta": float(coverage_delta),
        "skill_delta": int(skill_delta),
        "cgr": cgr,
        "evidence_support": bool(evidence and evidence.has_support()),
    }

    if skill_delta > 0 and utility_delta <= 0 and transfer_delta <= 0:
        reasons.append("skill_count_only_growth")

    if transfer_delta <= 0:
        reasons.append("non_positive_transfer_delta")
    if utility_delta <= 0:
        reasons.append("non_positive_utility_delta")
    if coverage_delta <= 0:
        reasons.append("non_positive_coverage_delta")

    if config.require_evidence:
        if evidence is None or not evidence.has_support():
            reasons.append("missing_growth_evidence")

    if cgr is not None and cgr < 0:
        reasons.append("negative_cgr")

    accepted = len(reasons) == 0
    if not accepted and not reasons:
        reasons.append("unspecified_rejection")
    return GrowthClaimResult(accepted=accepted, reasons=reasons, signals=signals)
