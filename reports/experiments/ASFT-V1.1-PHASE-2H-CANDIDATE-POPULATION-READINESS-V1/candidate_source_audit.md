# Phase 2H.1 — Candidate Source Audit

## Question and result

**Question:** What exact objects are intended for IDT ranking, and which available ARC pipeline stages can supply them?

**Answer:** Under Phase 1C and the production R1 implementation, the intended ranked object is an **invariant candidate** (a unique `Invariant` hypothesis produced from recurring reasoning structure), represented by a candidate card with calibration-only features. It is not a raw trace, solver program, or downstream skill. In the audited ARC path, the production candidate generator supplied **zero accepted invariant candidates**.

## Actual pipeline and source map

The production trace-mining path is: `ReasoningTrace` collection → normalization → `TraceFragment` segmentation → `MinedPattern` extraction → `AggregatedStructure` aggregation → `Invariant` candidate generation → validation/ranking/promotion → downstream `SkillCandidate`/`Skill` → later capability construction.

| Possible source | Exists in audited ARC records? | Current R1 candidate? | Assessment |
|---|---|---|---|
| Reasoning traces | Yes; records are emitted for tasks, including no-fit cases | No | Training/evidence material; not a stable candidate identity. |
| Trace fragments | Yes; e.g. 30 historical fragments and 10/20/30/30 in the four S1–S4 discovery inputs | No | Segmented operation n-grams; recurrence is not semantic invariant validity. |
| Mined patterns | Yes only under relaxed support in some conditions; four recurring signatures appear | No | `pattern_mining.py` explicitly says patterns are not invariants. The recurring content is generic schema/search/verification scaffolding. |
| Aggregated structures | Two per relaxed historical/S2/S3/S4 condition; zero under current support | No | Intermediate grouping of patterns; both relaxed proposals fail candidate rejection. |
| Invariant proposals | Two in each relaxed condition; none at current/strict support | **Intended object, but rejected** | Every proposal is rejected as `universal_noise`; accepted count is zero. |
| Validated/promotable invariants | None in audited ARC path | No current rows | Downstream validation/promotion does not receive an accepted candidate pool. |
| Skill candidates / skills | None in audited ARC results | No | Downstream of invariant validation; substituting them changes the ranked construct and policy question. |
| Capabilities | None in audited ARC results | No | Even later/downstream aggregate; not an invariant candidate. |
| ARC search programs | Yes, as Phase 2C program trials | No | Solver hypotheses evaluated against demonstrations, not trace-derived invariant objects. The trial ledger is not a candidate registry. |

The row-level source classifications are in `candidate_source_audit.csv`.

## What the evidence establishes

- Phase 2B records zero C4 invariant candidates in the 1,000-task budgeted and fullscan conditions; downstream stages are blocked/not reached.
- Phase 2E's support-floor audit confirms zero accepted candidates for Phase13G historical data and S1–S4 at current/strict thresholds. Relaxing support to two produces two proposals in some conditions, but both are rejected as generic universal-noise patterns.
- Thus the current production ARC R1 path does not presently furnish a nonzero eligible invariant population. This is a substrate/readiness failure, not an R1 ranking or FNTU result.

## Scope limit

This audit does **not** establish that IDT can never generate candidates on ARC, or that all possible task/task-family sources have been explored. It establishes that the saved, audited bounded ARC pipeline and its current candidate policy produced no accepted invariant candidate pool. No new ARC search or relaxed-threshold experiment was run in Phase 2H.