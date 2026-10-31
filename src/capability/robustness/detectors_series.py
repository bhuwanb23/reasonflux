"""Series / holdout CF detectors (CF5, CF6, CF8, CF10)."""

from __future__ import annotations

from typing import Sequence

from capability.robustness.config import CapabilityRobustnessConfig
from capability.robustness.metrics import saturation_ratio
from capability.robustness.taxonomy import CapabilityFailureKind, FailureDiagnosis
from invariants.robustness.escalation import FailureLevel


def _diag(
    kind: CapabilityFailureKind,
    level: FailureLevel,
    reasons: list[str],
    metrics: dict | None = None,
) -> FailureDiagnosis:
    return FailureDiagnosis(kind, level, reasons, metrics or {}, [])


def detect_cf5_saturation(
    *,
    new_cap: float,
    existing_cap: float,
    config: CapabilityRobustnessConfig,
) -> list[FailureDiagnosis]:
    csr = saturation_ratio(new_cap, existing_cap)
    if csr <= config.saturation_csr and existing_cap > 0:
        return [
            _diag(
                CapabilityFailureKind.CF5,
                FailureLevel.WARNING,
                ["capability_saturation"],
                {"csr": csr, "threshold": config.saturation_csr},
            )
        ]
    return []


def detect_cf6_regression(
    cgr_series: Sequence[float], config: CapabilityRobustnessConfig
) -> list[FailureDiagnosis]:
    trailing = 0
    for x in reversed(list(cgr_series)):
        if float(x) < -1e-12:
            trailing += 1
        else:
            break
    if trailing >= config.regression_negative_cgr_steps:
        return [
            _diag(
                CapabilityFailureKind.CF6,
                FailureLevel.RESTRICTED,
                ["sustained_negative_cgr"],
                {"trailing_neg": trailing},
            )
        ]
    return []


def detect_cf8_overfitting(
    *,
    train_success: float,
    holdout_success: float,
    config: CapabilityRobustnessConfig,
) -> list[FailureDiagnosis]:
    gap = float(train_success) - float(holdout_success)
    if gap >= config.overfitting_success_gap and train_success > 0.5:
        return [
            _diag(
                CapabilityFailureKind.CF8,
                FailureLevel.REJECTED,
                ["train_holdout_divergence"],
                {
                    "train_success": train_success,
                    "holdout_success": holdout_success,
                    "gap": gap,
                },
            )
        ]
    return []


def detect_cf10_collapse(
    cgr_series: Sequence[float], config: CapabilityRobustnessConfig
) -> list[FailureDiagnosis]:
    trailing = 0
    for x in reversed(list(cgr_series)):
        if float(x) <= config.collapse_cgr_threshold:
            trailing += 1
        else:
            break
    if trailing >= config.collapse_min_steps:
        return [
            _diag(
                CapabilityFailureKind.CF10,
                FailureLevel.REJECTED,
                ["capability_collapse"],
                {
                    "trailing_bad": trailing,
                    "threshold": config.collapse_cgr_threshold,
                },
            )
        ]
    return []
