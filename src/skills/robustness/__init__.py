"""Skill failure modes and robustness — Phase 11D-5."""

from skills.robustness.audit import LibraryAuditReport, audit_library
from skills.robustness.config import SkillRobustnessConfig
from skills.robustness.edge_cases import (
    detect_cannibalization,
    enforce_zombie_archive,
    is_ancient_core,
    rare_high_value_override,
)
from skills.robustness.gates import (
    SkillGateResult,
    confirm_skill_promotion,
    evaluate_skill_promotion_gate,
    evaluate_skill_retirement_gate,
)
from skills.robustness.metrics import (
    capability_growth_rate,
    retrieval_recall,
    skill_explosion_ratio,
    skill_ntr,
    task_family_diversity,
)
from skills.robustness.recovery import (
    RecoveryAction,
    apply_recovery,
    plan_recovery,
)
from skills.robustness.sf_capability import (
    AdversarialRisk,
    CollapseRisk,
    detect_adversarial_formation,
    detect_capability_collapse,
)
from skills.robustness.sf_composition import (
    CompositionFailureResult,
    assess_composition_failure,
)
from skills.robustness.sf_creation import (
    demote_skill,
    detect_duplicates,
    detect_premature_skill,
    enforce_library_capacity,
    merge_skills,
    ser_level,
    should_restrict_skill_promotion,
)
from skills.robustness.sf_retrieval import (
    RetrievalDiagnosis,
    boost_retrieval,
    diagnose_retrieval_failure,
)
from skills.robustness.sf_transfer import (
    TransferHealth,
    apply_transfer_health,
    assess_negative_transfer,
)
from skills.robustness.taxonomy import (
    FailureDiagnosis,
    SkillFailure,
    diagnose_skill,
)

__all__ = [
    "AdversarialRisk",
    "CollapseRisk",
    "CompositionFailureResult",
    "FailureDiagnosis",
    "LibraryAuditReport",
    "RecoveryAction",
    "RetrievalDiagnosis",
    "SkillFailure",
    "SkillGateResult",
    "SkillRobustnessConfig",
    "TransferHealth",
    "apply_recovery",
    "apply_transfer_health",
    "assess_composition_failure",
    "assess_negative_transfer",
    "audit_library",
    "boost_retrieval",
    "capability_growth_rate",
    "confirm_skill_promotion",
    "demote_skill",
    "detect_adversarial_formation",
    "detect_cannibalization",
    "detect_capability_collapse",
    "detect_duplicates",
    "detect_premature_skill",
    "diagnose_retrieval_failure",
    "diagnose_skill",
    "enforce_library_capacity",
    "enforce_zombie_archive",
    "evaluate_skill_promotion_gate",
    "evaluate_skill_retirement_gate",
    "is_ancient_core",
    "merge_skills",
    "plan_recovery",
    "rare_high_value_override",
    "retrieval_recall",
    "ser_level",
    "should_restrict_skill_promotion",
    "skill_explosion_ratio",
    "skill_ntr",
    "task_family_diversity",
]
