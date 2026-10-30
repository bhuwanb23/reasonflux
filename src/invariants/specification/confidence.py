"""Evidence-based confidence model (Phase 11C-1)."""

from __future__ import annotations

from core.invariant import Invariant, InvariantConfidence, InvariantEvidence
from invariants.specification.policy import InvariantPolicy


def confidence_from_evidence(
    evidence: InvariantEvidence,
    consistency: float,
    policy: InvariantPolicy | None = None,
) -> InvariantConfidence:
    """Derive a confidence category from evidence."""
    policy = policy or InvariantPolicy()
    recurrence = min(1.0, evidence.observations / max(policy.min_frequency * 3, 1))
    stability = max(0.0, min(1.0, consistency))
    breadth = min(1.0, evidence.task_family_count / max(policy.min_task_families * 2, 1))
    transfer = min(1.0, evidence.transfer_events / 3.0)
    score = (recurrence + stability + breadth + transfer) / 4.0
    return _confidence_for_score(score, policy)


def compute_confidence(
    invariant: Invariant, policy: InvariantPolicy | None = None
) -> InvariantConfidence:
    """Compute the confidence category for an invariant."""
    return confidence_from_evidence(invariant.evidence, invariant.consistency, policy)


def _confidence_for_score(score: float, policy: InvariantPolicy) -> InvariantConfidence:
    if score >= policy.strong_score:
        return InvariantConfidence.STRONG
    if score >= policy.moderate_score:
        return InvariantConfidence.MODERATE
    return InvariantConfidence.WEAK
