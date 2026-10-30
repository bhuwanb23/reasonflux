"""Pattern extraction and aggregation (Phase 11C-2 Stages 4–5).

Patterns are not invariants yet. Extraction finds recurring fragments;
aggregation groups similar patterns into shared structures.
"""

from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass, field
from typing import Iterable, Sequence

from traces.segmentation import TraceFragment

__all__ = [
    "AggregatedStructure",
    "MiningConfig",
    "MinedPattern",
    "aggregate_patterns",
    "extract_patterns",
    "longest_common_contiguous_subsequence",
    "mine_patterns",
    "patterns_share_core",
]


@dataclass(slots=True)
class MiningConfig:
    """Thresholds for the trace mining pipeline (Phase 11C-2)."""

    min_frequency: int = 3
    min_cross_trace: int = 2
    max_fragment_length: int = 4
    min_core_length: int = 2
    successful_trace_bias: bool = True

    def __post_init__(self) -> None:
        if self.min_frequency < 1:
            raise ValueError("min_frequency must be >= 1")
        if self.min_cross_trace < 1:
            raise ValueError("min_cross_trace must be >= 1")
        if self.max_fragment_length < 1:
            raise ValueError("max_fragment_length must be >= 1")
        if self.min_core_length < 1:
            raise ValueError("min_core_length must be >= 1")

    @classmethod
    def from_dict(cls, data: dict | None) -> MiningConfig:
        known = {f for f in cls.__dataclass_fields__}
        payload = {k: v for k, v in (data or {}).items() if k in known}
        return cls(**payload)


@dataclass(slots=True)
class MinedPattern:
    """A recurring fragment extracted across traces (not yet an invariant)."""

    pattern_id: str
    signature: tuple[str, ...]
    frequency: int = 0
    occurrences: int = 0
    trace_ids: list[str] = field(default_factory=list)
    success_count: int = 0
    failure_count: int = 0
    task_families: list[str] = field(default_factory=list)
    coverage: float = 0.0

    def __post_init__(self) -> None:
        if not self.pattern_id:
            raise ValueError("pattern_id must be non-empty")
        if not self.signature:
            raise ValueError("signature must not be empty")
        if self.frequency < 0:
            raise ValueError("frequency must be >= 0")
        if not 0.0 <= self.coverage <= 1.0:
            raise ValueError("coverage must be in [0, 1]")

    def to_dict(self) -> dict:
        return {
            "pattern_id": self.pattern_id,
            "signature": list(self.signature),
            "frequency": self.frequency,
            "occurrences": self.occurrences,
            "trace_ids": list(self.trace_ids),
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "task_families": list(self.task_families),
            "coverage": self.coverage,
        }


@dataclass(slots=True)
class AggregatedStructure:
    """A group of similar patterns representing one shared structure."""

    structure_id: str
    core: tuple[str, ...]
    representative: MinedPattern
    variants: list[MinedPattern] = field(default_factory=list)
    frequency: int = 0
    task_families: list[str] = field(default_factory=list)
    success_count: int = 0
    failure_count: int = 0
    occurrences: int = 0

    def to_dict(self) -> dict:
        return {
            "structure_id": self.structure_id,
            "core": list(self.core),
            "representative": self.representative.to_dict(),
            "variants": [v.to_dict() for v in self.variants],
            "frequency": self.frequency,
            "task_families": list(self.task_families),
            "success_count": self.success_count,
            "failure_count": self.failure_count,
            "occurrences": self.occurrences,
        }


def extract_patterns(
    fragments: Iterable[TraceFragment],
    *,
    total_traces: int,
    min_frequency: int = 3,
    min_cross_trace: int = 2,
) -> list[MinedPattern]:
    """Identify recurring fragments that meet mining constraints.

    Constraints:
    - frequency (distinct traces) >= min_frequency
    - distinct traces >= min_cross_trace (cannot occur in only one trace)
    """
    if total_traces < 0:
        raise ValueError("total_traces must be >= 0")
    if min_frequency < 1:
        raise ValueError("min_frequency must be >= 1")
    if min_cross_trace < 1:
        raise ValueError("min_cross_trace must be >= 1")

    by_sig: dict[tuple[str, ...], list[TraceFragment]] = defaultdict(list)
    for frag in fragments:
        by_sig[frag.signature].append(frag)

    patterns: list[MinedPattern] = []
    for index, (signature, items) in enumerate(sorted(by_sig.items()), start=1):
        trace_ids = sorted({f.trace_id for f in items if f.trace_id})
        frequency = len(trace_ids)
        if frequency < min_frequency or frequency < min_cross_trace:
            continue

        success_traces = {f.trace_id for f in items if f.success and f.trace_id}
        failure_traces = {f.trace_id for f in items if not f.success and f.trace_id}
        families = sorted({f.task_family for f in items if f.task_family})
        coverage = (frequency / total_traces) if total_traces > 0 else 0.0

        patterns.append(
            MinedPattern(
                pattern_id=f"P{index}",
                signature=signature,
                frequency=frequency,
                occurrences=len(items),
                trace_ids=trace_ids,
                success_count=len(success_traces),
                failure_count=len(failure_traces),
                task_families=families,
                coverage=coverage,
            )
        )

    patterns.sort(
        key=lambda p: (-p.frequency, -len(p.signature), p.signature, p.pattern_id)
    )
    # Re-assign stable pattern ids after sort for readability.
    for i, pattern in enumerate(patterns, start=1):
        pattern.pattern_id = f"P{i}"
    return patterns


def mine_patterns(
    fragments: Iterable[TraceFragment],
    *,
    total_traces: int,
    min_frequency: int = 3,
    min_cross_trace: int = 2,
) -> list[MinedPattern]:
    """Documented entry point for pattern extraction (delegates)."""
    return extract_patterns(
        fragments,
        total_traces=total_traces,
        min_frequency=min_frequency,
        min_cross_trace=min_cross_trace,
    )


def longest_common_contiguous_subsequence(
    a: Sequence[str], b: Sequence[str]
) -> tuple[str, ...]:
    """Longest contiguous subsequence shared by ``a`` and ``b``."""
    if not a or not b:
        return ()
    best: tuple[str, ...] = ()
    for i in range(len(a)):
        for length in range(1, len(a) - i + 1):
            sub = tuple(a[i : i + length])
            if length <= len(best):
                continue
            for j in range(len(b) - length + 1):
                if tuple(b[j : j + length]) == sub:
                    best = sub
                    break
    return best


def patterns_share_core(
    a: MinedPattern, b: MinedPattern, *, min_core_length: int = 2
) -> bool:
    """True when two patterns share a contiguous core of sufficient length."""
    core = longest_common_contiguous_subsequence(a.signature, b.signature)
    return len(core) >= min_core_length


def _select_representative(patterns: list[MinedPattern]) -> MinedPattern:
    return sorted(
        patterns,
        key=lambda p: (-p.frequency, -len(p.signature), p.signature, p.pattern_id),
    )[0]


def _structure_core(patterns: list[MinedPattern], min_core_length: int) -> tuple[str, ...]:
    """Pick the longest core shared by at least one pair; else the representative."""
    if len(patterns) == 1:
        return patterns[0].signature
    best: tuple[str, ...] = ()
    for i, left in enumerate(patterns):
        for right in patterns[i + 1 :]:
            core = longest_common_contiguous_subsequence(left.signature, right.signature)
            if len(core) >= min_core_length and len(core) > len(best):
                best = core
            elif len(core) == len(best) and core and (not best or core < best):
                best = core
    if best:
        return best
    return _select_representative(patterns).signature


def aggregate_patterns(
    patterns: Sequence[MinedPattern],
    *,
    min_core_length: int = 2,
) -> list[AggregatedStructure]:
    """Group similar patterns into shared structures via connected components.

    An edge exists between two patterns when they share a contiguous common
    subsequence of length >= ``min_core_length``.
    """
    items = list(patterns)
    if not items:
        return []

    n = len(items)
    parent = list(range(n))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(i: int, j: int) -> None:
        ri, rj = find(i), find(j)
        if ri != rj:
            parent[rj] = ri

    for i in range(n):
        for j in range(i + 1, n):
            if patterns_share_core(items[i], items[j], min_core_length=min_core_length):
                union(i, j)

    groups: dict[int, list[MinedPattern]] = defaultdict(list)
    for i, pattern in enumerate(items):
        groups[find(i)].append(pattern)

    structures: list[AggregatedStructure] = []
    for index, group in enumerate(sorted(groups.values(), key=lambda g: -len(g)), start=1):
        representative = _select_representative(group)
        all_trace_ids: set[str] = set()
        families: set[str] = set()
        success = 0
        failure = 0
        occurrences = 0
        for pattern in group:
            all_trace_ids.update(pattern.trace_ids)
            families.update(pattern.task_families)
            success += pattern.success_count
            failure += pattern.failure_count
            occurrences += pattern.occurrences

        # Unique-trace frequency for the structure (union of variant traces).
        frequency = len(all_trace_ids)
        # Recompute success/failure as unique traces across variants when possible.
        # Fall back to summed counters if trace sets are unavailable.
        success_ids: set[str] = set()
        failure_ids: set[str] = set()
        for pattern in group:
            # Approximate: if only successes, all its traces are successes.
            if pattern.failure_count == 0 and pattern.success_count == pattern.frequency:
                success_ids.update(pattern.trace_ids)
            elif pattern.success_count == 0 and pattern.failure_count == pattern.frequency:
                failure_ids.update(pattern.trace_ids)
            else:
                # Mixed — keep summed counters; unique success/failure unknown.
                success_ids.clear()
                failure_ids.clear()
                break
        if success_ids or failure_ids:
            success = len(success_ids)
            failure = len(failure_ids)

        structures.append(
            AggregatedStructure(
                structure_id=f"S{index}",
                core=_structure_core(group, min_core_length),
                representative=representative,
                variants=sorted(
                    group,
                    key=lambda p: (-p.frequency, -len(p.signature), p.signature),
                ),
                frequency=frequency,
                task_families=sorted(families),
                success_count=success,
                failure_count=failure,
                occurrences=occurrences,
            )
        )

    structures.sort(
        key=lambda s: (-s.frequency, -len(s.core), s.core, s.structure_id)
    )
    for i, structure in enumerate(structures, start=1):
        structure.structure_id = f"S{i}"
    return structures
