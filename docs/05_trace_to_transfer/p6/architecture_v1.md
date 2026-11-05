# T2T-P6 Architecture Blueprint

**Blueprint ID:** `T2T-P6-Blueprint-v1.0.0-draft`  
**Subphase:** P6.1 — Architecture  
**Status:** complete for design/documentation scope; no implementation or authorization.  
**Normative dependencies:** [P2 object contract](../formal_skill_object.md), [P3 fair-replay contract](../p3/fair_replay_controls_v1.md), [P4 boundary algorithm](../p4/boundary_algorithm_v1.md), and [P5 protocol proposal](../p5/protocol_v1.md).

## 1. Design objective and invariants

Map the agreed object and method to component responsibilities, trust boundaries, data flow, runtime and baseline interfaces, and resource accounting. This is a conceptual architecture; it selects no programming language, storage engine, cloud, agent framework, evaluator integration, or exact deployment topology.

Invariants that every eventual implementation must preserve:

1. `CandidateVersion` is a non-executable hypothesis. Only a separately specified, versioned `SkillVersion` can reach the runtime gate; schema validity does not establish authorization or efficacy.
2. Prediction is immutable and pre-action; later observations and `EffectAssessment` are separate append-only records.
3. `UNKNOWN`, `NOT_APPLICABLE`, absent, and known false are not conflated. Unknown required applicability, compatibility, input, or budget blocks invocation.
4. Event/provenance and lifecycle history are append-only. Corrections append a new linked record; no semantic overwrite.
5. Source construction/refinement evidence, validation, confirmatory target data, and restricted outcomes remain purpose-separated. A refinement event cannot validate that version or its descendants.
6. Baselines and treatments use the P3/P5 common observation/action/retrieval/logging wrapper and matched declared resource opportunities. Costs are vectors, not a composite score.
7. Restricted/hidden/test outcome stores have no path to candidate-generation, refinement, threshold-selection, or runtime-agent components. This design does not grant any access.
8. Every invocation is subject to the controlling project authorization, official environment rules, P2/P4 fail-closed conditions, and prospectively frozen P5 resource limits. P6 itself supplies none.

## 2. Component diagram (logical)

```text
                    CONTROL PLANE / REFERENCE REGISTRY
       protocol + permissions + manifests + arm/config/version hashes
                                |
                         Authorization Gate
                                |
   +----------------------------+------------------------------+
   |                                                           |
SOURCE / FORMATION PLANE                              RUN PLANE
   |                                                           |
Permitted Source Adapter                         Shared Comparison Harness
   |                                             /                       \
Observation Normalizer / Provenance Projector  Candidate generators      Runtime arms
   |                                              Ginv / Grec         B0/R0/R1/I0/I1/I-rel
Append-only Event Journal <--------------------------- Decision/Prediction Gate
   |                                                           |
Ginv / Grec proposal pipelines                          Applicability + Binding
   |                                                           |
Candidate/Skill Registry + Lifecycle              PredictionRecord (freeze)
   |                                                           |
   +-- candidate review/specification -- Runtime Authorization Gate
                                                               |
                                                       Action/Fallback Gate
                                                               |
                                                        Environment Adapter
                                                               |
                                                       Observation/Transition
                                                               |
                                             Effect Assessment / P4 Triage
                                                               |
                                             Journal + Budget/Cost Ledger

RESTRICTED EVALUATION ZONE (separate authority and storage)
Permitted evaluator adapter -> outcome store -> authorized analysis export
                                     X  (no feedback to agents, formation,
                                        refinement, tuning, or baseline edits)

Analysis/report materializer reads only role-authorized, frozen run artifacts.
```

The arrows are logical data dependencies, not a networking or deployment plan. The crossed line is a prohibited feedback path. A future evaluator adapter may exist only under live official rules and separate written authorization; it is not part of any P6 implementation.

## 3. Trust boundaries and data classes

| Zone | Components/data | Trust rule and allowed flow |
|---|---|---|
| **T0 — Authority/configuration** | Access approvals, protocol/manifest references, arm and artifact hashes, allowed resource limits. | Read-only control inputs to gated components. Missing/ambiguous permission or version fails closed. No credentials embedded in protocol or event payloads. |
| **T1 — Permitted source ingress** | Authorized source-event adapter, original observation/action refs, source manifest, provenance. | Ingress enforces source role/access class and integrity checks. Raw source records remain distinct from normalized/derived values. No hidden/test/confirmatory outcome material accepted as source. |
| **T2 — Formation and versioning** | Normalizer, P4 proposal/triage services, candidate/skill registry, append-only evidence/lifecycle records. | May read only role-eligible evidence under P2/P4. Candidate records cannot be executed. Version edits produce successors; no in-place mutation. |
| **T3 — Runtime interaction** | Shared agent wrapper, baseline adapters, applicability/prediction gate, authorized SkillVersion runtime, environment gateway, fallback gate. | Receives only permitted decision-time observations and fixed configuration. Must write prediction before action. Environment writes are only through the budget/action gate. No evaluator answer or future event reaches this zone. |
| **T4 — Run journal and cost ledger** | Event envelopes, immutable references, ordered action/prediction/observation/cost/failure records. | Append-only, role-aware; immutable event values cannot be silently edited. Sensitive raw payloads may remain in a controlled artifact store and be referenced only by authorized readers. |
| **T5 — Restricted evaluation/outcome** | Official evaluator connection and answer-bearing or hidden evaluation artifacts, if separately authorized. | Separate credentials, storage, service identity, and access policy. Agent and formation services have no read path. Outputs leave only through an approved analysis/export procedure; never back into candidate/baseline/tuning paths. |
| **T6 — Analysis/reporting** | Frozen run-artifact readers and prespecified report materializer. | Read-only and allowlisted. Any permitted use of an outcome for successor refinement must append a role-use event and permanently remove it from validation eligibility for that successor/descendants; restricted/confirmatory outcomes remain prohibited for refinement. |

This is a logical separation specification, not a claim that any current system enforces these controls. Security architecture, threat model, storage encryption, retention, and access review remain unresolved engineering decisions.

## 4. Module contracts

| Module | Responsibility | Input → output contract | Failure behavior |
|---|---|---|---|
| **1. Authorization/config gate** | Resolve the approved work scope, P5 protocol version, data-role permissions, arm/config/model/evaluator references, runtime authorization and caps. | Pinned references + access decision → `READY` or reason-coded `BLOCKED`. | No defaults for missing permissions, caps, hashes, or runtime authority. `BLOCKED` means no data flow/action. |
| **2. Environment/source adapter** | Translate permitted external observations, action requests/results, transitions, and source artifacts into event-schema references. | External typed input → `ObservationRecorded`, `Action*`, `TransitionObserved` refs. | Preserve raw/normalized split; record protocol faults; never synthesize hidden values. Does not access evaluator internals. |
| **3. Event journal / artifact resolver** | Append immutable event envelopes, resolve event and artifact refs, enforce ordering and access roles, expose audit snapshots. | Event request → immutable event ref or explicit rejection. | No update/delete endpoint; corrections append superseding refs. Hash profile and durable backend are unresolved. |
| **4. Representation/normalization service** | Apply only pinned schema/normalizer and create derived observations with raw provenance. | Raw permitted observation ref + version → typed normalized fields and field-level availability. | Unknown/occluded/conflicting values stay tagged; unsupported versions block downstream use. |
| **5. Candidate proposal pipeline (P4)** | Generate/audit non-executable candidates from permitted source evidence under frozen P4 config. | Source manifest + pinned P4 config → alignment audits, support ledger, CandidateVersion refs and lifecycle genesis events. | On unresolved config/profile/permission, return blocked/hold; never guess thresholds or emit a runnable object. |
| **6. Candidate review / SkillVersion specification** | Record separate evidence-linked human/policy decisions and produce SkillVersion specification only from accepted candidate under P2. | Candidate ref + review/promotion decision → new SkillVersion ref or hold/reject. | No implicit promotion, validation, activation, or authorization; preserve actor/provenance and append-only lifecycle. |
| **7. Version/evidence registry** | Resolve immutable P2 objects, lineage, evidence snapshots, representation and policy compatibility. | Version ref → validated structural/provenance view (not scientific validation). | Missing/stale refs, invalid lifecycle path, digest mismatch or quarantined state reject/abstain. |
| **8. Shared comparison harness and arm adapters** | Provide two explicit surfaces: a source-only candidate-generation interface for `Ginv`/`Grec`, and a common runtime `DecisionRequest` interface for `B0`, `R0`, `R1`, `I0`, `I1`, and relation ablation. A `Grec` runtime baseline adapter for Claim E is a separately frozen component over its generated recurrence artifact, not the generator itself. | `CandidateBatch` or `DecisionRequest → ArmResponse`, each with event refs and cost deltas. Candidate predictions for Claim A use the same frozen prediction/abstention scoring interface without enabling action execution. | Unsupported arm/version, invalid response, budget exceedance or timeout becomes a logged failure/abstention; no unmetered retry. Candidate-generation output cannot be dispatched. |
| **9. Applicability/binding gate** | Apply the P2 tri-state predicates and typed slot-binding rules before prediction/action. | Frozen SkillVersion + current permitted observation → `APPLICABLE`, `REJECT`, or `ABSTAIN`, reasons and predicate refs. | Any unknown required predicate/binding, incompatible representation, inactive/quarantined skill or unknown cap blocks invocation. |
| **10. Prediction gate** | Construct and freeze P2 `PredictionRecord` before an action that depends on the predicted effect. | Applicable skill/arm, context, action and pinned model refs → immutable prediction ref or abstention. | Cannot create a valid prediction => do not dispatch dependent action; no probability semantics without pinned calibration. |
| **11. Action/fallback gate** | Enforce action permissions, declared budget, policy termination, mismatch stop, and only separately authorized fallback/deopt. | Action proposal + prediction ref + remaining budget → dispatch/result/fallback/abort event refs. | Stop at first mismatch, cap breach, stale state or tool failure; never silently retry or repair the skill. |
| **12. Transition/effect assessor and P4 triage** | Append local observed transition and compare it to the frozen prediction under pinned representation/comparator; triage using P4 and P2 enums. | Prediction ref + action/execution refs + post-observation → `EffectAssessment`/triage sidecar refs. | Unknown attribution remains unresolved; P4 fine-grained subtype stays in sidecar, P2 coarse enum unchanged. |
| **13. Budget/cost ledger** | Record declared caps, realized cost vector and provenance across formation, validation, retrieval, invocation, fallback and evaluation stages. | Stage/resource measurement → append-only `CostMeasured` event linked to run/arm/stage. | Missing units or counters are explicitly missing; unknown cap blocks execution. No inferred zero and no composite cost score. |
| **14. Evaluator adapter/outcome store** | Under separate authorization only, transfer the official output to a segregated evaluator and store its result. | Submitted authorized output → evaluator-versioned outcome ref in restricted zone. | Unauthorized access/connection is blocked and audited. No outcome feedback to the agent, candidate or baseline path. |
| **15. Analysis/report materializer** | Join only allowlisted immutable events and approved outcomes to produce P5 claim tables. | Frozen run snapshot + authorized analysis policy → versioned report artifact. | Missing/invalid required artifacts marks analysis incomplete; no hidden imputation, post-hoc exclusions, or endpoint switching. |

## 5. Data flow and object lifecycle

### 5.1 Formation path (permitted source data only)

1. Authorization/config gate resolves source manifest, purpose, permissions, representation/normalizer and P4 algorithm version.
2. Source adapter and journal record immutable permitted observations/actions/transitions and provenance; the normalizer emits separate derived field refs.
3. P4 proposal pipeline consumes only eligible source-role refs and pinned configuration. It emits audits, denominators, evidence snapshot refs and a non-executable `CandidateVersion`.
4. Candidate review/lifecycle records may accept a candidate for skill specification, reject, or hold under a separately frozen policy. A `SkillVersion` is a distinct immutable object; no candidate-to-runtime shortcut exists.
5. Validation, activation, and runtime use require separate decisions and approvals under P2/P5 and existing project gates. P6 implements none of these transitions.

### 5.2 Runtime path (future, only when separately authorized)

1. Authorization gate checks protocol/arm/run versions, role access, resource caps and explicit runtime permission.
2. The shared wrapper delivers the same request shape and decision-time observation/history to each baseline/treatment adapter.
3. Applicability/binding resolves only permitted observed fields. `UNKNOWN` causes abstention; a known false precondition causes local reject.
4. Prediction gate records a pre-action immutable P2 `PredictionRecord`. The action gate dispatches only an allowed action within the budget and links it to the prediction.
5. Environment adapter records actual dispatch/acceptance and later observation/transition separately. Effect assessor links but does not overwrite prediction with observation; P4 triage may produce a separate detailed sidecar.
6. Fallback is selected only from the P2-declared, separately authorized set and reserved budget; absent an eligible fallback, terminate with abstain/no-op/abort as specified.
7. Cost, failure, stop, and lifecycle events are appended. Evaluator outcomes remain in separate storage.

### 5.3 Evaluation/report path

A future separately authorized evaluator run emits results to the restricted evaluation zone. An authorized analysis job may read only the specified immutable outputs and must retain the complete assigned/attempted denominator. It cannot send outcomes to candidate generation, method/baseline updates, metric/threshold selection, or a subsequent confirmatory run. Any future allowed refinement with permitted nonrestricted validation data requires a new event-use record and invalidates that event for validation of the successor and descendants, as P4/P5 specify.

## 6. Shared interfaces (conceptual, not code)

Names below are interface labels, not implemented APIs or a selected programming-language signature. Exact wire encoding and input sizes remain open.

| Interface | Required request | Required response |
|---|---|---|
| `prepare_run` | Authorized protocol/config refs, arm set, manifest-role refs, model/evaluator refs when permitted, and budget contract ref. | `READY` with resolved immutable refs or `BLOCKED` with reason list. |
| `propose_candidates` | Permitted source manifest ref, pinned representation/normalizer/P4 config refs, source-only budget ref. | CandidateBatch refs: alignment audits, support ledgers, zero or more non-executable CandidateVersions, and explicit block/failure state. |
| `review_candidate` | CandidateVersion ref, evidence snapshot, review policy, actor class and append-order context. | Append-only lifecycle decision plus optional accepted-for-specification outcome; never an executable skill. |
| `specify_skill` | Accepted CandidateVersion ref, typed binding/applicability/effect/policy/termination/fallback specification, resource refs. | Immutable SkillVersion ref in `DRAFT` or blocked result; no validation/activation implied. |
| `decide` | `DecisionRequest`: run/arm/version refs, latest allowed observation/context refs, action/step/time/compute remaining, common interface/config refs. | `ArmResponse`: typed prediction or explicit `ABSTAIN`/`REJECT`/failure, optional proposed action, immutable event refs, and cost delta. |
| `assess_effect` | Pre-action PredictionRecord ref, actual dispatched/accepted action refs, post-observation/transition refs and pinned effect comparator. | P2 `EffectAssessment` or unresolved status and, if justified, a separate P4 triage sidecar ref. |
| `fallback_or_stop` | Failure/mismatch/cap event, authorized fallback ref (if any), remaining reserved budget. | Authorized fallback action under its own checks, else `ABSTAIN`/`NO_OP`/abort with reason; never a silent retry. |
| `record_cost` | Resource dimension, amount/tagged availability, unit/method, scope/stage, arm/run refs, cap ref, measurement provenance. | Immutable `CostMeasured` ref or reason-coded missing measurement. |
| `evaluate` | Authorized submission/output and evaluator access grant, track-specific evaluator contract. | Restricted evaluator outcome ref and audit record; no direct agent response. |

### Common arm request/response semantics

`DecisionRequest` carries identical permitted observations/context for the compared arms, plus immutable run/arm/representation refs and the applicable budget. Treatment-specific access is limited to the explicitly named relation/guard component. `ArmResponse` must distinguish:

- `PREDICTION`: a P2-compatible prediction ref frozen before action/result;
- `ABSTAIN`: insufficient/unknown/incompatible information or a deliberate supported abstention;
- `REJECT`: a known false applicability/precondition for this context (not global skill rejection);
- `FAILURE`: parser/tool/runtime/resource/integrity problem with a reason and preserved event refs.

A proposed action is separate from the prediction. Only the action gate can dispatch it. Baselines may not silently omit prediction or cost logging when those are required by the P5 comparison.

## 7. Candidate-generation and runtime adapters

P5 separates candidate-generation methods from runtime decision arms. The architecture preserves this distinction: generation produces non-executable candidates and audits; an independent, frozen scoring interface evaluates candidate predictions for Claim A. Runtime arms receive the common `DecisionRequest` interface. If `Grec` is also used as a Claim E task-performance baseline, its candidate-generation role and its separately specified runtime adapter must be frozen as distinct artifacts before any future evaluation.

### Candidate-generation surface

| Generator slot | Architecture adapter | Boundary enforced |
|---|---|---|
| `Ginv` | P4 candidate proposal pipeline using the pinned P2 relation/template configuration. | Source-only formation; outputs CandidateVersions/audits, never executable policies. Exact generator configuration is future work. |
| `Grec` | Frozen non-invariant recurrence/motif miner over the same permitted source evidence. | Candidate-generation comparator for Claim A; cannot silently use P2 invariant semantics. Exact algorithm/config is a future freeze-gate choice. |

For Claim A, predictions from both generators are assessed through the same frozen prediction/abstention interface on the same permitted held-out contexts. Candidate counts, proposed artifacts and failures remain separate from prediction quality. Any runtime realization of recurrence for Claim E is another explicit adapter and may not be assumed from a candidate record alone.

### Runtime comparison surface

All runtime arms share the same outer observation, query/retrieval, action, fallback, event and budget interface. They are strategy modules behind a common wrapper, not separate harnesses.

| Arm slot from P5 | Architecture adapter | Boundary enforced |
|---|---|---|
| `B0` | Base agent without T2T/replay skill library. | Same wrapper/context/action/resources; no learned T2T skills. |
| `R0` | Exact ordered fixed-trace replay adapter. | Literal source assumptions; mismatch stops/abstains per P3; diagnostic only. |
| `R1` | Strong compressed/typed-slot trace replay adapter. | P3 frozen rules, same source/model/retrieval opportunities, no learned invariant boundary. Independent competence review remains a future gate. |
| `I0` | Invariant relation/prediction adapter with boundary updates fixed. | Primary Claim N treatment; P2 object semantics, P3 controls. |
| `I1` | I0 plus the P4-defined counterexample-boundary update factor. | Claim B/C/E arm; no Claim N attribution to this factor. |
| `I−rel` | I0 wrapper with explicit relation semantics replaced by the pinned R1-compatible representation. | Relation ablation; preserve wrapper, slots, retrieval and budget as far as feasible. |

The tables specify interfaces only; no baseline, generator or treatment is built. If an arm cannot meet the interface/resource contract, the corresponding future claim is `NOT_TESTED`/`INCONCLUSIVE`, not replaced silently.

## 8. Resource and budget accounting proposal

The P3/P5 resource vector is carried as a typed ledger; P6 chooses no numeric cap, unit convention, exchange rate, amortization horizon or parity tolerance.

| Cost stage/dimension | Minimum accounting record |
|---|---|
| Source exposure / preprocessing | permitted manifest ref, event and byte counts where available, annotations, conversion/normalization and producer refs. |
| Candidate creation / review | arm/candidate refs, tool/model calls/tokens, CPU/GPU/compute, wall time, manual review labor if measured, failures and missing fields. |
| Validation | immutable version and data-role refs, calls/tokens, compute/time, review/adjudication costs; role-use events for any later refinement. |
| Storage / retrieval | artifact/index version and bytes, cap ref, query/candidate counts, retrieval latency/compute, cache state. |
| Invocation | per-decision and per-episode calls/tokens, compute/time, memory/context, actions, retries, stop/fallback and failures. |
| Environment/evaluator | attempted/accepted actions, reset/retry use, evaluator version, output and authorized evaluator cost where available. |

Each cost measurement includes `resource`, `amount` or typed unknown, `unit_ref`, `measurement_method_ref`, `scope`, `stage`, `arm_ref`, `run_ref`, `cap_ref` or explicit `NOT_APPLICABLE`, `observed_at`, producer and provenance refs. Report declared caps and realized use separately. Do not silently convert unknown to zero or combine vector components into a score.

**Parity check:** arm comparisons are eligible for a matched-resource interpretation only when the prospectively frozen resource dimensions/opportunities and cap references resolve for every arm. A missing cap blocks execution; unequal or unknown realized usage is reported and may make the comparison inconclusive under P5. No padding, uncharged retries, hidden calls, or post-outcome selection of a favorable resource point.

## 9. Alternatives considered (not selected)

| Choice | Design position | Why / what remains open |
|---|---|---|
| Single monolithic agent module vs separated services | Prefer responsibility separation and shared typed interfaces. | Keeps data, inference, action, evaluation and audit boundaries reviewable. Physical service/process split is unresolved and may be one process initially if it preserves logical controls. |
| Mutable database rows vs append-only semantic events | Require immutable versioned objects and append-only event history. | Consistent with P2/P4; exact event store, transaction model, retention and tamper evidence are unresolved. |
| One harness per arm vs common wrapper | Require common wrapper and arm plug-in boundary. | Needed for P3/P5 fairness; treatment-specific logic is the declared relation/boundary factor. |
| Unified outcome store vs separated evaluation store | Require logical and access-control separation, with no feedback path. | Protects source/target separation; exact physical isolation and export controls require security review. |
| Fixed numeric budget now vs reference-based cap contract | Keep values `UNSET`; require future P5-authorized cap refs. | P5 explicitly leaves caps unset; P6 must not invent them. |

## 10. Non-goals and unresolved questions

No CGM controller, “intelligence growth” score, concept graph, recursive self-improvement, new model training, skill composition, multi-agent system, automatic policy promotion, or Phase 2I/3B/3D integration is included. The architecture does not grant permission to build, deploy, run, submit, or access outcomes.

Open decisions include programming language/runtime; package boundaries and deployment topology; event journal/database and object-store design; approved identity/canonicalization/hash profile; schema registry and migration policy; access-control/secret management, encryption, retention and threat model; operational monitor and audit owner; model/checkpoint and environment adapter; official evaluator integration; concrete R1 competence-review process; cost units/caps and parity rules; and named implementation/security reviewers. Owner review and separate authorization are required before any engineering work.
