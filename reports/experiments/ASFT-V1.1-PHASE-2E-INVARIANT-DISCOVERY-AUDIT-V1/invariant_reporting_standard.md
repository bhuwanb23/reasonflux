# Phase 2E.9 — Invariant Reporting Standard

Every future ARC invariant-discovery run must report, by frozen condition and discovery split:

## Input and recurrence

- Tasks processed, trace records, successful traces passed to the miner, failure/no-fit traces excluded, and unique task IDs.
- Trace normalization and segmentation version/hash; fragment occurrences and per-trace deduplication rule.
- Exact signature frequency by **distinct successful trace/task ID**, task coverage, cross-task support, and full support distribution **before validation**.
- Independent semantic-family annotations and their provenance; distinguish operator/solution-derived labels from independent task taxonomy.

## Pipeline stages

- For each stage: raw fragments, recurring patterns, aggregated structures, candidate proposals before filters, accepted candidates, rejected candidates with reason, validated invariants, transfer-verified invariants, and promotable invariants.
- State all thresholds separately at extraction, candidate policy, and validation: frequency, cross-trace support, consistency, family count, generality, and transfer/utility criteria.
- Candidate yield per successful trace; trace→pattern, pattern→structure, structure→candidate, candidate→validated, and validated→transfer-verified survival rates. Use `NOT_ESTIMABLE_ZERO_DENOMINATOR` when no candidate reaches a stage.

## Validation and interpretation

- V1 consistency and its source traces; V2 generality on an independent, predeclared task/family split; V3 stage survival; V4 false-discovery assessment against independent truth labels or an explicitly authorized method.
- Keep same-corpus diagnostic validator runs clearly separate from production candidate flow; never treat a structural F-C-G state, miner enum, frequency score, or hand-built fixture as proof of semantic truth.
- If FDR or generality cannot be independently assessed, state `NOT_ESTIMABLE`/`NOT_MEASURED`; do not report zero.
- Report invariant results separately from coverage, transfer success, skill promotion, capability, and accuracy. No performance or mechanism claim without a named comparator and identical conditions.