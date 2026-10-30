"""Propose sequential composition candidates with failure guards (Phase 11D-4)."""

from __future__ import annotations

from itertools import permutations
from typing import Sequence

from core.skill import Skill
from skills.candidate import classify_mvp_category
from skills.composition.models import CompositionCandidate, composition_id_for
from skills.composition.trigger import covers_all, skill_coverage
from skills.composition.utility import composition_cost_for, compute_cu
from skills.config import SkillConfig
from skills.library import SkillLibrary
from skills.retrieval import retrieve_skills
from skills.utility_components import compute_cp


def _merged_triggers(skills: Sequence[Skill]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for skill in skills:
        for t in skill.trigger_conditions or []:
            key = str(t).lower()
            if key not in seen:
                seen.add(key)
                out.append(str(t))
    return out


def _literal_count(triggers: Sequence[str]) -> int:
    return sum(1 for t in triggers if ":" in str(t))


def _category(skill: Skill) -> str:
    meta = skill.metadata or {}
    if meta.get("mvp_category"):
        return str(meta["mvp_category"])
    return classify_mvp_category(skill.trigger_conditions or [])


def is_redundant(
    skills: Sequence[Skill], config: SkillConfig
) -> str | None:
    """Return rejection reason if redundant, else None."""
    ids = [s.skill_id for s in skills]
    if config.compose_reject_identical and len(set(ids)) < len(ids):
        return "identical_skill_ids"
    cats = [_category(s) for s in skills]
    for a, b in zip(cats, cats[1:]):
        if a == b and a != "general":
            return "redundant_category"
    # Identical trigger signatures in sequence
    sigs = [tuple(sorted(str(t).lower() for t in (s.trigger_conditions or []))) for s in skills]
    for a, b in zip(sigs, sigs[1:]):
        if a and a == b:
            return "identical_signature"
    return None


def is_overspecialized(skills: Sequence[Skill], config: SkillConfig) -> bool:
    return _literal_count(_merged_triggers(skills)) > int(
        config.compose_max_literal_triggers
    )


def _jointly_covers(skills: Sequence[Skill], requirements: Sequence[str]) -> bool:
    """Ordered chain covers if union of triggers covers requirements."""
    from skills.composition.trigger import _norm_set

    req = _norm_set(requirements)
    if not req:
        return True
    union: set[str] = set()
    for skill in skills:
        union |= _norm_set(skill.trigger_conditions or [])
    return req <= union


def _seed_expectations(
    skills: Sequence[Skill], config: SkillConfig
) -> tuple[float, float]:
    utils = [float(s.utility or 0.0) for s in skills]
    cps = [compute_cp(s, config) for s in skills]
    mean_u = sum(utils) / len(utils) if utils else 0.0
    mean_cp = sum(cps) / len(cps) if cps else config.default_cp
    transfers = [float(s.transfer_score or 0.0) for s in skills]
    mean_t = sum(transfers) / len(transfers) if transfers else 0.0
    return mean_u * 0.5 + mean_cp * 0.5, mean_t


def propose_sequential(
    library: SkillLibrary,
    requirements: Sequence[str],
    config: SkillConfig | None = None,
    *,
    skills: Sequence[Skill] | None = None,
) -> list[CompositionCandidate]:
    """Generate ordered sequential candidates that jointly cover requirements."""
    config = config or SkillConfig()
    pool = list(skills) if skills is not None else retrieve_skills(library, config=config)
    if len(pool) < 2:
        return []

    # Prefer skills that cover at least one requirement.
    scored = sorted(
        pool,
        key=lambda s: (-skill_coverage(s, requirements), -float(s.utility or 0.0)),
    )
    # Cap exploration pool to limit explosion upstream of max_candidates.
    scored = scored[: max(6, config.compose_max_candidates_per_task)]

    candidates: list[CompositionCandidate] = []
    seen: set[str] = set()
    max_n = min(int(config.compose_max_skills), len(scored))

    for n in range(2, max_n + 1):
        for combo in permutations(scored, n):
            if any(covers_all(s, requirements) for s in combo):
                continue  # single skill already enough — skip
            if not _jointly_covers(combo, requirements):
                continue
            reason = is_redundant(combo, config)
            if reason:
                continue
            if is_overspecialized(combo, config):
                continue
            order = [s.skill_id for s in combo]
            cid = composition_id_for(order)
            if cid in seen:
                continue
            seen.add(cid)
            exp_u, exp_t = _seed_expectations(combo, config)
            cost = composition_cost_for(n, config)
            cand = CompositionCandidate(
                composition_id=cid,
                skill_ids=list(order),
                order=list(order),
                expected_utility=exp_u,
                expected_transfer=exp_t,
                composition_cost=cost,
                metadata={
                    "triggers": _merged_triggers(combo),
                    "categories": [_category(s) for s in combo],
                    "reuse_potential": exp_u,
                    "transfer_gain": exp_t,
                    "reasoning_reduction": exp_u * 0.5,
                    "level": n - 1,
                },
            )
            compute_cu(cand, config=config)
            candidates.append(cand)
            if len(candidates) >= int(config.compose_max_candidates_per_task):
                candidates.sort(key=lambda c: (-c.cu, c.composition_id))
                return candidates

    candidates.sort(key=lambda c: (-c.cu, c.composition_id))
    return candidates
