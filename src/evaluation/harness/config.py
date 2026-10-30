"""Harness thresholds (Phase 11E-4)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class HarnessConfig:
    """Evaluation harness knobs."""

    default_dt: float = 1.0
    min_cgr_success: float = 0.01
    min_igr_success: float = 0.005
    max_ntr_success: float = 0.3
    min_reuse_success: int = 1
    ci_z: float = 1.96  # ~95% normal CI
    report_dir: str = "reports/metrics"
    default_level: str = "capability"
    experiences_per_step: int = 5
    hard_validation: bool = True

    def __post_init__(self) -> None:
        if self.default_dt <= 0:
            raise ValueError("default_dt must be > 0")
        if self.ci_z <= 0:
            raise ValueError("ci_z must be > 0")

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> HarnessConfig:
        known = {f for f in cls.__dataclass_fields__}
        payload = {k: v for k, v in (data or {}).items() if k in known}
        return cls(**payload)
