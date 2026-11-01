# 14I-D — Statistical Validity

## Question

Are numerical estimates and comparisons supported at the correct independent unit and with appropriate precision?

| Threat | Examples | Consequence |
|---|---|---|
| Few independent seeds | 5 seeds in 13B; commonly 10 in later synthetic phases | Limits between-seed generalization; descriptive rows do not replace replication. |
| Sparse candidate populations | About 4.4 promoted IDT candidates per seed in 13B | Correlations can be unstable and sensitive to individual candidates. |
| Nested observations | 44 candidate rows/10 clusters in 13C; 114 13D records/10 seed clusters; 30 within-seed pairs in 13E | Rows/tasks are not independent seed replications; preserve cluster structure. |
| Near-zero variance / exact ties | 13B ranker ties; 13F exact-zero B3 contrasts | Standardized effects may be undefined; zero-width intervals do not imply universal certainty. |
| Multiple outcomes and comparisons | Many phases, metrics, correlations, ablations, robustness probes | Elevates false-positive/selection risk, especially for exploratory or posthoc results. Keep primary gates separate. |
| Non-comparable endpoints | Net value, task utility, transfer utility, CGR, C_t, IG, cost proxy | Pooling or using one as a substitute for another distorts conclusions. |
| Correction and reanalysis lineage | 13B accounting correction; corrected posthoc 13D analysis | Corrections are not independent replications; disclose which version/analysis supports each estimate. |
| Denominator ambiguity | ARC schema validity, full-DSL fit, arm accuracy, miner inputs, skill precision | Prevents valid comparisons if denominators are collapsed; null/unavailable is not zero. |

## Verdict

**Moderate-to-high risk, claim-dependent.** Paired comparisons, preregistered gates, explicit denominators, and cluster-aware summaries make the results informative. They do not remove the limitations of small seed clusters, sparse candidates, multiplicity, or phase-specific outcomes. Avoid exaggerated precision, especially where the number of clusters—not rows—is small.
