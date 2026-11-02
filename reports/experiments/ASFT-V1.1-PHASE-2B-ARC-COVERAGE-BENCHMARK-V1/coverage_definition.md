# Phase 2B.2 — Frozen Coverage Definition

## Primary definition

For task *i*, frozen representation *R*, search procedure/order/parameter inference *S*, and candidate budget *B*:

> **Operational coverage** is 1 if and only if the specified finite search finds at least one candidate whose inferred parameters reproduce every available training demonstration exactly within budget *B*; otherwise it is 0 for that run.

For a task set of *N* eligible task IDs, coverage is `sum(C1_i) / N`. Report numerator, denominator, percentage, representation version, parameter-inference version, program order, search budget, and runtime cap together. Budgeted (3-candidate) and diagnostic fullscan (10-candidate) rates are separate estimands.

This definition measures **found demo-fit coverage** for a representation-plus-search condition. “Representable” is shorthand for this finite operational result, not an oracle claim that all possible programs in the DSL have been searched.

## Explicitly not coverage

Coverage is not a correct held-out/test answer, task accuracy, transfer success, invariant acceptance, skill promotion, capability formation, ARC-family prevalence, Kaggle/leaderboard score, or evidence of intelligence. Those are distinct outcomes and, where applicable, use separate procedures and denominators.

## No-fit and unavailable rules

- No fit within the bounded candidate set, parameter heuristics, ordering, and budget → `no_fit_found_within_condition`; **not** “semantically unrepresentable.”
- If a stage is blocked because its upstream candidate pool is empty, report `0 reached` over the all-task denominator **and** mark the downstream conditional rate `not_estimable` when the prior-stage denominator is zero.
- If a measurement was not run or its output is unavailable, report `unavailable`/`not_run`, never numeric zero.
- A zero denominator is not a zero score.

## Independence from accuracy

The Phase 2B coverage runner parses only each task's `train` array and stops before the next top-level field. It uses no held-out/test outputs, does not call the Phase 13G `solve_task()` path, and computes no accuracy. The separate raw-file hash audit verifies source integrity only; hashes are not labels or scores.

Coverage and accuracy may be placed side-by-side in a report only as separately named measures. They may not be added, averaged, substituted, or interpreted as one another.