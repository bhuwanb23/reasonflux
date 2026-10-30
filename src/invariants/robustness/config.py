"""Robustness thresholds for Phase 11C-5 IDT hardening."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class RobustnessConfig:
    """Thresholds for failure modes, metrics, and hard promotion gate."""

    min_vst: float = 0.6
    ier_warn: float = 1.0
    ier_restrict: float = 3.0
    min_evidence: int = 3
    min_tc: float = 0.5
    min_tfd: float = 0.3
    min_task_families_hard: int = 2
    min_compatibility: float = 0.5
    similarity_merge: float = 0.85
    saturation_k: int = 5
    difficulty_near: float = 0.25
    difficulty_moderate: float = 0.5
    difficulty_compositional: float = 0.75
    difficulty_structural: float = 1.0
    ntr_blacklist_violations: int = 2

    def __post_init__(self) -> None:
        if not 0.0 <= self.min_vst <= 1.0:
            raise ValueError("min_vst must be in [0, 1]")
        if self.ier_warn < 0 or self.ier_restrict < self.ier_warn:
            raise ValueError("ier_restrict must be >= ier_warn >= 0")
        if self.min_evidence < 1:
            raise ValueError("min_evidence must be >= 1")
        if not 0.0 <= self.min_tc <= 1.0:
            raise ValueError("min_tc must be in [0, 1]")
        if not 0.0 <= self.min_tfd <= 1.0:
            raise ValueError("min_tfd must be in [0, 1]")
        if self.min_task_families_hard < 1:
            raise ValueError("min_task_families_hard must be >= 1")
        if not 0.0 <= self.min_compatibility <= 1.0:
            raise ValueError("min_compatibility must be in [0, 1]")
        if not 0.0 <= self.similarity_merge <= 1.0:
            raise ValueError("similarity_merge must be in [0, 1]")
        if self.saturation_k < 1:
            raise ValueError("saturation_k must be >= 1")
        if self.ntr_blacklist_violations < 1:
            raise ValueError("ntr_blacklist_violations must be >= 1")

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> RobustnessConfig:
        known = {f for f in cls.__dataclass_fields__}
        payload = {k: v for k, v in (data or {}).items() if k in known}
        return cls(**payload)
