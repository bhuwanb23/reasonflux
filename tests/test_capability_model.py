"""Capability model construction, membership, round-trip."""

from capability import Capability, CapabilityLifecycle, CapabilityType


def test_construct_and_multi_membership():
    cap = Capability(
        capability_id="cap-1",
        name="Geometric",
        capability_type=CapabilityType.COMPOSITE,
        skill_ids=["reflect", "rotate"],
    )
    cap.add_skill("translate")
    cap.add_skill("reflect")  # no duplicate
    assert cap.skill_ids == ["reflect", "rotate", "translate"]
    assert cap.remove_skill("rotate")
    assert "rotate" not in cap.skill_ids


def test_dict_round_trip():
    cap = Capability(
        capability_id="cap-2",
        capability_type=CapabilityType.EMERGENT,
        skill_ids=["a", "b"],
        state=CapabilityLifecycle.DEVELOPING,
        utility=0.4,
        metadata={"k": 1},
    )
    restored = Capability.from_dict(cap.to_dict())
    assert restored.capability_type is CapabilityType.EMERGENT
    assert restored.state is CapabilityLifecycle.DEVELOPING
    assert restored.skill_ids == ["a", "b"]
    assert restored.metadata["k"] == 1
