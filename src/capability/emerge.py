"""Propose capabilities from skill library signals (Phase 11E-1)."""

from __future__ import annotations

from collections import defaultdict
from typing import Sequence

from core.states import SkillState
from capability.config import CapabilityConfig
from capability.constraints import validate_capability
from capability.evidence import seed_from_skills
from capability.models import Capability, CapabilityType
from capability.utility import compute_capability_utility
from skills.library import SkillLibrary

ACTIVE_TIER = frozenset(
    {SkillState.ACTIVE, SkillState.GROWING, SkillState.CORE}
)


def _category(skill) -> str:
    meta = skill.metadata or {}
    cat = str(meta.get("mvp_category") or "general").strip().lower()
    return cat or "general"


def propose_capabilities_from_library(
    skill_library: SkillLibrary,
    *,
    config: CapabilityConfig | None = None,
    composition_graph=None,
    require_valid: bool = True,
) -> list[Capability]:
    """Propose atomic / composite / cross-domain / emergent capabilities.

    Does not auto-add to a CapabilityLibrary; caller validates and stores.
    """
    del composition_graph  # reserved for composition-edge emergent clustering
    config = config or CapabilityConfig()
    skills = [
        s for s in skill_library.list_skills() if s.state in ACTIVE_TIER
    ]
    proposed: list[Capability] = []
    seen: set[str] = set()

    def _add(cap: Capability) -> None:
        if cap.capability_id in seen:
            return
        seed_from_skills(cap, skill_library)
        compute_capability_utility(cap, skill_library, config)
        if require_valid and not validate_capability(cap, skill_library, config).valid:
            return
        seen.add(cap.capability_id)
        proposed.append(cap)

    # Atomic: CORE / capability_anchor skills.
    for skill in skills:
        meta = skill.metadata or {}
        if skill.state is SkillState.CORE or meta.get("capability_anchor"):
            cid = f"cap-atomic-{skill.skill_id}"
            _add(
                Capability(
                    capability_id=cid,
                    name=f"{skill.skill_id} Capability",
                    capability_type=CapabilityType.ATOMIC,
                    skill_ids=[skill.skill_id],
                )
            )

    # Composite: cluster by mvp_category (size ≥ 2).
    by_cat: dict[str, list[str]] = defaultdict(list)
    for skill in skills:
        cat = _category(skill)
        if cat != "general":
            by_cat[cat].append(skill.skill_id)
    for cat, ids in by_cat.items():
        if len(ids) < 2:
            continue
        cid = f"cap-composite-{cat}"
        _add(
            Capability(
                capability_id=cid,
                name=f"{cat.title()} Capability",
                capability_type=CapabilityType.COMPOSITE,
                skill_ids=list(ids),
            )
        )

    # Emergent: capability_candidate / composed_from skills clustered together.
    emergent_ids = [
        s.skill_id
        for s in skills
        if (s.metadata or {}).get("capability_candidate")
        or (s.metadata or {}).get("composed_from")
    ]
    if len(emergent_ids) >= 2:
        _add(
            Capability(
                capability_id="cap-emergent-composed",
                name="Emergent Composed Capability",
                capability_type=CapabilityType.EMERGENT,
                skill_ids=list(emergent_ids),
            )
        )

    # Cross-domain: ≥1 skill from ≥2 non-general categories.
    by_cat_all: dict[str, list[str]] = defaultdict(list)
    for skill in skills:
        cat = _category(skill)
        if cat != "general":
            by_cat_all[cat].append(skill.skill_id)
    if len(by_cat_all) >= 2:
        cross_ids: list[str] = []
        for cat in sorted(by_cat_all):
            if by_cat_all[cat]:
                cross_ids.append(by_cat_all[cat][0])
            if len(cross_ids) >= 6:
                break
        # Fill remaining slots from leftover members while preserving multi-cat.
        if len(cross_ids) >= 2:
            for cat in sorted(by_cat_all):
                for sid in by_cat_all[cat][1:]:
                    if sid not in cross_ids:
                        cross_ids.append(sid)
                    if len(cross_ids) >= 6:
                        break
                if len(cross_ids) >= 6:
                    break
            _add(
                Capability(
                    capability_id="cap-cross-domain",
                    name="Cross-Domain Capability",
                    capability_type=CapabilityType.CROSS_DOMAIN,
                    skill_ids=cross_ids,
                    metadata={"categories": sorted(by_cat_all)},
                )
            )

    return proposed


def accept_capabilities(
    proposals: Sequence[Capability],
    skill_library: SkillLibrary,
    config: CapabilityConfig | None = None,
) -> list[Capability]:
    """Filter proposals that pass validate_capability."""
    config = config or CapabilityConfig()
    return [
        c
        for c in proposals
        if validate_capability(c, skill_library, config).valid
    ]
