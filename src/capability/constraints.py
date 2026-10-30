"""Capability validity constraints (Phase 11E-1)."""

from __future__ import annotations

from dataclasses import dataclass, field

from capability.config import CapabilityConfig
from capability.evidence import transfer_event_count
from capability.models import Capability
from capability.utility import compute_capability_utility
from skills.library import SkillLibrary


@dataclass(slots=True)
class ConstraintResult:
    valid: bool
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"valid": self.valid, "reasons": list(self.reasons)}


def validate_capability(
    capability: Capability,
    library: SkillLibrary,
    config: CapabilityConfig | None = None,
) -> ConstraintResult:
    """Require ≥1 skill, transfer evidence, CapU floor, supporting evidence."""
    config = config or CapabilityConfig()
    reasons: list[str] = []

    if len(capability.skill_ids) < int(config.min_skills):
        reasons.append("min_skills")

    present = [sid for sid in capability.skill_ids if library.get(sid) is not None]
    if capability.skill_ids and len(present) < len(capability.skill_ids):
        reasons.append("missing_skills")

    transfers = transfer_event_count(capability, library)
    if transfers < int(config.min_transfer_events):
        reasons.append("transfer")

    breakdown = compute_capability_utility(
        capability, library, config, record_history=False
    )
    if breakdown.capu < float(config.min_utility):
        reasons.append("utility")

    evidence = capability.evidence or {}
    has_evidence = bool(
        evidence.get("skills")
        or evidence.get("transfer")
        or evidence.get("utility")
        or present
    )
    if not has_evidence:
        reasons.append("evidence")

    return ConstraintResult(valid=not reasons, reasons=reasons)
