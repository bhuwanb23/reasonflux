# Phase 1E / RQ4 — Preregistration Template

**Status:** design template only. Blank run-specific fields are intentional; no empirical evaluation is authorized.

## Immutable identity and data

- Protocol version/date: `[complete]`
- Task generator, evaluator, A–F battery, policy/agent versions and code hashes: `[complete]`
- Development/confirmatory/replication manifests and split hashes: `[complete]`
- Independent gold store checksum, custodian, and access log: `[complete]`
- CGM metric implementation/config hash for predictor snapshot: `[complete]`
- EBCS target-scoring/construct-separation audit hash: `[complete]`
- Budget/cost conversion and missingness code hash: `[complete]`
- Exact independent panel N from calibration-only power/precision analysis: `[complete before confirmation]`

## Capability construct

- Operational definition and capability-unit thresholds: as `capability_definition.md`; any run-specific thresholds: `[freeze from development only]`.
- Taxonomy C1–C6 and battery tests A–F: as specs; applicability by family/domain: `[complete]`.
- Primary endpoint: EBCS_future and ΔEBCS; rubric and equal weights: `[freeze]`.
- Primary CGM predictor: CGR_t. C_t/IG/IGR/IE are secondary unless multiplicity is preregistered.

## Predictive comparison

- B1 past performance feature derivation: `[freeze]`
- B2 experience count: `[freeze]`
- B3 memory strength: `[freeze]`
- B4 frequency statistics: `[freeze]`
- B5 related-success recency: `[freeze]`
- M0 B1–B5 simple baseline model and transforms: `[freeze]`
- M1 M0 + CGR_t model and transformations: `[freeze]`
- Primary estimand: ΔMAE = MAE(M0)−MAE(M1)
- SOI: +0.02 absolute EBCS MAE reduction.
- Positive-direction criterion, cluster interval method, blocked folds, and panel unit: `[freeze]`
- Model comparison and multiplicity rule: `[freeze]`

## Hypotheses and decision states

- **Metric wins:** adjusted 95% lower bound for ΔMAE > +SOI and CGR slope positive with lower bound >0.
- **Equivalent tie:** ΔMAE interval lies fully within [−SOI,+SOI]; supports no practically meaningful incremental value in this target/range.
- **Metric loses:** adjusted upper bound for ΔMAE < −SOI, or CGR slope reliably negative under the directional capability-growth claim.
- **Inconclusive:** interval crosses decision boundaries or direction is uncertain.
- **Unavailable:** leakage/construct/budget/integrity failure or missingness threshold breached.

CGR's potential lack of added value is a valid outcome. Do not relabel a tie as success or claim universal uselessness beyond the prespecified population.

## Leakage, budget, and outcome lock

- Confirmatory task templates/domains kept unseen: `[verify and hash]`
- Predictor snapshot ends at time t: `[verify]`
- No test tasks/answers in memory or capability stores: `[audit]`
- Outcome scoring completed without CGM metrics: `[independent reproducibility proof]`
- Raw outcomes and EBCS locked before predictor join: `[timestamp/hash]`
- Storage/compute/query/exposure budgets and actual usage: `[freeze]`
- Family A–F exclusion/missingness rules: `[freeze]`
- No interim efficacy peeking or outcome-driven stopping.

## Sample size, replication, and signatures

- Calibration-only power/precision simulation, assumptions and code seed: `[complete]`
- Final independent panel N: `[freeze]`
- Replication on disjoint task-family/template/domain blocks: `[manifest]`
- Author/reviewer and data custodian approvals: `[complete]`
- Rank/metric lock and sealed-store proof before outcome access: `[complete]`