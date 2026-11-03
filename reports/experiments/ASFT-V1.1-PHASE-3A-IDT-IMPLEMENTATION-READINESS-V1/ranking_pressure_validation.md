# Phase 3A — Ranking Pressure Validation

## Frozen Phase 1C pressure gate

Pressure is assessed before outcomes and excludes Oracle. For `N=40`, `K=8`, the Phase 1C gates are:

- R1-vs-R2 Frequency TopK-RDR ≥ 0.25
- R1-vs-R3 Reuse TopK-RDR ≥ 0.25
- R1-vs-R4 Compression TopK-RDR ≥ 0.25
- R1-vs-R5 Random TopK-RDR ≥ 0.125
- Mean TopK-RDR across all 10 R1–R5 pairs ≥ 0.30
- Mean normalized Kendall divergence across those pairs ≥ 0.15

Top-K overlap is reported as `1−TopK-RDR`. Normalized pairwise rank divergence is additionally reported as normalized Spearman footrule (mean absolute rank displacement / maximum possible); Phase 1C did not assign that supplemental diagnostic its own threshold, so it is not retroactively used as a gate.

## Phase 3A implementation re-run

The actual production R1 transfer-aware bridge plus R2–R5 engine was run on 100 deterministic panels from the Phase 1C designed synthetic feature recipe (`N=40`, `K=8`). All are development panels using one deliberately differentiated fixture recipe, not 100 independent empirical panels.

| Metric | Phase 3A synthetic result | Phase 1C original harness result |
|---|---:|---:|
| Panels passing frozen pressure gate | 100/100 | 100/100 |
| Mean all-pair TopK-RDR | 0.84325 | 0.8391 |
| Mean normalized Kendall divergence | 0.49084 | 0.4900 |
| Mean normalized pairwise rank divergence (supplemental) | 0.66220 | Not used as a gate |

The updated engine also tests the *failure behavior*: a deliberately converged five-policy ranking fails the frozen pressure gate. This check passed. R1 differs from frequency, reuse, compression, and random above the respective TopK-RDR floors on these constructed fixtures.

## Interpretation and gate status

These results verify that the benchmark engine can calculate pressure and that the gate detects convergence. They do **not** establish pressure on actual candidate pools: the 100 panels reuse the same deliberately separated type/feature recipe, and no real or independently generated candidate/task data were supplied. There is consequently no empirical pressure estimate, no actual candidate-disagreement matrix, and no basis to treat the synthetic 100/100 as a readiness pass for calibration.

**Verdict:** pressure mechanics and synthetic contract gate **PASS**; actual-pool pressure **NOT MEASURED**. Since insufficient/absent actual pressure is a blocking condition, Phase 3B calibration and Phase 3D confirmation remain blocked.