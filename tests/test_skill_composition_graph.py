"""Composition graph records successful edges."""

from skills.composition.graph import CompositionGraph


def test_record_success_edges():
    g = CompositionGraph()
    g.record_success(["reflect", "count", "group"])
    assert "count" in g.neighbors("reflect")
    assert "group" in g.neighbors("count")
    assert g.edge_count() == 2
    assert g.success_counts["reflect->count"] == 1
    restored = CompositionGraph.from_dict(g.to_dict())
    assert restored.neighbors("reflect") == {"count"}
