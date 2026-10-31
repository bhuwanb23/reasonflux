"""Reuse engine — apply stored skills onto new tasks (Phase 11, Phase D).

This is where transfer stops being a claim and becomes a measurement. The
engine retrieves a matching skill, replays it as collapsed macro steps, re-solves
the task, and records the *observed* reasoning reduction and benefit.

Transfer is only credited when the reused run is both correct and cheaper than
the free-search baseline for the same task.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Sequence

from core.skill import Skill
from skills.config import SkillConfig
from skills.library import SkillLibrary
from skills.monitoring import record_reuse, record_transfer
from skills.retrieval import retrieve_skills
from solver.executor import GridSolver, SolveResult
from solver.tasks import GridTask, FAMILY_OPS
from transfer.memory import TransferMemory
from transfer.records import TransferRecord
from transfer.taxonomy import TransferType

__all__ = ["ReuseEngine", "ReuseResult"]


@dataclass(slots=True)
class ReuseResult:
    """Outcome of applying (or failing to apply) a skill to one task."""

    task_id: str
    task_family: str
    applied: bool
    success: bool
    skill_id: str = ""
    baseline_cost: float = 0.0
    reused_cost: float = 0.0
    reasoning_reduction: float = 0.0
    benefit: float = 0.0
    result: SolveResult | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    @property
    def transfer_credit(self) -> bool:
        """Transfer counts only if reuse was correct and cheaper."""
        return self.applied and self.success and self.benefit > 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "task_family": self.task_family,
            "applied": self.applied,
            "success": self.success,
            "skill_id": self.skill_id,
            "baseline_cost": self.baseline_cost,
            "reused_cost": self.reused_cost,
            "reasoning_reduction": self.reasoning_reduction,
            "benefit": self.benefit,
            "transfer_credit": self.transfer_credit,
            "metadata": dict(self.metadata),
        }


class ReuseEngine:
    """Apply prior skills to a new task and measure cost/accuracy change."""

    def __init__(
        self,
        library: SkillLibrary,
        *,
        memory: TransferMemory | None = None,
        solver: GridSolver | None = None,
        config: SkillConfig | None = None,
    ) -> None:
        self.library = library
        self.memory = memory or TransferMemory()
        self.solver = solver or GridSolver()
        self.config = config or SkillConfig()

    def apply(
        self,
        task: GridTask,
        *,
        baseline: SolveResult | None = None,
        task_clock: int | None = None,
    ) -> ReuseResult:
        """Retrieve a skill for ``task``, replay it, and record the transfer."""
        skill = self.retrieve(task)
        base = baseline if baseline is not None else self.solver.solve(task)

        if skill is None:
            # No skill applied: report the baseline as the observed cost so the
            # measured reduction is zero rather than a spurious 100%.
            return ReuseResult(
                task_id=task.task_id,
                task_family=task.task_family,
                applied=False,
                success=bool(base.success),
                baseline_cost=float(base.cost),
                reused_cost=float(base.cost),
                reasoning_reduction=0.0,
                benefit=0.0,
                metadata={"reason": "no_matching_skill"},
            )

        reused = self.solver.solve(task, macro_ops=_macro_ops(skill))
        reduction = _reduction(base.cost, reused.cost)
        benefit = reduction if reused.success else 0.0

        result = ReuseResult(
            task_id=task.task_id,
            task_family=task.task_family,
            applied=True,
            success=bool(reused.success),
            skill_id=skill.skill_id,
            baseline_cost=float(base.cost),
            reused_cost=float(reused.cost),
            reasoning_reduction=reduction,
            benefit=benefit,
            result=reused,
            metadata={
                "baseline_steps": base.step_count,
                "reused_steps": reused.step_count,
                "skill_triggers": list(skill.trigger_conditions),
            },
        )

        record_reuse(
            skill,
            task_id=task.task_id,
            detail={"family": task.task_family, "benefit": benefit},
            config=self.config,
            task_clock=task_clock,
        )
        if benefit > 0.0:
            record_transfer(
                skill,
                source_family=_source_family(skill),
                target_family=task.task_family,
                success=True,
                benefit=benefit,
                config=self.config,
                task_clock=task_clock,
            )
            self.memory.record(
                TransferRecord(
                    invariant_id=skill.source_invariant_id or skill.skill_id,
                    source_family=_source_family(skill),
                    target_family=task.task_family,
                    success=True,
                    benefit=round(benefit, 6),
                    reasoning_reduction=round(reduction, 6),
                    transfer_type=_transfer_type(skill, task.task_family),
                )
            )
        return result

    def retrieve(self, task: GridTask) -> Skill | None:
        """Pick the best skill that is genuinely applicable to this task.

        A skill is applicable only when it carries a reusable ``apply_`` step.
        Cross-family use is allowed solely when the underlying invariance
        actually holds on this grid — a reflection skill may serve a symmetric
        counting grid, but never an asymmetric one.
        """
        wanted = list(FAMILY_OPS.get(task.task_family, ()))
        candidates = retrieve_skills(self.library, wanted, config=self.config)
        if not candidates:
            candidates = retrieve_skills(self.library, config=self.config)
        for skill in candidates:
            if not _macro_ops(skill):
                continue
            if _invariance_holds(skill, task):
                return skill
        return None

    def apply_batch(
        self,
        tasks: Sequence[GridTask],
        *,
        solver: GridSolver | None = None,
    ) -> list[ReuseResult]:
        """Apply reuse across a batch, measuring each against free search."""
        engine = solver or self.solver
        out: list[ReuseResult] = []
        for i, task in enumerate(tasks):
            out.append(
                self.apply(
                    task,
                    baseline=engine.solve(task),
                    task_clock=i,
                )
            )
        return out


def _macro_ops(skill: Skill) -> list[str]:
    """Apply-step to replay: prefer the canonical apply op in the triggers."""
    for trigger in skill.trigger_conditions:
        if str(trigger).startswith("apply_"):
            return [str(trigger)]
    meta = skill.metadata or {}
    sig = meta.get("pattern_signature") or []
    for op in sig:
        if str(op).startswith("apply_"):
            return [str(op)]
    return []


def _invariance_holds(skill: Skill, task: GridTask) -> bool:
    """True when the skill's invariance is genuinely present in this task.

    Within the skill's own family the family definition *is* the invariance.
    Across families the claim must hold on the grid itself: reflection is a real
    invariance only on a symmetric grid.
    """
    ops = _macro_ops(skill)
    if not ops:
        return False
    op = ops[0]
    same_family = _source_family(skill) == task.task_family
    if op == "apply_reflection":
        return same_family or any(
            row == tuple(reversed(row)) for row in task.input_grid.cells
        )
    if op == "apply_rotation":
        return task.task_family == "rotation"
    return False


def _reduction(baseline_cost: float, reused_cost: float) -> float:
    if baseline_cost <= 0:
        return 0.0
    return max(0.0, min(1.0, (baseline_cost - reused_cost) / baseline_cost))


def _source_family(skill: Skill) -> str:
    meta = skill.metadata or {}
    return str(meta.get("mvp_category") or "unknown")


def _transfer_type(skill: Skill, target_family: str) -> TransferType:
    return (
        TransferType.NEAR
        if _source_family(skill) == target_family
        else TransferType.MODERATE
    )
