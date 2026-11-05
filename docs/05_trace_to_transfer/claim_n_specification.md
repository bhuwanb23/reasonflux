# Claim N Specification — Invariant Value Beyond Replay

**Claim version:** `T2T-ClaimN-v1.0.0-draft`  
**Controlling design:** [`T2T-P3-FairReplay-v1.0.0-draft`](p3/fair_replay_controls_v1.md)  
**Status:** untested design claim; not novelty-cleared. P3 completion authorizes no implementation, experiment, benchmark, ARC run, split assignment, outcome-based tuning, or restricted-outcome access.

## Claim

**N (comparative):** Under matched permitted information, model/tool access, storage, context, retrieval, compute, action, and evaluation conditions, the explicit invariant-derived representation contributes predictive value beyond the strongest fair replay/parameterized-script representation built from the same source experience. A separate behavioral increment may be claimed only if its own predeclared endpoint supports it.

The primary mechanism endpoint is predictive because N concerns an explicit state/action/effect representation. Prediction and behavioral findings must be reported separately; no composite “invariant value” score is defined. Claim N is untested, and no current evidence establishes it.

## Required arms

1. **R0 — Raw fixed-trace replay:** exact ordered trace/script playback under recorded source-context assumptions; no parameter rebinding, repair, or adaptation. On mismatch, stop/abstain. Useful reference but insufficient alone.
2. **R1 — Strong trace-derived replay (required primary comparator):** competent compression, retrieval, typed slot binding (including new literal IDs where fixed schema/field rules allow), and bounded source-derived script control flow, with the same source events and common prediction/action interface. It may apply fixed schema/type/slot checks but has no learned cross-context invariant boundary, counterexample-derived guard, or target-outcome conditioning. For effect prediction, it only transports aligned source-trace effects through those fixed substitutions and otherwise abstains. It must not be intentionally weakened; exact implementation and independent competence review are frozen before any authorized evaluation.
3. **I0 — Invariant representation, boundary updates held fixed:** explicit versioned relation, typed state/action/effect variables, parameter mapping, observable applicability predicates, and prospective effect prediction, derived from the same permitted source corpus. Counterexample-based boundary updates are disabled or frozen identically for Claim N.

Optional `I1` (counterexample boundary update enabled) addresses the separate boundary-learning Claim B; it is not part of the primary N contrast. Optional no-skill is descriptive only. If R1 functionally matches I0, do not relabel its behavior as an invariant after seeing results.

## Primary comparison and estimand

The primary contrast is **I0 versus R1**, over the same permitted held-out decision contexts and target effects. Report prediction coverage and selective risk/error together; directly compare risk only at a prospectively specified common coverage/operating point, or use a prospective scoring rule that explicitly accounts for abstention. Conditional accuracy alone is insufficient; coverage is mandatory and abstentions remain in the all-context denominator. Exact prediction targets, scoring/loss and abstention operating point/cost, aggregation, uncertainty, sample size, and decision margins remain `UNSET` for a later protocol phase.

A secondary behavioral estimand compares I0 and R1 by intention-to-treat over all assigned tasks/episodes, including abstentions, errors, and fallbacks. Report official task score/progress and action efficiency separately. Do not condition the main estimate on post-treatment applicability or invocation. Report creation, validation, invocation, and resource costs as a vector, not a weighted score.

## Fairness and isolation requirements

- Same source-event manifest/cutoff, observation/action schema, permitted data, model/checkpoint, prompts/tools, common retrieval interface, target contexts, evaluator/version, and declared budget opportunities.
- Match information and resource caps prospectively; report actual use separately. Account for storage, context, retrieval, model/tool calls, creation/validation/invocation compute and time, actions, retries, and fallback.
- Freeze all arm artifacts, retrieval features, slot rules, prompts/configurations, metrics, operating points, and analysis decisions before target outcomes.
- No outcome-based baseline tuning; no target/test/hidden/leaderboard outcomes or post-hoc split labels may inform arm construction or thresholds.
- Keep counterexample-boundary updates out of the primary N contrast; otherwise N is confounded with B.
- If a difference in model, input, retrieval, assignment, evaluator, or resources could explain the effect and cannot be isolated, report the comparison as confounded/inconclusive, not evidence for N.

Exact definitions, budget matrix, ablations and design conformance checklist are in the [P3 fair replay control contract](p3/fair_replay_controls_v1.md).

## Falsifiers and interpretation

- R1 matches or exceeds I0 on the prospective predictive endpoint at comparable coverage and matched budgets: N is not supported under the tested conditions, even if both beat R0/no-skill.
- I0 beats R0 but not R1: the gain is consistent with compression, parameterization, retrieval, or ordinary engineering—not an invariant-specific increment.
- I0's lower error comes only from more abstentions: no predictive advantage absent the predeclared coverage/abstention criterion.
- A relation-stripped I0 ablation matches the full I0: no demonstrated incremental role for explicit invariant semantics.
- Any gain disappears at matched resource caps, relies on extra information/model/context/actions, or comes only from better macro execution without a predictive increment: N is unsupported as framed.
- Outcome leakage, post-hoc threshold/arm changes, or an unreviewed/crippled R1 makes the comparison invalid or inconclusive; it does not count as support.

If predictive benefit appears without behavioral benefit, report only a predictive increment. If behavior differs but prediction does not, do not attribute the difference to invariant semantics without a valid relation ablation and confound analysis. Exact significance/effect thresholds and uncertainty methods are not set here.

## Novelty and authorization boundary

P1 rejected standalone mechanism novelty and selected a comparative ARC-specific reframe provisionally; this is not novelty clearance. Claim N is a design target, not a result. No implementation, experiment, benchmark, ARC run, split assignment, outcome-based baseline tuning, or restricted-outcome access is authorized by this document.
