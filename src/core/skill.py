"""Skill and SkillCandidate — SCT knowledge objects (Phase 11B-1 Objects 5–6).

Skill = Executable Knowledge. Candidate is temporary pending SCV promotion.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.states import SKILL_TRANSITIONS, SkillState, assert_transition


def compute_scv(
    reuse: float,
    abstraction_gain: float,
    transfer_score: float,
    creation_cost: float,
) -> float:
    """SCV = Reuse × AG × TS − CreationCost."""
    return float(reuse) * float(abstraction_gain) * float(transfer_score) - float(
        creation_cost
    )


@dataclass(slots=True)
class SkillCandidate:
    """Invariant currently being evaluated for promotion to a Skill."""

    candidate_id: str
    source_invariant_id: str
    concept_id: str = ""
    trigger_conditions: list[str] = field(default_factory=list)
    execution_policy: str = ""
    expected_reuse: float = 0.0
    expected_transfer: float = 0.0
    abstraction_gain: float = 0.0
    transfer_score: float = 0.0
    creation_cost: float = 0.0
    reuse: float = 0.0
    scv: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.candidate_id or not str(self.candidate_id).strip():
            raise ValueError("candidate_id must be a non-empty string")
        if not self.source_invariant_id or not str(self.source_invariant_id).strip():
            raise ValueError("source_invariant_id must be a non-empty string")
        if self.creation_cost < 0:
            raise ValueError("creation_cost must be >= 0")
        if self.scv is None:
            self.scv = compute_scv(
                self.reuse if self.reuse else self.expected_reuse,
                self.abstraction_gain,
                self.transfer_score if self.transfer_score else self.expected_transfer,
                self.creation_cost,
            )

    def to_dict(self) -> dict[str, Any]:
        return {
            "candidate_id": self.candidate_id,
            "source_invariant_id": self.source_invariant_id,
            "concept_id": self.concept_id,
            "trigger_conditions": list(self.trigger_conditions),
            "execution_policy": self.execution_policy,
            "expected_reuse": self.expected_reuse,
            "expected_transfer": self.expected_transfer,
            "abstraction_gain": self.abstraction_gain,
            "transfer_score": self.transfer_score,
            "creation_cost": self.creation_cost,
            "reuse": self.reuse,
            "scv": self.scv,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SkillCandidate:
        return cls(
            candidate_id=data["candidate_id"],
            source_invariant_id=data["source_invariant_id"],
            concept_id=data.get("concept_id", ""),
            trigger_conditions=list(data.get("trigger_conditions") or []),
            execution_policy=data.get("execution_policy", ""),
            expected_reuse=float(data.get("expected_reuse", 0.0)),
            expected_transfer=float(data.get("expected_transfer", 0.0)),
            abstraction_gain=float(data.get("abstraction_gain", 0.0)),
            transfer_score=float(data.get("transfer_score", 0.0)),
            creation_cost=float(data.get("creation_cost", 0.0)),
            reuse=float(data.get("reuse", 0.0)),
            scv=data.get("scv"),
            metadata=dict(data.get("metadata") or {}),
        )


@dataclass(slots=True)
class Skill:
    """Reusable capability promoted from a SkillCandidate via SCT."""

    skill_id: str
    source_invariant_id: str = ""
    concept_id: str = ""
    trigger_conditions: list[str] = field(default_factory=list)
    execution_policy: str = ""
    abstraction_gain: float = 0.0
    transfer_score: float = 0.0
    creation_cost: float = 0.0
    reuse_count: int = 0
    utility: float = 0.0
    scv: float = 0.0
    state: SkillState = SkillState.PROMOTED
    transfer_history: list[dict[str, Any]] = field(default_factory=list)
    reuse_history: list[dict[str, Any]] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.skill_id or not str(self.skill_id).strip():
            raise ValueError("skill_id must be a non-empty string")
        if self.creation_cost < 0:
            raise ValueError("creation_cost must be >= 0")
        if self.reuse_count < 0:
            raise ValueError("reuse_count must be >= 0")
        if not isinstance(self.state, SkillState):
            self.state = SkillState(self.state)

    def transition_to(self, new_state: SkillState) -> None:
        assert_transition(self.state, new_state, SKILL_TRANSITIONS, "skill")
        self.state = new_state

    @classmethod
    def from_candidate(cls, candidate: SkillCandidate, skill_id: str | None = None) -> Skill:
        """Promote a candidate into a Skill (state=PROMOTED)."""
        return cls(
            skill_id=skill_id or candidate.candidate_id,
            source_invariant_id=candidate.source_invariant_id,
            concept_id=candidate.concept_id,
            trigger_conditions=list(candidate.trigger_conditions),
            execution_policy=candidate.execution_policy,
            abstraction_gain=candidate.abstraction_gain,
            transfer_score=candidate.transfer_score,
            creation_cost=candidate.creation_cost,
            reuse_count=int(candidate.reuse) if candidate.reuse else 0,
            scv=float(candidate.scv or 0.0),
            state=SkillState.PROMOTED,
            metadata=dict(candidate.metadata),
        )

    def to_dict(self) -> dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "source_invariant_id": self.source_invariant_id,
            "concept_id": self.concept_id,
            "trigger_conditions": list(self.trigger_conditions),
            "execution_policy": self.execution_policy,
            "abstraction_gain": self.abstraction_gain,
            "transfer_score": self.transfer_score,
            "creation_cost": self.creation_cost,
            "reuse_count": self.reuse_count,
            "utility": self.utility,
            "scv": self.scv,
            "state": self.state.value,
            "transfer_history": list(self.transfer_history),
            "reuse_history": list(self.reuse_history),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Skill:
        return cls(
            skill_id=data["skill_id"],
            source_invariant_id=data.get("source_invariant_id", ""),
            concept_id=data.get("concept_id", ""),
            trigger_conditions=list(data.get("trigger_conditions") or []),
            execution_policy=data.get("execution_policy", ""),
            abstraction_gain=float(data.get("abstraction_gain", 0.0)),
            transfer_score=float(data.get("transfer_score", 0.0)),
            creation_cost=float(data.get("creation_cost", 0.0)),
            reuse_count=int(data.get("reuse_count", 0)),
            utility=float(data.get("utility", 0.0)),
            scv=float(data.get("scv", 0.0)),
            state=SkillState(data.get("state", SkillState.PROMOTED.value)),
            transfer_history=list(data.get("transfer_history") or []),
            reuse_history=list(data.get("reuse_history") or []),
            metadata=dict(data.get("metadata") or {}),
        )
