# Phase 2E.1 — Historical Phase 13G Invariant Audit

## Reconstructed path

Phase 13G processed 600 discovery tasks. Of 600 valid trace records, 597 were no-fit and the miner's success-only filter passed only **3 successful traces** to invariant discovery. Those traces contain 30 deduplicated fragments (ten per trace).

| Stage | Observed result | Interpretation |
|---|---:|---|
| Successful discovery traces | 3 | Maximum possible distinct-trace support is 3. |
| Fragments | 30 | Four-step operation traces, n-grams of lengths 1–4. |
| Exact operation n-gram signatures recurring in ≥2 traces, before threshold | 4 | Three common single operations plus the common two-operation prefix. |
| Maximum support | 3 | Each recurring signature appears in all three successful tasks (0.50% of all 600 discovery tasks). |
| Frozen Stage 4 minimum frequency / cross-trace support | 5 / 5 | No observed signature can meet either floor. |
| Raw patterns after frozen extraction | 0 | The first observed invariant-pipeline attrition. |
| Aggregated structures / candidate proposals / accepted candidates | 0 / 0 / 0 | Downstream stages had no input. |
| Saved final invariants | 0 | `invariants.csv` contains no invariant rows. |
| Validation / transfer-verified / skills | Not reached / 0 / 0 | No candidate existed to validate or transfer. |

The stored miner summary and independent rerun agree on the historical counts. The frozen Phase 13G runner sets both `MiningConfig.min_frequency` and `min_cross_trace` to 5; its candidate policy also sets `min_frequency=5`. Therefore the raw-pattern stage was **mathematically unable to pass any observed pattern** from this three-trace input. This locates the first failure at support filtering, not at aggregation, candidate mapping, or validation.

## Frozen support sensitivity on the same three traces

At support 2 (relaxed), the miner emits four raw operation patterns and two aggregated structures. The structures generate two candidate proposals, but both are rejected by the candidate-generation `universal_noise` rule; no production candidate reaches validation. At support 5 (current) and 6 (strict), raw patterns, structures, and candidate proposals remain zero.

The two relaxed structures are instrumentation/procedure fragments—`validate_grid_schema → enumerate_candidate_programs` and `verify_demonstrations`—not ARC transformation rules. The `universal_noise` decision uses task-family labels mapped from the solved program classes (reflection/rotation/recoloring); these are not independent semantic-family annotations. Its firing is an observed software decision, not proof that the patterns are truly universal noise.

A separate in-memory diagnostic that bypasses only candidate-generation rejection passes the two proposals to the validator. Both reach the validator's **structural F-C-G `VALIDATED` state**, but neither is transfer-verified or promotable; both have transfer and reasoning-value scores of zero. This reuses the same three traces and is not a production candidate path, independent validation, or evidence that meaningful invariants were discovered.

## Conclusion

Phase 13G did not show that invariant structures do not exist or that the miner is ineffective. It showed three successes feeding a support floor of five, which prevented the miner from emitting any raw pattern. When the support floor is relaxed, the miner operates, but the resulting repeated trace-control operations do not establish domain invariants and are stopped by another policy gate. No historical outcome is changed.