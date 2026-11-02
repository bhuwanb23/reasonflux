# Phase 1H.3 — Mandatory Baseline Registry

All seven baseline slots must be declared in each experiment's registry. A slot may be `not applicable` only with a preregistered rationale and independent review; it may not be silently omitted. Oracle remains analysis-only and cannot compete for an empirical system win.

| ID | Baseline | Minimum frozen implementation | Main alternative explanation |
|---|---|---|---|
| BL1 | No Learning | Same base solver/tasks/horizon/resources, with the claimed learning mechanism disabled and no persistent learned updates. | Improvement may reflect base solver/task design rather than learning. |
| BL2 | Memory/Retrieval | A predeclared retrieval subtype with time-t-only records, no test-label access, exact output verification, and memory budget cap. | Gains may come from remembering/reusing traces/examples rather than abstraction/selection. |
| BL3 | Random | Randomized choice among exactly the same eligible candidates and legal actions, with frozen seed schedule and equal decisions/trials. | Gains may reflect candidate pool or chance rather than learned ranking. |
| BL4 | Frequency | Candidate ranking by training-only occurrence/reuse counts, with frozen recency/ties. | Frequency alone may explain apparent invariant/skill value. |
| BL5 | Compression | A named compression method or bounded proxy (e.g. exact trace-signature compression) with a frozen interface/budget. | Benefits may arise from shorter/reused representations rather than ASFT-specific theory. |
| BL6 | Hybrid Memory+Frequency | Fixed combination of BL2 retrieval and BL4 frequency, with weights/feature availability set on development only. | Simple component combination may explain gains attributed to the full system. |
| BL7 | Oracle analysis only | Gold/latent-rule upper bound; executed only after candidate and metric freeze in isolated analysis. | Quantifies headroom/benchmark ceiling; never evidence of deployable superiority. |

## Source-level cautions

- Phase 13C `MEMORY_ONLY` is raw trace-exemplar/macro-operation reuse, not literal full-solution episodic replay and not the same as B2 skill storage.
- Phase 13G B2 is nearest-episode retrieval using non-label grid-statistic distance and exact demonstration verification; it is not full exact-answer replay.
- Phase 13F B4 is a compression-only proxy, not canonical DreamCoder.
- A B2 or B4 result from one phase does not automatically instantiate the same baseline family in another; preserve versioned implementation and outcome definitions.

## Comparison rule

For a mechanism claim, require the most relevant baseline family, not merely all seven as an undifferentiated list. For every required slot, report implementation hash, opportunity/candidate pool, activation, budget, selected actions, eligible/attempted/completed counts, endpoint, and status. A baseline that never activates is not proof that ASFT beats that alternative.