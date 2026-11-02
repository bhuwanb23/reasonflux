# 1B.4 — Selection Pressure Design

## Fixed-choice environment

- Candidate panel: `N=20` technically eligible candidates per batch; four each of types A–E.
- Creation capacity: `K=8` candidates per selector, fixed before outcomes (`K/N=40%`).
- Evaluation horizon: ten paired task opportunities per candidate lane.
- All policies see the exact same candidate IDs, feature cards, task order, and resource budget. No outcomes or type labels are available at decision time.
- Every contested policy (S1–S5) selects exactly eight candidates (40%, neither 0 nor 100%). S6 NEVER_CREATE is an explicitly required zero-rate anchor and is the sole exception to the nondegenerate selection-rate rule. It cannot satisfy the pressure check. S7 oracle selects eight for ceiling analysis.

The capacity-limited ALWAYS baseline means “accept the first eight technically valid candidates in the frozen candidate ordering.” It does not exceed the common capacity. The ordering is generated independently of candidate type/value and is fixed in the data manifest.

## Selection Divergence Rate (SDR)

For selectors `a,b` with chosen sets `S_a,S_b` and `N=20`:

`D(a,b) = |S_a symmetric-difference S_b| / N`.

The batch contested-selector SDR is the mean of `D(a,b)` across the six pairs among S1–S4 (SCV, frequency, reuse-probability, random). Also report each pairwise value and `D(SCV,j)` for every comparator. This rate is the fraction of candidate-level accept/reject decisions that differ, averaged over selector pairs; it is not a performance metric.

## Pre-outcome pressure gate

A confirmatory batch qualifies only if, **before opening any outcome/type-label file**:

1. N=20, K=8, type counts meet the frozen four-per-type recipe, and all candidates pass the common technical-validity gate.
2. S1–S5 all select exactly 8/20; S6 selects 0/20 by design; S7 selects 8/20.
3. `D(SCV, frequency) >= 0.10`, `D(SCV, p_reuse) >= 0.10`, and `D(SCV, random) >= 0.10`.
4. Contested-selector `SDR >= 0.20`.
5. No selector can read latent type, task outcomes, candidate-level FNV, future task identifiers, or oracle scores.

Gate failure is `PRESSURE_UNAVAILABLE`, not evidence for or against SCV. Do not inspect outcome labels, adjust thresholds, or redraw a batch after a failure. Only predeclared reserve seeds may replace a batch rejected before outcome access; every reserve and rejection is logged. Never replace a batch because an outcome is unfavorable.

## Demonstration fixture

`selection_pressure_fixture.csv` is a hand-computed, ten-candidate **design fixture only** (K=4) showing how the frozen score and signal-only baselines can select different candidates. It includes no held-out outcome labels and is not a pilot, result, or confirmation. The per-batch acceptance assertions above are required for the eventual N=20 confirmatory panels; a fixture does not substitute for implementation contract tests.

## Why this does not leak the answer

The pressure check uses only pre-decision selector outputs from visible features and seeded randomization. The future-value labels and outcome store remain sealed. The benchmark deliberately conditions on a rich, decision-divergent candidate pool because RQ2 asks whether SCV is valuable **when good, bad, and neutral candidates compete**. This does not estimate prevalence-weighted value in an unconstrained deployment stream. Report the balanced-pool scope, and do not sample/curate panels based on observed confirmatory FNV.

## Readiness boundary

Phase 1B specifies the pressure gate and a deterministic worked fixture; no selector code or outcomes are run here. The Phase 4 confirmatory run remains blocked until the implementation passes the pre-outcome gates on development/contract fixtures and hashes the candidate generator, pressure checker, selector implementations, and protocol.