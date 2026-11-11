"""Tests for intelligence graph building and simple metrics."""

from capability import Capability, CapabilityLibrary
from evaluation import build_intelligence_graph, degree_centrality, out_degree


def test_build_graph_and_out_degree():
    caps = CapabilityLibrary()
    a = Capability(
        capability_id="a",
        skill_ids=["s1", "s2"],
        metadata={"composed_with": ["b"]},
    )
    b = Capability(
        capability_id="b",
        skill_ids=["s2", "s3"],
        metadata={"transfer_links": ["a"]},
    )
    caps.add(a)
    caps.add(b)
    g = build_intelligence_graph(caps)
    assert out_degree(g, "a") >= 1
    assert g.edge_count() >= 1
    cents = degree_centrality(g)
    assert "a" in cents
    assert cents["a"] > 0
