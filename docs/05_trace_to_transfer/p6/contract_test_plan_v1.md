# T2T-P6 Contract Test Plan

**Test-plan ID:** `T2T-ContractTests-v1.0.0-draft`  
**Subphase:** P6.3 — Contract tests  
**Status:** complete for documentation/design scope. Tests, test harness, fixtures, and validators were not implemented or executed.  
**Authority:** passing a future contract test would establish only the tested engineering property; it would not establish scientific validity, efficacy, safety, benchmark readiness, or run authorization.

## 1. Test boundaries and fixture policy

All tests below are requirements for a future separately authorized engineering phase. Test fixtures must be synthetic, hand-authored, and marked `SYNTHETIC_FIXTURE`; no real ARC tasks, hidden/test/confirmatory data, live evaluator, benchmark, model call, split, or actual outcome is needed or permitted for these contract tests. Existing P2 interoperability fixtures and P4 decision fixtures may be reused only as documentation fixtures until implementation is separately authorized.

Test plan is layered:

1. **Static/schema checks:** parse the pinned P2 and P6 schema versions, event envelope and references; reject unknown versions/fields where the selected contract is strict.
2. **Pure contract checks:** deterministic functions over synthetic immutable records (normalization references, P2 semantics, P4 decisions, lifecycle and accounting) without agent/environment execution.
3. **Adapter/interface checks:** synthetic observation/action/response records passed through a mock environment adapter; no official evaluator or network.
4. **Isolation/access checks:** policy tests use synthetic restricted canary labels and fake credentials; assert deny/no-flow behavior without requesting or reading real restricted artifacts.
5. **Future environment integration:** expressly out of scope here; requires separate approval and live rules review.

Every test result in a future implementation must include test-plan/schema/config version, fixture hash, software version, outcome and failure logs. Do not call this design document a test result.

## 2. Contract test matrix

### 2.1 Parsing, schema and P2/P4 interoperability

| ID | Fixture / operation | Expected contract result |
|---|---|---|
| `SC-01` | Parse each known P2 record type using its pinned schema and a valid synthetic fixture. | Structural validity is reported separately from scientific/authorization status. |
| `SC-02` | Add an unknown property to a strict P2 v1 object. | Reject per P2 `additionalProperties:false`; require a new reviewed P2 version, not silent extension. |
| `SC-03` | Event envelope with a known event type/version and all required references. | Structurally accepted only if field types and referenced versions resolve. |
| `SC-04` | Unknown event type/schema version or malformed/missing required envelope field. | Reject/hold; never coerce into a default event kind. |
| `SC-05` | Field tagged `UNKNOWN`, `NOT_APPLICABLE`, known `false`, and omitted optional field. | Four states remain distinguishable under P2/event semantics. |
| `SC-06` | `UNKNOWN` encoded as `null`, empty string, zero or false for a required value. | Reject as a semantic contract violation; no imputation. |
| `SC-07` | P4 triage fixture with a fine-grained subtype and one P2 coarse class. | P2 `CounterexampleRecord.classification` stays within existing enum; subtype only in the P4 sidecar. |
| `SC-08` | `CandidateVersion` record passed to a runtime interface. | Reject: candidate is non-executable and has no runtime policy. |
| `SC-09` | P2 `PredictionRecord` plus later separate observation/`EffectAssessment`. | Accept only if version refs resolve and the prediction and observed effect are not overwritten or conflated. |

### 2.2 Immutability, determinism, versioning and provenance

| ID | Fixture / operation | Expected contract result |
|---|---|---|
| `DV-01` | Repeat a pure P4 proposal operation with identical permitted manifests and fully pinned config. | Same ordered proposal/audit content under the pinned deterministic profile; unresolved identity/hash profile blocks emission rather than guessing. |
| `DV-02` | Change one semantic candidate field (relation, guard, evidence snapshot, or representation version). | New content/version identity and predecessor link required; old record remains byte-for-byte immutable. |
| `DV-03` | Append lifecycle decision for same candidate/skill with valid predecessor. | Append-only history; status is derived from events; no mutable status overwrite. |
| `DV-04` | Attempt illegal lifecycle transition or reactivation of quarantined version. | Reject/hold with reason; remediation requires a successor version under P2/P4. |
| `DV-05` | Append correction to a mistaken event. | Original remains intact; correction links original and records reason/impact; downstream audit sees both. |
| `DV-06` | Reuse event ID with different content, break digest, orphan a referenced parent, or mismatch schema version. | Integrity hold; no silent deduplication or repaired provenance. |
| `DV-07` | Duplicate source event with exact same ID/content; then same ID with changed content. | Exact duplicate is accounted once under pinned dedupe rule; conflicting reuse is integrity failure and blocks affected flow. |
| `DV-08` | Same timestamps with an impossible/non-monotone stream sequence or cross-stream causal link without a parent. | Do not infer order; block any pre-action claim and retain an audit fault. |

The deterministic digest/ID test is conditional on a future reviewed canonicalization profile. This plan does not select that profile.

### 2.3 Prediction, action, transition and applicability ordering

| ID | Fixture / operation | Expected contract result |
|---|---|---|
| `RT-01` | All required predicate evaluations are P2 `TRUE`; versions compatible; binding resolved. | `APPLICABLE` may proceed to a prediction request, subject to authorization and known budget. |
| `RT-02` | A required predicate is known `FALSE`. | Local `REJECT`; no skill action; do not globally reject the skill. |
| `RT-03` | A required predicate/binding/compatibility fact is `UNKNOWN`. | `ABSTAIN`; no action; unknown is not false or true. |
| `RT-04` | Prediction is absent when P5 requires it, or is recorded after dispatch/result. | Block dispatch / mark trace invalid. Never create a retrospective pre-action prediction. |
| `RT-05` | Prediction and dispatch share stream with valid order, but timestamp order is equal or reversed. | P2's required timestamp/append ordering is not established; block/mark invalid rather than relying on sequence alone. |
| `RT-06` | Action request exists but environment dispatch fails or rejects it. | Log request and actual result distinctly; downstream outcome is not treated as successful execution or invariant counterexample. |
| `RT-07` | Valid dispatch followed by reliable transition and pinned effect comparator. | Append a separate effect assessment (`MATCH`/`MISMATCH`/`UNKNOWN`) linked to prediction and observation. |
| `RT-08` | Required observation field is occluded/conflicting or has stale normalizer. | Keep uncertainty or classify verified observation fault through P4/P2; no guard refinement from unknown/corrupt data. |
| `RT-09` | Only final task/game failure exists, with no local prediction/transition mismatch. | P4 `OUTCOME_ONLY`; do not report a dynamics/scope counterexample. |
| `RT-10` | Prediction/action/observation logs are incomplete at a material mismatch. | Stop/hold and preserve incomplete state; no positive or negative scientific attribution. |

### 2.4 Runtime stop, fallback and failure behavior

| ID | Fixture / operation | Expected contract result |
|---|---|---|
| `FB-01` | Skill is draft, inactive, quarantined, stale, incompatible or not separately authorized. | Runtime gate rejects/abstains before action. |
| `FB-02` | Any runtime-critical action/step/time/compute cap or unit is missing/unknown. | Block invocation; never substitute a hard-coded/default cap. |
| `FB-03` | Mismatch, invalid response, stale state, cap expiry or timeout during invocation. | Stop before another skill action; append failure/mismatch and cost events. |
| `FB-04` | No separately authorized fallback or reserved budget exists. | Terminate with specified abstain/no-op/abort outcome; no hidden retry/deopt. |
| `FB-05` | Fallback exists but its own applicability or budget is unknown/false. | Do not dispatch fallback; log refusal and stop. |
| `FB-06` | Fallback/deopt is separately authorized, compatible, applicable and within reserved budget. | It may proceed through its own gate; charge and log all cost/actions, including recovery. |
| `FB-07` | Tool call fails after action request, or environment says action rejected. | Explicit failure path, not success; preserve event/denominator and do not continue script. |

### 2.5 Candidate generation, replay and baseline interfaces

| ID | Fixture / operation | Expected contract result |
|---|---|---|
| `AR-01` | `B0`, `R0`, `R1`, `Grec`, `I0`, `I1`, and relation-ablation adapters receive the same synthetic `DecisionRequest`. | Shared request fields, observation/history and wrapper version are identical; treatment factor is explicit in arm config. |
| `AR-02` | `R0` sees a mismatch against its exact trace. | Stop and abstain/error under P3; do not skip, retry, substitute, or alter trace. |
| `AR-03` | `R1` binds a typed slot uniquely from allowed observable fields. | It may transport only source-aligned fields/effects under its frozen P3 rules; event/cost references retained. |
| `AR-04` | `R1` slot binding is ambiguous, unknown, or unsupported. | Abstain; no invented relation, latent feature, or target-derived binding. |
| `AR-05` | `Grec` emits a recurrence candidate. | Candidate remains non-executable and is evaluated through the shared frozen prediction interface; no silent promotion. |
| `AR-06` | `I0` vs `I1` arm configs differ in more than the prospectively declared boundary-update factor. | Parity/contrast check fails or comparison is flagged confounded; do not attribute the result to boundary learning alone. |
| `AR-07` | Relation-ablation arm changes wrapper, retrieval, slot schema, model, or budget along with relation semantics. | Mark ablation non-isolating; no invariant-specific causal interpretation. |
| `AR-08` | Baseline and treatment have same declared cap refs but different realized resource use. | Preserve both cap and realized vector; evaluate using P5 prospective interpretation, never pad/normalize after outcomes. |
| `AR-09` | A common interface field is missing or a baseline emits a prediction without the required P2 record. | Fail contract/mark comparison incomplete; no arm gets a silent logging exemption. |
| `AR-10` | R1 comparison lacks a frozen artifact/config record or independent competence-review disposition. | Do not classify the R1-vs-I0 comparison as a valid primary Claim N comparison; mark blocked/inconclusive, not a baseline defect inferred after results. |

These tests check interfaces and control invariants only; they do not assess whether a baseline is competent or whether an arm wins.

### 2.6 Costs, budget parity and missingness

| ID | Fixture / operation | Expected contract result |
|---|---|---|
| `BC-01` | Each arm supplies declared cap refs and realized resource events for all P5-frozen dimensions. | Produce a vector comparison with units, stage, scope, provenance, missingness and both caps/use. |
| `BC-02` | Required cap, unit, or counter source is missing/unknown. | Parity is not certified; runtime blocks where cap is runtime-critical; no default value. |
| `BC-03` | Resource amount is unknown. | Retain `UNKNOWN` with reason; must not aggregate as zero. |
| `BC-04` | Uncharged model call, retry, action, fallback or tool use is injected. | Budget contract violation, stop/hold, preserve event; no retrospective cap expansion. |
| `BC-05` | Creation/validation cost omitted while invocation cost is present. | Accounting check fails completeness; report not eligible for full-method cost comparison. |
| `BC-06` | Different dimensions are combined into a weighted `total_cost` score without P5-approved rule. | Reject composite; report component vector only. |
| `BC-07` | Timeout, crash, abstention, fallback or no candidate occurs. | Keep unit in the correct assigned/opportunity denominator and reason-coded flow. |

No numeric cap, tolerance, pass/fail amount, or unit conversion is chosen in this plan; P5 freeze-gate decisions remain controlling.

### 2.7 Trust-boundary and outcome-isolation tests

| ID | Fixture / operation | Expected contract result |
|---|---|---|
| `IS-01` | Synthetic hidden-label canary is placed in the restricted-outcome test store. | Agent, candidate generator, baseline builder and refiner have no permitted read path; access is denied and logged. This is a mock policy test only. |
| `IS-02` | Restricted-outcome reference is passed to source/candidate creation API. | Reject/hold on role/access mismatch; no candidate/evidence entry is produced. |
| `IS-03` | Permitted validation event is later used for a successor refinement in a synthetic fixture. | Append evidence-use role change; event is ineligible to validate successor and descendants. |
| `IS-04` | A correction tries to erase an unfavorable outcome, failure or denominator event. | Reject correction semantics; original remains and correction is auditable. |
| `IS-05` | Credential-like data appear in a synthetic event payload. | Reject or redact under a separately specified secret policy and record incident; do not persist secrets in general log. Exact redaction policy remains open. |
| `IS-06` | Evaluator outcome export is attempted without separate authorization. | Deny; no event/outcome reaches agent or analysis path. |

## 3. Required synthetic fixture inventory

Minimum fixtures, each with `SYNTHETIC_FIXTURE` provenance and no connection to a real task:

- one source event and one derived normalized observation, with raw/derived refs distinct;
- known `TRUE`, known `FALSE`, `UNKNOWN`, `NOT_APPLICABLE`, malformed and missing-tag values;
- a valid pre-action prediction/action/transition/effect chain and a reordered invalid chain;
- a `CandidateVersion` without executable fields and a separate `SkillVersion` lifecycle chain;
- exact R0 replay, R0 mismatch, unambiguous R1 slot binding and ambiguous/unknown R1 binding;
- P4 sidecar examples for observation uncertainty, execution error, dynamics contradiction, scope miss, outcome-only and unresolved attribution, mapped to unchanged P2 classes;
- one authorized/active hypothetical skill, one quarantined skill, one unknown runtime cap, no fallback, and a separately budgeted fallback;
- cost vectors with known/unknown units, uncharged call, missing creation cost and equal caps with unequal actual use;
- synthetic restricted canary/credential-like string for mocked access-control deny paths; and
- append-only event correction, duplicate content, conflicting reused ID, digest mismatch and missing parent.

These fixtures are test design inputs, not empirical data or executed tests.

## 4. Acceptance criteria for a future test implementation

A future contract-test implementation is complete only when:

1. All matrix tests are mapped to an implemented schema/component version and traceable requirement.
2. Positive and negative paths are covered; untested items remain explicitly `NOT_TESTED` rather than implicitly passed.
3. Test runner has no network/evaluator/task-data access for synthetic contract tests.
4. Outputs include exact software/schema/fixture hashes, logs, failure reasons and reproducible invocation metadata under an authorized engineering scope.
5. P2/P4 interoperability and source/target isolation checks are independently reviewed.
6. Resource parity tests consume an approved P5 cap contract; before that, only missing/unknown blocking behavior can be tested, not numeric parity acceptance.
7. Passing test status is not presented as scientific evidence, a benchmark, or permission to execute.

## 5. Deliberately unresolved test-design choices

Test framework/language; schema parser and conformance dialect; property/fuzz testing strategy; deterministic replay fixture format; concurrency/clock fault injection; secret scanner/access-control policy; runtime sandbox and mock environment design; metric precision; test coverage target; and named engineering/security reviewer remain open. P6 sets no numerical test coverage threshold and does not run any test.
