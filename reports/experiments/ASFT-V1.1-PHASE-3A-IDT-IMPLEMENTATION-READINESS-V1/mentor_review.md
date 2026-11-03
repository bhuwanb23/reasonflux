# Phase 3A — Mentor Review and Disposition

**Review type:** Reconciliation of the mentor assessment supplied by the project owner  
**Date recorded:** 2026-11-02  
**Scope:** Phase 3A implementation-readiness decision only. This record does not open a new data split, run calibration, inspect confirmatory outcomes, or authorize Phase 3B/3D.

## Mentor verdict recorded

The mentor assessment accepts Phase 3A **as an implementation-plumbing review** and concurs with the scientific-readiness decision **BLOCKED**. It distinguishes a functioning development engine from a scientifically established benchmark population: “benchmark engine exists” does not imply “benchmark exists.”

| Area | Mentor assessment | Reconciled evidence |
|---|---|---|
| Implementation plumbing | PASS | R1–R5 engine and FNTU arithmetic execute on development fixtures. |
| Contract revalidation | PASS, 26/26 | All 26 Phase 1C contracts pass on the Phase 3A engine; synthetic/plumbing scope only. |
| Deterministic replay | PASS | Replay, tie-breaking, arrival-order invariance, and seeded R5 checks pass. |
| Ranker implementation | PASS, development scope | R1 invokes the production transfer-aware bridge/ranker; actual calibration feature provenance is not supplied. |
| Actual benchmark readiness | NOT ESTABLISHED | No real candidate/task pool, feature lineage, actual-pool pressure, or independent evaluator. |
| Scientific readiness | NOT ESTABLISHED | FNTU has arithmetic but no real utility/cost evaluator, λ, horizon, or outcome generation. |
| Outcome controls | NOT ESTABLISHED | The in-process vault is a mock; no sealed production store, access audit, or lock verification exists. |
| Phase 3B unlock | BLOCKED / NOT AUTHORIZED | Six prerequisites below remain open. |
| Phase 3D confirmation | NOT AUTHORIZED | No confirmatory readiness; no outcome access is allowed. |

## Four principal blockers affirmed

1. **Actual candidate pool:** an eligible candidate registry, source lineage, and real diversity evidence are absent. N=40 currently identifies the synthetic fixture design only.
2. **Actual-pool pressure:** rank divergence and TopK-RDR have only been demonstrated on the engineered synthetic recipe. The benchmark's real candidate population has not been pressure-tested.
3. **Independent primary endpoint:** FNTU@K is implemented as arithmetic, but the utility evaluator, cost evaluator, λ, task horizon, and independent outcome-generation/evaluation path are not present.
4. **Outcome store:** no production sealed store, active access log, signed lock verification, or independent custodian evidence is present.

The mentor's central caution is adopted: **26/26 plumbing contracts do not imply scientific benchmark readiness.** The 100/100 synthetic pressure result does not show pressure in an actual benchmark population.

## Required unlock gates before Phase 3B

All six gates below must be evidenced and reviewed before Phase 3B may begin. Completing a design document alone does not satisfy a gate that requires data, an implemented evaluator, or production access controls.

| # | Unlock gate | Required evidence | Current state |
|---|---|---|---|
| 1 | Actual candidate/task pool | Versioned candidate registry, task/family blocks, eligibility/duplication rule, N/K/H, opaque IDs, and source/task lineage | **OPEN** |
| 2 | Feature lineage freeze | Reproducible calibration-only derivation of F/C/G/T/R, reuse opportunity denominator, compression codec/ratio, provenance and feature hashes | **OPEN** |
| 3 | Actual-pool pressure validation | Pre-outcome R1–R5 full orders and pressure metrics on the eligible real pool; all Phase 1C pressure thresholds pass under the frozen rule | **OPEN** |
| 4 | Independent FNTU evaluator | Separate task evaluator, fixed horizon and family mix, paired no-candidate baseline, utility map, cost model/λ, and missingness rule | **OPEN** |
| 5 | Sealed outcome store | Independent store/custodian, immutable checksum, access controls/log, signed pre-outcome rank/pressure lock, and verification of no premature access | **OPEN** |
| 6 | Calibration-only power plan | Disjoint calibration/development/confirmatory/replication assignment, variance/precision simulation, independent-unit definition and justified final N | **OPEN** |

If an actual pressure gate fails or is insufficient, the benchmark is non-informative/blocked; do not tune, curate, or replace the pool based on outcomes. The saved Phase 13B tie remains a historical null result and must not be replaced by synthetic fixture performance.

## Final mentor disposition

- **Phase 3A:** accepted as implementation plumbing; scientific benchmark readiness is not established.
- **Phase 3B:** blocked and not authorized until all six unlock gates pass.
- **Phase 3D:** not authorized; outcome access remains prohibited.
- **Scientific claim:** IDT superiority is not established; IDT falsification is not established. Current prospective evaluation status is unavailable/non-informative, not a positive or negative efficacy finding.

No Phase 3B calibration or freeze has been performed as part of this review. This review does not assign datasets to calibration/confirmation, calculate N, freeze a new endpoint, or verify a sealed outcome store.