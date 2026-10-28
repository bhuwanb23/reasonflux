"""Invariant — recurring reasoning structure (Phase 11B-1 Object 3).

Supports Invariant Discovery Theory (IDT).
Invariant = Observation (not a Skill).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.states import (
    INVARIANT_TRANSITIONS,
    InvariantState,
    assert_transition,
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
        if self.pattern_signature is None:
            self.pattern_signature = []

    @property
    def strength(self) -> float:
        """IS = frequency × consistency × generality (unless overridden)."""
        if self._strength_override is not None:
            return self._strength_override
        return float(self.frequency) * self.consistency * self.generality

    def set_strength(self, value: float | None) -> None:
        """Optionally override computed strength (e.g. after external ranking)."""
        self._strength_override = value

    def transition_to(self, new_state: InvariantState) -> None:
        assert_transition(self.state, new_state, INVARIANT_TRANSITIONS, "invariant")
        self.state = new_state

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
