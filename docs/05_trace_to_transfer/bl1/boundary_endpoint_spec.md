# BL1-P0 — Boundary Endpoint Specification

**Status:** prospective definitions for planning only. No outcomes exist, and no experiment or implementation is authorized. BL1 is terminated at P0; these definitions do not authorize reopening it.

## Evaluation unit and labels

The unit is a frozen held-out context–candidate-skill pair. Before any prediction, define an eligibility target independently of either boundary learner:

- **Applicable (Y=1):** under the fixed skill/policy, execution meets the domain's predeclared success criterion from this context.
- **Inapplicable (Y=0):** execution does not meet that criterion.

The success criterion, run/retry rule for stochastic skills, context inclusion rule, and label custody must be frozen before any evaluation. Do not derive the target from the learned boundary's own decision. Invalid/missing outcomes are reported separately and excluded only under predeclared rules.

Each boundary predicts **permit** (the skill may activate), **reject**, or **abstain**. For the binary confusion counts, reject and abstain both count as not permitted for TP/FN/TN/FP, while abstentions are also reported as a separate outcome so a system cannot hide broad abstention.

## Primary endpoints

Let TP = applicable contexts permitted; FP = inapplicable contexts permitted; FN = applicable contexts not permitted; TN = inapplicable contexts not permitted. Report counts and their denominators for each arm and paired differences on the same held-out contexts.

1. **Applicability precision (primary precision endpoint)**

   `Precision = TP / (TP + FP)`

   This is the share of permitted activations that are truly applicable. If `TP + FP = 0`, precision is **undefined**, not 1; the arm cannot pass by permitting nothing. Also report false discovery proportion `FP/(TP+FP)` when defined (= 1 − precision).

2. **Useful coverage (guardrail; applicability sensitivity/recall)**

   `Useful coverage = TP / (TP + FN)`

   This is the share of all truly applicable held-out contexts for which the skill remains available. If there are no applicable contexts, it is undefined and the suite is invalid for this endpoint. Report coverage among all held-out contexts (`permitted / all valid contexts`) and abstention rate as descriptive safeguards, not substitutes for useful coverage.

3. **False activation rate (guardrail)**

   `False activation rate (FAR) = FP / (FP + TN)`

   This is the share of truly inapplicable contexts wrongly permitted. If there are no inapplicable contexts, FAR is undefined and the suite is invalid for this endpoint. FAR is not the same quantity as `FP/(TP+FP)`; report both FAR and precision.

## Comparison and decision quantities

- Primary contrast: paired absolute difference `ΔPrecision = Precision_treatment − Precision_control` on the identical frozen held-out suite.
- Guardrails: treatment useful coverage must meet its frozen minimum and must not be materially worse than control; treatment FAR must meet its frozen maximum. Report paired differences for coverage and FAR, abstention, and all raw counts.
- Report per-skill/task-stratum results as well as the aggregate; do not let a large easy stratum conceal failure in another.
- State the uncertainty procedure and interval level prospectively. If resampling, resample at the independent context-generation/task unit, not correlated repeated trials as though they were independent contexts. For stochastic execution, distinguish context count from execution replicates.
- A future protocol must set numeric effect/floor/ceiling values, suite size, and uncertainty rule before any held-out predictions or labels are available. No values are inferred from the S2 2/4→0/4 toy observation.

## Interpretation constraints

A precision increase alone is not success: it can result from rejecting most contexts. A coverage increase alone is not success: it can come with excessive false activations. The intended joint result is improved precision, with useful coverage maintained and FAR controlled, on genuinely held-out contexts. Undefined endpoints, failed integrity checks, or inadequate labeled denominators do not count as a pass.

These measures concern only the tested applicability-boundary estimand. They do not measure broader model quality, transfer, capability, or any other T2T claim.
