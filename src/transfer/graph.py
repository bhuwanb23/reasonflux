"""Transfer graph — task families as nodes, observed transfers as edges (11C-4)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from transfer.records import TransferRecord


@dataclass(slots=True)
class TransferEdge:
    """Directed weighted edge between task families."""

    source: str
    target: str
    weight: float = 1.0
    invariant_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "target": self.target,
            "weight": self.weight,
            "invariant_ids": list(self.invariant_ids),
        }


@dataclass
class TransferGraph:
    """Pure-Python transfer graph (no networkx required)."""

    _nodes: set[str] = field(default_factory=set)
    _edges: dict[tuple[str, str], TransferEdge] = field(default_factory=dict)

    def add_node(self, family: str) -> None:
        if family and str(family).strip():
            self._nodes.add(str(family).strip())

    def add_edge(
        self,
        source: str,
        target: str,
        weight: float = 1.0,
        invariant_id: str | None = None,
    ) -> None:
        src, tgt = str(source).strip(), str(target).strip()
        if not src or not tgt:
            raise ValueError("source and target must be non-empty")
        if weight < 0:
            raise ValueError("weight must be >= 0")
        self.add_node(src)
        self.add_node(tgt)
        key = (src, tgt)
        edge = self._edges.get(key)
        if edge is None:
            edge = TransferEdge(source=src, target=tgt, weight=weight)
            self._edges[key] = edge
        else:
            edge.weight += weight
        if invariant_id and invariant_id not in edge.invariant_ids:
            edge.invariant_ids.append(invariant_id)

    def nodes(self) -> list[str]:
        return sorted(self._nodes)

    def edges(self) -> list[TransferEdge]:
        return list(self._edges.values())

    def neighbors(self, family: str) -> list[str]:
        fam = str(family).strip()
        return sorted({e.target for e in self._edges.values() if e.source == fam})

    def invariants_between(self, source: str, target: str) -> list[str]:
        edge = self._edges.get((str(source).strip(), str(target).strip()))
        return list(edge.invariant_ids) if edge else []

    def to_dict(self) -> dict:
        return {
            "nodes": self.nodes(),
            "edges": [e.to_dict() for e in self.edges()],
        }

    @classmethod
    def from_records(cls, records: Iterable[TransferRecord]) -> TransferGraph:
        graph = cls()
        for record in records:
            # Only successful transfers contribute to the positive transfer graph.
            weight = 1.0 if record.success else 0.0
            if weight <= 0:
                # Still register nodes so negative attempts are visible as isolates.
                graph.add_node(record.source_family)
                graph.add_node(record.target_family)
                continue
            graph.add_edge(
                record.source_family,
                record.target_family,
                weight=weight,
                invariant_id=record.invariant_id,
            )
        return graph
