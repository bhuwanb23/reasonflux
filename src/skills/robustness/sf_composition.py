"""SF6 skill composition failure (Phase 11D-5)."""

from __future__ import annotations

from dataclasses import dataclass

from skills.composition.models import CompositionCandidate, CompositionState
from skills.robustness.config import SkillRobustnessConfig


@dataclass(slots=True)
class CompositionFailureResult:
    failed: bool
    reasons: list[str]
    raised_cost: float

    def to_dict(self) -> dict:
        return {
            "failed": self.failed,
            "reasons": list(self.reasons),
            "raised_cost": self.raised_cost,
        }


def assess_composition_failure(
    candidate: CompositionCandidate,
    config: SkillRobustnessConfig | None = None,
) -> CompositionFailureResult:
    """Reject harmful compositions (CU < min or NCR high); raise future cost."""
    config = config or SkillRobustnessConfig()
    reasons: list[str] = []
    if float(candidate.cu) < float(config.cu_min_composition):
        reasons.append("low_cu")
    if float(candidate.ncr) > float(config.composition_ncr_limit):
        reasons.append("high_ncr")
    raised = float(candidate.composition_cost or 0.0)
    if reasons:
        raised = raised + 0.1
        candidate.composition_cost = raised
        meta = dict(candidate.metadata or {})
        meta["composition_failure"] = {
            "reasons": reasons,
            "cu": float(candidate.cu),
            "ncr": float(candidate.ncr),
        }
        candidate.metadata = meta
        if candidate.state not in (
            CompositionState.DISCARDED,
            CompositionState.PROMOTED,
        ):
            candidate.state = CompositionState.DISCARDED
        return CompositionFailureResult(True, reasons, raised)
    return CompositionFailureResult(False, [], raised)
