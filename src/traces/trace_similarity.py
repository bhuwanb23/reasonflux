"""Trace similarity — compare reasoning traces for clustering / transfer.

Two signals are combined:

- Jaccard over the *set* of canonical operations (does the trace use the same
  vocabulary at all?)
- Longest-common-subsequence ratio over the ordered sequence (does it use them
  in the same order?)

The set score dominates so that synonym spellings still match after
normalization, with sequence order as a tie-breaker.
"""

from __future__ import annotations

from difflib import SequenceMatcher

from core.trace import ReasoningTrace
from traces.normalizer import normalized_operations_for

__all__ = ["operation_set", "sequence_similarity", "trace_similarity"]


def operation_set(trace: ReasoningTrace) -> set[str]:
    """Canonical operation vocabulary of a trace."""
    return set(normalized_operations_for(trace))


def sequence_similarity(a: ReasoningTrace, b: ReasoningTrace) -> float:
    """Ordered similarity in [0, 1] via the longest matching block ratio."""
    left = normalized_operations_for(a)
    right = normalized_operations_for(b)
    if not left and not right:
        return 1.0
    if not left or not right:
        return 0.0
    return float(SequenceMatcher(a=left, b=right).ratio())


def trace_similarity(a: ReasoningTrace, b: ReasoningTrace) -> float:
    """Similarity in [0, 1]; 0.7 * set overlap + 0.3 * ordering."""
    left, right = operation_set(a), operation_set(b)
    if not left and not right:
        return 1.0
    union = left | right
    jaccard = len(left & right) / len(union) if union else 0.0
    return round(0.7 * jaccard + 0.3 * sequence_similarity(a, b), 6)
