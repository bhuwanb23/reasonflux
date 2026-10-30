"""Growth evidence model and robustness / failure detectors (Phase 11E-2)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from evaluation.growth_config import GrowthConfig


@dataclass(slots=True)
class GrowthEvidence:
    """Evidence supporting a growth claim."""

    new_skills: int = 0
    transfer_events: int = 0
    coverage_expansion: float = 0.0
    utility_improvement: float = 0.0
    composition_growth: float = 0.0
    notes: list[str] = field(default_factory=list)

    @property
    def total_signal(self) -> int:
        bits = 0
        if self.new_skills > 0:
            bits += 1
        if self.transfer_events > 0:
            bits += 1
        if self.coverage_expansion > 0:
            bits += 1
        if self.utility_improvement > 0:
            bits += 1
        if self.composition_growth > 0:
            bits += 1
        return bits

    def has_support(self) -> bool:
        return self.total_signal > 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "new_skills": self.new_skills,
            "transfer_events": self.transfer_events,
            "coverage_expansion": self.coverage_expansion,
            "utility_improvement": self.utility_improvement,
            "composition_growth": self.composition_growth,
            "notes": list(self.notes),
            "total_signal": self.total_signal,
        }


@dataclass(slots=True)
class GrowthFailure:
    kind: str
    reasons: list[str] = field(default_factory=list)
    metrics: dict[str, float] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind,
            "reasons": list(self.reasons),
            "metrics": dict(self.metrics),
        }


@dataclass(slots=True)
class RobustnessResult:
    ok: bool
    failures: list[GrowthFailure] = field(default_factory=list)
    evidence: GrowthEvidence | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "ok": self.ok,
            "failures": [f.to_dict() for f in self.failures],
            "evidence": self.evidence.to_dict() if self.evidence else None,
        }


def build_growth_evidence(
    *,
    new_skills: int = 0,
    transfer_events: int = 0,
    coverage_expansion: float = 0.0,
    utility_improvement: float = 0.0,
    composition_growth: float = 0.0,
    notes: Sequence[str] | None = None,
) -> GrowthEvidence:
    return GrowthEvidence(
        new_skills=int(new_skills),
        transfer_events=int(transfer_events),
        coverage_expansion=float(coverage_expansion),
        utility_improvement=float(utility_improvement),
        composition_growth=float(composition_growth),
        notes=list(notes or []),
    )


def detect_skill_count_illusion(
    *,
    skill_delta: int,
    cgr: float,
    config: GrowthConfig | None = None,
) -> GrowthFailure | None:
    """More skills without capability growth."""
    cfg = config or GrowthConfig()
    if (
        skill_delta >= cfg.skill_count_illusion_min_skills
        and abs(cgr) <= cfg.skill_count_illusion_max_cgr
    ):
        return GrowthFailure(
            "skill_count_illusion",
            ["skills_up_cgr_flat"],
            {"skill_delta": float(skill_delta), "cgr": float(cgr)},
        )
    return None


def detect_transfer_illusion(
    *,
    tg: float,
    utility_delta: float,
    config: GrowthConfig | None = None,
) -> GrowthFailure | None:
    """Transfer appears positive but utility does not improve."""
    cfg = config or GrowthConfig()
    if tg >= cfg.transfer_illusion_min_tg and utility_delta <= cfg.transfer_illusion_max_utility_delta:
        return GrowthFailure(
            "transfer_illusion",
            ["tg_up_utility_flat"],
            {"tg": float(tg), "utility_delta": float(utility_delta)},
        )
    return None


def detect_coverage_inflation(
    *,
    ccg: float,
    transfer_delta: float,
    config: GrowthConfig | None = None,
) -> GrowthFailure | None:
    """Coverage up without transfer support."""
    cfg = config or GrowthConfig()
    if (
        ccg >= cfg.coverage_inflation_min_ccg
        and transfer_delta <= cfg.coverage_inflation_max_transfer_delta
    ):
        return GrowthFailure(
            "coverage_inflation",
            ["ccg_up_transfer_flat"],
            {"ccg": float(ccg), "transfer_delta": float(transfer_delta)},
        )
    return None


def detect_growth_without_utility(
    *,
    cgr: float,
    ug: float,
    config: GrowthConfig | None = None,
) -> GrowthFailure | None:
    """Capability expands but value does not."""
    cfg = config or GrowthConfig()
    if cgr >= cfg.growth_without_utility_min_cgr and ug <= cfg.growth_without_utility_max_ug:
        return GrowthFailure(
            "growth_without_utility",
            ["cgr_up_ug_flat"],
            {"cgr": float(cgr), "ug": float(ug)},
        )
    return None


def detect_metric_gaming(
    *,
    cgr: float,
    evidence: GrowthEvidence,
    config: GrowthConfig | None = None,
) -> GrowthFailure | None:
    """Positive CGR claim without supporting evidence signals."""
    cfg = config or GrowthConfig()
    if cgr >= cfg.metric_gaming_min_cgr and evidence.total_signal <= cfg.metric_gaming_max_evidence:
        return GrowthFailure(
            "metric_gaming",
            ["cgr_without_evidence"],
            {"cgr": float(cgr), "evidence_signal": float(evidence.total_signal)},
        )
    return None


def audit_growth(
    *,
    cgr: float,
    tg: float = 0.0,
    ug: float = 0.0,
    ccg: float = 0.0,
    skill_delta: int = 0,
    transfer_delta: float = 0.0,
    evidence: GrowthEvidence | None = None,
    config: GrowthConfig | None = None,
) -> RobustnessResult:
    """Run all growth failure detectors; reject unsupported claims."""
    cfg = config or GrowthConfig()
    ev = evidence or GrowthEvidence()
    failures: list[GrowthFailure] = []
    for detector in (
        detect_skill_count_illusion(
            skill_delta=skill_delta, cgr=cgr, config=cfg
        ),
        detect_transfer_illusion(tg=tg, utility_delta=ug, config=cfg),
        detect_coverage_inflation(
            ccg=ccg, transfer_delta=transfer_delta, config=cfg
        ),
        detect_growth_without_utility(cgr=cgr, ug=ug, config=cfg),
        detect_metric_gaming(cgr=cgr, evidence=ev, config=cfg),
    ):
        if detector is not None:
            failures.append(detector)
    # Positive CGR without any evidence is also a soft rejection.
    if cgr > 0 and not ev.has_support() and not any(
        f.kind == "metric_gaming" for f in failures
    ):
        failures.append(
            GrowthFailure(
                "unsupported_growth",
                ["no_evidence"],
                {"cgr": float(cgr)},
            )
        )
    return RobustnessResult(ok=not failures, failures=failures, evidence=ev)
