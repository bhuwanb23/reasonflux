"""Five skill qualification tests + constraints (Phase 11D-1)."""

from __future__ import annotations

from dataclasses import dataclass, field

from core.invariant import Invariant
from core.skill import SkillCandidate
from core.states import InvariantState
from skills.config import SkillConfig
from skills.library import SkillLibrary
from skills.trigger import SkillCreationTrigger


@dataclass(slots=True)
class QualificationResult:
    """Outcome of the five qualification tests."""

    qualified: bool
    reasons: list[str] = field(default_factory=list)
    tests: dict[str, bool] = field(default_factory=dict)

    def to_dict(self) -> dict:
        return {
            "qualified": self.qualified,
            "reasons": list(self.reasons),
            "tests": dict(self.tests),
        }


def qualify_candidate(
    candidate: SkillCandidate,
    *,
    invariant: Invariant,
    library: SkillLibrary | None = None,
    config: SkillConfig | None = None,
    ntr: float = 0.0,
) -> QualificationResult:
    """Run five tests and hard constraints before promotion."""
    config = config or SkillConfig()
    if library is None:
        library = SkillLibrary()
    trigger = SkillCreationTrigger(config)
    reasons: list[str] = []
    tests: dict[str, bool] = {}

    # Constraint: originate from validated / promotable invariant.
    if invariant.state not in (
        InvariantState.SKILL_CANDIDATE,
        InvariantState.TRANSFER_VERIFIED,
        InvariantState.VALIDATED,
        InvariantState.STRONG,
    ):
        reasons.append("not_validated_origin")
        tests["origin"] = False
    else:
        tests["origin"] = True

    # Test 1 — Frequency support
    freq_ok = invariant.frequency >= config.min_frequency
    tests["frequency"] = freq_ok
    if not freq_ok:
        reasons.append("frequency")

    # Test 2 — Consistency support
    cons_ok = invariant.consistency >= config.min_consistency
    tests["consistency"] = cons_ok
    if not cons_ok:
        reasons.append("consistency")

    # Test 3 — Transfer support (ITS / transfer_score)
    ts = candidate.transfer_score or candidate.expected_transfer
    transfer_ok = ts >= config.min_its
    tests["transfer"] = transfer_ok
    if not transfer_ok:
        reasons.append("transfer")

    # Test 4 — Reasoning reduction (AG / reasoning value)
    ag = candidate.abstraction_gain
    meta = invariant.metadata or {}
    rv = float(meta.get("reasoning_value", ag) or 0.0)
    reasoning_ok = max(ag, rv) >= config.min_reasoning_value
    tests["reasoning"] = reasoning_ok
    if not reasoning_ok:
        reasons.append("reasoning")

    # Test 5 — Economic viability
    economic_ok = trigger.should_create(candidate)
    tests["economic"] = economic_ok
    if not economic_ok:
        reasons.append("scv")

    # Evidence threshold
    evidence = 0
    if invariant.evidence is not None:
        evidence = int(invariant.evidence.observations or 0)
    if evidence < config.min_evidence and invariant.frequency < config.min_evidence:
        reasons.append("evidence")
        tests["evidence"] = False
    else:
        tests["evidence"] = True

    # Negative transfer limit
    if ntr > config.ntr_limit:
        reasons.append("negative_transfer")
        tests["ntr"] = False
    else:
        tests["ntr"] = True

    # Duplicate / similarity check (Failure E)
    signature = list(
        candidate.trigger_conditions
        or (candidate.metadata or {}).get("pattern_signature")
        or []
    )
    similar = library.find_similar(signature, config.similarity_merge)
    if similar:
        reasons.append("duplicate")
        tests["unique"] = False
    else:
        tests["unique"] = True

    return QualificationResult(qualified=not reasons, reasons=reasons, tests=tests)
