# Phase 1I.5 — Statistical Framework

## 1. Identify the independent unit first

The independent unit is the smallest unit independently sampled or randomized for the claim—not the number of rows in a CSV. Depending on design, it may be a seed/panel, task family, candidate pool, task, agent/run, or domain. Record the assignment unit, sampling unit, blocking/paired unit, and hierarchical nesting explicitly.

Examples:

- Many candidates nested within one seed/panel are **not** many independent replications.
- Tasks repeated across arms are paired task observations, not independent arms.
- Rounds within one agent/seed are repeated measures, not independent seeds.
- A new seed in the same generator can be an R1 replicate if the task/panel and outcome lineage are independent; changing only the random ordering of an exposed panel is not.
- Candidate-level inference requires independent candidate pools/seed clusters or a model that respects that hierarchy.

## 2. Sample-size and precision rationale

Before E3/E4 outcomes, choose N based on a prespecified smallest meaningful effect/SOI, expected variance and clustering from development-only data, desired power or precision, planned multiplicity, and expected missingness. Save code, assumptions, and simulation outputs. Report target and achieved **independent-unit counts**, plus nested row counts. A posthoc power calculation does not repair an underpowered study; wide uncertainty is inconclusive.

## 3. Estimation and uncertainty

- Freeze estimand, contrast direction, estimator, interval level, clustering/paired structure, randomization inference or model, covariates, transformations, multiplicity, and subgroups.
- Use uncertainty intervals appropriate to the assignment/sampling structure (e.g. seed-cluster bootstrap or hierarchical model when rows are clustered). Never treat nested task/candidate rows as independent to narrow intervals.
- A conventional two-sided 95% interval is the default only when no other justified interval method is preregistered; exact method and confidence/credible level must be frozen.
- If multiple required comparators/endpoints form a family, specify family-wise/multiplicity control or a conjunctive decision rule before outcomes.
- Report effect estimate, interval, units, N independent units, number of nested rows, denominator, missing count/rate, exact tie count, and zero-variance flag.

## 4. Denominator hierarchy

Record counts at each stage: sampled/assigned, eligible, offered, queried, selected, attempted, completed, valid, correct, failed, no-match/abstained, and missing. State which is the primary estimand denominator. Report intention-to-treat per eligible/assigned opportunity and conditional per-attempt performance separately when relevant. Unequal attempts can be a policy outcome, but a conditional success rate cannot replace the registered population-level endpoint.

- **Unavailable is not zero.** Undefined denominator, absent endpoint, masked-by-design metric, or unusable integrity record is unavailable.
- A valid zero outcome (e.g. observed zero successes among a nonzero eligible denominator) is zero, not missing.
- Never silently impute missing outcomes as zero. Missing-value treatment must be preregistered; show missingness reasons and sensitivity analysis.
- If missingness exceeds the registered threshold, classify according to the frozen policy; absent another valid analysis, the claim is unavailable, not a failure.

## 5. Ties and zero variance

Report exact ties and zero variance explicitly for arms, paired differences, selection sets, and candidate rankings. Do not divide by zero, omit tied rows, or report a standardized effect when the denominator variance is zero. An exact score tie may be informative if decisions diverged and adequate independent units give a precise equivalence interval. If all decisions/selections are identical, a mechanism-selection claim is non-informative regardless of a score summary. Zero variance alone does not prove broad equivalence; the SOI, independent-unit count, and design must support that interpretation.

## 6. Statistical result status

Use the five-state framework in `outcome_state_framework.md`. For a meaningful positive-superiority claim with effect defined as ASFT minus comparator:

- `supported`: the full preregistered uncertainty interval is beyond the minimum meaningful positive effect (SOI), after required multiplicity and integrity gates.
- `contradicted`: the valid interval rules out the preregistered meaningful positive effect (including a precise tie or opposite-direction result), or a registered opposite-direction claim is supported.
- `inconclusive`: interval crosses the relevant decision boundary, sample precision is insufficient, or confirmatory and replication outcomes conflict.
- `unavailable`: endpoint/denominator is absent, integrity or fairness fails, or the registered missingness rule blocks inference.
- `non_informative`: measurable data exist but the hypothesized mechanism contrast was not activated or decisions are identical on all common eligible opportunities.

A generic failure to pass a superiority test is not automatically “contradicted”; the CI must rule out the claimed meaningful effect. Likewise, an exact point estimate of zero is not enough to claim equivalence without adequate precision.

## 7. Reporting table schema

At minimum report, per primary contrast:

`experiment_id, class, endpoint_id, estimand, arm IDs, effect, CI/interval, SOI, decision, independent unit, independent-unit N, nested rows, denominator, missing n/rate, exact ties, zero variance, activation/divergence, protocol deviations, source/hash lineage`.

Statistical inference supports only the registered estimand and sampled population. It does not by itself validate the construct, explain mechanism causality, or establish external generalization.