"""Capability representation thresholds (Phase 11E-1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class CapabilityConfig:
    """Thresholds for CapU, coverage, lifecycle, and representation guards."""

    min_skills: int = 1
    min_transfer_events: int = 1
    min_utility: float = 0.0
    min_confidence: float = 0.3
    min_coverage: float = 0.1
    ccov_family_norm: int = 5
    capu_w_su: float = 0.4
    capu_w_ts: float = 0.25
    capu_w_cov: float = 0.2
    capu_w_comp: float = 0.15
    strength_reuse_norm: float = 10.0
    core_min_strength: float = 0.6
    core_min_confidence: float = 0.5
    decline_ug: float = -0.02
    overlap_similarity: float = 0.85
    max_capabilities: int = 30
    monolith_skill_fraction: float = 0.8
    archive_low_utility_periods: int = 3
    skill_count_norm: float = 5.0

    def __post_init__(self) -> None:
        if self.min_skills < 1:
            raise ValueError("min_skills must be >= 1")
        if self.min_transfer_events < 0:
            raise ValueError("min_transfer_events must be >= 0")
        if self.ccov_family_norm < 1:
            raise ValueError("ccov_family_norm must be >= 1")
        if self.max_capabilities < 1:
            raise ValueError("max_capabilities must be >= 1")
        if self.archive_low_utility_periods < 1:
            raise ValueError("archive_low_utility_periods must be >= 1")
        if self.strength_reuse_norm <= 0 or self.skill_count_norm <= 0:
            raise ValueError("strength_reuse_norm and skill_count_norm must be > 0")
        weight_sum = (
            self.capu_w_su + self.capu_w_ts + self.capu_w_cov + self.capu_w_comp
        )
        if abs(weight_sum - 1.0) > 1e-6:
            raise ValueError("capu weights must sum to 1.0")
        for name in (
            "min_confidence",
            "min_coverage",
            "core_min_strength",
            "core_min_confidence",
            "overlap_similarity",
            "monolith_skill_fraction",
        ):
            value = getattr(self, name)
            if not 0.0 <= float(value) <= 1.0:
                raise ValueError(f"{name} must be in [0, 1]")
        for name in ("capu_w_su", "capu_w_ts", "capu_w_cov", "capu_w_comp"):
            if float(getattr(self, name)) < 0:
                raise ValueError(f"{name} must be >= 0")

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> CapabilityConfig:
        known = {f for f in cls.__dataclass_fields__}
        payload = {k: v for k, v in (data or {}).items() if k in known}
        return cls(**payload)
