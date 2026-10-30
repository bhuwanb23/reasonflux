"""Harness data models (Phase 11E-4)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class LayerResult:
    layer: str  # invariant | skill | transfer | capability | intelligence
    passed: bool
    metrics: dict[str, float] = field(default_factory=dict)
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "layer": self.layer,
            "passed": self.passed,
            "metrics": dict(self.metrics),
            "notes": list(self.notes),
        }


@dataclass(slots=True)
class EvaluationSnapshot:
    step: int
    capability_score: float = 0.0
    cgr: float = 0.0
    ig: float = 0.0
    igr: float = 0.0
    coverage: float = 0.0
    mean_su: float = 0.0
    mean_ts: float = 0.0
    ntr: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "step": self.step,
            "capability_score": self.capability_score,
            "cgr": self.cgr,
            "ig": self.ig,
            "igr": self.igr,
            "coverage": self.coverage,
            "mean_su": self.mean_su,
            "mean_ts": self.mean_ts,
            "ntr": self.ntr,
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class ClaimEvidence:
    claim: str
    evidence: str
    metric: str
    experiment: str
    supported: bool = False

    def to_dict(self) -> dict[str, Any]:
        return {
            "claim": self.claim,
            "evidence": self.evidence,
            "metric": self.metric,
            "experiment": self.experiment,
            "supported": self.supported,
        }


@dataclass(slots=True)
class EvaluationRun:
    run_id: str
    level: str
    baseline: str | None = None
    ablation: str | None = None
    snapshots: list[EvaluationSnapshot] = field(default_factory=list)
    layers: list[LayerResult] = field(default_factory=list)
    maturity: int = 1
    success: bool = False
    claims: list[ClaimEvidence] = field(default_factory=list)
    stats: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "run_id": self.run_id,
            "level": self.level,
            "baseline": self.baseline,
            "ablation": self.ablation,
            "snapshots": [s.to_dict() for s in self.snapshots],
            "layers": [layer.to_dict() for layer in self.layers],
            "maturity": self.maturity,
            "success": self.success,
            "claims": [c.to_dict() for c in self.claims],
            "stats": dict(self.stats),
            "metadata": dict(self.metadata),
        }


# Alias used by plan / reports
BenchmarkResult = EvaluationRun
