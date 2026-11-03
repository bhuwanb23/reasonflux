# Phase 3A — Ranker Validation Report

## Scope and result

Implemented a Phase 3A development engine at `experiments/phase3a/benchmark_engine.py`. It executes R1–R5 over one allowlisted candidate-card pool, validates full orders, and keeps R6 in a separate post-lock path. This is executable contract plumbing, not evidence from real candidate/task data. Ranker contract checks and synthetic pressure revalidation passed; production feature construction and provenance remain incomplete.

## R1–R6 audit

| Ranker | Implementation and validation | Actual-data status |
|---|---|---|
| R1 — transfer-aware IDT | Uses the repository production `invariants.transfer_aware.rank_transfer_aware` bridge and `invariants.ranking` score, with `T=ITS×TU` from calibration `TransferMemory`; validates the card's `transfer_calibration` against the computed memory value. `F` is mapped from the normalized card into the production count normalizer with negligible quantization. Production score is `F×C×G×T×R`; ties sort by opaque ID. | **Partial:** production algorithm executes in synthetic tests. No real calibration-only memory, candidate cards, pinned config/dependency hash, or feature-source manifest is available. |
| R2 — frequency | Descending normalized `frequency`; tie by opaque ID. No other feature is read for its score. | Formula plumbing passes; real frequency denominator and source are not pinned. |
| R3 — reuse probability | Descending `reuse_probability`, constructed as `successful_reuses / eligible_reuse_attempts`, with no smoothing. A zero denominator is unavailable, never imputed to zero. Tie by opaque ID. | Formula plumbing passes; eligible-opportunity definition, actual counts, and calibration data are absent. Unsmoothed estimate is the Phase 3A implementation choice and must be frozen/approved before calibration. |
| R4 — compression | Descending supplied `compression_gain`; helper computes `(bits_before−bits_after)/bits_before`. Tie by opaque ID. | Formula plumbing passes only. The codec/description-length algorithm, corpus, and version are not pinned; no actual measurement exists. |
| R5 — random | Full permutation sorted by SHA-256 priorities keyed by the panel-derived seed and candidate ID. Independent of arrival order; same seed/panel replays exactly. | Seed derivation is executable and deterministic, but the confirmatory master-seed plan remains unfrozen. |
| R6 — Oracle | Excluded from the competitive policy registry and pressure metrics. Separate API accepts `OracleAccess` only after the exact ranks and pressure log match a pre-outcome lock. | Interface test passes. The in-process vault is explicitly a protocol mock, not a secure/sealed production outcome store. |

## Determinism and exclusions

- Complete deterministic tie-breaking is descending score then opaque candidate ID for score rankers; random priorities are deterministic per panel/seed.
- Replay with unchanged panel and seed is identical; changing the random seed changes R5; reversing arrival order does not change rank output.
- The candidate-card schema is exactly `candidate_id`, `frequency`, `consistency`, `generality`, `transfer_calibration`, `reasoning_value`, `reuse_probability`, and `compression_gain`. No latent class, task family, future value, outcome, or Oracle field is represented.
- R1's transfer input is computed only from the `TransferMemory` supplied to the ranker. The engine rejects a mismatch between computed calibration T and the card's T.
- Missing R1/R3/R4 features fail closed as unavailable; no post-hoc imputation is allowed.

## Execution evidence

The Phase 3A runner executed the production bridge/ranker using synthetic calibration records constructed solely to exercise the API. The card-to-memory agreement and product ordering therefore validate implementation wiring, not the truth or calibration quality of T. R2–R5 similarly ran on the Phase 1C designed feature recipe; these tests cannot demonstrate natural rank disagreement.

**Verdict:** ranker plumbing/determinism **PASS on development fixtures**; actual feature-provenance validation **BLOCKED**; no IDT efficacy conclusion.