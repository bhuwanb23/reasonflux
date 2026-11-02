# Phase 1D.1 — Memory Audit

**Phase:** `ASFT-V1.1-PHASE-1D`  
**Sources:** saved Phase 13C records/code and Phase 14C, 14F, 14H interpretations. No experiment was rerun.

## Executive finding

Phase 13C's `MEMORY_ONLY` result is a serious, comparator-specific challenge to SCT: mean net value **1.325** versus **0.345** for SCT; paired SCT-minus-memory **−0.980** (seed-bootstrap 95% CI **[−1.020, −0.940]**). On the same reported 440 eligible opportunities, the memory arm applied all 440 and was correct on 418; SCT applied 223, was correct on 201, failed on 22, and had 217 no-matches. Correct/eligible was 0.950 for memory and 0.457 for SCT.

**Critical code-level qualification:** Phase 14C describes this as “exact retrieval,” but the saved Phase 13C implementation does not replay a full exact task solution. `_evaluate_memory_only` chooses the first source trace matching the invariant pattern, extracts one macro operation (e.g. an `apply_*`, `count_objects`, or `group_by_color` op), then applies that macro to the eligible task opportunities. Operationally this is a **raw-trace-exemplar / partial-macro memory baseline**, not the M1 exact-episodic system defined for Phase 1D. Phase 1D must preserve this historical distinction rather than relabel it as full-answer replay.

## What likely contributed, and what cannot be decomposed

| Possible contributor | Evidence | Honest interpretation |
|---|---|---|
| Coverage/application rate | Memory applied 440/440 opportunities; SCT applied 223/440 and had 217 no-matches. | The largest directly observed gap is that the memory macro was applied much more often. This is not an opportunity-denominator imbalance—the reported eligible denominator is 440 in both arms—but it is an application-coverage difference. |
| Conditional correctness | Memory was correct on 418/440; SCT on 201/440. Memory's correct/eligible was 0.950 vs 0.457. | Supports much more reliable behavior on this task stream. It does not isolate exact retrieval from broad macro applicability. |
| Task repetition / generator alignment | Phase 13C is a controlled repetitive synthetic stream; memory uses a source-trace-derived macro and the same simulator's task operations. | A plausible source of advantage. No independent task-family test establishes generality. |
| Cost accounting | Net value uses normalized simulator creation/maintenance costs; it is not measured wall-clock/FLOPs or a byte-matched storage audit. | The 1.325 vs 0.345 result is for the frozen modeled metric, not an empirical resource-efficiency comparison. |
| Retrieval quality vs abstraction | Memory selects the first source trace matching a pattern and extracts a simple macro; SCT uses skill matches, with many no-matches. | The comparison changes representation and coverage at once. No factorial ablation isolates retrieval, abstraction, or match policy. |
| Storage / compute budget | The record retains modeled costs and exemplar/skill counts, but not a full matched byte/compute/retrieval-cost ledger under one common cap. | Budget equivalence under realistic storage and runtime is not established. Phase 1D makes these explicit. |

The exact denominators and confidence intervals are retained in [`memory_interpretation.md`](../PHASE-14C-SCT-CRITICAL-ANALYSIS-V1/memory_interpretation.md), [`phase14c_sct_analysis.md`](../PHASE-14C-SCT-CRITICAL-ANALYSIS-V1/phase14c_sct_analysis.md), and the original [`Phase 13C summary`](../PHASE-13C-SCT-V1/summary.md). The implementation behavior is visible in the saved [`Phase 13C source snapshot`](../PHASE-13C-SCT-V1/source_snapshot/phase13c_sct_frozen/part_02.txt).

## Phase 13F is a different comparator

Phase 13F `B2_MEMORY_SKILL_STORE` is not a replication of the Phase 13C `MEMORY_ONLY` arm. It is a different memory/skill-store policy in a different ten-seed, multi-arm protocol. Phase 14C reports B2 task utility **0.715** and CGR **0**, versus ASFT task utility **0.789906** and CGR **0.287172**; the frozen joint criterion favors ASFT there. Do not pool these endpoints or use the later result to erase Phase 13C's memory advantage.

Phase 14H accordingly treats memory/retrieval as a live, incompletely controlled alternative, not a universal explanation. Current evidence supports neither “abstraction always wins” nor “memory always wins.”

## Audit conclusion

> Phase 13C demonstrates that a raw-trace-exemplar macro memory policy outperformed SCT on that frozen synthetic stream and net-value model. Its higher application coverage and correctness are directly observed. The cause is not isolated, full storage/compute matching is not established, and it is not the same as literal exact-task solution replay. Phase 1D must compare distinct memory representations and abstraction under common exposure, storage, compute, candidate, retrieval, and task budgets.

This audit is retrospective only; it creates no new evidence about abstraction or memory performance.