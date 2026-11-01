# Phase 13F preregistration — PHASE-13F-BASELINE-ABLATION-V1

**Status:** configuration and protocol are frozen before Phase 13F outcomes. Confirmation uses replacement seed block 70–79 and writes only to `reports/experiments/PHASE-13F-BASELINE-ABLATION-V1/`. This is a new synthetic study; Phase 13C/D/E records remain unchanged. Attempt 01 partially executed seed 0 but failed before saving any records; to avoid reusing a potentially touched seed, seeds 70–79 replace the suggested 0–9 block. Attempt 01 is preserved separately and excluded. **Evidence scope:** synthetic ReasonFlux grid tasks only, not ARC or external validation.

## 13F-1 Research questions

The confirmatory questions are: (Q1) does ASFT outperform no learning; (Q2) does it outperform raw memory-only storage; (Q3) does SCT contribute beyond always-create/random creation; (Q4) does IDT contribute beyond frequency-only selection; (Q5) does measured reuse/transfer contribute; (Q6) does composition contribute; (Q7) which prespecified contribution has the largest paired effect; and (Q8) how much capability growth is lost when capability formation or portfolio aggregation is removed? The study estimates these effects only within the frozen synthetic task generator.

## 13F-2 Baseline philosophy and operational definitions

All arms in a seed share discovery traces, candidate pool where relevant, solver, held-out task IDs, task order, and common non-SCV qualification gate. Each arm is instantiated from a fresh library. ASFT uses the Phase 13E frozen growth metrics and existing capability APIs. B1 is the baseline solver with no learned skills. B2 stores raw trace episodes as executable memory, with no invariant representation, SCV selection, capability proposal, or composition. B3 creates a seed-keyed random sample of 75% of the common eligible invariant-backed pool without replacement (no SCV selection); the 75% budget is fixed before outcomes and contrasts with the ASFT-count-matched A2.1 selection. B4 is a transparent repeated-operation compression proxy; the repository does not provide canonical DreamCoder, so it will never be called canonical DreamCoder. These are plausible explanations, not intentionally weakened competitors.

## 13F-3 Baseline experiments

B1 tests whether learning is needed. B2 isolates episodic/raw-skill storage from invariant discovery and selection. B3 tests whether skill creation alone suffices. B4 tests a compression-only explanation. The key publication contrasts are ASFT versus B2 and B4, reported with paired seed-level effects, not just point differences. Baseline IS is not applicable to B1/B2; raw-trace memory is not assigned an artificial invariant-strength score.

## 13F-4 General ablation rule

Each ablation changes one named component while holding the remaining arm configuration, discovery stream, task stream, solver, and denominators fixed. Cross-component removals are separately labeled. No outcome-based retuning, arm deletion, baseline weakening, or threshold change is allowed. Contradictory, null, and unavailable results remain visible.

## 13F-5 IDT ablations

A1 removes invariant representation and consolidates only exact full operation sequences observed at least three times. A1.1 uses only observed candidate frequency to choose top-k candidates, where k equals ASFT selected count per seed; transfer-aware SCV does not determine ordering. Report invariant strength, SU, TS, utility, and growth where defined. Frequency-only is a deliberate substitute policy, not relabeled ASFT.

## 13F-6 SCT ablations

A2 creates every candidate passing the shared non-SCV eligibility gate. A2.1 random-selects exactly the ASFT birth count per seed from the same eligible pool. A2.2 disables existing skill lifecycle transitions while leaving all other ASFT components enabled. A2.3 disables composition only. B3 is deliberately distinct from A2.1: it uses a fixed 75% random creation budget, whereas A2.1 matches the ASFT birth count within each seed. Phase 13C's frozen calibration found its earlier Bernoulli control probability was 1.0; Phase 13F avoids reusing that degenerate randomized policy and uses a separately defined matched-budget random selection. This is a new policy arm, not a retrospective alteration of Phase 13C.

## 13F-7 CGM ablations

A3 keeps skills and transfer but creates no capability objects; under the frozen empty-portfolio convention C_t and CGR are 0.0, while skill-level metrics remain available. A3.1 preserves ASFT behavior but masks CGR/IGR/IG and related growth outputs, so it is not a performance comparator. A3.2 validates capabilities but reports them independently and withholds portfolio-level C_t/CGM aggregation. X4 disables capability formation while retaining skill transfer and CGM instrumentation to isolate proposal/formation from the measurement layer.

## 13F-8 Cross-component ablations

X1 disables skill retrieval/execution while retaining skill storage. X2 creates and counts selected skills but discards the library before held-out evaluation. X3 runs the same one-shot discovery and skills as ASFT, then discards discovery traces and episodic records; the runner has no online invariant-mining loop, so this ablation tests whether post-creation trace retention adds any value and may be behavior-identical. X4 disables capability formation but leaves the growth measurement pathway present. If an intervention cannot be operationalized without changing a metric definition or creating a new unsupported API, mark it unavailable rather than imply an effect.

## 13F-9 Sensitivity analysis

SCV threshold points are frozen as 0, 0.675, and 0.9666666666666666; the latter two are Phase 13C calibration q25/q75 values and are used as fixed context, not selected from Phase 13F outcomes. Invariant-strength thresholds are the existing default 5 and stricter 7.5/10. Composition lifecycle requirements vary only the predeclared success/reuse promotion requirements (loose/default/strict values in config). Report selected skill counts, composition availability, IS/SU/TS, task utility, CGR, and IG with seed-level intervals. These are sensitivity estimates; no favorable setting is selected post hoc.

## 13F-10 Statistical validation

The independent unit is seed (n=10). Report per-arm means, sample SDs and two-sided 95% Student-t CIs for IS, SU, TS, CGR, IG, task utility, coverage, and skill count where applicable. Primary contrasts are within-seed differences on identical tasks. Report paired Cohen's dz and small-sample Hedges-corrected g; if paired SD is zero, report effect size as undefined. The contribution-impact ranking is descriptive and is not a new pass gate. No treating tasks within a seed as independent observations. Results from Phase 13C/D/E are contextual and are not pooled with Phase 13F.

## 13F-11 Evidence package

The package contains a baseline figure, ablation figure, contribution-impact figure, sensitivity figure, tables for baseline results, ablation results, paired effect sizes, and sensitivity settings, plus a master matrix with seed-level and task-level data. The run manifest records frozen config/protocol/source hashes. B4 is labeled compression proxy in every artifact. All results are synthetic; external ARC validity is not claimed.

## Frozen metric boundary

IS means invariant strength, not the alternate repository intelligence-score concept; it is applicable only to invariant-backed skills. SU and TS use existing Skill Utility and measured successful transfer scores. CGR and IG use the same Phase 13E repository pathways and weights; Phase 13F does not change global definitions. Raw memory, missing capability portfolios, no-growth-tracking, and independent-capability conditions receive explicit `not_applicable`/`unavailable_by_design` status where a scalar would be misleading.
