"""Intelligence-level failure detectors and audit (Phase 11E-3)."""

from __future__ import annotations

from typing import Any

from evaluation.growth_checks import (
    GrowthEvidence,
    GrowthFailure,
    RobustnessResult,
    audit_growth,
)
from evaluation.growth_config import GrowthConfig


def detect_skill_hoarding(
    *,
    skill_count: int,
    ig_delta: float,
    config: GrowthConfig | None = None,
) -> GrowthFailure | None:
    """Many skills but no intelligence growth."""
    cfg = config or GrowthConfig()
    if (
        skill_count >= cfg.skill_count_illusion_min_skills
        and abs(ig_delta) <= cfg.skill_count_illusion_max_cgr
    ):
        return GrowthFailure(
            "skill_hoarding",
            ["many_skills_no_ig"],
            {"skill_count": float(skill_count), "ig_delta": float(ig_delta)},
        )
    return None


def detect_transfer_collapse(
    *,
    tg: float,
    previous_tg: float | None = None,
    config: GrowthConfig | None = None,
) -> GrowthFailure | None:
    """Transfer support collapses relative to prior period."""
    del config
    if previous_tg is not None and float(previous_tg) > 0 and tg < float(previous_tg) * 0.5:
        return GrowthFailure(
            "transfer_collapse",
            ["tg_drop"],
            {"tg": float(tg), "previous_tg": float(previous_tg)},
        )
    return None


def detect_fragmentation_persistence(
    *,
    fragmentation_score: float,
    threshold: float = 0.5,
) -> GrowthFailure | None:
    """Capabilities remain fragmented / non-integrated."""
    if fragmentation_score >= threshold:
        return GrowthFailure(
            "fragmentation_persistence",
            ["high_fragmentation"],
            {"fragmentation": float(fragmentation_score)},
        )
    return None


def detect_composition_failure(
    *,
    composition_success_rate: float,
    threshold: float = 0.1,
) -> GrowthFailure | None:
    """Composition rarely succeeds."""
    if composition_success_rate <= threshold:
        return GrowthFailure(
            "composition_failure",
            ["composition_low_success"],
            {"rate": float(composition_success_rate)},
        )
    return None


def detect_adaptation_failure(
    *,
    new_families: int,
    elasticity: float,
    min_elasticity: float = 0.01,
) -> GrowthFailure | None:
    """New domains appear but elasticity stays near zero."""
    if new_families > 0 and elasticity < min_elasticity:
        return GrowthFailure(
            "adaptation_failure",
            ["low_elasticity_on_new_families"],
            {
                "new_families": float(new_families),
                "elasticity": float(elasticity),
            },
        )
    return None


def detect_growth_illusion(
    *,
    ig_delta: float,
    cgr: float,
    evidence: GrowthEvidence,
    min_delta: float = 0.02,
) -> GrowthFailure | None:
    """IG/CGR rise without supporting evidence."""
    if (ig_delta >= min_delta or cgr >= min_delta) and not evidence.has_support():
        return GrowthFailure(
            "growth_illusion",
            ["metric_up_no_evidence"],
            {"ig_delta": float(ig_delta), "cgr": float(cgr)},
        )
    return None


def audit_intelligence(
    *,
    ig: float,
    ig_delta: float,
    evidence: GrowthEvidence | None = None,
    extra_metrics: dict[str, Any] | None = None,
    config: GrowthConfig | None = None,
) -> RobustnessResult:
    """Run growth baseline + intelligence-specific detectors."""
    del ig  # score available for callers; audit focuses on deltas/evidence
    cfg = config or GrowthConfig()
    ev = evidence or GrowthEvidence()
    em = extra_metrics or {}
    failures: list[GrowthFailure] = []

    growth_res = audit_growth(
        cgr=float(em.get("cgr", ig_delta)),
        tg=float(em.get("tg", 0.0)),
        ug=float(em.get("ug", 0.0)),
        ccg=float(em.get("ccg", 0.0)),
        skill_delta=int(em.get("skill_delta", 0)),
        transfer_delta=float(em.get("transfer_delta", 0.0)),
        evidence=ev,
        config=cfg,
    )
    failures.extend(growth_res.failures)

    for detector in (
        detect_skill_hoarding(
            skill_count=int(em.get("skill_count", 0)),
            ig_delta=ig_delta,
            config=cfg,
        ),
        detect_transfer_collapse(
            tg=float(em.get("tg", 0.0)),
            previous_tg=em.get("previous_tg"),
            config=cfg,
        ),
        detect_fragmentation_persistence(
            fragmentation_score=float(em.get("fragmentation", 0.0))
        ),
        detect_composition_failure(
            composition_success_rate=float(em.get("composition_success_rate", 1.0))
        ),
        detect_adaptation_failure(
            new_families=int(em.get("new_families", 0)),
            elasticity=float(em.get("elasticity", 1.0)),
        ),
        detect_growth_illusion(
            ig_delta=ig_delta,
            cgr=float(em.get("cgr", 0.0)),
            evidence=ev,
        ),
    ):
        if detector is not None:
            failures.append(detector)

    # Deduplicate by kind
    seen: set[str] = set()
    unique: list[GrowthFailure] = []
    for f in failures:
        if f.kind not in seen:
            seen.add(f.kind)
            unique.append(f)
    return RobustnessResult(ok=not unique, failures=unique, evidence=ev)
