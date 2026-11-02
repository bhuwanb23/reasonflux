# 1B.5 — Selector Competition Specification

## Common decision interface

Input: the same 20 candidate IDs and selector-visible feature cards for a batch. Output: a set of candidate IDs, at most eight; for S1–S5 exactly eight under the pressure-qualified panel. Candidate card fields, units, missingness, sort direction, and tie breaks are frozen. Labels, latent expected value, held-out tasks, task outcomes, and FNV are forbidden inputs. Every choice is logged with raw score, score source, rank, tie break, and selected/rejected reason.

All selectors have equal slot capacity (K=8), identical candidate pool and observation snapshot, common decision compute/time budget, identical task horizon and resource accounting. Shared precomputed feature extraction is available to all; each policy may use only its specified decision signal. Oracle is excluded from production fairness claims.

## Required selectors

| ID | Selector | Frozen decision rule |
|---|---|---|
| S1 | SCV | Compute legacy `SCV10` exactly as in `candidate_value_definition.md`; select the eight highest-SCV candidates with `SCV10>0`. If fewer than eight are positive, the panel fails the pre-outcome pressure gate; do not lower threshold or fill slots with negative scores. Ties: candidate-ID hash, fixed salt. |
| S2 | Frequency | Select top eight by observed eligible recurrence count in discovery data only. No transfer, abstraction, or outcome score. Ties: candidate-ID hash. |
| S3 | Reuse probability | Select top eight by the frozen `p_reuse` field used by SCV. Do not multiply by AG/TS or subtract cost. Ties: candidate-ID hash. |
| S4 | Random | Uniformly sample eight without replacement from the full common eligible pool using an independent, recorded RNG stream keyed to split and batch ID. No calibration-derived create probability and no outcome-informed redraw. |
| S5 | Always Create (capacity-limited) | Select the first eight candidates in the frozen value-independent arrival order. This preserves the always-create idea under the shared K=8 budget. |
| S6 | Never Create | Select none. Intentional zero-rate negative-control anchor; excluded from the contested-selector SDR and exempt from the active-policy nonzero-rate rule. |
| S7 | Oracle | Select the eight highest latent expected FNV candidates using sealed generator truth, solely to estimate the benchmark ceiling/regret. Not a production baseline, not accessible to selectors, and never included in the primary superiority family. |

S1's positive-score requirement is deliberate: if fewer than K SCV-positive candidates exist, there is no balanced budget-matched superiority test for that panel. The correct status is unavailable; do not silently change the score or compare a smaller SCV set with an eight-candidate comparator as if budgets were equal.

## Frozen invariants

- No selector may re-score or update choices after outcomes begin.
- Candidate pools are identical; no baseline receives fewer candidates or opportunities.
- Selector IDs and algorithm versions are separate from Phase 13C/13F labels where implementation changed.
- S4's random seed and draw are saved before outcomes; every seed produces exactly K choices.
- S5 ordering is independent of labels and feature score; S6 remains empty.
- S7 uses known expected value, not realized test outcomes, so it is an oracle ceiling rather than an impossibly optimistic hindsight comparator.

## Pressure contract tests required before Phase 4

1. Exact K/rate and unique candidate IDs for S1–S5; S6=0; S7=K.
2. SCV formula and feature mappings agree with the frozen Phase 13C equation.
3. Each selector receives the same candidate manifest; forbidden fields are absent from selector payloads.
4. Seeded S4 is reproducible and uniform over K-subsets in unit tests; no degenerate probability.
5. Tie breaks never read outcome/type fields.
6. The golden fixture produces the declared distinct sets/SDR.
7. Generator meets per-type quotas without examining realized held-out outcomes.
8. Confirmatory panel pressure checker runs and locks decisions before outcome store unlock.