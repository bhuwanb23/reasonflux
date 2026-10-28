"""Module interface contracts (Phase 11B-3).

These Protocols define what information modules may exchange.
Algorithm modules implement them later; Phase 11B only defines the boundaries.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol, runtime_checkable

from core.invariant import Invariant
from core.skill import Skill
from core.trace import ReasoningTrace


@dataclass(slots=True)
class SkillUsageStats:
    """Usage / reuse / transfer statistics for evaluation (Library → Evaluation)."""

    skill_id: str
    reuse_count: int = 0
    utility: float = 0.0
    transfer_score: float = 0.0
    transfer_events: int = 0
    last_used_timestamp: float | None = None
    metadata: dict = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "skill_id": self.skill_id,
            "reuse_count": self.reuse_count,
            "utility": self.utility,
            "transfer_score": self.transfer_score,
            "transfer_events": self.transfer_events,
            "last_used_timestamp": self.last_used_timestamp,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict) -> SkillUsageStats:
        return cls(
            skill_id=data["skill_id"],
            reuse_count=int(data.get("reuse_count", 0)),
            utility=float(data.get("utility", 0.0)),
            transfer_score=float(data.get("transfer_score", 0.0)),
            transfer_events=int(data.get("transfer_events", 0)),
            last_used_timestamp=data.get("last_used_timestamp"),
            metadata=dict(data.get("metadata") or {}),
        )


@runtime_checkable
class TraceBatchProvider(Protocol):
    """Contract 1: Trace Logger → Invariant Detector.

    Provides ReasoningTraces only. Detector must not see raw Tasks.
    """

    def get_traces(self) -> list[ReasoningTrace]:
        """Return a batch of reasoning traces for mining."""
        ...


@runtime_checkable
class ValidatedInvariantProvider(Protocol):
    """Contract 2: Invariant Detector → SCT.

    Provides validated invariants. SCT must not need raw traces.
    """

    def get_validated_invariants(self) -> list[Invariant]:
        """Return invariants that passed validation (validated or strong)."""
        ...


@runtime_checkable
class PromotedSkillProvider(Protocol):
    """Contract 3: SCT → Skill Library.

    Provides promoted skills. Library stores/manages; does not decide creation.
    """

    def get_promoted_skills(self) -> list[Skill]:
        """Return skills that passed SCT promotion."""
        ...


@runtime_checkable
class SkillUsageStatsProvider(Protocol):
    """Contract 4: Skill Library → Evaluation Engine.

    Provides usage statistics, reuse data, and transfer data.
    """

    def get_usage_stats(self) -> list[SkillUsageStats]:
        """Return per-skill usage / reuse / transfer statistics."""
        ...
