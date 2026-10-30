"""Capability coverage CCov (Phase 11E-1)."""

from __future__ import annotations

from typing import Sequence

from capability.config import CapabilityConfig
from capability.models import Capability
from skills.library import SkillLibrary


def _families_from_skill(skill) -> set[str]:
    out: set[str] = set()
    for event in list(skill.transfer_history or []):
        fam = str(event.get("target_family") or event.get("family") or "").strip()
        if fam:
            out.add(fam.lower())
    meta = skill.metadata or {}
    cat = str(meta.get("mvp_category") or "").strip()
    if cat and cat != "general":
        out.add(f"cat:{cat.lower()}")
    for t in skill.trigger_conditions or []:
        token = str(t).strip().lower()
        if token and ":" not in token:
            out.add(f"trig:{token}")
    return out


def supported_families(
    capability: Capability, library: SkillLibrary
) -> set[str]:
    families: set[str] = set()
    for sid in capability.skill_ids:
        skill = library.get(sid)
        if skill is not None:
            families |= _families_from_skill(skill)
    return families


def compute_coverage(
    capability: Capability,
    *,
    library: SkillLibrary,
    total_families: int | None = None,
    config: CapabilityConfig | None = None,
) -> float:
    """CCov = |supported_families| / max(total_families, ccov_family_norm)."""
    config = config or CapabilityConfig()
    families = supported_families(capability, library)
    denom = max(
        int(total_families) if total_families is not None else 0,
        int(config.ccov_family_norm),
        1,
    )
    if total_families is None and families:
        denom = max(denom, len(families))
    value = float(len(families)) / float(denom)
    capability.coverage = max(0.0, min(1.0, value))
    return capability.coverage
