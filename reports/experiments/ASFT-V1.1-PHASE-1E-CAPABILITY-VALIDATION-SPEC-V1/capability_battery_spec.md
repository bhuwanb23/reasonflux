# Phase 1E.4 — Independent Capability Battery Specification

## Target independence

The battery consists of task prompts/instances, allowed inputs, system outputs, and evaluator gold/rubric. It does **not** receive or read C_t, CGR, IG, IGR, IE, capability-object count, or internal capability labels. The evaluator scores behavior from task outputs only. The six component scores are equally weighted in the External Behavioral Capability Score (EBCS); each component is macro-averaged over task families, not pooled by raw task count.

## Required tests

| Test | Procedure | Success criterion | Failure interpretation |
|---|---|---|---|
| A — Novel Task Success | Evaluate on new instances and held-out templates in a trained task family; no exact query/answer appears in memory. | At least 20 items; accuracy ≥0.70 and cluster-aware lower CI ≥ baseline +0.05 on ≥2 surface partitions. | Failure to perform beyond exact replay or prior baseline. |
| B — Transfer Success | Evaluate on disjoint task families/transformations with no target-family demonstrations. | Meets behavioral capability-unit accuracy, transfer-family and positive-utility criteria; report per-family results. | No evidence of transfer if only source-family tasks pass. |
| C — Task Breadth | Test six or more predeclared family clusters with fixed task counts. | Breadth = fraction of families passing the family gate; report count and distribution, not just mean. | A high mean confined to one family is not broad capability. |
| D — Retention/Persistence | Repeat equivalent-but-not-identical behavioral probes after 20 intervening tasks without refresh or target feedback. | Delayed score ≥90% of immediate score and still clears absolute/baseline gate. | Loss after delay is not persistent capability. |
| E — Compositional Performance | Combine previously trained components in unseen orders/combinations; include best-single and wrong-order controls. | Exact/quality success and net utility exceed best-single baseline by SOI on held-out combinations. | Component possession without novel composition is not compositional capability. |
| F — Adaptation Performance | Change task distribution and provide exactly five new demonstrations (or fixed preregistered count); evaluate on unseen post-adaptation tasks. | Positive pre/post behavioral gain over same-budget baseline; retention probe preserves ≥90% of gain. | Improvement only on demonstration tasks or beyond-budget tuning is not adaptation. |

## Scores and denominators

- Every arm/panel receives the same battery items, query count, context/token allowance, wall-clock/compute cap, and permitted test-time memory access. Training exposure and adaptation demonstrations are separately logged and matched where the comparison calls for it.
- Task item score is exact correctness or a frozen partial-credit rubric; evaluator is blind to arm and internal metrics. The current contract prototype checks exact-match scoring only; task-specific rubric adapters remain to be implemented and frozen during development.
- EBCS is the equal-weight mean of the six family-level test scores. Keep all six components and raw counts visible; no score may be substituted when unavailable.
- Family breadth is the count/proportion meeting the behavior gate, not the count of internal capability objects.
- Report accuracy, utility, abstentions, failure mode, per-family denominator, delayed retention, and resource use.
- `NOT_APPLICABLE`, `FAILED`, `ABSTAINED`, and `MISSING` remain distinct. Missingness does not become zero.

## Construct-separation gate

Battery generation, task scoring, capability-unit classification, and EBCS computation must run without access to the CGM metric store. Only after the outcomes, task manifest, and scoring code are locked may predictor values be joined for RQ4 analysis. If the evaluator cannot compute EBCS without CGR/C_t/IG, the benchmark fails construct separation.