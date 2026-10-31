# Phase 11 — Completion Notes

Phase 11 is complete: all 24 modules implemented, all six MVP gates demonstrated,
no `NotImplementedError` left in `src/`. 500 tests pass.

## What was added to close the gap

Before this phase, every module was a library but nothing produced experience, so
all evidence came from synthetic scenario data in
`src/evaluation/harness/scenarios.py`.

### New subsystem: `src/solver/`

- `grid.py` — immutable `Grid`, pure ops (reflect, rotate, count, group).
- `tasks.py` — deterministic `make_task(family, seed, difficulty, variant, compose)`.
- `executor.py` — `GridSolver` that proposes readings, executes one, and verifies.

The solver never reads `expected` while building steps; verification is the only
place the answer is consulted, so traces remain honest learning material.

### The 14 former stubs

`TraceLogger`, `TraceStore`, `trace_similarity`, `cluster_traces`, `compute_is`,
`ReuseEngine`, `get_logger`, `plot_metric`, and the four pipelines.

`run_full_asft_pipeline` is the single end-to-end entry point.

## Design decisions worth remembering

- **Cross-family recurrence is structural, not contrived.** Counting and grouping
  grids are sometimes symmetric; the solver emits a real `find_symmetry` step on
  them. That is why reflection structure reaches generality 0.75 across three
  families without hand-tuning.
- **SCT priors are trace-derived.** Mining correctly leaves transfer at zero
  (it is a future claim). `invariants/sct_priors.py` supplies the smallest honest
  prior from observed data — pattern length / mean trace length, and cross-family
  support — and never overwrites a measured transfer score.
- **Growth is measured against accumulated experience.** The library is carried
  forward across rounds; rebuilding it each round would discard reuse and transfer
  evidence and make growth impossible by construction.
- **Transfer requires correct *and* cheaper.** `ReuseResult.transfer_credit`
  demands both. Incorrect reuse earns nothing, which is what keeps the transfer
  numbers defensible.
- **Success is judged against the trough, not the first reading.** Introducing a
  harder mechanism legitimately depresses capability before recovery.

## Bug found and fixed

`import transfer` failed cold with a circular import:
`transfer.gate` → `invariants.validation.scores` → `invariants/__init__` →
`robustness.hard_gate` → `transfer.gate`. `ValidationScores` is only used in
annotations there, so it moved under `TYPE_CHECKING`. A regression test now
imports each pipeline in a fresh interpreter.

This was a pre-existing defect flagged as a risk earlier; it was latent because
tests always imported `invariants` first.

## Artifacts

`reports/metrics/` — exp01, exp02, exp03, exp05 JSON + Markdown.
`reports/figures/` — IS by invariant, transfer benefit, capability growth.

## Known limitations

- Tasks are synthetic grids, not ARC. The mechanism is demonstrated; external
  validity is Phase 13.
- Runs are small (minutes). Paper-grade evidence needs more seeds and CIs.
- `exp05` reports baselines but not the A1–A5 ablation table yet.
