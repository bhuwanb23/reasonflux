# P3 Fair Replay and Claim N Design

**Contract ID:** `T2T-P3-FairReplay-v1.0.0-draft`  
**Status:** complete for documentation/design scope, 2026-11-04.  
**Authority:** design only. No implementation, experiments, benchmarks, ARC runs, split assignment, outcome-based tuning, or restricted-outcome access.

## 1. Purpose and claim ceiling

P3 defines a fair conceptual comparison for whether the explicit invariant representation contributes value beyond competent trace replay and parameterization. It does not assert that invariant semantics are novel or effective. P1's no-go on standalone mechanism novelty remains; the comparative ARC-specific reframe is provisional and not novelty-cleared.

The controlling claim is [`Claim N`](../claim_n_specification.md): at matched information and resource conditions, the invariant-derived representation should add predictive value (primary mechanism endpoint) and may separately add behavioral value beyond the strongest fair trace-derived replay representation. Predictive and behavioral findings are reported separately; they are not combined into an unvalidated score.

The design distinguishes representation from boundary learning. For Claim N's primary comparison, counterexample-based boundary updates are withheld/frozen identically in both invariant arms. A later with/without-counterexample comparison addresses Claim B, not Claim N. P3 does not authorize creation of a candidate, skill, or dataset.

## 2. Units, source data, and freeze points

- **Source corpus:** one exact, permitted source-event manifest, observation/action schema and version, normalizer, and source-evidence cutoff shared by every arm. The manifest, ordering, deduplication rules, and eligibility rules must be fixed before any target evaluation.
- **Target unit:** a permitted held-out decision context for prediction; for behavior, the independently assigned task/episode (or a justified paired block where the environment permits). Actions within a task/episode are repeated observations, not independent samples.
- **Common wrapper:** same outer input parser, context/query features, source-event index, retrieval API, action interface, fallback/timeout handling, evaluator, and logging. The treatment-specific relation/applicability module is the intended difference, not an excuse to change the wrapper.
- **Freeze:** version and hash each arm's artifact, prompts/configuration, retrieval index, model/checkpoint, preprocessing, permitted-data manifest, and budgets before the target cohort is exposed. Baseline capability and absence of invariant boundary learning require an independent design review before any authorized evaluation.
- **No outcome-based tuning:** do not change baseline algorithms, retrieval keys, slot rules, prompt, guard, thresholds, or resource allocation in response to target/evaluator outcomes. No target, hidden, test, leaderboard, or confirmatory outcomes may inform candidate or baseline construction. Any later revision is a new version; it requires a new, separately authorized evaluation cohort. P3 selects no cohort or split.

Source interaction records may contain observed transitions/effects because they are the allowed material from which all arms are constructed. This does not permit evaluator outcomes from a target cohort to leak into the arms.

## 3. Arm definitions

Use these names consistently. All arms receive the same permitted source corpus and common wrapper unless an ablation explicitly removes a component.

### R0 — Raw fixed-trace replay (P3.1)

A retrieved source trace is replayed as its original ordered action/script sequence, with literal recorded arguments and its native source-context assumptions. It does not compress repeated segments, rebind parameters, repair a mismatch, branch on a learned cross-context relation, or infer a new applicability region.

**Invocation:** the shared retrieval layer may select a source trace using the same frozen query and retrieval budget given to the other arms. The trace is invocable only when the declared source-context key/precondition is satisfied. Each available recorded pre-action check is applied exactly as specified. If the required context does not match, an observation/action is unavailable, an expected transition fails, or a check is ambiguous, stop and return `ABSTAIN/ERROR` per the frozen wrapper; never skip, retry, substitute, or edit subsequent actions. If the source trace has no pre-action checks, its fixed-state assumption is explicit and the trace is not treated as robust to an unobserved deviation.

For the predictive endpoint, R0 may issue only a recorded next-effect expectation associated with the selected exact trace/action; it abstains when the target context or event alignment is not exact. It cannot transform a recorded effect into a new relation. The replay log preserves source trace/version, selected retrieval key, every attempted action, matched/mismatched check, prediction/abstention, stop/fallback reason, and costs. R0 is a calibration/reference control, not sufficient evidence for Claim N.

### R1 — Strong trace-derived replay (P3.2; required primary comparator)

A compact or parameterized procedure constructed from the same source corpus. It may use:

- lossless deduplication, run-length/delta encoding, shared subsequences, and compression of repeated trace segments;
- typed argument/effect slots and deterministic rebinding from the same observable input schema, using declared positional/field/type correspondences that reconstruct the source actions and may bind new entity IDs in a target context;
- branching/selection among source-derived scripts when those branches are directly represented in source traces or selected by the shared retrieval interface;
- source-context checks, ordinary execution checks, safe stop/fallback, and exact or typed-key lookup over the same indexed evidence;
- a competent fixed compiler/authoring procedure and ordinary engineering needed to fit the common interface.

**Minimum construction recipe for a future R1 instantiation:** (1) normalize each permitted source trace into the shared typed event schema without adding latent state features; (2) identify only exact repeated actions/subsequences and losslessly deduplicate or compress them; (3) align trace steps by a fixed, frozen sequence/operation rule; (4) replace a literal argument/effect field with a typed slot only when the same declared field/type correspondence reconstructs the observed source instances; (5) retain all other constants and source pre/post checks; (6) form branches only from branches actually recorded in source traces, with shared retrieval used to select among templates; and (7) at invocation, bind slots from permitted current observations using deterministic unique field/type rules, replay the script with recorded checks, and abstain on ambiguity or mismatch. Expected-effect fields are carried through the same slot map for predictions. Compression choices may be selected by a source-only criterion such as exact representation size, never target/evaluator performance. This is an admissible reproducible recipe, not a claim that it is the only competent replay implementation.

R1 may not learn or store an explicit cross-context state/action/effect invariant, a generalized applicability boundary from counterexamples, or an outcome-conditioned activation rule. It may not infer a novel effect relation from target outcomes. Applicability may use source-context keys, exact recorded checks, fixed schema/type checks, and fixed typed slot-binding rules. It may generalize literal IDs through declared type/field/position substitutions and apply to new contexts where those rules resolve unambiguously; this is required to avoid reducing R1 to exact replay. It abstains when a slot is ambiguous, a required literal/check fails, or the context falls outside the fixed rules. A simple schema-based binding or efficient search is allowed and must be disclosed, because forbidding useful parameterization would straw-man replay.

For the predictive endpoint, R1 must implement the same frozen prediction interface as I0. It may emit only the source trace's recorded expected effect, or a value obtained by applying its declared slot substitutions to that recorded effect at the aligned script step. If no source effect aligns or a required field cannot be rebound by the fixed rules, it abstains. It cannot synthesize a new cross-context relation or target outcome. Every emitted prediction is frozen before the target action/result and linked to its source trace/effect under P2.

R1 must be given the same information, context, source event access, shared retrieval interface, model access, and development opportunity as the treatment. Its stored executable may be operationally equivalent to an invariant skill; do not relabel it after observing results. If R1 functionally matches the invariant treatment, that is evidence against an invariant-specific increment, not a baseline defect.

**Competence review:** before any future authorized evaluation, a reviewer not responsible for the invariant treatment checks that R1 implements the allowed compression, slot rebinding (including new literal IDs where type/field rules permit), source-script retrieval, prediction interface, and control-flow envelope; that no unnecessary limitations were added; that its artifacts and costs are logged; and that it contains no learned invariant/counterexample boundary. The algorithm, reviewer qualifications, artifacts, and disposition must be documented and frozen. P3 itself performs no such review or build.

### I0 — Invariant representation, counterexample boundary frozen (P3 Claim N treatment)

A versioned CandidateVersion/SkillVersion under P2: explicit typed state/action/effect relation, parameter mapping, observable applicability predicates, prospective effect prediction, policy and fallback. It is constructed only from the same permitted source corpus and frozen before target outcomes. The counterexample-based boundary update factor is disabled or frozen identically across comparisons; do not use target outcomes to revise it.

### I1 — Invariant plus counterexample boundary updates (separate factor)

Optional later arm for Claim B only. It differs from I0 only by the predeclared, permitted counterexample-based update procedure. It is not needed to estimate Claim N and must not be used to attribute a Claim N effect to invariant semantics. P3 does not specify the counterexample algorithm or authorize the evidence needed to run it.

### N0 — No learned skill (optional reference)

May be retained as a descriptive task-performance reference. It is not the primary comparator for Claim N and cannot replace R1.

## 4. Common evaluation and information controls (P3.3)

For every primary R1-versus-I0 comparison:

1. Use identical source events, source cutoff, observation and action schema, state normalization version, permitted context fields, and access manifest. Count source bytes/events and any annotation or preprocessing supplied to each arm.
2. Use the same model/checkpoint and access to calls/tools. If one arm uses no model for a component, report that fact; do not give it a hidden extra model, prompt, or adaptation budget. Freeze prompts, retrieval features, top-k/candidate handling, tie rules, and indexes; charge calls/tokens/latency to the relevant cost category.
3. Present identical decision-time observations/history and a common outer context/retrieval interface. All arms implement the same `PredictionRecord` target/output interface and return a prediction or explicit abstention; R0/R1 may only transport aligned source effects, while I0 uses its pinned relation. Freeze predictions before the target action/result per P2. Do not expose target labels, evaluator outcomes, hidden states, future events, or post-hoc split labels to any arm.
4. Evaluate on the same permitted target contexts with the same evaluator/version and logging. Pair contexts/episodes only where the environment and rules permit a legitimate shared initial condition. Do not assume arbitrary state forking or reset. If exact pairing is unavailable, use the predeclared independent/blocked unit and state that uncertainty increases; no action-level pseudo-replication.
5. Freeze arm order/randomization, seeds, reset/retry policy, timeout, stop/fallback behavior, and missing-data rules before evaluation. Log all assigned units, including abstentions, errors, timeouts, and failed episodes.
6. Keep treatment boundaries, retrieval and action interfaces identical. Any unavoidable difference is logged as a confound; if it could explain the apparent increment and cannot be isolated, Claim N is inconclusive, not supported.

## 5. Budget-matching contract

Treat resources as a vector, not a weighted score. The following conditions are required, with exact numeric caps left `UNSET` for a separately authorized protocol.

| Dimension | Matching rule | Required record | If exact match is infeasible |
|---|---|---|---|
| Source information | Identical permitted source-event manifest, event cutoff, source labels/annotations, schemas, and access rights. | Manifest digest, event/byte counts, preprocessing and provenance. | Do not claim matched-information Claim N; explain the asymmetry and classify comparison as descriptive/inconclusive. |
| Model and tools | Same model/checkpoint, tool versions, availability, call opportunity and instruction regime. | Model/config/prompt/tool hashes, calls, tokens, tool events. | Freeze a common interface and disclose remaining mismatch; if it changes task competence, no clean Claim N conclusion. |
| Context/input | Same observation fields, history length, resolution/encoding, context window and per-decision input. | Input bytes/tokens/frames, truncation, history and prompt logs. | Predeclare a cost frontier; no post-outcome choice of a favorable point. |
| Memory/storage | Same maximum persistent storage and retrieval-index capacity, including metadata/code/embeddings/caches. Report actual bytes and amortization separately. | Artifact/index hashes, allocated cap, actual bytes, cache policy. | Report outcome-versus-storage frontier for every predeclared cap; overflow is retained as failure/infeasibility, not silently compressed after results. |
| Retrieval | Same source corpus/index inputs, query features, top-k/candidate budget, latency/compute allowance and wrapper, except the named representation-specific semantic gate. | Query, candidates, selected artifact, latency, bytes and computation. | Explicitly decompose retrieval from representation; do not ascribe a retrieval-only gain to invariants. |
| Construction/validation | Same source evidence and declared model/tool access; account separately for manual/automated construction, review and validation resources. | Creation and validation cost by actions/tokens/wall-time/compute/labor where measurable. | Report resource vector and curve; do not omit treatment creation cost or grant R1 an undocumented inferior build process. |
| Invocation compute/time | Same per-decision and per-episode compute/wall-time limits and accounting method. | CPU/GPU/compute units, wall time, calls, timeouts, retries and fallback. | Predeclare common caps or a full resource frontier; an unmatched comparison cannot support a matched-budget claim. |
| Actions | Same action cap, action schema, retry/undo/reset permissions, stop conditions and fallback accounting. | Attempted and accepted actions, retries, invalid actions, abstentions and progress. | Do not select the comparison after seeing action counts; report separate action-efficiency outcomes and mark budget mismatch. |
| Evaluation | Same target manifest, evaluator version, assignment/ordering policy, observation points and missingness rules. | Cohort/permission manifest (when authorized), assignment, evaluator and audit logs. | If outcome exposure, assignment, or evaluator differs, treat as confounded/inconclusive; no leakage repair by retrospective exclusion. |

Matching means identical information and equal declared caps/opportunities, not necessarily identical realized consumption. Report both caps and actual use. No padding to equalize artifact sizes. Report creation, validation, invocation, and total costs separately; never collapse them into SCV or another composite. The allowed cap values, amortization horizon, acceptable residual mismatch, and frontier-selection rule remain open until P5 and separate authorization.

## 6. Ablation and comparison matrix

| Contrast | What it isolates | Interpretation limit |
|---|---|---|
| R0 vs R1 | Gain from compression, retrieval/selection, typed slots and ordinary replay engineering beyond exact fixed-trace playback. | Does not establish invariant value. |
| R1 vs I0 | **Primary Claim N contrast:** explicit invariant representation beyond strong trace-derived replay at matched resources, with counterexample boundary updates held fixed. | Any unmatched input, retrieval, wrapper or cost dimension makes the causal attribution weaker/inconclusive. |
| I0 vs relation-stripped I0 | Whether the explicit relation/prediction/applicability semantics change behavior when wrapper, slots, retrieval, policy interface and budgets are retained as far as possible. Replace only the invariant relation with the frozen R1-compatible trace representation. | If stripping the relation also changes the policy/interface/capacity, the ablation does not isolate semantics. |
| I0 vs I1 | Counterexample boundary contribution (Claim B), not Claim N. | Requires an independently specified/frozen counterexample protocol; do not pool this contrast into N. |
| N0 vs each active arm (optional) | Descriptive value of adding any learned/replayed procedure. | Cannot substitute for the R1 comparator or separate representation effects. |

No arm may receive extra target information. Ablation equivalence is judged by declared artifact/interface/resource differences, not by selecting only favorable outcomes.

## 7. Estimands and units

### Primary mechanism estimand — predictive value

For each eligible held-out decision context `j`, compare frozen target-effect predictions from R1 and I0 against the same separately stored observed effect. Report each arm's **coverage** (fraction of all contexts with a prediction) and **selective risk** (error among issued predictions), plus the paired coverage difference across the same contexts. Conditional risks may be directly contrasted only at the same prospectively declared operating point/common coverage; when coverage differs, a raw difference in selective risk is descriptive because the issued subsets may differ. If a scalar proper/decision loss with an abstention cost is selected later, its scoring rule and abstention cost must be frozen prospectively and reported alongside coverage. Calibration claims require a pinned calibration procedure under P2.

Let `A_mj=1` when arm `m` issues a prediction for target context `j` (and 0 for abstention/failure), and let `L_mj` be the predeclared loss for that prediction against the same observed effect. For arm `m`, coverage is `C_m = (1/n) Σ_j A_mj`; conditional risk is `R_m = Σ_j(A_mj L_mj) / Σ_j A_mj` when at least one prediction is issued. The paired coverage contrast is `ΔC = C_I0 − C_R1`. A risk contrast `ΔR = R_I0 − R_R1` is interpretable only at a shared, prospectively specified coverage/operating point; otherwise report arm-specific selective risks descriptively. If an arm issues no predictions, its risk is not estimable and must be reported as such. Conditional risk alone is not a claim: any support rule must prospectively specify acceptable coverage/non-inferiority and the scoring function.

The P3 direction is that prediction is the primary mechanism endpoint because Claim N concerns added state/action/effect representation, not only task success. Exact target variables, loss/scoring rule (including set-valued predictions), abstention operating point/cost, aggregation across contexts, acceptable coverage relation, and inferential procedure are explicitly `UNSET` for P5; no numerical margin is introduced here.

### Secondary behavioral estimand

For assigned task/episode `k`, let `Y_mk` be the predeclared task outcome and `ACTIONS_mk` the action count for assigned arm `m`. The intention-to-treat contrasts are `ΔY = E[Y_I0k − Y_R1k]` and separately `ΔACTIONS = E[ACTIONS_I0k − ACTIONS_R1k]`, over all assigned units, including abstentions, errors, and fallbacks. Report official task score/progress and action efficiency separately, with their own denominators and costs; do not combine them. Do not condition the main comparison on post-treatment applicability, invocation, or successful skill execution. Such conditional summaries may be descriptive only.

### Resource estimand

For each resource dimension, report the arm-wise cap and realized difference (storage, context/tokens, model/tool calls, creation/validation/invocation compute and time, actions, retries, and fallback). This is a vector of costs, not a composite outcome. A comparison is “matched” only for the predeclared dimensions/caps; extra budget cannot be excused by better score after the fact.

### Sampling and uncertainty

The unit is the held-out context for prediction and the assigned task/episode or justified paired block for behavior. Cluster repeated decisions/actions within a game/task. Estimate paired differences when valid pairing exists; otherwise use the assignment-level comparison and do not claim action-level independence. Exact cohort, sample size, randomization, uncertainty method, multiplicity control, missingness handling, minimum meaningful effect, and noninferiority margins remain `UNSET` for P5. These are not supplied by P3 and no split is assigned.

## 8. Interpretation and falsification rules

| Prospective pattern | Permitted conclusion |
|---|---|
| I0 improves on R0 but not R1 | No demonstrated invariant-specific increment; observed benefit is consistent with compression/parameterization/retrieval or ordinary engineering. |
| R1 matches or exceeds I0 on the primary predictive endpoint at comparable coverage and matched budgets | Claim N is not supported for the tested domain/conditions, even if both beat R0 or N0. |
| I0 has lower conditional prediction error only by abstaining more | No predictive advantage unless the predeclared coverage/abstention criterion is also met; report the coverage-risk trade-off. |
| I0 improves predictive endpoint but not behavioral outcome | Report predictive increment only; do not claim end-to-end or action-efficiency benefit. |
| I0 improves behavior but not prediction | Report a behavioral difference, but invariant-specific causal attribution remains unestablished until relation ablation and confounds support it. |
| Relation-stripped ablation matches I0 | The explicit invariant semantics have no demonstrated incremental role under that ablation. |
| Apparent gain vanishes at equal caps or depends on extra data/model/context/actions | Claim N is unsupported under matched resources; report resource-conditioned descriptive result only. |
| Data, retrieval, model, evaluation, or outcome leakage differs materially; baseline is not competent/frozen | Comparison is invalid or inconclusive; do not interpret as support or falsification of the underlying mechanism. |

Core falsifiers: strong replay matches/beats the invariant treatment; gain disappears under matched budgets; relation ablation is equivalent; gain is only a better macro/parameter binder with no predictive increment; effects occur only on source contexts; or any apparent benefit depends on target outcomes, post-hoc thresholds, exclusions, or baseline tuning. If an endpoint/operating point was not frozen, report it as exploratory and do not choose a favorable one retrospectively.

## 9. Unresolved questions (explicit P3 outputs)

- Which permitted source-event manifest, representation/normalizer versions, task family, and target population would be eligible in a future authorized study?
- Which concrete compression/parameterization/retrieval compiler instantiates R1, and who qualifies as an independent competence reviewer?
- Which source-context keys, slot correspondence rules, and binding ambiguities are allowed without crossing into learned invariant semantics?
- What are the permitted model/checkpoint, prompt/tool regime, exact memory/context/compute/action caps, and construction-cost amortization horizon?
- Can valid paired contexts, resets, or counterfactual branches be obtained under actual environment/rules, or must the unit be episode-level?
- What prediction targets, loss/scoring rule, abstention cost/operating point, behavioral endpoints, and task aggregation are meaningful and frozen before outcomes?
- What cohort size, assignment/ordering, uncertainty/multiplicity procedure, minimum meaningful effect, and acceptable residual budget mismatch are justified?
- How will source labels, target outcomes, evaluator results, and audit/access manifests be stored and independently checked?

These choices are deliberately not guessed. P3 closes the conceptual control design but cannot support an empirical conclusion until P5 resolves applicable protocol choices and the existing authorization/data-integrity gates are satisfied.

## 10. Design-only conformance checklist

A future protocol is not ready to claim Claim N unless it can answer yes to each item prospectively:

- R0, R1, I0, and any optional arms have immutable, unambiguous definitions and versioned artifacts.
- R1 has a documented competence review and is not intentionally weakened; it has the same source corpus, model, retrieval, input, and budget opportunities.
- The invariant relation and its target effects are explicit; the relation-stripped ablation changes only the intended factor as far as possible.
- Counterexample-boundary learning is held fixed for Claim N and isolated for Claim B.
- Source and target manifests, outcome separation, assignment, evaluator, units, metrics, and resource caps are frozen before target outcomes.
- Abstentions, failures, timeouts, and all assigned units are retained; coverage accompanies prediction risk.
- Budget mismatches, cost accounting, uncertainty, missingness, and falsifiers have prospective rules.
- No hidden/test/confirmatory outcomes or post-hoc threshold/baseline changes inform the methods.
- All approvals and data-access permissions come from existing controlling gates; this P3 document grants none.
