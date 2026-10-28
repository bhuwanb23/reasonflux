"""Invariant specification package (Phase 11C-1) — stable public API."""

from core.invariant import (
    MVP_INVARIANT_TYPES,
    Invariant,
    InvariantConfidence,
    InvariantEvidence,
    InvariantType,
)
from invariants.specification.confidence import (
    compute_confidence,
    confidence_from_evidence,
)
from invariants.specification.hierarchy import (
    HierarchyLevel,
    HierarchyNode,
    InvariantHierarchy,
    hierarchy_level_for,
    summarize_specification,
)
from invariants.specification.identity import (
    InvariantIdentity,
    can_become_skill_candidate,
)
from invariants.specification.policy import SPECIFICATION, InvariantPolicy
from invariants.specification.qualification import (
    QualificationRule,
    QualificationViolation,
    qualify_invariant,
    require_qualification,
)
from invariants.specification.rejection import (
    RejectionCriterion,
    RejectionReason,
    apply_rejection_criteria,
)
from invariants.specification.taxonomy import classify_invariant_type

__all__ = [
    "MVP_INVARIANT_TYPES",
    "Invariant",
    "InvariantConfidence",
    "InvariantEvidence",
    "InvariantType",
    "HierarchyLevel",
    "HierarchyNode",
    "InvariantHierarchy",
    "InvariantIdentity",
    "InvariantPolicy",
    "QualificationRule",
    "QualificationViolation",
    "RejectionCriterion",
    "RejectionReason",
    "SPECIFICATION",
    "apply_rejection_criteria",
    "classify_invariant_type",
    "compute_confidence",
    "confidence_from_evidence",
    "can_become_skill_candidate",
    "hierarchy_level_for",
    "qualify_invariant",
    "require_qualification",
    "summarize_specification",
]
