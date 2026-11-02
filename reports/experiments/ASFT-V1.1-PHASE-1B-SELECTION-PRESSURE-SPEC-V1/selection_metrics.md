# 1B.7 — Selection Metrics

## Primary endpoint (frozen)

**Mean selected-set Future Net Value per creation slot**, `Y_bs`, in TEU, as defined in `candidate_value_definition.md`:

`Y_bs = (sum of paired future task utility gains for the selector's selected portfolio − measured creation and maintenance costs converted by calibration-frozen lambda) / K`, with `K=8`.

The primary estimand for each simple comparator `j in {S2,S3,S4,S5,S6}` is the paired mean batch difference:

`Delta_j = mean_b [Y_b,S1 − Y_b,j]`.

Batches, not candidates/tasks, are independent units. All comparisons use the same batch, candidate pool, task IDs, and task order. S7 oracle is not in this primary family.

**Smallest effect of interest (SOI): +0.10 TEU per slot**, interpretable as one additional net exact-solve-equivalent per ten selected slots. The SOI is fixed before data collection and must not be altered after seeing results. Costs are reported beside gross utility so this exchange-rate-based endpoint remains auditable.

## Required primary interpretation

- **Supported:** pressure and validity gates pass; the familywise-adjusted one-sided 95% lower confidence bound for every `Delta_j` against S2–S6 exceeds +0.10 TEU/slot in confirmation, and replication has positive estimates against all simple selectors with no adjusted interval supporting a meaningful reversal. Claim is scoped to this balanced benchmark and cost model.
- **Contradicted:** pressure and validity gates pass, and at least one required simpler comparator has a multiplicity-adjusted 95% upper bound for `Delta_j` below −0.10 (SCV is meaningfully worse), or a preregistered equivalence test establishes SCV is not meaningfully higher than the strongest simple selector within ±0.10. Report comparator-specific results; no universal “SCV fails” claim beyond tested scope.
- **Inconclusive:** pressure/validity gates pass but intervals do not satisfy support or contradiction rules, or evidence is mixed without a decisive interval.
- **Unavailable:** pressure gate, cost/outcome instrumentation, split integrity, or required denominator fails. A pressure-unavailable run is not a null effect.

## Secondary outcomes

1. Gross selected-set future utility (before costs).
2. Creation and maintenance resource totals, and cost-adjusted net value components.
3. Future utility by task stratum: direct/source-family reuse, transfer, context/composition shift.
4. Selection precision among positive candidates; recall of positive and rare-high-impact candidates.
5. False-positive rate among negative (C+D) candidates; false-negative rate among positive (A+E) candidates.
6. Type-specific selection rates and mean FNV; deceptive-candidate selection and early-to-late value reversal.
7. Skill survival/availability at horizons 2, 6, and 10; maintenance cost and negative-transfer events.
8. Portfolio regret relative to S7 oracle; oracle gap is diagnostic only.
9. Per-selector task success, candidate count, rejection reason, failed application, no-match, and missingness.

## Diagnostic pressure measures

- Candidate and value-class distributions by batch (labels revealed only after choices lock).
- Selection rate per selector.
- Pairwise disagreement `D(a,b)=|S_a △ S_b|/20`; contested `SDR` across S1–S4; and all SCV-vs-comparator disagreements.
- Rank correlation and top-K overlap among S1–S3, secondary only.
- Score calibration/association with latent and realized value, secondary and not a replacement for selected-set outcome.

## Statistical plan

Use paired batch-level differences; summarize point estimates, SDs, two-sided 95% CIs, and one-sided simultaneous intervals for the primary family using Holm familywise α=.05. Use a cluster/bootstrap sensitivity analysis resampling whole batches, never individual candidate rows as independent observations. Report all per-batch differences and results for both confirmation and replication separately. Do not pool the two splits to manufacture precision. Secondary metrics are descriptive with intervals and no additional success claim unless separately preregistered.

## Missingness and denominator rules

No imputation. Preserve unavailable cells separately from zero. A complete batch is the unit: if a candidate lane fails after outcomes are opened, keep the partial record and mark the batch incomplete; do not score only favorable lanes. If more than 5% of confirmatory batches are incomplete, primary status is unavailable/inconclusive per preregistration. Any exact threshold and software-failure recovery rule is frozen before confirmation. Report all failures and reserve-seed use.