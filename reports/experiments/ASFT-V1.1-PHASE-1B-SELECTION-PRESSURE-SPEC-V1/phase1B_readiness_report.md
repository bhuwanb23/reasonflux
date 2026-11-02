# ASFT v1.1 Phase 1B — Readiness Review

**Phase ID:** `ASFT-V1.1-PHASE-1B`  
**Package:** `ASFT-V1.1-PHASE-1B-SELECTION-PRESSURE-SPEC-V1`  
**Decision:** **PASS for specification and fixture-level contract implementation; BLOCKED for confirmatory SCT/SCV evaluation.**  
**Evidence boundary:** 26/26 contract assertions passed on synthetic fixtures. No SCT experiment, calibration study, real task-run evaluation, or confirmatory outcomes were collected.

## What is complete

The specification now defines a balanced A–E candidate taxonomy, independent value rule, fixed capacity, all seven required selector policies, fairness rules, primary endpoint/SOI, data-split protocol, preregistration template, and a pre-outcome selection-divergence gate. The implementation package adds executable selector/pressure contracts, opaque candidate IDs, independent arrival ordering, a full contract result table, pairwise divergence matrix, pressure report, and win/tie/loss outcome-response sanity fixture.

- **Contract tests:** 26/26 PASS on fixture harness.
- **Pressure:** 100/100 synthetic fixture panels pass; mean contested SDR `0.3682`, minimum `0.2500`. Each panel meets SCV-vs-frequency/reuse/random disagreement thresholds.
- **Outcome response:** a separate adverse fixture makes SCV lose to random, capacity-limited always, and never-create; a tie fixture and win fixture also pass. This validates metric response only, not SCV performance.

See the [full Phase 1B audit report](../ASFT-V1.1-PHASE-1B-IMPLEMENTATION-CHECKLIST-V1/phase1B_full_audit_report.md), [readiness report with contract table](../ASFT-V1.1-PHASE-1B-IMPLEMENTATION-CHECKLIST-V1/phase1B_readiness_report.md), [contract results](../ASFT-V1.1-PHASE-1B-IMPLEMENTATION-CHECKLIST-V1/contract_test_results.csv), [pairwise matrix](../ASFT-V1.1-PHASE-1B-IMPLEMENTATION-CHECKLIST-V1/pairwise_divergence_matrix.csv), and [outcome-response sanity report](../ASFT-V1.1-PHASE-1B-IMPLEMENTATION-CHECKLIST-V1/outcome_response_sanity_report.md).

## Phase 1B exit checklist

| Criterion | Status | Evidence / limitation |
|---|---|---|
| Audit v1.0 selection failures in 13C/13F/14C/14F | PASS | `selection_failure_audit.md`; explains 44/44, random p=1, and four-of-four selection. |
| Taxonomy includes positive, neutral, negative, deceptive, rare high-impact candidates | PASS—FIXTURE | Four per A–E in synthetic contract panels; labels separated from selector cards. |
| Future value independent of SCV | PASS—FIXTURE | Value arithmetic uses a separate synthetic truth/cost record. Actual task-run ground truth is not yet implemented. |
| Selectors operational | PASS—FIXTURE | SCV, frequency, reuse-only, random, always-capacity, never, and isolated analysis-only Oracle. |
| Pressure measurable and divergent | PASS—FIXTURE | Pre-outcome pressure checker, SDR gate, 100/100 fixture passes. Must repeat on actual frozen study generator. |
| Fairness and leakage controls | PASS—API TESTS | Same candidate cards/slots/storage/horizon; hidden fields absent. This is not production OS-level outcome-store isolation. |
| Primary endpoint/SOI/decision categories | PASS—SPECIFIED | Future Net Value per slot, SOI +0.10 TEU/slot, win/tie/loss/unavailable categories. |
| Splits, sample-size rule, replication | PASS—SPECIFIED | Calibration/development/confirmation/replication and N rule specified; exact N still pending calibration. |
| Full run-specific hashes, final analysis, sealed store | PENDING | No final study data or outcome store exists yet. |
| Confirmatory experiment | NOT RUN | No results were collected. |

## Current execution gates

1. **Gate 1:** all 26 contract checks pass on fixtures.
2. **Gate 2:** pressure passes on fixture profile; must pass on actual development/confirmatory candidate cards before outcomes unlock.
3. **Gate 3:** exact final N is pending a calibration-only power/precision simulation.
4. **Gate 4:** fixture/spec hashes exist; production generator/task/seed/config hashes remain pending.
5. **Gate 5:** contract code exists; final research analysis code is not frozen.
6. **Gate 6:** no confirmatory outcome store has been created; implement and audit access control before use.

## Final readiness statement

> **Phase 1B contract-harness implementation: PASS. Full RQ2 benchmark readiness: BLOCKED.**

The fixture suite now makes it easy for SCV to lose in a constructed stress case and correctly reports that loss without concealing comparator outcomes. It does not establish that the real research benchmark has been run or that SCV is weak/strong. The next permissible Phase 1B action is actual candidate/task generator and outcome-runner implementation, followed by calibration, full pre-outcome pressure validation, exact-N freeze, and secure confirmatory lock. **Phase 1C is paused until this Phase 1B audit is accepted.**