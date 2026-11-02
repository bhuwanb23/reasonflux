# Phase 1H — Baseline, Ablation, and Fairness Preregistration Template

**Status:** framework template only; no future Phase 1B–1G empirical run is authorized by this package.

## Experiment identity and freeze

- Phase/claim/question/version/date: `[complete before outcomes]`
- Code, config, environment, evaluator, and metric hashes: `[complete]`
- Preregistration timestamp and independent reviewer: `[complete]`
- Independent unit, clustering, power/precision analysis, N: `[complete]`
- Primary/secondary endpoint, SOI, uncertainty and multiplicity plan: `[freeze]`

## Baseline registry

For each mandatory slot, provide implementation ID/version, allowed information, candidate/task pool, training exposure, activation rule, budget/storage/compute cap, evaluation horizon, expected decision vector, and endpoint:

- BL1 No Learning: `[specify what is disabled and retained]`
- BL2 Memory/Retrieval: `[subtype; raw trace vs exact replay vs skill store explicitly distinguished]`
- BL3 Random: `[candidate pool, decision count, seeds, randomization protocol]`
- BL4 Frequency: `[training-only counts/recency, transforms, ties]`
- BL5 Compression: `[exact method; proxy vs canonical algorithm disclosed]`
- BL6 Hybrid Memory+Frequency: `[fixed combination and weights]`
- BL7 Oracle (analysis only): `[gold/latent information and strict isolation]`
- Optional B6a heuristic/other declared baselines: `[feature scope and implementation]`
- Not-applicable slots and rationale: `[independent approval]`

## Ablation registry

For each A1–A9: component being disabled, claim tested, manipulation check, expected downstream deactivation, unaffected components, matched task/candidate set, budget, exposure, activation opportunities, endpoint, and analysis. No omissions without preregistered rationale.

## Fairness and comparator activation

- Same task/split manifest hash across arms: `[verify]`
- Common candidate pool for ranking claims: `[hash/eligibility rules]`
- Budget/config/runtime parity assertion: `[automated result]`
- Storage, compute, wall time, query, exposure and horizon caps: `[freeze]`
- Eligible/offered/selected/attempted/completed/failed denominators: `[schema]`
- Evaluator/gold isolation and access log: `[verify]`
- Pairwise rank/set overlap and decision divergence metric: `[freeze]`
- Minimum meaningful divergence/activation opportunity: `[development-calibrated, freeze]`
- Fairness gate and response to any mismatch: `[fail/unavailable; no outcome salvage]`

## Decision and interpretation lock

- Baseline comparison effect direction: `[define ASFT minus comparator]`
- SOI and win/tie/baseline-win/inconclusive/unavailable rules: `[freeze]`
- Ablation effect direction (`full − ablated`) and positive/no-measurable/negative/inconclusive/unavailable rules: `[freeze]`
- `non_informative_identical_decisions` and `unmatched_*` rules: as framework, confirm for this experiment.
- Interpretive rules 1–14: frozen in `interpretation_rules.md`; no post-outcome reinterpretation.
- Governance amendments: versions/amendments made before outcome access only; post-outcome changes require new independent confirmation.

## Replication and signatures

- Confirmatory and replication manifests disjoint: `[hashes]`
- Same baseline/ablation versions and resource rules in replication: `[verify]`
- Data custodian, implementer, statistician, independent reviewer signatures: `[complete]`
- Empirical authorization/readiness approval: `[separate authorization; not granted here]`