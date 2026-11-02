# Phase 1F / RQ5 — Preregistration Template

**Status:** design template; blank run-specific fields are pending. This document does not authorize empirical execution.

## Frozen identity and integrity

- Protocol/version/date: `[complete]`
- Task generator, policy, evaluator, A–F battery, rubric, and code hashes: `[complete]`
- IG implementation/config and predictor snapshot hash: `[complete; no formula tuning]`
- B1–B5 feature derivations and provenance: `[complete]`
- Development/confirmatory/replication manifest hashes: `[complete]`
- Independent gold custodian/access log and sealed-store proof: `[complete]`
- IG-disabled target scorer reproducibility hash: `[complete]`
- Budget, exposure, missingness, and exclusion code hashes: `[complete]`

## Construct and endpoint

- Frozen working intelligence definition: `intelligence_definition.md`.
- Taxonomy I1–I6 and battery tests A–F: `intelligence_taxonomy.md`, `intelligence_battery_spec.md`.
- Primary endpoint: Test A future learning-rate normalized AULC at exposures `[0,1,3,5]`.
- Primary candidate predictor: IG_t. Key secondary predictor: IGR_t, tested on Test A with Holm familywise adjustment. IE remains exploratory. IGR cannot rescue a failed IG_t primary claim.
- Primary SOI: `0.02` AULC MAE improvement.
- Secondary endpoint families and multiplicity method: `[freeze]`.

## Comparator and model lock

- B1 past performance: `[feature/rubric/time window]`
- B2 experience count: `[exposure definition]`
- B3 capability score: `[legacy C_t and independent prior behavioral score kept distinct]`
- B4 memory strength: `[probe, precision/coverage, store-size field]`
- B5 transfer metrics: `[legacy TS and prior external transfer kept distinct]`
- R7 random/chance and IG-permutation baselines: `[algorithm/seeds]`
- M0 transforms/model/blocked validation: `[freeze on development]`
- M1 = M0 + IG_t; transformations and fitting: `[freeze]`
- Primary estimand: `MAE(M0) − MAE(M1)` on Test A AULC.
- Positive IG slope and CI method: `[freeze]`

## Sample size, inference, and decisions

- Independent panel unit and domain/family clusters: `[freeze]`
- Development-only precision/power simulation, assumptions, code/seed: `[complete]`
- Final confirmatory and replication independent N: `[freeze before confirmation]`
- Cluster-aware CI/resampling and blocked prediction method: `[freeze]`
- Missingness thresholds and statuses: as metrics spec or stricter `[freeze]`.
- IG win/tie/loss/inconclusive/unavailable rule: as `intelligence_metrics.md`.
- Replication survival requirement: primary A wins plus at least one additional transfer/generalization/adaptation endpoint wins in both cohorts.

## Retirement commitment

- Adequately powered equivalence/loss criterion across A–F in confirmatory and replication: as `intelligence_retirement_rules.md`.
- If criteria are met, rename IG to an internal growth composite and stop using “intelligence” or “intelligence growth” for it.
- No post-result threshold changes or rescue endpoints.

## Leakage, budgets, and signatures

- Future tasks/shifts/domains unseen and disjoint: `[audit/hash]`
- Predictor snapshot ends before target window: `[verify]`
- IG disabled during target scoring and task selection: `[independent audit]`
- Gold/outcome lock precedes predictor join: `[timestamp/hash]`
- Equal exposure, context, compute, memory, and test query budgets: `[freeze and audit]`
- Evaluator blinding, split integrity, duplicate detection: `[complete]`
- Author, independent reviewer, and data custodian sign-off: `[complete]`