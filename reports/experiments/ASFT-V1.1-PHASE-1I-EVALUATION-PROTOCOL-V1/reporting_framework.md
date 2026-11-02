# Phase 1I.8 — Reporting Framework

Every E3/E4 report must be completed regardless of result direction. Report null, negative, contradictory, inconclusive, unavailable, and non-informative outcomes as first-class results.

## Mandatory report sections

1. **Identity and class:** experiment ID/version, E1–E4, replication type, timestamps, preregistration link/hash, deviations/amendments.
2. **Research question and hypothesis:** registered wording, estimand, direction, population, claim scope, SOI.
3. **Design:** assignment/sampling/independent unit, sample-size rationale, inclusion/exclusion, randomization/blinding, splits, task families, baseline/ablation IDs, budgets and evaluator.
4. **Endpoint map:** exactly one primary; secondary and diagnostic endpoints clearly separated; operational definitions, units, directions, denominators, validation boundaries.
5. **Primary result:** effect estimate, uncertainty interval, SOI, exact rule, five-state decision, multiplicity result, independent-unit N, nested rows, eligible/attempted/completed denominator, missing count/rate.
6. **Activation and fairness:** component activation, comparator divergence/selection overlap, matched tasks/candidates/budgets/storage/compute/horizon, config/runtime parity, integrity checks.
7. **Secondary results:** all registered supportive endpoints and multiplicity controls; do not promote a favorable secondary after a primary miss.
8. **Negative/null/contradicted results:** enumerate every failed gate, alternative win, tie/equivalence, negative ablation, and adverse outcome.
9. **Unavailable and non-informative results:** list by endpoint/stage with reasons; distinguish missing/undefined from valid zero and identical-decision degeneracy.
10. **Limitations and validity:** construct, internal, statistical, implementation, external, and interpretation limits; explain posthoc corrections and holdout exposure.
11. **Interpretation:** use frozen language and scope; state what is and is not demonstrated; no causal or generalization claim beyond design.
12. **Replication:** status/type, independent manifest, concordance/conflict, and whether generalization criteria were met.
13. **Lineage:** code/config/environment/evaluator/data/analysis hashes; source manifest; access logs; correction/version ledger.

## Mandatory tables

### Primary outcome table

`claim_id | endpoint_id | hypothesis | effect | interval | SOI | decision | state | independent unit | independent N | nested rows | denominator | missing n/rate | exact ties | zero variance`

### Arm and activation table

`arm_id | baseline/ablation version | eligible | offered | queried | selected | attempted | completed | valid | correct | failed | no-match | budget used | activation rate | divergence/overlap`

### Deviations and corrections ledger

`deviation_id | date | before/after outcome access | files/hashes | change | reason | impact | original preserved | new analysis needed`

## Selective-reporting prohibition

Report all preregistered primary and secondary outcomes, all specified comparator contrasts, all exclusions, and all outcomes that are unavailable or non-informative. Provide a deviation table even when empty. “No negative outcomes” must be explicitly stated only after every registered result is enumerated. Public abstract/summary language cannot exceed the full report's evidence ceiling.