# Phase 2E.5 — Support Threshold Audit

## Frozen sensitivity conditions

- **Current S1:** 5 distinct successful traces, matching Phase 13G `MIN_SUPPORT=5`.
- **Relaxed S2:** 2 distinct traces, the minimum that can establish recurrence across separate task IDs.
- **Strict S3:** 6 distinct traces, a minimal stricter stress condition.

The same floor was applied to `MiningConfig.min_frequency`, `min_cross_trace`, and `InvariantPolicy.min_frequency`; all other policy settings remained fixed. The support floor is therefore tested at both pattern extraction and candidate rejection without silently relaxing consistency, family, or other filters.

## Results

| Source | Max observed support | Current 5: patterns | Relaxed 2: patterns / proposals / accepted | Strict 6: patterns |
|---|---:|---:|---:|---:|
| Phase 13G historical | 3 | 0 | 4 / 2 / 0 | 0 |
| S1 | 1 | 0 | 0 / 0 / 0 | 0 |
| S2 | 2 | 0 | 4 / 2 / 0 | 0 |
| S3 | 3 | 0 | 4 / 2 / 0 | 0 |
| S4 | 3 | 0 | 4 / 2 / 0 | 0 |

The current support threshold **necessarily eliminates every observed repeated signature** in the available successful-trace pool: max support is 1–3, below 5. Relaxing to 2 reveals repeated patterns and structures in S2–S4 and Phase 13G, but the candidate policy rejects the resulting two proposals per source as `universal_noise`. The strict threshold also yields none, as expected. No support setting yields an accepted production candidate.

## Judgment

Threshold 5 is **too high for this observed trace supply**, in the operational sense that it makes the pattern stage unreachable. This audit cannot decide whether 5 is globally unreasonable: the input corpus is much smaller than the threshold and contains only 1–3 successful discovery traces. Nor does the relaxed threshold establish that support 2 is sufficient for true ARC invariants. It reveals instrumentation recurrence, not domain-rule recurrence. Threshold choice requires a future adequately populated, semantically grounded trace corpus and preregistered error/utility criteria; do not tune it to this outcome.