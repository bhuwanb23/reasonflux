"""Frozen Phase 13F arm construction using Phase 13E APIs."""
from __future__ import annotations

import random
from dataclasses import replace
from typing import Any

from capability import CapabilityLibrary
from core.skill import Skill
from core.states import SkillState
from experiments.phase13e.arms import _create_candidate_skill, _raw_pattern_skills, form_capabilities
from experiments.phase13e.common import capability_config_from_json, family_of_trace, signature_of_trace
from experiments.phase13e.runner import _run_task
from skills.config import SkillConfig
from skills.library import SkillLibrary

from .common import ArmRuntime, names


def _trace_episode_skills(traces: list[Any], seed: int) -> list[Skill]:
    """One executable record per raw episode; no invariant mining or consolidation."""
    out = []
    for index, trace in enumerate(traces):
        sig = signature_of_trace(trace)
        if not sig:
            continue
        out.append(Skill(
            skill_id=f"episode-{seed}-{index}", source_invariant_id="",
            trigger_conditions=list(sig), execution_policy="episodic_trace_memory",
            abstraction_gain=0.0, transfer_score=0.0, creation_cost=0.0, utility=0.0,
            state=SkillState.PROMOTED,
            metadata={"mvp_category": family_of_trace(trace), "raw_trace_pattern": True,
                      "episodic_memory": True, "confidence": 0.0, "provisional": True,
                      "source_task_id": str(trace.task_id)},
        ))
    return out


def _frequency(item: dict[str, Any]) -> float:
    inv = item["invariant"]
    validation = (inv.metadata or {}).get("validation") or {}
    return float(validation.get("frequency", item["score"].get("p_reuse_raw", 0.0)) or 0.0)


def _scv_selected(pool: list[dict[str, Any]], threshold: float = 0.0) -> list[dict[str, Any]]:
    return [x for x in pool if float(x["score"]["SCV10"]) > threshold]


def _make_library(items: list[dict[str, Any]], seed: int, *, random_order: bool = False) -> SkillLibrary:
    library = SkillLibrary()
    seq = list(items)
    if random_order:
        random.Random(seed + 74131).shuffle(seq)
    for item in seq:
        skill = _create_candidate_skill(item, library, SkillConfig())
        if skill is not None and library.get(skill.skill_id) is None:
            library.add(skill)
    return library


def _caps(name: str) -> bool:
    return name not in {"B1_NO_LEARNING", "B2_MEMORY_SKILL_STORE", "A3_NO_CAPABILITY_LAYER"}


def _composition(name: str) -> bool:
    return name not in {"B1_NO_LEARNING", "B2_MEMORY_SKILL_STORE", "B4_COMPRESSION_PROXY", "A2_3_NO_COMPOSITION", "X1_NO_TRANSFER", "X2_NO_SKILL_LIBRARY"}


def build_arms(seed: int, discovery: dict[str, Any], config: dict[str, Any]) -> dict[str, ArmRuntime]:
    pool = list(discovery["candidates"])
    traces = list(discovery["trace_run"].traces)
    asft = _scv_selected(pool)
    rng = random.Random(seed + 91371)
    random_budget = rng.sample(pool, min(len(asft), len(pool)))
    frequency_budget = sorted(pool, key=lambda x: (-_frequency(x), x["invariant"].invariant_id))[:len(asft)]
    scv_low, scv_high = config["sensitivity"]["scv_thresholds"][1:]
    is_mid, is_high = config["sensitivity"]["invariant_strength_thresholds"][1:]
    fraction = float(config["arms"]["b3_random_fraction"])
    random_b3 = random.Random(seed + 74132).sample(pool, min(len(pool), max(1, round(fraction * len(pool))))) if pool else []
    selected: dict[str, list[dict[str, Any]]] = {
        "ASFT": asft,
        "B3_RANDOM_SKILL_CREATION": random_b3,
        "A1_1_FREQUENCY_ONLY": frequency_budget,
        "A2_NO_SCV": list(pool),
        "A2_1_RANDOM_SCV": random_budget,
        "SENS_SCV_Q25": _scv_selected(pool, float(scv_low)),
        "SENS_SCV_Q75": _scv_selected(pool, float(scv_high)),
        "SENS_IS_7_5": [x for x in pool if float(x["invariant"].strength) >= float(is_mid)],
        "SENS_IS_10": [x for x in pool if float(x["invariant"].strength) >= float(is_high)],
    }
    runtimes: dict[str, ArmRuntime] = {}
    for name in names(config):
        lib = SkillLibrary()
        enabled_library = True
        if name == "B2_MEMORY_SKILL_STORE":
            for skill in _trace_episode_skills(traces, seed):
                lib.add(skill)
        elif name in {"B4_COMPRESSION_PROXY", "A1_NO_IDT"}:
            for skill in _raw_pattern_skills(traces, seed=seed, compression=name == "B4_COMPRESSION_PROXY"):
                if lib.get(skill.skill_id) is None:
                    lib.add(skill)
        elif name not in {"B1_NO_LEARNING", "A3_1_NO_GROWTH_TRACKING", "A3_2_INDEPENDENT_CAPABILITIES", "X1_NO_TRANSFER", "X2_NO_SKILL_LIBRARY", "X3_NO_EXPERIENCE_MEMORY", "X4_NO_CAPABILITY_FORMATION", "SENS_COMP_LOOSE", "SENS_COMP_STRICT"}:
            lib = _make_library(selected.get(name, asft), seed, random_order=name == "B3_RANDOM_SKILL_CREATION")
        elif name in {"A3_1_NO_GROWTH_TRACKING", "A3_2_INDEPENDENT_CAPABILITIES", "X1_NO_TRANSFER", "X2_NO_SKILL_LIBRARY", "X3_NO_EXPERIENCE_MEMORY", "X4_NO_CAPABILITY_FORMATION", "SENS_COMP_LOOSE", "SENS_COMP_STRICT"}:
            lib = _make_library(asft, seed)
        created_skill_count = len(lib)
        if name == "X2_NO_SKILL_LIBRARY":
            lib = SkillLibrary()
            enabled_library = False
        if name == "X1_NO_TRANSFER":
            enabled_library = False
        if name == "X3_NO_EXPERIENCE_MEMORY":
            for skill in lib.list_skills():
                meta = dict(skill.metadata or {})
                meta.pop("experience_history", None)
                meta["discovery_traces_discarded"] = True
                skill.metadata = meta
        runtime = ArmRuntime(
            arm=name, library=lib, capabilities=CapabilityLibrary(),
            enabled_library=enabled_library, enable_capabilities=_caps(name),
            enable_composition=_composition(name),
            atomic_only=False,
            mask_growth=name in {"A3_1_NO_GROWTH_TRACKING", "A3_2_INDEPENDENT_CAPABILITIES"},
            composition_rows=[], candidate_count=len(lib), formation_log=[],
        )
        runtime.created_skill_count = created_skill_count
        runtime.allow_capability_formation = name != "X4_NO_CAPABILITY_FORMATION"
        runtime.lifecycle_enabled = name != "A2_2_NO_LIFECYCLE"
        runtime.independent_capabilities = name == "A3_2_INDEPENDENT_CAPABILITIES"
        runtime.skill_config = SkillConfig()
        if name == "SENS_COMP_LOOSE":
            runtime.enable_composition = True
            runtime.skill_config = replace(SkillConfig(), compose_min_reuse_promote=2)
        elif name == "SENS_COMP_STRICT":
            runtime.enable_composition = True
            runtime.skill_config = replace(SkillConfig(), compose_min_successes_validate=2, compose_min_reuse_promote=4)
        runtimes[name] = runtime
    return runtimes


def run_task(runtime: ArmRuntime, task: Any, clock: int) -> tuple[dict[str, Any], Any]:
    """Apply the common task solver/reuse evaluator with frozen arm config."""
    return _run_task(runtime, task, clock, runtime.skill_config)


def form(runtime: ArmRuntime, config: dict[str, Any]) -> list[dict[str, Any]]:
    if not runtime.enable_capabilities or not runtime.allow_capability_formation:
        return []
    return form_capabilities(runtime, total_families=len(config["task_families"]), config=capability_config_from_json(config))
