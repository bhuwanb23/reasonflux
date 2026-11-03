# Phase 2H.2 — Candidate Yield Audit

## Result

Across the Phase 2E source/threshold audit (15 condition rows), **accepted invariant candidates = 0**. Current support floor 5 and strict floor 6 produce zero patterns/proposals. The relaxed support-2 diagnostic creates two candidate proposals in the historical, S2, S3, and S4 conditions; **all eight proposal rows are rejected** as `universal_noise`. Across those repeated conditions there are only two distinct canonical proposal IDs/signatures, not eight independent candidates. They are diagnostic repeats on overlapping/reused development material and are not pooled into a population.

| Source | Support setting | Discovery successes | Recurring patterns | Structures | Proposals before rejection | Accepted | Rejected |
|---|---:|---:|---:|---:|---:|---:|---:|
| Phase13G historical | Current 5 | 3 | 0 | 0 | 0 | **0** | 0 |
| Phase13G historical | Relaxed 2 | 3 | 4 | 2 | 2 | **0** | 2 (`universal_noise`) |
| Phase13G historical | Strict 6 | 3 | 0 | 0 | 0 | **0** | 0 |
| S1 / cap 3 | Relaxed 2 / Current 5 / Strict 6 | 1 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 | **0** | 0 |
| S2 / cap 6 | Relaxed 2 | 2 | 4 | 2 | 2 | **0** | 2 (`universal_noise`) |
| S2 / cap 6 | Current 5 / Strict 6 | 2 | 0 / 0 | 0 / 0 | 0 / 0 | **0** | 0 |
| S3 / cap 15 | Relaxed 2 | 3 | 4 | 2 | 2 | **0** | 2 (`universal_noise`) |
| S3 / cap 15 | Current 5 / Strict 6 | 3 | 0 / 0 | 0 / 0 | 0 / 0 | **0** | 0 |
| S4 / all ten | Relaxed 2 | 3 | 4 | 2 | 2 | **0** | 2 (`universal_noise`) |
| S4 / all ten | Current 5 / Strict 6 | 3 | 0 / 0 | 0 / 0 | 0 / 0 | **0** | 0 |

The exact 15-row counts (including signature support, discovery tasks, and repeated proposal IDs) are in `candidate_yield_audit.csv`; the machine summary is `yield_summary.json`.

## Yield and denominator interpretation

- Successful discovery traces are sparse: 3/600 in historical Phase 13G; 1/600, 2/600, 3/600, and 3/600 in S1–S4 discovery inputs. Phase 2D's broader task/condition trace counts must not be substituted for the discovery subset used by the invariant miner.
- At support floor 5, the maximum observed distinct-task support is 3. The threshold is therefore unreachable on the audited successful trace corpus; no accepted candidates result.
- At relaxed support 2, recurrent patterns are generic control-flow/verification operations; the candidate policy rejects the resulting structures. This is not evidence that a genuine semantic invariant was rejected.
- Candidate-to-validation survival is **not estimable** when no candidate enters validation. Do not report it as a measured 0% validation rate.
- Deduplicated eligible candidates: **0**. The relaxed proposals share two canonical IDs across repeated conditions, but none is accepted. No actual registry exists to measure natural deduplication or diversity.

## Decision

Current actual ARC R1 candidate yield is zero under the audited pipeline and policies. Relaxing support after observing this yield does not make an eligible benchmark pool; the saved relaxed analysis also rejects all proposals. Preserve thresholds/results, do not tune or relabel the proposals, and do not create synthetic candidate records to fill N=40.