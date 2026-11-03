# Phase 3A-R — Feature Lineage Freeze Audit

**Gate 2 status: BLOCKED.** Production source functions can be identified and hashed, but actual candidate inputs/derivations are absent, and the Phase 3A-R draft feature names conflict with the frozen Phase 1C R1 definition.

## Critical semantic conflict

Phase 1C freezes operational R1 as `InvariantScore = F × C × G × T × R`:

- `F`: normalized occurrence frequency;
- `C`: consistency;
- `G`: generality;
- `T`: calibration transfer score `ITS × TU` from the production transfer-aware bridge;
- `R`: reasoning value.

The supplied Phase 3A-R remediation outline labels the same symbols as `F=Frequency, C=Coverage, G=Growth, T=Transfer, R=Reuse`. Those are not equivalent substitutions:

- Coverage is a component within transfer utility in the existing `T` pipeline, not the production consistency field `C`.
- Growth/CGR is a downstream capability-growth outcome/diagnostic, not the production generality field `G`.
- Reuse probability is the separately specified R3 comparator feature, while the Phase 1C R1 `R` is reasoning value.

Changing C/G/R to coverage/growth/reuse silently would change R1 and overlap comparator information; it would no longer be a faithful Phase 1C revalidation. The discrepancy requires an explicit owner decision: retain Phase 1C semantics, or issue a versioned protocol amendment with new equations, comparators, contracts, thresholds, and historical-comparability rules. No interpretation is chosen here.

## Existing source map

`feature_source_hashes.csv` records SHA-256 hashes for the current production F/C/G/T/R functions and the Phase 3A adapter. Source code availability is not feature-lineage freeze: there are no actual candidate records, calibration event logs, frozen configuration values, or per-candidate feature snapshots to reproduce.

| Feature | Production source / status | Missing for a freeze |
|---|---|---|
| F | `score_frequency` and `normalize_count`; code hash recorded | Candidate occurrence denominator, training snapshot, `freq_norm` configuration/run hash |
| C | `score_consistency`; code hash recorded | Actual stability observations and missingness/source rule; name collision with draft “Coverage” |
| G | `score_generality`; code hash recorded | Actual variation/generalization observations; name collision with draft “Growth” |
| T | `transfer_aware.py` and `compute_transfer_score`; code hashes recorded | Calibration-only `TransferMemory`, eligible opportunity and family denominators, config, source/task hashes |
| R | `score_reasoning_value`; code hash recorded | Actual reasoning-value source/measurement; draft incorrectly calls it “Reuse” |
| R3 Reuse | Phase 3A helper uses successful reuse / eligible reuse attempts, unsmoothed | Frozen eligibility/opportunity definition and actual event logs; zero denominator is unavailable |
| R4 Compression | Phase 3A helper implements bits-saved ratio only | Codec, description-length method, corpus, normalization, and feature snapshots |

## Freeze decision

The source-code hashes are audit anchors, not frozen values or reproducible feature datasets. Feature lineage, missingness, denominators, and per-card values cannot be signed until the project resolves the semantic conflict and supplies calibration-only candidate evidence. **Do not run pressure or tune thresholds using an improvised C/G/R mapping.**