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
        for name in (
            "min_consistency",
            "min_generality",
            "min_reasoning_value",
            "default_cp",
            "core_su",
            "core_min_transfer",
        ):
            value = getattr(self, name)
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0, 1]")

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> SkillConfig:
        known = {f for f in cls.__dataclass_fields__}
        payload = {k: v for k, v in (data or {}).items() if k in known}
        return cls(**payload)
