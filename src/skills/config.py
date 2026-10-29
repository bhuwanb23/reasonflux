"""Skill creation and utility thresholds (Phase 11D-1 / 11D-2)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class SkillConfig:
    """Thresholds for skill intake, SCV, transfer, promotion, and SU."""

    skill_creation_threshold: float = 0.0
    skill_creation_threshold_strict: float = 2.0
    min_its: float = 0.5
    min_evidence: int = 3
    ntr_limit: float = 0.3
    similarity_merge: float = 0.85
    default_creation_cost: float = 0.1
    min_frequency: int = 3
    min_consistency: float = 0.6
    min_generality: float = 0.3
    min_reasoning_value: float = 0.1
    # Phase 11D-2 utility economics
    su_min: float = 0.0
    reuse_norm: float = 10.0
    tv_coverage_norm: float = 5.0
    base_maintenance: float = 0.05
    ntr_impact: float = 1.0
    default_cp: float = 0.3
    library_capacity: int = 50
    core_su: float = 0.6
    core_min_reuse: int = 3
    core_min_transfer: float = 0.5
    # Phase 11D-3 lifecycle
    growing_ug: float = 0.02
    dormant_after_tasks: int = 10
    core_growth_periods: int = 2
    retire_low_su_periods: int = 3
    retire_max_reuse: int = 1
    retire_max_ts: float = 0.1
    retire_min_age_tasks: int = 20
    decay_lambda: float = 0.01
    health_healthy: float = 0.75
    health_stable: float = 0.5
    health_weak: float = 0.25
    health_w_u: float = 0.4
    health_w_r: float = 0.2
    health_w_t: float = 0.2
    health_w_c: float = 0.2
    reactivate_min_evidence: int = 2
    reactivate_min_expected_su: float | None = None  # defaults to su_min
    reactivate_max_attempts: int = 2
    archive_after_tasks: int = 20

    def __post_init__(self) -> None:
        if self.min_evidence < 1:
            raise ValueError("min_evidence must be >= 1")
        if self.min_frequency < 1:
            raise ValueError("min_frequency must be >= 1")
        if not 0.0 <= self.min_its <= 1.0:
            raise ValueError("min_its must be in [0, 1]")
        if not 0.0 <= self.ntr_limit <= 1.0:
            raise ValueError("ntr_limit must be in [0, 1]")
        if not 0.0 <= self.similarity_merge <= 1.0:
            raise ValueError("similarity_merge must be in [0, 1]")
        if self.default_creation_cost < 0:
            raise ValueError("default_creation_cost must be >= 0")
        if self.reuse_norm <= 0 or self.tv_coverage_norm <= 0:
            raise ValueError("reuse_norm and tv_coverage_norm must be > 0")
        if self.base_maintenance < 0:
            raise ValueError("base_maintenance must be >= 0")
        if self.library_capacity < 1:
            raise ValueError("library_capacity must be >= 1")
        if self.core_min_reuse < 1:
            raise ValueError("core_min_reuse must be >= 1")
        if self.dormant_after_tasks < 1:
            raise ValueError("dormant_after_tasks must be >= 1")
        if self.core_growth_periods < 1:
            raise ValueError("core_growth_periods must be >= 1")
        if self.retire_low_su_periods < 1:
            raise ValueError("retire_low_su_periods must be >= 1")
        if self.retire_min_age_tasks < 1:
            raise ValueError("retire_min_age_tasks must be >= 1")
        if self.retire_max_reuse < 0:
            raise ValueError("retire_max_reuse must be >= 0")
        if self.archive_after_tasks < 1:
            raise ValueError("archive_after_tasks must be >= 1")
        if self.reactivate_min_evidence < 1:
            raise ValueError("reactivate_min_evidence must be >= 1")
        if self.reactivate_max_attempts < 1:
            raise ValueError("reactivate_max_attempts must be >= 1")
        if self.decay_lambda < 0:
            raise ValueError("decay_lambda must be >= 0")
        if self.reactivate_min_expected_su is None:
            self.reactivate_min_expected_su = self.su_min
        for name in (
            "min_consistency",
            "min_generality",
            "min_reasoning_value",
            "default_cp",
            "core_su",
            "core_min_transfer",
            "health_healthy",
            "health_stable",
            "health_weak",
            "retire_max_ts",
        ):
            value = getattr(self, name)
            if not 0.0 <= float(value) <= 1.0:
                raise ValueError(f"{name} must be in [0, 1]")
        for name in ("health_w_u", "health_w_r", "health_w_t", "health_w_c"):
            value = getattr(self, name)
            if float(value) < 0:
                raise ValueError(f"{name} must be >= 0")

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> SkillConfig:
        known = {f for f in cls.__dataclass_fields__}
        payload = {k: v for k, v in (data or {}).items() if k in known}
        return cls(**payload)
