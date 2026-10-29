"""Aging, recency weight, and tasks-since-use (Phase 11D-3)."""

from __future__ import annotations

import math
from typing import Any

from core.skill import Skill
from skills.config import SkillConfig


def _event_index(event: dict[str, Any]) -> int | None:
    for key in ("task_index", "task_clock", "timestamp", "t"):
        if key in event and event[key] is not None:
            try:
                return int(event[key])
            except (TypeError, ValueError):
                continue
    return None


def last_used_index(skill: Skill) -> int:
    """Latest task index from reuse_history / transfer_history (else 0)."""
    indices: list[int] = []
    for event in list(skill.reuse_history or []) + list(skill.transfer_history or []):
        if isinstance(event, dict):
            idx = _event_index(event)
            if idx is not None:
                indices.append(idx)
    meta = skill.metadata or {}
    birth = meta.get("birth_task")
    if birth is not None:
        try:
            indices.append(int(birth))
        except (TypeError, ValueError):
            pass
    return max(indices) if indices else 0


def recency_weight(t: float, config: SkillConfig | None = None) -> float:
    """RW = exp(−λ · t) with t = tasks since last use."""
    config = config or SkillConfig()
    t = max(0.0, float(t))
    return float(math.exp(-float(config.decay_lambda) * t))


def tasks_since_use(skill: Skill, task_clock: int | None = None) -> int:
    """Read metadata lifecycle counter, or derive from task_clock."""
    life = dict((skill.metadata or {}).get("lifecycle") or {})
    if "tasks_since_use" in life:
        try:
            return max(0, int(life["tasks_since_use"]))
        except (TypeError, ValueError):
            pass
    if task_clock is None:
        return 0
    last = last_used_index(skill)
    return max(0, int(task_clock) - last)


def note_task_tick(
    skill: Skill, *, used: bool = False, task_clock: int | None = None
) -> int:
    """Increment tasks_since_use (reset to 0 when used). Returns new value."""
    meta = dict(skill.metadata or {})
    life = dict(meta.get("lifecycle") or {})
    if used:
        life["tasks_since_use"] = 0
        if task_clock is not None:
            life["last_used_clock"] = int(task_clock)
    else:
        prev = int(life.get("tasks_since_use", 0) or 0)
        life["tasks_since_use"] = prev + 1
    meta["lifecycle"] = life
    skill.metadata = meta
    return int(life["tasks_since_use"])
