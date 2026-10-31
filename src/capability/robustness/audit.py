"""Ecosystem audit: CF1–CF10 + health + hard gate (Phase 11E-5)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from capability.library import CapabilityLibrary
from capability.robustness.config import CapabilityRobustnessConfig
from capability.robustness.detectors import (
    detect_cf1_growth_illusion,
    detect_cf2_fragmentation,
    detect_cf3_inflation,
    detect_cf4_transfer_collapse,
    detect_cf5_saturation,
    detect_cf6_regression,
    detect_cf7_metric_gaming,
    detect_cf8_overfitting,
    detect_cf9_intelligence_illusion,
    detect_cf10_collapse,
)
from capability.robustness.gates import GrowthClaimResult, validate_growth_claim
from capability.robustness.health import PortfolioHealth, score_portfolio
from capability.robustness.metrics import mean_transfer_score
from capability.robustness.taxonomy import FailureDiagnosis
from evaluation.growth_checks import GrowthEvidence
from skills.library import SkillLibrary


@dataclass(slots=True)
class ScoreSnapshot:
    """Lightweight longitudinal point for series detectors."""

    cgr: float = 0.0
    ig: float = 0.0
    mean_su: float = 0.0
    mean_ts: float = 0.0
    coverage: float = 0.0
    train_success: float | None = None
    holdout_success: float | None = None


@dataclass(slots=True)
class EcosystemAuditResult:
    """Aggregated capability-ecosystem robustness result."""

    ok: bool
    failures: list[FailureDiagnosis] = field(default_factory=list)
    health: PortfolioHealth | None = None
    growth_claim: GrowthClaimResult | None = None
    metrics: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "failures": [f.to_dict() for f in self.failures],
            "health": self.health.to_dict() if self.health else None,
            "growth_claim": (
                self.growth_claim.to_dict() if self.growth_claim else None
            ),
            "metrics": dict(self.metrics),
        }


def audit_capability_ecosystem(
    cap_lib: CapabilityLibrary,
    skill_lib: SkillLibrary,
    snapshots: Sequence[ScoreSnapshot] | None = None,
    *,
    config: CapabilityRobustnessConfig | None = None,
    evidence: GrowthEvidence | None = None,
    claimed_coverage: float | None = None,
    observed_coverage: float | None = None,
    new_cap: float | None = None,
    existing_cap: float | None = None,
    skill_delta: int = 0,
    hard_gate: bool = True,
) -> EcosystemAuditResult:
    """Run CF1–CF10 detectors, portfolio health, and optional hard gate."""
    config = config or CapabilityRobustnessConfig()
    snaps = list(snapshots or [])
    failures: list[FailureDiagnosis] = []

    after = snaps[-1] if snaps else ScoreSnapshot()
    before = snaps[-2] if len(snaps) >= 2 else None
    cgr = float(after.cgr)
    tg = float(after.mean_ts) - (float(before.mean_ts) if before else 0.0)
    ug = float(after.mean_su) - (float(before.mean_su) if before else 0.0)
    ccg = float(after.coverage) - (float(before.coverage) if before else 0.0)
    transfer_delta = tg
    ig = float(after.ig)
    ig_delta = ig - (float(before.ig) if before else 0.0)
    cgr_series = [float(s.cgr) for s in snaps]

    failures.extend(
        detect_cf1_growth_illusion(
            cgr=cgr,
            tg=tg,
            ug=ug,
            ccg=ccg,
            skill_delta=skill_delta,
            transfer_delta=transfer_delta,
            evidence=evidence,
            config=config,
        )
    )
    failures.extend(detect_cf2_fragmentation(cap_lib, skill_lib, config))
    failures.extend(
        detect_cf3_inflation(
            cap_lib,
            skill_lib,
            claimed_coverage=claimed_coverage,
            observed_coverage=observed_coverage
            if observed_coverage is not None
            else after.coverage,
            config=config,
        )
    )
    # Prefer snapshot mean_ts for collapse; fall back to library mean.
    curr_ts = float(after.mean_ts) if snaps else mean_transfer_score(skill_lib)
    if before is not None:
        failures.extend(
            detect_cf4_transfer_collapse(
                skill_lib,
                prev_ts=float(before.mean_ts),
                curr_ts=curr_ts,
                config=config,
            )
        )
    else:
        failures.extend(
            detect_cf4_transfer_collapse(skill_lib, prev_ts=None, config=config)
        )
    if new_cap is not None and existing_cap is not None:
        failures.extend(
            detect_cf5_saturation(
                new_cap=new_cap, existing_cap=existing_cap, config=config
            )
        )
    if cgr_series:
        failures.extend(detect_cf6_regression(cgr_series, config))
        failures.extend(detect_cf10_collapse(cgr_series, config))
    failures.extend(
        detect_cf7_metric_gaming(
            evidence=evidence, cgr=cgr, ug=ug, tg=tg, config=config
        )
    )
    train_s = after.train_success
    hold_s = after.holdout_success
    if train_s is not None and hold_s is not None:
        failures.extend(
            detect_cf8_overfitting(
                train_success=train_s,
                holdout_success=hold_s,
                config=config,
            )
        )
    failures.extend(
        detect_cf9_intelligence_illusion(
            ig=ig,
            ig_delta=ig_delta,
            evidence=evidence,
            extra={
                "cgr": cgr,
                "tg": tg,
                "ug": ug,
                "skill_count": len(skill_lib),
            },
            config=config,
        )
    )

    health = score_portfolio(cap_lib, skill_lib, config=config)
    claim: GrowthClaimResult | None = None
    if hard_gate:
        claim = validate_growth_claim(
            transfer_delta=transfer_delta,
            utility_delta=ug,
            coverage_delta=ccg,
            evidence=evidence,
            skill_delta=skill_delta,
            cgr=cgr,
            config=config,
        )

    ok = not failures and (claim is None or claim.accepted)
    return EcosystemAuditResult(
        ok=ok,
        failures=failures,
        health=health,
        growth_claim=claim,
        metrics={
            "cgr": cgr,
            "tg": tg,
            "ug": ug,
            "ccg": ccg,
            "ig": ig,
            "ig_delta": ig_delta,
            "n_failures": len(failures),
            "mean_chs": health.mean_chs,
            "mean_cs": health.mean_cs,
        },
    )
