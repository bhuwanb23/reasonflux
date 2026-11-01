# Phase 14H — Cross-Contribution Analysis

**Review ID:** `PHASE-14H-CROSS-CONTRIBUTION-ANALYSIS-V1`  
**Scope:** Cross-phase synthesis of Phase 13B–13G evidence and Phase 14B–14G critical analyses, supported by Phase 13H consolidation.  
**Method:** read-only synthesis. No experiment reruns, metric changes, new pooling, or edits to Phase 13 outputs.  
**Status:** complete.

## Deliverable index

- [Causal Chain Analysis](causal_chain_analysis.md)
- [Cross-Contribution Dependency Matrix](cross_contribution_dependency_matrix.csv) and [figure](cross_contribution_dependency_matrix.svg)
- [Interaction Analysis](interaction_analysis.md)
- [Synthetic-vs-ARC Comparison](synthetic_vs_arc_analysis.md)
- [Alternative-Explanation Analysis](alternative_explanation_analysis.md)
- [Revised ASFT Model](revised_asft_model.md)
- [End-to-End Scorecard](end_to_end_scorecard.csv)
- [Source/hash manifest](source_manifest.json) and [hash list](source_hashes.csv)

## Executive verdict

The evidence supports a **narrow synthetic operational subchain**: repeated operation-level patterns are detected in the known synthetic vocabulary; the pipeline constructs reflection/rotation skill objects from qualifying candidates; and recorded skill applications include successful reuse and reductions in the simulator's reasoning-step cost proxy. This is not open-ended invariant discovery, does not show that SCT's selection policy adds value, and does not establish broad transfer.

The **first major evidential break** in the proposed causal chain is **Transfer → Capability Growth**. Transfer events and positive simulator cost reductions are observed, but transfer is not shown to cause or reliably predict capability growth. Corrected Phase 13D has negative mean CGR despite a positive descriptive TS–CGR association; Phase 13E has positive CGR but a negative, uncertain TS–CGR association and no CGR decrement when SCT is removed. Phase 13F also shows that removing transfer can improve task utility while lowering a growth metric. These are inconsistent, phase-specific endpoints, not a causal bridge.

The subsequent link, **Capability Growth → Intelligence Growth**, is also unestablished. Repository growth/intelligence indices are computable and positive in one synthetic cohort, but they are internally constructed from capability, transfer, coverage, utility, and composition metrics; the IE trend is negative. No independent intelligence criterion validates their construct interpretation. A very small, preregistered within-cohort `C_t` → next-round utility association (`r=0.0498`) does not validate intelligence growth or a transfer-to-growth mechanism.

**ARC is a separate upstream failure.** Under the bounded 13G implementation, the first observed break is at task/program representation and invariant discovery: only 3/600 discovery tasks fit the full ten-program scan, and zero invariant candidates result. A source audit found that the frozen config declares three candidates per task while discovery code defaults to ten; only the reflection fit among the three saved discovery fits is within the first three fixed candidates. Skills, learned transfer, and capability growth therefore did not activate on ARC. This is a serious implementation/external-validity failure, not an independent test of each downstream theory link.

### One-line verdict

> **Synthetic recurrence → represented skills → some successful reuse is supported narrowly; transfer-to-capability causation is the first unestablished link, intelligence interpretation is unvalidated, and the full ASFT causal chain is not established end to end. ARC fails upstream in the bounded representation/coverage pipeline, so its downstream chain is unavailable rather than separately falsified.**

## 14H-1 — Reconstructed causal chain

The original theory is a conjunctive claim: every link must work for the complete chain to be validated.

`Experience → Invariants → Skills → Transfer → Capability Growth → Intelligence Growth`

| Link | Cross-phase status | Evidence summary | What the evidence does not establish |
|---|---|---|---|
| **C1 Experience → Invariants** | 🟡 Supported narrowly in synthetic tasks | Phase 13B recovered generator-expected operation signatures across five seeds (reported expected-family discovery 5/5; IP/IR 1.0 within that vocabulary). | Blinded/open-ended discovery, semantic novelty, or ARC invariants. The generator, candidate vocabulary, and labels overlap. |
| **C2 Invariants → Skills** | 🟡 Operationally demonstrated in a narrow synthetic pool | Phase 13C recorded 44 reflection/rotation skill instances across ten confirmation seeds. Validated candidates are mapped into reusable objects. | That the invariant trigger is necessary or uniquely responsible for value; broad family emergence; SCT/SCV selection advantage. All eligible confirmation candidates were selected. |
| **C3 Skills → Transfer** | 🟡 Supported narrowly in synthetic tasks | Phase 13C recorded 201 correct positive-credit SCT applications; 91/91 attempted cross-family SCT applications succeeded within the reflection/rotation pool. Correct applications had mean normalized step reduction 0.227. Corrected Phase 13D reports RCR 0.1493 (95% interval 0.1320–0.1579). | General/open-world transfer, search-compute savings, or universal ASFT superiority. These are simulator metrics and bounded skill families; memory is a strong comparator in 13C. |
| **C4 Transfer → Capability Growth** | ❌ Not established; first major evidential break | CGR/transfer associations are inconsistent by phase; no causal treatment effect from transfer to capability growth is demonstrated. Phase 13E no-SCT has zero CGR contrast. | Transfer as the cause or reliable predictor of capability growth. Positive CGM scores elsewhere do not supply this missing link. |
| **C5 Capability Growth → Intelligence Growth** | ❌ Not established | Phase 13E computes positive mean IG/IGR; metrics are formula-derived from internal growth components. | That these indices measure intelligence or independently validated intelligence growth. No external criterion is supplied. |
| **Entire conjunctive chain** | ❌ Not validated | Early synthetic operations exist, but C4 and C5 are unestablished; evidence comes from different phases and protocols. | A single end-to-end causal effect or full-theory validation. |

**Status convention:** “Supported narrowly” means a bounded operational behavior is present in the saved synthetic runs. It is not equivalent to proving a causal law or a general theory. “Not established” is not proof of impossibility or universal failure.

## 14H-2 — What is actually demonstrated?

The strongest evidence-supported path is:

> **Known synthetic experience → recurrence of operation-level trace signatures → construction of reflection/rotation skill objects → some successful skill reuse with simulator step-cost reduction.**

There are important limits at every arrow. Phase 13B's labels and operations are aligned to the synthetic generator; Phase 13C's skill policy selects all 44/44 eligible confirmation rows and ties ALWAYS_CREATE and RANDOM_CREATE; Phase 13C memory-only retrieval exceeds SCT on its primary net-value score; and transfer results are bounded to related generated tasks and a step-cost proxy. The evidence demonstrates pipeline behavior and successful events, not a unique or universally superior causal explanation.

This subchain is assembled across controlled synthetic phases. It is not a single randomized mediation experiment that independently manipulates every link while holding the rest fixed. The full ASFT chain therefore cannot be inferred simply by placing individually positive phase summaries in sequence.

## 14H-3 — First failure point: transfer to capability growth

“First failure” here means the first proposed link for which the evidence ceases to support the claimed causal transition. It does **not** mean that capability metrics never rise.

- **Phase 13D:** corrected mean CGR is `-0.060` over nine evaluable seeds. Its TS–CGR correlation is positive (`r≈0.483`) but descriptive; it coexists with negative mean CGR and does not identify a causal effect.
- **Phase 13E:** mean CGR is `+0.2946` in its ten-seed synthetic cohort, but TS–CGR is negative (`r=-0.503`, interval includes zero). The no-SCT contrast on CGR is `0.000`.
- **Phase 13F:** removing transfer gives higher all-task utility than ASFT by `0.036344`, while ASFT's CGR is higher by `0.287172`. Transfer-related and growth-score outcomes move in different directions.
- **Phase 13E prediction result:** the distinct preregistered `C_t` → next-round task-utility association did pass (`r=0.0498`, cluster interval `[0.0163,0.0922]`). Its magnitude is very small (descriptive `r²≈0.0025`), same-generator, and noncausal. It does not test transfer causing growth or validate intelligence.

Together, these findings support **metric growth in a particular synthetic cohort**, not the causal claim `Transfer → Capability Growth`. The evidence is mixed, protocol-dependent, and not pooled across unlike phases.

## 14H-4 — IDT, SCT, Transfer, and CGM contributions

| Contribution | What survives | What remains unproven |
|---|---|---|
| **IDT** | Repeated operation-level structures are found in the designed synthetic generator; candidate structures feed later pipeline stages. | General invariant discovery; invariant strength as a reliable transfer predictor; transfer-aware ranking superiority. In 13B, transfer-aware, frequency-only, and no-transfer rankers tie on the primary corrected endpoint. |
| **SCT** | Reflection/rotation skill objects are formed and reused; a narrow composition case is observed. | Selection advantage or necessity. In 13C SCT ties always-create/random-create; in 13F no-SCV/random-SCV also tie in the tested pool. “SCT = always create” describes the confirmation decision behavior, not the entire theory in all settings. |
| **Transfer** | Correct reuse, narrow cross-family applications, and positive simulator step-cost proxies are observed. | General transfer, search-compute savings, universal baseline superiority, or a causal contribution to CGR. |
| **CGM** | Capability objects and repository-defined `C_t`, CGR, IG, IGR, and IE can be computed; Phase 13E has positive score growth in its cohort. | Robust capability growth across phases, external construct validity, or an intelligence-growth interpretation. |

## 14H-5 — Did the contributions reinforce one another?

**Operational dependencies exist; demonstrated synergy does not.** The pipeline is modularly connected, but saved comparisons do not show that combining named contributions consistently beats simpler alternatives or produces an end-to-end gain.

| Cross-contribution interaction | Observed result | Interpretation |
|---|---|---|
| Transfer-aware IDT ranking vs frequency/no-transfer | Phase 13B corrected primary endpoint ties exactly; same ranking across five seeds. EXP-IDT-14 demotes an intentionally injected frequent no-op in a stress test. | Mechanism sensitivity under a constructed confound, not natural-data ranking superiority. |
| SCT/SCV policy vs simple creation policies | Phase 13C SCT, ALWAYS_CREATE, RANDOM_CREATE all net value `0.345`; all 44 eligible confirmation candidates selected. Phase 13F no-SCV and random-SCV tie ASFT. | The tested pools provide little selection pressure; policies did not demonstrate incremental advantage. |
| Learned skills vs episodic memory | Phase 13C MEMORY_ONLY net value `1.325` vs SCT `0.345`; memory has 440 applications/418 correct vs SCT 223/201. | Strong competing explanation, but application counts are unmatched and later B2 comparators differ; not a universal memory verdict. |
| Transfer vs task utility and growth | 13D has positive covered transfer utility; 13F no-transfer has higher task utility while ASFT has higher CGR. | Endpoint-specific trade-off; no general positive interaction. |
| Capability layer vs behavior | 13F no-capability-layer leaves task/composition utility unchanged while CGR changes. | Metric pathway can move without corresponding task-performance change. |
| Composition and capability growth | 13C has one successful rotation→reflection case; 13E composition incremental gain is `-0.1429` and 0/10 capability-count gains; 13F has a positive phase-specific composition result. | Composition evidence is narrow and phase-dependent, not a stable reinforcing effect. |

There is no cross-phase factorial design that estimates interactions among IDT, SCT, transfer, and CGM on common task instances and endpoints. Therefore “the interactions exist” is defensible as a description of linked software pathways, but not as evidence of positive causal synergy.

## 14H-6 — Synthetic versus ARC

### Synthetic

- Narrow recurrence detection is repeatable in a designed generator.
- Reflection/rotation skills are represented and reused; some successful transfer and simulator step savings occur.
- Selection advantage is not established; memory retrieval remains a viable alternative.
- Capability scores increase in one synthetic cohort, but transfer-to-growth causality and intelligence construct validity are not established.

### ARC-AGI-2 bounded adapter

- Full ten-program exact demonstration fits: discovery `3/600`, transfer `5/200`, holdout `2/200`; these are not test accuracy or semantic task-family rates.
- Saved discovery records are schema-valid, but only three successful discovery traces enter invariant mining; no invariant candidates, ASFT skills, or capabilities form.
- A budget audit found a config/code mismatch: the frozen per-task budget is three, but `discover()` searches ten by default. Only the reflection fit among the three saved successful discovery programs is among the first three fixed candidates. This makes the discovery trace yield even less representative of the declared three-candidate limit.
- ASFT transfer exact accuracy is `0/200`; learned-skill transfer precision is unavailable because there are zero applicable learned skills. B2's `1/200` transfer success is an episodic-memory result, not an ASFT skill.
- All five arms have holdout accuracy `1/200`; the shared exact solve does not evidence learned ASFT capability. Attempt 02 reused the same holdout after attempt 01 generated predictions in memory.

**ARC interpretation:** the first observed failure is upstream at bounded program coverage and invariant formation. The later ARC links are not independently tested after that point. Low coverage is a strong implementation diagnosis, not proof that ARC falsifies IDT/SCT/transfer/CGM in general.

## 14H-7 — Alternative explanation: memory and retrieval

The Phase 13C raw MEMORY_ONLY comparator is a serious alternative to a skill-abstraction account on that protocol: net value `1.325` vs SCT `0.345`, with more application opportunities and more correct applications. It shows that reusing stored experience can explain some of the observed benefit without requiring SCT's creation/selection policy to be superior.

This does not establish memory as a universal explanation. The 13C policies are not application-count matched; 13D B2 memory-only, 13E skill-storage-only, and 13F B2 memory-skill-store are not the same baseline; and later outcomes are mixed or favor ASFT on particular endpoints. The correct conclusion is that **memory/retrieval remains a live, incompletely controlled competing mechanism**, and the cross-phase record does not isolate its contribution from abstraction or selection.

## 14H-8 — Revised ASFT model

The evidence-supported model is narrower than the original full chain:

```text
Controlled synthetic experience
        ↓
Recurring operation-level trace patterns                 [supported narrowly]
        ↓
Reusable reflection/rotation skill objects              [constructed; selection value unproven]
        ↓
Successful reuse + simulator step-cost reduction       [supported narrowly]
        ↓
Capability-score growth                                 [? transfer-to-growth link unestablished]
        ↓
Intelligence growth                                     [? construct validity unestablished]
```

A separate competing path remains viable:

```text
Stored experience → episode retrieval → reuse/transfer
```

For the current ARC adapter, the path stops earlier:

```text
ARC experience → low full-DSL fit / sparse successful traces → no invariants
                                                   ↳ skills, learned transfer, and capabilities unavailable
```

This is an evidence-weighted model of the saved implementation, not a replacement theory or an assertion that the unobserved links are impossible.

## 14H-9 — Revised scientific claim

> **“Across controlled synthetic tasks, ASFT detects recurring operation-level trace patterns, constructs reusable reflection/rotation skill objects, and records successful reuse with reduced simulator reasoning-step cost. These results support a narrow synthetic subchain from recurring experience through skill reuse, but do not establish open-ended invariant discovery, SCT selection superiority, general transfer, or a causal transfer-to-capability-growth effect. Repository-defined capability and intelligence-growth indices rise in one synthetic cohort, but capability-to-intelligence validity is untested. The bounded ARC adapter fails upstream at task/program coverage and produces no invariant/skill/capability chain; this is an implementation/external-validity failure, not a direct falsification of the broader theories.”**

## 14H-10 — Final scorecard and exit decision

| Claim | Status | Basis |
|---|---|---|
| Experience → invariant | 🟡 Narrow synthetic support | Repeated expected operation signatures in the known generator; not blinded/open-ended. |
| Invariant → skill | 🟡 Operationally demonstrated | 44 reflection/rotation skill instances; selection necessity/superiority not shown. |
| Skill → transfer | 🟡 Narrow synthetic support | Positive-credit reuses, 91/91 attempted cross-family applications, step-cost proxy; bounded pool. |
| Transfer → capability growth | ❌ Not established | Cross-phase associations/outcomes are inconsistent; no causal effect demonstrated. |
| Capability growth → intelligence growth | ❌ Not established | Formula-derived indices without independent construct validation. |
| Full synthetic ASFT chain | ❌ Not validated | Early subchain behavior exists; downstream links and single end-to-end causation remain open. |
| ARC ASFT chain | ❌ Not activated | First observed break is low DSL representation/coverage; downstream mechanisms unavailable. |
| Memory/retrieval alternative | 🟡 Survives | Strong 13C raw-memory result, but unmatched applications and phase-specific controls. |
| Positive cross-component synergy | ❌ Not demonstrated | No unified factorial interaction evidence; several ties/trade-offs. |

**Exit decision: Phase 14H COMPLETE.** The most defensible conclusion is not that “the first five ideas all work except the last two,” nor that the complete theory has been disproven. The first three links have bounded synthetic operational evidence; the first missing causal bridge is transfer to capability growth; intelligence interpretation remains unvalidated; ARC fails upstream in the tested representation and budget implementation.

## Evidence sources

- Phase 14 reviews: [14B IDT](../PHASE-14B-IDT-CRITICAL-ANALYSIS-V1/phase14b_idt_analysis.md), [14C SCT](../PHASE-14C-SCT-CRITICAL-ANALYSIS-V1/phase14c_sct_analysis.md), [14D Transfer](../PHASE-14D-TRANSFER-CRITICAL-ANALYSIS-V1/phase14d_transfer_analysis.md), [14E CGM](../PHASE-14E-CGM-CRITICAL-RESULTS-ANALYSIS-V1/phase14e_cgm_critical_analysis.md), [14F Baselines/Ablations](../PHASE-14F-BASELINE-ABLATION-CRITICAL-ANALYSIS-V1/phase14f_baselines_ablations_analysis.md), [14G ARC](../PHASE-14G-ARC-FAILURE-ANALYSIS-V1/phase14g_arc_failure_analysis.md).
- Consolidated evidence: [13H master evidence package](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/master_evidence_package.md), [Package A IDT](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/package_A_IDT.md), [Package B SCT](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/package_B_SCT.md), [Package C CGM](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/package_C_CGM.md), [Package F ARC](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/package_F_ARC.md).
- Phase 13 outputs: [13C evidence](../PHASE-13C-SCT-V1/evidence_package.md), [13D results](../PHASE-13D-TRANSFER-V1/phase13d_results.md), [13E evidence](../PHASE-13E-CAP-GROWTH-V1/evidence_package.md), [13F evidence](../PHASE-13F-BASELINE-ABLATION-V1/evidence_package.md), [13G evidence](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/evidence_package.md).
