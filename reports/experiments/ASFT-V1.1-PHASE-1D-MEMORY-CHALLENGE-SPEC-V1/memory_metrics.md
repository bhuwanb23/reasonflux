# Phase 1D.6 — Metrics and Decision Rules

## Primary endpoint

Use **Held-Out Net Utility per task opportunity** (`HNU`). For each arm and panel:

`HNU_BF = (1/5) × Σ_{f∈{B,C,D,E,F}} mean_{t∈f}[Q(a,t) − λ_c·Compute(a,t) − λ_r·Retrieval(a,t)] − λ_s·Storage(a)/60`, for 12 tasks in each of the five primary families.

`Q` is the frozen task-quality score on `[0,1]` (exact task success and any preregistered partial-credit rubric); resource terms use calibration-only conversions and amortize persistent storage over the fixed future horizon. Primary contrasts are paired `Δ = HNU(B2_M4) − HNU(B1a/b/c)` at the panel/family-seed cluster level. Equal family weighting prevents the most repeated family from dominating the pooled result.

Family A exact replay is a positive-control secondary stratum. It is reported separately and not folded into the primary B–F contrast. This avoids allowing the deliberately memory-friendly repeat family to mask abstraction behavior where exact retrieval is insufficient.

**SOI:** `+0.10` normalized utility per future task opportunity. The score conversion, partial credit, λ values, storage amortization, and SOI must be reviewed and frozen on development/calibration material before confirmation; no outcome-based changes.

## Primary hypotheses and outcomes

- **Abstraction superiority supported:** simultaneous/Holm-adjusted 95% lower bounds for B2−B1a, B2−B1b, and B2−B1c exceed +SOI on the B–F primary macro-average.
- **Abstraction superiority contradicted at the SOI:** at least one adjusted 95% upper bound is below +SOI; state which memory variant blocks the broad claim. Do not infer memory always wins.
- **Inconclusive:** valid data but intervals overlap the SOI boundary or comparator conclusions are mixed.
- **Unavailable:** budget/leakage/pressure/data integrity fails, endpoint missingness exceeds limits, or outcome access is compromised.
- **Hybrid benefit:** secondary simultaneous contrasts of B3 vs B2 and each B1 variant; state whether any benefit is confined to Family C.
- **Memory sufficiency:** Family A comparison M1 vs B2; report exact-replay success and net utility.
- **Transition point:** estimate the first predeclared exact-repeat probability `p` where M1's HNU reaches/exceeds B2; if no crossing on `{0,.25,.5,.75,1}`, report no crossover in tested range. Do not extrapolate.

Use familywise alpha 0.05 across the three primary memory comparators with Holm adjustment. The independent unit is the panel/family-seed cluster, not individual episodes or tasks. Exact sample size is pending a calibration-only power/precision simulation.

## Secondary metrics and diagnostics

Report task success and partial quality; transfer success by family; reuse success; memory precision/recall; abstraction precision/coverage; hybrid resolution rate; retrieval count and precision; skill-use count; no-match/abstention rate; adversarial lure error rate; storage bytes; construction/query operations; failure type; cost components; family-level effect estimates; and the p×s transition surface. These are descriptive unless separately preregistered.

## Missingness

Separate `NOT_APPLICABLE`, `FAILED`, `ABSTAINED`, and `MISSING`. Apply a frozen failure utility to actual failures; abstentions use a fixed policy score; not-applicable tasks receive the frozen neutral outcome. Do not map missing logs to zero. Mark primary HNU unavailable if >5% of paired rows are missing or arm-specific missingness differs by >2 percentage points; always report counts and reasons.