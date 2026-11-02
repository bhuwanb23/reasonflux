# Phase 1C.1 — Ranking Failure Audit

**Phase:** `ASFT-V1.1-PHASE-1C`  
**Method:** retrospective audit of saved Phase 13B/14 records; no rerun and no replacement of prior results.  
**Decision boundary:** Phase 13B's primary ranking-superiority gate failed. The audit supports a pressure redesign; it does not show that IDT is ineffective or that lack of pressure was the unique causal root cause.

## Executive finding

The corrected Phase 13B primary comparison used top-K=2 held-out transfer utility. ASFT/transfer-aware, frequency-only, and no-transfer had the same mean TU (`0.095809`), zero paired mean differences, and the same semantic order in each of five seeds: reflection, rotation, counting, grouping. The preregistered strict per-seed superiority gate failed. Random's lower mean (`0.063113`) does not rescue the gate because beating random alone was insufficient.

**Observed proximate failure:** the tested policies did not produce different rankings in the saved five-seed pool. **Not established:** whether that tie was caused by absent ranking pressure, correlated ranking signals, a narrow candidate generator, score/accounting design, or genuinely low incremental value of transfer information. The audit treats “no observed ranking disagreement” as a direct observation and “pressure was the sole root cause” as unproven.

## Evidence ledger

| Record | Saved observation | Interpretation and limit |
|---|---|---|
| Corrected Phase 13B primary | Top-K=2 TU: ASFT `0.095809`, frequency `0.095809`, no-transfer `0.095809`; same semantic order in all five seeds; paired differences zero; strict gate failed. | No incremental ranking advantage demonstrated in that pool. A tie is neither universal failure nor proof the metric is useless. |
| Phase 13B candidate scale | About 4.4 promoted candidates per seed in the IS–TS summary; four expected semantic families recur. | Small, constructed ranking population with limited contrast. Counts are not independent natural concepts. |
| Accounting-version audit | Pre-correction local snapshot mean `0.1431299603`; corrected saved value `0.0958085317`; policy tie/gate failure persists in both. | Use the corrected saved value for current description; do not hide magnitude drift or imply remote history verification. |
| EXP-IDT-14 | Deliberately injects a frequent no-op into three of four families. Top-1 transfer-aware TU `0.164866`; frequency/no-transfer `0`; random `0.059557`. | Targeted exploratory stress response, not a repair/replication of the original Phase 13B gate. |
| Phase 13D predictive check | Corrected IS–TS `r=-0.0424`, seed-cluster 95% interval `[-0.1318, approximately 0]`. | Invariant-strength prediction is not established; this is relevant context, not a ranking outcome. |
| Phase 14F / 14H synthesis | Phase 14H records exact Phase 13B ranking tie; 14F reports mixed/comparator-specific baseline results across other protocols. | Do not pool endpoints/policies from different phases into one ranking experiment. |

## Tie hypotheses: what is and is not identifiable

1. **Candidate-pool restriction / low discriminative leverage — best-supported descriptive explanation.** The same semantic order was observed across all five seeds and across three informed policies. That shows the sampled pool did not expose different top-ranked structures; it does not prove why.
2. **Correlated signals — plausible, not isolated.** Frequency, IS, and the calibration transfer signal may be correlated in this generator. A controlled candidate design must include deliberate frequent-useless and rare-useful profiles, plus transfer-rich/poor cases.
3. **Too few distinct candidates — plausible.** Roughly four primary semantic structures leave little ranking opportunity. New panels need adequate candidate diversity and no result-driven semantic deduplication.
4. **Endpoint/accounting sensitivity — documented.** The TU magnitude changed after an output-cost correction, although the relative tie remained. A future endpoint and cost map must be frozen before confirmatory outcomes.
5. **True absence of transfer-aware advantage — remains possible.** The redesign must let IDT lose, tie, or win; it must not encode a favorable answer into generation or pressure thresholds.

## Phase 1C response

The new protocol makes candidate diversity explicit, fixes a top-K budget, requires pre-outcome divergence from each serious baseline, and evaluates selected portfolios against an independently held-out future task suite. It retains frequency, reuse-only, compression-only, and random controls; Oracle is post-lock analysis only. The designed quota and pressure gates are not allowed to inspect future utility.

The synthetic contract runner is deliberately separate. It verifies interface behavior, ranker disagreement, and win/tie/loss arithmetic using known synthetic values. Its outcomes are not a substitute for independent task execution.

## Final audit statement

> Phase 13B shows that the original corrected benchmark did not produce a different top-K order for transfer-aware, frequency-only, and no-transfer ranking. It failed the predeclared superiority gate. Phase 14 supports the interpretation that pressure and candidate diversity should be redesigned, but it does not prove that lack of pressure alone caused the tie or that IDT would win under stronger pressure.

Source records: [`Phase 14B IDT analysis`](../PHASE-14B-IDT-CRITICAL-ANALYSIS-V1/phase14b_idt_analysis.md), [`Phase 14B scorecard`](../PHASE-14B-IDT-CRITICAL-ANALYSIS-V1/idt_scorecard.csv), [`Phase 14B failure ledger`](../PHASE-14B-IDT-CRITICAL-ANALYSIS-V1/failure_analysis.csv), [`Phase 14F baseline analysis`](../PHASE-14F-BASELINE-ABLATION-CRITICAL-ANALYSIS-V1/phase14f_baselines_ablations_analysis.md), [`Phase 14H cross-contribution analysis`](../PHASE-14H-CROSS-CONTRIBUTION-ANALYSIS-V1/phase14h_cross_contribution_analysis.md), and [`EXP-IDT-14 exploratory stress report`](../EXP-IDT-14/report.md).