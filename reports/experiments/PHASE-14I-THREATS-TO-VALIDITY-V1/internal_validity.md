# 14I-A — Internal Validity

## Question

Are observed outcomes attributable to ASFT components, or could design, benchmark structure, controls, or phase differences explain them?

## Threats

### Shared generator–solver vocabulary — high

Synthetic generators, solver operations, trace vocabulary, and expected labels share an operation-level language. Phase 13B's recurring-signature result is real within that system, but the setup makes recovery of generator-aligned operation patterns easier to interpret than open-ended discovery. This threatens causal attribution to a general invariant mechanism, not the descriptive fact that the signatures were recovered.

### Benchmark alignment — high

The synthetic task set emphasizes operations represented in the system. Phase 13C creates only reflection and rotation skills. Positive results may reflect an aligned generator/candidate pool; there is no independent domain replication.

### Low decision pressure — critical for superiority claims

- In 13C, the primary cutoff accepts all 44/44 candidates; SCT, ALWAYS_CREATE, and RANDOM_CREATE make equivalent creation choices and tie at net value `0.345`.
- In corrected 13B, ASFT, frequency-only, and no-transfer have identical primary top-k=2 TU and semantic ranking across five seeds.

These are valid observed ties, but the candidate pools offer little or no rank/selection divergence. The studies therefore do not identify a robust advantage for the named selection/ranking policies.

### Retrieval as a competing pathway — high

13C MEMORY_ONLY reports net value 1.325 vs SCT 0.345, with 440/440 applications and 418 correct vs 223/440 and 201 correct. Unequal opportunities mean this comparison does not isolate per-attempt quality, yet it prevents uniquely attributing all reuse benefit to abstract skills.

### Cross-phase stitching and ablation interpretation — high

The six links are reconstructed across different phases, populations, arms, and endpoints, not one randomized mediation experiment. Some ablations change CGR without changing task utility; a zero contrast only describes the frozen intervention and pool. Do not concatenate separate positive results into an end-to-end causal claim.

### Data/protocol caveats — moderate to high

Phase 13B's output-cost correction changed absolute TU but not the tie/failed superiority gate. Corrected 13D posthoc analyses use saved outcomes and are not reruns. Phase 13G attempt 01 generated predictions in memory before failure; attempt 02 reused the same holdout.

## Verdict

**Moderate risk for bounded descriptive outcomes; high risk for causal and superiority claims.** The data support statements about what the frozen systems did. They do not resolve whether IDT/SCT caused the benefit uniquely, whether transfer causes capability growth, or whether a full chain operates across domains.
