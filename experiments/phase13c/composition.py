"""Task-grounded composition candidate evaluation and reuse."""
from __future__ import annotations

from statistics import mean
from typing import Any
from skills.composition.evaluate import record_composition_outcome
from skills.composition.lifecycle import advance_composition
from skills.composition.propose import propose_sequential
from skills.composition.trigger import should_compose
from skills.config import SkillConfig
from skills.library import SkillLibrary
from solver.executor import GridSolver
from solver.tasks import make_task
from .arms import _operation_for_skill


def _composition_eval(
    library: SkillLibrary,
    *,
    run_seed: int,
    config: SkillConfig,
    training_seed_offset: int,
    validation_seed_offset: int,
    reuse_seed_offset: int,
) -> list[dict[str, Any]]:
    skills = library.list_skills()
    categories = {str((s.metadata or {}).get("mvp_category", "general")): s for s in skills}
    cases = [
        ("reflection_counting", ("reflection", "counting"), "counting", False),
        ("rotation_reflection", ("rotation", "reflection"), "reflection", True),
        ("reflection_grouping_counting", ("reflection", "grouping", "counting"), "grouping", False),
    ]
    rows: list[dict[str, Any]] = []
    for case_id, category_order, target_family, use_compose_generator in cases:
        solver = GridSolver(compose=use_compose_generator)
        missing = [category for category in category_order if category not in categories]
        if missing:
            rows.append(
                {
                    "case_id": case_id,
                    "status": "not_evaluable_missing_component_skill",
                    "missing_categories": missing,
                    "n_tasks": 0,
                }
            )
            continue
        selected_skills = [categories[category] for category in category_order]
        requirements = [op for skill in selected_skills for op in skill.trigger_conditions]
        trigger = should_compose(requirements, skills, config)
        proposed = propose_sequential(library, requirements, config)
        wanted_ids = [skill.skill_id for skill in selected_skills]
        composition = next(
            (candidate for candidate in proposed if candidate.order == wanted_ids),
            None,
        )
        if composition is None:
            rows.append(
                {
                    "case_id": case_id,
                    "status": "no_proposal_from_composition_engine",
                    "n_tasks": 0,
                    "trigger": trigger.to_dict(),
                    "candidate_orders": [c.order for c in proposed],
                }
            )
            continue
        task_rows = []
        n_tasks = 10
        for index in range(n_tasks):
            task = make_task(
                target_family,
                seed=run_seed + training_seed_offset + index,
                variant=1 if case_id == "reflection_counting" else index % 2,
                difficulty=0.2,
                compose=use_compose_generator,
            )
            baseline = solver.solve(task)
            single_rows = []
            for skill in selected_skills:
                single_macro = _operation_for_skill(skill)
                single = solver.solve(task, macro_ops=single_macro)
                single_rows.append(single)
            composite_macros = [
                op
                for skill in selected_skills
                for op in _operation_for_skill(skill)
            ]
            composite = solver.solve(task, macro_ops=composite_macros)
            reduction = max(0.0, min(1.0, (baseline.cost - composite.cost) / baseline.cost)) if baseline.cost else 0.0
            benefit = reduction if composite.success else 0.0
            best_single_benefit = max(
                (max(0.0, min(1.0, (baseline.cost - single.cost) / baseline.cost)) if baseline.cost else 0.0)
                if single.success else 0.0
                for single in single_rows
            )
            record_composition_outcome(
                composition,
                success=bool(composite.success),
                transfer_gain=max(0.0, benefit - best_single_benefit),
                reasoning_reduction=benefit,
                task_family=task.task_family,
                config=config,
            )
            advance_composition(composition, config)
            task_rows.append(
                {
                    "task_id": task.task_id,
                    "task_family": task.task_family,
                    "baseline_cost": baseline.cost,
                    "composition_cost": composite.cost,
                    "baseline_success": baseline.success,
                    "composition_success": composite.success,
                    "composition_reduction": reduction,
                    "composition_benefit": benefit,
                    "best_single_success": any(item.success for item in single_rows),
                    "best_single_cost": min(item.cost for item in single_rows),
                    "composition_order": composition.order,
                }
            )
        single_after = []
        for skill in selected_skills:
            macro = _operation_for_skill(skill)
            task = make_task(target_family, seed=run_seed + validation_seed_offset, variant=1, difficulty=0.2,
                             compose=use_compose_generator)
            baseline = solver.solve(task)
            applied = solver.solve(task, macro_ops=macro)
            single_after.append({
                "skill_id": skill.skill_id,
                "task_id": task.task_id,
                "success": applied.success,
                "reduction": max(
                    0.0,
                    min(1.0, (baseline.cost - applied.cost) / baseline.cost)
                    if baseline.cost else 0.0,
                ),
            })
        # Reuse the same learned ordered composition on a separate task seed.
        reuse_task = make_task(target_family, seed=run_seed + reuse_seed_offset, variant=1, difficulty=0.2,
                               compose=use_compose_generator)
        reuse_base = solver.solve(reuse_task)
        reuse_composed = solver.solve(reuse_task, macro_ops=composite_macros)
        reuse_benefit = max(0.0, min(1.0, (reuse_base.cost - reuse_composed.cost) / reuse_base.cost)) if reuse_base.cost else 0.0
        rows.append(
            {
                "case_id": case_id,
                "status": "evaluated",
                "composition_id": composition.composition_id,
                "order": composition.order,
                "triggered": trigger.should_compose,
                "proposal_state": composition.state.value,
                "composition_utility": composition.cu,
                "composition_confidence": composition.confidence,
                "composition_ncr": composition.ncr,
                "n_tasks": len(task_rows),
                "success_rate": mean(float(r["composition_success"]) for r in task_rows),
                "mean_reasoning_reduction": mean(float(r["composition_benefit"]) for r in task_rows),
                "mean_composition_cost": mean(float(r["composition_cost"]) for r in task_rows),
                "composition_reused_on_new_task": bool(reuse_composed.success),
                "new_task_task_id": reuse_task.task_id,
                "new_task_reasoning_reduction": reuse_benefit if reuse_composed.success else 0.0,
                "new_task_baseline_cost": reuse_base.cost,
                "new_task_composition_cost": reuse_composed.cost,
                "task_results": task_rows,
                "single_skill_probe": single_after,
                "final_candidate": composition.to_dict(),
            }
        )
    return rows
