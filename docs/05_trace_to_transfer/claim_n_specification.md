# Claim N Specification — Invariant Value Beyond Replay

## Claim

**N:** Under matched information, storage, compute, action and retrieval budgets, the invariant-derived skill representation contributes predictive or behavioral value beyond the strongest fair replay/parameterized-script representation built from the same permitted experience.

This is the key novelty-separation claim. It is untested.

## Why the comparison must be strong

A raw action sequence is an intentionally weak baseline if the proposed method has variables, parameters, retrieval, or effect checks. Beating raw replay alone would show that richer engineering helps—not that invariant semantics matter. Compare at least:

1. **Raw replay:** source trajectory/script replayed under its native fixed-state assumptions.
2. **Strong replay/compression:** best-effort compact/parameterized trace-derived procedure using the same source data; it may bind simple parameters but does not learn a cross-context invariant boundary from counterexamples.
3. **Invariant skill:** explicitly represents the cross-context relation, parameters, applicability conditions and predicted effects; boundary learning is a separately controlled factor.

The baseline implementation must be frozen before evaluation and reviewed to ensure it is not artificially crippled.

## Isolation design

- Same source traces, task exposure, model, prompt/tool/runtime, retrieval budget, memory budget and compute/action caps.
- Same target contexts, order, and evaluator; no target outcome available to candidate construction.
- Report both absolute storage size and use-time context/compute; match or provide a prespecified cost curve if exact matching is impossible.
- Ablate invariant semantics while retaining the same skill wrapper/interface where possible.
- Separately ablate counterexamples so Claim N is not confounded with Claim B.

## Outcomes

1. **Predictive:** effect prediction accuracy/coverage on held-out contexts, with abstentions and denominators.
2. **Behavioral:** whether the procedure changes action selection under valid matched conditions.
3. **End-to-end:** official score/action efficiency in the full assigned evaluation cohort; all resource costs reported separately.

No custom weighted “invariant value” score is primary. If the baseline’s effect prediction and end-to-end performance are indistinguishable from the invariant version at matched budgets, Claim N is not supported even if both systems outperform no skill.

## Falsifiers

- Strong replay matches or beats invariant skills.
- Any gain disappears when storage/context/retrieval/compute are matched.
- Gains come only from a better action macro, with no incremental effect-prediction/generalization benefit.
- The invariant ablation performs equally well.
- Apparent benefit depends on target outcomes or post hoc threshold choices.
