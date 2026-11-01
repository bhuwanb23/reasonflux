# Package D — Baseline Consolidation

Comparators and endpoints differ by phase. The table preserves each phase's frozen metric rather than claiming a common scale. Positive differences favor ASFT only where the source defines the contrast as ASFT-minus-comparator.

| Phase | Comparator / endpoint | ASFT contrast or direct result | Frozen decision |
|---|---|---|---|
| 13B synthetic-v1 | Frequency-only, no-transfer; held-out TU, top-k=2 | ASFT `0.095809`; frequency-only `0.095809`; no-transfer `0.095809` | Strict per-seed all-control superiority **failed**. Random control was `0.063113`. |
| EXP-IDT-14 | Frequency/no-transfer/random; top-1 stress-test TU | ASFT `0.164866` (SD `0.0011`, CI `[0.1639,0.1658]`); frequency/no-transfer `0`; random `0.05956` | **Exploratory only**; not a retrospective Phase 13B pass. |
| 13C | Always-create/random-create/memory-only; primary net value | SCT `0.345 ± 0.063`; ties always/random; memory-only `1.325` | Strict SCT superiority **failed**. |
| 13D corrected | B1 no-learning; transfer-utility delta, n=10 seeds | `+0.018909`, SD `0.003450`, CI `[0.016727,0.020000]` | Passed this contrast. |
| 13D corrected | B2 memory-only; same endpoint | `+0.015273`, SD `0.003450`, CI `[0.013091,0.016364]` | Passed this contrast. |
| 13D corrected | B3 random-skills; same endpoint | `+0.728909`, SD `0.049113`, CI `[0.706364,0.761273]` | Passed this contrast; unusually large gap is comparator- and task-specific. |
| 13D corrected | B4 compression proxy; same endpoint | `-0.001091`, SD `0.003450`, CI `[-0.003273,0]`; 0/10 positive seeds | **Failed**; mandatory all-baseline gate therefore failed. B4 is not canonical DreamCoder. |
| 13E | B1 no-learning; all-task utility and final `C_t` | Utility `-0.036078` (lower CI `-0.036292`); final `C_t` delta `+1.1785` | Joint frozen comparison **failed/null** because task utility was adverse. |
| 13E | B2 skill-storage-only | Utility `+0.077344`; final `C_t` delta `+1.1785` | Passed the defined two-metric criterion. |
| 13E | B3 random-skill-creation | Utility `+0.077641`; final `C_t` delta `+0.1603` | Passed the defined two-metric criterion. |
| 13E | B4 compression proxy | Utility `+0.075172`; final `C_t` delta `+0.3455` | Passed the defined two-metric criterion; proxy caveat applies. |
| 13F | B1 no-learning; paired task utility/CGR | Utility `-0.036344` (CI `[-0.036586,-0.036101]`); CGR `+0.287172` (CI `[0.287151,0.287193]`) | Joint criterion **failed/null**. |
| 13F | B2 memory-skill store | Utility `+0.074906` (CI `[0.074664,0.075149]`); CGR `+0.287172` | Joint criterion passed. |
| 13F | B3 random skill creation | Utility `0`; CGR `0`; both SD 0 | Joint criterion **failed/null**; effects undefined at zero variance. |
| 13F | B4 compression proxy | Utility `+0.074906`; CGR `+0.081372` (CI `[0.081351,0.081393]`) | Joint criterion passed; proxy caveat applies. |
| 13G bounded ARC DSL | B1–B4, exact holdout task accuracy | Each of five arms `1/200 = 0.005`; paired deltas zero | No ASFT accuracy advantage; low-coverage/repeated-holdout limitations apply. |

## Overall interpretation

No phase-by-phase outcome should be added or averaged into a universal ASFT effect. On the explicit primary gates, Phase 13B, 13C, corrected 13D, and Phase 13F B1/B3 comparisons include failures; Phase 13E and Phase 13F pass only selected baselines; Phase 13G has no accuracy separation. The strongest defensible result is comparator-specific synthetic evidence, not general superiority.

Detailed tables: [`baseline_master_table.csv`](baseline_master_table.csv) for frozen primary contrasts and [`baseline_metric_summary.csv`](baseline_metric_summary.csv) for per-arm IS/SU/TS/CGR/IG summaries where recorded in saved seed-level outputs. Sources: [13B results](../../../docs/03_implementation/validation/phase_13b_results.md), [13C evidence](../PHASE-13C-SCT-V1/evidence_package.md), [13D corrected posthoc](../PHASE-13D-TRANSFER-V1/posthoc_analysis.md), [13E evidence](../PHASE-13E-CAP-GROWTH-V1/evidence_package.md), [13F evidence](../PHASE-13F-BASELINE-ABLATION-V1/evidence_package.md), [13G evidence](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/evidence_package.md).
