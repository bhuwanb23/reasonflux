# 1B.2 — Candidate Taxonomy

## Frozen taxonomy

Every candidate receives exactly one hidden challenge type, generated from its known latent future-value process. The selector-visible card never includes the type, label, task outcomes, or latent parameters.

| Type | Name | Operational definition | Value-sign stratum |
|---|---|---|---|
| A | Positive value | Ordinary candidate with latent expected full-horizon net value `theta >= +0.10` task-equivalent units. | Positive |
| B | Neutral value | Candidate with `-0.10 < theta < +0.10`. | Neutral |
| C | Negative value | Ordinary candidate with `theta <= -0.10`. | Negative |
| D | Deceptive value | Candidate has positive early value over opportunities 1–2 (`theta_2 >= +0.10`) but negative full-horizon value (`theta_10 <= -0.10`), due to late degradation, negative transfer, maintenance, or other prespecified mechanism. | Negative at the primary horizon |
| E | Rare high-impact | Opportunity probability is at most 0.10 per eligible task, while latent full-horizon expected net value is at least `+0.50`. | Positive |

A/C/D/E are not assigned using confirmatory realized outcomes. Type is set by the frozen data-generating mechanism's latent expected-value parameters; observed test outcomes are retained separately. D and E are distinct from ordinary A/C by definition, not merely post-hoc names for surprising results.

## Per-batch quotas

Each evaluation batch contains **20 technically valid candidates**, exactly four of each type A–E, before selector decisions. Therefore each batch contains 8 positive-value candidates (A+E), 4 neutral (B), and 8 negative-value candidates (C+D); deceptive and rare-high-impact challenges are each 20% of the pool. Candidate construction uses predeclared generator recipes and sealed latent labels. No candidate is selected into/out of a confirmatory batch by inspecting its realized held-out outcome.

If a batch fails the quota due to a generator or implementation error, it is pressure-invalid and unavailable; it is not repaired by replacing candidates after outcome access. A predeclared reserve-seed list may be used only when the batch is rejected before any outcome label is accessed, with the rejection reason logged.

## Candidate construction and information boundary

- All candidates pass the same minimal technical validity gate (executable schema, correct interface, no unsafe operation). The gate must not use future value, SCV, or task-outcome labels.
- For each candidate, the benchmark stores its type, latent expected value, true opportunity process, and task-level potential outcomes in the sealed outcome store.
- Every selector receives the same candidate IDs, shared pre-decision observation snapshot, and selector-visible feature card. Selectors use only their preregistered score input; they cannot access latent type, future tasks, outcomes, or the oracle record.
- Challenge types are included to test discrimination, not to assert that real-world candidate prevalence is 20% each. Results first generalize only to this balanced pressure benchmark.

## Horizon profile

Every candidate receives the same ten eligible future opportunities, with task slots fixed before confirmatory data generation:

1–2. immediate reuse / early-return opportunities;  
3–6. ordinary future reuse in the source family;  
7–8. near or cross-family transfer;  
9–10. context-shift or composition challenge.

Type D must show its early-positive/full-horizon-negative profile under this schedule. Type E's rare payoff appears only in a low-probability transfer/context slot. Candidate lanes use disjoint task IDs (or a predeclared non-overlap rule) so one selected skill cannot silently borrow another candidate's outcome. If interactions are later studied, they require a separately preregistered benchmark and do not replace this isolated selection test.

## Taxonomy validation

Before confirmation, a frozen generator contract test must establish: four candidates per type per batch; correct latent sign and horizon rule; no type/label fields in selector cards; no train/test task-ID overlap; and exact retention of any generation failures. Contract tests may use public calibration/development fixtures only. The confirmatory split remains unopened until its source, config, and selector hashes are locked.