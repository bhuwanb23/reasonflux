# Phase 1E.1 — Historical Capability Audit

**Sources:** Phase 13E, 13F, Phase 14E, 14H, and 14J saved records. No historical run was repeated or altered.

## Executive finding

Phase 13E shows **positive movement in the frozen internal score** in its ten-seed synthetic cohort: mean C_t/CGR `1.0227/0.2946`, with mean CGR 95% CI `[0.2857,0.3036]`; C_t was monotonic in 10/10 seeds. A capability object persisted. This demonstrates the score pipeline's behavior in that cohort—not independent capability growth.

The capability count was exactly **one at every seed-round after formation**. The same `cap-cross-domain` object persisted; its score and member inventory changed. New capability count was 1 at round 1 and 0 later. No accepted higher-order/emergent-type capability occurrences were recorded. Corrected Phase 13D mean CGR was `−0.060` over nine evaluable seeds, so robust growth across contexts was not shown.

## What C_t and CGR measured

Phase 14E audits C_t as a weighted portfolio score combining capability-member skill utility, transfer score, family coverage, and a composition bonus. CGR is `(C_t − C_(t−1))/Δt`; the first round is measured from a zero previous state, producing a large initialization jump. The score can rise when evidence/membership of one existing object changes; it is not a count of new capabilities or an independent behavioral criterion.

Phase 13E's round-1 mean CGR was `0.8405`, followed by `0.1194`, `0.1523`, and `0.0663`. C_t was monotone in 10/10 seeds, but capability count remained one. The initial-state jump and changing metric ingredients matter to interpretation.

## What was and was not established

| Question | Evidence | Verdict |
|---|---|---|
| Did C_t/CGR increase in 13E? | C_t monotonic 10/10; mean CGR `.2946`, CI `[.2857,.3036]`. | Yes, for the frozen internal score in this cohort. |
| Did an object persist? | Same validated `cap-cross-domain` object at rounds 1–4 in 10/10 seeds. | Yes, narrowly as representation persistence. |
| Did capability count grow? | One object at every round; later `new_capabilities=0`; 0/10 post-composition count gains. | No. |
| Did independent behavioral breadth grow? | No independent behavioral battery; C_t includes internal skill/transfer/coverage/composition quantities. | Not measured. |
| Did it generalize/transfer externally? | Same synthetic generator; Phase 13G produced no accepted ARC capability units. | Not established; ARC metric is unavailable after upstream pipeline coverage failure. |
| Did CGR predict behavior? | 13E C_t→next-round task utility `r=.0498`, cluster CI `[.0163,.0922]`, 10 seed clusters. | A preregistered but very small same-cohort association; not external, causal, or evidence that CGR predicts independent capability. |
| Did transfer cause growth? | 13E TS→CGR `r=-.5027`, CI spans zero; 13D TS→CGR had opposite descriptive sign while mean CGR was negative; 13E no-SCT CGR contrast 0. | Not established. |
| Did capability growth validate intelligence growth? | IG/IGR are weighted internal composites; IE divides IG by cumulative experience; no independent intelligence criterion. | No. |

The C_t→next-round utility result must not be erased: its frozen directional criterion passed. Its magnitude is tiny (`r²≈.0025` descriptively) and task utility is within the same synthetic process. It is distinct from TS→CGR and does not validate the capability construct.

## Why construct validity failed

1. **Criterion contamination:** C_t and IG are built from internal skill utility, transfer, coverage, composition, and growth values. These are not independent measures of capability behavior.
2. **Object-score conflation:** one persistent capability object can accrue a higher score without the system acquiring a new ability or solving a broader set of independent tasks.
3. **No external battery:** Phase 13E reports synthetic task utility and internal aggregates, not a held-out independent suite measuring novelty, transfer, breadth, retention, composition, and adaptation separately.
4. **Initialization sensitivity:** round 1 compares against zero; it contributes a large CGR/IG jump.
5. **Cross-context inconsistency:** 13D mean CGR is negative while 13E is positive; do not pool these unlike cohorts.
6. **Weak and internal prediction:** C_t's next-round association is small and same-generator; it does not test CGR against simpler predictors on an independent target.
7. **No emergent capability:** only one accepted portfolio object; no accepted higher-order occurrence.
8. **Downstream unavailability:** in 13G there are zero capability groups, so CGR/IG are unavailable, not zero.

## Phase 13F, 14H, and 14J context

Phase 13F shows endpoint dependence: ASFT's task-utility/CGR contrasts fail B1 and B3 but pass B2 and B4 under that protocol. Phase 14H identifies Transfer→Capability Growth as the first major missing causal bridge and Capability→Intelligence as unvalidated. Phase 14J's final scorecard says capability-growth interpretation is not established as robust capability growth; positive Phase 13E scores do not remove that limitation.

## Audit conclusion

> The saved evidence demonstrates internal metric computation, positive C_t/CGR movement in one synthetic cohort, and persistence of one capability object. It does not establish broader behavioral competence, external generalization, robust capability growth, transfer-caused growth, or intelligence growth. Phase 1E must define and score capability from independent task behavior before joining any CGR/C_t/IG predictor.