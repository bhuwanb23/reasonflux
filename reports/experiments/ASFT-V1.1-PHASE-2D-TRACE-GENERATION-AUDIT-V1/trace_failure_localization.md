# Phase 2D.8 — Trace Failure Localization

## Observed localization

**F6 — Mixed observed bottlenecks; F7 — primary causal attribution unresolved.**

| Possible failure | Evidence | Attribution limit |
|---|---|---|
| **F1 Representation** | All-ten Phase 2C scan finds demo fits on only 1% of tasks. | No matched richer representation; do not assign primary cause. |
| **F2 Search** | Cap3→6→all-ten increases successful traces 2→5→10 per 1,000. | Effect is specific to fixed DSL and exact demo-fit endpoint. |
| **F3 Trace yield** | Valid traces are abundant, but successful traces are 0.2–1.0%. | This is the earliest visible trace-stage attrition; upstream no-fit can reflect search and/or representation. |
| **F4 Trace diversity** | Fullscan discovery has three successful operation signatures, each support one; coarse structure has only two buckets across all ten successes. | Structural buckets are diagnostics, not semantic taxonomy. |
| **F5 Support threshold** | No operation reaches support five; actual miner emits no patterns/candidates. | Threshold is frozen; no lower-threshold experiment was run. |
| **Trace quality** | Successful traces fit every training demonstration; no partial traces are emitted. | Generality beyond demonstrations was not measured, so “good” trace quality is not established. |
| **Downstream miner** | Fragments are formed but raw pattern count is zero; no candidates are rejected. | No high-support positive control, so miner adequacy on sufficient inputs remains untested. |

The first observed attrition is **successful trace yield**, not trace record generation or structural validity. The later invariant gate is also not reached: three fullscan discovery successes do not recur across five task IDs. This points to a mixed chain—search/representation-limited demo-fit yield plus insufficient recurrence/diversity—not to one automatically culpable component.

## Classification and claim ceiling

Use **F6 mixed** for the observed pipeline. Retain **F7 unresolved** for causal/root-cause attribution. There is no evidence that the trace miner failed on adequate input, and no evidence that the full ASFT mechanism chain was meaningfully tested. ARC failure is neither ASFT success nor, by itself, a theory falsification.