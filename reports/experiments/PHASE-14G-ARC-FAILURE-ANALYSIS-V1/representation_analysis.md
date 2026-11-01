# Representation Analysis

## Separate three notions of “representation”

1. **Grid/task ingestion:** the public task files were loaded and basic rectangular/color-domain checks were applied. No evidence indicates a general file-format ingestion failure.
2. **Trace schema:** Phase 13G saved 600 discovery trace-quality rows with `trace_schema_valid=True`. Failed searches are represented as `candidate_budget_exhausted`/`no_exact_fit`; this is not the same as a successful reasoning trace. Three successful exact-fit traces were stable under ten demonstration-order permutations each.
3. **Task/program expressivity:** the DSL has ten fixed primitive programs. Only 3/600 discovery tasks fit its full inventory. Concepts including counting, grouping, object detection, and pattern completion were not operationalized. This is the dominant representation bottleneck.

## Why the invariant stage remained empty

The three successful programs are `reflect_vertical`, `rotate_270`, and `recolor_bijection`, each supported by one discovery task. The miner only receives successful traces and requires minimum frequency/cross-trace support of five; skill support is also five. The run records `raw_patterns=0`, `structures=0`, `candidates=0`, `rejected=0`. This indicates no candidate population reached acceptance/rejection—not a failed contest among multiple ARC hypotheses.

## Candidate budget and routing

Full-coverage scans test ten DSL programs, while the main transfer/holdout arms use a three-candidate limit. A source/config discrepancy matters: the frozen config declares a per-task limit of three, but `discover()` defaults to ten. Therefore the 3/600 successful discovery yield reflects the full inventory, not the declared three-trial budget. Of those three observed fits, only `reflect_vertical` is within the first three fixed programs. This is an inference from the saved fixed order and results, not a rerun. Since `eligible_programs=[]` and `ASFT_programs=[]`, ASFT falls back to fixed order. B3/B4 also have no eligible support-qualified operators. The B2 memory policy retrieves a nearest episode and can place its program first. This design makes program order and budget consistency part of the outcome, not just language expressivity.

**Verdict:** strong support for a task/program representation and coverage bottleneck; no support for a generic trace-serialization failure. The broader trace-to-invariant representation question remains open because the successful ARC trace sample is too small and operation-specific.
