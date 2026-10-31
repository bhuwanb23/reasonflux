"""Trace clustering for invariant discovery (IDT).

Greedy agglomeration: traces are grouped when their mean similarity to a
cluster's members clears ``threshold``. Clustering is a *pre-mining* aid — it
narrows a large corpus into coherent families before pattern extraction, and is
never used to decide promotion.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Sequence

from core.trace import ReasoningTrace
from traces.trace_similarity import trace_similarity

__all__ = ["TraceCluster", "cluster_traces"]


@dataclass(slots=True)
class TraceCluster:
    """A group of similar traces."""

    cluster_id: str
    traces: list[ReasoningTrace] = field(default_factory=list)
    cohesion: float = 0.0

    @property
    def size(self) -> int:
        return len(self.traces)

    @property
    def families(self) -> list[str]:
        return sorted(
            {
                str((t.metadata or {}).get("task_family") or t.task_id)
                for t in self.traces
            }
        )

    def to_dict(self) -> dict:
        return {
            "cluster_id": self.cluster_id,
            "trace_ids": [t.trace_id for t in self.traces],
            "families": self.families,
            "size": self.size,
            "cohesion": self.cohesion,
        }


def _mean_similarity(trace: ReasoningTrace, members: Sequence[ReasoningTrace]) -> float:
    if not members:
        return 1.0
    return sum(trace_similarity(trace, m) for m in members) / len(members)


def cluster_traces(
    traces: Sequence[ReasoningTrace],
    *,
    threshold: float = 0.6,
) -> list[TraceCluster]:
    """Group traces whose mean pairwise similarity is at least ``threshold``."""
    if not 0.0 <= float(threshold) <= 1.0:
        raise ValueError("threshold must be in [0, 1]")

    clusters: list[TraceCluster] = []
    # Seed in stable order so results are reproducible.
    for trace in sorted(traces, key=lambda t: t.trace_id):
        placed = False
        for cluster in clusters:
            if _mean_similarity(trace, cluster.traces) >= threshold:
                cluster.traces.append(trace)
                placed = True
                break
        if not placed:
            clusters.append(
                TraceCluster(cluster_id=f"C{len(clusters) + 1}", traces=[trace])
            )

    for cluster in clusters:
        cluster.cohesion = _cohesion(cluster.traces)
    clusters.sort(key=lambda c: (-c.size, c.cluster_id))
    return clusters


def _cohesion(members: Sequence[ReasoningTrace]) -> float:
    if len(members) < 2:
        return 1.0
    total = 0.0
    pairs = 0
    for i, a in enumerate(members):
        for b in members[i + 1 :]:
            total += trace_similarity(a, b)
            pairs += 1
    return round(total / pairs, 6) if pairs else 1.0
