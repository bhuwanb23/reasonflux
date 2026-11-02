# Phase 1G.7 — Transfer Benchmark Specification

## Estimands

Transfer is successful application of a validated skill or learned structure to a held-out task not used in its formation, with positive external task utility relative to a matched no-skill baseline. Report separately:

- eligible skill-task pairs and attempted applications;
- exact transfer rate among eligible attempts;
- partial/pixel utility and paired net utility under fixed budgets;
- positive, neutral, and negative transfer rates;
- source-to-target family/domain and task IDs;
- skill survival across transfer tests and resources/candidate trials.

Do not use task-level accuracy as transfer rate unless the skill was eligible and an explicit matched transfer contrast is defined. Transfer is not coverage or capability.

## Controls

Use same-task paired no-skill/fixed-search comparison, nearest-episode memory retrieval, random qualified-skill/program selection, and exact trace-signature compression as separately identified mechanisms. Preserve Phase 13G source distinctions: B2 is nearest-episode retrieval without invariant abstraction, B3 random ordering of the same qualified operator pool, B4 exact trace-signature compression—not canonical DreamCoder. Freeze the transfer eligibility rule, task assignment, and resource budgets.

## Denominator rules

- If no validated skill applies to a target task, that pair is ineligible; do not count it as a transfer attempt.
- If eligible pairs exist but no attempt is made due a logged policy failure, report policy omission distinctly.
- If eligible attempted pairs = 0, transfer rate/precision/utility are **unavailable**, not zero.
- Negative transfer is an observed behavior result and is reported even if overall accuracy is high.