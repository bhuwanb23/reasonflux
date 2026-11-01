# Transfer cost reduction — interpretation and limits

| Phase/arm | Saved cost result | Correct interpretation |
|---|---:|---|
| 13C SCT, successful applications | Normalized reasoning reduction `0.227`; raw saving `1.000` step on applied rows | Correctness is separate; incorrect applications receive zero benefit. This is a synthetic step-cost proxy. |
| 13C MEMORY_ONLY, successful applications | Normalized reasoning reduction `0.213`; raw saving `1.000` step | A memory baseline also reduces the same simulator cost and applies more often in the 13C stream. |
| Corrected 13D ASFT | Success-gated normalized RCR `0.149288`, 95% seed interval `[0.131979,0.157943]`; positive in all 10 seed summaries | Recomputed from saved rows by posthoc audit; no task rerun. Still not real compute/time. |
| Phase 13D search-effort proxy | No usable `solver_search_candidates` reduction in saved summaries | Retrieval candidate counts do not establish solver search reduction. Do not claim search-compute savings. |

The validated claim is that reusing a skill can reduce the repository's reasoning-step measure in synthetic tasks. These phase-specific normalized scores are not a single pooled effect, and neither they nor raw step savings measure wall-clock time, FLOPs, or external economic value. The Phase 13D posthoc correction fixed reporting/coverage interpretation and preserved the frozen outcomes; it did not revise the cost metric after the fact.
