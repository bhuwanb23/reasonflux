# Phase 3A-R — Actual-Pool Pressure Report

**Gate 3 status: NOT COMPUTABLE — BLOCKED.** No eligible actual candidate registry exists for the target RQ1 benchmark.

## Audit finding

The Phase 2E audited ARC R1 path has zero accepted candidates under current support settings and zero accepted candidates in the relaxed S1–S4 audit conditions; Phase 2B reports zero C4 invariant candidates across 1,000 tasks in both budgeted and fullscan modes. Phase 1C's 40 cards are engineered synthetic fixtures and are disallowed for actual-pool pressure. Phase 2C candidate-trial rows are search attempts/programs, not candidate cards.

With no eligible R1–R5 candidate pool, there are no full rankings or Top-K sets for the real target benchmark. Accordingly, **no pressure values are reported**; this is not a zero-divergence estimate and not a pressure pass/fail result from observed rankings.

## Required metrics/status

| Metric | Required comparison | Result | Status |
|---|---|---:|---|
| TopK-RDR | R1 vs R2 Frequency | N/A | Not computable: candidate pool absent |
| TopK-RDR | R1 vs R3 Reuse | N/A | Not computable: candidate pool absent |
| TopK-RDR | R1 vs R4 Compression | N/A | Not computable: candidate pool absent |
| TopK-RDR | R1 vs R5 Random | N/A | Not computable: candidate pool absent |
| Normalized Kendall divergence | All 10 competitive pairs | N/A | Not computable: no rankings |
| Top-K overlap | R1 vs R2–R5 | N/A | Not computable: no Top-K sets |
| Pairwise rank-divergence matrix | R1–R5 | N/A | Not computable: no full orders |

The Phase 1C thresholds remain the prescribed gates: R1-vs-R2/R3/R4 TopK-RDR ≥0.25; R1-vs-R5 ≥0.125; mean competitive TopK-RDR ≥0.30; mean normalized Kendall divergence ≥0.15. These thresholds are not altered. The synthetic Phase 3A result (100/100 constructed fixture panels) is excluded from this report's actual-pool assessment.

## No post-pressure edits

No actual pool or actual pressure run exists, so a “freeze after pressure” check cannot pass. Once an eligible pool is supplied, hash the complete pre-outcome candidate snapshot and full orders before examining any outcomes. If a threshold fails, record blocked/non-informative; do not alter candidate membership, feature recipes, seed, K, or thresholds in response.