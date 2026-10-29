"""Skill lifecycle management — Phase 11D-3."""

from skills.lifecycle.aging import (
    last_used_index,
    note_task_tick,
    recency_weight,
    tasks_since_use,
)
from skills.lifecycle.apply import apply_lifecycle, evaluate_lifecycle
from skills.lifecycle.biography import append_biography_event, build_biography
from skills.lifecycle.health import HealthScore, apply_recency, compute_health
from skills.lifecycle.metrics import LifecycleMetrics, compute_lifecycle_metrics
from skills.lifecycle.policy import LifecycleDecision, decide_lifecycle
from skills.lifecycle.sweep import LibraryLifecycleResult, evaluate_library_lifecycle

__all__ = [
    "HealthScore",
    "LibraryLifecycleResult",
    "LifecycleDecision",
    "LifecycleMetrics",
    "append_biography_event",
    "apply_lifecycle",
    "apply_recency",
    "build_biography",
    "compute_health",
    "compute_lifecycle_metrics",
    "decide_lifecycle",
    "evaluate_library_lifecycle",
    "evaluate_lifecycle",
    "last_used_index",
    "note_task_tick",
    "recency_weight",
    "tasks_since_use",
]
