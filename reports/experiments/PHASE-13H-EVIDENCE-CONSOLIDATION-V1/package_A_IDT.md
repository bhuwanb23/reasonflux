# Package A — Invariant Discovery and Transfer (IDT)

**Question:** Do traces produce useful invariants, does IS predict transfer, and does transfer-aware ranking beat frequency-only/no-transfer?  
**Scope:** Controlled synthetic environments in 13B–13D; bounded ARC adapter in 13G.

## Evidence ledger

| Evidence | Result | Interpretation |
|---|---|---|
| Phase 13B synthetic-v1 discovery | Reflection/rotation/counting/grouping discovery rates each `1.000`; IP/IR each `1.000`; mean IS `5.856` (SD `0.238`, 95% CI `[5.648,6.064]`); mean TS `0.0176` (`0.0009`, `[0.0169,0.0184]`); TU `0.0657` (`0.0032`, `[0.0629,0.0685]`); VST `1.000`; noise/top-rank stability `0.720` (`0.110`, `[0.624,0.816]`). Semantic ranking was the same in all five seeds: reflection, rotation, counting, grouping. IS–TS correlations were perfect, but population was only about 4.4 promoted candidates/seed. | Positive behavior in the designed generator; fragile predictive evidence, not external validation. |
| Phase 13B primary rank gate | ASFT top-k=2 held-out TU `0.095809`; frequency-only and no-transfer each `0.095809`; random control `0.063113`. Strict per-seed superiority against all required controls failed. | A tie cannot establish incremental ranker value. Preserve the failed gate. |
| EXP-IDT-14 top-1 | ASFT `0.164866` (reported SD `0.0011`, 95% CI `[0.1639,0.1658]`); frequency and no-transfer `0`; random `0.05956`. | Exploratory stress test intentionally injected a frequent no-op marker. Shows rejection of that constructed confound only. It does not repair Phase 13B. |
| Phase 13D corrected association | IS–TS Pearson `r=-0.0424`, 95% seed-cluster bootstrap CI `[-0.1318, ~0]`, 114 observations/10 seed clusters. SU–TS `r=-0.0129`, CI `[-0.0725, ~0]`. | Corrected posthoc evidence does not support positive predictive association. Candidate rows are clustered; n=114 is not 114 independent seeds. |
| Phase 13G ARC adapter | Three exact-fit discovery examples; five recurrence support required; zero invariant candidates. | Predictive association unavailable; low DSL coverage prevents a broad theory test. |

## Consolidated judgment

- **Invariant recurrence in synthetic generator:** supported narrowly.
- **IS as a general predictor of future transfer:** not established; 13B's perfect correlation is small-sample and contradicted by corrected 13D near-zero/non-positive association.
- **Transfer-aware ranking superiority:** original frozen Phase 13B gate failed. EXP-IDT-14 remains exploratory and is not a retrospective pass.
- **ARC invariant discovery:** not demonstrated; 13G has zero candidates after only three exact-fit discovery traces.

## Defensible claim

> “The system detects recurring operation signatures in the controlled synthetic task generator. Current evidence does not show that invariant strength generally predicts transfer or that transfer-aware ranking beats frequency-only/no-transfer on the original benchmark.”

## Required disclosures

Keep EXP-IDT-14 top-k=1 primary and top-k=2 secondary; enforce strict per-seed success; disclose excluded prototypes; preserve the original synthetic-v1 results and failed `baseline_comparison`. Do not pad top-10 lists with duplicate signatures or retune thresholds. See [master evidence](master_evidence_package.md), [Phase 13B results](../../../docs/03_implementation/validation/phase_13b_results.md), [EXP-IDT-14 report](../EXP-IDT-14/report.md), and [corrected Phase 13D posthoc](../PHASE-13D-TRANSFER-V1/posthoc_analysis.md).
