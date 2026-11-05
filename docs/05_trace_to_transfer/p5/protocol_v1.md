# T2T-P5 Experimental Protocol Proposal

**Protocol ID:** `T2T-P5-Protocol-v1.0.0-draft`  
**Status:** complete for design/documentation scope, 2026-11-04.  
**Implementation status:** no code/tooling implemented; the user selected design-only scope.  
**Authorization:** not a preregistration, split assignment, experiment/benchmark/run approval, or permission to access restricted outcomes. Existing project/data/competition gates remain controlling.

## 1. Purpose and claim/evidence ceiling

This document proposes a future ARC-AGI-3 study whose arms and measures separately address Claims A, N, B, C, D, and E in the [claim-evidence map](../../../reports/competition/arc_prize_2026_claim_evidence_map_v1.md). It integrates the controlling [P2 skill-object contract](../formal_skill_object.md), [P3 fair replay contract](../p3/fair_replay_controls_v1.md), and [P4 boundary algorithm](../p4/boundary_algorithm_v1.md).

The study is **not run-ready**. There is no authorized task cohort, split, budget, MME, sample size, alpha, or score access. No hidden/test/confirmatory data or target outcomes have been inspected for this proposal. P1's rejection of standalone mechanism novelty remains; the comparative reframe is provisional and not novelty-cleared. The current evidence ceiling in `current_evidence.md` controls: P2–P5 documents, synthetic results from other phases, and contract checks are not ARC-AGI-3 support.

## 2. P5.1 — Claim-specific arms and estimands

### 2.1 Arm registry

One common base agent/harness, observation/action interface, evaluator and permitted source-event policy is used. Arm names follow P3/P4. Candidate-generation arms are distinguished from runtime decision arms. These are protocol slots, not implemented agents. Under P2, a `CandidateVersion` is non-executable; only an authorized, frozen `SkillVersion` may execute. I0/I1 refer to such future skill versions, not runnable artifacts created here.

| Arm | Definition | Role |
|---|---|---|
| `B0` — No learned skills | Base agent with no T2T-derived or replayed skill library; all other model/harness settings matched. | Reference for any learned/replayed capability and one Claim E comparator. |
| `R0` — Raw replay | P3 exact ordered fixed-trace replay; mismatch stops/abstains. | Weak diagnostic control; never the sole Claim N comparator. |
| `R1` — Strong replay | P3 competent source-trace compression/retrieval/typed-slot baseline with aligned-effect prediction interface; no learned cross-context invariant boundary or CE refinement. | Required primary Claim N comparator and Claim E baseline. |
| `Grec` — Simple recurrence generator | Frozen non-invariant recurrence/motif miner over the same permitted source traces; it may emit trace/macro candidates but not P2 invariant semantics. | Candidate-generation comparator for Claim A; its exact algorithm must be frozen and reviewed before any future run. |
| `I0` — Invariant, boundary fixed | P2 invariant skill derived from `Ginv`, with counterexample-driven boundary update disabled/frozen. | Primary Claim N treatment; comparison control for B/C. |
| `I1` — Invariant + counterexample boundary | Same candidate-generation evidence and skill representation as I0; only the P4-defined counterexample-boundary information/update is enabled. | Full-method treatment; primary Claim B/C factor and Claim E treatment. |
| `I−rel` — Relation ablation | I0 wrapper/policy/parameters/interface retained as far as possible, with explicit relation semantics replaced by the frozen R1-compatible trace representation. | Mechanism ablation for N; not a separate efficacy claim. |

No arm can receive extra target context, hidden information, model calls, or action opportunity. Exact implementation artifacts, model/checkpoint, prompt, retrieval index, and costs must be hashed/frozen before future target evaluation. If an arm cannot be specified or fairly budgeted, do not silently substitute another arm; mark the affected claim `NOT_TESTED` or `INCONCLUSIVE` before outcomes.

### 2.2 Claim-to-contrast and primary estimand table

| Claim | Primary contrast | Primary estimand and unit | Required interpretation |
|---|---|---|---|
| **A — Candidate generalization** | `Ginv` vs `Grec` on identical permitted source experience; candidate-level held-out prediction assessed for every proposal, including rejects/abstentions. `R0`/raw storage is descriptive context. | Difference in held-out relation/effect-prediction quality at reported coverage, clustered by source/target game or episode; candidate yield is secondary, not proof. | Existing motif frequency or a constructed CandidateVersion is not success. Require a frozen nontriviality/held-out criterion; no support threshold is invented. |
| **N — Invariant value beyond replay** | `I0` vs `R1`, with counterexample updates fixed; `R0` is diagnostic, `I−rel` isolates semantics. | P3 predictive coverage/selective-risk contrast at a predeclared common operating point or a scoring rule that charges abstention; unit is held-out decision context, clustered within game/episode. Behavioral ITT is secondary. | Raw replay alone is insufficient. If R1 matches or beats I0 at matched resources, N is not supported under those conditions. |
| **B — Counterexamples improve scope** | `I1` vs `I0`; candidate generator, source traces, representation, compute, policy wrapper and target contexts otherwise fixed. | Difference in scope false-activation/error rate together with coverage/abstention on independently adjudicated held-out contexts; unit is the decision context, clustered by game/episode. | A lower false-activation rate obtained by suppressing almost all use is not improvement; report coverage separately and do not create a composite. |
| **C — Better boundary reduces harm** | `I1` vs `I0` under the same assigned task/episode set; compare full event rates and categories. | Intention-to-treat difference in probability of any predeclared harmful-transfer event per assigned task/episode; also report each harm category and invocation-conditional rate descriptively. | Never infer safety from low invocation or condition the causal estimate on actual invocation. A harm event requires predeclared local evidence/attribution under P4. |
| **D — Reduced harm improves efficiency** | `I1` vs `I0` and appropriate common baseline(s), with same task/episode assignment and resources. | Separate ITT contrasts in official task score/progress and actions to progress/completion per assigned unit; game/episode is the unit. | Fewer harmful events do not establish improved action efficiency. Score and action use are separate endpoints; a future regression/noninferiority rule must be frozen. |
| **E — Full method at acceptable cost** | `I1` vs `B0`, `R0`, `R1`, and `Grec`/simple recurrence, with the full method and each baseline frozen and budgeted. | Official ARC-AGI-3 evaluator score over the full assigned cohort (ITT, game/episode unit); total cost is a vector reported beside it. | Must beat meaningful baselines under the predeclared score rule and cost guardrails. No composite score or reuse count substitutes for official outcomes. |

For Claim A, both generators are evaluated through the same frozen prediction/abstention interface on the same eligible held-out contexts: `Grec` may transport only aligned source effects under P3, while `Ginv` uses its pinned P2 relation. Report every proposal, including no-prediction/rejected cases, with counts clustered by source/game; candidate count/yield never substitutes for prediction quality.

A study may have several claim-specific contrasts but only one primary estimand per claim. Secondary mechanism/cost measures are reported separately. Claim A or N success does not imply B; B does not imply C; C does not imply D; and none imply E. If a prerequisite claim is unsupported, report later links as untested or inconclusive rather than inferring them.

### 2.3 Assignment and estimand principles

- Use intention-to-treat (ITT) as the primary task-level comparison: analyze every unit assigned to an arm, including abstentions, timeouts, fallback, invalid actions and failure to produce a candidate/skill.
- Where legal and technically valid identical starts exist, use paired/blocked assignments and analyze at the paired game/episode level. Do not assume a state fork or use arbitrary hidden state. Otherwise randomize or block whole permitted games/episodes under a prospectively frozen allocation procedure.
- Skill invocation, applicability, candidate acceptance, and successful execution are post-assignment events. Invocation-conditional results are descriptive/mechanistic, not substitutes for ITT.
- The unit is a game/episode or justified independent block. Actions, predictions within a game, candidate rows from one trace, and multiple levels of one episode are clustered/repeated observations, not independent samples.

## 3. P5.2 — Permitted data, cohort, and budgets

### 3.1 Data-role separation

Use an immutable, track-specific data manifest and prospective role assignment. No actual task IDs, split labels, hidden data refs, or answer-bearing artifacts are present in this P5 proposal.

| Role | Permitted use | Separation rule |
|---|---|---|
| **Source/formation** | Build R0/R1/Grec/Ginv artifacts and source evidence under the approved access policy. | Same source event manifest/cutoff and labels to compared arms; outcomes are source evidence only, not target confirmation. |
| **Development/refinement** | Revise candidates/guards only when separately permitted; P4 roles and append-only successor rules apply. | Every event used for refinement is ineligible as held-out validation for that successor and descendants. Do not silently reuse it. |
| **Validation** | Assess a frozen candidate/skill and tune only prospectively permitted design choices if authorized. | Prediction/version frozen before outcome. If reused for successor refinement, append role change and it ceases to validate that successor. |
| **Confirmatory/target** | Evaluate only frozen arms/metrics under a future separate authorization. | No target outcomes in candidate/baseline construction, thresholds, prompts, arms, or exclusions. Keep evaluation outcomes separate. No split assigned here. |
| **Restricted/hidden/test** | No method construction, refinement, or tuning access. Any official evaluator access requires the controlling existing authorization and rules. | Do not open, inspect, scrape, label, or expose these outcomes to the agent or analysis before authorized evaluation. |

The minimum manifest fields to be frozen later are: project/track and source system; dataset/task/game version and license/access class; artifact/event IDs and hashes; role/purpose and allowed fields; episode/reset boundaries; source and target relationship; representation/normalizer and evaluator versions; model/tool/config versions; annotator/label provenance; leakage checks; assignment block/seed fields when authorized; exclusions and reasons; and owner/access approvals. The template has no populated task/split identifiers.

P2/P4 evidence uses the corresponding `EvidenceSnapshot.purpose`; P4 fine-grained `REFINEMENT_FOR_SUCCESSOR` use is append-only. Do not pool ARC-AGI-2, synthetic, Phase 13/14, or unrelated results with ARC-AGI-3 endpoints. Such results may inform design only when their provenance and non-transfer limits are explicit.

### 3.2 Eligible target cohort and units (criteria only)

The intended target population is the complete prospectively declared set of permitted ARC-AGI-3 game/episode units that can be evaluated under the official track contract, with a declared source/target separation and no restricted answer exposure. Eligible game/episode IDs, exact cohort size, evaluation date, and split assignment are `UNSET` and intentionally absent. Before any future authorization, freeze:

1. the track and official evaluator/output contract;
2. which games/episodes are legally and operationally available for research evaluation;
3. source/target disjointness criteria at task-family/generating-rule level where known (not merely random item separation from the same known template);
4. episode and reset boundaries, persistence of memory/library across games, and cross-game feedback availability;
5. legal repeat/paired-start/reset rules; and
6. task order, assignment blocks, and the full attempted-unit denominator.

No game is assumed to be forkable or resettable. If same-state pairing is disallowed or infeasible, the estimand is episode/game-level under randomized/blocked assignment; do not claim a within-state counterfactual. Any cohort exclusions must be made by manifest/eligibility rules before outcomes; later access or integrity violations are reported, not hidden by replacing tasks.

### 3.3 Resource and environment matching

Use the P3 resource vector. All exact limits/caps are `UNSET` pending an approved, track-specific protocol. Match declared opportunities and record realized use for:

- permitted source events/bytes, annotations, preprocessing and model-training exposure;
- model/checkpoint, prompts, decoding, tools, retrieval inputs/top-k/index, candidate/context windows and observation history;
- persistent memory/storage including code, metadata, indexes, embeddings and caches;
- construction, validation, invocation and adjudication resources (tokens/calls, CPU/GPU/compute, wall time, storage);
- environment actions, retries/undo/reset permissions, per-episode step/time/compute caps and fallback reserves; and
- evaluator version, observation schedule, game order, seeds, initialization and failure handling.

Equal declared caps do not imply equal realized use. Report both; no padding, uncharged tool call, hidden retry, or extra treatment budget. If a component cannot be matched, specify a prospective resource frontier and its full costs before evaluation; if residual differences plausibly explain the outcome, the comparison is confounded/inconclusive. Model and environment state must be isolated across arms to prevent library or outcome contamination.

## 4. P5.3 — Outcomes, metrics, and denominators

### 4.1 Claim-specific outcomes

1. **Official task outcome (D/E):** official ARC-AGI-3 evaluator score/result, evaluator version, game/episode progress/completion; report per-unit raw values and official aggregate. No in-house score replaces it.
2. **Candidate generalization (A):** number of candidates proposed/accepted/rejected/held; candidate support contexts; and held-out effect prediction coverage/error for every eligible candidate, including failures/abstentions. Candidate yield alone is not evidence.
3. **Prediction quality (N):** prediction coverage `# contexts with a frozen prediction / # eligible assigned prediction contexts`; selective risk/error among issued predictions; and either risk at a prospective common coverage or a prospectively specified loss that accounts for abstention. Report unknown/invalid predictions separately. Probability metrics require P2-pinned calibration; no calibration is presumed.
4. **Boundary quality (B):** on separately adjudicated contexts, report admitted/applicable count, false activation (`admitted` but reliable local behavior violates the frozen effect contract), false rejection where ground-truth applicable contexts can be independently established, unknown/abstention count, coverage, and denominator for every rate. Do not collapse precision, recall, coverage, and abstention into a custom boundary score.
5. **Negative transfer (C):** P4-classified harm categories separately: dynamics/scope mismatch with consequence; avoidable wasted/invalid actions; lost progress; fallback or recovery burden; and lower matched task outcome when causally interpretable. Report (a) any predeclared harm event per all assigned units (primary ITT denominator), (b) each category per assigned unit, and (c) harm per invocation as a descriptive mechanism rate. A final score difference alone is not automatically a local counterexample.
6. **Action efficiency (D):** attempted/accepted actions to progress/completion, invalid actions, retries, fallback/recovery actions, levels/progress, and time/compute. Report per assigned unit including failures/timeouts; do not report only successful completions.
7. **Cost vector (all claims):** candidate creation, review/validation, storage, retrieval, model calls/tokens, CPU/GPU/compute, wall time, environment actions, fallback/recovery and total resource ledger, with units and missingness. Keep components separate; no SCV or weighted cost composite.

### 4.2 Failure, missingness, and denominator ledger

Retain a flow table for every stage: eligible source traces; considered alignments; candidate proposals; candidate holds/rejections; skill versions; eligible invocations; applicable/reject/abstain decisions; predictions issued/unknown; assigned task/episodes; attempted episodes; completed/failed/timeouts; fallback events; and valid evaluator outputs. Every count has its own numerator/denominator and provenance.

Abstention, no proposal, invalid action, crash, timeout, mismatch, quarantined version, missing prediction, and fallback are outcomes—not reasons to erase a unit. Keep unknown, unresolved, and unassessed outcomes distinct from false predictions or false boundary decisions. Evaluate each pre-action `PredictionRecord` separately from later observed effect assessment; predictive correctness does not itself establish a skill effect. Preserve P4 fine-grained triage detail while mapping it only through P4's documented mapping to P2's existing coarse counterexample enum—do not add or reinterpret coarse labels. Report missing evaluator values as missing, give reason-coded rates, and use only a prospectively specified sensitivity/bounds method. No post-hoc imputation or completion-only denominator.

## 5. P5.4 — Analysis, uncertainty, exclusions, and falsifiers

### 5.1 Estimation and uncertainty proposal

- For valid paired starts, estimate per-game/episode paired differences; otherwise estimate arm-level ITT differences under the authorized blocked/randomized assignment. Report absolute values, contrasts, denominators, and per-game distributions.
- For repeated contexts/actions/candidates within a game/episode, use a cluster-level resampling/uncertainty unit at game/episode (paired resampling where valid); never resample actions as independent observations. The exact interval confidence level, number of resamples, random seed, small-sample method, and fallback inference method remain `UNSET` for preregistration.
- Report point estimates and uncertainty intervals for all primary endpoints. If assignment is not randomized or pairing assumptions fail, qualify causal language and report an associational/descriptive estimate instead.
- The primary contrast and direction for each claim are those in §2.2. Exact score/loss, common-coverage operating point/abstention cost, aggregation, and confidence method must be frozen before outcomes; P5 does not choose them.

### 5.2 Multiplicity and claim hierarchy

Predeclare one primary estimand/contrast per claim and a finite confirmatory family. Proposed multiplicity control is Holm family-wise adjustment across all primary claim-level contrasts designated confirmatory; the family composition and alpha are `UNSET` and must be frozen before data access. Where Claim E requires several baseline comparisons, include all required contrasts in the family—do not select the easiest baseline after results. Secondary endpoints are descriptive unless separately included in the frozen family. No switching endpoints or promoting an exploratory outcome after inspection.

The claim chain is gated: A and N are prerequisites for an invariant-value interpretation; B is needed for a counterexample-boundary claim; C for harm-reduction; D for an action-efficiency link; E for full-method superiority. Failure or inconclusiveness upstream limits downstream claims; no substitution from official score or reuse count.

### 5.3 Minimum meaningful effects, sample size, and regression margins

For each primary claim define `delta_min_claim`, any score noninferiority/regression margin, harm tolerance, and acceptable cost bounds before confirmatory evaluation. **Every numerical value is `UNSET`.** Justify them by task/user relevance and independent review, not observed treatment effects or variance from the confirmatory cohort. Determine sample size/power from those frozen estimands, eligible independent game/episode counts, and permitted prior variance information; **sample size and power target are `UNSET`**. If the approved cohort cannot support the claim-specific precision/power, label the result exploratory/inconclusive; do not lower margins or switch units.

### 5.4 Exclusions and protocol deviations

- Freeze eligibility and exclusions in the manifest before assignment/outcomes. Pre-assignment exclusions are limited to documented ineligibility, invalid/missing artifact/permission, duplicates under the frozen rule, or evaluator/environment incompatibility.
- After assignment, retain every unit in ITT. Protocol faults, crashes, timeouts, no candidate, abstentions and fallbacks remain in the denominator. Do not exclude based on score, invocation, mismatch, or method failure.
- A data-integrity/access breach, hidden-outcome leak, arm-version mismatch, or evaluator mismatch triggers a labeled protocol violation and may invalidate the affected confirmatory analysis. Preserve the record and report the violation; never replace the unit silently.
- Any adjudicated exclusion or missing outcome carries a blinded reason code, provenance and sensitivity result under the frozen method. No exclusion decision may depend on a favorable/unfavorable result.

### 5.5 Falsifiers and stop rules

**Claim-level falsifiers** follow the claim map and P2–P4 contracts:

- A: candidates remain source-specific, fail held-out effect prediction, or do no better than recurrence/replay controls.
- N: R1 matches/beats I0 at comparable coverage and matched resources; relation ablation matches; or all gains are explained by compression/parameterization/retrieval.
- B: counterexample access does not improve boundary error at comparable coverage, or apparent improvement comes from abstaining on nearly everything.
- C: harmful-transfer incidence does not fall, or decreases only because the method rarely invokes/abstains, or harm reduction is offset by loss of useful coverage.
- D: the predeclared action-efficiency endpoint does not improve, or score/regression costs exceed the prospectively frozen guardrail.
- E: full I1 does not outperform the required baseline family under the frozen official score/cost rules, or the implemented submission does not contain the described mechanism.

**Immediate stop/hold conditions:** unauthorized or restricted data/outcome access; manifest/hash/permission failure; post-outcome candidate/baseline/threshold edit; missing pre-action PredictionRecord where required; unbudgeted action/retry/model call; arm/model/evaluator/version mismatch; invalid reset/pairing; uncontrolled cross-arm memory contamination; resource-cap breach; tool/environment failure that prevents valid measurement; safety-relevant unexpected behavior; or incomplete audit logs. Stop affected activity, quarantine artifacts/data as required, preserve all logs, and seek the existing gate/review before any restart. A restart requires an approved new protocol/version and cannot reuse a result as untouched confirmation.

No efficacy/futility peeking or early success stop is proposed. If a future protocol requests interim analysis, it must define an independent monitor and prospective sequential error-control rule before outcomes; until then, no interim claim-driven stopping or adaptation is permitted.

## 6. Freeze gate and required unresolved fields

This proposal is not ready for preregistration/run approval until all of the following are completed and separately authorized:

- protocol owner and independent reviewers;
- claim set and confirmatory family, per-claim `delta_min`, score/regression/harm/cost margins, alpha/confidence level, multiplicity map;
- sample-size/power justification and uncertainty implementation details;
- exact allowed source/target manifests, evaluator version, cohort eligibility, data roles, task-family separation and access permissions;
- arm code/artifact hashes, baseline competence review, candidate/skill/prediction/evidence schema versions;
- model/checkpoint, prompts/tools, environment/runtime, memory/context/retrieval/compute/action/time caps, and total resource accounting;
- reset/fork, assignment, randomization/blocking, order, seeds, contamination/isolation and missingness/exclusion procedures;
- prediction target, primary loss or common-coverage operating point, abstention cost, calibration rule, boundary adjudication, negative-transfer definitions and reporting denominators;
- stop/safety contacts, audit ownership, outcome storage separation and deviation review; and
- a separate written authorization for code, permitted data access, split assignment, or any run. This proposal supplies none of these approvals.

Exact split/task IDs are deliberately absent. All numerical thresholds/sample size/caps that govern study conclusions remain `UNSET`; no result-based tuning is allowed.
