# ARC Root-Cause Analysis

## Finding

The dominant proximate failure in Phase 13G is the **bounded task/program representation and coverage layer**, followed by a support-threshold bottleneck that makes invariant/skill formation impossible in the observed pool. This is a strong diagnosis of the *tested implementation path*, not proof that this is the unique root cause of ARC difficulty or that richer representation would validate ASFT theory.

## Evidence chain

1. The solver had ten hand-specified primitive program families: identity, horizontal/vertical reflection, three rotations, transpose/anti-transpose, constant translation, and bijective recoloring.
2. A full-inventory demonstration fit exists for 3/600 discovery tasks, 5/200 transfer tasks, and 2/200 holdout tasks. These are training-demo fits, not exact test-task accuracy.
3. Only three discovery traces fit demonstrations; the supported programs are reflection, rotation, and recoloring—one task each, with order stability 1.0 for each of the three.
4. The invariant miner sees only successful traces, is configured with `min_frequency=5` and `min_cross_trace=5`, and finds zero raw patterns/candidates. Per-program support is one, below `MIN_SUPPORT=5`; eligible program and ASFT skill lists are empty.
5. Skill qualification also expects at least three applicable transfer tasks. With no invariant/skill candidates, learned-skill transfer precision is null (zero denominator); no capabilities or CGM outputs are available.

## Root-cause confidence

- **Strong:** the fixed DSL is grossly under-covering the task distribution under its own exact-demo-fit test.
- **Strong:** the downstream minimum-support gate and the three successful examples interact to block invariant formation in this cohort.
- **High:** the three-candidate scored-arm budget and fixed ordering further reduce reachable programs beyond the full ten-program coverage scan.
- **Critical audit discrepancy:** frozen config declares a three-candidate per-task budget, but `discover()` defaults to ten; the reported discovery fit yield therefore reflects a more permissive scan. Only the reflection fit among the three successful discovery programs lies in the first three fixed candidates. This finding comes from saved source/results, not a rerun.
- **Not established:** whether IDT would work on richer recurrence-bearing ARC traces; whether the current invariant miner is sufficient after coverage expands; whether ARC “difficulty” is independent of representation mismatch.

## Important qualification

All 600 discovery rows are marked schema-valid; the trace serializer did not fail on 597 tasks. The issue is that most traces document a failed DSL search, not successful semantic traces. The precise claim is **program/task representation coverage failure**, not a generic trace-format failure.
