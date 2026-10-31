"""Trace normalizer — align step types for mining (Phase 11C-2 Stage 2).

Without normalization, the same reasoning idea can appear as different
raw operation strings. Canonicalization reduces representation noise.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Mapping

from core.trace import ReasoningTrace

__all__ = [
    "DEFAULT_SYNONYM_MAP",
    "NormalizedTrace",
    "canonicalize_operation",
    "normalize_lookup_key",
    "normalize_trace",
    "normalize_traces",
    "normalized_operations_for",
]

# Lookup keys are lowercase alphanumeric only (punctuation stripped).
DEFAULT_SYNONYM_MAP: dict[str, str] = {
    "locateobject": "detect_object",
    "detectobject": "detect_object",
    "detect": "detect_object",
    "findmirroraxis": "find_symmetry",
    "findsymmetry": "find_symmetry",
    "findsym": "find_symmetry",
    "reflect": "apply_reflection",
    "applyreflection": "apply_reflection",
    "reflection": "apply_reflection",
    "findrotation": "find_rotation",
    "applyrotation": "apply_rotation",
    "rotate": "apply_rotation",
    "verify": "verify_output",
    "verifyoutput": "verify_output",
    "check": "verify_output",
    "count": "count_objects",
    "countobjects": "count_objects",
}


@dataclass(slots=True)
class NormalizedTrace:
    """Canonical form of a reasoning trace for mining."""

    trace_id: str
    task_id: str
    task_family: str
    operations: list[str] = field(default_factory=list)
    success: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def step_count(self) -> int:
        return len(self.operations)

    def to_dict(self) -> dict[str, Any]:
        return {
            "trace_id": self.trace_id,
            "task_id": self.task_id,
            "task_family": self.task_family,
            "operations": list(self.operations),
            "success": self.success,
            "step_count": self.step_count,
            "metadata": dict(self.metadata),
        }


def normalize_lookup_key(name: str) -> str:
    """Lowercase and strip non-alphanumeric characters for synonym lookup."""
    return re.sub(r"[^a-z0-9]", "", str(name).lower())


def canonicalize_operation(
    name: str, synonym_map: Mapping[str, str] | None = None
) -> str:
    """Map a raw operation name to its canonical form.

    Unmapped names pass through as lowercase with spaces/hyphens as
    underscores (snake_case-ish), preserving readability.
    """
    mapping = synonym_map if synonym_map is not None else DEFAULT_SYNONYM_MAP
    key = normalize_lookup_key(name)
    if key in mapping:
        return mapping[key]
    # Pass-through: normalize separators without synonym rewrite.
    cleaned = re.sub(r"[\s\-]+", "_", str(name).strip().lower())
    cleaned = re.sub(r"_+", "_", cleaned).strip("_")
    return cleaned or str(name).strip().lower()


def _resolve_task_family(trace: ReasoningTrace) -> str:
    """Resolve task family without seeing a raw Task object (Contract 1)."""
    family = trace.metadata.get("task_family") if trace.metadata else None
    if family and str(family).strip():
        return str(family).strip()
    return trace.task_id


def normalize_trace(
    trace: ReasoningTrace,
    synonym_map: Mapping[str, str] | None = None,
) -> NormalizedTrace:
    """Normalize a ReasoningTrace into a canonical operation sequence."""
    operations = [
        canonicalize_operation(step.operation, synonym_map) for step in trace.steps
    ]
    success = True if trace.outcome is None else bool(trace.outcome.success)
    return NormalizedTrace(
        trace_id=trace.trace_id,
        task_id=trace.task_id,
        task_family=_resolve_task_family(trace),
        operations=operations,
        success=success,
        metadata=dict(trace.metadata or {}),
    )


def normalize_traces(
    traces: list[ReasoningTrace],
    synonym_map: Mapping[str, str] | None = None,
) -> list[NormalizedTrace]:
    """Normalize a batch of traces."""
    return [normalize_trace(t, synonym_map) for t in traces]


def normalized_operations_for(
    trace: ReasoningTrace,
    synonym_map: Mapping[str, str] | None = None,
) -> list[str]:
    """Canonical operation sequence for one trace (order preserved)."""
    return [
        canonicalize_operation(step.operation, synonym_map) for step in trace.steps
    ]
