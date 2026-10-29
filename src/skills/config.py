"""Skill creation thresholds (Phase 11D-1 SCT)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class SkillConfig:
    """Thresholds for skill intake, SCV, transfer, and promotion."""

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
        for name in ("min_consistency", "min_generality", "min_reasoning_value"):
            value = getattr(self, name)
            if not 0.0 <= value <= 1.0:
                raise ValueError(f"{name} must be in [0, 1]")

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> SkillConfig:
        known = {f for f in cls.__dataclass_fields__}
        payload = {k: v for k, v in (data or {}).items() if k in known}
        return cls(**payload)
