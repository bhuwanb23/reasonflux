"""Intelligence graph — capability nodes with transfer/composition/shared edges."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from capability.graph import CapabilityGraph
from capability.library import CapabilityLibrary
from skills.library import SkillLibrary


@dataclass(slots=True)
class IntelligenceGraph:
    graph: CapabilityGraph

    def to_dict(self) -> dict[str, Any]:
        return self.graph.to_dict()

    def edge_count(self) -> int:
        return self.graph.edge_count()


def build_intelligence_graph(
    capability_library: CapabilityLibrary,
    skill_library: SkillLibrary | None = None,
) -> IntelligenceGraph:
    """Build capability-level graph from shared skills + metadata links."""
    del skill_library  # reserved for transfer-family edges later
    caps = capability_library.list_capabilities()
    g = CapabilityGraph()
    g.link_shared_skills(caps)
    for cap in caps:
        meta = cap.metadata or {}
        for other in meta.get("composed_with") or []:
            g.link(cap.capability_id, str(other), "composition")
        for other in meta.get("transfer_links") or []:
            g.link(cap.capability_id, str(other), "transfer")
    return IntelligenceGraph(graph=g)


def out_degree(graph: IntelligenceGraph, capability_id: str) -> int:
    return len(graph.graph.neighbors(capability_id))


def degree_centrality(graph: IntelligenceGraph) -> dict[str, float]:
    """Simple degree / (n−1) centrality over capability nodes."""
    nodes = set(graph.graph.edges.keys())
    # Include destinations that may only appear as neighbors.
    for rels in graph.graph.edges.values():
        for dsts in rels.values():
            nodes |= set(dsts)
    n = len(nodes)
    if n <= 1:
        return {nid: 0.0 for nid in nodes}
    denom = float(n - 1)
    return {nid: out_degree(graph, nid) / denom for nid in nodes}
