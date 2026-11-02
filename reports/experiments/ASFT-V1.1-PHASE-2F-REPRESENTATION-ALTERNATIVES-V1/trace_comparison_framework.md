# Phase 2F.5 — Trace Comparison Framework

## Common trace contract

Each task-condition emits at most one primary `ReasoningTrace`, including no-fit attempts. A four-step high-level trace has: (1) input validation; (2) representation construction/parsing; (3) candidate enumeration/application summary; (4) exact training-demonstration verification. The detailed candidate-trial ledger is separate, so compact traces do not hide evaluated or skipped work. A versioned independent validator must check IDs, task linkage, step schema, outcome consistency, and representation version at generation time.

A candidate failure is not a partial trace unless executed, incomplete reasoning steps are explicitly recorded. A valid no-fit trace is not a successful trace. Parser failure, invalid input, no candidate, budget exhaustion, trace invalidity, and successful exact demo fit have separate statuses.

## Endpoints

For each representation and split, report:

- trace records generated / eligible tasks;
- structurally valid and invalid traces with validator version;
- successful exact-demo-fit traces and rate over tasks and generated traces;
- parse failures, no-fit, budget-exhausted, and ambiguous-fit counts;
- step count, operation/event sequence, candidate trials, trace signature distribution, support across distinct task IDs, diversity/entropy, and missing/duplicate trace IDs;
- demonstration-only consistency among selected candidates; generality beyond demonstrations is unavailable unless separately authorized and test-blindly measured.

Compare paired task-level trace-success rates and valid-trace rates with numerators, denominators, discordant counts, and predeclared paired intervals. Diversity metrics must not use invariant, skill, capability, or accuracy scores.

## Cross-representation trace semantics

Store raw operation IDs plus representation-qualified IDs and parameters. Freeze any representation-neutral canonical mapping before evaluation; report raw and mapped recurrence separately. No post-outcome mapping of an alternative primitive to an R1 primitive. If no defensible equivalence exists, compare yield/support counts but mark cross-representation signature identity `NOT_COMPARABLE`.

Use the same discovery task IDs and the same invariant support policy downstream. Family labels must be a shared independent annotation; selected-program labels are prohibited as independent semantic families. If unavailable, report family-breadth eligibility as `UNAVAILABLE`, not zero.