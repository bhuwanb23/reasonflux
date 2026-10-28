"""Trace segmentation — mine fragments, not whole traces (Phase 11C-2 Stage 3).

Skills emerge from substructures. Contiguous n-grams of length 1..max_length
increase discovery power over whole-trace matching.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Sequence

from traces.normalizer import NormalizedTrace

__all__ = [
    "TraceFragment",
    "segment_trace",
    "segment_traces",
]


@dataclass(slots=True)
class TraceFragment:
    """A contiguous operation subsequence extracted from a normalized trace."""

    signature: tuple[str, ...]
    source_index: int
    trace_id: str = ""
    task_id: str = ""
    task_family: str = ""
    success: bool = True

    def __post_init__(self) -> None:
        if not self.signature:
            raise ValueError("signature must not be empty")
        if self.source_index < 0:
            raise ValueError("source_index must be >= 0")

    @property
    def length(self) -> int:
        return len(self.signature)

    def to_dict(self) -> dict:
        return {
            "signature": list(self.signature),
            "source_index": self.source_index,
            "trace_id": self.trace_id,
            "task_id": self.task_id,
            "task_family": self.task_family,
            "success": self.success,
            "length": self.length,
        }


def segment_trace(
    operations: Sequence[str],
    *,
    max_length: int = 4,
    min_length: int = 1,
    trace_id: str = "",
    task_id: str = "",
    task_family: str = "",
    success: bool = True,
    dedupe: bool = True,
) -> list[TraceFragment]:
    """Extract contiguous n-gram fragments from an operation sequence.

    When ``dedupe`` is True, identical signatures within one trace are kept
    once (first occurrence), so frequency counts distinct traces.
    """
    if max_length < 1:
        raise ValueError("max_length must be >= 1")
    if min_length < 1:
        raise ValueError("min_length must be >= 1")
    if min_length > max_length:
        raise ValueError("min_length must be <= max_length")

    ops = [str(op) for op in operations if str(op).strip()]
    if not ops:
        return []

    fragments: list[TraceFragment] = []
    seen: set[tuple[str, ...]] = set()
    upper = min(max_length, len(ops))
    for length in range(min_length, upper + 1):
        for start in range(0, len(ops) - length + 1):
            signature = tuple(ops[start : start + length])
            if dedupe and signature in seen:
                continue
            if dedupe:
                seen.add(signature)
            fragments.append(
                TraceFragment(
                    signature=signature,
                    source_index=start,
                    trace_id=trace_id,
                    task_id=task_id,
                    task_family=task_family,
                    success=success,
                )
            )
    return fragments


def segment_traces(
    traces: Iterable[NormalizedTrace],
    *,
    max_length: int = 4,
    min_length: int = 1,
    dedupe: bool = True,
) -> list[TraceFragment]:
    """Segment a batch of normalized traces into fragments."""
    fragments: list[TraceFragment] = []
    for trace in traces:
        fragments.extend(
            segment_trace(
                trace.operations,
                max_length=max_length,
                min_length=min_length,
                trace_id=trace.trace_id,
                task_id=trace.task_id,
                task_family=trace.task_family,
                success=trace.success,
                dedupe=dedupe,
            )
        )
    return fragments
