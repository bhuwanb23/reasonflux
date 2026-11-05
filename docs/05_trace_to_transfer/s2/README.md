# T2T-S2 — Synthetic Mechanism Prototype

**Status:** user-authorized prototype and exploratory mechanism check completed, 2026-11-04.  
**Scope:** one key/door world; Claims N and B only. No ARC/AGI-3, benchmark, model, evaluator, leaderboard, or paper work.

## What was implemented

- One deterministic key/door transition world and a single color-match relation family.
- R1-Max as a source-only compressed trace-to-script baseline, using a fixed predicate grammar and shortest consistent conjunction.
- I0 as a one-family relation fit, plus G0 and an append-only synthetic counterexample/update to successor G1.
- Finite N and B scoring; focused tests at `tests/test_t2t_s2_mechanism.py` (**8 passed**).

## What happened

An initial pilot used a weaker shared-slot replay implementation and showed I0 8/8 versus replay 4/8. After seeing that output, R1-Max was strengthened and I0 was revised; the same N holdout was reused. The revised raw scores tied at 8/8. The first apparent N advantage and the later tie are therefore **exploratory**; Claim N's decision-grade status is **BLOCKED** until a new, prospectively frozen test uses fresh contexts.

The B design/data were not changed in the pilot revision: G0 produced 2/4 false activations; CE-updated G1 produced 0/4 while both admitted 2/2 applicable contexts. That is a bounded deterministic toy-fixture pass only—not general boundary-learning evidence or demonstrated harm reduction.

Details: [`S2 plan`](s2_plan.md), [`results report`](results_v1.md), [`revised machine record`](results/keydoor_run_v1.json), and [`v0 pilot audit`](results/keydoor_pilot_v0.md).

## Current interpretation and boundary

This fixture shows that a compact source-derived script can reproduce the simple invariant on the revised cases, while a fixed counterexample update changes the boundary as intended. It does not settle whether N succeeds or fails in a valid independent test; it does not support population, novelty, ARC, task-harm, or cost claims. P1's no-go on generic guard-refinement novelty remains. Under S1.1, do not label this sequence O3 because N is blocked. No further program, ARC work, or S3 is authorized by the current result.
