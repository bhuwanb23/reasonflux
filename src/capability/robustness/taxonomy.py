"""Capability failure taxonomy CF1–CF10 (Phase 11E-5)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from invariants.robustness.escalation import FailureLevel


class CapabilityFailureKind(str, Enum):
    """Capability-side failure identifiers."""

    CF1 = "cf1_growth_illusion"
    CF2 = "cf2_fragmentation"
    CF3 = "cf3_inflation"
    CF4 = "cf4_transfer_collapse"
    CF5 = "cf5_saturation"
    CF6 = "cf6_regression"
    CF7 = "cf7_metric_gaming"
    CF8 = "cf8_benchmark_overfitting"
    CF9 = "cf9_intelligence_illusion"
    CF10 = "cf10_capability_collapse"


@dataclass(slots=True)
class FailureDiagnosis:
    """One diagnosed capability-ecosystem failure."""

    kind: CapabilityFailureKind
    level: FailureLevel
    reasons: list[str] = field(default_factory=list)
    metrics: dict[str, Any] = field(default_factory=dict)
    capability_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "kind": self.kind.value,
            "level": self.level.value,
            "reasons": list(self.reasons),
            "metrics": dict(self.metrics),
            "capability_ids": list(self.capability_ids),
        }


def kind_from_legacy(name: str) -> CapabilityFailureKind | None:
    """Map growth/intel failure string kinds onto CF ids when possible."""
    mapping = {
        "skill_count_illusion": CapabilityFailureKind.CF1,
        "growth_without_utility": CapabilityFailureKind.CF1,
        "growth_illusion": CapabilityFailureKind.CF9,
        "fragmentation": CapabilityFailureKind.CF2,
        "too_many_tiny": CapabilityFailureKind.CF2,
        "coverage_inflation": CapabilityFailureKind.CF3,
        "ghost": CapabilityFailureKind.CF3,
        "transfer_collapse": CapabilityFailureKind.CF4,
        "transfer_illusion": CapabilityFailureKind.CF4,
        "metric_gaming": CapabilityFailureKind.CF7,
        "unsupported_growth": CapabilityFailureKind.CF7,
        "skill_hoarding": CapabilityFailureKind.CF9,
        "composition_without_transfer": CapabilityFailureKind.CF9,
        "shallow_diversity": CapabilityFailureKind.CF9,
    }
    return mapping.get(str(name))
