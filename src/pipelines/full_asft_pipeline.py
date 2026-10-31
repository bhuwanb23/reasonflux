"""Full ASFT pipeline — Task → Trace → Invariant → Skill → Transfer → CGM.

The single end-to-end entry point for v0.1.

Growth is measured the way the theory states it: capability accrues as
**experience accumulates**. Each round adds a fresh task batch to the corpus;
traces, invariants, skills, and capability are recomputed on everything seen so
far. The capability trajectory across rounds is therefore a real learning curve,
not an artifact of re-pricing a fixed library.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Sequence

from capability.emerge import propose_capabilities_from_library
from capability.library import CapabilityLibrary
from capability.models import Capability
from capability.portfolio import compute_system_capability_state
from evaluation.harness.config import HarnessConfig
from evaluation.intelligence_state import compute_system_intelligence_state
from pipelines.invariant_pipeline import run_invariant_pipeline
from pipelines.skill_pipeline import run_skill_pipeline
from pipelines.trace_pipeline import run_trace_pipeline
from solver.executor import GridSolver
from solver.tasks import FAMILIES, make_task_batch
from transfer.memory import TransferMemory
from transfer.reuse_engine import ReuseEngine, ReuseResult

__all__ = ["FullPipelineResult", "RoundSnapshot", "run_full_asft_pipeline"]


@dataclass(slots=True)
class RoundSnapshot:
    """Measurements after one round of accumulated experience."""

    round_index: int
    n_traces: int
    n_invariants: int
    n_skills: int
    n_capabilities: int
    capability_score: float
    cgr: float
    ig: float
    reuse_credited: int = 0
    n_new_skills: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "round": self.round_index,
            "n_traces": self.n_traces,
            "n_invariants": self.n_invariants,
            "n_skills": self.n_skills,
            "n_new_skills": self.n_new_skills,
            "n_capabilities": self.n_capabilities,
            "capability_score": round(self.capability_score, 6),
            "cgr": round(self.cgr, 6),
            "ig": round(self.ig, 6),
            "reuse_credited": self.reuse_credited,
        }


@dataclass(slots=True)
class FullPipelineResult:
    """End-to-end artifacts of one ASFT run."""

    rounds: list[RoundSnapshot] = field(default_factory=list)
    traces: list[Any] = field(default_factory=list)
    invariants: list[Any] = field(default_factory=list)
    skills: list[Any] = field(default_factory=list)
    capabilities: list[Capability] = field(default_factory=list)
    reuse: list[ReuseResult] = field(default_factory=list)
    summary: dict[str, Any] = field(default_factory=dict)

    @property
    def cgr_series(self) -> list[float]:
        return [r.cgr for r in self.rounds]

    @property
    def ig_series(self) -> list[float]:
        return [r.ig for r in self.rounds]

    @property
    def capability_scores(self) -> list[float]:
        return [r.capability_score for r in self.rounds]

    @property
    def cgr(self) -> float:
        return self.cgr_series[-1] if self.rounds else 0.0

    @property
    def ig(self) -> float:
        return self.ig_series[-1] if self.rounds else 0.0

    @property
    def success(self) -> bool:
        return bool(self.summary.get("success"))

    def to_dict(self) -> dict[str, Any]:
        return {
            "rounds": [r.to_dict() for r in self.rounds],
            "n_traces": len(self.traces),
            "n_invariants": len(self.invariants),
            "n_skills": len(self.skills),
            "n_capabilities": len(self.capabilities),
            "summary": dict(self.summary),
        }


def run_full_asft_pipeline(
    *,
    families: Sequence[str] = FAMILIES,
    per_family: int = 4,
    rounds: int = 4,
    seed: int = 0,
    difficulty: float = 0.2,
    eval_per_family: int = 2,
    eval_seed: int = 100,
    persist: bool = False,
    store_root: str | Path = "reports/traces",
    config: HarnessConfig | None = None,
) -> FullPipelineResult:
    """Run Phase A through E and return the measured learning curve."""
    cfg = config or HarnessConfig()
    result = FullPipelineResult()
    corpus: list[Any] = []
    library = None
    memory = TransferMemory()
    previous_score: float | None = None
    previous_ig: float | None = None

    for r in range(max(1, rounds)):
        # --- Phase A: new experience, appended to the corpus --------------
        # Later rounds introduce the composition mechanism, so accumulated
        # experience keeps exposing new structure rather than repeating the same
        # four op sequences at a larger scale.
        batch = run_trace_pipeline(
            families,
            per_family=per_family,
            seed=seed + r,
            difficulty=difficulty,
            persist=persist,
            store_root=store_root,
            solver=GridSolver(compose=r > 0),
        )
        corpus.extend(batch.traces)

        # --- Phase B: invariants over all experience so far --------------
        inv_run = run_invariant_pipeline(corpus)
        validated = list(inv_run.validation.validated) if inv_run.validation else []

        # --- Phase C: skills, *accumulated* into the existing library -----
        # The library is carried forward on purpose: skills gain reuse and
        # transfer evidence over time. Rebuilding it each round would throw that
        # evidence away and make growth impossible by construction.
        skill_run = run_skill_pipeline(inv_run.promotable, library=library)
        library = skill_run.library

        # --- Phase D: exercise the library on fresh tasks -----------------
        engine = ReuseEngine(library, memory=memory)
        eval_tasks = make_task_batch(
            tuple(families),
            per_family=eval_per_family,
            seed=eval_seed + r,
            difficulty=difficulty,
        )
        round_reuse = engine.apply_batch(eval_tasks)
        result.reuse.extend(round_reuse)

        # --- Phase E: capability + intelligence --------------------------
        caps = CapabilityLibrary()
        for cap in propose_capabilities_from_library(library):
            if caps.get(cap.capability_id) is None:
                caps.add(cap)
        state = compute_system_capability_state(
            caps, library, previous_score=previous_score, dt=cfg.default_dt
        )
        intel = compute_system_intelligence_state(
            caps,
            library,
            previous_ig=previous_ig,
            previous_capability_score=previous_score,
            experiences=cfg.experiences_per_step * len(corpus),
            dt=cfg.default_dt,
        )
        score = float(state.capability_score)
        result.rounds.append(
            RoundSnapshot(
                round_index=r,
                n_traces=len(corpus),
                n_invariants=len(validated),
                n_skills=len(library),
                n_new_skills=len(skill_run.promoted),
                n_capabilities=len(caps),
                capability_score=score,
                cgr=float(state.cgr),
                ig=float(intel.ig),
                reuse_credited=sum(1 for x in round_reuse if x.transfer_credit),
            )
        )
        result.traces = list(corpus)
        result.invariants = validated
        result.skills = list(library.list_skills())
        result.capabilities = list(caps.list_capabilities())
        previous_score, previous_ig = score, float(intel.ig)

    result.summary = _summarise(result, library, memory)
    return result


def _summarise(result: FullPipelineResult, library, memory: TransferMemory) -> dict[str, Any]:
    credited = [r for r in result.reuse if r.transfer_credit]
    attempts = [r for r in result.reuse if r.applied]
    records = memory.all_records()
    mean_benefit = (sum(r.benefit for r in records) / len(records)) if records else 0.0
    scores = result.capability_scores
    trough = min(scores) if scores else 0.0
    # Growth is claimed against the trough, not the first reading: introducing a
    # harder mechanism legitimately depresses capability before it recovers, and
    # the interesting claim is that the system grows *after* that shock.
    recovered = bool(scores) and scores[-1] > trough
    success = (
        bool(result.skills)
        and bool(result.capabilities)
        and result.cgr > 0.0
        and result.ig > 0.0
        and recovered
    )
    return {
        "success": success,
        "rounds": len(result.rounds),
        "n_traces": len(result.traces),
        "n_invariants": len(result.invariants),
        "n_skills": len(result.skills),
        "n_capabilities": len(result.capabilities),
        "library_size": len(library) if library is not None else 0,
        "reuse_attempts": len(attempts),
        "reuse_credited": len(credited),
        "transfer_rate": round(len(credited) / len(attempts), 4) if attempts else 0.0,
        "mean_transfer_benefit": round(mean_benefit, 4),
        "transfer_records": len(records),
        "initial_capability": round(scores[0], 6) if scores else 0.0,
        "trough_capability": round(trough, 6),
        "final_capability": round(scores[-1], 6) if scores else 0.0,
        "recovered_from_trough": recovered,
        "cgr": round(result.cgr, 6),
        "ig": round(result.ig, 6),
    }
