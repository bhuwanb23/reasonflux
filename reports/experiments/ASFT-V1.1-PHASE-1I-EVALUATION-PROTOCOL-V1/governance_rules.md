# Phase 1I.9 — Governance Rules

These are binding rules for every confirmatory v1.1 experiment. Any breach is disclosed; it is not repaired by silently changing the claim.

| Rule | Requirement | Consequence of violation |
|---|---|---|
| **G1 — Frozen protocol** | Do not change registered hypotheses, endpoints, SOI/thresholds, splits, budgets, baselines, ablations, exclusions, analysis, or decision rules after outcome access. | Mark deviation; original claim is analyzed under original protocol or unavailable if integrity is compromised; revised test requires new version and independent data. |
| **G2 — No gate relabeling** | A failed preregistered gate remains failed/contradicted under its registered estimand. | No swapping primary/secondary, lowering thresholds, or substituting a different baseline posthoc. |
| **G3 — No hiding negatives** | Publish/report negative, null, adverse, tie, inconclusive, unavailable, and non-informative results. | Report is incomplete; readiness fails. |
| **G4 — E1/E2 do not become E3/E4** | Exploratory/development outcomes can motivate a new hypothesis, never serve as confirmatory evidence for that same outcome after tuning. | New independent data and preregistration required. |
| **G5 — Unavailable is not failure** | Missing endpoint, undefined denominator, mask-by-design, or failed valid measurement is not zero and not a failure outcome. | Preserve as unavailable with reason; no zero imputation absent preregistered policy. |
| **G6 — Version every amendment** | Date, author, rationale, fields changed, outcome-access status, affected hashes, and whether independent data are needed. | Unversioned changes invalidate confirmatory interpretation. |
| **G7 — Preserve lineage** | Hash source/data/task/split/config/environment/evaluator/analysis/report; preserve original and corrected artifacts append-only. | Provenance gate fails or result is unavailable. |
| **G8 — Seal outcomes** | Custodian controls confirmatory labels/holdout; log every access, download, query, prediction, and exposure. | Exposure is disclosed and classification/reuse rules applied; compromised data cannot be called pristine. |
| **G9 — Corrections are not silent** | Correct coding/reporting errors with original retained, correction dated, saved inputs identified, and effect on conclusions quantified. | Correction is posthoc unless applied blind under a registered process; new confirmatory data may be required. |
| **G10 — One primary endpoint** | Keep primary, secondary, diagnostic endpoints separate; no outcome-driven promotion. | Gate fails if endpoint hierarchy was not frozen. |
| **G11 — No posthoc exclusions** | Apply only preregistered inclusion/exclusion/stop rules; report all removed units and reasons. | Unregistered exclusions require sensitivity analysis and downgrade. |
| **G12 — No unregistered pooling** | Do not combine phases, accounting versions, denominators, or endpoints without a prospectively harmonized estimand. | Report separately; pooled result is exploratory. |
| **G13 — Independent review** | Independent reviewer validates preregistration, access controls, analysis lock, and final status. | No confirmatory readiness sign-off. |

## Amendment timing

- **Before outcome access:** prospective amendment is allowed only if timestamped, versioned, independently reviewed, and outcomes remain sealed. The original version remains available.
- **After outcome access:** any threshold, endpoint, split, baseline, budget, or analysis change is exploratory/posthoc for exposed data. It cannot rescue the original E3/E4 result. A new confirmatory version requires independent, disjoint data.

## Reporting and retention

Store preregistration, raw outcomes, run logs, environment and source hashes, analysis code, all generated reports, access logs, and amendments in an immutable/append-only record. Report readiness and deviation status with every result.