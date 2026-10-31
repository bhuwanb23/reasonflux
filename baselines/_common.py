"""Shared harness for the v0.1 baselines.

Every baseline reports the same five numbers as the full pipeline so the paper
table is directly comparable. The measurement is deliberately identical: what
differs is only *how the library is built*.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from capability.emerge import propose_capabilities_from_library
from capability.library import CapabilityLibrary
from capability.portfolio import compute_system_capability_state
from core.skill import Skill
from core.states import SkillState
from evaluation.harness.config import HarnessConfig
from evaluation.intelligence_state import compute_system_intelligence_state
from solver.tasks import FAMILIES, make_task_batch
from transfer.memory import TransferMemory
from transfer.reuse_engine import ReuseEngine
from skills.library import SkillLibrary

__all__ = ["BaselineResult", "measure_library", "make_skill", "eval_tasks_for"]


@dataclass(slots=True)
class BaselineResult:
    """Comparable metrics for one baseline."""

    name: str
    mean_su: float = 0.0
    mean_ts: float = 0.0
    cgr: float = 0.0
    ig: float = 0.0
    capability_score: float = 0.0
    n_skills: int = 0
    n_capabilities: int = 0
    reuse_credited: int = 0
    success: bool = False
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "mean_su": round(self.mean_su, 6),
            "mean_ts": round(self.mean_ts, 6),
            "cgr": round(self.cgr, 6),
            "ig": round(self.ig, 6),
            "capability_score": round(self.capability_score, 6),
            "n_skills": self.n_skills,
            "n_capabilities": self.n_capabilities,
            "reuse_credited": self.reuse_credited,
            "success": self.success,
            "metadata": dict(self.metadata),
        }


def eval_tasks_for(
    *, seed: int = 100, per_family: int = 2, difficulty: float = 0.2
) -> list:
    return make_task_batch(
        FAMILIES, per_family=per_family, seed=seed, difficulty=difficulty
    )


def make_skill(
    skill_id: str,
    *,
    category: str,
    triggers: Sequence[str],
    utility: float = 0.3,
    transfer_score: float = 0.0,
    reuse: int = 1,
) -> Skill:
    """Build a skill in ACTIVE state with an apply step so reuse can replay it."""
    return Skill(
        skill_id=skill_id,
        trigger_conditions=list(triggers),
        utility=float(utility),
        transfer_score=float(transfer_score),
        reuse_count=int(reuse),
        state=SkillState.ACTIVE,
        metadata={
            "mvp_category": category,
            "pattern_signature": list(triggers),
            "utility_breakdown": {"su": float(utility)},
        },
    )


def measure_library(
    name: str,
    library: SkillLibrary,
    *,
    tasks: Sequence[Any] | None = None,
    seed: int = 100,
    config: HarnessConfig | None = None,
) -> BaselineResult:
    """Measure a library exactly the way the full pipeline is measured."""
    cfg = config or HarnessConfig()
    skills = library.list_skills()
    memory = TransferMemory()
    engine = ReuseEngine(library, memory=memory)
    reuse = engine.apply_batch(tasks or eval_tasks_for(seed=seed))

    caps = CapabilityLibrary()
    for cap in propose_capabilities_from_library(library):
        if caps.get(cap.capability_id) is None:
            caps.add(cap)
    state = compute_system_capability_state(caps, library, dt=cfg.default_dt)
    intel = compute_system_intelligence_state(
        caps, library, experiences=cfg.experiences_per_step * len(reuse), dt=cfg.default_dt
    )

    mean_su = sum(float(s.utility or 0.0) for s in skills) / len(skills) if skills else 0.0
    mean_ts = (
        sum(float(s.transfer_score or 0.0) for s in skills) / len(skills)
        if skills
        else 0.0
    )
    credited = sum(1 for r in reuse if r.transfer_credit)
    return BaselineResult(
        name=name,
        mean_su=mean_su,
        mean_ts=mean_ts,
        cgr=float(state.cgr),
        ig=float(intel.ig),
        capability_score=float(state.capability_score),
        n_skills=len(skills),
        n_capabilities=len(caps),
        reuse_credited=credited,
        success=bool(skills) and credited > 0 and float(state.capability_score) > 0,
        metadata={
            "mean_transfer_benefit": round(
                sum(r.benefit for r in reuse) / len(reuse), 4
            )
            if reuse
            else 0.0,
            "transfer_records": len(memory.all_records()),
        },
    )
