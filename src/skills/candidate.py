"""Stage 2 — SkillCandidate factory from promotable invariants (11D-1)."""

from __future__ import annotations

from typing import Sequence

from core.invariant import Invariant
from core.skill import SkillCandidate
from skills.config import SkillConfig
from skills.intake import intake_invariant

_CATEGORY_HINTS: dict[str, tuple[str, ...]] = {
    "reflection": ("reflect", "reflection", "symmetry"),
    "rotation": ("rotate", "rotation"),
    "counting": ("count", "counting"),
    "grouping": ("group", "grouping", "cluster"),
}


def classify_mvp_category(signature: Sequence[str]) -> str:
    """Tag MVP skill category from pattern signature heuristics."""
    lowered = " ".join(str(s).lower() for s in signature)
    for category, tokens in _CATEGORY_HINTS.items():
        if any(tok in lowered for tok in tokens):
            return category
    return "general"


def _estimate_reuse(inv: Invariant) -> float:
    meta = inv.metadata or {}
    if "expected_reuse" in meta:
        return float(meta["expected_reuse"])
    # Normalize frequency lightly into expected reuse scale.
    return min(1.0, max(0.0, float(inv.frequency) / 10.0))


def _estimate_transfer(inv: Invariant, *, allow_prior: bool = False) -> float:
    """Measured transfer contribution.

    ``metadata["prior_transfer"]`` is excluded by default: a prior is evidence
    *about whether to trial the skill*, not a measured transfer score. Letting it
    through here would carry it into CapU's TS term and IG, double-counting one
    trace statistic as generality, transfer, TV and TS.

    ``allow_prior`` is used only when building a provisional trial candidate,
    where the prior is needed to price the experiment. Provisional skills are
    excluded from capability scoring until Phase D measures them.
    """
    meta = inv.metadata or {}
    if "expected_transfer" in meta:
        return float(meta["expected_transfer"])
    validation = meta.get("validation") or {}
    if inv.transfer_contribution > 0:
        return float(inv.transfer_contribution)
    measured = float(validation.get("transfer", 0.0) or 0.0)
    if measured > 0 or not allow_prior:
        return measured
    return float(meta.get("prior_transfer", 0.0) or 0.0)


def _estimate_ag(inv: Invariant) -> float:
    """Abstraction gain from measured values, falling back to the SCT prior.

    The prior is explicitly named ``prior_reasoning_value`` so the fallback is
    visible at the call site rather than hidden behind a generic key.
    """
    meta = inv.metadata or {}
    if "abstraction_gain" in meta:
        return float(meta["abstraction_gain"])
    if "reasoning_value" in meta:
        return float(meta["reasoning_value"])
    if "prior_reasoning_value" in meta:
        return float(meta["prior_reasoning_value"])
    validation = meta.get("validation") or {}
    return float(validation.get("reasoning_value", 0.0) or 0.0)


def from_invariant(
    invariant: Invariant,
    *,
    config: SkillConfig | None = None,
    candidate_id: str | None = None,
    allow_prior_transfer: bool = False,
) -> SkillCandidate:
    """Build a SkillCandidate under evaluation from a promotable invariant."""
    config = config or SkillConfig()
    meta = dict(invariant.metadata or {})
    creation_cost = float(
        meta.get("creation_cost", config.default_creation_cost)
    )
    category = classify_mvp_category(invariant.pattern_signature)
    reuse = _estimate_reuse(invariant)
    transfer = _estimate_transfer(invariant, allow_prior=allow_prior_transfer)
    ag = _estimate_ag(invariant)
    cid = candidate_id or f"SC-{invariant.invariant_id}"

    return SkillCandidate(
        candidate_id=cid,
        source_invariant_id=invariant.invariant_id,
        concept_id=str(meta.get("concept_id", category)),
        trigger_conditions=list(invariant.pattern_signature),
        execution_policy=str(meta.get("execution_policy", f"apply_{category}")),
        expected_reuse=reuse,
        expected_transfer=transfer,
        abstraction_gain=ag,
        transfer_score=transfer,
        creation_cost=creation_cost,
        reuse=reuse,
        metadata={
            **meta,
            "status": "under_evaluation",
            "mvp_category": category,
            "pattern_signature": list(invariant.pattern_signature),
            "frequency": invariant.frequency,
            "consistency": invariant.consistency,
            "generality": invariant.generality,
        },
    )


def generate_candidates(
    invariants: Sequence[Invariant],
    config: SkillConfig | None = None,
) -> list[SkillCandidate]:
    """Intake-filter then map invariants to skill candidates."""
    config = config or SkillConfig()
    out: list[SkillCandidate] = []
    for inv in invariants:
        if not intake_invariant(inv, config).accepted:
            continue
        out.append(from_invariant(inv, config=config))
    return out
