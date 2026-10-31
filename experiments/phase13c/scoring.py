"""Phase-13C-only SCV10 mapping and shared non-SCV eligibility gate."""
from __future__ import annotations

from dataclasses import replace
from typing import Any
from core.invariant import Invariant
from core.skill import SkillCandidate
from skills.candidate import from_invariant
from skills.config import SkillConfig
from skills.library import SkillLibrary
from skills.promotion import promote_skill
from skills.qualification import qualify_candidate
from .common import clip01


def _candidate_score(inv: Invariant, config: SkillConfig) -> tuple[SkillCandidate, dict[str, Any]]:
    candidate = from_invariant(
        inv, config=config, allow_prior_transfer=True
    )
    raw_reuse = float(candidate.reuse if candidate.reuse != 0 else candidate.expected_reuse)
    raw_ag = float(candidate.abstraction_gain)
    raw_ts = float(
        candidate.transfer_score
        if candidate.transfer_score != 0
        else candidate.expected_transfer
    )
    p_reuse = clip01(raw_reuse)
    ag = clip01(raw_ag)
    ts = clip01(raw_ts)
    cc = max(0.0, float(candidate.creation_cost))
    mc = float(config.base_maintenance) + 0.01
    horizon = 10
    score = horizon * p_reuse * ag * ts - cc - horizon * mc
    meta = inv.metadata or {}
    validation = meta.get("validation") or {}
    reuse_source = "metadata.expected_reuse" if "expected_reuse" in meta else "frequency/10_mapping"
    ag_source = next((key for key in ("abstraction_gain", "reasoning_value", "prior_reasoning_value") if key in meta),
                     "validation.reasoning_value" if "reasoning_value" in validation else "default_zero")
    if "expected_transfer" in meta:
        ts_source = "metadata.expected_transfer"
    elif inv.transfer_contribution > 0:
        ts_source = "invariant.transfer_contribution"
    elif float(validation.get("transfer", 0.0) or 0.0) > 0:
        ts_source = "validation.transfer"
    elif "prior_transfer" in meta:
        ts_source = "metadata.prior_transfer"
    else:
        ts_source = "default_zero"
    details = {
        "p_reuse_raw": raw_reuse,
        "p_reuse": p_reuse,
        "p_reuse_source": reuse_source,
        "AG_raw": raw_ag,
        "AG": ag,
        "AG_source": ag_source,
        "TS_raw": raw_ts,
        "TS": ts,
        "TS_source": ts_source,
        "CC": cc,
        "CC_source": "metadata.creation_cost" if "creation_cost" in meta else "SkillConfig.default_creation_cost",
        "MC": mc,
        "MC_source": "base_maintenance_plus_storage_weight",
        "horizon": horizon,
        "SCV10": score,
        "creates_at_primary_threshold": score > 0.0,
    }
    candidate.scv = score
    return candidate, details


def _gate_config(config: SkillConfig) -> SkillConfig:
    """Bypass only the legacy SCV inequality after applying SCV10 ourselves."""
    return replace(config, skill_creation_threshold=-1.0e9)


def _eligible_pool(
    promotable: list[Invariant], config: SkillConfig
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    """Apply the common non-SCV qualification gate, retaining failed reasons."""
    gate_cfg = _gate_config(config)
    library = SkillLibrary()
    eligible: list[dict[str, Any]] = []
    rejected: list[dict[str, Any]] = []
    for inv in sorted(promotable, key=lambda item: item.invariant_id):
        candidate, score = _candidate_score(inv, config)
        qualification = qualify_candidate(
            candidate,
            invariant=inv,
            library=library,
            config=gate_cfg,
            allow_prior_evidence=True,
        )
        if not qualification.qualified:
            rejected.append(
                {
                    "invariant_id": inv.invariant_id,
                    "signature": list(inv.pattern_signature),
                    "reasons": list(qualification.reasons),
                    "SCV10": score["SCV10"],
                }
            )
            continue
        promoted = promote_skill(
            candidate,
            invariant=inv,
            library=library,
            config=gate_cfg,
            allow_prior_evidence=True,
        )
        if not promoted.promoted or promoted.skill is None:
            rejected.append(
                {
                    "invariant_id": inv.invariant_id,
                    "signature": list(inv.pattern_signature),
                    "reasons": list(promoted.reasons or ["promotion_rejected"]),
                    "SCV10": score["SCV10"],
                }
            )
            continue
        eligible.append(
            {
                "invariant": inv,
                "candidate": from_invariant(inv, config=config, allow_prior_transfer=True),
                "score": score,
                "source_skill_state": promoted.skill.state.value,
                "source_provisional": bool((promoted.skill.metadata or {}).get("provisional")),
                "birth_record": promoted.birth.to_dict() if promoted.birth else None,
            }
        )
    return eligible, rejected
