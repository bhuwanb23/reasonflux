# Phase 13F preflight — PHASE-13F-BASELINE-ABLATION-V1

**Status:** frozen before confirmation. **Confirmation seed block:** 70–79 (replacement block). **Output:** `reports/experiments/PHASE-13F-BASELINE-ABLATION-V1/`. Attempt 01 partially executed seed 0, then stopped on a missing Phase 13E metric-config field before any records/report were saved; it is preserved separately and excluded. No Phase 13C/D/E benchmark was replayed. The frozen confirmation block is 70–79, selected before inspecting any outcome records.

## Frozen operationalization

- 24 arms: ASFT; B1–B4; IDT/SCT/CGM and cross-component ablations; six prespecified SCV, invariant-strength, and composition sensitivity variants.
- B2 is a raw episodic skill-memory comparator: it stores executable trace episodes and consumes no invariant candidates, SCV selection, capability formation, or composition. B4 is only a transparent compression proxy; no canonical DreamCoder implementation is claimed.
- Baseline task streams and non-SCV eligible candidate pool are paired within seed. B3 uses a fixed 75% random sample; A2.1 matches the ASFT candidate count; A2 creates the entire eligible pool.
- IS means invariant strength. SU, TS, CGR, and IG retain repository definitions; CGR/IG use the Phase 13E-frozen pathway and weights. Missing/ill-defined values remain unavailable.
- A3 removes the capability layer; A3.1 masks growth measurements while preserving behavior; A3.2 reports capabilities independently; X4 keeps the measurement pathway but blocks formation.
- Phase 13C frozen q25/q75 SCV points are used as sensitivity points, not new confirmatory thresholds. Invariant strength points are 5/7.5/10. Composition points vary only validation/promotion requirements.

## Verification before freeze

`PYTHONPATH=src:. python -m pytest -q tests/test_phase13f_contracts.py` — **11 passed**. `compileall`, JSON validation, `git diff --check`, and source line counts passed. No Phase 13F outcome package existed. The run CLI requires explicit `--confirm`, writes a pre-run frozen manifest, refuses output overwrite, and preserves previous phases.

## Caveats recorded before outcomes

Phase 13C previously found its Bernoulli random-create probability degenerated to 1.0; Phase 13F uses a distinct fixed-budget random selection policy and does not rewrite the earlier finding. X3 is limited by the current one-shot discovery design and can be behavior-matched; interpret it only as a test of post-creation trace retention. Synthetic results are not ARC external validation. Expected direction is not a pass criterion.
