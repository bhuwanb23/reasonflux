# Phase 14F — Baselines & Ablations Critical Results Analysis

**Review ID:** `PHASE-14F-BASELINE-ABLATION-CRITICAL-ANALYSIS-V1`  
**Scope:** saved Phase 13B–13G evidence, Phase 13H consolidation, Phase 14A/14B accounting lineage, and Phase 13C–13G baseline/ablation definitions.  
**Method:** read-only synthesis. No experiment reruns, no baseline removals, no metric or threshold changes, and no Phase 13 output edits.  
**Status:** complete.

## Deliverable index

- [Baseline Interpretation Report](baseline_interpretation_report.md)
- [Alternative-Explanation Analysis](alternative_explanation_analysis.md)
- [Ablation Interpretation Report](ablation_interpretation_report.md)
- [Component-Importance Assessment](component_importance_assessment.md)
- [Threats-to-Validity Assessment](threats_to_validity.md) and [risk register](threats_to_validity.csv)
- [Revised Baseline Claims](revised_baseline_claims.md)
- [Final Baseline & Ablation Scorecard](baseline_ablation_scorecard.csv)
- [Cross-phase baseline table](cross_phase_baselines.csv)
- [Component/ablation evidence matrix](component_evidence_matrix.csv)
- [Phase 13B accounting versions](../PHASE-14B-IDT-CRITICAL-ANALYSIS-V1/phase13b_accounting_versions.csv)
- [Source/hash manifest](source_manifest.json) and [hash list](source_hashes.csv)

## Executive verdict

The evidence supports ASFT as a functioning synthetic learning framework that sometimes gains over no-learning and randomized controls on specified endpoints. It does **not** show that all major ASFT components are necessary, that ASFT universally outperforms simpler policies, or that a single causal explanation accounts for the results.

The strongest alternative explanation is **retrieval/memory** in Phase 13C's raw MEMORY_ONLY protocol: it achieves net value `1.325` versus SCT `0.345`, and 418/440 correct applications versus SCT's 201/440. But that result does not establish that memory explains everything: later memory-style comparators in Phases 13D–13F are distinct and ASFT beats them on some phase-specific endpoints. Do not pool Phase 13C raw MEMORY_ONLY with Phase 13F `B2_MEMORY_SKILL_STORE` or Phase 13E B2.

**Compression remains a live alternative, but evidence is mixed.** Phase 13D's corrected all-baseline superiority gate fails because ASFT is `-0.001091` below B4 compression proxy on transfer utility (95% CI `[-0.003273,0]`); 13E and 13F pass their separate B4 task/growth criteria. B4 is a proxy, not canonical DreamCoder. The defensible claim is not “compression beats ASFT” or “ASFT beats compression”; it is “ASFT has not demonstrated universal superiority to compression-oriented alternatives.”

**SCT/SCV selection is not established as necessary by these runs.** In Phase 13C all 44 eligible confirmation candidate rows are selected; all calibration candidates have SCV10>0, so the frozen random-create probability is 1.0 and the RANDOM_CREATE arm degenerates to ALWAYS_CREATE. In Phase 13F ASFT, no-SCV, and random-SCV each construct four skills from a four-item common pool, and their saved task utility/CGR differences are zero. These are strong indications that selection had little differential leverage in those tested pools. They do not establish that selection can never matter, nor that every synthetic benchmark is incapable of distinguishing rankers.

The best causal reading is **local and mechanism-specific**: removing invariants lowers selected transfer/growth endpoints in some settings; removing SCT/SCV or lifecycle often changes no policy decisions/outcomes because the relevant choice was not exercised; removing capability measurement can change CGR without changing task utility; transfer can improve a transfer-specific metric while lowering task utility in a separate ablation. Component necessity is therefore not established by positive metric deltas alone.

## 14F-1 — Cross-phase baseline findings

| Phase | Baseline/result | What it supports | What it does not support |
|---|---|---|---|
| 13B synthetic-v1 | Corrected top-k=2 ASFT/frequency-only/no-transfer mean TU all `0.095809`; random pattern `0.063113`. Historical pre-correction informed-arm value `0.143130`; both versions tie and fail strict per-seed all-control gate. | ASFT beats the tested random-pattern comparator on that endpoint. | No incremental transfer-aware ranking advantage over frequency/no-transfer; do not mix accounting versions. |
| 13C SCT | Net value `.345`; ALWAYS_CREATE and RANDOM_CREATE `.345`; raw MEMORY_ONLY `1.325`; NEVER_CREATE `0`. | Learning/reuse beats NEVER_CREATE under that simulator cost model; memory-only is a strong competing policy. | SCT superiority over always/random or raw memory-only; this strict gate fails. |
| 13D corrected | ASFT-minus B1 `+.018909`, B2 `+.015273`, B3 `+.728909`, B4 `-.001091` on transfer utility. | Specific transfer-utility gains over B1–B3. | All-baseline superiority; B4 causes the mandatory gate to fail. |
| 13E | Joint final-C_t/task-utility gate passes B2/B3/B4, fails B1 because task utility is lower (`-.0361`) despite final C_t `+1.1785`. | ASFT beats selected controls under that two-metric rule. | General performance improvement or universal baseline victory. |
| 13F | Joint task-utility/CGR gate passes B2/B4; fails B1 (utility `-.0363`) and B3 (both contrasts zero). | Comparator-specific gains on its frozen joint endpoints. | Universal superiority; no tie should be rephrased as a win. |
| 13G bounded ARC | Five main arms have identical holdout exact accuracy `1/200=.005`; zero validated invariant/skill/capability pipeline. | No demonstrated separation under this low-coverage adapter. | A fair test of ASFT vs ARC-capable learned baselines or a general ARC conclusion. |

**Version control:** Phase 13B pre-correction and corrected results remain separate records. The accounting correction changed absolute TU magnitude but did not change the tie or failed strict gate. Phase-specific comparator labels and endpoints differ; do not aggregate these rows into one overall effect.

## 14F-2 — Baseline-by-baseline interpretation

### B1 — No learning

**Verdict: mixed.** Phase 13C SCT has positive net value relative to NEVER_CREATE; Phase 13D ASFT has positive transfer utility relative to B1; Phase 13E and 13F show lower ASFT all-task utility than B1, despite positive capability/transfer/growth-specific measures. Phase 13B also ties ASFT with a no-transfer control. Learning can improve selected internal or transfer metrics without improving task utility on every stream.

### B2 — Memory/retrieval

**Verdict: surviving alternative, not a universal explanation.** In Phase 13C, MEMORY_ONLY is raw trace-exemplar retrieval, not a learned skill library. It applies 440/440 opportunities and records 418 correct applications; SCT applies 223/440 and records 201 correct. Its net value is `1.325` vs SCT `.345` (net-value contrast `-.980` for SCT). The policies are not application-count matched: this net-value gap combines match/application frequency and correctness, so it does not isolate per-attempt retrieval quality from abstraction quality. It is nevertheless the sharpest counterexample to SCT's superiority in that phase.

The later B2s are different: Phase 13D B2_MEMORY_ONLY is narrowly below ASFT on corrected transfer utility (`ASFT−B2=+.015273`); Phase 13E skill-storage-only and Phase 13F B2_MEMORY_SKILL_STORE are beaten on their own frozen task utility/CGR criteria. Those results prevent the broader statement “memory explains everything,” but they do not erase the Phase 13C result or create a pooled memory-vs-skill estimate.

### B3 — Random skills / random creation

**Verdict: mixed-to-favorable for ASFT in some contrasts, not eliminated as an alternative.** Phase 13D has a large ASFT advantage over its random-skills comparator on transfer utility; Phase 13E passes its B3 two-metric comparison; Phase 13B's random-pattern control is lower. Conversely, Phase 13C's RANDOM_CREATE exactly ties SCT because random-create degenerates to always-create on the all-positive eligible pool, and Phase 13F B3_RANDOM_SKILL_CREATION ties ASFT on both task utility and CGR. These controls are not identical across phases. “ASFT is not random” is supportable only for the specific random baselines/endpoints where a strict positive contrast was measured.

### B4 — Compression proxy

**Verdict: compression alternative survives; relative outcome is phase-specific.** Corrected 13D ASFT is slightly below B4 on transfer utility and fails the all-mandatory-baseline gate. Phase 13E and 13F favor ASFT over B4 on their frozen joint outcomes. Because B4 is a compression-only proxy and not canonical DreamCoder, neither victory nor tie fully tests the broad compression explanation.

## 14F-3 — Ablations: what was and was not isolated

| Component | Saved results | Critical interpretation |
|---|---|---|
| IDT / invariants | 13B: ASFT ties frequency/no-transfer. Corrected 13D: ASFT exceeds A1_NO_INVARIANTS by `.018909` on the pooled covered transfer-utility endpoint. 13E: removing IDT reduces CGR by `.05950`. 13F: ASFT−A1_NO_IDT utility `-.002438`, CGR `+.015001`; A1.1 frequency-only ties ASFT on utility/CGR. | Some endpoint-specific contribution is observed, but it is not a consistent task-utility win and not clearly distinct from simple frequency in every pool. **Partial, local support; not universal necessity.** |
| SCT | 13C SCT=ALWAYS_CREATE=RANDOM_CREATE. Corrected 13D A2_NO_SCT contrast is zero on evaluated comparisons. 13E A2_NO_SCT CGR contrast is zero. | Existing runs often do not show SCT's incremental necessity; in 13C and 13F candidate policies select all four/44 candidates, so the contrast may not test meaningful selection. **Necessity not established.** |
| SCV | 13C all calibration SCV10 values are positive; primary cutoff selects 44/44 and random-create probability is 1.0. SCV10 correlates with shadow value (`ρ=.700`), but frequency (`ρ=.748`) and p_reuse (`ρ=.884`) are at least as high. 13F A2_NO_SCV and A2.1_RANDOM_SCV both tie ASFT; all construct four skills from a four-candidate pool. | Correlation is not incremental policy value. No-SCV/random-SCV ties are informative because SCV did not change selections in those arms. **SCV necessity/unique contribution unsupported in tested pools.** |
| Skill persistence | Corrected 13D ASFT exceeds A3_NO_PERSISTENCE by `+.017018` (95% CI `[+.015055,+.018000]`) on transfer utility. | Local evidence that retained skills matter for this endpoint; not a cross-phase necessity claim. Persistence is distinct from lifecycle policy. |
| Lifecycle | 13C lifecycle-enabled and lifecycle-disabled net value both `.345` in every seed; 13F A2.2_NO_LIFECYCLE task utility/CGR differences are zero. | Lifecycle had no detected incremental effect in these frozen streams; it may have faced no consequential retirement/selection pressure. **Necessity not established, not proof lifecycle is useless generally.** |
| Transfer | 13D positive transfer utility in covered cells. 13F X1_NO_TRANSFER: ASFT-minus-X1 task utility `-.036344`, composed-task utility `-.34125`, CGR `+.287172`. | Transfer can improve transfer-specific or growth scores without improving task utility; its utility effect is not uniformly positive. **No general causal performance benefit.** |
| CGM | 13E growth metrics positive in one cohort; 13F A3_NO_CAPABILITY_LAYER leaves utility/composed-task utility unchanged while CGR differs `+.287172` by construction/measurement pathway. A5_NO_CGM masks growth outputs by design. | Removing the measurement layer changes the metric, not necessarily behavior. Growth-score movement is not task-performance evidence. |
| Composition | 13C rotation→reflection is successful in its single evaluable pair (ordered composition and no-skill composition-capable solver both succeed 100%; best single skill 0%; normalized step reduction `.429`); 13D unavailable due missing components; 13E incremental gain `-.1429` and 0/10 capability-count growth; 13F no-composition contrast favors ASFT on its composed-task endpoint (`+.6188`) and utility (`+.0773`). | A bounded cost/plumbing result in 13C and a positive 13F stream coexist with unavailable/adverse results. **Mixed evidence; no general capability-generation claim.** |

A zero result is a result for the intervention as actually implemented and the frozen candidate/task pool. It is not evidence that the component can never matter. Conversely, a score change caused by disabling the score-generating subsystem is not proof of a behavior-level mechanism.

## 14F-4 — Is low selection pressure a benchmark or theory problem?

The observed degeneracy is concrete and repeated:

- Phase 13C: 22/22 calibration candidates have SCV10>0; random-create probability is frozen at 1.0; 44/44 confirmation rows are selected by SCT, ALWAYS_CREATE, and RANDOM_CREATE. Their outcomes are exactly identical. In this run the selection policy has no opportunity to demonstrate discriminatory value.
- Phase 13F: ASFT, A2_NO_SCV, and A2.1_RANDOM_SCV each construct 4 skills from a common pool of 4; task utility and CGR differences are exactly zero. The fixed high-SCV sensitivity point constructs zero skills, indicating sensitivity to cutoffs, but that sensitivity arm cannot be used to rewrite the frozen primary threshold or claim a retroactive pass.

This supports a **tested-pool diagnosis**: candidate qualification and task distribution did not create enough divergence for SCV/SCT/lifecycle necessity to be identified. It does not establish that the entire synthetic benchmark is incapable of distinguishing rankers, nor that the theory would fail under stronger candidate heterogeneity, negative candidates, or decision pressure. Those are future-test design needs, not posthoc repairs.

## 14F-5 — Causal story and surviving explanations

### What the interventions support locally

- In some Phase 13D cells, removing invariants/persistence reduces the measured transfer endpoint; Phase 13E shows lower CGR when IDT is removed. These support local dependencies in the tested pipeline.
- Removing SCV/SCT/lifecycle often leaves the selected set or score outcomes unchanged; those components' necessity is not identified where the mechanism does not change behavior.
- Capability measurement/formation removals can alter CGR while task utility is unchanged, demonstrating that metric activation and task performance must be separated.
- Transfer has distinct outcomes: positive corrected 13D transfer utility, but negative Phase 13F task-utility contrast against no-transfer. No single sign describes all endpoints.

### Explanations not ruled out

1. **Memory/retrieval:** strong in Phase 13C raw MEMORY_ONLY and still comparator-specific elsewhere.
2. **Frequency or reuse heuristics:** Phase 13B ties frequency/no-transfer; Phase 13C frequency correlates with shadow value at least as strongly as SCV10; Phase 13F frequency-only ties ASFT on utility/CGR.
3. **Compression:** B4 is competitive and defeats the strict 13D all-baseline claim; it is only a proxy.
4. **Generator and candidate-pool regularity:** repeated operation families, mostly eligible candidates, and no selection divergence can explain positive reuse and null selection ablations without demonstrating broad theory.
5. **Metric construction:** positive CGM changes may partly reflect the mathematical scoring layer; this is not necessarily task-performance improvement.

No comparative result justifies a single universal causal account. The evidence supports multiple operational effects, but not necessity or exclusivity of ASFT's named mechanisms.

## 14F-6 — ARC context

Phase 13G has zero invariant candidates, zero skills/capabilities, and identical exact accuracy (`.005`) across the main arms. Therefore its baseline comparison is uninformative about which mechanism would win if the ARC candidate pipeline were active. Preserve the bounded DSL, low fit coverage, and same-holdout rerun caveats. Do not cite this as a successful baseline separation or as proof of universal baseline equivalence.

## 14F-7 — Revised baseline interpretation

> **ASFT shows non-random, comparator-specific synthetic learning and transfer behavior. It sometimes exceeds no-learning and random controls, and some invariant-removal contrasts reduce selected transfer/growth metrics. However, Phase 13C raw memory-only retrieval is substantially stronger than SCT on its net-value protocol; compression remains competitive in corrected 13D; later B2/B4 outcomes differ by phase and endpoint. Several SCT/SCV/lifecycle ablations tie because candidate selection or lifecycle decisions do not diverge in the tested pools. Current evidence does not establish universal ASFT superiority, exclusive explanation by its named mechanisms, or causal necessity of several components.**

## 14F-8 — Final scorecard

| Question | Status | Concise evidence |
|---|---|---|
| Better than no-learning? | 🟡 Mixed | Positive in some net/transfer comparisons; task utility lower than B1 in 13E/13F; tie in 13B. |
| Better than random alternatives? | 🟡 Often, not universally | 13D/13E and 13B random-pattern favor ASFT; 13C random-create and 13F B3 tie. |
| Better than memory? | ❌ Not established | Raw MEMORY_ONLY wins 13C; distinct B2 comparators are beaten in selected later endpoints. |
| Better than compression? | ❌ Not universally established | 13D B4 contrast is negative and all-baseline gate fails; 13E/13F pass their B4 comparisons; B4 is a proxy. |
| IDT necessary? | 🟡 Partial/local | Invariant removal affects some transfer/growth endpoints; other phases tie frequency or show no task-utility gain. |
| SCT necessary? | ❌ Not established | No-SCT ties in 13D/13E; primary candidate selection often degenerates. |
| SCV necessary/unique? | ❌ Not supported in tested pools | No-SCV and random-SCV ties; SCV correlation is not unique or incremental policy value. |
| Lifecycle necessary? | ❌ Not established | Exact 13C and 13F null contrasts; few consequential lifecycle events. |
| Transfer improves utility generally? | ❌ Not established | Phase 13D transfer endpoint positive; 13F no-transfer arm has higher task utility. |
| Composition valuable? | 🟡 Mixed | 13C/13F positive in specific tests; 13D unavailable; 13E negative value/no capability count gain. |
| CGM component adds task performance? | 🟡 Endpoint-dependent | Capability scores can change without task-utility change; measurement ablation is not behavior evidence. |
| Alternatives eliminated? | ❌ No | Memory, frequency, compression, generator-specific accumulation survive. |
| ARC baseline evidence? | ⚪ Unavailable for mechanism ranking | No candidate pipeline and no arm separation under bounded adapter. |

**Exit decision: Phase 14F COMPLETE.** The core finding is not that ASFT fails, nor that simpler approaches always win. It is that current evidence supports a working synthetic framework while leaving memory/retrieval/compression explanations alive and component necessity unresolved in several low-pressure or metric-dependent ablations.

## Evidence sources

- Phase 13B / accounting lineage: [`EXP-IDT-BASELINES report`](../EXP-IDT-BASELINES/report.md), [`Phase 13B implementation results`](../../../docs/03_implementation/validation/phase_13b_results.md), [`Phase 14B accounting versions`](../PHASE-14B-IDT-CRITICAL-ANALYSIS-V1/phase13b_accounting_versions.csv).
- Phase 13C: [`evidence_package.md`](../PHASE-13C-SCT-V1/evidence_package.md), [`matched_controls.csv`](../PHASE-13C-SCT-V1/matched_controls.csv), [`candidate_level.csv`](../PHASE-13C-SCT-V1/candidate_level.csv), [`lifecycle_ablation.csv`](../PHASE-13C-SCT-V1/lifecycle_ablation.csv).
- Corrected Phase 13D: [`posthoc_analysis.md`](../PHASE-13D-TRANSFER-V1/posthoc_analysis.md), [`posthoc_corrected_criteria.json`](../PHASE-13D-TRANSFER-V1/posthoc_corrected_criteria.json), [`posthoc_pairwise_baselines.csv`](../PHASE-13D-TRANSFER-V1/posthoc_pairwise_baselines.csv), [`table_matched_ablations.csv`](../PHASE-13D-TRANSFER-V1/table_matched_ablations.csv).
- Phase 13E: [`evidence_package.md`](../PHASE-13E-CAP-GROWTH-V1/evidence_package.md), [`analysis.json`](../PHASE-13E-CAP-GROWTH-V1/analysis.json).
- Phase 13F: [`evidence_package.md`](../PHASE-13F-BASELINE-ABLATION-V1/evidence_package.md), [`candidate_selection.csv`](../PHASE-13F-BASELINE-ABLATION-V1/candidate_selection.csv), [`master_result_matrix.csv`](../PHASE-13F-BASELINE-ABLATION-V1/master_result_matrix.csv).
- Phase 13G: [`evidence_package.md`](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/evidence_package.md), [`summary.json`](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/summary.json).
- Phase 13H consolidation: [`Package D — Baselines`](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/package_D_Baselines.md), [`Package E — Ablations`](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/package_E_Ablations.md), [`baseline master table`](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/baseline_master_table.csv), [`ablation master table`](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/ablation_master_table.csv).
