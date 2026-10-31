"""Invariant pipeline — traces → candidates → ranked/promotable (Phase 11, B).

Composes the existing 11C-2 miner and 11C-3 validator; adds no new logic. The
only novel part is that it accepts a ``TraceStore`` so Phase B can start from
persisted experience rather than an in-memory list.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from core.invariant import Invariant
from core.states import InvariantState
from core.trace import ReasoningTrace
from invariants.detector import MiningConfig, MiningResult, TraceMiner
from invariants.promotion import advance_to_promotable
from invariants.sct_priors import attach_sct_priors
from invariants.validator import ValidationResult, validate_and_rank
from traces.trace_store import TraceStore

__all__ = ["InvariantPipelineResult", "run_invariant_pipeline"]


@dataclass(slots=True)
class InvariantPipelineResult:
    """Mining plus validation outputs."""

    mining: MiningResult | None = None
    validation: ValidationResult | None = None
    n_traces: int = 0

    @property
    def candidates(self) -> list[Invariant]:
        return list(self.mining.candidates) if self.mining else []

    @property
    def promotable(self) -> list[Invariant]:
        return list(self.validation.promotable) if self.validation else []

    def to_dict(self) -> dict[str, Any]:
        return {
            "n_traces": self.n_traces,
            "mining": self.mining.to_dict() if self.mining else None,
            "validation": self.validation.to_dict() if self.validation else None,
            "n_candidates": len(self.candidates),
            "n_promotable": len(self.promotable),
        }


def run_invariant_pipeline(
    traces: Sequence[ReasoningTrace] | TraceStore | None = None,
    *,
    mining_config: MiningConfig | None = None,
    transfer_scores: dict[str, float] | None = None,
    validate: bool = True,
    attach_priors: bool = True,
    bootstrap: bool = False,
) -> InvariantPipelineResult:
    """Mine invariants from traces (or a store) and validate them.

    ``attach_priors`` adds trace-derived SCT priors to ``metadata`` only, so
    structural validation remains a pure IDT judgment.

    ``bootstrap`` optionally advances *validated* invariants to the SCT input
    state when no invariant could satisfy the transfer/reasoning gates from
    mining alone. Mining cannot supply transfer evidence by construction, so
    without this bootstrap Phase C would have nothing to trial and the system
    could never measure transfer. Bootstrapped invariants are admitted only as
    provisional skills (see ``allow_prior_evidence``) and never enter the
    capability portfolio until Phase D measures them.
    """
    if isinstance(traces, TraceStore):
        raw = traces.load_all()
    else:
        raw = list(traces or [])
    if not raw:
        return InvariantPipelineResult(
            mining=MiningResult(), validation=None, n_traces=0
        )

    miner = TraceMiner(mining_config or MiningConfig())
    mining = miner.mine(raw)

    validation = None
    if validate:
        validation = validate_and_rank(
            mining.candidates, transfer_scores=transfer_scores
        )
        if attach_priors:
            families = {t.task_family for t in mining.normalized if t.task_family}
            attach_sct_priors(
                validation.validated,
                mean_trace_length=_mean_trace_length(raw),
                n_families=len(families),
            )
        if bootstrap and not validation.promotable:
            validation.promotable = _bootstrap_promotable(validation)
    return InvariantPipelineResult(
        mining=mining, validation=validation, n_traces=len(raw)
    )


def _bootstrap_promotable(validation: ValidationResult) -> list[Invariant]:
    """Advance structurally validated invariants to the SCT input state.

    Records that this happened in metadata so downstream code and reports can
    distinguish a bootstrapped trial from an evidence-qualified promotion.
    """
    out: list[Invariant] = []
    for inv in validation.validated:
        if inv.state is InvariantState.SKILL_CANDIDATE:
            out.append(inv)
            continue
        advance_to_promotable(inv)
        inv.metadata = dict(inv.metadata or {})
        inv.metadata["bootstrapped"] = True
        out.append(inv)
    return out


def _mean_trace_length(traces: Sequence[ReasoningTrace]) -> float:
    lengths = [len(t.steps) for t in traces if t.steps]
    return (sum(lengths) / len(lengths)) if lengths else 0.0
