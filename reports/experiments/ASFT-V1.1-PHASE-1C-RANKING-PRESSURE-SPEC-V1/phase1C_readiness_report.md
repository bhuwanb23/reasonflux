# ASFT v1.1 Phase 1C — Readiness Report

**Phase ID:** `ASFT-V1.1-PHASE-1C`  
**Package:** `ASFT-V1.1-PHASE-1C-RANKING-PRESSURE-SPEC-V1`  
**Decision:** **PASS for ranking-benchmark specification and synthetic contract layer. NOT a confirmatory RQ1 evaluation.**  
**Build provenance:** This Phase 1C package was created afresh from the accepted Phase 1B state; no withdrawn Phase 1C draft was carried forward.

## Executive decision

Phase 1C has converted the v1.0 IDT ranking tie into an answerable benchmark design: candidate types and quotas are explicit, future value is separated from ranker scores, five competing rankers have frozen inputs/rules, Oracle is isolated, ranking divergence is measured before outcomes, and the primary endpoint and decision categories are specified. The synthetic contract harness verifies that the interface creates meaningfully different rankings and that the outcome calculator can register an IDT win, tie, or loss.

**Phase 1B acceptance note:** “Phase 1B demonstrates that selector disagreement and outcome-response can be measured under controlled synthetic fixtures; it does not yet provide evidence regarding the effectiveness of SCV, SCT, or skill-selection policies on independent task outcomes.” This statement remains the evidence boundary for Phase 1B.

## Completion checklist

| Phase 1C deliverable | Status | Evidence |
|---|---|---|
| 1C.1 Ranking failure audit | PASS—RETROSPECTIVE | Phase 13B tie, failed strict gate, accounting-version note, EXP-IDT-14 scope, and uncertainty about root cause documented. |
| 1C.2 Candidate taxonomy | PASS—SPECIFIED | Eight mutually exclusive hidden primary archetypes; N=40 quotas include 8 B and 8 C. |
| 1C.3 Independent future value | PASS—SPECIFIED | Portfolio-level paired FNTU@K, separate no-candidate baseline, fixed costs, no score circularity. |
| 1C.4 Ranking pressure | PASS—FIXTURE | Frozen TopK-RDR/Kendall gates; 100/100 synthetic panels pass. |
| 1C.5 Required rankers | PASS—SPECIFIED/CONTRACTED | IDT, frequency, reuse, compression, random; Oracle is post-lock only. |
| 1C.6 Transfer ground truth | PASS—SPECIFIED | Calibration-only predictor inputs; future task outcomes held separately; Oracle locked out. |
| 1C.7 Metrics and decision rules | PASS—SPECIFIED | Primary paired FNTU@K; four comparator contrasts; SOI +0.10; Holm family; four result states. |
| 1C.8 Data splits | PASS—SPECIFIED | Calibration/development/confirmatory/replication split and panel-level independent unit. |
| 1C.9 Preregistration | PASS—TEMPLATE | Run-specific N, hashes, sealed store, and power fields must be completed before any confirmation. |
| Contract suite | **26/26 PASS** | Synthetic test fixtures only. |

## Synthetic pressure results

The harness used 100 seeds of one controlled feature/type recipe (`N=40`, `K=8`). It passed the pre-outcome pressure gate on **100/100** panels. Mean TopK-RDR over all competitive ranker pairs was **0.8391** (minimum **0.7875**); mean normalized Kendall divergence was **0.4900** (minimum **0.4538**). Mean IDT-vs-Frequency/Reuse/Compression/Random TopK-RDR was **0.9463 / 0.7600 / 0.5550 / 0.8038**.

These statistics establish fixture-level pressure mechanics only. The feature means and type profiles are deliberately designed to make the rankers disagree; the 100 seeds reuse that same recipe, so this does **not** show that independently generated or natural benchmark panels will contain pressure. The results are not 100 independent experimental samples, do not estimate natural candidate distributions, and do not show whether IDT improves future task utility.

**Important limitation of the outcome-response checks:** the harness computes rankings first and then constructs truth vectors that assign positive value to Frequency-only selections (loss), equal value to every candidate (tie), or positive value to IDT-only selections (win). These are winner-conditioned arithmetic tests—not independent future outcomes. They show the aggregator can print `IDT < Frequency`, `=`, or `>`; they do not show that the specified task generator can naturally produce all three under outcome-blind rules. The formal independent FNTU@K protocol is specified, but the task-derived outcome runner is not implemented.

## Gates not satisfied for an empirical evaluation

| Gate | Status |
|---|---|
| Actual frozen candidate/task generator and solver outcome runner | PENDING |
| Calibration-derived cost conversion and empirical utility validation | PENDING |
| Calibration-only power/precision simulation and exact independent N | PENDING |
| Final production ranker/card/panel/task/config hashes | PENDING |
| Final analysis implementation and run-specific preregistration | PENDING |
| Sealed confirmatory truth store and access audit | PENDING |
| Independent family/template replication dataset | PENDING |

**No confirmatory ranking evaluation is unlocked. No Phase 4, SCT experiment, or outcome collection is authorized by this report.**

## Final readiness statement

> **Phase 1C benchmark design and synthetic contract validation: PASS. Empirical IDT ranking claim: UNTESTED.**

The design allows transfer-aware ranking to win, tie, or lose against frequency, reuse, compression, and random policies under predeclared pressure. It still requires real task/outcome implementation, calibration, final hashes, sample-size freeze, analysis freeze, and sealed-store controls before confirmatory evaluation. Memory, capability, intelligence, and broader ASFT claims remain outside this Phase 1C result.