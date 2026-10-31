"""Structure aggregation over mined patterns (Phase 11C-2 Stage 5).

Split out of ``pattern_mining`` to keep every module within the 300-line budget.
Groups similar patterns into shared structures using connected components, where
an edge means the two patterns share a contiguous common core.
"""

from __future__ import annotations

from collections import defaultdict
from typing import Sequence

from invariants.pattern_mining import (
    AggregatedStructure,
    MinedPattern,
    longest_common_contiguous_subsequence,
    patterns_share_core,
)

__all__ = ["aggregate_patterns", "structure_core"]


def _select_representative(patterns: list[MinedPattern]) -> MinedPattern:
    return sorted(
        patterns,
        key=lambda p: (-p.frequency, -len(p.signature), p.signature, p.pattern_id),
    )[0]


def structure_core(
    patterns: list[MinedPattern], min_core_length: int
) -> tuple[str, ...]:
    """Longest core shared by at least one pair; else the representative."""
    if len(patterns) == 1:
        return patterns[0].signature
    best: tuple[str, ...] = ()
    for i, left in enumerate(patterns):
        for right in patterns[i + 1 :]:
            core = longest_common_contiguous_subsequence(
                left.signature, right.signature
            )
            if len(core) >= min_core_length and len(core) > len(best):
                best = core
            elif len(core) == len(best) and core and (not best or core < best):
                best = core
    return best or _select_representative(patterns).signature


def _unique_outcome_counts(group: list[MinedPattern]) -> tuple[int, int] | None:
    """Unique success/failure trace counts, or ``None`` when a pattern is mixed."""
    success_ids: set[str] = set()
    failure_ids: set[str] = set()
    for pattern in group:
        pure_success = (
            pattern.failure_count == 0 and pattern.success_count == pattern.frequency
        )
        pure_failure = (
            pattern.success_count == 0 and pattern.failure_count == pattern.frequency
        )
        if pure_success:
            success_ids.update(pattern.trace_ids)
        elif pure_failure:
            failure_ids.update(pattern.trace_ids)
        else:
            return None
    return len(success_ids), len(failure_ids)


def aggregate_patterns(
    patterns: Sequence[MinedPattern],
    *,
    min_core_length: int = 2,
) -> list[AggregatedStructure]:
    """Group similar patterns into shared structures via connected components."""
    items = list(patterns)
    if not items:
        return []

    parent = list(range(len(items)))

    def find(i: int) -> int:
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if not patterns_share_core(
                items[i], items[j], min_core_length=min_core_length
            ):
                continue
            root_i, root_j = find(i), find(j)
            if root_i != root_j:
                parent[root_j] = root_i

    groups: dict[int, list[MinedPattern]] = defaultdict(list)
    for i, pattern in enumerate(items):
        groups[find(i)].append(pattern)

    structures: list[AggregatedStructure] = []
    for group in sorted(groups.values(), key=len, reverse=True):
        trace_ids: set[str] = set()
        families: set[str] = set()
        success = failure = occurrences = 0
        for pattern in group:
            trace_ids.update(pattern.trace_ids)
            families.update(pattern.task_families)
            success += pattern.success_count
            failure += pattern.failure_count
            occurrences += pattern.occurrences

        unique = _unique_outcome_counts(group)
        if unique is not None:
            success, failure = unique

        structures.append(
            AggregatedStructure(
                structure_id="",
                core=structure_core(group, min_core_length),
                representative=_select_representative(group),
                variants=sorted(
                    group,
                    key=lambda p: (-p.frequency, -len(p.signature), p.signature),
                ),
                frequency=len(trace_ids),
                task_families=sorted(families),
                success_count=success,
                failure_count=failure,
                occurrences=occurrences,
            )
        )

    structures.sort(
        key=lambda s: (-s.frequency, -len(s.core), s.core, s.representative.pattern_id)
    )
    for i, structure in enumerate(structures, start=1):
        structure.structure_id = f"S{i}"
    return structures
