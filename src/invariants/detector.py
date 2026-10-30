"""Invariant Detector / Trace Miner — Phase 11C-2 orchestration.

Six-stage pipeline:
Trace Collection → Normalization → Segmentation → Pattern Extraction
→ Pattern Aggregation → Candidate Generation

Boundary (must NOT): create skills, rank transfer, decide promotion,
manage memory, or compute CGR.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, Sequence

from core.invariant import Invariant
from core.trace import ReasoningTrace
from invariants.candidate_generation import (
    CandidateGenerationResult,
    generate_candidates,
)
from invariants.pattern_mining import (
    AggregatedStructure,
    MiningConfig,
    MinedPattern,
    aggregate_patterns,
    extract_patterns,
)
from invariants.specification import InvariantPolicy
from traces.normalizer import NormalizedTrace, normalize_traces
from traces.segmentation import TraceFragment, segment_traces

__all__ = [
    "InvariantDetector",
    "MiningResult",
    "MiningStatistics",
    "TraceMiner",
]


@dataclass(slots=True)
class MiningStatistics:
    """Counts produced by a mining run."""

    traces_in: int = 0
    traces_success: int = 0
    traces_failure: int = 0
    fragments: int = 0
    raw_patterns: int = 0
    structures: int = 0
    candidates: int = 0
    rejected: int = 0

    def to_dict(self) -> dict:
        return {
            "traces_in": self.traces_in,
            "traces_success": self.traces_success,
            "traces_failure": self.traces_failure,
            "fragments": self.fragments,
            "raw_patterns": self.raw_patterns,
            "structures": self.structures,
            "candidates": self.candidates,
            "rejected": self.rejected,
        }


@dataclass(slots=True)
class MiningResult:
    """Full outputs of the Phase 11C-2 mining pipeline."""

    success_patterns: list[MinedPattern] = field(default_factory=list)
    failure_patterns: list[MinedPattern] = field(default_factory=list)
    structures: list[AggregatedStructure] = field(default_factory=list)
    candidates: list[Invariant] = field(default_factory=list)
    rejected: list[tuple[Invariant, list[str]]] = field(default_factory=list)
    statistics: MiningStatistics = field(default_factory=MiningStatistics)
    normalized: list[NormalizedTrace] = field(default_factory=list)

    def to_dict(self) -> dict:
        return {
            "success_patterns": [p.to_dict() for p in self.success_patterns],
            "failure_patterns": [p.to_dict() for p in self.failure_patterns],
            "structures": [s.to_dict() for s in self.structures],
            "candidates": [c.to_dict() for c in self.candidates],
            "rejected": [
                {"invariant": inv.to_dict(), "reasons": list(reasons)}
                for inv, reasons in self.rejected
            ],
            "statistics": self.statistics.to_dict(),
        }


class TraceMiner:
    """Six-stage trace mining orchestrator (Phase 11C-2)."""

    def __init__(
        self,
        config: MiningConfig | None = None,
        policy: InvariantPolicy | None = None,
    ) -> None:
        self.config = config or MiningConfig()
        self.policy = policy or InvariantPolicy()

    def mine(
        self,
        traces: Sequence[ReasoningTrace] | object,
    ) -> MiningResult:
        """Run the full mining pipeline.

        ``traces`` may be a sequence of ``ReasoningTrace`` or any object
        implementing ``get_traces()`` (``TraceBatchProvider``).
        """
        raw = _coerce_traces(traces)

        # Stage 1 — collection (already provided) / Stage 2 — normalization
        normalized = normalize_traces(raw)
        success_traces = [t for t in normalized if t.success]
        failure_traces = [t for t in normalized if not t.success]

        # Stage 3 — segmentation
        success_frags = segment_traces(
            success_traces,
            max_length=self.config.max_fragment_length,
        )
        failure_frags = segment_traces(
            failure_traces,
            max_length=self.config.max_fragment_length,
        )

        # Stage 4 — pattern extraction (success and failure separately)
        success_patterns = extract_patterns(
            success_frags,
            total_traces=len(success_traces) if success_traces else len(normalized),
            min_frequency=self.config.min_frequency,
            min_cross_trace=self.config.min_cross_trace,
        )
        failure_patterns = extract_patterns(
            failure_frags,
            total_traces=len(failure_traces) if failure_traces else 0,
            min_frequency=self.config.min_frequency,
            min_cross_trace=self.config.min_cross_trace,
        )

        # Stage 5 — aggregation (structures from success patterns by default)
        primary_patterns = (
            success_patterns if self.config.successful_trace_bias else success_patterns + failure_patterns
        )
        # When bias is on but no success patterns, fall back to all.
        if self.config.successful_trace_bias and not primary_patterns:
            primary_patterns = failure_patterns

        structures = aggregate_patterns(
            primary_patterns, min_core_length=self.config.min_core_length
        )

        # Stage 6 — candidate generation
        families = {t.task_family for t in normalized if t.task_family}
        generation = generate_candidates(
            structures,
            total_families=max(len(families), 1),
            policy=self.policy,
        )

        stats = MiningStatistics(
            traces_in=len(normalized),
            traces_success=len(success_traces),
            traces_failure=len(failure_traces),
            fragments=len(success_frags) + len(failure_frags),
            raw_patterns=len(success_patterns) + len(failure_patterns),
            structures=len(structures),
            candidates=len(generation.candidates),
            rejected=len(generation.rejected),
        )
        return MiningResult(
            success_patterns=success_patterns,
            failure_patterns=failure_patterns,
            structures=structures,
            candidates=generation.candidates,
            rejected=generation.rejected,
            statistics=stats,
            normalized=normalized,
        )


class InvariantDetector:
    """Discover and validate invariants from reasoning traces.

    Phase 11C-2: ``detect`` / ``mine`` produce candidates.
    Phase 11C-3: ``validate`` / ``detect_and_validate`` rank and promote.
    """

    def __init__(
        self,
        config: MiningConfig | None = None,
        policy: InvariantPolicy | None = None,
        validation_config: object | None = None,
    ) -> None:
        self.miner = TraceMiner(config=config, policy=policy)
        self.policy = policy
        self.validation_config = validation_config

    def detect(self, traces: Sequence[ReasoningTrace] | object) -> list[Invariant]:
        """Return invariant candidates mined from ``traces``."""
        return self.miner.mine(traces).candidates

    def mine(self, traces: Sequence[ReasoningTrace] | object) -> MiningResult:
        """Return the full mining result (patterns, structures, candidates)."""
        return self.miner.mine(traces)

    def validate(
        self,
        candidates: Sequence[Invariant],
        *,
        transfer_scores: dict[str, float] | None = None,
    ):
        """Rank and promote candidate invariants (Phase 11C-3)."""
        from invariants.validator import validate_and_rank

        return validate_and_rank(
            candidates,
            config=self.validation_config,  # type: ignore[arg-type]
            transfer_scores=transfer_scores,
            policy=self.policy,
        )

    def detect_and_validate(
        self,
        traces: Sequence[ReasoningTrace] | object,
        *,
        transfer_scores: dict[str, float] | None = None,
    ):
        """Mine candidates then validate/rank them end-to-end."""
        return self.validate(self.detect(traces), transfer_scores=transfer_scores)


def _coerce_traces(traces: Sequence[ReasoningTrace] | object) -> list[ReasoningTrace]:
    if hasattr(traces, "get_traces") and callable(traces.get_traces):
        return list(traces.get_traces())
    if isinstance(traces, (list, tuple)):
        return list(traces)
    if isinstance(traces, Iterable) and not isinstance(traces, (str, bytes)):
        return list(traces)
    raise TypeError(
        "traces must be a sequence of ReasoningTrace or a TraceBatchProvider"
    )
