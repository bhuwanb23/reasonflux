"""One confirmatory seed: common candidate pool, arms, lifecycle, composition."""
from __future__ import annotations

import random
from statistics import mean
from typing import Any
from pipelines.invariant_pipeline import run_invariant_pipeline
from skills.candidate import from_invariant
from skills.config import SkillConfig
from skills.library import SkillLibrary
from .arms import _candidate_arm_result, _clone_skill
from .common import load_config
from .composition import _composition_eval
from .lifecycle import _run_lifecycle
from .scoring import _eligible_pool
from .tasking import _enforce_opportunity_horizon, _task_batches
from .evaluation import _evaluate_skill


def run_confirmation_seed(run_seed: int, frozen: dict[str, Any]) -> dict[str, Any]:
    config_data = load_config()
    skill_config = SkillConfig()
    trace_run, eval_tasks = _task_batches(run_seed, config_data)
    inv_run = run_invariant_pipeline(trace_run.traces, bootstrap=True)
    eligible, rejected = _eligible_pool(inv_run.promotable, skill_config)
    eligible, rejected = _enforce_opportunity_horizon(
        eligible, rejected, eval_tasks,
        int(config_data["tasks"]["evaluation_opportunities_per_candidate"]),
    )
    rng = random.Random(run_seed + 8173)
    candidates_out: list[dict[str, Any]] = []
    skill_objects: list[Skill] = []
    for item in eligible:
        inv = item["invariant"]
        candidate = item["candidate"]
        arm_results: dict[str, Any] = {}
        for arm in ("SCT", "NEVER_CREATE", "ALWAYS_CREATE", "RANDOM_CREATE", "MEMORY_ONLY"):
            row, skill = _candidate_arm_result(
                item,
                arm,
                trace_run,
                eval_tasks,
                skill_config,
                float(frozen["random_create_probability"]),
                rng,
            )
            arm_results[arm] = row
            if arm == "SCT" and skill is not None:
                skill_objects.append(skill)
        # Isolated shadow outcome for every common eligible candidate, irrespective
        # of SCT decision; this avoids selecting only positive-SCV candidates.
        primary_mc = float(skill_config.base_maintenance) + 0.01
        shadow = _evaluate_skill(
            inv,
            from_invariant(inv, config=skill_config, allow_prior_transfer=True),
            trace_run,
            eval_tasks,
            skill_config,
            maintenance_per_opportunity=primary_mc,
            lifecycle_enabled=True,
        )
        shadow_skill = shadow.pop("skill", None)
        no_lifecycle = _evaluate_skill(
            inv,
            from_invariant(inv, config=skill_config, allow_prior_transfer=True),
            trace_run,
            eval_tasks,
            skill_config,
            maintenance_per_opportunity=primary_mc,
            lifecycle_enabled=False,
        )
        no_lifecycle.pop("skill", None)
        candidate_metrics = {
            "invariant_id": inv.invariant_id,
            "signature": list(inv.pattern_signature),
            "category": str((candidate.metadata or {}).get("mvp_category", "general")),
            "frequency": int(inv.frequency),
            "task_families": list(inv.task_families),
            **item["score"],
            "shadow_realized_net_value": float(shadow.get("realized_net_value", 0.0)),
            "shadow_mean_SU_at_end": float(shadow.get("mean_SU_at_end", 0.0)),
            "shadow_reuse_count": int(shadow.get("reuse_statistics", {}).get("reuse_count", 0)),
            "shadow_TS_cross_family": float(shadow.get("reuse_statistics", {}).get("TS_cross_family", 0.0)),
            "no_lifecycle_realized_net_value": float(no_lifecycle.get("realized_net_value", 0.0)),
            "shadow_task_results": shadow.get("task_results", []),
            "no_lifecycle_task_results": no_lifecycle.get("task_results", []),
            "no_lifecycle_utility_timeline": no_lifecycle.get("utility_timeline", []),
            "arms": arm_results,
        }
        candidates_out.append(candidate_metrics)
        if shadow_skill is not None:
            del shadow_skill
    arm_values = {}
    arm_values_by_mc = {}
    for arm in ("SCT", "NEVER_CREATE", "ALWAYS_CREATE", "RANDOM_CREATE", "MEMORY_ONLY"):
        values = [float(row["arms"][arm]["realized_net_value"]) for row in candidates_out]
        arm_values[arm] = mean(values) if values else 0.0
        arm_values_by_mc[arm] = {
            f"{mc:.2f}": mean(
                float(row["arms"][arm].get("realized_net_value_by_mc", {}).get(f"{mc:.2f}", 0.0))
                for row in candidates_out
            ) if candidates_out else 0.0
            for mc in MC_SENSITIVITY
        }
    thresholds = {"primary": 0.0, **dict(frozen["thresholds"])}
    threshold_sensitivity = {
        name: mean(
            float(row["shadow_realized_net_value"])
            if float(row["SCV10"]) > float(cutoff) else 0.0
            for row in candidates_out
        ) if candidates_out else 0.0
        for name, cutoff in thresholds.items()
    }
    no_lifecycle_mean = mean(
        float(row["no_lifecycle_realized_net_value"]) for row in candidates_out
    ) if candidates_out else 0.0
    lifecycle_mean = mean(
        float(row["shadow_realized_net_value"]) for row in candidates_out
    ) if candidates_out else 0.0
    contrasts = {
        f"SCT_minus_{control}": arm_values["SCT"] - arm_values[control]
        for control in ("NEVER_CREATE", "ALWAYS_CREATE", "RANDOM_CREATE", "MEMORY_ONLY")
    }
    lifecycle_rows = []
    for skill in skill_objects:
        lifecycle_rows.append(
            _run_lifecycle(
                skill,
                run_seed,
                skill_config,
                probe_seed_offset=int(config_data["tasks"]["lifecycle_probe_seed_offset"]),
            )
        )
    sct_library = SkillLibrary()
    for skill in skill_objects:
        # Only the SCT policy-created skills are exposed to composition.
        if sct_library.get(skill.skill_id) is None:
            sct_library.add(_clone_skill(skill))
    composition_rows = _composition_eval(
        sct_library,
        run_seed=run_seed,
        config=skill_config,
        training_seed_offset=int(config_data["tasks"]["composition_training_seed_offset"]),
        validation_seed_offset=int(config_data["tasks"]["composition_validation_seed_offset"]),
        reuse_seed_offset=int(config_data["tasks"]["composition_reuse_seed_offset"]),
    )
    lifecycle_task_ids = {
        str(probe["task_id"])
        for row in lifecycle_rows
        for transition in row.get("transitions", [])
        for probe in transition.get("probe_task_results", [])
    }
    composition_task_ids = {
        str(task["task_id"])
        for row in composition_rows
        for task in row.get("task_results", [])
    }
    composition_task_ids.update(
        str(task["task_id"])
        for row in composition_rows
        for task in row.get("single_skill_probe", [])
        if task.get("task_id")
    )
    composition_task_ids.update(
        str(row["new_task_task_id"])
        for row in composition_rows
        if row.get("new_task_task_id")
    )
    if lifecycle_task_ids & composition_task_ids:
        raise AssertionError("lifecycle and composition task IDs overlap")
    return {
        "seed": run_seed,
        "discovery_seed": run_seed + config_data["tasks"]["discovery_seed_offset"],
        "evaluation_seed": run_seed + config_data["tasks"]["evaluation_seed_offset"],
        "trace_count": len(trace_run.traces),
        "promotable_count": len(inv_run.promotable),
        "eligible_candidate_count": len(eligible),
        "rejected_candidates": rejected,
        "candidates": candidates_out,
        "arm_mean_net_values": arm_values,
        "arm_mean_net_values_by_mc": arm_values_by_mc,
        "threshold_sensitivity": threshold_sensitivity,
        "lifecycle_ablation": {
            "lifecycle_enabled_mean_net_value": lifecycle_mean,
            "lifecycle_disabled_mean_net_value": no_lifecycle_mean,
            "paired_difference_enabled_minus_disabled": lifecycle_mean - no_lifecycle_mean,
        },
        "paired_contrasts": contrasts,
        "lifecycle": lifecycle_rows,
        "composition": composition_rows,
        "failure_cases": [
            {"candidate_id": row["invariant_id"], "arm": arm, "reasons": row["arms"][arm].get("rejection_reasons", [])}
            for row in candidates_out
            for arm in ("SCT", "ALWAYS_CREATE", "RANDOM_CREATE")
            if row["arms"][arm].get("selected") and not row["arms"][arm].get("created")
        ],
    }
