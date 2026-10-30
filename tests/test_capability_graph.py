"""CapabilityGraph shared-skill edges."""

from capability import Capability, CapabilityGraph


def test_shared_skill_edges():
    caps = [
        Capability(capability_id="a", skill_ids=["s1", "s2"]),
        Capability(capability_id="b", skill_ids=["s2", "s3"]),
        Capability(capability_id="c", skill_ids=["s4"]),
    ]
    g = CapabilityGraph()
    added = g.link_shared_skills(caps)
    assert added == 1
    assert "b" in g.neighbors("a", "shared_skill")
    assert "a" not in g.neighbors("c")
    g.link("a", "c", "transfer")
    assert "c" in g.neighbors("a", "transfer")
    restored = CapabilityGraph.from_dict(g.to_dict())
    assert restored.neighbors("a", "shared_skill") == g.neighbors("a", "shared_skill")
