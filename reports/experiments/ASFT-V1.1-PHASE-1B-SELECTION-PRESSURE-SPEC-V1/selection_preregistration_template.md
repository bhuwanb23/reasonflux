# 1B.9 — RQ2 Preregistration Template (Frozen Design Fields)

**Phase:** ASFT-V1.1-PHASE-1B / RQ2 benchmark design; confirmatory evaluation is planned for the designated later experiment phase.  
**Protocol ID:** `ASFT-V1.1-RQ2-SELECTION-PRESSURE-V1`  
**Status:** design template frozen; run-specific code/config/data hashes must be completed before confirmation.  
**No confirmatory outcomes have been collected in Phase 1B.**

## Frozen question and hypotheses

**RQ2:** Does SCV improve skill-selection decisions when good, bad, and neutral candidates compete?  
**H1:** SCV improves held-out selected-set future utility under fixed capacity.  
**H0:** SCV has no incremental decision value relative to the required simpler selectors.  
**Primary endpoint:** selected-set Future Net Value per slot (`Y_bs`, TEU/slot).  
**SOI:** +0.10 TEU/slot.  
**Independent unit:** candidate-panel batch seed.  
**Primary policy:** S1 SCV using frozen legacy `SCV10` formula and top-eight-positive rule.

## Confirmatory comparisons

Paired S1-minus-S2, S3, S4, S5, and S6 contrasts on the same candidate batch and task lanes. S7 oracle is diagnostic only. Familywise α=.05 with Holm adjustment. Primary formula and decision categories are specified in `selection_metrics.md` and cannot be replaced after outcomes.

## Frozen design values

- Candidate panel: N=20, four each of Types A–E; eight creation slots; fixed ten-opportunity horizon.
- Type value thresholds and challenge rules: `candidate_taxonomy.md`.
- Value/cost formula and frozen SCV equation: `candidate_value_definition.md`.
- Selector algorithms and tie breaks: `selector_competition_spec.md`.
- Pressure gate/SDR: `selection_pressure_design.md`.
- Baseline parity: `baseline_fairness_protocol.md`.
- Split structure and N rule: `selection_dataset_protocol.md`.
- Missingness: no imputation; preserve zero/unavailable/failed separately; complete-batch analysis; >5% incomplete confirmatory batches makes primary outcome unavailable/inconclusive.
- Software failures: no outcome-informed reruns, redraws, threshold changes, or candidate substitutions. Preserve partial records and reserve use.

## Sample-size and replication commitment

At least 100 independent confirmation batches and the same number in replication. Final N is the deterministic calibration-only power-rule output in the dataset protocol (90% power at SOI under the Holm family, maximum 300); record the exact N, variance inputs, simulation seed/code, and output here before confirmation. If the rule requires >300, stop and redesign rather than run underpowered confirmation. Replication uses disjoint IDs/seeds and the identical frozen method; it is same-generator replication, not external-domain replication.

## Required pre-unlock registration fields

Fill these before any confirmatory outcome access; a missing field blocks confirmation:

- Registration timestamp and public/private immutable archive URI: `[complete before run]`
- Protocol version/hash: `[complete]`
- Selector source commit/hash and unit/contract-test report: `[complete]`
- Candidate generator and configuration hashes: `[complete]`
- Pressure-checker hash and golden fixture pass: `[complete]`
- Calibration/development/confirmatory/replication seed manifests and hashes: `[complete]`
- Resource instrumentation, calibration conversion `lambda`, and calibration report hash: `[complete]`
- Final N, power simulation hash, α/multiplicity code hash: `[complete]`
- Outcome-store access control / unlock protocol: `[complete]`
- Analysis script hash and report template hash: `[complete]`

## Preregistered outcomes

- **Supported:** all pressure/validity gates pass; every adjusted lower confidence bound for S1-minus-S2…S6 exceeds +0.10 TEU/slot; replication estimates remain positive for all simple selectors and show no meaningful reversal. State synthetic balanced-panel scope.
- **Contradicted:** all gates pass and a required comparator has an adjusted upper bound below −0.10, or equivalence within ±0.10 is established against the strongest simple selector. Report the comparator-specific failure.
- **Inconclusive:** pressure and integrity pass but neither the support nor contradiction rules are satisfied; or confirmation and replication conflict without decisive intervals.
- **Unavailable:** pressure, denominator, cost conversion, instrumentation, split, or implementation validity fails. No effect interpretation.

## Declaration

The outcome labels and confirmatory outcomes are not used to define SCV, tune selectors, curate confirmatory panels, select an endpoint, or change the decision rule. The balanced challenge taxonomy is generated from predeclared latent mechanisms; all candidate choices are locked before label/outcome release. Any protocol deviation is versioned and reported, with no claim that the affected comparison is confirmatory.