"""CF1–CF4 / CF7 / CF9 detectors wrapping growth/intel/representation audits."""

from __future__ import annotations

from typing import Any, Sequence

from capability.failures import audit_representation
from capability.library import CapabilityLibrary
from capability.robustness.config import CapabilityRobustnessConfig
from capability.robustness.detectors_series import (
    detect_cf5_saturation,
    detect_cf6_regression,
    detect_cf8_overfitting,
    detect_cf10_collapse,
)
from capability.robustness.metrics import (
    fragmentation_ratio,
    mean_transfer_score,
    negative_transfer_rate,
)
from capability.robustness.taxonomy import (
    CapabilityFailureKind,
    FailureDiagnosis,
    kind_from_legacy,
)
from evaluation.growth_checks import GrowthEvidence, audit_growth
from evaluation.intelligence_checks import audit_intelligence
from invariants.robustness.escalation import FailureLevel
from skills.library import SkillLibrary

__all__ = [
    "detect_cf1_growth_illusion",
    "detect_cf2_fragmentation",
    "detect_cf3_inflation",
    "detect_cf4_transfer_collapse",
    "detect_cf5_saturation",
    "detect_cf6_regression",
    "detect_cf7_metric_gaming",
    "detect_cf8_overfitting",
    "detect_cf9_intelligence_illusion",
    "detect_cf10_collapse",
]


def _diag(
    kind: CapabilityFailureKind,
    level: FailureLevel,
    reasons: list[str],
    metrics: dict[str, Any] | None = None,
    caps: list[str] | None = None,
) -> FailureDiagnosis:
    return FailureDiagnosis(kind, level, reasons, metrics or {}, caps or [])


def _from_legacy(
    failures: Sequence[Any], *, default_level: FailureLevel
) -> list[FailureDiagnosis]:
    out: list[FailureDiagnosis] = []
    for f in failures:
        kind = kind_from_legacy(getattr(f, "kind", "") or "")
        if kind is None:
            continue
        out.append(
            _diag(
                kind,
                default_level,
                list(getattr(f, "reasons", []) or []),
                dict(getattr(f, "metrics", {}) or {}),
                list(getattr(f, "capability_ids", []) or []),
            )
        )
    return out


def detect_cf1_growth_illusion(
    *,
    cgr: float,
    tg: float,
    ug: float,
    ccg: float,
    skill_delta: int,
    transfer_delta: float,
    evidence: GrowthEvidence | None,
    config: CapabilityRobustnessConfig,
) -> list[FailureDiagnosis]:
    del config
    report = audit_growth(
        cgr=cgr,
        tg=tg,
        ug=ug,
        ccg=ccg,
        skill_delta=skill_delta,
        transfer_delta=transfer_delta,
        evidence=evidence,
    )
    out = [
        d
        for d in _from_legacy(report.failures, default_level=FailureLevel.REJECTED)
        if d.kind in (CapabilityFailureKind.CF1, CapabilityFailureKind.CF7)
    ]
    if skill_delta > 0 and ug <= 0 and cgr > 0:
        out.append(
            _diag(
                CapabilityFailureKind.CF1,
                FailureLevel.REJECTED,
                ["skill_count_without_utility"],
                {"skill_delta": skill_delta, "ug": ug, "cgr": cgr},
            )
        )
    return out


def detect_cf2_fragmentation(
    cap_lib: CapabilityLibrary,
    skill_lib: SkillLibrary,
    config: CapabilityRobustnessConfig,
) -> list[FailureDiagnosis]:
    out: list[FailureDiagnosis] = []
    fr = fragmentation_ratio(cap_lib, skill_lib)
    if fr > config.max_fragmentation_ratio:
        out.append(
            _diag(
                CapabilityFailureKind.CF2,
                FailureLevel.RESTRICTED,
                ["high_fragmentation_ratio"],
                {"fr": fr, "threshold": config.max_fragmentation_ratio},
            )
        )
    out.extend(
        _from_legacy(
            audit_representation(cap_lib, skill_lib),
            default_level=FailureLevel.RESTRICTED,
        )
    )
    cf2 = [d for d in out if d.kind is CapabilityFailureKind.CF2]
    return cf2[:1] if cf2 else []


def detect_cf3_inflation(
    cap_lib: CapabilityLibrary,
    skill_lib: SkillLibrary,
    *,
    claimed_coverage: float | None = None,
    observed_coverage: float | None = None,
    config: CapabilityRobustnessConfig,
) -> list[FailureDiagnosis]:
    out = [
        d
        for d in _from_legacy(
            audit_representation(cap_lib, skill_lib),
            default_level=FailureLevel.REJECTED,
        )
        if d.kind is CapabilityFailureKind.CF3
    ]
    if (
        claimed_coverage is not None
        and observed_coverage is not None
        and (claimed_coverage - observed_coverage) > config.inflation_coverage_gap
    ):
        out.append(
            _diag(
                CapabilityFailureKind.CF3,
                FailureLevel.REJECTED,
                ["claimed_vs_observed_coverage"],
                {
                    "claimed": claimed_coverage,
                    "observed": observed_coverage,
                    "gap": claimed_coverage - observed_coverage,
                },
            )
        )
    return out


def detect_cf4_transfer_collapse(
    skill_lib: SkillLibrary,
    *,
    prev_ts: float | None = None,
    curr_ts: float | None = None,
    config: CapabilityRobustnessConfig,
) -> list[FailureDiagnosis]:
    ts = float(curr_ts) if curr_ts is not None else mean_transfer_score(skill_lib)
    ntr = negative_transfer_rate(skill_lib)
    out: list[FailureDiagnosis] = []
    if prev_ts is not None and prev_ts > 0:
        drop = (prev_ts - ts) / prev_ts
        if drop >= config.transfer_collapse_ratio:
            out.append(
                _diag(
                    CapabilityFailureKind.CF4,
                    FailureLevel.RESTRICTED,
                    ["transfer_score_collapse"],
                    {"prev_ts": prev_ts, "ts": ts, "drop": drop, "ntr": ntr},
                )
            )
    if ntr > 0.5 and ts <= config.min_tg_positive:
        out.append(
            _diag(
                CapabilityFailureKind.CF4,
                FailureLevel.RESTRICTED,
                ["high_ntr_low_transfer"],
                {"ntr": ntr, "ts": ts},
            )
        )
    return out


def detect_cf7_metric_gaming(
    *,
    evidence: GrowthEvidence | None,
    cgr: float,
    ug: float,
    tg: float,
    config: CapabilityRobustnessConfig,
) -> list[FailureDiagnosis]:
    del config
    report = audit_growth(
        cgr=cgr,
        tg=tg,
        ug=ug,
        ccg=0.0,
        skill_delta=1 if cgr > 0 else 0,
        transfer_delta=tg,
        evidence=evidence,
    )
    return [
        d
        for d in _from_legacy(report.failures, default_level=FailureLevel.REJECTED)
        if d.kind is CapabilityFailureKind.CF7
    ]


def detect_cf9_intelligence_illusion(
    *,
    ig: float,
    ig_delta: float,
    evidence: GrowthEvidence | None,
    extra: dict[str, Any] | None = None,
    config: CapabilityRobustnessConfig,
) -> list[FailureDiagnosis]:
    report = audit_intelligence(
        ig=ig, ig_delta=ig_delta, evidence=evidence, extra_metrics=extra
    )
    mapped = [
        d
        for d in _from_legacy(report.failures, default_level=FailureLevel.REJECTED)
        if d.kind is CapabilityFailureKind.CF9
    ]
    if abs(ig_delta) <= config.ig_stagnation_eps and ig > 0 and (
        evidence is None or not evidence.has_support()
    ):
        mapped.append(
            _diag(
                CapabilityFailureKind.CF9,
                FailureLevel.WARNING,
                ["intelligence_stagnation"],
                {"ig": ig, "ig_delta": ig_delta},
            )
        )
    return mapped
