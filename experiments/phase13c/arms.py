"""Matched policy arm execution and small Skill representation helpers."""
from __future__ import annotations

import random
from typing import Any
from core.skill import Skill
from skills.config import SkillConfig
from .common import MC_SENSITIVITY
from .evaluation import _evaluate_memory_only, _evaluate_skill
from .scoring import _candidate_score
from .tasking import _opportunities


def _candidate_arm_result(
    item: dict[str, Any],
    arm: str,
    trace_run: Any,
    eval_tasks: list[GridTask],
    skill_config: SkillConfig,
    random_create_probability: float,
    rng: random.Random,
) -> tuple[dict[str, Any], Skill | None]:
    inv = item["invariant"]
    candidate, score = _candidate_score(inv, skill_config)
    selected = {
        "SCT": score["SCV10"] > 0.0,
        "NEVER_CREATE": False,
        "ALWAYS_CREATE": True,
        "RANDOM_CREATE": rng.random() < random_create_probability,
        "MEMORY_ONLY": False,
    }[arm]
    source_family = str((candidate.metadata or {}).get("mvp_category", "general"))
    opportunities = _opportunities(inv, eval_tasks, 10)
    cc = max(0.0, float(candidate.creation_cost))
    primary_mc = float(skill_config.base_maintenance) + 0.01
    if arm == "MEMORY_ONLY":
        result = _evaluate_memory_only(
            inv,
            trace_run,
            eval_tasks,
            creation_cost=cc,
            maintenance_per_opportunity=primary_mc,
        )
        result["realized_net_value_by_mc"] = {
            f"{mc:.2f}": (
                float(result["total_success_gated_benefit"])
                - float(result["creation_cost_proxy"])
                - len(opportunities) * mc
                if result["created"] else 0.0
            )
            for mc in MC_SENSITIVITY
        }
        return (
            {
                "arm": arm,
                "selected": bool(result["created"]),
                "created": bool(result["created"]),
                "creation_cost": result["creation_cost_proxy"],
                "maintenance_cost": result["maintenance_cost"],
                "total_success_gated_benefit": result["total_success_gated_benefit"],
                "realized_net_value": result["realized_net_value"],
                "realized_net_value_by_mc": result["realized_net_value_by_mc"],
                "reuse_statistics": result["reuse_statistics"],
                "task_results": result["task_results"],
                "utility_timeline": [],
                "representation": result["representation"],
                "retrieved_trace_id": result["source_trace_id"],
                "macro_retrieved": result["macro_retrieved"],
            },
            None,
        )
    if not selected:
        return (
            {
                "arm": arm,
                "selected": False,
                "created": False,
                "creation_cost": 0.0,
                "maintenance_cost": 0.0,
                "total_success_gated_benefit": 0.0,
                "realized_net_value": 0.0,
                "realized_net_value_by_mc": {f"{mc:.2f}": 0.0 for mc in MC_SENSITIVITY},
                "reuse_statistics": {
                    "eligible_opportunities": len(opportunities),
                    "applied_attempts": 0,
                    "successful_applications": 0,
                    "credited_reuses": 0,
                    "failed_applications": 0,
                    "no_match": len(opportunities),
                    "reuse_rate_opportunity": 0.0,
                    "TS_cross_family": 0.0,
                    "unique_skill_reused": 0,
                    "reuse_count": 0,
                },
                "task_results": [],
                "utility_timeline": [],
                "representation": "no_executable_skill",
            },
            None,
        )
    evaluation = _evaluate_skill(
        inv,
        candidate,
        trace_run,
        eval_tasks,
        skill_config,
        maintenance_per_opportunity=primary_mc,
    )
    skill = evaluation.pop("skill", None)
    evaluation["realized_net_value_by_mc"] = {
        f"{mc:.2f}": (
            float(evaluation["total_success_gated_benefit"])
            - float(evaluation["creation_cost"])
            - int(evaluation["reuse_statistics"]["eligible_opportunities"]) * mc
        )
        if evaluation["created"] else 0.0
        for mc in MC_SENSITIVITY
    }
    return ({"arm": arm, "selected": selected, **evaluation, "representation": "Skill"}, skill)


def _clone_skill(skill: Skill) -> Skill:
    return Skill.from_dict(skill.to_dict())


def _operation_for_skill(skill: Skill) -> list[str]:
    return _macro_ops_for_signature(skill.trigger_conditions)
