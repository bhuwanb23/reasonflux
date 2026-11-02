# Phase 2E.8 — Invariant Failure Localization

## Outcome: **F6 Mixed observed bottlenecks; F7 unresolved primary causal attribution**

| Possible cause | Evidence | Limits |
|---|---|---|
| **F1 Trace scarcity** | Only 1–3 successful discovery traces enter mining per condition; 597/600 Phase 13G traces are valid no-fit records and excluded by the success-only miner. | Upstream task no-fit is not localized to representation versus search here. |
| **F2 Recurrence scarcity** | Exact operation n-gram support maxes at 1–3; no signature reaches current support 5. | The four repeated signatures are control-flow instrumentation, not meaningful ARC structures. |
| **F3 Candidate generation** | At current support, no pattern/structure reaches the generator. At S2, it maps two structures to proposals, then rejects both. | No accepted candidate exists to assess on adequate input. |
| **F4 Support threshold** | The current 5/5 extraction floors make Stage 4 impossible on the observed pool; S2 yields four patterns. | This shows incompatibility with current supply, not that support 5 is globally wrong. |
| **F5 Validation** | No production candidate reaches validation. In a bypass diagnostic, structural F-C-G states occur for some proposals, but T/R are zero and no promotion occurs. | Same-input diagnostics and outcome-derived family labels cannot establish candidate truth, generality, or FDR. |
| **Miner implementation** | The pattern extractor emits four patterns and aggregation two structures at S2 on the same corpus. | This demonstrates executable functionality, not semantic discovery competence or adequacy on richer traces. |

The earliest production-path loss is **support filtering at pattern extraction**; it is preceded by trace-supply scarcity and low recurrence. Under relaxed support, the next observed loss is the `universal_noise` rejection rule. The final validator has measurable gates but no production candidates. These observations separate the stages, but they do not identify a single causal root or establish whether meaningful ARC invariants exist.

Do not assign blame to the miner, support policy, representation, or trace generator alone. Phase 2E supports the statement: *the current pipeline cannot discover an invariant from the available trace corpus under its frozen thresholds; its pattern code executes under relaxed support, but its semantic discovery ability and candidate false-discovery rate remain untested.*