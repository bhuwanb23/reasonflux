"""SCT prior evidence derived from trace statistics (Phase 11).

Mining deliberately leaves transfer and reasoning value at zero: those are
*claims about the future* that Phase D must verify by actually reusing the
skill. But SCT has to decide whether to create a skill at all, and that
decision needs a prior.

This module derives the smallest honest prior from observed data only:

- ``reasoning_value`` = pattern length / mean trace length, i.e. the fraction of
  a trace the skill could replace.
- ``transfer_contribution`` = cross-family support, i.e. how many of the
  observed task families the pattern already recurs in.

Neither is allowed to invent signal. Both are recomputed from the mined
corpus, and Phase D overwrites them with measured values.
"""

from __future__ import annotations

from typing import Sequence

from core.invariant import Invariant

__all__ = ["attach_sct_priors", "reasoning_value_prior"]


def reasoning_value_prior(pattern_length: int, mean_trace_length: float) -> float:
    """Fraction of a trace the pattern could replace, clamped to [0, 1]."""
    if mean_trace_length <= 0:
        return 0.0
    return max(0.0, min(1.0, float(pattern_length) / float(mean_trace_length)))


def attach_sct_priors(
    invariants: Sequence[Invariant],
    *,
    mean_trace_length: float,
    n_families: int,
) -> list[Invariant]:
    """Attach trace-derived priors so SCT can evaluate SCV.

    Existing non-zero values are preserved: a measured transfer score must never
    be overwritten by a prior.
    """
    families = max(1, int(n_families))
    for inv in invariants:
        meta = dict(inv.metadata or {})
        if "reasoning_value" not in meta:
            meta["reasoning_value"] = reasoning_value_prior(
                len(inv.pattern_signature), mean_trace_length
            )
        if inv.transfer_contribution <= 0.0:
            observed = len(set(inv.task_families or meta.get("task_families") or []))
            inv.transfer_contribution = min(1.0, observed / families)
            meta["transfer_prior"] = inv.transfer_contribution
            meta["transfer_verified"] = False
        inv.metadata = meta
    return list(invariants)
