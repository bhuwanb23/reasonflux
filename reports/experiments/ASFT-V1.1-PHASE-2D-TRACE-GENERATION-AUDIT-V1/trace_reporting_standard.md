# Phase 2D.9 — Trace Reporting Standard

Every future ARC trace run must report, by split, condition, and unique task ID:

## Trace production and validity

- Candidate programs available/generated and candidate trials evaluated, separately.
- Search calls, task IDs, trace records emitted, maximum steps, structural-validator version/hash, valid/invalid traces, and execution failures.
- Successful traces and success rate over both emitted traces and eligible tasks; define exact demonstration-fit rule.
- Partial traces, if supported, with explicit operation/execution evidence; never infer partial work from no-fit.
- Candidate pruning, trace pruning, first-fit skips, and budget-excluded candidates separately.

## Diversity and quality

- Unique trace IDs **and** unique solution/program-context signatures.
- Structural, operation, and template diversity, with operational definitions and entropy/support where appropriate. Semantic family labels must be independently annotated; operator-derived taxonomy is not a substitute.
- Q1 demo fit; Q2 cross-demo consistency; Q3 generality/unseen-input validation only under separately authorized labels; Q4 support across distinct task IDs; Q5 reuse potential distinguished from observed transfer.
- Trace-to-invariant flow: miner inputs, fragments, raw patterns, structures, candidate/rejected invariants, threshold policy, and support distribution.
- State whether metrics use invariant, skill, capability, or accuracy scores; trace-quality metrics must not use them.

## Denominators and interpretation

Report tasks processed, trace records, distinct task IDs, candidate trials, successful task IDs, discovery-only miner inputs, and zero denominators. “Trace generated” is not “successful”; successful is not generalizable; transfer-relevant is not transfer success; high support is not an accepted invariant. Use `NOT_MEASURED`, `NOT_ESTIMABLE`, `NOT_RUN`, `BLOCKED_UPSTREAM`, and `ZERO` distinctly.

Report coverage, transfer, capability, and accuracy in separate fields. If test labels are not authorized/read, state accuracy `NOT_MEASURED` rather than inferring it from trace or coverage metrics.