"""Baseline A — no learning: solve every task independently, reuse nothing."""

from __future__ import annotations

from skills.library import SkillLibrary
from solver.executor import GridSolver
from solver.tasks import FAMILIES, make_task_batch

from baselines._common import eval_tasks_for, measure_library

__all__ = ["run"]

NAME = "no_learning"


def run(*, seed: int = 100, per_family: int = 2, difficulty: float = 0.2) -> dict:
    """Empty library, measured with the same instrument as the full pipeline."""
    solver = GridSolver()
    tasks = make_task_batch(
        FAMILIES, per_family=per_family, seed=seed, difficulty=difficulty
    )
    solved = [solver.solve(t) for t in tasks]
    accuracy = sum(1 for s in solved if s.success) / len(solved) if solved else 0.0
    mean_cost = sum(s.cost for s in solved) / len(solved) if solved else 0.0

    result = measure_library(NAME, SkillLibrary(), tasks=eval_tasks_for(seed=seed))
    result.metadata.update(
        {"accuracy": round(accuracy, 4), "mean_cost": round(mean_cost, 4)}
    )
    return result.to_dict()
