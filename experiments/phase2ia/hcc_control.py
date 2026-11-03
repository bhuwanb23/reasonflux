"""Deterministic synthetic HCC positive-control generator and plumbing check.

All HCC examples/oracle targets are generated in memory. They are never ARC
examples and are never written to an ARC registry or candidate population.
"""
from __future__ import annotations
from dataclasses import dataclass
import hashlib
from pathlib import Path
from typing import Any

from core.trace import ReasoningStep, ReasoningTrace, TraceOutcome
from experiments.phase13g.common import apply_program as _r1_apply_registered
from representations.r3 import Action, Demonstration, Selector, apply_action, parse_grid
from traces.semantic_adapter import Representation, adapt_successful_candidate
from experiments.phase2ia.runtime_config import build_trace_miner, phase2i_structural_violations

ROOT=Path(__file__).resolve().parents[2]
PKG=ROOT/"reports/experiments/ASFT-V1.1-PHASE-2I-A-CANDIDATE-PRODUCTION-ENABLEMENT-V1"
HCC_VERSION="ASFT-2I-HCC-SYNTH-V1"
RULES=("identity","reflect_horizontal","reflect_vertical","rotate_90","recolor_bijection","translate_constant")
COHORTS_BY_RULE={
 "identity":("layout_a","layout_b"),
 "reflect_horizontal":("layout_b","layout_c"),
 "reflect_vertical":("layout_a","layout_c"),
 "rotate_90":("layout_a","layout_b"),
 "recolor_bijection":("layout_b","layout_c"),
 "translate_constant":("layout_a","layout_c"),
}
MASKS={
 "layout_a":(
  ((0,0),(0,1),(1,0),(1,1),(2,1),(2,2)),
  ((0,0),(1,0),(1,1),(1,2),(2,1),(2,2)),
 ),
 "layout_b":(
  ((0,0),(0,1),(0,2),(1,2),(2,2),(2,1)),
  ((0,0),(1,0),(2,0),(2,1),(1,1),(1,2)),
 ),
 "layout_c":(
  ((0,0),(0,1),(1,1),(1,2),(2,1),(2,2)),
  ((0,0),(0,1),(0,2),(1,0),(1,1),(2,1)),
 ),
}

@dataclass(frozen=True, slots=True)
class HCCTask:
    task_id: str
    rule_family: str
    synthetic_family: str
    demonstrations: tuple[Demonstration,...]

@dataclass(frozen=True, slots=True)
class HCCSummary:
    control_version: str
    task_count: int
    rule_counts: dict[str,int]
    cohort_counts: dict[str,int]
    training_pair_count: int
    r1_equivalent_demo_checks: int
    r3_equivalent_demo_checks: int
    r1_traces: int
    r3_traces: int
    r1_candidates: int
    r3_candidates: int
    r1_structurally_eligible: int
    r3_structurally_eligible: int
    identical_candidate_signatures: bool
    scope: str="SYNTHETIC_PLUMBING_ONLY_NOT_ARC_EVIDENCE"


def _grid(mask: tuple[tuple[int,int],...], color:int=1) -> tuple[tuple[int,...],...]:
    rows=[[0]*7 for _ in range(7)]
    for r,c in mask: rows[r+2][c+2]=color
    return tuple(tuple(row) for row in rows)


def _oracle_target(raw:Any,rule:str) -> tuple[tuple[int,...],...]:
    """Independent coordinate-level HCC target generator on the 7x7 board."""
    g=tuple(tuple(int(v) for v in row) for row in raw)
    h,w=len(g),len(g[0]); out=[[0]*w for _ in range(h)]
    for r,row in enumerate(g):
        for c,value in enumerate(row):
            if value==0: continue
            if rule=="identity": rr,cc,color=r,c,value
            elif rule=="reflect_horizontal": rr,cc,color=r,w-1-c,value
            elif rule=="reflect_vertical": rr,cc,color=h-1-r,c,value
            elif rule=="rotate_90": rr,cc,color=c,h-1-r,value
            elif rule=="recolor_bijection": rr,cc,color=r,c,2 if value==1 else 1 if value==2 else value
            elif rule=="translate_constant": rr,cc,color=r,c+1,value
            else: raise ValueError(f"unregistered HCC rule {rule}")
            if 0<=rr<h and 0<=cc<w: out[rr][cc]=color
    return tuple(tuple(row) for row in out)


def _apply_registered_r1(raw:Any,rule:str) -> tuple[tuple[int,...],...]:
    """Run the registered R1 implementation with HCC-known train parameters."""
    grid=tuple(tuple(int(v) for v in row) for row in raw)
    if rule=="translate_constant": context={"dy":0,"dx":1,"bg":0}
    elif rule=="recolor_bijection": context={"mapping":{c:(2 if c==1 else 1 if c==2 else c) for c in range(10)}}
    else: context={}
    result=_r1_apply_registered(rule,grid,context)
    if result is None: raise AssertionError(f"registered R1 HCC candidate failed: {rule}")
    return result


def _r3_candidate(rule:str) -> tuple[str,Action]:
    if rule=="identity": return "move",Action.make("move",dy=0,dx=0)
    if rule=="reflect_horizontal": return "reflect_vertical_axis",Action.make("reflect_vertical_axis")
    if rule=="reflect_vertical": return "reflect_horizontal_axis",Action.make("reflect_horizontal_axis")
    if rule=="rotate_90": return "rotate_90",Action.make("rotate",k=1)
    if rule=="recolor_bijection": return "recolor",Action.make("recolor",color=2)
    if rule=="translate_constant": return "move",Action.make("move",dy=0,dx=1)
    raise ValueError(f"unregistered HCC rule {rule}")


def assert_no_hcc_task_in_arc_inputs(hcc_task_ids:tuple[str,...]|list[str],arc_task_ids:tuple[str,...]|list[str]) -> None:
    """Fail closed if any synthetic-control task can enter an ARC input list."""
    hcc=set(hcc_task_ids); arc=set(arc_task_ids)
    if any(not task_id.startswith("HCC-") for task_id in hcc):
        raise ValueError("HCC namespace contains a non-HCC task ID")
    overlap=hcc & arc
    if overlap:
        raise ValueError(f"HCC task IDs cannot enter ARC inputs: {sorted(overlap)}")


def build_hcc_tasks() -> tuple[HCCTask,...]:
    """Build 20 paired task IDs for each of the six known synthetic rules."""
    tasks=[]
    for rule in RULES:
        cohorts=COHORTS_BY_RULE[rule]
        for i in range(20):
            cohort=cohorts[0] if i<10 else cohorts[1]
            demos=[]
            for d in range(2):
                mask=MASKS[cohort][(i+d)%2]
                grid=_grid(mask)
                target=_oracle_target(grid,rule)
                demos.append(Demonstration(grid,target))
            tasks.append(HCCTask(f"HCC-{rule}-{i:02d}",rule,cohort,tuple(demos)))
    return tuple(tasks)


def _sha(path:Path) -> str: return hashlib.sha256(path.read_bytes()).hexdigest()


def _candidate_summary(traces:list[ReasoningTrace]) -> tuple[list[tuple[str,tuple[str,...],tuple[str,...]]],int]:
    """Mine oracle-selected action-event fixtures, not complete production traces.

    WP5 isolates the frozen miner from generic control-event fragments that
    otherwise connect all six known actions under min_core_length=1. This is a
    candidate-stage positive control only; it does not validate search coverage
    or establish an end-to-end ARC production result.
    """
    miner=build_trace_miner()
    result=miner.mine(traces)
    records=[(c.invariant_id,tuple(c.pattern_signature),tuple(sorted(c.task_families))) for c in result.candidates]
    eligible=sum(not phase2i_structural_violations(c,miner.policy) for c in result.candidates)
    return records,eligible


def _action_event_fixture(trace:ReasoningTrace, *, family:str) -> ReasoningTrace:
    """One-step, oracle-selected action observation for the HCC miner control."""
    event=trace.steps[2]
    return ReasoningTrace(
      trace_id=f"HCC-MINER-{trace.trace_id}", task_id=trace.task_id, timestamp=0.0,
      steps=[ReasoningStep(step_id=f"HCC-MINER-{trace.task_id}",operation=event.operation,inputs=[])],
      outcome=TraceOutcome(success=True,result=None,cost=0.0),
      metadata={"task_family":family,"hcc_scope":"synthetic_oracle_action_fixture"})


def run_hcc_control() -> HCCSummary:
    """Check six R1/R3 equivalents and candidate-pipeline plumbing in memory."""
    tasks=build_hcc_tasks()
    assert_no_hcc_task_in_arc_inputs([t.task_id for t in tasks],[])
    r1_ok=r3_ok=0
    r1_traces=[]; r3_traces=[]
    r1_miner_fixtures=[]; r3_miner_fixtures=[]
    r1_grammar_hash=_sha(PKG/"../ASFT-V1.1-PHASE-2F-REPRESENTATION-ALTERNATIVES-V1/representation_registry.csv")
    r3_grammar_hash=_sha(PKG/"r3_grammar_addendum_v1.md")
    r1_impl_hash=_sha(ROOT/"experiments/phase13g/common.py")
    r3_impl_hash=_sha(ROOT/"src/representations/r3.py")
    for task in tasks:
        op_name,action=_r3_candidate(task.rule_family)
        for demo in task.demonstrations:
            oracle=_oracle_target(demo.input_grid,task.rule_family)
            if oracle!=demo.output_grid: raise AssertionError("HCC oracle target mismatch")
            if _apply_registered_r1(demo.input_grid,task.rule_family)!=oracle:
                raise AssertionError(f"HCC registered R1 equivalent failed: {task.task_id}/{task.rule_family}")
            r1_ok+=1
            parsed=parse_grid(demo.input_grid)
            applied=apply_action(parsed,Selector("exact_color",1),action)
            if applied.status.value!="APPLIED" or applied.grid!=oracle:
                raise AssertionError(f"HCC R3 equivalent failed: {task.task_id}/{task.rule_family}")
            r3_ok+=1
        candidate_id=f"HCC-ORACLE-{task.rule_family}-{task.task_id}"
        r1=adapt_successful_candidate(representation=Representation.R1,operation=task.rule_family,
          task_id=task.task_id,candidate_id=candidate_id,grammar_hash=r1_grammar_hash,
          implementation_hash=r1_impl_hash,trial_index=1,trace_id=f"HCC-R1-{task.task_id}")
        r3=adapt_successful_candidate(representation=Representation.R3,operation=action,
          task_id=task.task_id,candidate_id=candidate_id,grammar_hash=r3_grammar_hash,
          implementation_hash=r3_impl_hash,trial_index=1,trace_id=f"HCC-R3-{task.task_id}")
        r1_projected=r1.mining_projection(independent_task_family=task.synthetic_family)
        r3_projected=r3.mining_projection(independent_task_family=task.synthetic_family)
        r1_traces.append(r1_projected); r3_traces.append(r3_projected)
        r1_miner_fixtures.append(_action_event_fixture(r1_projected,family=task.synthetic_family))
        r3_miner_fixtures.append(_action_event_fixture(r3_projected,family=task.synthetic_family))
    r1_candidates,r1_eligible=_candidate_summary(r1_miner_fixtures)
    r3_candidates,r3_eligible=_candidate_summary(r3_miner_fixtures)
    rule_counts={r:sum(t.rule_family==r for t in tasks) for r in RULES}
    cohort_counts={c:sum(t.synthetic_family==c for t in tasks) for c in sorted({t.synthetic_family for t in tasks})}
    return HCCSummary(HCC_VERSION,len(tasks),rule_counts,cohort_counts,sum(len(t.demonstrations) for t in tasks),
      r1_ok,r3_ok,len(r1_traces),len(r3_traces),len(r1_candidates),len(r3_candidates),
      r1_eligible,r3_eligible,r1_candidates==r3_candidates)
