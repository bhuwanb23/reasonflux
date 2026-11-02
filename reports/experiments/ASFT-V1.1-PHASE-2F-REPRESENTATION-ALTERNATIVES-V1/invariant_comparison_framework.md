# Phase 2F.6 — Invariant Comparison Framework

## Frozen downstream pipeline

For all representations, hold the Phase 2E TraceMiner, normalizer/segmentation policy, candidate generator, rejection policy, invariant validator, and support rules fixed. Current frozen values are min-frequency 5, min-cross-trace 5, consistency 1.0, and at least two task families. Because Phase 2E found family labels derived from selected programs non-independent, the next comparison must use one shared, outcome-blind task-family annotation; otherwise the family-dependent gates are `UNAVAILABLE` and cannot be interpreted as comparable.

## Stage metrics

Per representation and condition, report:

1. successful discovery traces input;
2. fragments and unique operation signatures before thresholds;
3. support distribution by distinct task IDs before validation;
4. raw patterns after support filters;
5. aggregated structures;
6. candidate proposals before rejection, accepted candidates, and named rejection reasons;
7. validator inputs, scores/states, validated, transfer-verified, and rejected/blocked counts;
8. unique invariant signatures and support across tasks;
9. `candidate → accepted invariant` and `invariant per task/trace` yields with explicit denominators.

A no-candidate condition has validator survival `NOT_ESTIMABLE_ZERO_CANDIDATES`, not 0%. Report both raw representation-specific signatures and any pre-frozen common canonical mapping. Repeated trace-control steps are patterns until independently grounded as a task rule; a miner enum or `VALIDATED` software state is not truth evidence.

## Comparison and interpretation

Compare R1 vs the registered alternative on identical discovery task IDs under the same support thresholds. Report paired differences and interval estimates for candidate/validated-invariant yields, exact support distribution, and conditional survival. Do not relax thresholds for one arm. A separate threshold factor requires new preregistration and multiplicity handling. Invariants and accuracy/transfer/capability remain distinct. A representation that increases coverage but yields only singleton patterns has not activated invariant discovery.