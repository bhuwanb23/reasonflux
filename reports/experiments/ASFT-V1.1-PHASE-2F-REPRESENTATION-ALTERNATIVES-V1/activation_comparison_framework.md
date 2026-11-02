# Phase 2F.7 — Downstream Activation Framework

The activation chain is measured with stage-specific outcomes and denominators, not a single end score:

| Stage | Operational endpoint | Required reporting |
|---|---|---|
| **Coverage** | At least one exact training-demo fit within the registered language/budget. | Tasks covered, fit candidates, capped no-fits, parser/parameter failures. |
| **Trace generation** | One trace emitted; independently validated. | Generated/valid/invalid; no-fit vs success. |
| **Successful trace** | Selected candidate exactly replays every training demonstration. | Successful traces/tasks and rate; demo fit is not accuracy. |
| **Invariant discovery** | Candidate survives frozen support/miner/generation gates; validated state separately recorded. | Raw recurrence, proposals, rejection reasons, validator input and states. |
| **Skill eligibility** | Validated invariant maps through a pretested representation adapter to the unchanged SkillCandidate schema and satisfies unchanged `SkillConfig`/`qualify_candidate` rules. | Eligible, ineligible with reason, or `UNAVAILABLE_INTERFACE`; no auto-conversion of invariant count into skills. |
| **Transfer eligibility** | Qualified skill has at least three predeclared applicable transfer tasks under the unchanged Phase 13G rule. | Applicability denominator and eligibility separately from test success. Zero denominator is unavailable. |
| **Capability eligibility** | Existing capability builder receives the required active/transfer-supported skill units and passes unchanged capability criteria. | Eligible/ineligible and missing inputs; unavailable is not zero capability/intelligence. |
| **Accuracy** | Exact task-level test success, only through separately authorized sealed evaluator. | Separate endpoint, comparator, split, uncertainty, and submission status; `NOT_MEASURED` until authorized. |

For every arrow report survivors and attrition reasons. `BLOCKED_UPSTREAM`, `NOT_RUN`, `UNAVAILABLE_INTERFACE`, `NOT_ESTIMABLE_ZERO_DENOMINATOR`, and observed zero are different states. Keep the downstream code/config identical across representations. A representation-specific adapter is an interface contract, not permission to alter qualification logic; it must pass the same frozen contract tests before outcome runs. If a skill cannot execute on an alternative's representation, report interface-unavailable rather than attributing it to SCT or counting a failure.

### Key falsifiable pattern

If an alternative increases coverage substantially but recurrence/invariant yield remains zero under the same frozen support policy, that is evidence that improved coverage alone did not activate the mechanism chain and weakens a representation-only explanation. If coverage and valid successful traces rise but invariants do not, localize the next failure to recurrence/mining/support. If validated invariants appear but skills/transfer/capability do not, localize further downstream. None of these alone proves theory-wide failure or success.