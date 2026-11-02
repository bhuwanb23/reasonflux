# Phase 2D.1 — Historical Phase 13G Trace Audit

## Reconstruction

Phase 13G processed **600 discovery task IDs**. Its `discover()` path emitted one serialized `ReasoningTrace` per task after a ten-candidate main search (the declared config budget was three). It also ran ten demonstration-order stability searches per task; those 6,000 extra searches did **not** emit extra traces.

| Historical stage | Count | Rate / status |
|---|---:|---|
| Discovery tasks processed | 600 | denominator |
| Candidate program slots in main discovery | 6,000 | 10/task; static ten-program DSL |
| Main candidate trials recorded in trace outcome costs | 5,989 | max 10/task |
| Stability searches | 6,000 | 10/task, cap 10; original per-permutation trial logs absent |
| Serialized trace records | 600 | 1/task |
| Retrospectively structurally valid serialized records | 600 | 100%; validated in Phase 2D from saved records |
| Generation-time trace validator established | — | **No**; `trace_schema_valid=True` was hard-coded |
| Successful traces / exact demonstration fits | 3 | **0.50% of tasks / emitted records** |
| Valid but unsuccessful no-fit traces | 597 | 99.50% |
| Successful traces supplied to TraceMiner | 3 | success-only filter |
| Fragments / raw patterns / structures | 30 / 0 / 0 | saved mining summary; re-run exactly reproduced |
| Invariant candidates / skills | 0 / 0 | no candidate reached later stages |

The retrospective structural check establishes that the **saved serialized records** parse and match the trace schema; it does not establish that a runtime validator existed during Phase 13G execution. The three successful records were independently replayed against their training demonstrations in Phase 2D; all three fit exactly. No test outputs were used for this audit.

## What passed through the lifecycle

`discover()` produces a trace even when no program fits. Thus “trace generated” (600/600) is not “successful trace” (3/600). `mine_invariants()` filters its input to traces with a successful outcome, so **597 records never entered invariant mining**. The miner received three success traces, generated 30 fragments, then zero raw patterns, structures, or candidates. No skill or transfer stage could be meaningfully assessed from this pool.

The three successful discovery program signatures were `reflect_vertical`, `rotate_270`, and `recolor_bijection`, each with support one. The frozen invariant policy requires minimum frequency/cross-trace support five, consistency 1.0, and at least two task families. The observed trace set is plainly below the recurrence floor.

## Interpretation boundary

Phase 13G did not distinguish whether the absent invariants resulted from too few successful traces, low trace/signature diversity, the support/family policy, or miner behavior on an adequate positive-control corpus. Its `trace_schema_valid` flag is not validation evidence. The Phase 2D retrospective checks repair auditability of saved artifacts only; they do not alter Phase 13G outcomes or prove that the miner works when supplied sufficient traces.