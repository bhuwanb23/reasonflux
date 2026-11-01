# Package G — Statistical Evidence and Interpretation

This package records estimates at their original analysis unit. The attached [`statistical_summary.csv`](statistical_summary.csv) includes a source path and uncertainty method for each row. [`baseline_metric_summary.csv`](baseline_metric_summary.csv) contains phase-specific 13E/13F arm means, SDs, and descriptive 95% t intervals for IS/SU/TS/CGR/IG computed from the saved per-seed `seed_summary.csv` only; these 13H calculations are descriptive, not new preregistered tests. `n` may mean independent seeds, candidate rows clustered within seeds, or task IDs; these units are not interchangeable.

## Metric-level synthesis

| Metric / evidence | Estimate | Unit and uncertainty | Interpretation |
|---|---|---|---|
| Phase 13B IS | Mean `5.856`, SD `0.238`, 95% CI `[5.648,6.064]` | 5 seeds | Synthetic-v1 only. |
| Phase 13B IS–TS | Reported `r=1.0` | About 4.4 promoted candidates/seed; small constructed population | Fragile association; cannot be treated as a robust confirmatory relation. |
| Phase 13C SCV10→shadow net value | Spearman `ρ=0.700`, CI `[0.545,0.931]` | 44 candidate rows in 10 seed clusters; cluster bootstrap | Association. Frequency `ρ=0.748` and p_reuse `ρ=0.884`; not proof of SCV policy value. |
| Phase 13C SCT net value | `0.345`, SD `0.063`, CI `[0.306,0.384]` | 10 seeds | Tied always/random creation and below memory-only. |
| Phase 13D IS–TS | Pearson `r=-0.0424`, CI `[-0.1318,~0]` | 114 rows / 10 seed clusters; seed-cluster bootstrap | No positive association. Do not treat 114 clustered observations as independent. |
| Phase 13D SU–TS | Pearson `r=-0.0129`, CI `[-0.0725,~0]` | 114 rows / 10 clusters; cluster bootstrap | No positive association. |
| Phase 13D TS–CGR | Pearson `r=0.4834`, CI `[0.4820,0.4842]` | 36 rows / 9 clusters; cluster bootstrap | Descriptive association; very narrow interval does not create independent-seed precision. Mean CGR was `-0.060` across nine seeds. |
| Phase 13D success-gated RCR | Mean approximately `0.1493`, CI approximately `[0.132,0.158]` | 10 seed summaries | Synthetic measured step-cost reduction; not wall-clock or external compute savings. |
| Phase 13E CGR | Mean `0.2946`, SD `0.0125`, CI `[0.2857,0.3036]` | 10 seeds | Positive frozen synthetic metric. |
| Phase 13E IG | Mean `0.2294`, SD `0.0069`, CI `[0.2245,0.2343]` | 10 seeds | Positive repository metric, not general intelligence. |
| Phase 13E IGR | Mean `0.00904`, CI approximately `[0.00903,0.00906]` | 10 seeds | Positive metric-pathway result. |
| Phase 13E IE slope | `-0.00394`, CI `[-0.00421,-0.00367]` | 10 seeds | Negative trend, contrary to a simple sustained-growth interpretation. |
| Phase 13E TS→CGR | `r=-0.503`, CI `[-0.860,0.186]` | 10 seeds | Not positive; very imprecise. |
| Phase 13E SU→CGR | `r=0.993`, CI `[0.969,0.998]` | 10 seeds | Descriptive within the constructed cohort, not causal. |
| Phase 13F paired task utility vs B1 | `-0.036344`, CI `[-0.036586,-0.036101]` | 10 paired seeds | ASFT is lower; joint criterion fails despite CGR delta. |
| Phase 13F paired task utility vs B2/B4 | `+0.074906`, CI `[0.074664,0.075149]` | 10 paired seeds | Positive in these specific comparisons. |
| Phase 13F ASFT vs B3 | `0.000`, SD `0` | 10 paired seeds | Tie; standardized effect undefined. |
| Phase 13G holdout exact accuracy | All arms `1/200=0.005` | 200 task IDs; task-paired bootstrap in source package | No separation; repeated holdout exposure and low DSL coverage limit inference. |

## Statistical cautions

1. Do not combine phase means, standard deviations, correlations, or confidence intervals. Synthetic-v1, SCT, transfer, growth, ablation, and ARC adapter runs differ in tasks, metric definitions, arms, and independent units.
2. Report the 95% interval method as stored. Seed-based t/normal intervals, seed-cluster bootstrap intervals, and task-level bootstrap intervals answer different questions.
3. Correlations over candidate rows may have many rows but few independent seed clusters. Use the cluster count as the basis for inference.
4. Several paired contrasts are deterministic or near-deterministic. Huge Cohen/Hedges standardized effects (e.g., Phase 13F) are artifacts of tiny paired SD; where SD is zero, effects are undefined. Prefer raw differences and task meaning.
5. Intervals were not globally multiplicity-adjusted across all secondary contrasts. Do not promote exploratory correlations to preregistered gates.
6. Phase 13C sensitivity results are retained as sensitivity, not replacement criteria: primary cutoff `0.000` selected 44/44 candidates for net value `0.345`; low-q25 cutoff `0.675` selected 28/44 for `0.418`; median/high-q75 `0.966667` selected 4/44 for `0.018`. Modeled maintenance-cost sensitivity changed net value from `0.945` at MC `0.00` to `0.645` at `0.03`, `0.345` at `0.06`, and `-0.255` at `0.12`.
7. Phase 13F raw paired utility contrasts are small-to-moderate in task terms but produce extreme standardized effects because paired SD is tiny: ASFT–B1 task utility Cohen dz `-107.164` / Hedges g `-97.978`; ASFT–B1 CGR dz `9667.091` / g `8838.483`. These values are unstable, not evidence of enormous practical effects. Exact values and all zero-variance undefined effects remain in source `analysis.json`.
8. Phase 13D corrected paired baseline/composition tables replace the defective frozen reporter fields for interpretation; the earlier files remain preserved for audit. Phase 13E/F corrections are saved-record posthoc only.
9. Phase 13G’s task interval does not remove the same-holdout rerun exposure. Seven contract tests demonstrate software contracts, not scientific performance.

Sources: experiment evidence packages, corrected Phase 13D JSON/analysis, and CSV data referenced row-by-row in `statistical_summary.csv` and `source_manifest.json`.
