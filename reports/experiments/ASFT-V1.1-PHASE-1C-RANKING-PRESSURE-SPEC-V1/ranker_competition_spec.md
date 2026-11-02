# Phase 1C.5 — Ranker Competition Specification

## Common inputs and restrictions

Every ranker receives the same N=40 candidate pool, same public card schema, same candidate order (or order-invariant implementation), same K=8, and same fixed evaluation budget. Cards contain only pre-outcome features computed from calibration/development material. Hidden type labels, future values, future task outcomes, and Oracle scores are prohibited from all five competitive rankers. All tie-breaks are deterministic and frozen. Feature values are normalized to `[0,1]`; exact source, denominators, and missing-data rules must be hashed before confirmation.

## Required policies

| ID | Ranker | Primary score/order | Permitted information |
|---|---|---|---|
| R1 | Transfer-aware IDT | Frozen v1.1 transfer-aware validation score using calibration-only transfer evidence; current operational form is `InvariantScore = F × C × G × T × R`, with transfer component supplied by the pinned transfer-aware implementation (`T = ITS × TU`, clipped as defined in code). | Same public card; `F,C,G,R` from allowed training evidence; `ITS/TU` from calibration transfer episodes only. No future outcomes. |
| R2 | Frequency-only | Descending normalized occurrence frequency `F`; tie by opaque candidate ID. | Frequency field only. |
| R3 | Reuse-only | Descending calibration success probability `successful reuses / eligible reuse attempts`; exact denominator and smoothing fixed before confirmation. | Reuse field only. |
| R4 | Compression-oriented | Descending calibration bits-saved ratio from frozen compressor/description-length procedure. | Compression feature only. |
| R5 | Random | One full permutation from a frozen seed derivation per panel; tie/replay behavior deterministic. | Candidate IDs and seed only. |
| R6 | Oracle | Descending actual future portfolio/candidate value, after outcome lock. | Held-out truth only; analysis ceiling. |

**Oracle isolation:** R6 is not registered among competitive methods; it is excluded from RDR gates, budgets, primary comparator family, and ranker tuning. It is computed only after all rank lists and pressure logs are hash-locked.

Production reference for the current R1 definition: [`transfer_aware.py`](../../../src/invariants/transfer_aware.py), [`ranking.py`](../../../src/invariants/ranking.py), and [`ValidationScores`](../../../src/invariants/validation/scores.py). Their exact code and dependencies must be hashed in the later run manifest; the Phase 1C synthetic harness is a simplified contract implementation, not an execution of the real production pipeline.

## Historical Phase 13B comparability note

The corrected saved Phase 13B comparator used calibration transfer utility in its ASFT order construction and reported a tie with frequency/no-transfer. The current production transfer-aware module exposes the explicit `T=ITS×TU` override within the `F×C×G×T×R` score. Phase 1C adopts one frozen v1.1 operational R1 for its new benchmark; it must not silently switch to the historical score or another transfer-aware formula after results. If exact historical rescore is desired, it must be registered as a distinct sensitivity analysis before outcomes, not substituted for R1.

## Tie handling and incomplete signals

Sort descending score, then deterministic opaque ID; no outcome-based tie break. For a score that is genuinely zero with observed opportunities, retain zero. For unavailable calibration measurement (e.g. no eligible attempts), retain NA and its reason; do not relabel it as zero. The generator's calibration opportunity design must supply comparable eligible measurements for all candidates before final ranking. If it cannot, mark that ranker/panel unavailable under the preregistered rule rather than post-hoc imputing.

## Fair comparison

Top-K selection is the intervention. Every method gets exactly K slots and is scored against the same full future task suite, costs, and horizon. The test compares complete sets; it does not compare raw score scales across rankers. All policy outputs and feature snapshots are retained to enable deterministic replay.