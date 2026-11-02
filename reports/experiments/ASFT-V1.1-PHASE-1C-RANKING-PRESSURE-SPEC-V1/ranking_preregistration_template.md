# Phase 1C / RQ1 — Preregistration Template (Complete Before Confirmation)

**Template status:** design-ready; blank run-specific fields below are deliberately not filled with invented values. No confirmatory run is authorized by this template.

## Identity and immutable artifacts

- Phase/package: `ASFT-V1.1-PHASE-1C` / `ASFT-V1.1-PHASE-1C-RANKING-PRESSURE-SPEC-V1`
- Protocol version/date: `[complete]`
- Candidate generator, task runner, feature pipeline, R1–R5 code commit/hash: `[complete]`
- Configuration, candidate cards, task/family split manifest, random seeds: `[complete]`
- Endpoint/cost-conversion and analysis code hashes: `[complete]`
- Outcome-store checksum, custodian, access policy/log location: `[complete]`
- Exact independent panel N from calibration-only power/precision simulation: `[complete before confirmation]`

## Frozen question and policies

**Primary question:** Does frozen transfer-aware R1 improve held-out `FNTU@K` over each of Frequency, Reuse-only, Compression-oriented, and Random when the pre-outcome ranking-pressure gate passes?

- Candidate pool `N=40`; `K=8`; horizon `H=[freeze]`.
- Required competitors: R1 `F×C×G×T×R` with calibration-only transfer score `T`; R2 frequency; R3 reuse probability; R4 compression score; R5 seeded random; R6 Oracle analysis-only post-lock.
- Comparator family: R1−R2, R1−R3, R1−R4, R1−R5.
- Type recipe: A4/B8/C8/D4/E4/F4/G4/H4 for controlled generator; hidden from rankers.

## Endpoint and hypotheses

- Primary: paired panel-level `FNTU@K` contrast; utility/cost definitions and `λ`: `[freeze using future_value_definition.md]`.
- Smallest effect of interest: `+0.10` normalized net utility per selected slot per future-task opportunity.
- Primary family-wise alpha: 0.05; Holm adjustment across four comparator contrasts.
- Independent unit: panel/family-seed cluster; not candidates/tasks.
- Primary supported/contradicted/inconclusive/unavailable rules: as in `ranking_metrics.md`; no post-outcome changes.
- Secondary metrics: `[list before confirmatory access; default list in ranking_metrics.md]`.

## Pre-outcome pressure and lock

- Compute R1–R5 complete orders and Top-K sets before accessing future outcomes.
- Each panel must satisfy IDT-vs-frequency/reuse/compression TopK-RDR ≥0.25, IDT-vs-random ≥0.125, mean all-pair TopK-RDR ≥0.30, and mean normalized Kendall divergence ≥0.15.
- Hash/store all input features, full orders, sets, pressure results, and analysis plan. Confirm the outcome store is sealed and access log empty.
- If any gate fails: `[freeze protocol action; do not inspect truth or silently remove/reseed panels]`.

## Data, missingness, and exclusions

- Calibration/development/confirmatory/replication task-family assignments: `[complete and hash]`.
- Candidate identity/duplicate rule: canonical representation hash before ranking.
- Missing threshold: primary unavailable if >5% paired future rows missing or policy differential missingness >2 percentage points; preserve missing vs zero vs failed.
- Pre-outcome exclusions and exact reason codes: `[complete]`.
- No exclusions or replacements based on the direction of results.

## Sample size and analysis

- Calibration-only power/precision code, assumptions, and simulation seeds: `[complete]`.
- Final number of independent panel clusters: `[freeze; no fewer than justified by simulation]`.
- Paired cluster estimator/interval method, bootstrap or randomization details, and multiplicity implementation: `[freeze]`.
- No candidate/task-level pseudo-replication; report all four paired contrasts and intervals.

## Outcome categories and stopping

- **Supported:** adjusted lower 95% bounds exceed SOI for all four comparisons.
- **Contradicted:** at least one adjusted upper 95% bound lies below SOI; state comparator-specific failure, not universal IDT failure.
- **Inconclusive:** valid data but uncertainty straddles SOI or mixed comparisons do not meet the other rules.
- **Unavailable:** invalid pressure/data/lock, endpoint not estimable, or missingness threshold exceeded.
- No interim efficacy peeking or outcome-driven stopping. Operational stopping rules: `[freeze]`.

## Signatures / lock record

- Protocol author/date: `[complete]`
- Independent reviewer/date: `[complete]`
- Data custodian confirms sealed outcome store: `[complete]`
- Rank lists/pressure lock timestamp and hashes: `[complete before outcome access]`
- Outcome access timestamp and authorized evaluator: `[post-lock only]`