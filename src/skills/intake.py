"""Stage 1 — ingest promotable invariants from IDT (Phase 11D-1)."""

from __future__ import annotations

from dataclasses import dataclass, field

from core.invariant import Invariant
from core.states import InvariantState
from skills.config import SkillConfig


@dataclass(slots=True)
class IntakeResult:
    """Outcome of Stage 1 invariant intake."""

    accepted: bool
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {"accepted": self.accepted, "reasons": list(self.reasons)}


def is_promotable_invariant(invariant: Invariant) -> bool:
    """True when the invariant is in the SCT input state."""
    return invariant.state is InvariantState.SKILL_CANDIDATE


def intake_invariant(
    invariant: Invariant, config: SkillConfig | None = None
) -> IntakeResult:
    """Re-check 11C floors before creating a skill candidate."""
    config = config or SkillConfig()
    reasons: list[str] = []

    if not is_promotable_invariant(invariant):
        reasons.append("not_skill_candidate")

    if invariant.frequency < config.min_frequency:
        reasons.append("frequency")
    if invariant.consistency < config.min_consistency:
        reasons.append("consistency")
    if invariant.generality < config.min_generality:
        reasons.append("generality")

    transfer = float(invariant.transfer_contribution or 0.0)
    meta = invariant.metadata or {}
    validation = meta.get("validation") or {}
    if transfer <= 0 and float(validation.get("transfer", 0.0) or 0.0) <= 0:
        reasons.append("transfer")

    evidence = 0
    if invariant.evidence is not None:
        evidence = int(invariant.evidence.observations or 0)
    if evidence < config.min_evidence and invariant.frequency < config.min_evidence:
        reasons.append("evidence")

    return IntakeResult(accepted=not reasons, reasons=reasons)
