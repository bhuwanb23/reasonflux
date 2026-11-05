# P4 Counterexample-Guided Boundary Algorithm

**Contract ID:** `T2T-P4-Boundary-v1.0.0-draft`  
**Status:** complete for documentation/design scope, 2026-11-04.  
**Authority:** documentation only. This is not code, an implementation, candidate/skill-generation result, experiment, benchmark, ARC run, split assignment, or access approval.

## 1. Purpose, dependencies, and invariant rules

This contract specifies a deterministic procedure, conditional on pinned configuration, for proposing candidates from permitted traces, triaging mismatches, proposing boundary changes, and failing closed at runtime. Its normative inputs are the [P2 formal skill-object contract](../formal_skill_object.md), the [P2 JSON Schema](../p2/schema_v1.json), and the [P3 fair-replay/Claim N controls](../p3/fair_replay_controls_v1.md). The root-level [algorithm sketch](../counterexample_boundary_algorithm.md) is an overview of this version.

The P1 standalone-novelty no-go and comparative reframe remain in force. P4 does not claim that this mechanism is novel or useful. All CandidateVersion and SkillVersion records remain distinct: candidate generation emits **non-executable hypotheses only**; no trace, motif, macro, prediction, or counterexample record is silently promoted to a skill. A successor semantic version is immutable; all edits append new versions and decision events.

### Determinism and fail-closed configuration

The algorithm is deterministic **given** immutable inputs and a fully pinned configuration. Required pins include source-manifest/access policy, state/action/effect representation, normalizer, relation/predicate language and template inventory, structural-alignment rule, identity/hash profile, taxonomy, lifecycle policy, and resource/fallback policy. If a required reference, permission, or rule is missing, ambiguous, or `UNSET`, the relevant stage returns `BLOCKED_UNRESOLVED` / `HOLD` / `ABSTAIN`; it never fills a default or invents a threshold. P2's exact canonical hash/ID profile and P2/P5 numeric evidence, support, promotion, and runtime thresholds remain open; the algorithm may not claim executable readiness until required profiles are supplied by a future authorized protocol.

Tie handling is deterministic and conservative: stable IDs and event indexes order records; all structurally distinct maximal alignments are retained; ambiguous correspondence is marked `UNKNOWN` rather than resolved by a favorable guess. Exact relation operators, ontology, domain-level adjudication policy, support thresholds, and action/compute caps are not selected here.

## 2. Versioned inputs, outputs, and data-use boundary

### Inputs

1. **Permitted source manifest:** immutable list of source trace/event refs, access class, source purpose, context/run IDs, event ordering, provenance, and raw observation refs. Only `PERMITTED_SOURCE` evidence may enter candidate formation or contradiction review. A broken permission/reference check blocks the pipeline.
2. **Representation bundle:** pinned normalizer and typed state/action/effect schemas. Original observations remain immutable; normalized fields are derived artifacts linked back to them. `UNKNOWN`, missing, occluded, conflicting, or malformed values are never treated as wildcards or `FALSE` by default.
3. **Relation-template bundle:** an already specified, versioned DSL/operator set and finite list of candidate templates, each with typed inputs, predicted effect, observable predicate vocabulary, and an explicit falsifier. P4 does not invent operators or infer hidden state.
4. **Algorithm configuration:** alignment rule, event eligibility and deduplication rules, proposal/audit format, taxonomy and lifecycle policy. The config is hashed/frozen before processing.
5. **Prediction and lifecycle records:** for mismatch triage only, a P2 `PredictionRecord` frozen before its target action/result, matching SkillVersion, append-only observations, execution/tool logs, and evidence refs.

### Outputs

- A deterministic **MotifAlignmentAudit-v1** for every considered alignment: `audit_id`, algorithm/config refs, ordered trace IDs and event-index ranges, signature/template refs, field correspondence map, alignment status (`UNAMBIGUOUS`, `AMBIGUOUS`, `INCOMPLETE`, `NO_MATCH`), alternate/tie refs, exclusions, and reason codes.
- Zero or more immutable **CandidateVersion** records, each with explicit relation/preconditions/falsifier, observed-context scope, permitted EvidenceSnapshot, and provenance, plus a separate genesis `LifecycleEvent` (`NOT_APPLICABLE → PROPOSED`). No mutable status field or executable policy is emitted.
- A **ProposalSupportLedger-v1** sidecar keyed by `candidate_version_id` in the immutable P4 proposal-run manifest. It stores the source/algorithm/config refs; raw occurrence count; unique event, trace, run, and context counts; counts and event refs by `SUPPORTS`, `CONTRADICTS`, `QUALIFIES`, `CONTROL`, `UNRESOLVED`; duplicate, excluded, incomplete, ambiguous, and unknown counts/reasons; and derivation time/order. The run manifest pins the algorithm config and source manifest; the sidecar is linked by version ID rather than folded into the candidate digest, avoiding a circular hash. Counts describe evidence; they are not promotion thresholds or independent-trial claims.
- For each eligible mismatch, an immutable **TriageAssessment-v1** sidecar with the diagnostic subtype, evidence checklist, adjudication state, rationale, and linked prediction/observation/version refs. Its digest is recorded by the P4 classifier/provenance artifacts. The P2 `CounterexampleRecord.classification` stays within the existing P2 enum; detailed P4 subtypes live in the sidecar, not as unrecognized P2 fields.
- Append-only `CounterexampleRecord`, lifecycle/hold/quarantine/rejection decisions, and—only where policy permits—successor CandidateVersion/SkillVersion proposals. Existing records and versions are never edited.
- Runtime logs for applicability, prediction, action, mismatch, stop/fallback, and cost.

P4 sidecar names describe future data contracts only; none are created or executed by this documentation.

### Prohibited data uses and P2 purpose mapping

P2 `EvidenceSnapshot.purpose` remains unchanged: candidate formation uses `CANDIDATE_FORMATION`; mismatch triage and guard refinement use `CONTRADICTION_REVIEW`; validation is `FUTURE_AUTHORIZED_VALIDATION` only under separate authorization. Fine-grained evidence-use roles (`REFINEMENT_FOR_SUCCESSOR`, etc.) live in the P4 append-only use ledger/sidecars, not in new P2 enum values.

- Hidden/test/confirmatory answers and private leaderboard feedback are categorically unavailable for candidate construction, refinement, validation-threshold choice, or promotion. No future event is available at decision time.
- A permitted development/source observation may inform its designated construction/refinement role. A held-out validation outcome may assess only the immutable version frozen before it. If an authorized policy later permits reusing that event to refine a successor, append a new evidence-use event marking it `REFINEMENT_FOR_SUCCESSOR`; never count it as validation of that successor or its descendants. The original source/result record is not rewritten. This is the P4 rule preventing a target result from refining a version and then being counted as its held-out validation.
- A final level/game outcome is not a local dynamics/scope label by itself. Only a prediction frozen before the local event and the permitted local state/action/effect record can enter counterexample triage.
- Assign evidence roles prospectively. An event used to construct or refine a version cannot validate that same version or any semantic descendant. Refinement consumes that event for validation purposes; fresh, separately permitted evidence and a frozen future protocol are required.
- Source interactions may include observed transitions/effects because they form the allowed source experience. Keep observed records, predictions, triage, and evaluator outcomes distinct under P2/P3.
- Never remove a failure, duplicate, ambiguous alignment, abstention, or quarantined version to improve support or coverage. Preserve exclusions with reason codes.

## 3. P4.1 — Candidate generation

### 3.1 Preflight and normalization

For source manifest `M` and pinned config `C`:

1. Verify every manifest ref, permission, schema/normalizer version, source purpose, and content digest. If an event's access class is not `PERMITTED_SOURCE`, exclude it from this algorithm and record the exclusion; if the manifest as a whole cannot be trusted, halt.
2. Deduplicate only exact repeated `event_id`/content pairs. Reuse of an ID with differing content is an integrity failure and halts the affected trace. Preserve duplicate provenance; do not count duplicate copies as independent support.
3. Sort traces by pinned stable trace ID and events by source sequence/index (timestamp only as a logged cross-check). Preserve original data.
4. Apply the pinned normalizer to each permitted observation, action, and effect. Produce typed field paths and raw-to-normalized refs. A missing or uncertain field is tagged unknown with a reason; do not impute it.
5. Create a `TransitionView` only when the pre-state, executed action, post-observation/effect, and their provenance refs are linkable. Incomplete views remain in the audit but cannot provide positive support or a clean contradiction.

No automatic object identity, color/position interpretation, or game-specific meaning is inferred outside the pinned representation bundle.

### 3.2 Structural trace alignment

For each pair of traces in stable order, form one structural signature per `TransitionView`:

`Sig(t) = (representation_version, action_operator_ref, sorted(argument_path,type_ref), sorted(prestate_path,type_ref), sorted(effect_path,type_ref))`.

The state/effect paths are exactly the paths enumerated by the pinned relation-template inventory and the versioned schemas; no annotator chooses a new “relevant” field after seeing results. Values are not erased from the evidence ledger; the signature omits values only for locating possible typed correspondences. Any signature with a missing/unknown/malformed required path is ineligible for alignment; unknown does not match known or unknown and is retained in the audit. The relation-template bundle, not string similarity, determines which fields can later be variables.

Enumerate every **maximal common contiguous run** of equal signatures: test each pair of start indexes; extend while signatures match; retain a run if it cannot extend left or right. Keep all distinct maximal event-index correspondences, including ties and repeated occurrences. Do not greedily select whichever alignment yields the most favorable relation. If two or more alignments assign a source event to different slot correspondences, mark that motif `ALIGNMENT_AMBIGUOUS`; keep its audit and do not make a positive support assertion from the ambiguous mapping.

This exact structural rule is one deterministic, conservative baseline. More tolerant alignment (edit distance, embedding similarity, learned object correspondence, cross-game normalization) is not silently substituted; it requires its own pinned version, evidence ceiling, and prospective policy. The minimum motif size and cross-level/game recurrence policy remain unset. A one-context motif may be logged as a proposal hypothesis but must carry its observed scope/support count and cannot be called validated recurrence or promoted by P4.

### 3.3 Motif and candidate proposal

For every unambiguous alignment and every compatible template in the frozen relation-template bundle:

1. Match template inputs to normalized field paths only when path/type constraints are satisfied. Apply the template's fixed variableization rule: values at the same typed path may become a parameter only when the rule permits; otherwise retain them as constants. Never infer a latent relation because it happens to explain a target outcome.
2. Instantiate the relation over pre-state/action/effect fields. It must contain at least one typed state, action, and effect component, an explicit predicted-effect form, at least one proposed observable precondition (an explicit unconditional predicate is permitted only if the pinned DSL represents it), and a falsifier. If any field or the falsifier is unavailable, record a `MOTIF_ONLY` audit rather than a CandidateVersion.
3. Enumerate all compatible templates in stable template-ID order. Do not choose the best-looking template by target performance. A relation/parameter/template/profile mismatch creates no candidate and a reason-coded audit.
4. Search **permitted source evidence only** under the instantiated relation and preconditions. For each event, store one of `SUPPORTS`, `CONTRADICTS`, `QUALIFIES`, `CONTROL`, or `UNRESOLVED` with the relevant event and predicate refs. A positive support label requires known state/action/effect fields and a successful relation check. Unknown comparisons remain unresolved. Candidate formation evidence is not held-out validation.
5. Compute support ledger counts separately: total occurrences; unique event IDs; unique traces; unique run IDs; unique context IDs; support/contradiction/qualification/control/unresolved counts; duplicate events; incomplete views; ambiguous alignments; and unknown fields. Counts are not weighted into a score and are not evidence of statistical independence. Do not set a minimum support/promotion threshold in P4.
6. If the P2 identity/hash profile and all required record refs are pinned, emit a non-executable `CandidateVersion` with source-scope context refs, exact evidence snapshot, relation/template/representation refs, explicit falsifier, and provenance; append a separate genesis `LifecycleEvent` from `NOT_APPLICABLE` to `PROPOSED`. Link the Proposal Support Ledger through the versioned P4 run/provenance artifact. If the hash/identity profile is unresolved, halt candidate emission rather than fabricating a digest.
7. Apply no automatic acceptance, rejection, skill creation, or execution. Lifecycle remains `PROPOSED` until an independently frozen promotion policy acts. One or many source matches do not imply truth or eligibility.

The deterministic procedure yields the same proposal set and support ledger for the same manifests/configuration. If a later operator library, normalizer, template, tie rule, or source set changes, create a new algorithm/config version and record that this is a new proposal run.

## 4. P4.2 — Counterexample taxonomy and triage

### 4.1 Triage preconditions

A comparison can be evaluated only if a matching P2 `PredictionRecord` was frozen before the target action/result and identifies the exact SkillVersion, context, action, predicates, predicted effect, evidence snapshot, timestamp, and append order. If the prediction is missing, stale, edited, or ordered after the result, do not label a dynamics or scope counterexample; mark the record `OUTCOME_ONLY` or `AMBIGUOUS_UNRESOLVED` according to the P2 class and preserve an integrity reason.

### 4.2 Ordered diagnosis

Run these checks in order and record evidence for each; a failed/unknown check is not skipped:

1. **Permission/version integrity:** prediction, observation, and action records resolve to permitted sources and the invoked immutable version. Otherwise no scientific classification; isolate the record and block use pending integrity review.
2. **Observation reliability:** confirm required features are observable and correctly normalized under the pinned versions. Verified sensor/normalizer/perception fault maps to P2 `OBSERVATION_ERROR`; occlusion, conflicting values, or uncertain correspondence maps to `AMBIGUOUS_UNRESOLVED` with P4 subtype `OBSERVATION_UNCERTAIN`.
3. **Execution fidelity:** compare commanded action, dispatched action, accepted action, and tool/environment result. A missing, altered, invalid, or failed action maps to `EXECUTION_ERROR`; do not call its downstream outcome an invariant/scope counterexample.
4. **Outcome-only check:** an evaluator/game/level failure with no local frozen prediction/effect mismatch maps to `OUTCOME_ONLY`, not a local counterexample.
5. **Effect check:** apply the frozen effect comparator/representation to the prior predicted effect and reliable observed effect. Match = no counterexample. Missing comparison rule or unknown target field = unresolved, not mismatch.
6. **Attribution:** if a reliable mismatch remains, distinguish:
   - **Dynamics contradiction:** all declared state/action variables and the observed effect are reliable; the current relation's predicted effect is contradicted within its stated scope. Map to `DYNAMICS_COUNTEREXAMPLE` and challenge the candidate relation/effect model.
   - **Scope miss:** the skill's recorded guard returned `APPLICABLE`, the action/observation path is reliable, but the admitted context is shown by the frozen contract/evidence to lie outside the relation's valid scope. Map to `SCOPE_COUNTEREXAMPLE`. This says the boundary admitted a bad context; it does not alone prove the relation false.
   - **Missing-condition hypothesis:** an observable predicate from the pinned vocabulary may distinguish the failed context from prior supporting contexts. This is a diagnostic subtype, not a new P2 enum and not proof. Keep it `HYPOTHESIZED` until the prospective evidence criterion is met; otherwise top-level class stays `AMBIGUOUS_UNRESOLVED` or `SCOPE_COUNTEREXAMPLE` according to the operational scope-miss fact.
   - **Unresolved:** more than one explanation remains, relevant state is hidden/unmeasured, attribution depends on an unpinned ontology, or available evidence cannot tell dynamics failure from omitted scope. Map to `AMBIGUOUS_UNRESOLVED`; do not narrow a guard.

A single event can establish a safety-relevant admission failure and trigger quarantine, while its causal explanation remains unresolved. Conversely, a task-level failure without a local predicted-effect contradiction is not a counterexample. Preserve primary P2 classification and any secondary diagnostic flags in the immutable P4 TriageAssessment sidecar; never relabel one class to improve a result.

### 4.3 P4 triage sidecar and P2 taxonomy interoperability

The P4 `TriageAssessment-v1` artifact records `assessment_id`, `taxonomy_version`, `counterexample_record_id` (when a P2 record exists), `skill_version_id`, `prediction_id`, `observed_event_id`, `primary_p2_class`, zero or more diagnostic subtypes, `adjudication_state` (`CONFIRMED`, `PROVISIONAL`, `UNRESOLVED`, or `NOT_APPLICABLE`), ordered checklist results, predicate-difference refs, rationale/evidence refs, adjudication method and actor refs, classifier/provenance refs, timestamp, and append-order identity. It contains no probability by default. A proposed missing-condition predicate is recorded as a hypothesis with its observations, not as a settled cause.

P2 `CounterexampleRecord.classification` remains exactly one of `DYNAMICS_COUNTEREXAMPLE`, `SCOPE_COUNTEREXAMPLE`, `EXECUTION_ERROR`, `OBSERVATION_ERROR`, `OUTCOME_ONLY`, or `AMBIGUOUS_UNRESOLVED`. P4 subtypes (`OBSERVATION_UNCERTAIN`, `MISSING_CONDITION_HYPOTHESIS`, `PREDICTION_INTEGRITY_FAILURE`, and adjudication state) live in the P4 sidecar referenced by the immutable classifier/provenance artifact refs. No new unrecognized field or enum is added to `schema_v1.json` by P4.

## 5. P4.3 — Scope refinement, versioning, and evidence separation

### 5.1 Freeze the parent and protect data roles

On a confirmed material scope/dynamics contradiction, stop the current invocation and append a `CounterexampleRecord` linked to the old SkillVersion. Quarantine the affected immutable SkillVersion where its prediction/applicability may cause harm or cannot be trusted. Never edit its guard, prediction, evidence snapshot, or digest in place.

Every source/event ref receives a prospective role before its outcome is used: candidate construction, contradiction diagnosis, candidate refinement, validation, or later confirmatory evaluation (only if separately authorized). An event used for refinement is permanently ineligible as validation evidence for the refined CandidateVersion, derived SkillVersion, or semantic descendants. A revised guard creates a new CandidateVersion and, only after a separate decision, a new SkillVersion; the new version needs fresh evidence for validation. No target result refines the same version and then counts as held-out validation.

### 5.2 Adding a condition (specialization proposal)

For a confirmed scope miss or well-supported missing-condition diagnosis:

1. Enumerate only predicates in the frozen, versioned observable predicate vocabulary. Reject any predicate requiring hidden state, evaluator outcomes, future events, post-hoc split labels, or an unpinned feature.
2. Require the predicate evaluation to be `KNOWN` at the mismatch and in every prior support context used to assess the proposal. If any relevant evaluation is `UNKNOWN`, do not use that predicate to create a positive refinement; retain an abstention/unresolved outcome.
3. For each predicate `q` that is KNOWN and FALSE at the miss and KNOWN/TRUE in at least one reliable prior support context, produce a separate proposed successor CandidateVersion guard `G' = G AND q` in stable predicate-ID order, with an explicit predecessor link and genesis `LifecycleEvent` to `PROPOSED`. A corresponding successor SkillVersion requires a separate promotion/specification decision. This is a minimal observed contrast, not a support threshold; retain all such proposals and record their support/coverage accounting. Do not select a favorable condition after target results. A stricter guard can only be a proposal, not automatic proof of validity.
4. If no observable `q` is available, do not add an opaque exact-context blacklist or guessed condition. Keep the old version quarantined/disabled under policy, lower use to abstention, or reject/hold the candidate pending a genuine representation change.
5. Adding a guard may reduce coverage. Report eligible, `TRUE`, `FALSE`, `UNKNOWN`, abstained, and invoked context counts separately. Do not optimize coverage on target outcomes or call lower coverage a successful refinement by itself.

A single verified scope miss may justify a fail-closed/quarantine decision and a **draft** stricter successor proposal; it does not meet any unstated support, generalization, validation, or promotion threshold.

### 5.3 Removing conditions, splitting, and rejection

- **Remove/relax a condition:** never do so merely because a later success occurred or because a stricter guard has low coverage. Generate a relaxation proposal only from fresh, permitted evidence under an explicit prospective redundancy/generalization policy and independent review. If no policy/threshold is pinned, keep the condition or abstain; no automatic relaxation.
- **Split a candidate/skill:** if a pinned observable predicate partitions contexts with distinct supported relation/effect hypotheses, emit separate successor CandidateVersion proposals for `G AND q` and `G AND NOT q`. `UNKNOWN` belongs to neither child and must abstain. Do not merge identities or overwrite the parent. Both branches remain proposals until separately reviewed.
- **Reject the relation:** if reliable evidence directly falsifies a deterministic relation under its declared preconditions/variables, append a rejection decision for that CandidateVersion and quarantine any derived SkillVersion. For stochastic/noisy relations, reject only under a previously frozen statistical criterion; if none exists, hold/unresolve rather than inventing a threshold.
- **No distinguishing condition:** if a miss cannot be separated using allowed observable predicates, do not specialize on event ID, level ID, screenshot hash, or target label. Reject/hold the current relation, or abstain pending a genuinely new representation; record the lost coverage.

All refinements use P2 append-only lifecycle/version semantics. Candidate promotion, SkillVersion creation, validation, activation, and runtime authorization remain distinct decisions; P4 makes none automatically.

## 6. P4.4 — Runtime applicability, fallback, and logging state machine

Runtime semantics are normative but not implemented. Invocation is allowed only for an independently authorized `ACTIVE` SkillVersion with compatible pinned artifacts and known runtime-critical caps; a draft or merely structurally valid SkillVersion is not executable.

### State machine

1. **LOAD/PREFLIGHT:** resolve immutable SkillVersion, candidate parent, representation/normalizer, policy, evidence snapshot, lifecycle chain, and authorization. If missing, stale, quarantined, retired, superseded, incompatible, or not `ACTIVE`, return `REJECT/ABSTAIN` with a reason; take no skill action.
2. **OBSERVE/NORMALIZE:** record current raw observation and normalize only with the pinned version. If required fields are missing, uncertain, occluded, or conflicting, record `UNKNOWN` and abstain. Do not infer hidden values.
3. **BIND:** bind each required parameter from permitted observations through pinned typed rules. If zero or multiple matches, type mismatch, or unresolved binding, abstain. Never pick an arbitrary entity.
4. **APPLICABILITY:** evaluate each required predicate in stable ID order. All `TRUE` and compatible -> locally `APPLICABLE`; any known `FALSE` -> `REJECT` this invocation; any `UNKNOWN` -> `ABSTAIN`. Do not coerce unknown to false or true.
5. **PREDICT/FREEZE:** create and append P2 `PredictionRecord` with SkillVersion, context/action, all-TRUE required predicate evaluations, predicted effect, model/config, evidence snapshot, timestamp and order **before** dispatching the target action. If a valid prediction cannot be formed, do not invoke a policy that requires it; use the authorized fallback or abstain.
6. **EXECUTE/VERIFY:** dispatch only the declared action under the P2 action/step/wall-time/compute limits. Record command and actual dispatch/acceptance. Compare observed local effects only against the frozen prediction using the pinned comparator. Never retry, skip, or continue after a material mismatch unless an independently authorized fallback policy explicitly permits a safe, budgeted recovery.
7. **STOP ON MISMATCH:** stop the skill immediately on action mismatch, invalid tool response, unexpected effect, stale state, failed postcondition, or expired budget. Append observations and a P2 CounterexampleRecord/TriageAssessment with unresolved states preserved. A confirmed scope/dynamics contradiction or risk-relevant unresolved mismatch triggers fail-closed quarantine/review according to the prospective lifecycle policy; no in-place repair.
8. **FALLBACK:** choose only the P2-declared fallback. Default when no separate fallback is available is `ABSTAIN`/`NO_OP`/abort, not a guessed action. `AUTHORIZED_SAFE_POLICY` may run only if separately versioned, validated/authorized, compatible, within a reserved budget, and its own applicability checks pass. `DEOPT` may call a separately authorized baseline only if its input, action and cost budget were prospectively included; no hidden extra model or uncharged retry.
9. **CLOSE/LOG:** append all prediction, observations, action attempts, checks, result/assessment, fallback, resource costs, and lifecycle decisions. Keep evaluator task outcomes in their separate store. Do not update the active version from its own just-observed outcome.

### Limits and mismatch handling

P2 requires explicit action, step, wall-time, and compute limits. If any runtime-critical limit, unit, or enforcement policy is unknown, the SkillVersion is not eligible to invoke. At the first exhausted limit, stop before issuing another action. A fallback action is allowed only if a separate budget was reserved and its policy was authorized; otherwise terminate with abstention/no-op. P4 sets no numerical step, action, time, or compute cap.

Every mismatch stops the current skill invocation. Proven execution/observation errors are recorded as such and do not narrow the invariant's guard. Confirmed scope/dynamics contradiction creates a counterexample and may quarantine the immutable version. An unresolved mismatch never becomes a negative training label or guard condition; use fail-closed abstention and preserve it for review.

## 7. Deterministic high-level pseudocode

```text
P4_PROPOSE(manifest M, pinned_config C):
    if !permissions_ok(M) or !all_required_refs_pinned(C): return BLOCKED_UNRESOLVED
    E := deduplicate_exact_ids_or_halt(M)
    V := normalize_with_pinned_versions(E)          # preserve UNKNOWN and raw refs
    T := build_complete_transition_views(V)         # audit incomplete views
    A := enumerate_maximal_structural_alignments(T, stable_order=True)
    P := []
    for alignment in A:
        if alignment.has_ambiguous_field_mapping:
            audit(alignment, ALIGNMENT_AMBIGUOUS); continue
        for template in C.relation_templates_in_stable_order:
            if !typed_template_match(template, alignment):
                audit(alignment, NO_TEMPLATE_MATCH); continue
            proposal := instantiate_without_hidden_inference(template, alignment)
            if !has_state_action_effect_falsifier_and_predicates(proposal):
                audit(proposal, MOTIF_ONLY); continue
            ledger := classify_all_permitted_source_events(proposal, E)
            audit := count_unique_refs_and_all_evidence_roles(ledger)
            if !C.identity_profile_pinned: audit(proposal, ID_PROFILE_UNSET); continue
            candidate := emit_immutable_CandidateVersion(proposal, ledger)
            append_genesis_LifecycleEvent(candidate, NOT_APPLICABLE -> PROPOSED)
            link(candidate, audit)
            P.append(candidate)
    return stable_sort(deduplicate_identical_proposals(P)), all_audits

P4_TRIAGE(prediction p, observed event o, skill s, config C):
    if !permitted_refs(p, o):
        return BLOCKED_INTEGRITY_REVIEW
    if !valid_pre_outcome_prediction(p, s, o):
        if evaluator_outcome_only(o): return OUTCOME_ONLY
        return AMBIGUOUS_UNRESOLVED(PREDICTION_INTEGRITY_FAILURE)
    if verified_observation_fault(o): return OBSERVATION_ERROR
    if observation_uncertain(o): return AMBIGUOUS_UNRESOLVED(OBSERVATION_UNCERTAIN)
    if !action_execution_matches(p, o): return EXECUTION_ERROR
    if evaluator_outcome_only(o): return OUTCOME_ONLY
    if effect_matches_under_pinned_comparator(p, o, C): return NO_COUNTEREXAMPLE
    if !all_required_inputs_reliable(p, o) or !attribution_resolved(p, o):
        return AMBIGUOUS_UNRESOLVED
    if guard_admitted_but_context_outside_supported_scope(p, o):
        return SCOPE_COUNTEREXAMPLE_WITH_OPTIONAL_MISSING_CONDITION_HYPOTHESES
    return DYNAMICS_COUNTEREXAMPLE

P4_REFINE(parent version v, triage x, frozen predicate vocabulary Q):
    if evidence is hidden/test/confirmatory or not permitted: return BLOCKED_NO_REFINE
    append x; stop current invocation
    if a validation event is being reused for a successor:
        append evidence-use event REFINEMENT_FOR_SUCCESSOR; forbid it as validation of successors
    if x is confirmed material scope/dynamics contradiction or risk-relevant unresolved:
        append QUARANTINED decision for v under policy; never edit v
    if x is DYNAMICS_COUNTEREXAMPLE:
        if relation_is_deterministic(v) and all_inputs_and_execution_verified(x):
            append REJECT decision for candidate parent; return REJECTED_NO_GUARD_EDIT
        return HOLD_NO_GUARD_EDIT                 # stochastic/noisy criterion is not set
    if x is not a confirmed scope miss: return HOLD_OR_NO_GUARD_PROPOSAL
    successors := []
    for q in Q sorted by predicate_id:
        if q is permitted, observable, KNOWN and FALSE at the miss, and KNOWN/TRUE in at least one reliable prior support context:
            successors.append(new CandidateVersion with guard parent_guard AND q)
    if successors is empty: return ABSTAIN_OR_HOLD_OR_REJECT_PER_FROZEN_POLICY
    for successor in successors:
        append genesis LifecycleEvent NOT_APPLICABLE -> PROPOSED with predecessor/evidence refs
        append separate source/evidence/cost/coverage ledger
    return successors                 # no automatic SkillVersion, validation, or activation
```

Pseudocode specifies deterministic control flow, not an executable implementation. Helper predicates, alignments, effect comparators, lifecycle transitions, thresholds, policy decisions and identity/hashing require the referenced pinned contracts. If absent, use the fail-closed return state; do not invent them.

## 8. Synthetic decision fixtures

The [P4 decision fixtures](decision_fixtures.md) exercise candidate proposal, all taxonomy branches, refinement, data-role protection, and runtime stop/fallback. They are hand-authored contract examples and have not been executed.

## 9. Explicit unresolved questions

- Which ARC observation/state/object correspondence and action/effect ontology, normalizer and relation/predicate DSL are permitted, and who versions/reviews them?
- Which exact alignment/token fields, motif size policy, duplicate/context independence rule, and tie handling beyond the conservative draft are appropriate?
- Which candidate relation-template inventory and variableization rules are defensible without hand-coding task-specific structure or importing hidden labels?
- What support, recurrence, counterexample adjudication, guard-refinement, validation and promotion criteria are justified and prospectively frozen? No numeric threshold is set.
- What constitutes reliable perception/action execution and who adjudicates disputed/unresolved mismatches?
- Which data manifests, evidence-role partitions and validation cohort are permitted under existing authorization; how can a fresh successor-validation set be obtained without a state fork?
- What safe fallback policies, action/step/time/compute budgets, reserved recovery costs and runtime authorization gates are available?
- How should ambiguous multi-cause cases and multiple plausible guard refinements be prioritized without outcome-based selection?
- What is the approved stable-ID/hash canonicalization profile required by P2?

These are explicit later design questions, not a reason to guess now. P4 completion means the algorithm's control flow, data distinctions, versioning, and failure semantics are specified at a bounded design level; it does not mean a domain ontology, executable policy, support threshold, fallback skill, or validation study has been selected.
