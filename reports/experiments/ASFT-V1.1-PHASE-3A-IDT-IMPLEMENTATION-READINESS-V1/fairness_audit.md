# Phase 3A — Fairness and Comparability Audit

## Common comparison conditions checked

- R1–R5 rank the same unique candidate IDs and return full orders for the same pool.
- Every method is evaluated at the same K=8; the endpoint interface requires exactly K unique selections from that pool.
- R2 reads only normalized frequency; R3 only reuse probability; R4 only compression gain; R5 candidate IDs and seed; R1 F/C/G/T/R from the public card and calibration transfer memory.
- Top-K comparison uses complete candidate orders, not incompatible raw score magnitudes.
- The endpoint enforces exactly the same H task IDs and paired no-candidate baseline across policies, and requires an identical task horizon.
- The primary portfolio cost is fixed across each policy's horizon; the frozen cost model and λ must be common to all methods.
- Oracle is explicitly excluded from the policy competition, budgets, pressure gate, and primary contrasts.

The implementation contracts verify shared pools, K selections, order-invariant replay, and paired endpoint arithmetic. The Phase 1C specification also requires equal evaluator, compute/time limits, visibility, retries, and no extra task feedback; those conditions are not exercised because no real evaluator/task runner exists.

## Feature visibility and unresolved production checks

The common card is supplied to a shared engine call, but each scorer accesses only its specified field(s); the interface/schema does not supply outcomes or latent labels. This is a code-path check, not an independent process-level visibility audit. No production ranker snapshots, feature source hashes, budget telemetry, retry logs, evaluator version, or policy-specific information-access logs were available.

R1's richer input is its defined calibration transfer evidence; it does not receive held-out outcomes. Before a real run, the transfer calibration split and the comparator feature calibration split must be frozen consistently, and any differences in calibration opportunity access documented. All policies must face the identical future evaluator, task horizon, cost model, compute limits, and outcome visibility.

**Verdict:** fairness/comparability logic **PASS for plumbing**; empirical equality of execution budgets, evaluator, horizon, costs, and visibility **UNVERIFIED**. This remains a readiness gate.