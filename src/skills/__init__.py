"""Skill Creation Trigger Theory (SCT) — Phase 11D-1..11D-4."""

from skills.birth import SkillBirthRecord, make_birth_record
from skills.candidate import classify_mvp_category, from_invariant, generate_candidates
from skills.competition import rank_by_utility, select_dominant
from skills.composition import (
    CompositionCandidate,
    CompositionGraph,
    advance_composition,
    compute_cu,
    promote_composition,
    propose_sequential,
    should_compose,
    try_compose,
)
from skills.config import SkillConfig
from skills.economics import (
    EconomicsProjection,
    evaluate_promotion_economics,
    expected_future_utility,
    lifetime_cost,
)
from skills.evidence import SkillEvidence, compute_skill_confidence, seed_evidence_from_invariant
from skills.intake import IntakeResult, intake_invariant, is_promotable_invariant
from skills.library import SkillLibrary
from skills.lifecycle import (
    apply_lifecycle,
    build_biography,
    compute_health,
    compute_lifecycle_metrics,
    evaluate_library_lifecycle,
    evaluate_lifecycle,
)
from skills.monitoring import record_negative, record_reuse, record_transfer
from skills.pipeline import (
    SkillCreationResult,
    SkillCreationStatistics,
    create_skills_from_invariants,
)
from skills.portfolio import PortfolioMetrics, compute_portfolio_metrics
from skills.promotion import PromotionResult, promote_skill
from skills.qualification import QualificationResult, qualify_candidate
from skills.reactivation import ReactivationResult, reactivate_skill
from skills.retrieval import retrieve_skills
from skills.retirement import retire_skills
from skills.trigger import SkillCreationTrigger
from skills.utility import (
    classify_economic_status,
    compute_su,
    refresh_skill_utility,
    score_skill_utility,
)
from skills.utility_components import SkillUtilityBreakdown

__all__ = [
    "CompositionCandidate",
    "CompositionGraph",
    "EconomicsProjection",
    "IntakeResult",
    "PortfolioMetrics",
    "PromotionResult",
    "QualificationResult",
    "ReactivationResult",
    "SkillBirthRecord",
    "SkillConfig",
    "SkillCreationResult",
    "SkillCreationStatistics",
    "SkillCreationTrigger",
    "SkillEvidence",
    "SkillLibrary",
    "SkillUtilityBreakdown",
    "advance_composition",
    "apply_lifecycle",
    "build_biography",
    "classify_economic_status",
    "classify_mvp_category",
    "compute_cu",
    "compute_health",
    "compute_lifecycle_metrics",
    "compute_portfolio_metrics",
    "compute_skill_confidence",
    "compute_su",
    "create_skills_from_invariants",
    "evaluate_library_lifecycle",
    "evaluate_lifecycle",
    "evaluate_promotion_economics",
    "expected_future_utility",
    "from_invariant",
    "generate_candidates",
    "intake_invariant",
    "is_promotable_invariant",
    "lifetime_cost",
    "make_birth_record",
    "promote_composition",
    "promote_skill",
    "propose_sequential",
    "qualify_candidate",
    "rank_by_utility",
    "reactivate_skill",
    "record_negative",
    "record_reuse",
    "record_transfer",
    "refresh_skill_utility",
    "retire_skills",
    "retrieve_skills",
    "score_skill_utility",
    "seed_evidence_from_invariant",
    "select_dominant",
    "should_compose",
    "try_compose",
]
