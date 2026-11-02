# Phase 2C.8 — Search Reporting Standard

Every future ARC search run must publish a per-condition, per-split report and machine-readable task logs with the following fields.

## Configuration and budget parity

- Run ID, code/runtime hash, config hash, budget-registry hash, dataset and split-manifest hashes.
- B1 requested candidate budget, effective/enforced cap, unique pool available, candidates generated, candidates evaluated, actual trial count, budget-unavailable candidates, first-fit skipped candidates, and pruned candidates as separate fields.
- B2 search depth, grammar/composition status, program order, ranking and termination rule.
- B3 trace cap, emitted/valid/successful/pruned trace counts, steps/trace, schema validator version, and IDs/hashes.
- B4 declared wall-clock cap and observed per-task/run elapsed times; timeout counts.
- B5 declared memory cap and enforcement mechanism plus observed peak memory.
- B6 task-ID/evaluation budget, split denominators, primary/replay invocation counts, and test-label access scope.
- Runtime/logged/declared values must match or the run is labeled `PROTOCOL_VIOLATION` and excluded from substantive interpretation.

## Search and outcome metrics

Report unique tasks; candidate generation/evaluation counts; exact-demo-fit coverage count/rate; trace-emission and independent-validation rates; successful trace count/rate; candidate/trace pruning (or explicit zero/not implemented); invariant candidates/support; stage transition counts; replay consistency; runtime and memory. Publish task-level search and candidate-trial logs, not aggregate metrics alone.

## Accuracy separation

Report task accuracy in a distinct section with its own frozen endpoint, eligible task IDs, denominator, test-pair count, scoring code/hash, and evaluation authorization. If not measured, state `NOT_MEASURED`. Never use accuracy as coverage, treat a no-fit as incorrect accuracy, merge coverage and accuracy, or claim fullscan as performance.

## Status semantics

Distinguish measured zero, not applicable, unavailable, not run, blocked upstream, and protocol violation. Zero denominators yield `not_estimable`. Budget caps, unique candidate pool size, realized candidate trials, and replay work must not be collapsed into one “search budget” number.