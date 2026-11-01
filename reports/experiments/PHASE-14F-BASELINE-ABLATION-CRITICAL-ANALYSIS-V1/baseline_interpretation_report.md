# Baseline Interpretation Report

## B1 — No learning

**Result: mixed.** In Phase 13C, SCT's net value (`.345`) exceeds NEVER_CREATE (`0`), and corrected Phase 13D ASFT exceeds B1 on the transfer-utility endpoint (`+.018909`). But Phase 13E ASFT task utility is `-.0361` versus B1 despite final C_t `+1.1785`; Phase 13F task utility is `-.036344` versus B1 despite CGR `+.287172`; Phase 13B ASFT ties the no-transfer control. “Learning helps” is endpoint- and task-stream-specific, not an overall result.

## B2 — Memory and retrieval

**Result: strong surviving counterexample, but phase-specific.** Phase 13C raw MEMORY_ONLY stores trace exemplars and scores net value `1.325`, far above SCT `.345`, with 418/440 correct applications vs 201/440 for SCT. This directly challenges SCT superiority in that protocol. Application frequency differs (440/440 vs 223/440), so the net-value contrast does not isolate retrieval quality per attempt from policy match rate. It is not the same method as later B2 skill stores. In corrected 13D ASFT beats B2_MEMORY_ONLY on transfer utility by `+.015273`; in 13E and 13F ASFT wins selected B2 contrasts on separate task utility/CGR gates. Thus memory does not explain every later result, but the 13C result cannot be dismissed or pooled away.

## B3 — Random skills/create

**Result: often favorable to ASFT, not a universal rejection of randomness.** Phase 13D has a large positive transfer-utility contrast over B3; 13E passes B3's paired C_t/task-utility criterion; 13B is above its random-pattern control. However, Phase 13C RANDOM_CREATE exactly matches SCT because its random-create probability is 1.0 and every eligible row is created; Phase 13F B3 ties ASFT on task utility and CGR. The policy definitions and pools differ, so “random” is not one pooled control.

## B4 — Compression proxy

**Result: mixed and incomplete test of compression.** Phase 13D fails the strict all-baseline claim on the slight negative ASFT-minus-B4 contrast `-.001091`, CI `[-.003273,0]`. Phase 13E and 13F pass their own B4 comparisons. B4 is a compression-only proxy, not canonical DreamCoder. The evidence says ASFT has not shown universal superiority to compression, not that compression universally wins.

## Cross-phase interpretation rule

Keep Phase 13B pre-correction `.1431299603` and corrected `.0958085317` separate; the informed arms tie and the strict gate fails under both. Keep Phase 13C raw MEMORY_ONLY distinct from Phase 13E B2 skill storage and Phase 13F B2_MEMORY_SKILL_STORE. Phase 13D's corrected transfer utility, Phase 13E's joint C_t/task utility, Phase 13F's joint task utility/CGR, and Phase 13G exact accuracy are different endpoints. Do not average them.
