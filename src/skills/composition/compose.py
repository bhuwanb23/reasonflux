"""Orchestrator: try_compose end-to-end (Phase 11D-4)."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from core.skill import Skill
from skills.composition.evaluate import record_composition_outcome
from skills.composition.graph import CompositionGraph
from skills.composition.lifecycle import advance_composition, promote_composition
from skills.composition.models import CompositionCandidate, CompositionState
from skills.composition.propose import propose_sequential
from skills.composition.trigger import ComposeTriggerResult, should_compose
from skills.config import SkillConfig
from skills.library import SkillLibrary
from skills.retrieval import retrieve_skills


@dataclass(slots=True)
class ComposeOutcome:
    """Synthetic or observed outcome applied to each tried candidate."""

    success: bool = True
    transfer_gain: float = 0.2
    reasoning_reduction: float = 0.2
    task_family: str = ""


@dataclass(slots=True)
class ComposeResult:
    """Result of one try_compose pass."""

    triggered: bool
    trigger: ComposeTriggerResult | None = None
    candidates: list[CompositionCandidate] = field(default_factory=list)
    kept: list[CompositionCandidate] = field(default_factory=list)
    discarded: list[CompositionCandidate] = field(default_factory=list)
    promoted: list[Skill] = field(default_factory=list)
    graph: CompositionGraph | None = None
    metrics: dict[str, Any] = field(default_factory=dict)
    reasons: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        return {
            "triggered": self.triggered,
            "trigger": self.trigger.to_dict() if self.trigger else None,
            "candidates": [c.to_dict() for c in self.candidates],
            "kept": [c.to_dict() for c in self.kept],
            "discarded": [c.to_dict() for c in self.discarded],
            "promoted": [s.skill_id for s in self.promoted],
            "graph": self.graph.to_dict() if self.graph else None,
            "metrics": dict(self.metrics),
            "reasons": list(self.reasons),
        }


def _metrics(cands: Sequence[CompositionCandidate]) -> dict[str, Any]:
    if not cands:
        return {"cu": 0.0, "cr": 0.0, "ct": 0.0, "cc": 0.0, "ncr": 0.0}
    cus = [float(c.cu) for c in cands]
    reuses = [int((c.evidence or {}).get("uses", 0) or 0) for c in cands]
    transfers = [
        len((c.evidence or {}).get("transfer_events") or []) for c in cands
    ]
    confs = [float(c.confidence) for c in cands]
    ncrs = [float(c.ncr) for c in cands]
    n = len(cands)
    return {
        "cu": sum(cus) / n,
        "cr": sum(reuses) / n,
        "ct": sum(transfers) / n,
        "cc": sum(confs) / n,
        "ncr": sum(ncrs) / n,
    }


def try_compose(
    library: SkillLibrary,
    requirements: Sequence[str],
    *,
    config: SkillConfig | None = None,
    graph: CompositionGraph | None = None,
    outcome: ComposeOutcome | None = None,
    max_apply: int = 1,
    registry: dict[str, CompositionCandidate] | None = None,
) -> ComposeResult:
    """Gate → propose → evaluate (optional) → advance / promote → graph update.

    Pass a persistent ``registry`` keyed by composition_id to accumulate
    evidence across calls (experiments / e2e).
    """
    config = config or SkillConfig()
    graph = graph or CompositionGraph()
    registry = registry if registry is not None else {}
    skills = retrieve_skills(library, config=config)
    trigger = should_compose(requirements, skills, config)
    if not trigger.should_compose:
        return ComposeResult(
            triggered=False,
            trigger=trigger,
            graph=graph,
            reasons=list(trigger.reasons),
        )

    proposed = propose_sequential(library, requirements, config, skills=skills)
    # Merge with registry so reuse evidence persists across try_compose calls.
    merged: list[CompositionCandidate] = []
    for fresh in proposed:
        existing = registry.get(fresh.composition_id)
        if existing is not None and existing.state is not CompositionState.DISCARDED:
            merged.append(existing)
        else:
            registry[fresh.composition_id] = fresh
            merged.append(fresh)

    result = ComposeResult(
        triggered=True,
        trigger=trigger,
        candidates=list(merged),
        graph=graph,
        reasons=["composed"],
    )
    if not merged:
        result.reasons = ["no_viable_candidates"]
        return result

    apply_n = max(0, min(int(max_apply), len(merged)))
    for cand in merged[:apply_n]:
        if outcome is not None:
            record_composition_outcome(
                cand,
                success=outcome.success,
                transfer_gain=outcome.transfer_gain,
                reasoning_reduction=outcome.reasoning_reduction,
                task_family=outcome.task_family,
                config=config,
            )
        advance_composition(cand, config)
        if (
            outcome is not None
            and outcome.success
            and cand.state is not CompositionState.DISCARDED
        ):
            graph.record_success(cand.order)
        promoted = promote_composition(cand, library, config)
        if promoted is not None:
            result.promoted.append(promoted)
        if cand.state is CompositionState.DISCARDED:
            result.discarded.append(cand)
        elif cand.state in (
            CompositionState.VALIDATED,
            CompositionState.REUSABLE,
            CompositionState.PROMOTED,
        ):
            result.kept.append(cand)
        registry[cand.composition_id] = cand

    result.metrics = _metrics(merged[:apply_n] or merged)
    result.graph = graph
    return result
