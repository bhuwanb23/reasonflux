"""Invariant — recurring reasoning structure (Phase 11B-1 / 11C-1).

Supports Invariant Discovery Theory (IDT).

Phase 11C-1 definition: an invariant is a recurring reasoning structure that
remains stable across multiple successful task-solving experiences and
contributes to future transfer.

Invariant = Observation (not a Skill).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from core.states import (
    INVARIANT_TRANSITIONS,
    InvariantState,
    assert_transition,
)


class InvariantType(str, Enum):
    """Invariant taxonomy (Phase 11C-1).

    Operational  — recurring single operations.
    Procedural   — recurring operation sequences (core of the MVP).
    Structural   — recurring higher-level reasoning structure.
    Transfer     — structures reused across task families (highest value).
    """

    OPERATIONAL = "operational"
    PROCEDURAL = "procedural"
    STRUCTURAL = "structural"
    TRANSFER = "transfer"


#: Types supported by the v0.1 MVP (11C-1 MVP Scope).
MVP_INVARIANT_TYPES: frozenset[InvariantType] = frozenset(
    {InvariantType.OPERATIONAL, InvariantType.PROCEDURAL}
)


class InvariantConfidence(str, Enum):
    """Confidence category derived from recurrence, stability, transfer."""

    WEAK = "weak"
    MODERATE = "moderate"
    STRONG = "strong"


@dataclass(slots=True)
class InvariantEvidence:
    """Evidence supporting an invariant (Phase 11C-1 evidence model).

    Every invariant must maintain evidence; without evidence there is no
    promotion.
    """

    observations: int = 0
    task_families: list[str] = field(default_factory=list)
    transfer_events: int = 0
    reuse_events: int = 0

    def __post_init__(self) -> None:
        if self.observations < 0:
            raise ValueError("observations must be >= 0")
        if self.transfer_events < 0:
            raise ValueError("transfer_events must be >= 0")
        if self.reuse_events < 0:
            raise ValueError("reuse_events must be >= 0")

    @property
    def task_family_count(self) -> int:
        return len(set(self.task_families))

    def record_observation(self, task_family: str | None = None) -> None:
        self.observations += 1
        if task_family and task_family not in self.task_families:
            self.task_families.append(task_family)

    def record_transfer(self, amount: int = 1) -> None:
        if amount < 0:
            raise ValueError("transfer amount must be >= 0")
        self.transfer_events += amount

    def record_reuse(self, amount: int = 1) -> None:
        if amount < 0:
            raise ValueError("reuse amount must be >= 0")
        self.reuse_events += amount

    def to_dict(self) -> dict[str, Any]:
        return {
            "observations": self.observations,
            "task_families": list(self.task_families),
            "transfer_events": self.transfer_events,
            "reuse_events": self.reuse_events,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> InvariantEvidence:
        return cls(
            observations=int(data.get("observations", 0)),
            task_families=list(data.get("task_families") or []),
            transfer_events=int(data.get("transfer_events", 0)),
            reuse_events=int(data.get("reuse_events", 0)),
        )


@dataclass(slots=True)
class Invariant:
    """Stable structure recurring across reasoning experiences."""

    invariant_id: str
    pattern_signature: list[str]
    frequency: int = 0
    consistency: float = 0.0
    generality: float = 0.0
    transfer_contribution: float = 0.0
    associated_concepts: list[str] = field(default_factory=list)
    source_trace_ids: list[str] = field(default_factory=list)
    state: InvariantState = InvariantState.DETECTED
    metadata: dict[str, Any] = field(default_factory=dict)
    # Phase 11C-1 identity / taxonomy / evidence
    origin: str = ""
    task_families: list[str] = field(default_factory=list)
    invariant_type: InvariantType = InvariantType.PROCEDURAL
    evidence: InvariantEvidence = field(default_factory=InvariantEvidence)
    confidence: InvariantConfidence = InvariantConfidence.WEAK
    _strength_override: float | None = field(default=None, repr=False)

    def __post_init__(self) -> None:
        if not self.invariant_id or not str(self.invariant_id).strip():
            raise ValueError("invariant_id must be a non-empty string")
        if self.frequency < 0:
            raise ValueError("frequency must be >= 0")
        if not 0.0 <= self.consistency <= 1.0:
            raise ValueError("consistency must be in [0, 1]")
        if not 0.0 <= self.generality <= 1.0:
            raise ValueError("generality must be in [0, 1]")
        if not isinstance(self.state, InvariantState):
            self.state = InvariantState(self.state)
        if not isinstance(self.invariant_type, InvariantType):
            self.invariant_type = InvariantType(self.invariant_type)
        if not isinstance(self.confidence, InvariantConfidence):
            self.confidence = InvariantConfidence(self.confidence)
        if self.pattern_signature is None:
            self.pattern_signature = []
        if not self.task_families and self.evidence.task_families:
            self.task_families = list(self.evidence.task_families)

    # -- derived quantities -------------------------------------------------

    @property
    def strength(self) -> float:
        """IS = frequency × consistency × generality (unless overridden)."""
        if self._strength_override is not None:
            return self._strength_override
        return float(self.frequency) * self.consistency * self.generality

    @property
    def is_mvp_supported(self) -> bool:
        """True if this invariant type is in the v0.1 MVP scope."""
        return self.invariant_type in MVP_INVARIANT_TYPES

    def set_strength(self, value: float | None) -> None:
        """Optionally override computed strength (e.g. after external ranking)."""
        self._strength_override = value

    # -- evidence -----------------------------------------------------------

    def record_observation(self, task_family: str | None = None) -> None:
        """Record one observed occurrence and keep evidence/counters aligned."""
        self.frequency += 1
        self.evidence.record_observation(task_family)
        if task_family and task_family not in self.task_families:
            self.task_families.append(task_family)

    def record_transfer(self, amount: int = 1) -> None:
        self.evidence.record_transfer(amount)

    def record_reuse(self, amount: int = 1) -> None:
        self.evidence.record_reuse(amount)

    # -- lifecycle ----------------------------------------------------------

    def transition_to(self, new_state: InvariantState) -> None:
        assert_transition(self.state, new_state, INVARIANT_TRANSITIONS, "invariant")
        self.state = new_state

    # -- serialization ------------------------------------------------------

    def to_dict(self) -> dict[str, Any]:
        return {
            "invariant_id": self.invariant_id,
            "pattern_signature": list(self.pattern_signature),
            "frequency": self.frequency,
            "consistency": self.consistency,
            "generality": self.generality,
            "strength": self.strength,
            "transfer_contribution": self.transfer_contribution,
            "associated_concepts": list(self.associated_concepts),
            "source_trace_ids": list(self.source_trace_ids),
            "state": self.state.value,
            "metadata": dict(self.metadata),
            "origin": self.origin,
            "task_families": list(self.task_families),
            "invariant_type": self.invariant_type.value,
            "evidence": self.evidence.to_dict(),
            "confidence": self.confidence.value,
            "_strength_override": self._strength_override,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Invariant:
        inv = cls(
            invariant_id=data["invariant_id"],
            pattern_signature=list(data.get("pattern_signature") or []),
            frequency=int(data.get("frequency", 0)),
            consistency=float(data.get("consistency", 0.0)),
            generality=float(data.get("generality", 0.0)),
            transfer_contribution=float(data.get("transfer_contribution", 0.0)),
            associated_concepts=list(data.get("associated_concepts") or []),
            source_trace_ids=list(data.get("source_trace_ids") or []),
            state=InvariantState(data.get("state", InvariantState.DETECTED.value)),
            metadata=dict(data.get("metadata") or {}),
            origin=data.get("origin", ""),
            task_families=list(data.get("task_families") or []),
            invariant_type=InvariantType(
                data.get("invariant_type", InvariantType.PROCEDURAL.value)
            ),
            evidence=InvariantEvidence.from_dict(data.get("evidence") or {}),
            confidence=InvariantConfidence(
                data.get("confidence", InvariantConfidence.WEAK.value)
            ),
        )
        override = data.get("_strength_override")
        if override is None and "strength" in data:
            computed = float(inv.frequency) * inv.consistency * inv.generality
            stored = float(data["strength"])
            if abs(stored - computed) > 1e-9:
                inv.set_strength(stored)
        elif override is not None:
            inv.set_strength(float(override))
        return inv
