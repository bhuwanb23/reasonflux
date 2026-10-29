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


def _estimate_transfer(inv: Invariant) -> float:
    meta = inv.metadata or {}
    if "expected_transfer" in meta:
        return float(meta["expected_transfer"])
    validation = meta.get("validation") or {}
    if inv.transfer_contribution > 0:
        return float(inv.transfer_contribution)
    return float(validation.get("transfer", 0.0) or 0.0)


def _estimate_ag(inv: Invariant) -> float:
    meta = inv.metadata or {}
    if "abstraction_gain" in meta:
        return float(meta["abstraction_gain"])
    if "reasoning_value" in meta:
        return float(meta["reasoning_value"])
    validation = meta.get("validation") or {}
    return float(validation.get("reasoning_value", 0.0) or 0.0)


def from_invariant(
    invariant: Invariant,
    *,
    config: SkillConfig | None = None,
    candidate_id: str | None = None,
) -> SkillCandidate:
    """Build a SkillCandidate under evaluation from a promotable invariant."""
    config = config or SkillConfig()
    meta = dict(invariant.metadata or {})
    creation_cost = float(
        meta.get("creation_cost", config.default_creation_cost)
    )
    category = classify_mvp_category(invariant.pattern_signature)
    reuse = _estimate_reuse(invariant)
    transfer = _estimate_transfer(invariant)
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
