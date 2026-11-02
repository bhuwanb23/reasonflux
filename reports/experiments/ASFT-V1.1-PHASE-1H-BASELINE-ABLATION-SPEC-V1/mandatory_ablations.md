# Phase 1H.5 — Mandatory Ablation Framework

Every major mechanism claim requires its mapped removal test from `ablation_taxonomy.md` before an affirmative claim is made. The nine registered ablations A1–A9 cover IDT, SCT, SCV, transfer, capability, lifecycle, composition, memory, and ARC extension.

## Conditions for interpretable removal

1. **Manipulation check:** verify the component is actually disabled and descendants/metrics affected are logged.
2. **Isolation:** hold tasks, candidate pool, resource caps, horizon, evaluator, and other components constant where technically possible. If removal necessarily changes eligibility, report both a common-support comparison and a natural-system comparison; do not conflate them.
3. **Equal budgets:** do not reallocate saved compute/storage/opportunities to the remaining components unless the reallocation estimand is separately preregistered.
4. **Exposure and opportunity accounting:** report component activation, choices, candidates, attempts, eligible opportunities, and downstream denominators. A dormant component is not tested merely because a flag was changed.
5. **Outcome separation:** report primary external behavior endpoint separately from internal scores. A5_NO_CAPABILITY can make CGR unavailable by design; this is not a task-performance loss.
6. **No rescue:** no post-result alternative ablation or outcome may replace a failed preregistered test.

## Allowed ablation conclusions

- **Positive contribution under tested conditions:** full system outperforms ablation beyond SOI with verified removal and fair/active comparison.
- **No measurable contribution under tested conditions:** powered equivalence interval lies within SOI and the component was actually exercised/removed.
- **Negative contribution under tested conditions:** the ablated system beats the full system beyond SOI.
- **Inconclusive:** uncertainty spans the decision boundaries.
- **Unavailable/non-informative:** manipulation failed, component never activated, there is no eligible denominator, fairness failed, or endpoint is absent.

These are local findings. A positive ablation effect does not prove universal necessity; a tie does not prove the component is useless in other pools; an unavailable ablation is not a null.