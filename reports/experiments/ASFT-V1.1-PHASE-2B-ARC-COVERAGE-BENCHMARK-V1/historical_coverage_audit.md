# Phase 2B.1 — Historical Phase 13G Coverage Audit

## Purpose and evidence boundary

This is a reconstruction of the saved Phase 13G implementation, configuration, and outputs, supplemented by the Phase 2A source audit. It preserves Phase 13G results; it does not reinterpret a demo fit as accuracy. A separate, test-output-blind Phase 2B coverage-only run is reported in the companion benchmark documents.

## What Phase 13G measured

| Split | Tasks | Saved full-inventory exact demo fits | Rate | Saved `unsupported_v1` | Successful discovery traces |
|---|---:|---:|---:|---:|---:|
| Discovery | 600 | 3 | 0.50% | 597 | 3 |
| Transfer | 200 | 5 | 2.50% | 195 | No discovery trace pool generated for this split |
| Holdout | 200 | 2 | 1.00% | 198 | No discovery trace pool generated for this split |
| **Total** | **1,000** | **10** | **1.00%** | **990** | **3 discovery successes** |

“Exact demo fit” means an enumerated candidate program with inferred parameters exactly replayed all training demonstrations. It does not mean a correct held-out answer, transfer, skill, capability, or ARC task solution. `unsupported_v1` means no candidate fit was found within that bounded implementation; it does not prove semantic unrepresentability.

## Frozen configuration versus executed search

- The Phase 13G configuration declares a per-task budget of **3** from a fixed ten-program order.
- `discover()` has a default of **10** and was called without a budget override. Its discovery traces therefore came from a ten-candidate search.
- Scored transfer/holdout arms use a three-candidate search.
- The coverage scan uses all ten candidates and is diagnostic.
- `solve_task()` stops at the first training-demo fit. It then checks test outputs and returns immediately; a test mismatch does not trigger search for a later demo-consistent candidate.

Therefore the saved discovery trace yield of 3/600 is not a conformant measurement of the declared three-candidate production budget. The saved fullscan demo-fit rates are descriptive bounded coverage, not test accuracy.

## What was and was not measured

**Measured:** split counts; bounded exact demo fits; candidate trials under the particular paths; trace records emitted for discovery; trace success as a demo-fit proxy; exact-match task accuracy in historical scoring paths; invariant/skill/capability activation outcomes. The historical report contains all of these in different tables and denominators.

**Not independently established:** semantic ARC-family representability; the fraction of tasks that a richer representation could express; a clean separation of representation from candidate order/parameter inference/budget; production-budget discovery coverage under one consistent run; an isolated trace validator (the discovery code sets `trace_schema_valid=True`); a test-label-blind coverage execution path (the coverage scan calls `solve_task()`, which computes test outcomes on fit candidates); or causal representation attribution.

## Denominator cautions

- Full-scan demo-fit rate uses all 600/200/200 task IDs as denominators.
- Trace yield 3/600 uses discovery task IDs only and is generated with the ten-candidate `discover()` default.
- Accepted invariant count is zero; three successful discovery signatures each have support one, below the frozen support threshold five.
- Accuracy is a separate task-level outcome in Phase 13G, but was computed in the same solver path. It is not a coverage denominator or a substitute for coverage.
- Transfer precision/eligibility has zero-applicability cases; unavailable/zero-denominator states must not be silently converted to evidence of failure.

The Phase 2B rerun reproduced the saved fullscan demo-fit counts (3/600, 5/200, 2/200) while separately measuring the declared three-candidate mode. It did not alter or overwrite any Phase 13G outcome.