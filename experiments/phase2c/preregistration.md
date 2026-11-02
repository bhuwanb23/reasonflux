# ASFT v1.1 Phase 2C — Frozen Search/Budget Integrity Protocol

**Phase:** `ASFT-V1.1-PHASE-2C`  
**Package:** `ASFT-V1.1-PHASE-2C-SEARCH-BUDGET-AUDIT-V1`  
**Scope:** descriptive search-coverage and runtime-integrity benchmark; not accuracy testing or confirmatory ASFT efficacy evaluation.  
**Status:** protocol, JSON config, and YAML budget registry frozen before execution.

## Research questions

- **R2C-1:** Can a frozen search run be deterministically reproduced? Compare primary and replay ordered candidate-trial fingerprints and selected results for every task/condition.
- **R2C-2:** Do declared, runtime-enforced, and logged budget values match for B1–B6? Any mismatch is a protocol violation and invalidates the benchmark.
- **R2C-3:** How much found-fit coverage changes across search budgets while representation, task IDs, candidate order, inference code, and exact-fit criterion stay fixed?
- **R2C-4:** Can search-budget effects be separated from bounded representation effects? Estimate the paired effect of candidate allowance within this DSL; causal attribution to representation requires a future matched representation factorial.

## Dataset and data isolation

Use the 1,000 ARC-AGI-2 public training task IDs from the frozen Phase 13G split manifest (600 discovery, 200 transfer, 200 holdout). The coverage/search runner parses only the first top-level `train` array and stops before the next field. It does not access test outputs, call `solve_task()`, compute accuracy, or score official evaluation. Each condition uses identical task IDs and training demonstrations. Raw task-file hashes are used for lineage only.

## Frozen search implementation

Keep Phase 13G's ten ordered candidate programs and `infer_context` implementation unchanged. Search is one flat level with no composition. Each program counts as one candidate trial, including all internal parameter inference and exact demonstration replay; no separate operation cost is silently added. Select the first exact demonstration fit and stop; do not backtrack or enumerate later fits. A ten-program scan is unrestricted only relative to the existing finite ten-program DSL.

## Sensitivity conditions

- **S1:** cap 3.
- **S2:** cap 6 (2× S1).
- **S3:** cap 15 (5× S1); the candidate pool contains only ten unique programs, so pool exhaustion occurs before the numeric cap.
- **S4:** `unrestricted` means all ten unique programs in this DSL. No candidate repetition or composition is allowed.

All four conditions are paired on the same 1,000 task IDs. Search traces are emitted once per task/condition (4,000 primary traces), with at most four steps. A separate deterministic replay clears the parameter-inference cache, then searches each task/condition once (4,000 additional search invocations) without emitting duplicate traces. Replay validates search reproducibility, not benchmark sample size.

## Frozen B1–B6 budgets

The YAML registry is the budget source of truth and must match `config.json`:

- **B1 candidate budget:** condition cap (3, 6, 15, or unrestricted/all-10); log requested cap, enforced cap, unique candidate pool, and actual trials separately.
- **B2 search depth:** one flat program; composition off.
- **B3 trace budget:** one primary trace per task/condition, maximum four steps; zero replay traces.
- **B4 runtime:** 30 seconds per individual primary/replay task-condition search; observe and fail closed on cap breach.
- **B5 memory:** 2,048 MiB process address-space limit, enforced using the OS resource limit and logged with peak RSS.
- **B6 evaluation:** 1,000 primary task IDs and 1,000 replay task IDs per condition; 2,000 search invocations per condition, 8,000 total. No test labels or test-output evaluation budget is allocated.

At runtime, every primary log row records its condition's declared and enforced values, actual candidate trials, trace counts, depth, wall time/cap, memory cap, and evaluation budget. The audit record independently checks config ↔ registry ↔ runtime ↔ log parity.

## Search and trace metrics

Report unique candidates available/generated, candidates evaluated, candidate slots excluded by the budget, candidates not evaluated after first-fit stopping, candidates pruned, traces generated, valid traces, successful traces, traces pruned, invariant candidates, candidate trials, runtime, and coverage. Current Phase 13G has no trace pruning, so trace-pruned count is zero; do not relabel first-fit-skipped candidates as pruned. Run the actual Phase 13G TraceMiner on successful discovery traces under support 5/consistency 1.0.

## Integrity and stop rules

Compute hashes for config, registry, executed runner/runtime source, candidate-trial log, task-condition search log, replay log, and the budget audit record. A deterministic replay mismatch; hash mismatch; budget mismatch; task/split mismatch; trace schema/replay failure; timeout; or memory-cap failure automatically sets `protocol_violation`, invalidates result interpretation, and prevents a PASS. Preserve all primary/replay logs. Fullscan is diagnostic only.

## Interpretation ceiling

Increases in found demo-fit coverage under fixed representation provide evidence that search allowance affects coverage in this implementation. Flat coverage across budgets is consistent with (but does not prove) a representation ceiling. No pattern here alone establishes a causal representation bottleneck; changing representation, inference, candidate order, parameterization, or support threshold is a separate preregistered factor. Accuracy remains separate and unmeasured.