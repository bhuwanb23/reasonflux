# Phase 14E — Contribution 3 (CGM) Critical Results Analysis

**Review ID:** `PHASE-14E-CGM-CRITICAL-RESULTS-ANALYSIS-V1`  
**Evidence:** saved Phase 13D, 13E, 13F, 13G, and 13H artifacts, plus read-only inspection of the frozen CGM metric implementations.  
**Method:** no reruns, no threshold/formula changes, and no modifications to Phase 13 outputs.  
**Status:** complete.

## Deliverable index

- [CGM Claim Review](cgm_claim_review.md)
- [Capability Interpretation](capability_interpretation.md)
- [Growth Interpretation](growth_interpretation.md)
- [Intelligence-Metric Analysis](intelligence_metric_analysis.md)
- [Baseline Interpretation](baseline_interpretation.md)
- [Composition Analysis](composition_analysis.md)
- [ARC Interpretation](arc_interpretation.md)
- [Threats-to-Validity Assessment](threats_to_validity.md) and [register](threats_to_validity.csv)
- [Revised CGM Claim](revised_cgm_claim.md)
- [Final CGM Scorecard](cgm_scorecard.csv)
- [Source/hash manifest](source_manifest.json) and [hash list](source_hashes.csv)

## Executive verdict

Phase 13E shows that the repository's capability and intelligence **metrics can be computed reproducibly across the ten-seed synthetic cohort**. It also shows a persistent capability object and positive movement in the capability score. These are valid results about the frozen measurement pipeline.

They do **not**, by themselves, validate the construct labels “capability growth” or “intelligence growth.” The key measurement fact is that `C_t` is a weighted score of a capability's skill utility, transfer score, coverage, and composition bonus; it is not a count of newly formed capabilities. In the Phase 13E ASFT arm there is exactly one capability in every seed at every round: the same `cap-cross-domain` object persists, while its score and member inventory change. Capability count rises at round 1, then stays at one; the scored C_t rises thereafter as the existing portfolio's measured components change.

`IG` is a configured weighted sum of CGR, transfer growth, utility growth, coverage growth, and composition growth. `IGR` is the first difference of that composite; `IE` is `IG / cumulative experiences`. These are internally defined indices, not independent tests of intelligence. Phase 13E's positive mean IG/IGR is especially sensitive to the initial transition from a zero previous state: mean IG is about `0.657` in round 1 and only `0.036` in round 4; IGR is negative in rounds 2 and 4; IE falls sharply as the initial increment is divided by a growing experience denominator.

Cross-phase results weaken a robust-growth interpretation: Phase 13D's corrected mean CGR is `-0.060` over nine evaluable seeds, while Phase 13E's mean is `+0.2946` over ten. Phase 13E's TS→CGR relationship is negative (`r=-0.5027`, CI crosses zero), and its no-SCT ablation does not reduce CGR. Composition has negative incremental value versus the best single skill (`-0.1429`) and no post-composition capability-count gains. Phase 13F baseline results are comparator-dependent. Phase 13G produces no validated ARC capability unit, so external validity is unavailable.

**Important correction to the proposed 14E-5 wording:** the preregistered Phase 13E *C_t-to-next-round-task-utility* prediction criterion did pass: `r=0.0498`, seed-clustered 95% CI `[0.0163, 0.0922]`, with 10 seed clusters and 30 within-seed round pairs. This is a very small, same-generator association (approximately `r²=0.0025` descriptively), not a robust or causal growth-to-performance effect. It is distinct from the negative TS→CGR correlation. Therefore “future prediction unsupported” is too absolute for the frozen 13E endpoint; the defensible conclusion is **weak within-cohort predictive association, no evidence for a substantial, causal, or externalizable effect**.

## Metric interpretation: what the pipeline computes

| Measure | Frozen operational definition | What a positive value establishes—and does not establish |
|---|---|---|
| `C_t` | Mean non-archived capability score; each score is weighted mean skill utility, mean transfer score, capability coverage, and composition bonus | A higher portfolio score under these components; not necessarily more capability objects, broader competence, or external capability. |
| `CGR` | `(C_t − C_(t−1)) / Δt`; first round compares against a zero previous state | Change in the internal score under the frozen update; first-round formation contributes a large initialization jump. |
| `CCG` | Round-to-round change in union of successful target-family coverage divided by the four synthetic task families | Coverage movement in this generator; not open-world breadth or semantic generalization. |
| `IG` | `.35*CGR + .25*TG + .20*UG + .15*CCG + .05*CompG` | Positive weighted composite of internal growth deltas; not an independent measure of intelligence. |
| `IGR` | `(IG_t − IG_(t−1)) / Δt` | Change in the composite index; can be negative while the across-round mean remains positive. |
| `IE` | `IG / cumulative experiences` | Ratio of the internal index to task/trace count; a negative slope means this ratio declines, not that an independently measured cognitive efficiency declined. |

The Phase 13E frozen config gives C_t/CapU weights `.40 SU + .25 TS + .20 coverage + .15 composition`; SU and transfer values are repository skill metrics. Since the components can change as member skills are reused or added, C_t can rise while the number of capability objects remains constant. In Phase 13E the mean task utility is also derived from task success minus reasoning cost/100, so the predictor/target are task-process related; they are not independent external constructs.

## 14E-1 — CGM claim review

| Thesis claim | Phase 14E judgment | Evidence-weighted reading |
|---|---|---|
| CGM-1: capabilities emerge from skills | **Partially supported as validated skill aggregation** | A cross-domain capability object built from reflection/rotation skills persists 10/10 seeds. No accepted higher-order/emergent-type capability occurrence; evidence is stronger for representation/aggregation than new capability emergence. |
| CGM-2: capabilities grow over time | **Partially supported as C_t score growth in 13E** | C_t rises monotonically in 10/10 seeds; one capability object remains present. Corrected 13D mean CGR is negative. Do not generalize metric growth to robust ontological growth. |
| CGM-3: capability growth predicts future performance | **Weakly supported only for one preregistered 13E association** | C_t→next-round task utility `r=.0498`, CI `[.0163,.0922]`, criterion pass; tiny, same-generator, 10-cluster result, noncausal. The separate TS→CGR relation is negative/uncertain; no strong transfer-to-growth chain. |
| CGM-4: intelligence growth can be measured | **Metrics computable; intelligence interpretation not validated** | IG/IGR/IE are repeatably computed, but are formula-derived composites of the same internal growth inputs; no independent behavioral or external construct validation. |
| CGM-5: capability growth is a proxy for intelligence growth | **Not supported** | No external validation or independent criterion; overlap between C_t and IG is built into their formulas, not evidence of proxy validity. |

## 14E-2 — Phase 13E trajectory: averages versus time path

The preregistered seed-level summaries are correct, but means across four rounds hide the large first-round transition and non-monotonic IG/IGR path. ASFT round means from saved `seed_round_arm.csv`:

| Round | Mean C_t | Mean CGR | Mean IG | Mean IGR | Mean IE | Mean CCG | Mean CompG |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | `0.8405` | `0.8405` | `0.6573` | `0.6573` | `0.01369` | `0.90` | `0` |
| 2 | `0.9599` | `0.1194` | `0.0801` | `-0.5772` | `0.00125` | `0.10` | `0` |
| 3 | `1.1122` | `0.1523` | `0.1442` | `0.0641` | `0.00180` | `0` | `1` |
| 4 | `1.1785` | `0.0663` | `0.0362` | `-0.1080` | `0.00038` | `0` | `0` |

Across independent seeds, Phase 13E reports mean CGR `0.2946` (95% CI `[0.2857,0.3036]`), mean IG `0.2294` (`[0.2245,0.2343]`), mean IGR `0.00904` (`[0.00903,0.00906]`), mean IE `0.0043` (`[0.0041,0.0044]`), and IE slope `-0.00394` (`[-0.00421,-0.00367]`). The positive means and the time path are both retained; neither is selectively substituted for the other.

C_t is monotonic in 10/10 ASFT seeds and a capability persists across at least two consecutive rounds in 10/10. However, exactly one capability is present at every round in all 10 seeds. New capability count is 1 at round 1 and 0 thereafter. Thus “positive capability trajectory” here means a repeated increase of the score attached to a persistent portfolio—not a growing number of capabilities.

## 14E-3 — Capability emergence and composition

Phase 13E's accepted `cap-cross-domain` capability combines reflection and rotation skills. It is present across all four rounds; its state progresses from developing to established to core, and its member set expands from two skills to three when a composed skill is added. This supports a validated capability representation/aggregation layer and persistence in the tested system.

It does not show broad higher-order emergence: accepted emergent-type occurrences are zero; the capability count remains one; zero of ten seeds meet the descriptive round-4-over-round-2 capability-count growth condition with successful held-out composition. Held-out composition incremental gain is `-0.1429` versus the best single component. A successful composition evaluation can still have negative incremental value when its cost is worse than the best single skill.

Because composition membership/bonus enters C_t and CompG enters IG, an internal score can increase when the composition object is added even though its incremental task value is negative and no new capability object is created. This is a measurement result, not proof composition generated new capability.

## 14E-4 — Growth, transfer, prediction, and phase comparison

- **Phase 13E CGR/IG:** positive preregistered cohort means and monotonic C_t in 10/10 seeds; evidence for the defined scores increasing in this synthetic cohort.
- **Phase 13D corrected CGR:** mean `-0.060` over nine evaluable seeds. This directly limits cross-context robustness; it does not falsify the arithmetic metrics, but shows outcomes are generator/phase dependent.
- **Transfer to growth:** Phase 13E TS→CGR is `r=-0.5027`, 95% Fisher interval `[-0.8601,0.1857]`; it is uncertain and directionally negative. Phase 13D TS↔CGR is `r≈+0.483` over 36 observations in nine seed clusters, while its mean CGR is still negative. Directions differ across protocols, and neither association is causal.
- **Growth to future task utility:** distinct endpoint: Phase 13E's preregistered C_t→next-round task-utility `r=0.0498`, 95% cluster-bootstrap interval `[0.0163,0.0922]` passes its frozen directional gate. The association is small and only within this synthetic generator/cohort; it tests the capability score C_t, not CGR as a predictor, is not a test of transfer causing growth, and is not an external validation.
- **Internal metric coupling:** Phase 13E SU→CGR is `r=0.993` across ten seed summaries (descriptive). This close association is consistent with overlapping internal performance-derived ingredients; it is not independent validation of CGR.
- **Ablation check:** Phase 13E A2_NO_SCT does not reduce CGR relative to ASFT under the frozen gate (observed CGR contrast `0.0000`). This weakens the claim that transfer is necessary for the observed CGR.

## 14E-5 — Baseline interpretation

### Phase 13E

ASFT's paired baseline criterion requires positive lower bounds for both final C_t and mean held-out task utility. It fails B1 even though final C_t is higher, because task utility is lower:

| Comparator | ASFT minus comparator: final C_t | ASFT minus comparator: all-task utility | Frozen decision |
|---|---:|---:|---|
| B1 no learning | `+1.1785` (lower CI `+1.1428`) | `-0.0361` (lower CI `-0.0363`) | **Fail** |
| B2 skill storage only | `+1.1785` | `+0.0773` | Pass |
| B3 random skill creation | `+0.1603` | `+0.0776` | Pass |
| B4 compression proxy | `+0.3455` | `+0.0752` | Pass |

### Phase 13F

Its joint gate requires both task utility and CGR to improve. ASFT fails B1 (utility `-0.0363`, CGR `+0.2872`) and ties B3 (both differences zero); it passes B2 (utility `+0.0749`, CGR `+0.2872`) and B4 (utility `+0.0749`, CGR `+0.0814`). B4 remains a compression proxy, not canonical DreamCoder.

**Judgment:** capability-metric and task-utility superiority are comparator- and phase-dependent. Higher C_t versus an empty B1 metric does not erase lower task utility; positive CGR is not synonymous with better downstream performance.

## 14E-6 — Intelligence metrics and validity

Phase 13E reports positive mean IG (`0.2294`) and IGR (`0.00904`), but the code defines IG as a weighted sum of CGR, transfer-score change, CapU change, family-coverage change, and composition-count change. The values therefore establish that this formula produced positive averages. They do not supply an independent intelligence criterion.

The path matters: mean IG is highest in round 1 (`0.6573`) and falls to `0.0362` by round 4; IGR is strongly negative in round 2 (`-0.5772`) and negative again in round 4 (`-0.1080`). IE is literally IG divided by cumulative experiences; its mean is positive, while its slope is negative. Calling the falling ratio “less intelligence gained per experience” is only a label-level interpretation unless IE is validated against an independent capability-acquisition target.

No human, real-world, held-out domain, or external intelligence measure validates IG, IGR, or IE. Phase 13H's CGM synthesis accordingly treats these as repository-defined synthetic growth metrics, not general intelligence measurements.

## 14E-7 — ARC and external validity

Phase 13G's bounded ARC adapter produced zero accepted invariants, zero skill candidates/promotions, and zero capability groups. CGR/IG/IGR were unavailable where validated capability units/components were absent. This is a failure of the upstream candidate/coverage pipeline to instantiate CGM in this adapter, not a measured negative CGM effect and not evidence that ARC has no capability growth. It leaves ARC external validity **not demonstrated**.

## 14E-8 — Why the metrics appear positive

Two explanations remain compatible with the evidence:

1. **Real but narrow improvement:** verified skill reuse and expanding member evidence can improve the performance-related components of one synthetic capability score.
2. **Accumulation/generator coupling:** repeated synthetic tasks increase measured utility, transfer opportunities, family coverage, and composition features; those same ingredients mechanically raise C_t/IG. One existing capability can gain members/score without new capability emergence or external generalization.

Phase 13E cannot cleanly separate these explanations. Its controls and ablations help locate pipeline behavior, but the failed B1 utility comparison, no-SCT CGR tie, negative composition incremental value, phase-13D CGR reversal, and missing ARC pathway limit the strong interpretation.

## 14E-9 — Threats to validity

See [`threats_to_validity.csv`](threats_to_validity.csv). Highest-severity risks: construct/criterion contamination in composite scores; no accepted higher-order capability; phase- and generator-dependent CGR; small and low-magnitude within-cohort prediction; mechanically coupled C_t/IG inputs; negative IE slope under a ratio definition; negative composition value; comparator dependence; and no ARC capability unit.

## 14E-10 — Revised CGM claim

> **“The frozen Phase 13E pipeline reproducibly computes capability-oriented portfolio scores and derived growth indices, with a persistent synthetic capability and positive mean C_t/CGR/IG values in its ten-seed cohort. These findings establish metric behavior and score growth within that generator, not robust capability emergence or intelligence growth. The preregistered C_t-to-next-round task-utility association is positive but very small and same-cohort; transfer-to-growth is inconsistent, composition yields no positive incremental value or capability-count growth, baseline superiority is mixed, and ARC capability growth is unavailable.”**

## 14E-11 — Final CGM scorecard

| Claim | Status | Basis |
|---|---|---|
| Metrics are internally computable | ✅ Supported | Frozen APIs and Phase 13E records compute C_t, CGR, CCG, IG, IGR, IE. |
| Capability persistence | ✅ Supported narrowly | Same capability object persists ≥2 rounds in 10/10 seeds. |
| Positive C_t/CGR in 13E | ✅ Supported in cohort | CGR mean `.2946`, CI `[.2857,.3036]`; C_t monotonic in 10/10. |
| Robust capability growth across phases | 🟡 Partial / not robust | 13E positive, corrected 13D CGR mean `-.060`; protocols differ. |
| Capability emergence from skills | 🟡 Partial | Validated cross-domain aggregation; no accepted higher-order emergent type. |
| Positive IG/IGR values | ✅ Computed, metric scope | IG `.2294`, IGR `.00904`; time path includes large initialization and negative IGR rounds. |
| IG/IGR measure intelligence | ❌ Not established | Weighted internal composite; no independent construct validation. |
| IE reflects intelligence efficiency | ❌ Not established | IE is IG divided by experiences; slope `-.00394`, not externally validated. |
| C_t predicts next-round task utility | 🟡 Weak within-cohort association | Preregistered gate passes, `r=.0498`, CI `[.0163,.0922]`; small, 10 clusters, synthetic. |
| Transfer drives CGM growth | ❌ Not supported | TS→CGR `r=-.503` in 13E; 13D direction differs; no-SCT ablation CGR tie. |
| Composition creates capability/value | ❌ Not supported | Composition incremental gain `-.1429`; 0/10 count gains; zero accepted higher-order instances. |
| ASFT universally beats baselines | 🟡 Mixed | 13E fails B1; 13F fails B1/B3, passes B2/B4. |
| ARC capability growth | ⚪ Not demonstrated | No eligible ARC capabilities, so growth metrics unavailable. |

**Exit decision: Phase 14E COMPLETE.** CGM survives as a computable synthetic metric framework with one-cohort score growth and persistence. Capability-growth and intelligence-growth interpretations remain substantially narrower than the metric names imply.

## Evidence sources

- Phase 13E: [`evidence_package.md`](../PHASE-13E-CAP-GROWTH-V1/evidence_package.md), [`analysis.json`](../PHASE-13E-CAP-GROWTH-V1/analysis.json), [`seed_summary.csv`](../PHASE-13E-CAP-GROWTH-V1/seed_summary.csv), [`seed_round_arm.csv`](../PHASE-13E-CAP-GROWTH-V1/seed_round_arm.csv), [`capability_formation.csv`](../PHASE-13E-CAP-GROWTH-V1/capability_formation.csv), [`composition_task_level.csv`](../PHASE-13E-CAP-GROWTH-V1/composition_task_level.csv), [`robustness_probes.csv`](../PHASE-13E-CAP-GROWTH-V1/robustness_probes.csv), [`config.json`](../../../experiments/phase13e/config.json), [`preregistration.md`](../../../experiments/phase13e/preregistration.md), [`metrics.py`](../../../experiments/phase13e/metrics.py), [`statistics.py`](../../../experiments/phase13e/statistics.py).
- Phase 13D corrected: [`posthoc_analysis.md`](../PHASE-13D-TRANSFER-V1/posthoc_analysis.md), [`posthoc_corrected_criteria.json`](../PHASE-13D-TRANSFER-V1/posthoc_corrected_criteria.json), [`task_level.jsonl`](../PHASE-13D-TRANSFER-V1/task_level.jsonl).
- Phase 13F: [`evidence_package.md`](../PHASE-13F-BASELINE-ABLATION-V1/evidence_package.md), [`master_result_matrix.csv`](../PHASE-13F-BASELINE-ABLATION-V1/master_result_matrix.csv).
- Phase 13G: [`evidence_package.md`](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/evidence_package.md), [`summary.json`](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/summary.json), [`growth.csv`](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/growth.csv).
- Phase 13H: [`Package C — CGM`](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/package_C_CGM.md), [`claim evidence matrix`](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/claim_evidence_matrix.csv), [`negative evidence register`](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/negative_evidence_register.csv).
- Metric source: [`growth_metrics.py`](../../../src/evaluation/growth_metrics.py), [`intelligence.py`](../../../src/evaluation/intelligence.py), [`capability utility`](../../../src/capability/utility.py), [`capability portfolio`](../../../src/capability/portfolio.py).
