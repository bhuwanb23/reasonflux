"""Composition candidate model and states (Phase 11D-4)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class CompositionState(str, Enum):
    """Lifecycle of a sequential composition (not SkillState)."""

    CANDIDATE = "candidate"
    VALIDATED = "validated"
    REUSABLE = "reusable"
    DISCARDED = "discarded"
    PROMOTED = "promoted"


def composition_id_for(skill_ids: list[str]) -> str:
    """Stable id for an ordered sequential chain."""
    return "+".join(str(s) for s in skill_ids)


@dataclass(slots=True)
class CompositionCandidate:
    """Temporary sequential combination of two or more skills."""

    composition_id: str
    skill_ids: list[str]
    order: list[str] = field(default_factory=list)
    expected_utility: float = 0.0
    expected_transfer: float = 0.0
    composition_cost: float = 0.0
    cu: float = 0.0
    confidence: float = 0.0
    state: CompositionState = CompositionState.CANDIDATE
    evidence: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.skill_ids or len(self.skill_ids) < 2:
            raise ValueError("skill_ids must contain at least 2 skills")
        if not self.order:
            self.order = list(self.skill_ids)
        if not self.composition_id:
            self.composition_id = composition_id_for(self.order)
        if not isinstance(self.state, CompositionState):
            self.state = CompositionState(self.state)
        if not self.evidence:
            self.evidence = {
                "uses": 0,
                "successes": 0,
                "failures": 0,
                "transfer_events": [],
                "families": [],
                "cost_reductions": [],
            }

    @property
    def ncr(self) -> float:
        uses = int(self.evidence.get("uses", 0) or 0)
        if uses <= 0:
            return 0.0
        return float(self.evidence.get("failures", 0) or 0) / uses

    def to_dict(self) -> dict[str, Any]:
        return {
            "composition_id": self.composition_id,
            "skill_ids": list(self.skill_ids),
            "order": list(self.order),
            "expected_utility": self.expected_utility,
            "expected_transfer": self.expected_transfer,
            "composition_cost": self.composition_cost,
            "cu": self.cu,
            "confidence": self.confidence,
            "state": self.state.value,
            "evidence": dict(self.evidence),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CompositionCandidate:
        return cls(
            composition_id=data.get("composition_id")
            or composition_id_for(list(data.get("order") or data.get("skill_ids") or [])),
            skill_ids=list(data["skill_ids"]),
            order=list(data.get("order") or data["skill_ids"]),
            expected_utility=float(data.get("expected_utility", 0.0)),
            expected_transfer=float(data.get("expected_transfer", 0.0)),
            composition_cost=float(data.get("composition_cost", 0.0)),
            cu=float(data.get("cu", 0.0)),
            confidence=float(data.get("confidence", 0.0)),
            state=CompositionState(data.get("state", CompositionState.CANDIDATE.value)),
            evidence=dict(data.get("evidence") or {}),
            metadata=dict(data.get("metadata") or {}),
        )
