# Phase 3A — Revalidation of the 26 Phase 1C Contracts

## Result

The Phase 1C contract suite was re-expressed and rerun against `experiments/phase3a/benchmark_engine.py`, which calls the production transfer-aware bridge for R1. **26/26 contracts passed.** The full row-level results and per-panel pre-outcome pressure records are in `experiments/phase3a/contract_results.json`; runner: `experiments/phase3a/run_contracts.py`.

| Contract | Revalidated behavior | Result |
|---|---|---|
| CT-1 | N=40 and hidden A–H synthetic fixture quotas, including B/C stress classes | PASS |
| CT-2 | Opaque IDs and exact card allowlist; hidden fields excluded | PASS |
| CT-3 | Unique IDs and independently seeded arrival permutation | PASS |
| CT-4 | R1–R5 use the same pool | PASS |
| CT-5 | Same-seed deterministic replay | PASS |
| CT-6 | Complete unique orders / K=8 selection support | PASS |
| CT-7 | Designed fixture disagrees with each comparator | PASS |
| CT-8 | R1/Frequency TopK-RDR threshold | PASS |
| CT-9 | R1/Reuse TopK-RDR threshold | PASS |
| CT-10 | R1/Compression TopK-RDR threshold | PASS |
| CT-11 | Outcome-blind pressure gate | PASS |
| CT-12 | Truth/labels/Oracle absent from operational ranker API | PASS |
| CT-13 | Oracle output after lock authorization | PASS |
| CT-14 | Pressure API accepts ranks and K only | PASS |
| CT-15 | Separate truth mutation does not alter rank output | PASS |
| CT-16 | Non-identical Top-1 selections in designed fixture | PASS |
| CT-17 | Independent arithmetic can report R1 loss vs Frequency | PASS |
| CT-18 | Equal outcome fixture returns a tie | PASS |
| CT-19 | Independent arithmetic can report R1 win | PASS |
| CT-20 | Hidden labels and truth separate from candidate cards | PASS |
| CT-21 | Seven public feature channels independently represented | PASS |
| CT-22 | Features bounded in [0,1] or explicitly unavailable | PASS |
| CT-23 | 100 designed synthetic panels meet frozen pressure gate | PASS (100/100) |
| CT-24 | Mean all-pair TopK-RDR exceeds Phase 1C threshold | PASS (0.84325) |
| CT-25 | Mean normalized Kendall exceeds Phase 1C threshold | PASS (0.49084) |
| CT-26 | Pressure panel log explicitly pre-outcome | PASS |

## Additional required readiness checks

Also passed: deterministic opaque-ID tie-breaking; arrival-order invariance; R5 changes with seed; convergence negative control fails the pressure gate; invalid rank permutations are rejected; Oracle is omitted from all 10 competitive pressure pairs. These supplements do not change the original 26 contract count.

## Evidence boundary

This 26/26 is **specification/plumbing evidence only**. CT-1, CT-7–11, and CT-23–26 use deliberately constructed synthetic features and outcomes; CT-17–19 use winner-conditioned arithmetic fixtures. The suite does not demonstrate natural candidate-pool pressure, independent FNTU@K task outcomes, transfer construct validity, or IDT efficacy. A passing contract suite does not override the blocked actual-data, endpoint, cost-freeze, and sealed-store gates.
