"""Skill evidence buckets and confidence (Phase 11D-1)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class SkillEvidence:
    """Four evidence buckets for a skill."""

    discovery: list[dict[str, Any]] = field(default_factory=list)
    transfer: list[dict[str, Any]] = field(default_factory=list)
    utility: list[dict[str, Any]] = field(default_factory=list)
    negative: list[dict[str, Any]] = field(default_factory=list)
    consistency: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "discovery": list(self.discovery),
            "transfer": list(self.transfer),
            "utility": list(self.utility),
            "negative": list(self.negative),
            "consistency": self.consistency,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> SkillEvidence:
        data = data or {}
        return cls(
            discovery=list(data.get("discovery") or []),
            transfer=list(data.get("transfer") or []),
            utility=list(data.get("utility") or []),
            negative=list(data.get("negative") or []),
            consistency=float(data.get("consistency", 0.0) or 0.0),
        )


def compute_skill_confidence(evidence: SkillEvidence) -> float:
    """Confidence = f(Evidence, Transfer, Consistency) in [0, 1]."""
    discovery_n = len(evidence.discovery)
    transfer_n = len(evidence.transfer)
    negative_n = len(evidence.negative)
    evidence_score = min(1.0, discovery_n / 3.0)
    transfer_score = min(1.0, transfer_n / 3.0)
    consistency = max(0.0, min(1.0, float(evidence.consistency)))
    penalty = min(1.0, negative_n / 5.0) * 0.3
    raw = 0.4 * evidence_score + 0.4 * transfer_score + 0.2 * consistency
    return max(0.0, min(1.0, raw - penalty))


def seed_evidence_from_invariant(
    *,
    invariant_id: str,
    frequency: int,
    consistency: float,
    transfer_score: float,
    transfer_events: int = 0,
) -> SkillEvidence:
    """Seed discovery/transfer evidence at skill birth."""
    discovery = [
        {
            "kind": "discovery",
            "invariant_id": invariant_id,
            "frequency": frequency,
        }
    ]
    transfer: list[dict[str, Any]] = []
    if transfer_score > 0 or transfer_events > 0:
        transfer.append(
            {
                "kind": "transfer",
                "score": transfer_score,
                "events": max(transfer_events, 1 if transfer_score > 0 else 0),
            }
        )
    return SkillEvidence(
        discovery=discovery,
        transfer=transfer,
        consistency=consistency,
    )
