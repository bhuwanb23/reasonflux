"""Capability entity — collection of skills (Phase 11E-1)."""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any

from capability.states import (
    CapabilityLifecycle,
    assert_capability_transition,
)


class CapabilityType(str, Enum):
    """How a capability is structured."""

    ATOMIC = "atomic"
    COMPOSITE = "composite"
    CROSS_DOMAIN = "cross_domain"
    EMERGENT = "emergent"


@dataclass(slots=True)
class Capability:
    """Stable reusable transferable collection of skills."""

    capability_id: str
    name: str = ""
    capability_type: CapabilityType = CapabilityType.ATOMIC
    skill_ids: list[str] = field(default_factory=list)
    coverage: float = 0.0
    utility: float = 0.0
    strength: float = 0.0
    confidence: float = 0.0
    state: CapabilityLifecycle = CapabilityLifecycle.EMERGING
    transfer_history: list[dict[str, Any]] = field(default_factory=list)
    utility_history: list[dict[str, Any]] = field(default_factory=list)
    growth_history: list[dict[str, Any]] = field(default_factory=list)
    evidence: dict[str, Any] = field(default_factory=dict)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.capability_id or not str(self.capability_id).strip():
            raise ValueError("capability_id must be a non-empty string")
        if not self.name:
            self.name = self.capability_id
        if not isinstance(self.capability_type, CapabilityType):
            self.capability_type = CapabilityType(self.capability_type)
        if not isinstance(self.state, CapabilityLifecycle):
            self.state = CapabilityLifecycle(self.state)
        if not self.evidence:
            self.evidence = {
                "skills": [],
                "transfer": [],
                "utility": [],
                "growth": [],
            }
        # Deduplicate membership while preserving order.
        seen: set[str] = set()
        ordered: list[str] = []
        for sid in self.skill_ids:
            key = str(sid)
            if key and key not in seen:
                seen.add(key)
                ordered.append(key)
        self.skill_ids = ordered

    def add_skill(self, skill_id: str) -> None:
        sid = str(skill_id).strip()
        if sid and sid not in self.skill_ids:
            self.skill_ids.append(sid)

    def remove_skill(self, skill_id: str) -> bool:
        sid = str(skill_id)
        if sid in self.skill_ids:
            self.skill_ids.remove(sid)
            return True
        return False

    def transition_to(self, new_state: CapabilityLifecycle) -> None:
        assert_capability_transition(self.state, new_state)
        self.state = new_state

    def to_dict(self) -> dict[str, Any]:
        return {
            "capability_id": self.capability_id,
            "name": self.name,
            "capability_type": self.capability_type.value,
            "skill_ids": list(self.skill_ids),
            "coverage": self.coverage,
            "utility": self.utility,
            "strength": self.strength,
            "confidence": self.confidence,
            "state": self.state.value,
            "transfer_history": list(self.transfer_history),
            "utility_history": list(self.utility_history),
            "growth_history": list(self.growth_history),
            "evidence": dict(self.evidence),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Capability:
        return cls(
            capability_id=data["capability_id"],
            name=data.get("name", ""),
            capability_type=CapabilityType(
                data.get("capability_type", CapabilityType.ATOMIC.value)
            ),
            skill_ids=list(data.get("skill_ids") or []),
            coverage=float(data.get("coverage", 0.0)),
            utility=float(data.get("utility", 0.0)),
            strength=float(data.get("strength", 0.0)),
            confidence=float(data.get("confidence", 0.0)),
            state=CapabilityLifecycle(
                data.get("state", CapabilityLifecycle.EMERGING.value)
            ),
            transfer_history=list(data.get("transfer_history") or []),
            utility_history=list(data.get("utility_history") or []),
            growth_history=list(data.get("growth_history") or []),
            evidence=dict(data.get("evidence") or {}),
            metadata=dict(data.get("metadata") or {}),
        )
