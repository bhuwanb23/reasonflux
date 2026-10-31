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
) -> InvariantPipelineResult:
    """Mine invariants from traces (or a store) and validate them.

    ``attach_priors`` adds trace-derived SCT priors (see
    :mod:`invariants.sct_priors`) to the *validated* invariants only, so
    structural validation remains a pure IDT judgment.
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
            mean_len = _mean_trace_length(raw)
            families = {t.task_family for t in mining.normalized if t.task_family}
            attach_sct_priors(
                validation.validated,
                mean_trace_length=mean_len,
                n_families=len(families),
            )
            # Validated invariants are one legal hop short of SCT's input state;
            # advance them through the documented promotion path.
            for inv in validation.validated:
                advance_to_promotable(inv)
            validation.promotable = [
                inv
                for inv in validation.validated
                if inv.state is InvariantState.SKILL_CANDIDATE
            ]
    return InvariantPipelineResult(
        mining=mining, validation=validation, n_traces=len(raw)
    )


def _mean_trace_length(traces: Sequence[ReasoningTrace]) -> float:
    lengths = [len(t.steps) for t in traces if t.steps]
    return (sum(lengths) / len(lengths)) if lengths else 0.0
