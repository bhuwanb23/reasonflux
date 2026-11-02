# ASFT v1.1 Phase 1D — Readiness Report

**Phase ID:** `ASFT-V1.1-PHASE-1D`  
**Package:** `ASFT-V1.1-PHASE-1D-MEMORY-CHALLENGE-SPEC-V1`  
**Decision:** **PASS for specification/schema-contract layer; NOT ready for scientific benchmark execution or RQ3 confirmation.**  
**Experiments:** none run for Phase 1D. Historical Phase 13C/14 data are audited only.

## Executive conclusion

Phase 13C gives a substantial comparator-specific result: `MEMORY_ONLY` net value **1.325** vs SCT **0.345** (paired difference −0.980; seed-bootstrap CI [−1.020,−0.940]). Memory applied 440/440 opportunities and was correct on 418; SCT applied 223/440 and was correct on 201, with 217 no-matches and 22 failures. The same eligible denominator was used, but realized application coverage differed sharply.

A source-code audit qualifies a common summary: the saved Phase 13C memory arm was **not literal exact task-solution replay**. It chose a source trace matching an invariant pattern, extracted one macro operation, and applied that macro over eligible tasks. It is best described as raw-trace-exemplar/partial-macro memory. Phase 1D explicitly adds a true exact-episodic M1 arm alongside partial episodic M2, pattern M3, abstraction M4, and hybrid M5. The historical outcome does not establish why memory won, nor a general memory advantage.

## Phase 1D design completion

| Deliverable | Status | Evidence |
|---|---|---|
| 1D.1 Historical memory audit | PASS—RETROSPECTIVE | Phase 13C outcome, coverage, source implementation, normalized-cost caveat, and distinct Phase 13F baseline reconciled. |
| 1D.2 Memory taxonomy | PASS—SPECIFIED | M1 exact, M2 partial, M3 pattern, M4 abstraction, M5 hybrid separated. |
| 1D.3 Challenge families | PASS—SPECIFIED | A exact replay, B context shift, C composition, D analogy, E far transfer, F adversarial retrieval. |
| 1D.4 Budget matching | PASS—SPECIFIED | Same caps for exposure, bytes, items, build/query compute, retrieval inspections, and horizon. |
| 1D.5 Comparators | PASS—SPECIFIED/CONTRACTED | Memory-only suite, abstraction, hybrid, random retrieval, no learning, Oracle. |
| 1D.6 Metrics | PASS—SPECIFIED | HNU on B–F, Family A positive control, SOI and decision states. |
| 1D.7 Dataset design | PASS—SPECIFIED | Development/confirmatory/replication; every family in confirmation and replication. |
| 1D.8 Leakage controls | PASS—SPECIFIED/SCHEMA CONTRACT | Storage/retrieval/exposure audits and explicit Family A repeat exception. Production controls pending. |
| 1D.9 Preregistration | PASS—TEMPLATE | Run-specific N/hashes/access fields remain blank until calibration/freeze. |
| Contract suite | 26/26 PASS | Schema/design assertions only; no task outcomes or policy wins measured. |

## What the contract results do—and do not—say

The 26 contracts check that all six family definitions exist, memory representations remain distinct, resource caps are shared, the B1 suite is not collapsed to one baseline, Family A's planned exact exposure is explicitly isolated, hidden answer fields are rejected from policy payloads, and all splits/families are declared.

**They do not run a task solver or demonstrate that M1 wins A, M4 wins B–F, or M5 wins C.** Those are falsifiable challenge-design hypotheses, not results. A development implementation must instantiate the rule/task generator and verify the intended contrasts using task-derived outputs before confirmation. It must not hard-code arm outcomes or build labels from which policy won.

## Gates still blocked

| Gate | Status |
|---|---|
| Executable task generator/base solver and task-derived gold outcomes | PENDING |
| Actual implementations for M1–M5, retrieval baseline, and common instrumentation | PENDING |
| Byte-level storage, compute, candidate, retrieval and exposure counters | PENDING |
| Calibration of utility/cost coefficients and SOI | PENDING |
| Development validation of family constructs and expected win/lose patterns | PENDING |
| Calibration-only power/precision simulation and exact panel N | PENDING |
| Production split hashes, leakage audits, sealed test-label store/access log | PENDING |
| Frozen analysis code and untouched replication panel | PENDING |

## Final readiness statement

> **Phase 1D specification and contract schema: PASS. Scientific memory-vs-abstraction benchmark: NOT YET READY. RQ3: UNTESTED.**

The package answers how to compare memory and abstraction without equating their forms or budgets. It does not yet answer what kinds of problems require abstraction. Do not proceed to confirmatory testing until the task-derived generator, arm implementations, cost calibration, sample size, hashes, leakage controls, and sealed outcomes are ready.