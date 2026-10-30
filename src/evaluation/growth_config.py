"""Growth measurement thresholds (Phase 11E-2)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class GrowthConfig:
    """Weights and thresholds for CGR / IG / robustness checks."""

    # C_t / CapU-aligned weights (must sum to 1.0)
    w_su: float = 0.4
    w_ts: float = 0.25
    w_cov: float = 0.2
    w_comp: float = 0.15
    # IG = w_cgr·CGR + w_tg·TG + w_ug·UG + w_ccg·CCG + w_compg·CompG
    ig_w_cgr: float = 0.35
    ig_w_tg: float = 0.25
    ig_w_ug: float = 0.2
    ig_w_ccg: float = 0.15
    ig_w_compg: float = 0.05
    # Robustness / failure detectors
    skill_count_illusion_min_skills: int = 5
    skill_count_illusion_max_cgr: float = 0.01
    transfer_illusion_min_tg: float = 0.05
    transfer_illusion_max_utility_delta: float = 0.0
    coverage_inflation_min_ccg: float = 0.05
    coverage_inflation_max_transfer_delta: float = 0.0
    growth_without_utility_min_cgr: float = 0.02
    growth_without_utility_max_ug: float = 0.0
    metric_gaming_min_cgr: float = 0.05
    metric_gaming_max_evidence: int = 0
    # Saturation
    saturation_low_csr: float = 0.05
    # Default Δt
    default_dt: float = 1.0

    def __post_init__(self) -> None:
        ct = self.w_su + self.w_ts + self.w_cov + self.w_comp
        if abs(ct - 1.0) > 1e-6:
            raise ValueError("C_t weights must sum to 1.0")
        ig = (
            self.ig_w_cgr
            + self.ig_w_tg
            + self.ig_w_ug
            + self.ig_w_ccg
            + self.ig_w_compg
        )
        if abs(ig - 1.0) > 1e-6:
            raise ValueError("IG weights must sum to 1.0")
        if self.default_dt <= 0:
            raise ValueError("default_dt must be > 0")

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> GrowthConfig:
        known = {f for f in cls.__dataclass_fields__}
        payload = {k: v for k, v in (data or {}).items() if k in known}
        return cls(**payload)

    def ig_weights(self) -> dict[str, float]:
        return {
            "cgr": self.ig_w_cgr,
            "tg": self.ig_w_tg,
            "ug": self.ig_w_ug,
            "ccg": self.ig_w_ccg,
            "compg": self.ig_w_compg,
        }
