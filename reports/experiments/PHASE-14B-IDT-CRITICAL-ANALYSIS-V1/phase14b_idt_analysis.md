# Phase 14B — Contribution 1 (IDT) Critical Results Analysis

**Review ID:** `PHASE-14B-IDT-CRITICAL-ANALYSIS-V1`  
**Scope:** Contribution 1 only — Invariant Discovery Theory (IDT).  
**Method:** critical interpretation of saved Phase 13 records only. No benchmark rerun, no threshold or metric changes, no result replacement.  
**Status:** complete; Phase 14C may proceed.

## Executive verdict

The surviving IDT contribution is **narrow, repeatable synthetic operation-signature discovery**. Phase 13B repeatedly recovered generator-expected operation patterns, with reported IP/IR of 1.0 inside the known synthetic vocabulary. This supports recurring-trace detection and candidate-generation behavior in that generator, not open-ended discovery of abstract or general invariants.

The two stronger predictive claims do not survive:

- **IDT-2 — IS predicts future transfer:** not established. Phase 13B's Pearson/Spearman correlations near 1.0 came from about 4.4 promoted candidates per seed in a tightly controlled, shared-vocabulary system. Corrected Phase 13D reports IS–TS `r=-0.0424` with a seed-cluster 95% interval `[-0.1318, approximately 0]`; Phase 13G has no invariant candidates and therefore no estimate.
- **IDT-3 — transfer-aware ranking beats frequency-only:** the original Phase 13B strict gate failed. In the corrected saved report, ASFT, frequency-only, and no-transfer each have mean top-k=2 TU `0.095809` and the exact same semantic ranking across the five seeds. The failure supports no superiority claim. The best-supported explanation is low discriminative leverage in this task/candidate pool, not proof that transfer awareness is universally useless.

EXP-IDT-14 shows that the ranker responds to a deliberately inserted frequent no-op, but it remains exploratory and cannot repair the original gate. Phase 13G demonstrates **no ARC invariant discovery with its bounded adapter**; because exact-fit discovery coverage was only 3/600 and the support threshold was five, this is not a broad test of unrestricted IDT.

**Final claim ceiling:** “In controlled synthetic tasks, ASFT repeatedly detects operation-level trace structures aligned with known generator families. Current evidence does not establish that IS reliably predicts transfer, that transfer-aware ranking outperforms frequency-only ranking on the original benchmark, or that the mechanism discovers invariants on ARC.”

## 14B-1 — Original thesis and independent claim decisions

| Claim | Phase 14B status | Decision basis |
|---|---|---|
| IDT-1: useful invariants emerge from experience | **Supported narrowly in synthetic scope; strong/general version unsupported** | Expected operation patterns are recovered repeatedly under the synthetic generator's known vocabulary; this is not blinded abstraction discovery. |
| IDT-2: invariant strength predicts future transfer | **Not established** | 13B strong but tiny/constructed association; 13D corrected association near zero/non-positive; 13G unavailable. |
| IDT-3: transfer-aware discovery beats frequency-only | **Failed on primary benchmark** | Original strict all-controls/per-seed gate fails; ASFT ties frequency-only/no-transfer in 13B. EXP-IDT-14 is exploratory. |

## 14B-2 — What the evidence actually shows

### Narrow positive findings

- Phase 13B reports the four generator-expected family signatures found in every one of five seeds: reflection `[find_symmetry, apply_reflection]`, rotation `[find_rotation, apply_rotation]`, counting `[count_objects]`, and grouping `[group_by_color]`. The output is an operation/signature match in a synthetic system whose task generator, solver vocabulary, and expected labels overlap.
- Reported discovery and invariant precision/recall are all `1.0` for those predefined patterns. This is useful implementation evidence under the current benchmark definition, but does not establish independent semantic correctness.
- The four family discovery rates are each `1.000` across five seeds. This supports repeatability within this generator and seed block, not broad distributional robustness.
- Noise diagnostics report variation survival `VST=1.0` and rank stability `0.72`. These are within-family perturbation results. Sparse-data sensitivity is weaker: sparse recall is `0.20` and mean IS is `1.8` in the stored summary.

### Limits and contradictions

- The Phase 13B IS–TS relation was summarized as Pearson `1.0` and Spearman approximately `1.0`, but the effective promoted-candidate population was only about 4.4 per seed. The operation categories and task outcomes are not independent natural concepts.
- Corrected Phase 13D found IS–TS `r=-0.0424` (95% seed-cluster bootstrap CI `[-0.1318, approximately 0]`; 114 rows nested in 10 seed clusters). This later evidence does not replicate positive predictive validity.
- Phase 13B ASFT and frequency-only/no-transfer produce the same semantic ranking in every seed. The primary comparison therefore has no observed incremental ranking change.
- Phase 13G produces zero invariant candidates, but its exact-fit discovery count is only 3/600 against a minimum support rule of five. The metric is unavailable after the coverage bottleneck; it is not an ARC estimate of IS predictive validity.

## 14B-3 — IDT-1: useful invariants emerge

### Strong version

> “ASFT discovers general, reusable invariants from experience.”

**Status: unsupported.** IP/IR of 1.0 is conditional on expected signatures/labels supplied by the synthetic task system. The Phase 13B report itself warns that expected-signature checks can accept an operation component of a multi-operation concept and recommends treating discovery as component-level evidence until blinded semantic annotation is available. Consequently, a high score here is not an independent test that the algorithm discovered a concept the generator/solver did not already define.

### Narrow version

> “ASFT repeatedly detects generator-expected operation-level structures in synthetic reasoning traces.”

**Status: supported within synthetic scope.** Each expected family signature is found in 5/5 seeds in the saved Phase 13B report. The candidate layer also produces recurring primitives such as `detect_object` and `verify_output`; those are trace operations and should not automatically be promoted to useful abstract invariants.

### Interpretation

This is a credible demonstration of **recurrence extraction from structured traces**. The remaining gap is construct validity: whether recurrence and the IS formula identify useful, abstraction-level invariants beyond the vocabulary/labels used to construct tasks and solver traces. Discovery repeatability should not be conflated with concept discovery or with downstream utility.

## 14B-4 — IDT-2: does IS predict transfer?

### Early result

Phase 13B reports Pearson IS–TS `r=1.0` and Spearman approximately `1.0`. The report also records a correlation population averaging about 4.4 promoted executable candidates per seed. Thus, this is a very small, constructed candidate set; a high correlation can be driven by the limited contrast among the families (especially reflection versus rotation) rather than many independent invariant classes.

### Later result

Corrected Phase 13D reports IS–TS `r=-0.0424`, 95% seed-cluster bootstrap interval `[-0.1318, approximately 0]` across 114 candidate/task-associated rows grouped in 10 seed clusters. The number 114 is not 114 independent seeds. The relationship is near zero and not positive by the corrected interval. In Phase 13G there are no accepted ARC invariant candidates, so the IS-to-transfer relationship is unavailable.

### Judgment

**IDT-2 is not established.** The 13B result is one positive synthetic association; 13D fails to reproduce it, and ARC supplies no estimable relationship. A defensible statement is “IS was associated with TS in one small controlled synthetic population,” not “IS reliably predicts transfer.”

## 14B-5 — IDT-3: does transfer-aware ranking beat frequency-only?

### Primary Phase 13B result

The corrected Phase 13B report uses the predeclared top-k=`2` outcome. Mean held-out TU is `0.095809` for ASFT, frequency-only, and no-transfer; each paired mean difference is `0.000000`. The strict gate required ASFT to strictly beat all three controls for every seed and remains **failed**. The ranking diagnostics show the same semantic order on each of five seeds: reflection, rotation, counting, grouping. The random control is lower (`0.063113`), but beating only random does not satisfy the mandatory gate.

### Measurement-version note from Phase 14A

The Phase 13B report discloses a post-result family-output cost-accounting correction. The local `HEAD` snapshot stores a prior baseline mean TU of `0.143130` for ASFT/frequency/no-transfer; the corrected working-tree report stores `0.095809`. Both versions show the same tie among informed ranking policies and fail the strict gate. The 14B conclusion about **no demonstrated ranking superiority** is therefore robust to the two recorded accounting versions; exact TU magnitude is version-dependent and must be labeled. See [`phase13b_accounting_versions.csv`](phase13b_accounting_versions.csv).

### Scientific meaning

The primary benchmark did not show that transfer awareness changes the ranking or improves the required outcome. This is a direct failure of the frozen superiority claim, not evidence that the gate should be weakened. It is also not proof that transfer signals are useless in every environment.

## 14B-6 — EXP-IDT-14 interpretation

EXP-IDT-14 deliberately injected `normalize_grid`, a frequent no-op trace marker, into discovery traces in three of four families after the Phase 13B tie. With top-k=1 as the primary endpoint, ASFT mean TU was `0.164866` (SD `0.001100`, 95% CI `[0.163902,0.165831]`); frequency-only and no-transfer were `0`, and random was `0.059557`. At top-k=2, ASFT was `0.096322` versus `0.082433` for frequency/no-transfer. The no-op was selected first by frequency-only/no-transfer and not by transfer-aware ranking.

This supports a narrow mechanism-sensitivity conclusion: **in this deliberately constructed stress test, the transfer-aware score can demote the injected frequent no-op.** It does not establish natural-data superiority, independent confirmation, or an exception to Phase 13B's failure. The full interpretation is in [`exp_idt14_interpretation.md`](exp_idt14_interpretation.md).

## 14B-7 — Why did the primary ranking claim fail?

### Explanation best supported by the saved diagnostics

The Phase 13B candidate pool and ranking rules yielded identical ASFT, frequency-only, and no-transfer semantic orderings in all five seeds. In this benchmark, the relevant frequency/strength/transfer signals did not create competing orderings. Therefore the evaluation had **low discriminative leverage for incremental transfer-aware ranking benefit** on the observed candidate pool.

This explains the tie more directly than the claim that transfer awareness is universally useless. However, this is a descriptive explanation, not a randomized causal diagnosis of why policies coincide. The evidence cannot distinguish whether the cause is the specific generator, candidate selection, score construction, or a general lack of useful transfer information without a separately justified and preregistered benchmark.

### What the failure means

- The original primary superiority criterion failed and must remain failed.
- The benchmark showed no incremental benefit where the rankers agreed; it did not identify a positive transfer-aware advantage.
- EXP-IDT-14 shows sensitivity to one deliberately inserted confound only.
- Future results cannot retrospectively repair the frozen 13B gate; any new benchmark would be a new confirmatory study with its own predeclared protocol.

Full table: [`failure_analysis.csv`](failure_analysis.csv).

## 14B-8 — Robustness interpretation

- **Variation survival:** `VST=1.0` in the stored Phase 13B summary; expected variation survived the tested generator perturbation.
- **Trace-noise/rank stability:** `RANK_STABILITY=0.72` (reported as 72% by the stored metric); useful but imperfect stability, not invariance to all noise.
- **Sparse evidence:** sparse precision `1.0`, sparse recall `0.20`, mean IS `1.8`, and mean sparse candidates `2.4`, according to the saved summary. High precision under sparse data coexists with missed expected patterns; calling discovery “robust” without this sensitivity qualification would overstate the result.
- **Scope:** all are synthetic-v1 perturbation checks with the same family/operation vocabulary. They do not demonstrate robustness to semantic drift, a different trace language, an unknown solver, or ARC task diversity.

**Judgment:** robustness is partial and metric-specific—good variation survival and moderate rank stability in the tested generator, but weak sparse recall and no external robustness claim. See [`robustness_arc_interpretation.md`](robustness_arc_interpretation.md).

## 14B-9 — ARC interpretation

Phase 13G's bounded adapter exact-fit only 3/600 discovery tasks; the frozen invariant support threshold was five. It therefore produced zero accepted invariant candidates, zero skills, and zero capabilities. There is no ARC IS–TS estimate. This is the direct evidence that **the current bounded adapter did not demonstrate IDT on ARC**.

It is not a clean test of unrestricted IDT: the ten-program DSL covered only a small operation subset, exact-fit coverage was low, several semantic task families were not operationalized, and the same holdout was reused after attempt 01 generated predictions in memory. Therefore:

- **Claim:** ARC-level invariant discovery has not been demonstrated — supported.
- **Claim:** ASFT/IDT cannot discover ARC invariants in principle — not supported by this experiment.
- **Claim:** current ARC adapter has a coverage/representation bottleneck — strongly supported as a limitation of this implementation.

## 14B-10 — Threats to validity

The detailed register is [`threats_to_validity.csv`](threats_to_validity.csv). The principal IDT threats are:

1. **Shared generator vocabulary (high):** task construction, trace operations, and expected labels overlap, inflating the apparent independence of discovery.
2. **Operation-level labels (medium):** component signatures can match expected composite concepts; this validates operation recovery, not necessarily abstraction.
3. **Tiny candidate population (high):** roughly 4.4 promoted candidates per seed make correlation estimates fragile.
4. **Synthetic dependence (high):** all 13B–13F IDT-related inference is tied to related synthetic mechanisms; phase results are not independent replications across domains.
5. **ARC DSL coverage (high):** only 3 exact-fit discovery tasks and a 5-candidate support threshold yield no estimable ARC discovery relationship.
6. **Phase 13B measurement-version drift (medium):** post-result output-cost accounting changed absolute TU from the local pre-correction snapshot; the gate outcome remained a tie/failure in both versions.
7. **EXP-IDT-14 posthoc design (medium):** confound was deliberately inserted after observing the original tie; interpret as targeted stress evidence only.

## 14B-11 — What survives

### Survives

- Recurring operation-level trace structures are detected in this controlled synthetic generator.
- Expected synthetic signatures repeat across the five Phase 13B seeds, and the generated candidate set/ranking diagnostics are inspectable.
- The implementation has a transfer-aware scoring/ranking pathway and can respond to one deliberately injected frequent-no-op confound in EXP-IDT-14.
- Tested synthetic variation survival is high (`VST=1.0`), with reported rank stability `0.72`.

### Does not survive as a scientific conclusion

- General abstract invariant discovery.
- Reliable predictive validity of IS for future transfer.
- Transfer-aware superiority over frequency-only/no-transfer on the original primary benchmark.
- ARC-level invariant discovery or broad external validity.

## 14B-12 — Revised IDT claim

> **“In controlled synthetic environments, ASFT can repeatedly identify operation-level structures in reasoning traces that align with known generator families. The current evidence does not establish that invariant strength reliably predicts future transfer, that transfer-aware ranking outperforms frequency-only ranking on the original benchmark, or that IDT discovers invariants on ARC.”**

This statement preserves the positive synthetic discovery result while keeping the failed ranking gate, conflicting IS–TS evidence, and ARC coverage limits explicit.

## 14B-13 — Final scorecard and exit decision

| IDT result | Status | Reason |
|---|---|---|
| Narrow operation-level invariants emerge | ✅ Supported, synthetic scope | Expected signatures found 5/5 seeds in the controlled generator. |
| Discovery repeatable across seeds | ✅ Supported, narrow | Five-seed family discovery rates are 1.0; same vocabulary/generator. |
| Robust discovery | ⚠ Partial | VST 1.0, rank stability 0.72; sparse recall only 0.20. |
| General/open-ended invariant discovery | ❌ Unsupported | Shared generator/solver vocabulary; operation-level labels and checks. |
| IS predicts transfer | ❌ Not established | Tiny positive 13B association not replicated; corrected 13D near zero/non-positive; 13G unavailable. |
| Transfer-aware ranking > frequency-only | ❌ Primary gate failed | 13B TU tie and zero paired difference; strict per-seed gate fails. |
| EXP-IDT-14 mechanism sensitivity | 🟡 Exploratory support only | Rejects the deliberately injected frequent no-op in the designed stress test. |
| ARC invariant discovery | ❌ Not demonstrated | Zero candidates under low-coverage bounded DSL; broad claim remains untested. |
| IDT external validity | ❌ Not demonstrated | Synthetic dependence and bounded ARC adapter. |

**Exit decision: Phase 14B COMPLETE.** The narrow discovery mechanism survives; predictive and superiority claims do not. Proceed to Phase 14C without revisiting Phase 13 thresholds, candidate definitions, or the failed Phase 13B gate.

## Evidence sources

- Phase 13B: [`phase_13b_results.md`](../../../docs/03_implementation/validation/phase_13b_results.md), [`idt_evidence/summary.json`](../idt_evidence/summary.json), [`EXP-IDT-01`](../EXP-IDT-01/report.md), [`EXP-IDT-BASELINES`](../EXP-IDT-BASELINES/report.md).
- EXP-IDT-14: [`report.md`](../EXP-IDT-14/report.md), [`record.json`](../EXP-IDT-14/record.json); the Phase 13B gate remains the original reference point.
- Phase 13D: [corrected saved-record posthoc analysis](../PHASE-13D-TRANSFER-V1/posthoc_analysis.md), [`posthoc_corrected_criteria.json`](../PHASE-13D-TRANSFER-V1/posthoc_corrected_criteria.json).
- Phase 13G: [bounded ARC evidence package](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/evidence_package.md).
- Integrity context: [Phase 14A report](../PHASE-14A-EVIDENCE-INTEGRITY-REVIEW-V1/evidence_integrity_report.md).
