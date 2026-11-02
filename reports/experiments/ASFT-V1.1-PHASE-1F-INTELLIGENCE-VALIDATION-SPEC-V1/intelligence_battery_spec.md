# Phase 1F.4 — Independent Intelligence Battery Specification

## Independence rule

The battery is scored from task inputs, system outputs, evaluator gold/rubrics, exposure logs, and resource logs. It does not read IG, IGR, IE, CGR, C_t, capability-object metrics, or internal transfer scores. Each test has its own outcome and denominator; there is no posthoc one-number intelligence score. All policies receive the same task opportunities, demonstrations, context/compute caps, and evaluation procedure.

## Frozen tests A–F

| Test | Procedure and target | Why it is construct-relevant | Success/failure criterion |
|---|---|---|---|
| A — Future Learning Rate (**primary**) | Present a novel task family with fixed feedback at 0, 1, 3, and 5 examples; score on separate held-out items after each exposure. Target is normalized area under the external accuracy curve (AULC), averaged first within family and then across families. | Directly observes how quickly future competence is acquired rather than how much an internal score changes. | A positive-direction, practically meaningful out-of-sample prediction beyond M0, with the preregistered SOI; capability/learning gate also requires above-chance task performance. |
| B — Adaptation Speed | After a stable baseline, shift one rule, task distribution, family, or vocabulary dimension; provide a fixed small evidence budget and probe on unseen post-shift tasks. | Directly measures recovery/flexibility under changed conditions. | Recovery AULC or examples-to-criterion improves over the matched no-learning/random control and baseline; no test-item tuning. |
| C — Novel Environment Success | Evaluate in independently generated environments/templates not seen in training or development; provide a fixed zero-shot/limited context. | Tests transfer/generalization beyond the familiar generator. | Held-out family accuracy exceeds chance and fixed baseline with cluster-aware interval; report each environment. |
| D — Few-Shot Acquisition | Give exactly one and five demonstrations for a novel operation and unseen compositions; score on disjoint queries. | Tests rapid acquisition and compositional competence from scarce evidence. | Held-out performance increases with the fixed evidence, exceeds no-learning and best-single-component controls, and stays within budget. |
| E — Cross-Domain Learning | Learn in source domain, then present a disjoint target domain with a fixed adaptation budget; use at least two domains and separate evaluators. | Tests transfer-enabled learning, not merely source-domain reuse. | Positive target-domain learning gain over matched no-source-learning and random baselines in preregistered domains. |
| F — Generalization Retention / Relearning | After 20 intervening tasks without refresh, probe delayed novel variants; then measure examples needed to reacquire a related skill. | Tests durability and whether prior learning supports later generalization/relearning. | Delayed held-out success retains ≥90% of immediate external performance or shows preregistered relearning savings, while still exceeding chance. |

## Primary endpoint

`A_future_learning_rate_normalized_auc` is the primary endpoint. At fixed exposure points `[0,1,3,5]`, calculate the trapezoidal area under evaluator-scored accuracy, divided by the exposure range. Average within task family before equally weighting families. Higher values indicate better observed future learning efficiency. The raw curve, slope, threshold success, and all task denominators remain visible.

## Scoring and handling

- Exact correctness or frozen task-specific rubrics; current contract prototype implements exact match and normalized AULC only. Rubric adapters, task generators, and evaluators remain to be implemented and frozen on development data.
- Separate task outputs and gold/rubric stores; evaluators blind to IG and predictor values.
- Record abstentions, failures, missing tasks, exposures, compute/tokens, and family/domain IDs separately.
- No internal metric may select tasks, set thresholds, impute outcomes, or determine success labels.
- If an external outcome cannot be computed with IG disabled, Phase 1F fails construct separation.