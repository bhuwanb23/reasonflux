"""Capability strength and confidence (Phase 11E-1)."""

from __future__ import annotations

from capability.config import CapabilityConfig
from capability.evidence import transfer_event_count
from capability.models import Capability
from skills.library import SkillLibrary


def _clamp01(value: float) -> float:
    return max(0.0, min(1.0, float(value)))


def compute_strength(
    capability: Capability,
    library: SkillLibrary,
    config: CapabilityConfig | None = None,
) -> float:
    """Strength = maturity from skill count, reuse, transfer, CapU stability."""
    config = config or CapabilityConfig()
    n = len(capability.skill_ids)
    skill_n = _clamp01(n / max(config.skill_count_norm, 1e-9))
    reuse = 0
    ts_vals: list[float] = []
    for sid in capability.skill_ids:
        skill = library.get(sid)
        if skill is None:
            continue
        reuse += int(skill.reuse_count or 0)
        ts_vals.append(float(skill.transfer_score or 0.0))
    reuse_n = _clamp01(reuse / max(config.strength_reuse_norm, 1e-9))
    mean_ts = sum(ts_vals) / len(ts_vals) if ts_vals else 0.0
    hist = [float(h.get("utility", 0.0)) for h in (capability.utility_history or [])]
    if len(hist) >= 2:
        mean_u = sum(hist) / len(hist)
        var = sum((x - mean_u) ** 2 for x in hist) / len(hist)
        stability = _clamp01(1.0 - var)
    else:
        stability = 0.5
    value = _clamp01(
        0.25 * skill_n + 0.25 * reuse_n + 0.25 * mean_ts + 0.25 * stability
    )
    capability.strength = value
    return value


def compute_confidence(
    capability: Capability,
    library: SkillLibrary,
    config: CapabilityConfig | None = None,
) -> float:
    """Confidence from evidence / transfer / consistency — independent of CapU."""
    del config
    evidence = capability.evidence or {}
    skill_ev = list(evidence.get("skills") or [])
    transfer_events = transfer_event_count(capability, library)
    evidence_score = _clamp01(len(skill_ev) / max(1, len(capability.skill_ids) or 1))
    transfer_norm = _clamp01(transfer_events / 5.0)
    # Consistency: fraction of members with positive transfer_score.
    ok = 0
    total = 0
    for sid in capability.skill_ids:
        skill = library.get(sid)
        if skill is None:
            continue
        total += 1
        if float(skill.transfer_score or 0.0) > 0:
            ok += 1
    consistency = (ok / total) if total else 0.0
    value = _clamp01(
        0.4 * evidence_score + 0.3 * transfer_norm + 0.3 * consistency
    )
    capability.confidence = value
    return value


def refresh_capability_scores(
    capability: Capability,
    library: SkillLibrary,
    config: CapabilityConfig | None = None,
) -> tuple[float, float]:
    """Update strength and confidence; return (strength, confidence)."""
    return (
        compute_strength(capability, library, config),
        compute_confidence(capability, library, config),
    )
