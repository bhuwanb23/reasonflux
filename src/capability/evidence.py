"""Capability evidence buckets (Phase 11E-1)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from capability.models import Capability
from skills.library import SkillLibrary


@dataclass(slots=True)
class CapabilityEvidence:
    skills: list[dict[str, Any]] = field(default_factory=list)
    transfer: list[dict[str, Any]] = field(default_factory=list)
    utility: list[dict[str, Any]] = field(default_factory=list)
    growth: list[dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "skills": list(self.skills),
            "transfer": list(self.transfer),
            "utility": list(self.utility),
            "growth": list(self.growth),
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any] | None) -> CapabilityEvidence:
        data = data or {}
        return cls(
            skills=list(data.get("skills") or []),
            transfer=list(data.get("transfer") or []),
            utility=list(data.get("utility") or []),
            growth=list(data.get("growth") or []),
        )


def _write(capability: Capability, evidence: CapabilityEvidence) -> None:
    capability.evidence = evidence.to_dict()


def append_skill_evidence(capability: Capability, skill_id: str, **payload: Any) -> None:
    ev = CapabilityEvidence.from_dict(capability.evidence)
    ev.skills.append({"skill_id": skill_id, **payload})
    _write(capability, ev)


def append_transfer_evidence(capability: Capability, **payload: Any) -> None:
    ev = CapabilityEvidence.from_dict(capability.evidence)
    ev.transfer.append(dict(payload))
    capability.transfer_history = list(capability.transfer_history or [])
    capability.transfer_history.append(dict(payload))
    _write(capability, ev)


def append_utility_evidence(capability: Capability, **payload: Any) -> None:
    ev = CapabilityEvidence.from_dict(capability.evidence)
    ev.utility.append(dict(payload))
    _write(capability, ev)


def append_growth_evidence(capability: Capability, **payload: Any) -> None:
    ev = CapabilityEvidence.from_dict(capability.evidence)
    ev.growth.append(dict(payload))
    capability.growth_history = list(capability.growth_history or [])
    capability.growth_history.append(dict(payload))
    _write(capability, ev)


def seed_from_skills(
    capability: Capability,
    library: SkillLibrary,
    skill_ids: Sequence[str] | None = None,
) -> CapabilityEvidence:
    """Seed evidence buckets from member skills currently in the library.

    Idempotent: skips skill/transfer rows already present for a skill_id.
    Canonical transfer list is ``evidence.transfer`` (mirrored to
    ``transfer_history`` only when appending new events).
    """
    ids = list(skill_ids) if skill_ids is not None else list(capability.skill_ids)
    ev = CapabilityEvidence.from_dict(capability.evidence)
    seeded_skills = {str(e.get("skill_id")) for e in ev.skills if e.get("skill_id")}
    for sid in ids:
        skill = library.get(sid)
        if skill is None:
            continue
        if sid not in seeded_skills:
            ev.skills.append(
                {
                    "skill_id": sid,
                    "utility": float(skill.utility or 0.0),
                    "transfer_score": float(skill.transfer_score or 0.0),
                }
            )
            seeded_skills.add(sid)
        # Only seed transfers once per skill_id.
        already = any(e.get("skill_id") == sid for e in ev.transfer)
        if already:
            continue
        for event in list(skill.transfer_history or []):
            payload = {"skill_id": sid, **dict(event)}
            ev.transfer.append(payload)
            capability.transfer_history = list(capability.transfer_history or [])
            capability.transfer_history.append(payload)
    _write(capability, ev)
    return ev


def transfer_event_count(
    capability: Capability,
    library: SkillLibrary | None = None,
) -> int:
    """Count unique transfer support for a capability.

    Prefer evidence.transfer when present; otherwise capability.transfer_history.
    Optionally union in member-skill transfers that were never seeded.
    """
    ev = CapabilityEvidence.from_dict(capability.evidence)
    if ev.transfer:
        count = len(ev.transfer)
    else:
        count = len(capability.transfer_history or [])
    if library is None:
        return count
    seeded = {str(e.get("skill_id")) for e in ev.transfer if e.get("skill_id")}
    for sid in capability.skill_ids:
        if sid in seeded:
            continue
        skill = library.get(sid)
        if skill is not None:
            count += len(skill.transfer_history or [])
    return count
