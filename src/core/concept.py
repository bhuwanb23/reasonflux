"""Concept — lightweight semantic link across invariants (Phase 11B-1 Object 4).

MVP: concepts exist but remain lightweight / future-facing in v0.1.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class Concept:
    """Semantic explanation connecting multiple invariants."""

    concept_id: str
    label: str
    invariant_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not self.concept_id or not str(self.concept_id).strip():
            raise ValueError("concept_id must be a non-empty string")
        if not self.label or not str(self.label).strip():
            raise ValueError("label must be a non-empty string")

    def to_dict(self) -> dict[str, Any]:
        return {
            "concept_id": self.concept_id,
            "label": self.label,
            "invariant_ids": list(self.invariant_ids),
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Concept:
        return cls(
            concept_id=data["concept_id"],
            label=data["label"],
            invariant_ids=list(data.get("invariant_ids") or []),
            metadata=dict(data.get("metadata") or {}),
        )
