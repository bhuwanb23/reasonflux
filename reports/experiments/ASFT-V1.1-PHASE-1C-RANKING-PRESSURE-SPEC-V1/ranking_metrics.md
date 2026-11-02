# Phase 1C.7 — Ranking Metrics and Decision Rules

## Primary endpoint

`FNTU@K` is defined in [`future_value_definition.md`](future_value_definition.md). The primary estimand is the paired panel-level difference `Δ_j = FNTU@K(R1_IDT) − FNTU@K(Rj)` for each comparator `j ∈ {R2,R3,R4,R5}`. The same panel and held-out task opportunities are paired across policies. The independent unit is the predeclared task-family/generator-seed panel cluster, not individual candidates or task rows.

## Primary hypothesis family and smallest effect of interest

Set `SOI = +0.10 normalized net utility per selected slot per future-task opportunity` on the frozen utility scale. This is a design target that must be reviewed and calibrated before preregistration; it may not be changed after any confirmation outcomes are viewed. Family-wise type-I error is 0.05 across the four primary contrasts using Holm adjustment, with paired cluster-level intervals/test. Final sample size is **not set in Phase 1C**; it requires calibration-only power/precision simulation under the frozen generator and endpoint.

**Supported:** for every required comparator, the multiplicity-adjusted 95% lower confidence bound for Δ exceeds +SOI.  
**Contradicted (minimum meaningful superiority):** for at least one required comparator, the adjusted 95% upper confidence bound is below +SOI. Report which comparator; do not call that universal failure of IDT.  
**Inconclusive:** data are valid but intervals cross the SOI boundary or required comparator conclusions are mixed without meeting the contradicted rule.  
**Unavailable:** endpoint cannot be estimated under its frozen rules, pressure/data-integrity gate fails, or outcome lock is breached. Report unavailable reasons; do not convert to zero or null.

The all-comparator rule intentionally makes a broad superiority claim demanding. Comparator-specific estimates and intervals are always reported even when the overall decision is not supported.

## Ranking and pressure diagnostics

- **TopK-RDR:** `1 - |TopK_i ∩ TopK_j|/K`.
- **Normalized Kendall divergence:** discordant pair fraction over the full order.
- **Top-K overlap:** `|intersection|/K`; report as an interpretable companion.
- **Mean pairwise RDR:** across R1–R5, excluding Oracle.
- Report full divergence matrix before outcomes and keep its hash.

## Secondary outcome metrics

Report (not decision-driving unless separately preregistered): precision@K for candidates with positive standalone future net value; recall@K of all positive future-value candidates; transfer recall for positive cross-family candidates; NDCG@K using standalone future net value after the predeclared nonnegative mapping; gross task utility; net costs; compression utility; per-family values; candidate coverage; and rank stability across development/calibration perturbations. Never pick K or a secondary metric after seeing primary confirmation results.

## Analysis and multiplicity

Use paired contrasts per panel, cluster-aware inference at the independent panel/family level, fixed missingness rules, and Holm adjustment across four primary contrasts. No candidate-level pseudo-replication. Freeze estimator, interval method, randomization/bootstrap seed plan, family weights, and report-generation code before unlocking outcomes. A calibration-stage sample-size simulation can adjust N only before confirmation. Report all four contrasts, not only a favorable baseline.