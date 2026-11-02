# ASFT v1.1 Phase 1B — Readiness Report

**Phase ID:** `ASFT-V1.1-PHASE-1B`  
**Package:** `ASFT-V1.1-PHASE-1B-IMPLEMENTATION-CHECKLIST-V1`  
**Decision:** **PASS for contract-harness implementation; BLOCKED for confirmatory SCT/SCV evaluation.**  
**Evidence boundary:** 26/26 checks passed on synthetic contract fixtures. No SCT experiment, calibration study, independent task evaluation, or confirmatory data collection was performed.

## What was corrected

The previous Phase 1B response overstated readiness: it had a pressure fixture but did not test that SCV could lose on an independent value record, and its fixture IDs/order exposed type information. Both issues are corrected. IDs are now opaque, arrival order is independently randomized, and the suite includes explicit outcome-response tests for a loss, a tie, and a win. This report supersedes the earlier 23-test status.

## Contract results

| Contract group | Result |
|---|---:|
| Candidate classes, quotas, label concealment (CT-1A–C) | 3/3 PASS |
| Value independence and score mutation (CT-2A–B) | 2/2 PASS |
| Seven selector operations, determinism, tie breaks (CT-3A–C) | 3/3 PASS |
| Pressure/divergence and pre-outcome check (CT-4A–C) | 3/3 PASS |
| Storage, opportunity, horizon, information parity (CT-5A–D) | 4/4 PASS |
| Leakage and split namespace checks (CT-6A–C) | 3/3 PASS |
| Oracle isolation (CT-7A–B) | 2/2 PASS |
| Cost, reward, horizon, sensitivity (CT-8A–C) | 3/3 PASS |
| Outcome-response loss/tie/win checks (CT-9A–C) | 3/3 PASS |
| **Total** | **26/26 PASS** |

The exact row-level test log is [`contract_test_results.csv`](contract_test_results.csv). The full forensic reasoning and source mapping are in [`phase1B_full_audit_report.md`](phase1B_full_audit_report.md).

## Pressure validation

100 deterministic fixture panels passed the pre-outcome gate. This is the **same fixed feature/type recipe** across seeds—not 100 independent experimental panels.

| Measure | Result | Gate |
|---|---:|---:|
| Fixture gate pass | 100/100 | All fixtures |
| Mean contested SDR (S1–S4) | 0.3682 | ≥0.20 |
| Minimum / maximum SDR | 0.2500 / 0.5000 | Minimum ≥0.20 |
| Mean/min SCV–frequency divergence | 0.4000 / 0.4000 | ≥0.10 each |
| Mean/min SCV–reuse divergence | 0.4000 / 0.4000 | ≥0.10 each |
| Mean/min SCV–random divergence | 0.4590 / 0.3000 | ≥0.10 each |

### Pairwise divergence matrix — fixture seed 0

`D(a,b)=|S_a △ S_b|/20`.

| Selector | SCV | Frequency | Reuse | Random | Always-cap | Never |
|---|---:|---:|---:|---:|---:|---:|
| SCV | 0.00 | 0.40 | 0.40 | 0.60 | 0.40 | 0.40 |
| Frequency | 0.40 | 0.00 | 0.00 | 0.50 | 0.60 | 0.40 |
| Reuse | 0.40 | 0.00 | 0.00 | 0.50 | 0.60 | 0.40 |
| Random | 0.60 | 0.50 | 0.50 | 0.00 | 0.40 | 0.40 |
| Always-cap | 0.40 | 0.60 | 0.60 | 0.40 | 0.00 | 0.40 |
| Never | 0.40 | 0.40 | 0.40 | 0.40 | 0.40 | 0.00 |

The standalone [`pressure_validation_report.md`](pressure_validation_report.md), [`pairwise_divergence_matrix.csv`](pairwise_divergence_matrix.csv), and [`pressure_validation.json`](pressure_validation.json) provide full details.

## Brutal-honesty outcome-response test

On the synthetic adverse-value fixture, SCV selects four positive A and four deceptive negative D candidates; it misses the rare high-impact E candidates. Its mean value is **−0.5500 TEU/slot**, versus **+1.2313** for Random, **+1.1688** for capacity-limited Always, **0.0000** for Never, and **−3.1750** for Frequency and Reuse. The metric pipeline also passes separate tie and win assertions. These values are test fixtures only—not experiment results or a claim about real SCV performance. Details: [`outcome_response_sanity_report.md`](outcome_response_sanity_report.md) and [`outcome_response_sanity.csv`](outcome_response_sanity.csv).

## Confirmatory unlock status

| Gate | Status |
|---|---|
| Contract tests | PASS on synthetic fixtures |
| Pressure gate | PASS on fixture recipe; must be rerun on actual frozen candidate generator |
| Exact sample size | PENDING calibration-only power/precision simulation |
| Run-specific generator/task/seed/config hashes | PENDING |
| Final statistical analysis code freeze | PENDING |
| Sealed confirmatory outcome store/access log | PENDING |
| Actual solver/task counterfactual and empirical cost validation | PENDING |

**No confirmatory evaluation is unlocked.** The next Phase 1B work, if authorized, is to implement and pressure-test the actual task/candidate generator, calibrate costs and sample size on allowed data, freeze all run-specific hashes and analysis, and demonstrate an outcome store that remains sealed until ranking and pressure are locked.

## Final readiness statement

> **Phase 1B contract implementation: PASS. Full RQ2 benchmark readiness: BLOCKED.**

The benchmark can now mechanically create divergent decisions and the test suite can register SCV wins, ties, or losses. It has not yet demonstrated those properties in an independent research dataset. Phase 1C remains paused until this Phase 1B audit is accepted and the remaining gates are resolved.