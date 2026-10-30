"""Capability robustness thresholds (Phase 11E-5)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class CapabilityRobustnessConfig:
    """Thresholds for CF1–CF10 detectors, CHS/CS, and hard growth gates."""

    # Fragmentation / inflation
    max_fragmentation_ratio: float = 0.8  # caps/skills
    min_skills_per_cap: float = 1.0
    inflation_coverage_gap: float = 0.4  # claimed - observed
    # Transfer / growth
    transfer_collapse_ratio: float = 0.5
    min_tg_positive: float = 0.0
    regression_negative_cgr_steps: int = 2
    saturation_csr: float = 0.05
    # Collapse / gaming / overfitting
    collapse_cgr_threshold: float = -0.05
    collapse_min_steps: int = 2
    overfitting_success_gap: float = 0.5  # train success vs holdout
    # Intelligence stagnation
    ig_stagnation_eps: float = 0.005
    # Health / stability
    chs_excellent: float = 0.8
    chs_healthy: float = 0.6
    chs_stable: float = 0.4
    chs_weak: float = 0.2
    cs_unstable: float = 0.3  # high variance → low CS
    # Hard gate
    hard_validation: bool = True
    require_evidence: bool = True

    def __post_init__(self) -> None:
        if self.regression_negative_cgr_steps < 1:
            raise ValueError("regression_negative_cgr_steps must be >= 1")
        if self.collapse_min_steps < 1:
            raise ValueError("collapse_min_steps must be >= 1")

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> CapabilityRobustnessConfig:
        known = {f for f in cls.__dataclass_fields__}
        payload = {k: v for k, v in (data or {}).items() if k in known}
        return cls(**payload)
