"""Composition evaluation, evidence, confidence, NCR (Phase 11D-4)."""

from __future__ import annotations

from skills.composition.models import CompositionCandidate
from skills.composition.utility import compute_cu
from skills.config import SkillConfig


def compute_composition_confidence(candidate: CompositionCandidate) -> float:
    """Confidence from success rate, transfer events, and family diversity."""
    ev = candidate.evidence or {}
    uses = int(ev.get("uses", 0) or 0)
    if uses <= 0:
        return 0.0
    successes = int(ev.get("successes", 0) or 0)
    success_rate = successes / uses
    transfers = list(ev.get("transfer_events") or [])
    transfer_score = min(1.0, len(transfers) / 3.0)
    families = {str(f) for f in (ev.get("families") or []) if str(f).strip()}
    diversity = min(1.0, len(families) / 3.0)
    return max(
        0.0,
        min(1.0, 0.5 * success_rate + 0.3 * transfer_score + 0.2 * diversity),
    )


def record_composition_outcome(
    candidate: CompositionCandidate,
    *,
    success: bool,
    transfer_gain: float = 0.0,
    reasoning_reduction: float = 0.0,
    task_family: str = "",
    config: SkillConfig | None = None,
) -> CompositionCandidate:
    """Append evidence, recompute CU / confidence / NCR fields."""
    config = config or SkillConfig()
    ev = dict(candidate.evidence or {})
    ev["uses"] = int(ev.get("uses", 0) or 0) + 1
    if success:
        ev["successes"] = int(ev.get("successes", 0) or 0) + 1
    else:
        ev["failures"] = int(ev.get("failures", 0) or 0) + 1

    families = list(ev.get("families") or [])
    if task_family and task_family not in families:
        families.append(task_family)
    ev["families"] = families

    transfers = list(ev.get("transfer_events") or [])
    if transfer_gain > 0 or task_family:
        transfers.append(
            {
                "success": success,
                "transfer_gain": float(transfer_gain),
                "family": task_family,
            }
        )
    ev["transfer_events"] = transfers

    reductions = list(ev.get("cost_reductions") or [])
    reductions.append(float(reasoning_reduction))
    ev["cost_reductions"] = reductions
    candidate.evidence = ev

    uses = int(ev["uses"])
    reuse_potential = (
        float(ev.get("successes", 0) or 0) / max(1, uses)
    ) * float(candidate.expected_utility or 0.5)
    # Blend latest gains with running means.
    mean_tg = sum(
        float(t.get("transfer_gain", 0.0)) for t in transfers
    ) / max(1, len(transfers))
    mean_rr = sum(reductions) / max(1, len(reductions))
    compute_cu(
        candidate,
        transfer_gain=mean_tg if transfers else transfer_gain,
        reasoning_reduction=mean_rr,
        reuse_potential=reuse_potential,
        config=config,
    )
    candidate.confidence = compute_composition_confidence(candidate)
    meta = dict(candidate.metadata or {})
    meta["ncr"] = candidate.ncr
    candidate.metadata = meta
    return candidate
