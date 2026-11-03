# Phase 3A — Leakage and Isolation Audit

## Controls exercised

1. **Operational schema:** frozen slotted `CandidateCard` contains only an opaque ID and seven bounded public features. Hidden archetype, source/target family, future utility, future task labels, Oracle score, and outcome fields are not accepted.
2. **Ranker API:** `rank_all` accepts cards, panel/seed, calibration `TransferMemory`, and family count; it has no outcome, truth, label, or Oracle parameter. R1 consumes calibration memory only. Pressure metrics accept only rank orders and K.
3. **Label separation:** synthetic type labels and future-truth maps are held in separate opaque-ID-keyed mappings by the contract runner and are not passed into ranking or pressure calls.
4. **Outcome mutation:** a changed external truth mapping leaves the rank output identical because no truth is available to the operational API.
5. **Oracle:** R6 is excluded from `POLICIES`, pressure diagnostics, and FNTU comparator set. Its separate interface requires the exact ranking/pressure lock hashes and a sealed-vault access object; mismatched ranks/pressure are rejected.
6. **Hidden-value correctness:** Oracle ordering uses future value only after authorization; it is upper-bound analysis, never a feasible policy or tuning comparator.

All corresponding contracts and supplemental checks passed on synthetic fixtures.

## Important limits

The `OutcomeVault` is an in-process protocol mock, not a secure storage boundary: the fixture runner holds the synthetic outcome map in memory, and Python private attributes are not access-control enforcement. No production sealed store, signing key, independent evaluator principal, immutable audit log, or actual access-control test exists. The Phase 1C spec's post-rank signed lock and separately held confirmatory outcome store therefore remain unimplemented as production governance.

No real candidate/task dataset was available for lineage-based leakage review. Static schema/API checks cannot rule out leakage in an upstream serializer, feature-calibration job, or data store.

**Verdict:** ranker/pressure API separation **PASS in development**; production leakage isolation and outcome-store sealing **NOT VERIFIED / BLOCKING**. Do not unlock outcomes.