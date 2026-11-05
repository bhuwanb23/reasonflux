# T2T-S1.2 — Claim N Decision Rule

**ID:** `T2T-S1.2-ClaimNRule-v1.0.0-draft`  
**Question:** does the invariant representation predict a held-out effect better than the strongest fair replay representation from the same permitted source experience?

## Chosen primary outcome: all-context exact effect-prediction accuracy

Use **one-step transition-effect prediction accuracy** as the primary Claim N outcome. Do not choose among prediction accuracy, transfer accuracy, task success, compression-adjusted utility, or a composite after seeing results. Behavioral task performance and resource use remain separate secondary outcomes.

For each prospectively eligible held-out decision context `j`:

- Freeze the arm's predicted local effect before the action/result.
- Compare it with the later observed effect using the same versioned, exact effect comparator and normalized representation for both arms.
- Score `1` only for an exact match; score `0` for an incorrect prediction, abstention/no prediction, malformed/invalid prediction, or other failure to issue a valid prediction.
- Include every eligible context in the denominator. Do not calculate the primary outcome only over contexts on which an arm chose to predict.

For arm `m`:

`Acc_m = (number of exact correct predictions by m) / (number of all eligible held-out contexts)`

The primary contrast is:

`Delta_N = Acc_I0 - Acc_R1`

where **I0** is the invariant representation with counterexample-boundary updates frozen/disabled, and **R1** is the competent strong replay baseline. Both use the same source corpus, observable context, prediction interface, target contexts, and prospectively matched resource opportunities. Claim N is not tested against raw replay alone.

## Exact S1 decision

For an exhaustive deterministic S1 toy state space, the operational success criterion is simply:

> **N passes the toy mechanism check iff `Acc_I0 > Acc_R1` over the same exhaustive eligible contexts, with abstentions scored as incorrect.**

A tie or lower I0 accuracy is a failure of this toy criterion. This is an exact finite-domain comparison, not a statistical claim about ARC or a task population.

For any future sampled/stochastic study, a positive point difference alone is not enough to claim population-level support. The inferential rule must be frozen before outcomes in a later protocol; at minimum it must require a lower uncertainty bound for the paired `Delta_N` to exceed a prospectively chosen meaningful-effect threshold. The confidence level, threshold, sample size/power, and uncertainty method remain **UNSET**; this S1 document does not guess them or make the P5 protocol run-ready.

## Mandatory diagnostic reporting (not alternate primaries)

Also report, without replacing the primary outcome:

- per-arm coverage and abstention/invalid-prediction counts;
- P3-compatible selective risk and coverage-risk summaries;
- paired context-level wins/ties/losses and the complete denominator;
- the R1/I0 resource vector (source information, storage, retrieval, model/tools, context, construction, invocation compute/time, actions and fallback); and
- relation-stripped and replay stress-test outcomes when available.

Because the primary accuracy denominator includes all contexts and abstentions score zero, an apparent gain cannot be created simply by reporting accuracy on a narrower selective subset. Coverage remains essential for diagnosis and for interpreting whether either representation is useful.

## Freeze and validity requirements

- The target effect definition, normalizer, exact-match comparator, eligible-context rule, and missing/outcome handling must be pinned before results.
- Predictions must be versioned and frozen before the target action/result; later assessments cannot rewrite predictions.
- The prediction context must be held out from the artifact's construction/refinement evidence. An outcome used to refine a version or descendant cannot validate that version or descendant.
- Counterexample-derived boundary learning is held fixed in I0 and R1 for N. It is isolated as the separate B factor.
- R1 competence, implementation, construction opportunity, and source-only tuning must be reviewed and frozen before target outcomes. If R1 is straw-manned or the common information/resource conditions fail, classify N as invalid/inconclusive—not supported.

## Scope and limitation

This rule chooses a measurable operational endpoint. It does not prove that the representation is novel, that a prediction advantage changes actions, reduces harm, improves official score, or justifies costs. It does not resolve the ARC observation/effect ontology or P5's future statistical freeze fields. Those remain separate gates.
