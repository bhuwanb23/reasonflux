"""Composition lifecycle advance and promotion to Skill (Phase 11D-4)."""

from __future__ import annotations

from core.skill import Skill
from core.states import SkillState
from skills.composition.models import CompositionCandidate, CompositionState
from skills.config import SkillConfig
from skills.library import SkillLibrary
from skills.utility import refresh_skill_utility


def advance_composition(
    candidate: CompositionCandidate,
    config: SkillConfig | None = None,
) -> CompositionCandidate:
    """Advance candidate → validated → reusable, or discard on failure gates."""
    config = config or SkillConfig()
    if candidate.state in (CompositionState.DISCARDED, CompositionState.PROMOTED):
        return candidate

    ev = candidate.evidence or {}
    uses = int(ev.get("uses", 0) or 0)
    successes = int(ev.get("successes", 0) or 0)
    ncr = candidate.ncr

    if uses > 0 and (
        candidate.cu < config.cu_min or ncr > config.compose_ncr_limit
    ):
        # Only discard after evidence exists and economics fail.
        if successes == 0 or ncr > config.compose_ncr_limit:
            candidate.state = CompositionState.DISCARDED
            meta = dict(candidate.metadata or {})
            meta["discard_reason"] = (
                "high_ncr" if ncr > config.compose_ncr_limit else "low_cu"
            )
            candidate.metadata = meta
            return candidate

    if candidate.state is CompositionState.CANDIDATE:
        if (
            successes >= int(config.compose_min_successes_validate)
            and candidate.cu >= config.cu_min
        ):
            candidate.state = CompositionState.VALIDATED

    if candidate.state is CompositionState.VALIDATED:
        # Single use must not become reusable / stored.
        if (
            uses >= int(config.compose_min_reuse_store)
            and candidate.confidence >= float(config.compose_min_confidence)
            and candidate.cu >= config.cu_min
        ):
            candidate.state = CompositionState.REUSABLE
            # Capability-candidate flag when multi-skill reusable chain.
            if len(candidate.skill_ids) >= 2:
                meta = dict(candidate.metadata or {})
                meta["capability_candidate"] = True
                candidate.metadata = meta

    return candidate


def promote_composition(
    candidate: CompositionCandidate,
    library: SkillLibrary,
    config: SkillConfig | None = None,
) -> Skill | None:
    """Promote reusable composition to a Skill when reuse threshold met."""
    config = config or SkillConfig()
    if candidate.state is CompositionState.PROMOTED:
        existing = library.get(candidate.composition_id)
        return existing
    if candidate.state is not CompositionState.REUSABLE:
        return None
    uses = int((candidate.evidence or {}).get("uses", 0) or 0)
    if uses < int(config.compose_min_reuse_promote):
        return None
    if candidate.confidence < float(config.compose_min_confidence):
        return None

    order = list(candidate.order or candidate.skill_ids)
    level = max(1, len(order) - 1)
    triggers = list((candidate.metadata or {}).get("triggers") or [])
    skill = Skill(
        skill_id=candidate.composition_id,
        source_invariant_id="",
        trigger_conditions=triggers,
        execution_policy="compose:" + "+".join(order),
        abstraction_gain=float(candidate.expected_utility or 0.0),
        transfer_score=float(candidate.expected_transfer or 0.0),
        creation_cost=float(candidate.composition_cost or 0.0),
        reuse_count=uses,
        utility=float(candidate.cu),
        scv=float(candidate.cu),
        state=SkillState.ACTIVE,
        metadata={
            "composed_from": order,
            "composition_level": level,
            "composition_id": candidate.composition_id,
            "capability_candidate": bool(
                (candidate.metadata or {}).get("capability_candidate")
            ),
            "mvp_category": "composed",
            "composition_potential": min(1.0, 0.5 + 0.1 * level),
            "confidence": float(candidate.confidence),
            "cu_breakdown": dict(
                (candidate.metadata or {}).get("cu_breakdown") or {}
            ),
        },
    )
    refresh_skill_utility(skill, config)
    if library.get(skill.skill_id) is None:
        library.add(skill)
    candidate.state = CompositionState.PROMOTED
    meta = dict(candidate.metadata or {})
    meta["promoted_skill_id"] = skill.skill_id
    candidate.metadata = meta
    return skill
