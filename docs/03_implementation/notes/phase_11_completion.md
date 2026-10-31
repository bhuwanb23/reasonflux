# Phase 11 — Completion Notes

Phase 11 is complete: all 24 modules implemented, all six MVP gates demonstrated,
no `NotImplementedError` in `src/`. 501 tests pass.

## What was added to close the gap

Before this phase every module was a library but nothing produced experience, so
all evidence came from synthetic scenario data in
`src/evaluation/harness/scenarios.py`.

### New subsystem: `src/solver/`

- `grid.py` — immutable `Grid`, pure ops (reflect, rotate, count, group).
- `tasks.py` — deterministic `make_task(family, seed, difficulty, variant, compose)`.
- `executor.py` — `GridSolver` that proposes readings, executes one, verifies.

The solver never reads `expected` while building steps; verification is the only
place the answer is consulted, so traces stay honest learning material.

### The 14 former stubs

`TraceLogger`, `TraceStore`, `trace_similarity`, `cluster_traces`, `compute_is`,
`ReuseEngine`, `get_logger`, `plot_metric`, and the four pipelines.
`run_full_asft_pipeline` is the single end-to-end entry point.

## Design decisions worth remembering

### Trial-then-confirm, not evidence-first promotion

Mining cannot produce transfer evidence — transfer is a property of *applying* a
skill. So Phase C admits a skill as a **provisional trial** (state `PROMOTED`,
`metadata["provisional"]=True`) that Phase D then measures. Only a correct *and*
cheaper reuse confirms it to `ACTIVE`.

This was the single hardest design point. The naive alternative — writing a
trace-derived transfer prior into `transfer_contribution` — made the pipeline
work immediately but was circular: one trace statistic was counted as generality,
transfer contribution, transfer score and TV simultaneously. Zeroing that value
dropped ASFT below its own DreamCoder baseline, which proved the headline result
was an artifact.

### Containment rule for priors

Priors live in `metadata` only (`prior_transfer`, `prior_reasoning_value`) and are
never written to `transfer_contribution`. Provisional skills are excluded from
`C_t` and `IG` by `_scored_library`, so a prior can never inflate a reported
score.

### Transfer must be correct *and* cheaper

`ReuseResult.transfer_credit` requires `applied and success and benefit > 0`.
Macro steps are priced at the real cost of the steps they replace, so a saving
comes from skipping work rather than from an asserted discount. Failures are
recorded via `record_negative`, so NTR is not structurally zero.

### Cross-family transfer must be a real invariance

`_invariance_holds` requires whole-grid horizontal symmetry (all rows
palindromic), not `any(row == reversed(row))` — which is true for nearly every
mostly-empty grid and previously let a no-op reflection "transfer" to counting.

### Growth measured over accumulated experience

The library is carried forward across rounds; rebuilding it each round discards
reuse and transfer evidence and makes growth impossible by construction.

## Bugs found and fixed after review

A Python-review pass found several results were inflated by real defects. Each
was verified before fixing:

1. **Circular import** — `import transfer` failed cold
   (`transfer.gate → invariants.validation.scores → invariants/__init__ →
   robustness.hard_gate → transfer.gate`). `ValidationScores` is annotation-only
   there, so it moved under `TYPE_CHECKING`. A regression test imports each
   pipeline in a fresh interpreter.
2. **skill_storage baseline always scored 0.0** — read `metadata["mvp_category"]`
   which invariants never carry. Now uses `classify_mvp_category`.
3. **DreamCoder baseline labelled everything "reflection"** — matched on any
   shared op (`detect_object` is in every family). Now matches the discriminating
   op.
4. **Transfer credit was just "correct"** — a 0.25× macro discount made every
   correct reuse cheaper by construction. Now priced at real replaced cost.
5. **Cross-family macro was a no-op** — `_apply_macro("apply_reflection", grid,
   "counting")` returned the grid unchanged yet earned credit.
6. **Pipeline bypassed the validator's T/R verdict** — recomputed `promotable`
   from `validated` and walked to `TRANSFER_VERIFIED` while writing
   `transfer_verified=False`. Removed; replaced by the explicit trial-then-confirm
   path.
7. **Path traversal in `TraceStore`** — `_safe("..")` returned `".."`. Now
   collapses dot-segments and asserts every resolved path stays under the root.
8. **`run_skill_pipeline` discarded a caller's empty library** — `library or
   SkillLibrary()` with a falsy (empty) library. Now `is not None`.
9. **Two tests could silently assert nothing** — guarded by `if` on the failure
   path. Now assert the precondition first.

## Remaining limitations (must appear in the paper)

- Tasks are synthetic grids, not ARC. Mechanism demonstrated; external validity is
  Phase 13.
- One capability cluster at this scale; growth is mostly skill accumulation.
- Single seed, four rounds; paper-grade evidence needs multiple seeds and CIs.
- The A1–A5 ablation table is not yet in `exp05`.

## Artifacts

`reports/metrics/` — exp01, exp02, exp03, exp05 JSON + Markdown.
`reports/figures/` — IS by invariant, transfer benefit, capability growth.
