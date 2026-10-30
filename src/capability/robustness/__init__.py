"""Capability failure modes & robustness (Phase 11E-5)."""

from capability.robustness.audit import (
    EcosystemAuditResult,
    ScoreSnapshot,
    audit_capability_ecosystem,
)
from capability.robustness.config import CapabilityRobustnessConfig
from capability.robustness.gates import GrowthClaimResult, validate_growth_claim
from capability.robustness.health import (
    CapabilityHealth,
    HealthBand,
    PortfolioHealth,
    score_capability,
    score_portfolio,
)
from capability.robustness.recovery import RecoveryAction, apply_recovery, plan_recovery
from capability.robustness.taxonomy import CapabilityFailureKind, FailureDiagnosis

__all__ = [
    "CapabilityFailureKind",
    "CapabilityHealth",
    "CapabilityRobustnessConfig",
    "EcosystemAuditResult",
    "FailureDiagnosis",
    "GrowthClaimResult",
    "HealthBand",
    "PortfolioHealth",
    "RecoveryAction",
    "ScoreSnapshot",
    "apply_recovery",
    "audit_capability_ecosystem",
    "plan_recovery",
    "score_capability",
    "score_portfolio",
    "validate_growth_claim",
]
