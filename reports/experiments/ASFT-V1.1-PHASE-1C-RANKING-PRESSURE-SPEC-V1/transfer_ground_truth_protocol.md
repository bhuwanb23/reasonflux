# Phase 1C.6 — Transfer Ground-Truth Protocol

## Definition

A candidate transfers when applying it to a task from a **disjoint future task family/template block** yields a positive paired task-utility difference relative to the same solver with no candidate, after frozen cost treatment. `TransferValue_i` is the mean paired net utility over the preregistered future opportunities; portfolio value is evaluated jointly as defined in [`future_value_definition.md`](future_value_definition.md).

Transfer truth is generated from actual held-out task execution or, for synthetic contracts only, from a separate latent outcome process. It is never defined as IDT's `T`, `ITS`, `TU` calibration score, frequency, reuse probability, compression gain, or candidate label.

## Calibration and outcome separation

1. Use calibration episodes only to compute R1's transfer input and the other public candidate features.
2. Development episodes may be used to test runner correctness, estimate variance, and finalize the generator/preregistered N. They cannot provide the confirmatory outcome labels.
3. The confirmatory future-task suite is generated/identified and hashed before ranks; its outcomes remain in a separate store.
4. Freeze candidate pool, ranker full orders, Top-K lists, RDR gate, K, endpoint code, and run manifest; then produce a signed lock record.
5. Only after lock may an authorized evaluator open the outcome store, compute R6 Oracle, and score all five policies and Oracle together.
6. Replication uses disjoint family/template blocks and task instances; no tuning based on confirmatory or replication outcomes.

## Held-out transfer opportunities

- The protocol fixes H future opportunities per panel and a common family mix before ranker execution.
- Every selected portfolio is evaluated on the same opportunities, with equal time/compute limits and identical no-candidate counterfactuals.
- A not-applicable candidate/task pair has zero candidate benefit under the frozen rule; a failed application receives the frozen failure utility; a system/data omission is missing and remains distinct.
- The primary transfer score is cross-family. Same-family/local reuse is reported separately and cannot substitute for transfer.
- Exact task-family rules, executable versions, evaluator hashes, seeds, counterfactual treatment, and score conversion must be pinned in the later run manifest.

## Oracle handling

Oracle ranks by the final held-out future value only after ordinary methods and their pressure diagnostics are locked. It is an upper-bound diagnostic, not a feasible policy or primary comparator. If any Oracle output leaks into card fields or ranker tuning, invalidate that run and report the breach.

## Limitation

The Phase 1C fixture harness uses a synthetic truth dictionary keyed by opaque IDs only to verify metric response and pressure separation. It does not execute independent task solvers, create a sealed production store, establish transfer construct validity, or produce confirmatory evidence.