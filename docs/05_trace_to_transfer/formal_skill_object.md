# Formal Skill Object Contract — T2T-P2

**Contract ID:** `T2T-SkillObject-v1.0.0-draft`  
**P2 disposition:** complete for the owner-approved idea-stage documentation scope.  
**Normative companion:** [`p2/schema_v1.json`](p2/schema_v1.json)  
**Interoperability fixtures:** [`p2/interoperability_fixtures.md`](p2/interoperability_fixtures.md)  
**Boundary:** a design contract only. It is not an implementation, candidate-generation result, validation result, experiment authorization, benchmark readiness decision, or permission to access restricted outcomes.

## 1. Contract in brief

A reusable invariant skill is **not** a trace, macro, option, candidate, or status label. It is an immutable, versioned executable specification that:

1. refers to a separately versioned **candidate invariant hypothesis** over a declared state/action/effect representation;
2. declares typed parameters and bindings rather than copying source-trace values;
3. declares observable applicability predicates and a predictive effect contract;
4. specifies a policy artifact, termination condition, and fallback behavior;
5. pins the permitted evidence snapshot and provenance used to create the version; and
6. receives lifecycle status only through append-only, evidence-linked decision events.

`CandidateVersion`, `SkillVersion`, `EvidenceSnapshot`, `LifecycleEvent`, `PromotionDecision`, `ApplicabilityResult`, `PredictionRecord`, `EffectAssessment`, and `CounterexampleRecord` are distinct record types. Passing schema checks establishes only structural validity. It does not show that the invariant is true, useful, transferable, novel, or eligible to run.

## 2. Object model and non-equivalence rules

### 2.1 Candidate invariant

A `CandidateVersion` is a falsifiable, non-executable hypothesis that a typed relation among normalized state, action, and observed effect recurs across contexts. It contains a versioned representation reference, relation/parameter definitions, proposed preconditions, a pinned evidence snapshot, and provenance. A candidate may be rejected, held, or accepted for skill specification; none of those decisions silently makes it an executable skill.

A frequent action label, string match, repeated screenshot, or recurring sequence is not sufficient by itself to meet this definition. The relation must state what variables correspond, what relation is claimed, what effect is predicted, and what observation could contradict it.

### 2.2 Skill version

A `SkillVersion` is the immutable executable specification derived from one candidate version. It adds an invocation policy, invocation-time applicability contract, predicted effect, parameter-binding rules, termination condition, fallback, resource accounting references, and a derivation snapshot. A skill version can be structurally complete while remaining unvalidated and inactive.

### 2.3 Trace, macro, option, and invariant skill

| Object | Minimum semantics | What it does **not** establish |
|---|---|---|
| **Trace** | Ordered observations, actions, observed transitions/effects, context, cost and provenance. | Reusable abstraction or applicability outside the recorded events. |
| **Raw replay** | Replays a stored trace/script under its recorded assumptions. | Parameter rebinding, transfer, or learned scope. |
| **Parameterized/compressed replay** | Stores a reusable procedure with explicit slots/parameters and binds values in a new context. | A cross-context invariant claim unless a separate relation is stated, supported, and tested. A capable baseline may encode semantics functionally; if it matches the treatment, no invariant-specific gain is established. |
| **Option / macro** | Temporally extended procedure/policy with an initiation rule and termination/fallback semantics. | That its policy was derived from, or tested as, a cross-context state/action/effect invariant. |
| **Candidate invariant** | Non-executable, falsifiable relation hypothesis with evidence and representation versions. | A deployable skill or scientific validation. |
| **Invariant skill version** | Executable conditional policy derived from a candidate, with typed bindings, applicability, predicted effect, termination, fallback and evidence lineage. | Truth, usefulness, calibration, transfer, safety, novelty, or run authorization merely by being well-formed. |

No conversion is implicit. A trace or macro becomes an invariant skill only when a separately versioned candidate relation and evidence-linked derivation are present. If the “invariant” can be removed without changing the represented behavior, it is not the treatment distinction for Claim N.

## 3. Identity, versions, and canonicalization

### 3.1 IDs

- `candidate_id`: stable lineage ID for a conceptual candidate family.
- `candidate_version_id`: immutable content digest for one candidate hypothesis version.
- `skill_id`: stable lineage ID for the executable skill derived from a candidate family.
- `skill_version_id`: immutable content digest for one skill's executable semantics.
- `event_id`: immutable identity of one source trace event.
- `evidence_snapshot_id`: immutable digest of an ordered, purpose-specific set of evidence references.
- `decision_id`: immutable identity of one lifecycle decision event.

Stable lineage IDs use UUIDs or another project-approved globally unique scheme. Version and snapshot digests use `sha256:<64 lowercase hex>` over canonical UTF-8 JSON. Canonicalization must be versioned and specify object-key ordering, Unicode normalization, numeric representation, and treatment of omitted optional fields. Array order is significant unless that field's contract explicitly says otherwise.

### 3.2 Hash boundary

The candidate-version digest covers the normalized hypothesis, relation language/version, representation version, parameter declarations, proposed preconditions, and derivation parent reference. The skill-version digest covers the candidate-version reference, executable policy reference, binding rules, applicability predicates, predicted-effect contract, termination, fallback, and required environment/representation compatibility. It excludes mutable lifecycle status, runtime counters, evaluation results, and later-added evidence.

An evidence snapshot has its own digest. Appending evidence does not rewrite an old candidate or skill version. If new evidence changes the hypothesis, binding schema, guard, policy, predicted effect, termination, or fallback, issue a successor version with a new digest and an explicit predecessor link. Never recycle a version ID after changing content.

### 3.3 Version axes

Every record pins `schema_version`. Candidate and skill records also pin the state/action/effect representation and normalizer versions; predicate/relation language versions; and policy artifact version/hash where applicable. A change in any semantic dependency requires a new dependent candidate/skill version or an explicit compatibility review recorded as a lifecycle decision. It must not silently reinterpret historical observations.

The normative JSON contract is [`p2/schema_v1.json`](p2/schema_v1.json). `additionalProperties` are rejected in v1: extending the contract requires a new schema version, not an undocumented field.

## 4. Typed values, missingness, and predicates

### 4.1 Unknown is a value, not a default

Do not use `null`, `false`, zero, an empty list, or a guessed default to mean “unknown.” A field whose value is unavailable uses the tagged form:

```json
{"availability":"UNKNOWN","reason_code":"NOT_OBSERVED","source_refs":[]}
```

A known field uses `{"availability":"KNOWN","value":...,"source_refs":[]}`. `NOT_APPLICABLE` is distinct from `UNKNOWN`. Unknown values that could affect invocation, predicted effect, identity, or evidence eligibility prevent a positive applicability result.

### 4.2 Predicate evaluation

A precondition evaluation has exactly one of `TRUE`, `FALSE`, or `UNKNOWN`, plus the predicate/version reference, observed value reference if available, and reason code. `FALSE` means the observed permitted state contradicts the predicate. `UNKNOWN` means it cannot be evaluated reliably from permitted observations. Never turn `UNKNOWN` into `FALSE`, and never treat either as `TRUE`.

An invocation-time `ApplicabilityResult` has:

- `applicable`: all required predicates are `TRUE`, the skill and representation versions are compatible, and no active contradiction invalidates the decision;
- `reject`: at least one required precondition is known `FALSE`; do not invoke in this context;
- `abstain`: a required predicate, compatibility fact, or evidence condition is `UNKNOWN`, missing, stale, or ambiguous; do not invoke.

`reject` is a local invocation verdict, not automatic global rejection of the skill. Numeric confidence is omitted unless a calibration procedure and version are specified; an uncalibrated score is not a probability.

## 5. Normative record fields

The companion JSON Schema gives exact required keys, types, and enumerations. The following semantics are normative.

### 5.1 CandidateVersion

Required groups:

- identity: `record_type`, `schema_version`, `candidate_id`, `candidate_version_id`, optional predecessor;
- representation: `representation_id`, `representation_version`, state/action/effect schema refs, normalizer ref, relation-language ref;
- claim: typed variables/parameter slots, relation AST/reference, proposed applicability predicates, claimed effect relation, explicit falsifier/contradiction criteria;
- evidence: one `evidence_snapshot_id` and refs to source manifest/provenance; roles distinguish support, contradiction, qualification, control, and unresolved evidence;
- provenance: source-event refs, producer/tool/prompt/config versions, creation time;
- `hypothesis_scope`: the contexts over which the hypothesis is asserted. A finite observed context list is evidence scope, not proof of universal validity.

It has no executable policy, runtime status, or hidden evaluator outcome field.

### 5.2 SkillVersion

In addition to its candidate reference, a `SkillVersion` requires:

- typed `parameter_schema` and explicit `bindings`; each bound value refers to permitted evidence or is tagged unknown;
- `applicability`: versioned, observable precondition predicates with tri-state evaluation contract and scope;
- `effect_model`: a prediction form, target fields, representation ref, and prediction-time/source-event ref; predicted and observed values are never overwritten into one another. A `DISTRIBUTION` output is not a calibrated probability unless its calibration procedure/version is pinned;
- `policy_artifact`: immutable artifact ref/hash plus explicit entrypoint, input/output schema refs, supported-action refs, and compatibility refs;
- `termination`: explicit condition plus separately typed action, step, wall-time, and compute limits. Unknown/unset runtime-critical limits block eligibility to execute; P2 sets no numerical cap;
- `fallback`: explicit no-op/abstain/deopt/error path, and conditions for selecting it;
- `derivation`: candidate version and evidence snapshot IDs;
- separated creation/validation/runtime cost references, without a composite score.

Schema validity does not mean a runtime policy has been implemented. P2 creates no executable skills.

### 5.3 EvidenceSnapshot and EvidenceRef

An `EvidenceSnapshot` is a frozen ordered manifest of allowed source evidence. Each `EvidenceRef` points to an immutable event/trace manifest, event index, context ref, representation/normalizer versions, and evidence role. The snapshot identifies the question it supports (candidate formation, contradiction review, structural validation, or a future authorized study). A reference must resolve to permitted source material and must not point to a hidden/test/confirmatory outcome.

Keep raw source event, derived interpretation, and prediction in separate fields. A separate `PredictionRecord` pins the skill version, context/action, all-TRUE applicability predicates, predicted target/effect values, prediction model, evidence snapshot, timestamp, and append order before the target action/result; a later `EffectAssessment` links the prediction to the separately stored observation.

- `OBSERVED`: directly recorded observation/action/effect;
- `INFERRED`: hypothesis or annotation derived from observations, with annotator/method and provenance;
- `PREDICTED`: frozen expectation made before the target event;
- `COUNTEREXAMPLE`: observed event classified against a pinned prior prediction and conditions;
- evaluator `OUTCOME`: kept in a separate evaluation record/store; unavailable to earlier candidate construction, promotion, and threshold selection.

A matched WITH/WITHOUT utility label is `COUNTERFACTUAL_ACTIVATION` evidence. It does not become a dynamics counterexample or skill-scope counterexample merely because its outcome differs. An `INFERRED` evidence reference must pin its derivation method and producer provenance. Producer class (`HUMAN`, `SOFTWARE`, `AGENT`, or `IMPORT`) is explicit: an AI-generated/drafted label must never be reported as an independent human annotation stream. If a later work package requires independent human annotation, it must separately enforce distinct human annotators and adjudication; this schema does not certify independence.

### 5.4 LifecycleEvent and PromotionDecision

Status is derived from an append-only lifecycle event stream; it is not a mutable field in candidate/skill semantic content. Every event records subject ID/version, prior and next status, decision type/reason, policy version, evidence snapshot, actor class, timestamp, and predecessor event. No event is deleted or rewritten; a correction is an appended superseding event that preserves the original.

Candidate statuses: `PROPOSED`, `UNDER_REVIEW`, `ACCEPTED_FOR_SKILL_SPEC`, `REJECTED`, `SUPERSEDED`.

Skill statuses: `DRAFT`, `ELIGIBLE_FOR_VALIDATION`, `VALIDATED`, `ACTIVE`, `QUARANTINED`, `RETIRED`, `SUPERSEDED`.

| Record | Allowed status path (policy may skip only where stated) |
|---|---|
| Candidate version | Genesis `NOT_APPLICABLE → PROPOSED`; then `PROPOSED → UNDER_REVIEW / REJECTED / SUPERSEDED`; `UNDER_REVIEW → ACCEPTED_FOR_SKILL_SPEC / REJECTED / SUPERSEDED`; accepted/rejected/superseded versions are terminal. Reconsideration creates a successor version and a new decision chain. |
| Skill version | Genesis `NOT_APPLICABLE → DRAFT`; `DRAFT → ELIGIBLE_FOR_VALIDATION / QUARANTINED / RETIRED`; `ELIGIBLE_FOR_VALIDATION → VALIDATED / QUARANTINED / RETIRED`; `VALIDATED → ACTIVE / QUARANTINED / RETIRED`; `ACTIVE → QUARANTINED / RETIRED / SUPERSEDED`; `QUARANTINED → RETIRED / SUPERSEDED`. `RETIRED` and `SUPERSEDED` are terminal. A quarantined version is never reactivated; a fix creates a new successor version. |

`ELIGIBLE_FOR_VALIDATION` means the object passes structural/provenance checks only. `VALIDATED` can be entered only after an applicable future protocol defines evidence and criteria prospectively; no threshold is set in P2. `ACTIVE` means runtime use was separately authorized, not just that a skill exists. P2 authorizes no transition into `VALIDATED` or `ACTIVE` based on this document.

A material contradiction, likely harm, stale dependency/normalizer, or evidence-integrity concern can quarantine the affected skill version pending review. Quarantine disables invocation; it does not edit the version. A revision creates a new successor candidate/skill version and cites the decision/evidence that motivated it. Retirement is terminal for that version but does not erase its lineage or prevent a separately reviewed successor.

There is no numeric support, recurrence, breadth, confidence, or promotion threshold in P2. A future promotion policy must be justified and frozen before the evidence it will judge; thresholds must not be lowered after observing yield.

## 6. Invariant-versus-replay operational contract

Use the same source events and comparable retrieval, storage, context, model, compute, and action budgets for the treatment and replay comparator. Define three representations separately:

1. **Raw replay:** stored actions/trace with source-context assumptions.
2. **Strong parameterized/compressed replay:** best-effort reusable script/procedure distilled from the same allowed traces, with typed slots, parameter binding, compression, and ordinary execution checks. It must not be intentionally weakened. It may reproduce a relation functionally; if it does, that is a comparator result, not a reason to relabel it.
3. **Invariant-skill representation:** an explicit versioned relation over typed state/action/effect variables, distinct from the stored sequence, with parameter mappings, applicability predicates, prospective effect prediction, and evidence-linked scope.

A relation counts as an **operational semantic delta** from replay only if all of the following are inspectable:

- the relation and its variables/typing are explicit and versioned, not merely a trace hash, prose label, or post hoc explanation;
- its applicability and predicted effect can be evaluated from permitted observations before the target outcome;
- evidence shows it is intended to cover contexts beyond exact replay of its source events (the required recurrence/context threshold remains unset);
- a held-out, permitted context can distinguish the relation's prediction/decision from exact replay, while a strong parameterized comparator receives equivalent data and resources; and
- ablation of the relation/scope semantics preserves the surrounding wrapper, parameters, retrieval, memory, and budgets as far as possible.

If the relation cannot be evaluated independently of replay, the target contexts never distinguish the representations, or strong replay matches the invariant treatment under the fair comparison, Claim N is unidentifiable or unsupported. Compression, generalization, and conditional invocation are not by themselves proof of invariant-specific value. The P1 packet establishes that novelty of the broad mechanism is not cleared; this section defines the experimental distinction only.

## 7. Prediction, counterexample, and outcome integrity

Every prediction record pins the skill version, state/action representation, source state, action, predicted effect, predicate results, timestamp/order, and evidence snapshot. The prediction must be frozen before the target action/result. The observation record is appended separately afterward.

- A **dynamics counterexample** contradicts a transition/effect prediction under the recorded state/action model.
- A **scope counterexample** is a classified event showing that the guard admitted a context in which the skill prediction was invalid. It may justify quarantine and later scope analysis; it does not by itself prove the underlying relation false.
- An **ambiguous mismatch** stays `UNKNOWN/UNRESOLVED`; it must not narrow a guard or be counted as positive support.
- A final task/level failure is an evaluator outcome, not automatically a local counterexample.
- No outcome, target/test answer, restricted result, or post hoc split label may be written into the pre-outcome evidence snapshot or promotion decision. Store permitted interaction events and evaluator outcomes separately.

## 8. Cost and resource contract

Record creation cost, validation cost, invocation cost, and total costs separately with units, measurement method, scope, missingness, and provenance (e.g. actions, tokens, wall time, compute, storage). Do not collapse them into the draft `SCV` intuition or another unvalidated weighted score. Unknown cost stays explicit. Any future budget match or trade-off rule belongs in the protocol and remains unset here.

## 9. Structural validation and invariants

A record is structurally valid only if:

1. `record_type` and `schema_version` are recognized and no unrecognized keys occur;
2. every ID/digest is well-formed, content digests match canonical content, and parent refs resolve;
3. required semantic fields are present or use the explicit typed unknown form where permitted—never silent defaults;
4. all evidence refs resolve to an immutable manifest and declared versions;
5. observed, inferred, predicted, counterexample, and outcome data are not conflated;
6. relation/predicate/policy/effect language and representation versions are pinned;
7. a skill's policy, termination, fallback, and applicability contract exist before it is marked eligible; unknown runtime-critical fields prevent invocation;
8. status changes have append-only, version-linked lifecycle events and evidence/decision provenance;
9. any semantic edit creates a new content digest and successor version;
10. evidence and lifecycle records do not claim scientific validity, novelty, or authorization merely because schema validation passes; and
11. each `PredictionRecord` precedes the target action/result in both timestamp and append order, while its later `EffectAssessment` resolves to a separate observation record.

The JSON Schema enforces record shape; the invariants above also require semantic/reference checks that JSON Schema alone cannot guarantee.

## 10. Interoperability fixtures

The normative, non-executed fixtures and expected decisions are in [`p2/interoperability_fixtures.md`](p2/interoperability_fixtures.md). They cover a candidate that is not executable, a valid skill specification, true/false/unknown applicability, predictions frozen before outcomes, append-only mismatch handling, version tampering, outcome separation, and raw/parameterized/invariant representation distinctions. They are design examples, not test results or scientific evidence.

## 11. Decisions deliberately left open

These are explicit P2 outputs, not blockers to closing the documentation contract:

- exact canonical JSON algorithm/digest profile and the project-approved stable-ID scheme;
- ARC observation/state/object-correspondence and action/effect ontology versions;
- exact relation/predicate DSL and its operator inventory;
- recurrence, evidence breadth, minimum support, validation, and promotion thresholds;
- deterministic macro versus conditional policy versus predictive program as the first executable implementation;
- how to obtain matched state/counterfactual branches where the environment cannot fork;
- calibrated uncertainty/confidence, if any;
- exact fallback action/resource limits and budget-matching policy;
- source manifests and evidence identifiers for any later authorized study.

These choices remain open because P2 specifies object boundaries and data contracts, not the candidate generator, algorithm, thresholds, protocol, or implementation. P2 grants no authorization for experiments, ARC runs, restricted outcome access, split assignment, or implementation.
