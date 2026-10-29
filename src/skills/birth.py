"""Skill birth event — when / why / from which invariant (11D-1)."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SkillBirthRecord:
    """Official birth record emitted at skill promotion."""

    skill_id: str
    source_invariant_id: str
    conditions: dict[str, Any] = field(default_factory=dict)
    evidence: dict[str, Any] = field(default_factory=dict)
    transfer_history: list[dict[str, Any]] = field(default_factory=list)
    timestamp: float = 0.0
    reasons: list[str] = field(default_factory=list)

    def __post_init__(self) -> None:
        if not self.skill_id or not str(self.skill_id).strip():
            raise ValueError("skill_id must be a non-empty string")
        if not self.source_invariant_id or not str(self.source_invariant_id).strip():
            raise ValueError("source_invariant_id must be a non-empty string")
        if self.timestamp <= 0:
            self.timestamp = time.time()

    def to_dict(self) -> dict[str, Any]:
        return {
            "skill_id": self.skill_id,
            "source_invariant_id": self.source_invariant_id,
            "conditions": dict(self.conditions),
            "evidence": dict(self.evidence),
            "transfer_history": list(self.transfer_history),
            "timestamp": self.timestamp,
            "reasons": list(self.reasons),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> SkillBirthRecord:
        return cls(
            skill_id=data["skill_id"],
            source_invariant_id=data["source_invariant_id"],
            conditions=dict(data.get("conditions") or {}),
            evidence=dict(data.get("evidence") or {}),
            transfer_history=list(data.get("transfer_history") or []),
            timestamp=float(data.get("timestamp", 0.0) or 0.0),
            reasons=list(data.get("reasons") or []),
        )


def make_birth_record(
    *,
    skill_id: str,
    source_invariant_id: str,
    scv: float,
    transfer_score: float,
    evidence: dict[str, Any],
    transfer_history: list[dict[str, Any]] | None = None,
    reasons: list[str] | None = None,
) -> SkillBirthRecord:
    """Build a birth record from promotion conditions."""
    return SkillBirthRecord(
        skill_id=skill_id,
        source_invariant_id=source_invariant_id,
        conditions={
            "scv": scv,
            "transfer_score": transfer_score,
            "passed": True,
        },
        evidence=dict(evidence),
        transfer_history=list(transfer_history or []),
        reasons=list(reasons or ["promoted"]),
    )
