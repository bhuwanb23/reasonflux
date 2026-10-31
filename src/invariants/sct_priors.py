"""SCT prior evidence derived from trace statistics (Phase 11).

Mining deliberately leaves transfer and reasoning value at zero: those are
*claims about the future* that Phase D must verify by reusing the skill.

SCT still has to decide whether creating a skill is worth paying for, so it
needs a prior. This module supplies the smallest honest one, derived from
observed trace statistics only:

- ``reasoning_value``  = pattern length / mean trace length, i.e. the fraction of
  a trace the skill could replace.
- ``prior_transfer``   = cross-family support, i.e. how many observed task
  families the pattern already recurs in.

**Critical containment rule.** Priors are written to ``metadata`` ONLY. They are
never written into ``invariant.transfer_contribution``, because that field feeds
``Skill.transfer_score``, then CapU's TS term and Ig — which would let a trace
statistic be counted simultaneously as generality, transfer, TV and TS. Measured
transfer must come from Phase D, not from a prior.

Use :func:`prior_evidence` to read the values when building an SCV decision.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from core.invariant import Invariant

__all__ = ["SctPrior", "attach_sct_priors", "prior_evidence", "reasoning_value_prior"]


@dataclass(frozen=True, slots=True)
class SctPrior:
    """Trace-derived prior evidence for one invariant."""

    reasoning_value: float
    prior_transfer: float
    observed_families: int

    def to_dict(self) -> dict[str, float]:
        return {
            "reasoning_value": self.reasoning_value,
            "prior_transfer": self.prior_transfer,
            "observed_families": float(self.observed_families),
        }


def reasoning_value_prior(pattern_length: int, mean_trace_length: float) -> float:
    """Fraction of a trace the pattern could replace, clamped to [0, 1]."""
    if mean_trace_length <= 0:
        return 0.0
    return max(0.0, min(1.0, float(pattern_length) / float(mean_trace_length)))


def prior_evidence(invariant: Invariant) -> SctPrior:
    """Read the prior attached by :func:`attach_sct_priors`."""
    meta = invariant.metadata or {}
    return SctPrior(
        reasoning_value=float(meta.get("prior_reasoning_value", 0.0) or 0.0),
        prior_transfer=float(meta.get("prior_transfer", 0.0) or 0.0),
        observed_families=int(meta.get("prior_observed_families", 0) or 0),
    )


def attach_sct_priors(
    invariants: Sequence[Invariant],
    *,
    mean_trace_length: float,
    n_families: int,
    unverified_transfer: float = 0.0,
) -> list[Invariant]:
    """Attach trace-derived priors to ``metadata`` only.

    ``unverified_transfer`` controls what ``transfer_contribution`` becomes. By
    default it is left at 0.0 so no prior can ever reach a capability score.
    Passing a positive value is an explicit, documented opt-in for exploratory
    runs and must not be used for reported results.
    """
    families = max(1, int(n_families))
    for inv in invariants:
        meta = dict(inv.metadata or {})
        observed = len(set(inv.task_families or []))
        meta["prior_reasoning_value"] = meta.get(
            "prior_reasoning_value",
            reasoning_value_prior(len(inv.pattern_signature), mean_trace_length),
        )
        meta["prior_transfer"] = meta.get("prior_transfer", min(1.0, observed / families))
        meta["prior_observed_families"] = observed
        meta["transfer_verified"] = False
        inv.metadata = meta
        if inv.transfer_contribution <= 0.0:
            inv.transfer_contribution = float(unverified_transfer)
    return list(invariants)
