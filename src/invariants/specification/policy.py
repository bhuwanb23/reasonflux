"""Invariant policy thresholds and formal specification constants (11C-1)."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.invariant import MVP_INVARIANT_TYPES, InvariantConfidence, InvariantType
from core.states import InvariantState

#: The four conditions an invariant must satisfy (all required).
QUALIFICATION_RULES: tuple[str, ...] = (
    "recurrence",
    "stability",
    "generality",
    "transfer_utility",
)

SPECIFICATION: dict[str, Any] = {
    "definition": (
        "An invariant is a recurring reasoning structure that remains stable "
        "across multiple successful task-solving experiences and contributes "
        "to future transfer."
    ),
    "qualification_rules": QUALIFICATION_RULES,
    "taxonomy": [t.value for t in InvariantType],
    "mvp_supported_types": sorted(t.value for t in MVP_INVARIANT_TYPES),
    "lifecycle": [
        InvariantState.CANDIDATE.value,
        InvariantState.DETECTED.value,
        InvariantState.VALIDATED.value,
        InvariantState.TRANSFER_VERIFIED.value,
        InvariantState.SKILL_CANDIDATE.value,
    ],
    "confidence_levels": [c.value for c in InvariantConfidence],
    "hierarchy": ["operations", "patterns", "invariants"],
}


@dataclass(slots=True)
class InvariantPolicy:
    """Thresholds governing qualification, rejection, and confidence."""

    min_frequency: int = 3
    min_consistency: float = 0.6
    min_task_families: int = 2
    min_generality: float = 0.0
    require_transfer_evidence: bool = True
    min_transfer_events: int = 1
    universal_noise_generality: float = 0.95
    task_specific_terms: tuple[str, ...] = (
        "red",
        "blue",
        "green",
        "yellow",
        "triangle",
        "square",
        "circle",
        "row 0",
        "col 0",
    )
    moderate_score: float = 0.4
    strong_score: float = 0.7

    def __post_init__(self) -> None:
        if self.min_frequency < 1:
            raise ValueError("min_frequency must be >= 1")
        if not 0.0 <= self.min_consistency <= 1.0:
            raise ValueError("min_consistency must be in [0, 1]")
        if self.min_task_families < 1:
            raise ValueError("min_task_families must be >= 1")

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> InvariantPolicy:
        known = {f for f in cls.__dataclass_fields__}
        payload = {k: v for k, v in (data or {}).items() if k in known}
        if "task_specific_terms" in payload:
            payload["task_specific_terms"] = tuple(payload["task_specific_terms"])
        return cls(**payload)
