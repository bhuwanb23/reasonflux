"""Phase 13E policy arms and evidence-backed capability formation."""
from __future__ import annotations

import random
from dataclasses import dataclass, replace
from typing import Any

from capability import (
    CapabilityConfig,
    CapabilityLibrary,
    CapabilityType,
    advance_capability,
    compute_capability_utility,
    propose_capabilities_from_library,
    validate_capability,
)
from core.skill import Skill
from core.states import SkillState
from evaluation.growth_config import GrowthConfig
from skills.composition.evaluate import record_composition_outcome
from skills.composition.lifecycle import advance_composition, promote_composition
from skills.composition.propose import propose_sequential
from skills.config import SkillConfig
from skills.library import SkillLibrary
from skills.promotion import promote_skill

from .common import family_of_trace, signature_of_trace


@dataclass
class ArmRuntime:
    arm: str
    library: SkillLibrary
    capabilities: CapabilityLibrary
    enabled_library: bool = True
    enable_capabilities: bool = True
    enable_composition: bool = True
    atomic_only: bool = False
    mask_growth: bool = False
    composition: Any | None = None
    composition_skill_id: str = ""
    composition_rows: list[dict[str, Any]] | None = None
    candidate_count: int = 0
    formation_log: list[dict[str, Any]] | None = None


def _create_candidate_skill(item: dict[str, Any], lib: SkillLibrary, config: SkillConfig) -> Skill | None:
    inv = item["invariant"]
    candidate = item["candidate"]
    gate = replace(config, skill_creation_threshold=-1.0e9)
    result = promote_skill(
        candidate,
        invariant=inv,
        library=lib,
        config=gate,
        allow_prior_evidence=True,
    )
    return result.skill if result.promoted else None


def _raw_pattern_skills(traces: list[Any], *, seed: int, compression: bool) -> list[Skill]:
    """Transparent repeated-program proxy; not attributed to IDT or DreamCoder."""
    groups: dict[tuple[str, ...], list[Any]] = {}
    compressible = {"find_symmetry", "apply_reflection", "find_rotation", "apply_rotation", "count_objects", "group_by_color"}
    for trace in traces:
        raw = signature_of_trace(trace)
        sig = tuple(op for op in raw if op in compressible) if compression else raw
        if sig:
            groups.setdefault(sig, []).append(trace)
    out: list[Skill] = []
    for index, (sig, rows) in enumerate(sorted(groups.items())):
        if len(rows) < 3:
            continue
        family_counts: dict[str, int] = {}
        for trace in rows:
            fam = family_of_trace(trace)
            family_counts[fam] = family_counts.get(fam, 0) + 1
        family = sorted(family_counts, key=lambda x: (-family_counts[x], x))[0]
        sid = f"raw-{seed}-{index}"
        metadata = {
            "mvp_category": family,
            "raw_trace_pattern": True,
            "compression_proxy": bool(compression),
            "observed_frequency": len(rows),
            "pattern_signature": list(sig),
            "confidence": 0.0,
            "provisional": True,
        }
        out.append(
            Skill(
                skill_id=sid,
                source_invariant_id="",
                trigger_conditions=list(sig),
                execution_policy="raw_trace_pattern",
                abstraction_gain=0.0,
                transfer_score=0.0,
                creation_cost=0.0,
                utility=0.0,
                state=SkillState.PROMOTED,
                metadata=metadata,
            )
        )
    return out


def build_arms(seed: int, discovery: dict[str, Any], config: dict[str, Any]) -> dict[str, ArmRuntime]:
    """Instantiate all preregistered arms from the same discovery records."""
    pool = list(discovery["candidates"])
    scv = [x for x in pool if float(x["score"]["SCV10"]) > 0.0]
    rng = random.Random(int(seed) + 91371)
    shuffled = list(pool)
    rng.shuffle(shuffled)
    random_items = shuffled[: len(scv)]
    traces = list(discovery["trace_run"].traces)
    names = ["ASFT", "B1_NO_LEARNING", "B2_SKILL_STORAGE_ONLY", "B3_RANDOM_SKILL_CREATION", "B4_COMPRESSION_PROXY", "A1_NO_IDT", "A2_NO_SCT", "A3_NO_SKILL_LIBRARY", "A4_NO_COMPOSITION", "A5_NO_CGM"]
    runtimes: dict[str, ArmRuntime] = {}
    skill_cfg = SkillConfig()
    for name in names:
        lib = SkillLibrary()
        enabled_library = name != "A3_NO_SKILL_LIBRARY"
        enable_caps = name not in {"B1_NO_LEARNING", "A3_NO_SKILL_LIBRARY"}
        enable_comp = name not in {"B1_NO_LEARNING", "B2_SKILL_STORAGE_ONLY", "B3_RANDOM_SKILL_CREATION", "B4_COMPRESSION_PROXY", "A1_NO_IDT", "A3_NO_SKILL_LIBRARY", "A4_NO_COMPOSITION"}
        if name in {"ASFT", "A4_NO_COMPOSITION", "A5_NO_CGM"}:
            selected = scv
        elif name == "B2_SKILL_STORAGE_ONLY":
            selected = scv
        elif name == "B3_RANDOM_SKILL_CREATION":
            selected = random_items
        elif name == "A2_NO_SCT":
            selected = pool
        else:
            selected = []
        if enabled_library and name not in {"B4_COMPRESSION_PROXY", "A1_NO_IDT"}:
            for item in selected:
                skill = _create_candidate_skill(item, lib, skill_cfg)
                if skill is not None and lib.get(skill.skill_id) is None:
                    pass  # promote_skill already inserted it in the library
        if name in {"B4_COMPRESSION_PROXY", "A1_NO_IDT"}:
            for skill in _raw_pattern_skills(traces, seed=seed, compression=name == "B4_COMPRESSION_PROXY"):
                if lib.get(skill.skill_id) is None:
                    lib.add(skill)
        runtimes[name] = ArmRuntime(
            arm=name,
            library=lib,
            capabilities=CapabilityLibrary(),
            enabled_library=enabled_library,
            enable_capabilities=enable_caps,
            enable_composition=enable_comp,
            atomic_only=name == "B2_SKILL_STORAGE_ONLY",
            mask_growth=name == "A5_NO_CGM",
            composition_rows=[],
            candidate_count=len(lib),
            formation_log=[],
        )
    return runtimes


def form_capabilities(runtime: ArmRuntime, *, total_families: int = 4, config: CapabilityConfig | None = None) -> list[dict[str, Any]]:
    """Propose, validate, merge, refresh, and advance true API capabilities."""
    if not runtime.enable_capabilities:
        return []
    cap_config = config or CapabilityConfig()
    events: list[dict[str, Any]] = []
    proposals = propose_capabilities_from_library(runtime.library, config=cap_config, require_valid=True)
    if runtime.atomic_only:
        proposals = [p for p in proposals if p.capability_type is CapabilityType.ATOMIC]
    for proposal in proposals:
        result = validate_capability(proposal, runtime.library, cap_config)
        if not result.valid:
            events.append({"capability_id": proposal.capability_id, "accepted": False, "reasons": result.reasons})
            continue
        cap = runtime.capabilities.get(proposal.capability_id)
        if cap is None:
            runtime.capabilities.add(proposal)
            cap = proposal
            before = 0.0
        else:
            before = float(cap.utility or 0.0)
            for sid in proposal.skill_ids:
                cap.add_skill(sid)
            # Refresh evidence from newly-added members using the repository API.
            from capability.evidence import seed_from_skills
            seed_from_skills(cap, runtime.library)
        compute_capability_utility(cap, runtime.library, cap_config, total_families=total_families)
        advance_capability(
            cap,
            library=runtime.library,
            config=cap_config,
            previous_utility=before,
            total_families=total_families,
        )
        members = [runtime.library.get(sid) for sid in cap.skill_ids]
        present_members = [s for s in members if s is not None]
        categories = [str((s.metadata or {}).get("mvp_category", "general")) for s in present_members]
        member_ts = [float(s.transfer_score or 0.0) for s in present_members]
        member_reuse = [float(s.reuse_count or 0) for s in present_members]
        counts = {cat: categories.count(cat) for cat in set(categories)}
        target_sets = [
            {str(e.get("target_family")) for e in (s.transfer_history or []) if e.get("success") and e.get("target_family")}
            for s in members if s is not None
        ]
        pairwise = []
        for i, left in enumerate(target_sets):
            for right in target_sets[i + 1:]:
                union = left | right
                pairwise.append(len(left & right) / len(union) if union else 0.0)
        events.append({
            "capability_id": cap.capability_id,
            "accepted": True,
            "type": cap.capability_type.value,
            "member_skill_ids": list(cap.skill_ids),
            "member_categories": categories,
            "category_purity": max(counts.values()) / len(categories) if categories else None,
            "mean_member_ts": sum(member_ts) / len(member_ts) if member_ts else None,
            "mean_member_reuse_count": sum(member_reuse) / len(member_reuse) if member_reuse else None,
            "mean_pairwise_target_family_jaccard": sum(pairwise) / len(pairwise) if pairwise else None,
            "state": cap.state.value,
            "confidence": float(cap.confidence),
            "utility": float(cap.utility),
        })
    if runtime.formation_log is not None:
        runtime.formation_log.extend(events)
    return events


def propose_composition(runtime: ArmRuntime, config: SkillConfig | None = None) -> Any | None:
    """Return the preregistered rotation→reflection proposal if learned skills support it."""
    if not runtime.enable_composition or len(runtime.library) < 2:
        return None
    skills = runtime.library.list_skills()
    by_category: dict[str, Skill] = {}
    for skill in sorted(skills, key=lambda x: x.skill_id):
        category = str((skill.metadata or {}).get("mvp_category", "general"))
        if category in {"rotation", "reflection"} and category not in by_category:
            by_category[category] = skill
    if set(by_category) != {"rotation", "reflection"}:
        return None
    ordered = [by_category["rotation"], by_category["reflection"]]
    requirements = [op for skill in ordered for op in skill.trigger_conditions]
    candidates = propose_sequential(runtime.library, requirements, config or SkillConfig(), skills=ordered)
    wanted = [skill.skill_id for skill in ordered]
    return next((candidate for candidate in candidates if candidate.order == wanted), None)


def record_composition_task(runtime: ArmRuntime, task: Any, baseline: Any, macros: list[str], config: SkillConfig | None = None) -> dict[str, Any] | None:
    """Run a real composed macro on its reference task and advance composition lifecycle."""
    if not runtime.enable_composition:
        return None
    if runtime.composition is None:
        runtime.composition = propose_composition(runtime, config)
    candidate = runtime.composition
    if candidate is None:
        return {"status": "unavailable_no_learned_proposal", "task_id": task.task_id}
    from solver.executor import GridSolver
    solver = GridSolver(compose=True)
    composite = solver.solve(task, macro_ops=macros)
    best_single = None
    for skill_id in candidate.order:
        skill = runtime.library.get(skill_id)
        op = next((str(t) for t in (skill.trigger_conditions if skill else []) if str(t).startswith("apply_")), None)
        single = solver.solve(task, macro_ops=[op] if op else [])
        if best_single is None or single.cost < best_single.cost:
            best_single = single
    base_cost = float(baseline.cost)
    benefit = max(0.0, min(1.0, (base_cost - float(composite.cost)) / base_cost)) if base_cost else 0.0
    single_benefit = max(0.0, min(1.0, (base_cost - float(best_single.cost)) / base_cost)) if best_single and base_cost else 0.0
    gain = benefit - single_benefit if composite.success else 0.0
    record_composition_outcome(
        candidate,
        success=bool(composite.success),
        transfer_gain=max(0.0, gain),
        reasoning_reduction=benefit,
        task_family=task.task_family,
        config=config or SkillConfig(),
    )
    advance_composition(candidate, config or SkillConfig())
    promoted = promote_composition(candidate, runtime.library, config or SkillConfig())
    if promoted is not None:
        runtime.composition_skill_id = promoted.skill_id
        if composite.success:
            from skills.monitoring import record_transfer
            record_transfer(
                promoted,
                source_family="composed",
                target_family=task.task_family,
                success=True,
                benefit=benefit,
                config=config or SkillConfig(),
            )
            successes = [e for e in promoted.transfer_history or [] if e.get("success")]
            promoted.transfer_score = sum(float(e.get("benefit", 0.0) or 0.0) for e in successes) / len(successes) if successes else 0.0
            from skills.utility import refresh_skill_utility
            refresh_skill_utility(promoted, config or SkillConfig())
    row = {
        "status": "evaluated",
        "task_id": task.task_id,
        "candidate_id": candidate.composition_id,
        "order": list(candidate.order),
        "success": bool(composite.success),
        "baseline_success": bool(baseline.success),
        "baseline_cost": base_cost,
        "composed_cost": float(composite.cost),
        "best_single_cost": float(best_single.cost) if best_single else None,
        "composition_benefit": benefit if composite.success else 0.0,
        "best_single_benefit": single_benefit,
        "incremental_gain": gain,
        "lifecycle_state": candidate.state.value,
        "promoted_skill_id": runtime.composition_skill_id or None,
    }
    if runtime.composition_rows is not None:
        runtime.composition_rows.append(row)
    return row
