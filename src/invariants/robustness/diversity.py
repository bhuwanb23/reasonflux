"""Task family diversity and multi-family requirements (F7)."""

from __future__ import annotations

from typing import Sequence

from core.invariant import Invariant
from core.task import Task
from invariants.robustness.config import RobustnessConfig
from invariants.robustness.metrics import compute_tfd


def compute_tfd_from_tasks(tasks: Sequence[Task]) -> float:
    """TFD from a task stream."""
    if not tasks:
        return 0.0
    families = {t.task_family for t in tasks if t.task_family}
    return compute_tfd(len(families), len(tasks))


def low_diversity_warning(
    tasks: Sequence[Task], config: RobustnessConfig | None = None
) -> bool:
    config = config or RobustnessConfig()
    return compute_tfd_from_tasks(tasks) < config.min_tfd


def meets_multi_family(
    invariant: Invariant, config: RobustnessConfig | None = None
) -> bool:
    """True when invariant has survived enough task families."""
    config = config or RobustnessConfig()
    families = invariant.task_families or []
    return len(set(families)) >= config.min_task_families_hard
