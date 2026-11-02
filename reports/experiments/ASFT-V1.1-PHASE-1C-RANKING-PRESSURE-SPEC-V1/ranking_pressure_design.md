# Phase 1C.4 — Ranking-Pressure Design

## Fixed panel and budget

Each synthetic contract panel has `N=40`, `K=8` (20% selection), and identical candidate cards for every ranker. Rankers submit a full deterministic ordering and a Top-K set. One slot and one storage unit are allocated per selected candidate; no ranker may spend extra evaluation or task budget. Future outcome access occurs only after the panel's ranks and pre-outcome gate are locked.

## Divergence metrics

For equal-sized Top-K sets `A` and `B`:

`TopK-RDR(A,B) = 1 − |A ∩ B| / K`.

Thus 0 means identical selected sets; 0.25 means two of eight slots differ. For complete orderings, normalized Kendall divergence is the fraction of all candidate pairs ordered oppositely. Report both: a different lower rank alone does not create decision pressure if Top-K is unchanged.

## Frozen pre-outcome gates

On every panel intended for confirmation, before truth is unlocked:

1. IDT-vs-Frequency, IDT-vs-Reuse, and IDT-vs-Compression TopK-RDR each ≥0.25.
2. IDT-vs-Random TopK-RDR ≥0.125.
3. Mean TopK-RDR across the ten pairs among R1–R5 ≥0.30.
4. Mean normalized Kendall divergence across the same pairs ≥0.15.

The gate consumes only candidate cards and rankings. It accepts no latent types, outcome values, or Oracle list. Log all candidate IDs, all five full orders, all Top-K sets, code/config hashes, and gate decisions before outcome access. A failed confirmatory panel is not dropped/reseeded by outcome direction; the full study remains blocked/unavailable unless the pre-registered protocol specifies a valid replacement before data collection.

## Generator and interpretation

The controlled generator assigns the eight hidden strata before outcomes and includes the B/C quotas. Feature signals are deliberately non-identical: the ranking methods must face both obvious and adversarial cues. This makes mechanical pressure testable, but does not establish that pressure is natural or that IDT's signal is useful. A separate natural-data replication must report its candidate composition and must not curate by future labels.

## Contract fixture results

The synthetic harness passed 100/100 seeded pressure panels. Across the fixed feature/type recipe, mean all-pair TopK-RDR was **0.8391** (minimum **0.7875**), mean normalized Kendall divergence was **0.4900** (minimum **0.4538**). Mean IDT-vs-Frequency/Reuse/Compression/Random RDR was **0.9463 / 0.7600 / 0.5550 / 0.8038**. These are deliberately constructed contract-fixture diagnostics, not benchmark evidence or effect estimates.

See [`synthetic_pressure_report.md`](synthetic_pressure_report.md), [`synthetic_pressure_validation.json`](synthetic_pressure_validation.json), and [`phase1C_contract_test_results.csv`](phase1C_contract_test_results.csv).