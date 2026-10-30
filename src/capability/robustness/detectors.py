"""CF1–CF10 detectors wrapping representation/growth/intelligence audits."""

from __future__ import annotations

from typing import Any, Sequence

from capability.failures import audit_representation
from capability.library import CapabilityLibrary
from capability.robustness.config import CapabilityRobustnessConfig
from capability.robustness.metrics import (
    fragmentation_ratio,
    mean_transfer_score,
    negative_transfer_rate,
    saturation_ratio,
    series_cgr_signs,
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


def _diag(
    kind: CapabilityFailureKind,
    level: FailureLevel,
    reasons: list[str],
    metrics: dict[str, Any] | None = None,
    caps: list[str] | None = None,
) -> FailureDiagnosis:
    return FailureDiagnosis(
        kind, level, reasons, metrics or {}, caps or []
    )


def _from_legacy(
    failures: Sequence[Any], *, default_level: FailureLevel
) -> list[FailureDiagnosis]:
    out: list[FailureDiagnosis] = []
    for f in failures:
        kind = kind_from_legacy(getattr(f, "kind", "") or "")
        if kind is None:
            continue
        caps = list(getattr(f, "capability_ids", []) or [])
        out.append(
            _diag(
                kind,
                default_level,
                list(getattr(f, "reasons", []) or []),
                dict(getattr(f, "metrics", {}) or {}),
                caps,
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
    report = audit_growth(
        cgr=cgr,
        tg=tg,
        ug=ug,
        ccg=ccg,
        skill_delta=skill_delta,
        transfer_delta=transfer_delta,
        evidence=evidence,
    )
    mapped = _from_legacy(report.failures, default_level=FailureLevel.REJECTED)
    # Prefer CF1 for skill-count / utility illusions.
    out = [
        d
        for d in mapped
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
    fr = fragmentation_ratio(cap_lib, skill_lib)
    out: list[FailureDiagnosis] = []
    if fr > config.max_fragmentation_ratio:
        out.append(
            _diag(
                CapabilityFailureKind.CF2,
                FailureLevel.RESTRICTED,
                ["high_fragmentation_ratio"],
                {"fr": fr, "threshold": config.max_fragmentation_ratio},
            )
        )
    report = audit_representation(cap_lib, skill_lib)
    out.extend(_from_legacy(report, default_level=FailureLevel.RESTRICTED))
    # Dedup CF2
    seen = False
    uniq: list[FailureDiagnosis] = []
    for d in out:
        if d.kind is CapabilityFailureKind.CF2:
            if seen:
                continue
            seen = True
        uniq.append(d)
    return [d for d in uniq if d.kind is CapabilityFailureKind.CF2]


def detect_cf3_inflation(
    cap_lib: CapabilityLibrary,
    skill_lib: SkillLibrary,
    *,
    claimed_coverage: float | None = None,
    observed_coverage: float | None = None,
    config: CapabilityRobustnessConfig,
) -> list[FailureDiagnosis]:
    out: list[FailureDiagnosis] = []
    report = audit_representation(cap_lib, skill_lib)
    out.extend(
        d
        for d in _from_legacy(report, default_level=FailureLevel.REJECTED)
        if d.kind is CapabilityFailureKind.CF3
    )
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
    config: CapabilityRobustnessConfig,
) -> list[FailureDiagnosis]:
    ts = mean_transfer_score(skill_lib)
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
    neg, _ = series_cgr_signs(cgr_series)
    # Count trailing negatives
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
                {"trailing_neg": trailing, "neg_total": neg},
            )
        ]
    return []


def detect_cf7_metric_gaming(
    *,
    evidence: GrowthEvidence | None,
    cgr: float,
    ug: float,
    tg: float,
    config: CapabilityRobustnessConfig,
) -> list[FailureDiagnosis]:
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


def detect_cf10_collapse(
    cgr_series: Sequence[float], config: CapabilityRobustnessConfig
) -> list[FailureDiagnosis]:
    bad = sum(
        1 for x in cgr_series if float(x) <= config.collapse_cgr_threshold
    )
    if bad >= config.collapse_min_steps:
        return [
            _diag(
                CapabilityFailureKind.CF10,
                FailureLevel.REJECTED,
                ["capability_collapse"],
                {"bad_steps": bad, "threshold": config.collapse_cgr_threshold},
            )
        ]
    return []
