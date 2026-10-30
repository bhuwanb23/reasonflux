"""Capability representation failure detectors (Phase 11E-1)."""

from __future__ import annotations

from dataclasses import dataclass, field

from capability.config import CapabilityConfig
from capability.evidence import transfer_event_count
from capability.library import CapabilityLibrary
from capability.models import Capability
from capability.states import CapabilityLifecycle
from skills.library import SkillLibrary


@dataclass(slots=True)
class RepresentationFailure:
    kind: str  # fragmentation | monolith | overlap | ghost
    reasons: list[str] = field(default_factory=list)
    metrics: dict[str, float] = field(default_factory=dict)
    capability_ids: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "kind": self.kind,
            "reasons": list(self.reasons),
            "metrics": dict(self.metrics),
            "capability_ids": list(self.capability_ids),
        }


def detect_fragmentation(
    capability_library: CapabilityLibrary,
    config: CapabilityConfig | None = None,
) -> RepresentationFailure | None:
    """Too many tiny capabilities."""
    config = config or CapabilityConfig()
    caps = [
        c
        for c in capability_library.list_capabilities()
        if c.state is not CapabilityLifecycle.ARCHIVED
    ]
    tiny = [c for c in caps if len(c.skill_ids) <= 1]
    if len(caps) > int(config.max_capabilities) or (
        len(caps) >= 5 and len(tiny) / max(1, len(caps)) >= 0.8
    ):
        return RepresentationFailure(
            "fragmentation",
            ["too_many_tiny"],
            {"count": float(len(caps)), "tiny": float(len(tiny))},
            [c.capability_id for c in tiny],
        )
    return None


def detect_monolith(
    capability_library: CapabilityLibrary,
    skill_library: SkillLibrary,
    config: CapabilityConfig | None = None,
) -> RepresentationFailure | None:
    """One capability owns most of the skill library."""
    config = config or CapabilityConfig()
    n_skills = len(skill_library)
    if n_skills <= 0:
        return None
    for cap in capability_library.list_capabilities():
        if cap.state is CapabilityLifecycle.ARCHIVED:
            continue
        fraction = len(cap.skill_ids) / float(n_skills)
        if fraction >= float(config.monolith_skill_fraction) and len(cap.skill_ids) >= 3:
            return RepresentationFailure(
                "monolith",
                ["skill_fraction"],
                {"fraction": fraction},
                [cap.capability_id],
            )
    return None


def detect_overlap(
    capability_library: CapabilityLibrary,
    config: CapabilityConfig | None = None,
) -> list[RepresentationFailure]:
    """Multiple capabilities representing nearly the same skill set."""
    config = config or CapabilityConfig()
    caps = [
        c
        for c in capability_library.list_capabilities()
        if c.state is not CapabilityLifecycle.ARCHIVED and c.skill_ids
    ]
    failures: list[RepresentationFailure] = []
    for i, a in enumerate(caps):
        set_a = set(a.skill_ids)
        for b in caps[i + 1 :]:
            set_b = set(b.skill_ids)
            union = set_a | set_b
            if not union:
                continue
            jaccard = len(set_a & set_b) / len(union)
            if jaccard >= float(config.overlap_similarity):
                failures.append(
                    RepresentationFailure(
                        "overlap",
                        ["high_jaccard"],
                        {"jaccard": jaccard},
                        [a.capability_id, b.capability_id],
                    )
                )
    return failures


def detect_ghost(
    capability: Capability,
    skill_library: SkillLibrary | None = None,
) -> RepresentationFailure | None:
    """Capability claim without transfer support."""
    transfers = transfer_event_count(capability)
    if skill_library is not None:
        for sid in capability.skill_ids:
            skill = skill_library.get(sid)
            if skill is not None:
                transfers += len(skill.transfer_history or [])
    if transfers == 0 and (
        float(capability.utility or 0.0) > 0
        or float(capability.confidence or 0.0) > 0
        or capability.state
        in (CapabilityLifecycle.ESTABLISHED, CapabilityLifecycle.CORE)
    ):
        return RepresentationFailure(
            "ghost",
            ["no_transfer"],
            {"utility": float(capability.utility or 0.0)},
            [capability.capability_id],
        )
    if transfers == 0:
        return RepresentationFailure(
            "ghost",
            ["no_transfer"],
            {},
            [capability.capability_id],
        )
    return None


def audit_representation(
    capability_library: CapabilityLibrary,
    skill_library: SkillLibrary,
    config: CapabilityConfig | None = None,
) -> list[RepresentationFailure]:
    """Run all representation failure detectors."""
    config = config or CapabilityConfig()
    out: list[RepresentationFailure] = []
    frag = detect_fragmentation(capability_library, config)
    if frag:
        out.append(frag)
    mono = detect_monolith(capability_library, skill_library, config)
    if mono:
        out.append(mono)
    out.extend(detect_overlap(capability_library, config))
    for cap in capability_library.list_capabilities():
        ghost = detect_ghost(cap, skill_library)
        if ghost:
            out.append(ghost)
    return out
