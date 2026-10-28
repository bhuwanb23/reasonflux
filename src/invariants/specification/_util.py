"""Shared helpers for the invariant specification package."""

from __future__ import annotations

from core.invariant import Invariant


def family_set(invariant: Invariant) -> set[str]:
    """Distinct non-empty task families from invariant + evidence."""
    families = set(invariant.task_families) | set(invariant.evidence.task_families)
    return {f for f in families if f}
