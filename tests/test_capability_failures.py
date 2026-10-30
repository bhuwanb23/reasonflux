"""Representation failure detectors."""

from capability import (
    Capability,
    CapabilityConfig,
    CapabilityLibrary,
    detect_fragmentation,
    detect_ghost,
    detect_monolith,
    detect_overlap,
)
from core import Skill, SkillState
from skills import SkillLibrary


def test_fragmentation_monolith_overlap_ghost():
    skills = SkillLibrary()
    for i in range(5):
        skills.add(Skill(skill_id=f"s{i}", state=SkillState.ACTIVE))

    caps = CapabilityLibrary()
    # Many tiny capabilities → fragmentation
    for i in range(5):
        caps.add(Capability(capability_id=f"tiny-{i}", skill_ids=[f"s{i}"]))
    frag = detect_fragmentation(caps, CapabilityConfig(max_capabilities=30))
    assert frag is not None
    assert frag.kind == "fragmentation"

    # Monolith: one cap owns ≥80% of skills with ≥3 members
    mono_lib = CapabilityLibrary()
    mono_lib.add(Capability(capability_id="mono", skill_ids=["s0", "s1", "s2", "s3"]))
    mono = detect_monolith(mono_lib, skills, CapabilityConfig(monolith_skill_fraction=0.8))
    assert mono is not None
    assert mono.kind == "monolith"

    # Overlap
    olib = CapabilityLibrary()
    olib.add(Capability(capability_id="a", skill_ids=["s0", "s1", "s2"]))
    olib.add(Capability(capability_id="b", skill_ids=["s0", "s1", "s2"]))
    overlaps = detect_overlap(olib, CapabilityConfig(overlap_similarity=0.85))
    assert overlaps and overlaps[0].kind == "overlap"

    ghost = detect_ghost(Capability(capability_id="g", skill_ids=["s0"], utility=0.5), skills)
    assert ghost is not None
    assert ghost.kind == "ghost"
