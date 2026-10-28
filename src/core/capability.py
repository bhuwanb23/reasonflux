"""CapabilityState — system intelligence snapshot for CGM (Phase 11B-1 Object 7)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.states import (
    CAPABILITY_PHASE_TRANSITIONS,
    SystemCapabilityPhase,
    assert_transition,
)


@dataclass(slots=True)
class CapabilityState:
    """Current intelligence state of the system (used by CGM)."""

    state_id: str
    skill_ids: list[str] = field(default_factory=list)
    transfer_metrics: dict[str, float] = field(default_factory=dict)
    growth_metrics: dict[str, float] = field(default_factory=dict)
    phase: SystemCapabilityPhase = SystemCapabilityPhase.COLD_START
    history: list[dict[str, Any]] = field(default_factory=list)
    timestamp: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.state_id or not str(self.state_id).strip():
            raise ValueError("state_id must be a non-empty string")
        if self.timestamp < 0:
            raise ValueError("timestamp must be >= 0")
        if not isinstance(self.phase, SystemCapabilityPhase):
            self.phase = SystemCapabilityPhase(self.phase)

    def transition_to(self, new_phase: SystemCapabilityPhase) -> None:
        assert_transition(self.phase, new_phase, CAPABILITY_PHASE_TRANSITIONS, "capability")
        self.phase = new_phase

    def snapshot(self) -> dict[str, Any]:
        """Append current metrics to history and return a copy."""
        entry = {
            "phase": self.phase.value,
            "skill_ids": list(self.skill_ids),
            "transfer_metrics": dict(self.transfer_metrics),
            "growth_metrics": dict(self.growth_metrics),
            "timestamp": self.timestamp,
        }
        self.history.append(entry)
        return dict(entry)

    def to_dict(self) -> dict[str, Any]:
        return {
            "state_id": self.state_id,
            "skill_ids": list(self.skill_ids),
            "transfer_metrics": dict(self.transfer_metrics),
            "growth_metrics": dict(self.growth_metrics),
            "phase": self.phase.value,
            "history": list(self.history),
            "timestamp": self.timestamp,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CapabilityState:
        return cls(
            state_id=data["state_id"],
            skill_ids=list(data.get("skill_ids") or []),
            transfer_metrics={
                str(k): float(v) for k, v in (data.get("transfer_metrics") or {}).items()
            },
            growth_metrics={
                str(k): float(v) for k, v in (data.get("growth_metrics") or {}).items()
            },
            phase=SystemCapabilityPhase(
                data.get("phase", SystemCapabilityPhase.COLD_START.value)
            ),
            history=list(data.get("history") or []),
            timestamp=float(data.get("timestamp", 0.0)),
            metadata=dict(data.get("metadata") or {}),
        )
