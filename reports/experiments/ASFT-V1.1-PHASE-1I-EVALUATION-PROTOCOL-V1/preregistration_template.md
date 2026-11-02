# Phase 1I.3 — Confirmatory/Replication Preregistration Template

> Complete, review, timestamp, and hash this document **before outcome access**. A blank template is not a preregistration and confers no confirmatory status. See `experiment_classification_framework.md` and `governance_rules.md`.

## A. Identity and class

- Experiment ID/version: `[required]`
- Class: `[E1/E2/E3/E4; one only]`
- Replication type if E4: `[R1/R2/R3/R4]`
- Registration date/time, custodian, independent reviewer: `[required]`
- Outcomes previously inspected? `[yes/no; describe scope/access logs]`
- Claims permitted from this experiment: `[specific claim IDs]`
- Protocol parent/replication link: `[if applicable]`

## B. Research question and hypothesis

- Research question: `[one answerable question]`
- Primary hypothesis and direction: `[specific; no bundled mechanisms]`
- Null/alternative or estimand: `[define]`
- Minimum meaningful effect / SOI: `[value, units, rationale, source]`
- Claim scope/population/domain: `[define]`
- Competing explanations and falsifiers: `[memory, frequency, compression, random, representation, etc. as relevant]`
- What result would contradict the claim? `[state before outcomes]`

## C. Design and sample

- Design: `[randomized/paired/clustered/observational; explain assignment]`
- Independent unit: `[seed/panel/task family/candidate pool/agent/domain; identify the unit at which treatment is independent]`
- Nested/repeated units: `[tasks, candidates, rounds, outputs; relationship to independent unit]`
- Number of independent units and sample-size rationale: `[power/precision simulation; code/data hash; target N and stopping rule]`
- Inclusion/exclusion rules: `[freeze before outcomes; list all planned exclusions]`
- Randomization, blocking, pairing, order, blinding: `[method/seed/hash]`
- Training/development/confirmatory/replication split manifest hashes: `[disjointness proof]`
- Sample-size adaptation, interim analyses, stopping: `[none unless prespecified; alpha-spending if applicable]`

## D. Intervention and comparator registry

- ASFT implementation and mechanism switches: `[version/hash]`
- Mandatory Phase 1H baseline IDs and exact implementations: `[BL1–BL7; mark N/A with justification]`
- Required mapped ablations: `[A1–A9; state applicability/manipulation check]`
- Candidate pool/task opportunity definition: `[hash, eligibility, action set]`
- Budgets: `[task exposure, compute/wall time, storage, candidate/query/attempt caps, horizon]`
- Comparator activation and decision-divergence measure: `[freeze]`
- Fairness/integrity gates: `[same tasks/splits, pool when relevant, resources, exposure, evaluator, config/runtime parity]`

## E. Endpoint specification

Exactly **one primary endpoint** is decision-driving.

- Primary endpoint ID: `[one]`
- Operational definition, data source, units, direction: `[required]`
- Analysis population and denominator: `[e.g. intention-to-treat per eligible opportunity]`
- Measurement validity and independent gold/evaluator: `[who/what; blinding; construct boundaries]`
- Primary estimator and contrast direction: `[e.g. ASFT − comparator]`
- SOI and interval/decision rule: `[freeze]`
- Multiplicity handling across mandatory contrasts: `[family and method]`
- Secondary endpoints (supportive only): `[IDs, definitions, multiplicity]`
- Diagnostic metrics (mechanism understanding only): `[IDs; explicitly non-decision-driving]`
- Internal scores excluded from external target labels/scoring: `[confirm: no IG/IGR/IE/CGR/C_t etc. unless specifically validated and permitted]`

## F. Statistical analysis

- Estimator/model and covariates: `[fully specified]`
- Independent-unit analysis and clustering: `[cluster bootstrap/random effects/paired aggregation; unit count, not row count, drives inference]`
- Uncertainty interval and confidence/posterior level: `[freeze]`
- Exact tie and zero-variance handling: `[report counts; no undefined standardized effect]`
- Missing-data policy: `[complete-case with denominator / multiple imputation / bounded sensitivity / other preregistered strategy]`
- Missingness threshold, reasons, and sensitivity analysis: `[freeze]`
- Denominator hierarchy: `[eligible/offered/selected/attempted/completed/successful/missing; primary denominator]`
- Outliers, transformations, multiplicity, subgroup/interaction analyses: `[freeze; exploratory labels]`
- Five-state claim rule: `[supported/contradicted/inconclusive/unavailable/non-informative; SOI and pressure gates attached]`

## G. Data handling and outcome access

- Dataset provenance/license/split/access rules: `[record]`
- Gold/label custody and blinding: `[separate custodian, access control]`
- Outcome-store location, seal/hash, access log: `[record; no analyst access before lock]`
- Permitted development data and tuning boundary: `[identify]`
- Test/external data exposure history: `[disclose downloads, parsing, predictions, queries, and prior use]`
- Security/leakage checks: `[features, logs, source-code audit, automated assertions]`
- Immutable artifact list: `[data, code, config, environment, evaluator, analysis, report schema hashes]`

## H. Replication plan

- Independent replication class/type: `[R1/R2/R3/R4; if generalization claimed, R2/R3/R4 required]`
- Independent sampling frame and disjoint manifest: `[hash/source]`
- Frozen protocol/effect direction/endpoint/SOI: `[same as confirmatory unless explicit, justified deviation]`
- What constitutes successful replication: `[predeclare]`
- How conflict, null, failure, or unavailability will be reported: `[predeclare]`

## I. Reporting and governance lock

- Report all primary, secondary, negative, null, inconclusive, non-informative, and unavailable results: `[confirm]`
- Protocol deviations and corrections ledger: `[append-only owner/location]`
- No post-outcome threshold/endpoint/split/baseline/budget/decision-rule changes: `[confirm]`
- Amendment policy: `[version, date, reason, outcome-access state; new data required post-outcome]`
- Source lineage and SHA-256 manifest: `[location]`
- Statistical code frozen before outcome access: `[hash]`
- Signatures: investigator, data custodian, statistician, independent reviewer: `[complete]`

**Preregistration status:** `[complete/incomplete; E3/E4 eligibility is blocked unless complete and independently reviewed]`