# Phase 14D — Transfer Critical Analysis

**Review ID:** `PHASE-14D-TRANSFER-CRITICAL-ANALYSIS-V1`  
**Scope:** Transfer claims across saved Phase 13C, 13D, 13E, 13F, 13G, and 13H evidence.  
**Method:** read-only synthesis of existing evidence, including the corrected Phase 13D posthoc view. No reruns, no metric/threshold changes, and no edits to Phase 13 outputs.  
**Status:** complete.

## Deliverable index

- [Transfer Claim Review](transfer_claim_review.md)
- [Cost Reduction Analysis](cost_reduction_analysis.md)
- [Baseline Interpretation](baseline_interpretation.md)
- [Negative Transfer Analysis](negative_transfer_analysis.md)
- [Structural Transfer Review](structural_transfer_review.md)
- [ARC Transfer Analysis](arc_transfer_analysis.md)
- [Transfer Taxonomy Update](transfer_taxonomy.csv)
- [Revised Transfer Claim](revised_transfer_claim.md)
- [Final Transfer Scorecard](transfer_scorecard.csv)
- [Cost and baseline table](transfer_cost_baselines.csv)
- [Threats to validity](threats_to_validity.csv)
- [Source/hash manifest](source_manifest.json) and [hash list](source_hashes.csv)

## Executive verdict

Transfer is one of the stronger **synthetic mechanism** results: the saved 13C ledger records 201 correct positive-credit skill reuses, including 91/91 attempted cross-family applications, with a mean normalized step reduction of 0.227 among correct applications. Corrected Phase 13D also reports positive success-gated normalized reasoning-cost reduction (mean `0.1493`, 95% cluster interval `[0.1320,0.1579]`) and positive task-transfer utility in source-covered near/moderate cells. These are bounded simulator outcomes—not wall-clock compute savings or evidence of general transfer.

The bridge from transfer to capability growth is **not established**. Phase 13D reports a positive descriptive TS–CGR association (`r≈0.483`) but mean CGR is negative (`-0.060` across nine evaluable seeds). Phase 13E has a positive CGR cohort mean (`0.2946`) but TS–CGR is negative (`r=-0.503`, CI includes zero). These results do not show that transfer causes or reliably predicts growth.

Transfer categories must be qualified by source-skill coverage. Phase 13D's near/moderate cells include some covered, positive results and some cells unavailable for missing count/group skills. Although compositional/structural rows show positive raw TS values, **no required component source skills were present and no composition was activated**; the corrected Phase 13D addendum explicitly treats those endpoints as unavailable. They are not validated structural or multi-skill transfer.

Baseline superiority is comparator- and endpoint-dependent. Phase 13D's corrected transfer-utility contrasts favor ASFT over B1/B2/B3, but ASFT is slightly below B4 compression proxy and the all-mandatory-baseline claim fails. Phase 13F's no-transfer ablation has higher task utility than ASFT while ASFT has a positive CGR contrast; those outcomes are not interchangeable. ARC transfer was not demonstrated because the bounded adapter formed no skills and had negligible exact-fit coverage.

**Revised transfer claim:** “In controlled synthetic tasks, reflection- and rotation-based skills can be reused across related tasks, including observed cross-family applications, and this reuse reduces the repository's success-gated reasoning-step cost proxy. The evidence does not establish that transfer drives capability growth, validate structural/multi-skill transfer, show superiority over every competitive baseline, or demonstrate transfer on ARC.”

## 14D-1 — Claim review

| Transfer claim | 14D judgment | What the evidence supports |
|---|---|---|
| TR-1: skills transfer across tasks | **Supported narrowly, synthetic** | Repeated same-task-family/related-task reuse; some covered near/moderate cells; 13C records 91 successful attempted cross-family applications. |
| TR-2: transfer reduces reasoning cost | **Supported in simulator, narrowly** | Positive success-gated step-cost reduction in 13C and corrected 13D; not compute-time/FLOP savings. |
| TR-3: transfer contributes to capability growth | **Not established** | 13D TS–CGR association is positive but mean CGR negative; 13E relationship is negative with CI including zero. |
| TR-4: transfer beats non-transfer baselines | **Comparator-dependent; universal claim fails** | 13D favors ASFT over B1/B2/B3 but not B4; 13F includes an adverse task-utility contrast for transfer ablation. |
| TR-5: transfer scales to ARC-like settings | **Not demonstrated** | Bounded 13G adapter yields no skill candidates, so transfer is unavailable, not observed as zero performance of a transfer policy. |

## 14D-2 — What actually transferred?

### Phase 13C event ledger

Phase 13C's ten-seed confirmation block records 440 eligible SCT opportunities: 223 applications, 201 correct/positive-credit applications, 22 failed applications, and 217 no-matches. The 201 positive-credit reuses occurred across 44 created candidate instances. The cross-family row records 91/91 attempted SCT cross-family applications as correct/positive-credit; the memory-only arm records 308/308 attempted cross-family applications. These are **attempt-level outcomes in the synthetic generator**, not independent domains or tasks sampled from open-world distributions.

The skills available for this evidence were reflection and rotation only. Therefore a 91/91 cross-family result means the represented reflection/rotation operations were successfully reused on the tested generated cross-family cases; it does not mean all four planned families or arbitrary abstract skills transferred.

### What the Phase 13D source pool contained

The saved Phase 13D training pools contain recurring trace-derived signatures built from `apply_reflection`, `find_symmetry`, `find_rotation`, and `apply_rotation`, sometimes with `detect_object` in the signature. Each seed's pool records 48 traces, eight candidates, six eligible/promotable skills; no count/group skill is present. This identifies what was reused more concretely: generator-defined reflection/rotation operation fragments with repeated trace structure. Shared operation vocabulary and recurring traces are plausible enabling conditions, but the evidence does not isolate either as a causal mechanism.

The intended taxonomy includes related-rotation and multi-operation reflection variants, including cases that also involve count/group operations. Those multi-operation targets do not establish whole-task transfer when the required count/group component is absent: Phase 13D's corrected complex-cell coverage is zero and fallback supplies missing operations. Credit only the covered reflection/rotation fragment in an eligible application.

### Phase 13D corrected transfer cells

Corrected Phase 13D identifies 10 run seeds (50–59) and 14,400 task-level rows. Its corrected view preserves positive TS results in the supported cells while separating them from cells where the required source skill is absent:

- **Near:** EXP-TR-01 has source-skill coverage in 9/10 seeds and positive ASFT TS; EXP-TR-02 has coverage in 10/10 and positive TS. EXP-TR-03 has no source skill in any seed (counting) and is unavailable.
- **Moderate:** EXP-TR-04 has source-skill coverage in 9/10 seeds and positive TS; EXP-TR-05 has coverage in 10/10 and positive TS. EXP-TR-06 is unavailable for missing source skill.
- Reflection/rotation skills recur across the transfer experiments; no counting or grouping source skill is born in the cohort.

Thus, near and moderate transfer are supported **for eligible, covered synthetic cells**, not every cell listed under those taxonomies. Positive TS also does not imply an incremental ASFT advantage: in the saved cell tables ASFT ties `BEST_SINGLE` on the reported TS, and B4 ties or is slightly higher in some eligible cells. Interpret these as measured reuse/utility events, not evidence that ASFT is the superior ranker.

## 14D-3 — TR-2: reasoning-cost reduction and accounting

| Evidence | Saved result | Interpretation boundary |
|---|---:|---|
| Phase 13C SCT, correct applications | Mean normalized reasoning reduction `0.227`; mean raw step saving `1.000` on applied rows | Correctness is separate; incorrect applications receive zero cost benefit. Simulator step proxy only. |
| Phase 13C MEMORY_ONLY, correct applications | Mean normalized reduction `0.213`; 418/440 correct | Memory-only also reduces measured step costs and applied more often in that task stream. |
| Corrected Phase 13D ASFT | Success-gated normalized RCR mean `0.149288`, 95% interval `[0.131979,0.157943]`; positive in 10/10 seed summaries | Posthoc calculation from saved task rows; not an empirical compute or time measure. |
| Phase 13D exact task accuracy | 1.0 in several covered positive-transfer cells | Step savings do not necessarily increase exact accuracy where baseline accuracy is already saturated. |

The Phase 13D posthoc correction repaired reporting/lookup defects and audited source-component coverage without rerunning tasks or changing outcomes. It retained the original records and supplies the corrected comparison view. Phase-specific RCR values use their own frozen task/protocol units; do not average 13C and 13D into a single transfer effect.

**Search reduction caution:** the saved Phase 13D summaries do not provide a usable solver-search-candidate reduction measure (`solver_search_candidates` is null in relevant records). Retrieval-candidate evaluation counts are not equivalent to solver search effort. The defensible cost claim is about the repository's reasoning-step/RCR proxy, not reduced search compute.

## 14D-4 — TR-3: does transfer drive capability growth?

### Phase 13D

Corrected Phase 13D reports TS–CGR `r≈0.483` (`n=36` rows in nine seed clusters; the saved cluster interval is approximately `[0.482,0.484]`). But mean per-seed CGR is `-0.060` across nine evaluable seeds, with one missing seed. A positive association can coexist with negative mean growth and does not show that transfer produced net growth.

### Phase 13E

Phase 13E reports positive cohort-level synthetic CGR (`0.2946`) and IG (`0.2294`) for its frozen cohort, but TS–CGR is `r=-0.5027` with 95% interval `[-0.8601,0.1857]`, which includes zero. The same phase reports zero of ten seeds meeting the post-composition capability-count growth condition and a negative IE slope. Positive metric levels in Phase 13E therefore do not establish transfer-driven growth.

### Judgment

**TR-3 is not established.** The 13D positive correlation is descriptive and conflicts with its negative mean CGR and with the direction in 13E. Growth metrics vary by phase and cohort; no causal mediation analysis or consistent transfer→growth effect survives these records.

## 14D-5 — TR-4: baseline interpretation

### Corrected Phase 13D transfer-utility contrasts

| Comparator | ASFT minus comparator mean | 95% seed-level interval | Result |
|---|---:|---:|---|
| B1 no-learning | `+0.018909` | `[+0.016727,+0.020000]` | Positive in 10/10 seeds |
| B2 memory-only | `+0.015273` | `[+0.013091,+0.016364]` | Positive in 10/10 seeds |
| B3 random skills | `+0.728909` | `[+0.706364,+0.761273]` | Positive in 10/10; unusually large, comparator/task-specific contrast |
| B4 compression proxy | `-0.001091` | `[-0.003273,0]` | ASFT is not strictly above; 0/10 positive seeds |

The 13D all-mandatory-baseline superiority criterion fails on B4. B4 is explicitly a compression proxy, not canonical DreamCoder. These are Phase 13D's transfer-utility contrasts; they must not be substituted for net value, task utility, or the baselines from other phases.

### Cross-phase outcome dependence

Phase 13F's X1_NO_TRANSFER arm illustrates the metric trade-off: ASFT-minus-X1 task utility is `-0.0363` (ASFT lower), composed-task utility is `-0.3412`, and CGR is `+0.2872`. In the 13F baseline matrix, ASFT fails/null versus B1 and B3, passes versus B2 and B4 under that phase's joint task-utility/CGR rule. Phase 13C's exact MEMORY_ONLY policy also exceeds SCT on 13C net value (`1.325` vs. `0.345`).

**Judgment:** transfer can improve a transfer-specific metric against some controls, while not improving every downstream endpoint or every comparator. No universal superiority claim is supported.

## 14D-6 — Negative transfer: what the diagnostic proves

Corrected Phase 13D's forced diagnostics cover 190 evaluable forced applications. All have a decrease in the saved success-probability variable (`P_after < P_before`), giving forced harm rate `1.0`. Yet the normalized accuracy-NTR is `0.0`: the forced cases remained task-correct after transfer. Thus, the primary harm signal here is a confidence/success-probability decrement, **not an observed increase in exact task failures**.

The retrieval guard rejects 90/90 evaluable rows in the targeted negative diagnostic; 10 additional rows are unavailable. This supports that the guard blocks the specific forced-mismatch cases constructed for this diagnostic. It does not estimate a general false-positive rate on a matched set of beneficial transfer cases, nor prove calibrated discrimination over arbitrary helpful and harmful skills.

**Judgment:** targeted negative-transfer detection/guard rejection is supported narrowly. “ASFT generally distinguishes all helpful from harmful transfer” is too strong.

## 14D-7 — Structural, compositional, and multi-skill transfer

The corrected Phase 13D review found zero counting/grouping source skills, zero component-coverage seeds for EXP-TR-07–11, zero composition candidates, and zero active composition applications. The original frozen reporter had treated some partial transfer on complex tasks as composition. The posthoc correction explicitly prevents that inference: missing operations were supplied by reference fallback, and A4/no-composition ties ASFT on the EXP-TR-07–11 TS outcomes.

Raw table TS can be positive in those experiments, but without the preregistered source components and an active composition application it is **not coverage-qualified structural or compositional transfer**. These cells are unavailable—not negative proof that composition can never work, but also not positive evidence that it did work in Phase 13D.

## 14D-8 — ARC transfer

Phase 13G's bounded ARC adapter had 3 exact demonstration fits among 600 discovery tasks, 5/200 on transfer and 2/200 on holdout. It formed/promoted zero invariant candidates and zero skills, so the transfer precision denominator is zero and transfer evidence is unavailable. The bounded system's holdout exact-task accuracy is `0.005` for all arms.

The supported conclusion is **ARC transfer was not demonstrated because the upstream invariant/skill pipeline did not produce eligible skills under this adapter's low-coverage DSL**. This is not evidence that ARC contains no transferable skills or that unrestricted ASFT transfer fails. The Phase 13G fixed-holdout rerun followed an initial report-serialization failure and is not pristine independent confirmation.

## 14D-9 — Revised transfer taxonomy

| Transfer type | Updated status | Rationale |
|---|---|---|
| Near-task reuse/transfer | ✅ Supported in covered synthetic cells | 13D EXP-TR-01/02 positive with coverage in 9/10 and 10/10 seeds; EXP-TR-03 unavailable. |
| Moderate transfer | ✅ Supported in covered synthetic cells | EXP-TR-04/05 positive with coverage in 9/10 and 10/10 seeds; EXP-TR-06 unavailable. |
| Cross-family synthetic transfer | ✅ Observed narrowly | 13C records 91/91 attempted cross-family SCT applications successful; only reflection/rotation skill pool and generated tasks. |
| Compositional transfer | ⚪ Unavailable in 13D | Missing count/group source skills; zero composition activation; positive raw TS is not qualified. |
| Structural transfer | ⚪ Unavailable in 13D | EXP-TR-10/11 lack required source-skill coverage; reference fallback fills missing operations. |
| General multi-skill transfer | ⚪ Unavailable | No valid component-complete chain in corrected 13D. |
| Negative transfer | ✅ Targeted diagnostic only | Forced harmful cases show probability decrement and guard rejection; exact accuracy NTR remains zero. |
| ARC transfer | ❌ Not demonstrated | No eligible ARC skills; transfer denominator unavailable in bounded adapter. |

## 14D-10 — What survives and what does not

### Survives

- Reuse/transfer events occur repeatedly in controlled synthetic task streams.
- Reflection/rotation-based skills can transfer across related generated tasks, with 91/91 successful attempted cross-family applications in the Phase 13C ledger.
- Success-gated simulator step-cost reductions are positive in 13C and corrected 13D.
- A targeted guard rejects the forced negative-transfer probes in the saved 13D diagnostic.

### Not established

- Transfer as a cause or reliable predictor of capability growth.
- Search-compute reduction beyond the measured reasoning-step proxy.
- Complete structural, compositional, or multi-skill transfer in Phase 13D.
- Superiority over all baselines or across downstream task metrics.
- Transfer on ARC or other external distributions.

## 14D-11 — Threats to validity

See [`threats_to_validity.csv`](threats_to_validity.csv). Principal limits: common synthetic generator and operation vocabulary; only reflection/rotation source skills; candidate/task rows nested within ten seed clusters; confidence-step cost proxy rather than compute; coverage/fallback contamination in complex transfer cells; corrected 13D reporting after a frozen dashboard defect; mixed growth relationships; comparator-specific baselines; targeted negative diagnostic without broad specificity estimates; low ARC DSL coverage and same-holdout rerun history.

## 14D-12 — Revised transfer claim

> **“In controlled synthetic tasks, reflection- and rotation-based skills can be reused across related tasks, including observed cross-family applications, and this reuse reduces the repository's success-gated reasoning-step cost proxy. The evidence does not establish that transfer drives capability growth, validate structural or general multi-skill transfer, show superiority over all competitive baselines, or demonstrate transfer on ARC.”**

## 14D-13 — Final scorecard and exit decision

| Claim | Status | Basis |
|---|---|---|
| Transfer events exist | ✅ Supported, synthetic scope | 201 correct positive-credit 13C applications; covered positive cells in corrected 13D. |
| Transfer reduces reasoning-step cost | ✅ Supported, simulator scope | 13C mean normalized reduction `.227`; corrected 13D success-gated RCR `.1493`. |
| Cross-family transfer | ✅ Narrowly supported | 91/91 attempted 13C cross-family applications, within reflection/rotation pool. |
| Transfer can harm or reduce success probability | 🟡 Targeted diagnostic support | 190 forced cases show P decrement; exact task accuracy NTR `0.0`. |
| Guard rejects forced harmful cases | ✅ Narrow diagnostic support | 90/90 evaluable negative rows rejected; 10 unavailable. No broad specificity estimate. |
| Transfer drives capability growth | ❌ Not established | 13D CGR mean `-0.060`; 13D positive correlation is descriptive; 13E TS–CGR `r=-.503`, CI includes zero. |
| Structural/compositional transfer | ⚪ Unavailable in corrected 13D | Required skills absent, zero active composition, fallback used. |
| Universal baseline superiority | ❌ Not supported | 13D B4 contrast negative; 13F outcomes vary by comparator and endpoint. |
| ARC transfer | ❌ Not demonstrated | No eligible skills; low exact-fit coverage; denominator unavailable. |

**Exit decision: Phase 14D COMPLETE.** Transfer as synthetic reuse and a reasoning-step-cost effect survives; transfer as a validated growth mechanism, general structural capability, or ARC result does not.

## Evidence sources

- Phase 13C: [`evidence_package.md`](../PHASE-13C-SCT-V1/evidence_package.md), [`reuse_statistics.csv`](../PHASE-13C-SCT-V1/reuse_statistics.csv), [`matched_controls.csv`](../PHASE-13C-SCT-V1/matched_controls.csv).
- Corrected Phase 13D: [`posthoc_analysis.md`](../PHASE-13D-TRANSFER-V1/posthoc_analysis.md), [`posthoc_corrected_criteria.json`](../PHASE-13D-TRANSFER-V1/posthoc_corrected_criteria.json), [`posthoc_pairwise_baselines.csv`](../PHASE-13D-TRANSFER-V1/posthoc_pairwise_baselines.csv), [`posthoc_experiment_coverage.csv`](../PHASE-13D-TRANSFER-V1/posthoc_experiment_coverage.csv), [`phase13d_results.md`](../PHASE-13D-TRANSFER-V1/phase13d_results.md), [`task_level.jsonl`](../PHASE-13D-TRANSFER-V1/task_level.jsonl).
- Phase 13E: [`evidence_package.md`](../PHASE-13E-CAP-GROWTH-V1/evidence_package.md).
- Phase 13F: [`evidence_package.md`](../PHASE-13F-BASELINE-ABLATION-V1/evidence_package.md), [`master_result_matrix.csv`](../PHASE-13F-BASELINE-ABLATION-V1/master_result_matrix.csv).
- Phase 13G: [`evidence_package.md`](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/evidence_package.md).
- Phase 13H: [`Package B — SCT`](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/package_B_SCT.md), [`Package C — CGM`](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/package_C_CGM.md), [`Package D — Baselines`](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/package_D_Baselines.md), [`negative evidence register`](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/negative_evidence_register.csv).
