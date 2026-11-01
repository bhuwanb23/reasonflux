# Cross-Contribution Interaction Analysis

## Verdict

ASFT's software modules and data flow are connected, but evidence of **positive causal reinforcement or synergy** among IDT, SCT, transfer, and CGM is not established. The available results include exact ties, policy degeneracy, endpoint trade-offs, and cross-phase differences. There is no common factorial interaction design that isolates the combined contribution of all four mechanisms.

## Evidence ledger

| Interaction | Saved result | Cross-contribution inference |
|---|---|---|
| IDT transfer-aware ranking × candidate frequency | Corrected 13B ASFT, frequency-only, and no-transfer tie at top-k=2 TU `0.095809`; same semantic ordering in all five seeds. | No primary incremental ranking advantage. EXP-IDT-14 shows sensitivity to an intentionally inserted frequent no-op only. |
| SCT/SCV selection × skill creation | 13C SCT, ALWAYS_CREATE, and RANDOM_CREATE all have net value `0.345`; 44/44 eligible candidates selected. 13F ASFT/no-SCV/random-SCV also tie on utility and CGR, each selecting all four available candidates. | Skill objects form, but selection's incremental advantage was not exercised or demonstrated in those candidate pools. |
| Skill creation × memory/retrieval | 13C MEMORY_ONLY net value `1.325` vs SCT `0.345`; memory applies 440/440 opportunities and records 418 correct, SCT applies 223/440 and records 201 correct. | Memory is a serious alternative on that protocol, but the unequal application counts do not isolate per-attempt quality or abstract-skill value. |
| Transfer × task utility | 13D corrected ASFT has positive transfer-utility contrasts vs B1–B3 but is `0.001091` below B4; 13F no-transfer has higher all-task utility by `0.036344`. | Transfer-specific benefit does not guarantee broad task-utility improvement or universal baseline superiority. |
| Transfer × capability growth | 13D CGR mean `-0.060`; 13E TS–CGR negative/uncertain and no-SCT CGR contrast `0`; 13F transfer removal favors task utility but lowers CGR. | Endpoints diverge; no robust transfer-causes-growth effect. |
| Capability layer × behavior | In 13F, removing the capability layer leaves task/composition utility unchanged but changes CGR. | Measurement-layer movement is not behavior-level improvement. |
| Composition × growth/value | 13C provides one successful rotation→reflection composition; 13E has incremental value `-0.1429` and no post-composition capability-count gain; 13F has positive composition-specific outcomes. | Limited, phase-dependent composition evidence; no stable contribution across contexts. |

## Interpretation

1. **A dependency is not a synergy.** Later stages require earlier artifacts by software design. That does not show that combining them improves a relevant outcome over simpler mechanisms.
2. **A tie is informative but local.** It shows no contrast under the frozen pool and endpoint; it does not prove universal irrelevance.
3. **Metric movement is not automatically behavior movement.** The no-capability-layer result is a direct caution against interpreting CGR changes as task improvement.
4. **Baselines differ.** MEMORY_ONLY in 13C, B2 in 13D, B2 skill storage in 13E, and B2 memory-skill store in 13F are not interchangeable or poolable.
5. **No factorial estimate exists.** The record cannot tell whether IDT+SCT+transfer+CGM yields a positive interaction above the sum of its parts.

**Conclusion:** component interactions are present in the pipeline and some local pathways are observed; claimed advantages of those interactions remain unproven.
