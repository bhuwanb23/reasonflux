"""Capability graph — shared skills / transfer / composition edges (Phase 11E-1)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from capability.models import Capability


@dataclass
class CapabilityGraph:
    """Undirected multi-relation graph over capability ids."""

    edges: dict[str, dict[str, set[str]]] = field(default_factory=dict)
    # edges[src][relation] = {dst, ...}

    def link(
        self, a: str, b: str, relation: str = "shared_skill"
    ) -> None:
        if a == b:
            return
        for src, dst in ((a, b), (b, a)):
            bucket = self.edges.setdefault(src, {})
            bucket.setdefault(relation, set()).add(dst)

    def neighbors(
        self, capability_id: str, relation: str | None = None
    ) -> set[str]:
        bucket = self.edges.get(capability_id) or {}
        if relation is None:
            out: set[str] = set()
            for vals in bucket.values():
                out |= vals
            return out
        return set(bucket.get(relation, set()))

    def edge_count(self) -> int:
        # Undirected: count each pair once.
        seen: set[tuple[str, str, str]] = set()
        for src, rels in self.edges.items():
            for rel, dsts in rels.items():
                for dst in dsts:
                    pair = (rel, min(src, dst), max(src, dst))
                    seen.add(pair)
        return len(seen)

    def link_shared_skills(self, capabilities: Sequence[Capability]) -> int:
        """Add shared_skill edges for overlapping membership. Returns new links."""
        caps = list(capabilities)
        added = 0
        for i, a in enumerate(caps):
            set_a = set(a.skill_ids)
            for b in caps[i + 1 :]:
                if set_a & set(b.skill_ids):
                    before = self.edge_count()
                    self.link(a.capability_id, b.capability_id, "shared_skill")
                    if self.edge_count() > before:
                        added += 1
        return added

    def to_dict(self) -> dict[str, Any]:
        return {
            src: {rel: sorted(dsts) for rel, dsts in rels.items()}
            for src, rels in self.edges.items()
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> CapabilityGraph:
        graph = cls()
        for src, rels in (data or {}).items():
            for rel, dsts in (rels or {}).items():
                for dst in dsts:
                    graph.link(str(src), str(dst), str(rel))
        return graph
