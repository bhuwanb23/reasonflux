"""Composition graph — successful sequential edges (Phase 11D-4)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence


@dataclass
class CompositionGraph:
    """Directed adjacency: A→B means sequential A then B succeeded."""

    edges: dict[str, set[str]] = field(default_factory=dict)
    success_counts: dict[str, int] = field(default_factory=dict)

    def record_success(self, order: Sequence[str]) -> None:
        ids = [str(x) for x in order if str(x).strip()]
        for a, b in zip(ids, ids[1:]):
            self.edges.setdefault(a, set()).add(b)
            key = f"{a}->{b}"
            self.success_counts[key] = int(self.success_counts.get(key, 0)) + 1

    def neighbors(self, skill_id: str) -> set[str]:
        return set(self.edges.get(skill_id, set()))

    def edge_count(self) -> int:
        return sum(len(v) for v in self.edges.values())

    def to_dict(self) -> dict[str, Any]:
        return {
            "edges": {k: sorted(v) for k, v in self.edges.items()},
            "success_counts": dict(self.success_counts),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> CompositionGraph:
        data = data or {}
        edges_raw = data.get("edges") or {}
        edges = {str(k): set(v) for k, v in edges_raw.items()}
        counts = {
            str(k): int(v) for k, v in (data.get("success_counts") or {}).items()
        }
        return cls(edges=edges, success_counts=counts)
