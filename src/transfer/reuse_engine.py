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
from core.states import SkillState
from skills.config import SkillConfig
from skills.library import SkillLibrary
from skills.monitoring import record_negative, record_reuse, record_transfer
from skills.retrieval import retrieve_skills
from solver.executor import GridSolver, SolveResult
from solver.grid import Grid
from solver.tasks import FAMILY_OPS, GridTask
from transfer.memory import TransferMemory
from transfer.records import TransferRecord
from transfer.taxonomy import TransferType

__all__ = ["ReuseEngine", "ReuseResult"]

#: Families whose reduction legitimately uses reflection as an invariance.
CROSS_FAMILY_REFLECTION = frozenset({"counting", "grouping"})


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

        # Reuse is only credit-bearing when the replayed skill was correct. A
        # failure must be recorded as negative evidence, otherwise NTR is
        # structurally always zero and negative transfer is invisible.
        if reused.success:
            record_reuse(
                skill,
                task_id=task.task_id,
                detail={"family": task.task_family, "benefit": benefit},
                config=self.config,
                task_clock=task_clock,
            )
        else:
            record_negative(
                skill,
                reason="reuse_incorrect",
                detail={
                    "task_id": task.task_id,
                    "family": task.task_family,
                },
                config=self.config,
            )

        if benefit > 0.0:
            _confirm(skill)
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
        actually holds on this grid. Provisional skills (admitted on a prior) are
        eligible: trialling them is what generates the transfer evidence.
        """
        wanted = list(FAMILY_OPS.get(task.task_family, ()))
        candidates = retrieve_skills(self.library, wanted, state=None, config=self.config)
        if not candidates:
            candidates = retrieve_skills(self.library, state=None, config=self.config)
        for skill in candidates:
            if not _is_retrievable(skill):
                continue
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


def _is_retrievable(skill: Skill) -> bool:
    """Active-tier skills, plus provisional trials awaiting confirmation."""
    if skill.state in (SkillState.ACTIVE, SkillState.GROWING, SkillState.CORE):
        return True
    meta = skill.metadata or {}
    return bool(meta.get("provisional")) and skill.state is SkillState.PROMOTED


def _confirm(skill: Skill) -> None:
    """Promote a provisional skill to ACTIVE once transfer is measured."""
    meta = dict(skill.metadata or {})
    meta["transfer_verified"] = True
    meta["provisional"] = False
    skill.metadata = meta
    if skill.state is SkillState.PROMOTED:
        skill.transition_to(SkillState.ACTIVE)


def _macro_ops(skill: Skill) -> list[str]:
    """Apply-step to replay: prefer the canonical apply op in the triggers."""
    for trigger in skill.trigger_conditions:
        if str(trigger).startswith("apply_"):
            return [str(trigger)]
        if str(trigger) == "find_symmetry":
            return ["apply_reflection"]
        if str(trigger) == "find_rotation":
            return ["apply_rotation"]
        if str(trigger) in {"count_objects", "group_by_color"}:
            return [str(trigger)]
    meta = skill.metadata or {}
    sig = meta.get("pattern_signature") or []
    for op in sig:
        if str(op).startswith("apply_"):
            return [str(op)]
        if str(op) == "find_symmetry":
            return ["apply_reflection"]
        if str(op) == "find_rotation":
            return ["apply_rotation"]
    return []


def _invariance_holds(skill: Skill, task: GridTask) -> bool:
    """True when the skill's invariance is genuinely present in this task.

    A skill may only be applied across families when the claimed invariance holds
    on the grid *as a whole* — not merely on one palindromic row, which every
    mostly-empty grid has. Within its own family the family definition is the
    invariance.
    """
    ops = _macro_ops(skill)
    if not ops:
        return False
    op = ops[0]
    family = task.task_family
    if _source_family(skill) == family:
        return True
    if op == "apply_reflection":
        # Reflection must actually be a symmetry of the grid, and the family must
        # be one whose output could legitimately involve it.
        return family in CROSS_FAMILY_REFLECTION and _is_symmetric(task.input_grid)
    if op == "apply_rotation":
        return family == "rotation"
    return False


def _is_symmetric(grid: Grid) -> bool:
    """Whole-grid horizontal symmetry: every row reads the same both ways."""
    return all(row == tuple(reversed(row)) for row in grid.cells)


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
