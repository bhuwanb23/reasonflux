# Ablation Interpretation Report

| Ablation/component | Phase evidence | Interpretation |
|---|---|---|
| IDT / invariants | 13D corrected ASFT−A1_NO_INVARIANTS `+.018909` on transfer utility; 13E removing IDT reduces CGR `+.05950`; 13F ASFT−A1_NO_IDT task utility `-.002438`, CGR `+.015001`; 13B frequency/no-transfer ties ASFT | Some local transfer/growth endpoint contribution; task-utility effect not consistent and frequency sometimes ties. Partial evidence, not universal necessity. |
| SCT | 13C SCT=ALWAYS_CREATE=RANDOM_CREATE; 13D A2_NO_SCT difference 0; 13E A2_NO_SCT CGR difference 0 | Incremental necessity not established. In 13C/13F, selection often chose the whole eligible pool, reducing information in the ablation. |
| SCV | 13C all 44 eligible confirmation rows selected; SCV10 shadow correlation `.700` vs frequency `.748` and p_reuse `.884`; 13F no-SCV and random-SCV both tie ASFT | No incremental/unique SCV contribution demonstrated in these selection pools; predictive correlation alone is insufficient. |
| Skill persistence | Corrected 13D ASFT−A3_NO_PERSISTENCE `+.017018` on transfer utility | Persistence matters for that synthetic transfer endpoint, but evidence is phase-specific. Do not conflate persistence with lifecycle policy. |
| Lifecycle | 13C enabled vs disabled net value differs by 0 in every seed; 13F A2.2_NO_LIFECYCLE utility/CGR differences are 0 | No measured contribution in these task streams; cannot infer universal uselessness. |
| Transfer | 13F X1_NO_TRANSFER: ASFT−X1 task utility `-.036344`, composed utility `-.34125`, CGR `+.287172`; 13D transfer metric results positive in covered cells | Benefits depend on endpoint; transfer does not yield a uniform task-utility advantage. |
| Capability/CGM layer | 13F A3_NO_CAPABILITY_LAYER utility/composed-task differences 0 while CGR differs; A5_NO_CGM masks metrics by design | Measurement-layer changes can alter reported growth without behavior change; not a performance effect. |
| Composition | 13C rotation→reflection: ordered composition and the no-skill composition-capable solver both succeed 100%, best single skill 0%, with normalized step reduction `.429` on one evaluable pair; 13D unavailable; 13E value `-.1429`, no count gains; 13F no-composition arm loses on one composed-task stream | Mixed, task-specific evidence. One operation pair and one phase cannot establish general composition value or capability generation. |

## What a null ablation means here

A zero paired difference is a result for the frozen intervention and endpoint—not proof the component never matters. It may mean the mechanism was not exercised (e.g., identical selected candidate set, no lifecycle event changing the portfolio), or the metric is insensitive. Conversely, removing an instrumented metric layer can force metric changes while leaving behavior untouched. Interpret only the endpoint and manipulation actually recorded.
