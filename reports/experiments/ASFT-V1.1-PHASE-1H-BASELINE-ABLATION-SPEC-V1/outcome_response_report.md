# Phase 1H — Outcome-Response and Attribution Audit

The contracts use constructed intervals and choice vectors to exercise result states. They are not task outcomes, empirical rankings, or analysis of ASFT performance.

| Constructed case | Code status | Why it matters |
|---|---|---|
| ASFT meaningful positive contrast | `asft_wins` | ASFT can win when the interval exceeds the SOI. |
| Comparator meaningful positive contrast | `baseline_wins` | Memory/frequency/compression/random alternatives can win. |
| Equivalence interval | `equivalent_tie` | No practically meaningful difference can be reported. |
| Wide/overlapping interval | `inconclusive` | Uncertainty is not forced into a winner. |
| Missing endpoint | `unavailable` | Missing is not zero. |
| Verified ablation positive | `positive_contribution_under_tested_conditions` | Local component contribution is possible. |
| Verified ablation equivalence | `no_measurable_contribution_under_tested_conditions` | Removing a component without detectable change is representable. |
| Verified ablation negative | `negative_contribution_ablation_better_under_tested_conditions` | A component may harm the tested endpoint. |
| Same choices by all comparators | `non_informative_comparison` | A decision comparison cannot be reported as a mechanism win. |
| Unfair or mismatched comparison | `comparison_invalid` | Favorable numbers cannot repair pool/opportunity/budget mismatch. |

**Evidence boundary:** these are hand-constructed code-path tests, not historical or new empirical evidence. They demonstrate that the framework does not structurally favor ASFT and that an alternative or ablation can win.