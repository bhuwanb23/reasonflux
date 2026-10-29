"""Skill robustness thresholds (Phase 11D-5)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class SkillRobustnessConfig:
    """Thresholds for SF1–SF8, edge cases, and skill gates."""

    ser_warn: float = 0.5
    ser_restrict: float = 0.8
    min_confidence_promote: float = 0.4
    min_evidence_promote: int = 3
    min_utility_promote: float = 0.0
    duplicate_similarity: float = 0.85
    ntr_warn: float = 0.2
    ntr_restrict: float = 0.3
    ntr_retire: float = 0.5
    rr_min: float = 0.6
    retrieval_boost: float = 0.2
    cu_min_composition: float = 0.0
    composition_ncr_limit: float = 0.3
    cgr_collapse: float = -0.05
    collapse_periods: int = 2
    tfd_min_promote: float = 0.2
    transfer_override_min: float = 0.7
    ancient_core_min_age: int = 50
    zombie_permanent_archive_attempts: int = 2
    cannibalization_ratio: float = 0.5
    audit_max_actions: int = 5
    library_capacity: int = 50
    retire_max_reuse: int = 1
    retire_max_ts: float = 0.1
    su_min: float = 0.0

    def __post_init__(self) -> None:
        if self.ser_warn < 0 or self.ser_restrict < self.ser_warn:
            raise ValueError("ser_restrict must be >= ser_warn >= 0")
        if self.min_evidence_promote < 1:
            raise ValueError("min_evidence_promote must be >= 1")
        if self.collapse_periods < 1:
            raise ValueError("collapse_periods must be >= 1")
        if self.ancient_core_min_age < 1:
            raise ValueError("ancient_core_min_age must be >= 1")
        if self.zombie_permanent_archive_attempts < 1:
            raise ValueError("zombie_permanent_archive_attempts must be >= 1")
        if self.audit_max_actions < 1:
            raise ValueError("audit_max_actions must be >= 1")
        if self.library_capacity < 1:
            raise ValueError("library_capacity must be >= 1")
        if not 0.0 <= self.ntr_warn <= self.ntr_restrict <= self.ntr_retire <= 1.0:
            raise ValueError("ntr_warn <= ntr_restrict <= ntr_retire must hold in [0, 1]")
        for name in (
            "min_confidence_promote",
            "duplicate_similarity",
            "rr_min",
            "retrieval_boost",
            "composition_ncr_limit",
            "tfd_min_promote",
            "transfer_override_min",
            "cannibalization_ratio",
            "retire_max_ts",
        ):
            value = getattr(self, name)
            if not 0.0 <= float(value) <= 1.0:
                raise ValueError(f"{name} must be in [0, 1]")

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> SkillRobustnessConfig:
        known = {f for f in cls.__dataclass_fields__}
        payload = {k: v for k, v in (data or {}).items() if k in known}
        return cls(**payload)
