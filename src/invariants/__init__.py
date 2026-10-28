"""Invariant Discovery Theory (IDT) — specification, mining, ranking.

Phase 11C-1 defines what qualifies as an invariant.
Phase 11C-2 mines candidate invariants from reasoning traces.
Phase 11C-3 ranks and validates candidates for SCT handoff.
"""

from core.invariant import Invariant, InvariantConfidence, InvariantEvidence, InvariantType
from invariants.candidate_generation import CandidateGenerationResult, generate_candidates
from invariants.detector import (
    InvariantDetector,
    MiningResult,
    MiningStatistics,
    TraceMiner,
)
from invariants.pattern_mining import (
    AggregatedStructure,
    MiningConfig,
    MinedPattern,
    aggregate_patterns,
    extract_patterns,
    longest_common_contiguous_subsequence,
    mine_patterns,
    patterns_share_core,
)
from invariants.promotion import advance_to_promotable, apply_promotion, meets_promotion_criteria
from invariants.ranking import RankedInvariant, compute_validation_scores, rank_invariants
from invariants.specification import (
    MVP_INVARIANT_TYPES,
    HierarchyLevel,
    InvariantHierarchy,
    InvariantIdentity,
    InvariantPolicy,
    QualificationRule,
    QualificationViolation,
    RejectionCriterion,
    RejectionReason,
    apply_rejection_criteria,
    can_become_skill_candidate,
    classify_invariant_type,
    compute_confidence,
    confidence_from_evidence,
    hierarchy_level_for,
    qualify_invariant,
    require_qualification,
    summarize_specification,
)
from invariants.strength import (
    MINIMUM_INVARIANT_STRENGTH,
    compute_invariant_strength,
    is_above_threshold,
)
from invariants.validation import ValidationConfig, ValidationScores
from invariants.validator import ValidationResult, ValidationStatistics, validate_and_rank

__all__ = [
    "AggregatedStructure",
    "CandidateGenerationResult",
    "HierarchyLevel",
    "Invariant",
    "InvariantConfidence",
    "InvariantDetector",
    "InvariantEvidence",
    "InvariantHierarchy",
    "InvariantIdentity",
    "InvariantPolicy",
    "InvariantType",
    "MVP_INVARIANT_TYPES",
    "MINIMUM_INVARIANT_STRENGTH",
    "MinedPattern",
    "MiningConfig",
    "MiningResult",
    "MiningStatistics",
    "QualificationRule",
    "QualificationViolation",
    "RankedInvariant",
    "RejectionCriterion",
    "RejectionReason",
    "TraceMiner",
    "ValidationConfig",
    "ValidationResult",
    "ValidationScores",
    "ValidationStatistics",
    "advance_to_promotable",
    "aggregate_patterns",
    "apply_promotion",
    "apply_rejection_criteria",
    "can_become_skill_candidate",
    "classify_invariant_type",
    "compute_confidence",
    "compute_invariant_strength",
    "compute_validation_scores",
    "confidence_from_evidence",
    "extract_patterns",
    "generate_candidates",
    "hierarchy_level_for",
    "is_above_threshold",
    "longest_common_contiguous_subsequence",
    "meets_promotion_criteria",
    "mine_patterns",
    "patterns_share_core",
    "qualify_invariant",
    "rank_invariants",
    "require_qualification",
    "summarize_specification",
    "validate_and_rank",
]
