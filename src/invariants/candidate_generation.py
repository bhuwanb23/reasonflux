"""Candidate generation — structures → invariant candidates (Phase 11C-2 Stage 6).

Candidates move to Phase 11C-3 for validation/ranking. Transfer evidence is
left at zero here; transfer verification belongs downstream.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from core.invariant import Invariant, InvariantEvidence
from core.states import InvariantState
from invariants.pattern_mining import AggregatedStructure
from invariants.specification import (
    InvariantIdentity,
    InvariantPolicy,
    apply_rejection_criteria,
    classify_invariant_type,
    confidence_from_evidence,
)

__all__ = [
    "CandidateGenerationResult",
    "generate_candidates",
]


@dataclass(slots=True)
class CandidateGenerationResult:
    """Accepted candidates plus rejected (invariant, reasons) pairs."""

    candidates: list[Invariant] = field(default_factory=list)
    rejected: list[tuple[Invariant, list[str]]] = field(default_factory=list)


def generate_candidates(
    structures: list[AggregatedStructure],
    *,
    total_families: int,
    policy: InvariantPolicy | None = None,
    apply_rejections: bool = True,
) -> CandidateGenerationResult:
    """Map aggregated structures to ``Invariant`` objects in CANDIDATE state."""
    policy = policy or InvariantPolicy()
    if total_families < 1:
        total_families = 1

    accepted: list[Invariant] = []
    rejected: list[tuple[Invariant, list[str]]] = []

    for structure in structures:
        inv = _structure_to_invariant(structure, total_families=total_families)
        if apply_rejections:
            reasons = apply_rejection_criteria(inv, policy)
            if reasons:
                rejected.append((inv, reasons))
                continue
        accepted.append(inv)

    return CandidateGenerationResult(candidates=accepted, rejected=rejected)


def _structure_to_invariant(
    structure: AggregatedStructure, *, total_families: int
) -> Invariant:
    representative = structure.representative
    frequency = max(structure.frequency, 1)
    consistency = min(1.0, representative.frequency / frequency)
    family_count = len(structure.task_families)
    generality = min(1.0, family_count / max(total_families, 1))

    evidence = InvariantEvidence(
        observations=structure.occurrences,
        task_families=list(structure.task_families),
        transfer_events=0,
        reuse_events=0,
    )
    inv_type = classify_invariant_type(
        list(representative.signature),
        task_family_count=max(family_count, 1),
    )
    confidence = confidence_from_evidence(evidence, consistency)
    identity = InvariantIdentity(
        origin="trace_mining",
        pattern_signature=tuple(representative.signature),
        task_families=tuple(sorted(structure.task_families)),
    )

    return Invariant(
        invariant_id=identity.invariant_id,
        pattern_signature=list(representative.signature),
        frequency=structure.frequency,
        consistency=consistency,
        generality=generality,
        associated_concepts=[],
        source_trace_ids=list(representative.trace_ids),
        state=InvariantState.CANDIDATE,
        origin="trace_mining",
        task_families=list(structure.task_families),
        invariant_type=inv_type,
        evidence=evidence,
        confidence=confidence,
        metadata={
            "structure_id": structure.structure_id,
            "pattern_id": representative.pattern_id,
            "core": list(structure.core),
            "variant_signatures": [list(v.signature) for v in structure.variants],
            "success_count": structure.success_count,
            "failure_count": structure.failure_count,
            "coverage": representative.coverage,
        },
    )
