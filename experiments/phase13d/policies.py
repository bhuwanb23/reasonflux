"""Policy-arm cloning, operation retrieval, and deterministic cost evaluation."""
from __future__ import annotations
import random
from typing import Any
from .common import OP_COST, STEP_PENALTY
from core.skill import Skill
from skills.library import SkillLibrary
from skills.config import SkillConfig
from skills.monitoring import record_negative, record_reuse, record_transfer
from skills.composition.propose import propose_sequential
from skills.composition.evaluate import record_composition_outcome
from skills.composition.lifecycle import advance_composition
from transfer.reuse_engine import _confirm
from .task_programs import TransferTask, execute_program, normalize_expected
from .baselines import memory_matches, literal_memory_matches, compressed_chunks


SKILL_POLICIES = {"ASFT", "A2_NO_SCT", "A3_NO_PERSISTENCE", "A4_NO_COMPOSITION", "BEST_SINGLE"}


def clone_pool(pool: list[dict[str, Any]]) -> tuple[SkillLibrary, list[dict[str, Any]]]:
    library = SkillLibrary()
    copied = []
    for item in pool:
        skill = Skill.from_dict(item["skill"].to_dict())
        library.add(skill)
        copied.append({**item, "skill": skill})
    return library, copied


def init_policy_state(pool: list[dict[str, Any]], policy: str, *, random_seed: int) -> dict[str, Any]:
    library, skills = clone_pool(pool)
    if policy in {"ASFT", "A4_NO_COMPOSITION", "BEST_SINGLE"}:
        skills = [s for s in skills if float(s["SCV10"]) > 0.0]
        library = SkillLibrary()
        for item in skills:
            library.add(item["skill"])
    return {"library": library, "skills": skills, "ephemeral_used": set(),
            "composition": None, "random_seed": int(random_seed), "rng": random.Random(random_seed)}


def best_skill(skills: list[dict[str, Any]], op: str) -> dict[str, Any] | None:
    matches = [s for s in skills if s["op"] == op]
    return sorted(matches, key=lambda s: (-float(s["SCV10"]), s["skill"].skill_id))[0] if matches else None


def proposal_for(library: SkillLibrary, skills: list[dict[str, Any]], ops: tuple[str, ...], config: SkillConfig):
    if len(ops) < 2:
        return None
    selected = [best_skill(skills, op) for op in ops]
    if any(item is None for item in selected):
        return None
    candidates = propose_sequential(library, list(ops), config, skills=[item["skill"] for item in selected])
    wanted = [item["skill"].skill_id for item in selected]
    return next((c for c in candidates if c.order == wanted), None)


def op_steps(op: str) -> int:
    return int(OP_COST[op])


def run_policy(task: TransferTask, policy: str, pool: list[dict[str, Any]], examples: list[dict[str, Any]],
               compression: list[tuple[str, ...]], *, state: dict[str, Any] | None = None,
               allow_composition: bool = False, config: SkillConfig | None = None) -> dict[str, Any]:
    """Run one arm on one task. Pass a shared state across tasks in a seed/cell."""
    config = config or SkillConfig()
    state = state or init_policy_state(pool, policy, random_seed=task.run_seed + 7000)
    library, skills = state["library"], state["skills"]
    before = execute_program(task.input_grid, task.ops)
    baseline_steps = sum(op_steps(op) for op in task.ops) + 1
    actual_ops = tuple(task.ops)
    prefix: tuple[str, ...] = ()
    assigned = False
    reused = False
    used_skill_ids: list[str] = []
    selected: list[dict[str, Any] | None] = [None for _ in task.ops]
    retrieved = 0
    if policy == "B3_RANDOM_SKILLS" and skills:
        chosen = skills[state["rng"].randrange(len(skills))]
        prefix = (chosen["op"],)
        actual_ops = prefix + task.ops
        assigned = reused = True
        used_skill_ids = [chosen["skill"].skill_id]
    elif policy == "EXP15_FORCED_REFLECTION":
        reflection_skill = best_skill(skills, "apply_reflection")
        if reflection_skill:
            prefix = ("apply_reflection",)
            actual_ops = prefix + task.ops
            assigned = reused = True
            used_skill_ids = [reflection_skill["skill"].skill_id]
    elif policy == "EXP16_RANDOM_FORCED" and skills:
        chosen = skills[state["rng"].randrange(len(skills))]
        prefix = (chosen["op"],)
        actual_ops = prefix + task.ops
        assigned = reused = True
        used_skill_ids = [chosen["skill"].skill_id]
    elif policy == "EXP17_WRONG_COMPOSITION":
        wrong_components = [best_skill(skills, op) for op in ("apply_reflection", "group_by_color")]
        if all(wrong_components):
            prefix = ("apply_reflection", "group_by_color")
            actual_ops = prefix + task.ops
            assigned = reused = True
            used_skill_ids = [item["skill"].skill_id for item in wrong_components]
    elif policy == "B2_MEMORY_ONLY":
        selected = [({"op": op} if memory_matches(examples, op, task.input_family) else None) for op in task.ops]
        retrieved = len(examples)
    elif policy == "A1_NO_INVARIANTS":
        selected = [({"op": op} if literal_memory_matches(examples, task.input_grid, op) else None) for op in task.ops]
        retrieved = len(examples)
    elif policy == "B4_COMPRESSION_PROXY":
        selected = [({"op": op} if (op,) in compression else None) for op in task.ops]
        retrieved = len(compression)
    elif policy in SKILL_POLICIES:
        selected = [best_skill(skills, op) for op in task.ops]
        retrieved = len(skills)
    if policy == "A3_NO_PERSISTENCE":
        for i, item in enumerate(selected):
            if item and item.get("skill"):
                sid = item["skill"].skill_id
                if sid in state["ephemeral_used"]:
                    selected[i] = None
                else:
                    state["ephemeral_used"].add(sid)
    proposal = None
    if allow_composition and policy in {"ASFT", "A2_NO_SCT"}:
        proposal = state.get("composition")
        if proposal is None:
            proposal = proposal_for(library, skills, task.ops, config)
            state["composition"] = proposal
    composition_trial = bool(proposal)
    composition_active = bool(proposal and proposal.state.value in {"reusable", "active", "validated", "promoted"})
    if policy == "BEST_SINGLE" and selected:
        best = max((item for item in selected if item), key=lambda item: float(item["SCV10"]), default=None)
        selected = [best] + [None] * max(0, len(task.ops) - 1)
    if policy in {"B3_RANDOM_SKILLS", "EXP15_FORCED_REFLECTION", "EXP16_RANDOM_FORCED", "EXP17_WRONG_COMPOSITION"}:
        steps = baseline_steps + 2 * len(prefix)
    elif policy == "B4_COMPRESSION_PROXY":
        chunks = compressed_chunks(task.ops, compression)
        steps = 1 + sum((1 + len(chunk)) if chunk in compression else op_steps(chunk[0]) for chunk in chunks)
        reused = any(chunk in compression for chunk in chunks)
        assigned = reused
    elif composition_active:
        steps = 1 + len(task.ops) + 1
        assigned = reused = True
    else:
        steps = 1 + sum((2 if item else op_steps(op)) for op, item in zip(task.ops, selected))
        assigned = assigned or any(selected)
        reused = any(selected)
    after = execute_program(task.input_grid, task.ops, prefix_ops=prefix)
    correct = normalize_expected(after) == normalize_expected(task.expected)
    p_before = 1.0 - STEP_PENALTY * baseline_steps
    p_after = float(correct) - STEP_PENALTY * steps
    transfer_by_op = {item["op"]: item for item in selected if item and item.get("skill")}
    for item in transfer_by_op.values():
        skill = item["skill"]
        if correct:
            record_reuse(skill, task_id=task.task_id, detail={"benefit": max(0.0, (baseline_steps - steps) / max(1, baseline_steps))}, config=config, task_clock=task.index)
            if p_after < p_before:
                record_negative(skill, reason="phase13d_performance_harm", detail={"task_id": task.task_id}, config=config)
            if steps < baseline_steps:
                benefit = max(0.0, (baseline_steps - steps) / max(1, baseline_steps))
                _confirm(skill)
                record_transfer(skill, source_family=item.get("family", ""), target_family=task.input_family,
                                success=True, benefit=benefit, config=config, task_clock=task.index)
        else:
            record_negative(skill, reason="phase13d_incorrect_application", detail={"task_id": task.task_id}, config=config)
    logged = {item["skill"].skill_id for item in transfer_by_op.values()}
    for sid in set(used_skill_ids) - logged:
        item = next((candidate for candidate in skills if candidate["skill"].skill_id == sid), None)
        if item and correct:
            record_reuse(item["skill"], task_id=task.task_id,
                         detail={"forced_policy": policy, "benefit": 0.0}, config=config, task_clock=task.index)
        if item and (not correct or p_after < p_before):
            record_negative(item["skill"], reason="phase13d_forced_negative_transfer",
                            detail={"task_id": task.task_id, "policy": policy}, config=config)
    if proposal is not None:
        reduction = max(0.0, (baseline_steps - steps) / max(1, baseline_steps))
        record_composition_outcome(proposal, success=correct, transfer_gain=reduction,
                                   reasoning_reduction=reduction, task_family=task.input_family, config=config)
        advance_composition(proposal, config)
    return {
        "task_id": task.task_id, "experiment_id": task.experiment_id,
        "taxonomy": task.taxonomy, "input_family": task.input_family,
        "ops": list(task.ops), "policy": policy,
        "P_before": p_before, "P_after": p_after,
        "baseline_steps": baseline_steps, "transfer_steps": steps,
        "correct_before": True, "correct_after": correct,
        "assigned_application": bool(assigned), "reused": bool(reused),
        "composition_candidate": composition_trial,
        "composition_active": composition_active,
        "reused_skill_ids": sorted(set(used_skill_ids) | {item["skill"].skill_id for item in transfer_by_op.values()}),
        "retrieval_candidates_evaluated": retrieved,
        "random_seed": state.get("random_seed") if policy in {"B3_RANDOM_SKILLS", "EXP16_RANDOM_FORCED"} else None,
        "expected": normalize_expected(task.expected), "actual": normalize_expected(after),
    }
