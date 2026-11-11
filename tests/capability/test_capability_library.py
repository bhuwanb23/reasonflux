"""CapabilityLibrary CRUD and find_by_skill."""

from capability import Capability, CapabilityLibrary, CapabilityLifecycle


def test_library_crud_and_find_by_skill():
    lib = CapabilityLibrary()
    a = Capability(capability_id="a", skill_ids=["s1", "s2"])
    b = Capability(capability_id="b", skill_ids=["s2", "s3"])
    lib.add(a)
    lib.add(b)
    assert lib.get("a") is a
    assert len(lib.find_by_skill("s2")) == 2
    assert lib.find_by_skill("s3")[0].capability_id == "b"
    overlaps = lib.find_overlapping(["s1", "s2"], min_jaccard=0.4)
    assert any(c.capability_id == "a" for c, _ in overlaps)
    assert lib.archive("a")
    assert a.state is CapabilityLifecycle.ARCHIVED
    assert lib.remove("b")
    assert lib.get("b") is None
