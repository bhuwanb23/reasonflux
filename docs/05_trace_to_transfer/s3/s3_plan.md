# T2T-S3 Plan — Claim N Resolution Program

**Plan ID:** `T2T-S3-ClaimNResolution-v1.1.0`  
**Scope decision:** user authorized **plan and implementation, no run**. The implementation is synthetic mechanism code plus development-fixture verification only; no S3 evaluation, held-out-context generation/exposure, outcome calculation, or Claim N decision is authorized.  
**Date:** 2026-11-04.

## 1. Purpose

Resolve one question only:

> Can the predeclared invariant representation I0 achieve higher all-context exact one-step effect-prediction accuracy than the strongest fair source-derived replay/compiler R4 on fresh synthetic contexts?

S2 showed why this needs a clean test: a weaker baseline yielded an apparent advantage; after strengthening replay and reusing the exposed holdout, the result tied. S3 prevents that sequence by freezing R0–R4, I0, source evidence, transformation cells, scoring, and the analysis rule before the held-out suite is evaluated.

S3 does **not** test B, C, D, or E. The S2 toy B result remains a finite fixture observation only.

## 2. Hard scope and authorization boundary

### Proposed S3 scope

- One deterministic synthetic relational-object world.
- One invariant family and one action/effect interface.
- A replay ladder R0–R4, with one primary comparator (R4).
- Predeclared source/development/test roles and a finite surface-transformation suite.
- The S1 all-context exact effect-prediction accuracy endpoint.

### Explicitly excluded

- ARC, AGI-3, Mini-ARC, competition data, task IDs, split files, evaluator, leaderboard, models, network, restricted/hidden outcomes, live environments, benchmarks, paper submission, and Claims B–E.
- Full skill ecosystem, promotion/lifecycle system, boundary updates, SCT, CGM, candidate yield, or broad agent behavior.
- Any S3 evaluation run, held-out-context generation/exposure, outcome calculation, Claim N decision, or assignment of source/development/held-out roles under the current implementation-only scope.

This plan does not change P3/P5 contracts or the P1 novelty no-go. The current authorization covers implementation and development-fixture software checks only; S3 remains synthetic mechanism testing, and execution requires a separate authorization.

## 3. S3.1 — Harder synthetic world proposal

### Candidate world: Relational Unlock World

Use one small deterministic world with typed objects and actions. A state contains:

- a set of object records with arbitrary `object_id`, visible role/type, optional appearance fields (color/shape), and coordinates;
- a key-like object with a visible `opens_target_id` relation;
- one or more closed target objects;
- agent adjacency and path-clear fields; and
- no hidden state used by either predictor or simulator.

The single true transition rule is:

`USE(object_id, target_id)` opens and advances exactly when the selected object is a usable key, its `opens_target_id == target_id`, the target is closed, the agent is adjacent, and the path is clear. On a complete observable state, a failed predicate yields exact no-effect; if a required field is unknown/incomplete, the simulator returns unknown and predictors abstain rather than treating unknown as false.

The one candidate invariant family is the typed state/action/effect relation:

`matching unlock relation + required observable context → open target and advance`.

The relation is fixed before implementation; S3 does not test open-ended candidate discovery. It tests whether this representation gives any predictive increment over replay/compressed/compiled scripts derived from the same demonstrations.

### Surface transformations

Predeclare transformations that preserve the transition rule while changing surface realization:

- rename every object ID, including fresh IDs never seen in source traces;
- permute colors and shapes independently of the unlock relation;
- translate/rotate or permute coordinates while preserving adjacency/path facts;
- reorder object records and change which visual object occupies each spatial role; and
- add distractor objects that do not alter the relation or the effect.

Include both applicable and non-applicable contexts: valid unlocks, wrong-key/wrong-target pairs, no key, open target, non-adjacent actor, blocked path, and ambiguous/missing required fields. Unknown or ambiguous required values must trigger abstention, not be filled from hidden state.

### Source/holdout separation

Construct source and held-out contexts from disjoint transformation cells, not merely new IDs over identical feature tuples. I0 and every replay arm receive the same source traces and observable schema. Reserve entire combinations of surface transformations for held-out evaluation. A source event used in construction cannot also validate that version. The recipe-level cell/role manifest is recorded in [`transformation_cells_v1.json`](transformation_cells_v1.json): canonical source, development software fixtures, and held-out surface families are distinct. No context IDs, contexts, counts, or sample sizes are assigned/materialized. Unknown-required-state diagnostics lack a simulator outcome under the no-hidden-state world and are excluded from the primary scored cells unless the owner prospectively revises the world/scoring contract.

## 4. S3.2 — Replay expressivity sweep

Implement and freeze the following ladder from weakest to strongest. Every rung sees the same source experience, observation/action/effect schema, wrapper, prediction timing, holdout, and declared resource opportunities.

| Arm | Permitted representation | Diagnostic purpose |
|---|---|---|
| **R0 Raw Replay** | Exact ordered source trace with literal values and source-context checks; stops/abstains on mismatch. | Exact playback reference only. |
| **R1 Parameterized Replay** | R0 plus typed slots, deterministic object-ID rebinding, and fixed field/type correspondences. | Measures ordinary slot binding. |
| **R2 Compressed Replay** | R1 plus lossless deduplication, shared subsequences, and trace compression. | Measures compression/storage effects. |
| **R3 Grammar Replay** | Exact source-derived decision table over the five frozen unary predicates; conflicting rows and unseen feature vectors abstain. | Measures a bounded one-step unary decision grammar, not general program synthesis. |
| **R4 Replay-Max** | Minimum source-consistent binary decision tree over the five unary predicates plus the direct key-to-selected-target relation predicate; each predicate is tested at most once per path; fixed complexity/tie-break; supports all Boolean functions over this six-feature grammar. | **Primary Claim N comparator.** Strongest compiler in the frozen six-Boolean grammar; tests whether a source-derived script can reproduce the I0 relation. |

The implemented R3 table and R4 minimum decision-tree compiler, including deterministic tie-breaking and unknown-state abstention, are specified below. The R4 hypothesis class represents every Boolean function over the six frozen predicates; fitting and tie-breaking use source labels only. Source trace counts/opportunity details and the resource vector remain unset and must be frozen before any S3 run. R4 may not use held-out target labels, counterexample updates from held-out contexts, hidden state, future events, or outcome-based rule selection; source effect labels are the permitted fitting input. Do not call R4 “weak” merely because it matches I0. If it reproduces I0, N fails under this program's criterion.

#### Implemented arm algorithms (version 1)

- **Shared fitting input:** an explicit tuple of complete synthetic source traces, unique trace IDs, visible state/action, and observed one-step effect. Fitting accepts `SYNTHETIC_SOURCE` by default; software fixtures require explicit `allow_development=True`. The fitter rejects duplicate IDs, incomplete states, dangling key relations, unsupported partial effects, development traces without the opt-in, and non-synthetic provenance. No run-specific context manifest or counts are assigned.
- **R0:** dictionary replay on exact ordered observable state signature + literal action IDs. `context_id` is logging/provenance metadata only and is excluded from every predictor input. Identical signatures with conflicting effects are rejected; any observable mismatch abstains.
- **R1:** a fixed typed key/target slot macro. It rebinds caller-supplied IDs by visible roles and checks target-closed, adjacency, and path-clear; it intentionally omits the `opens_target_id` relation test. Missing/unknown bindings abstain. The expected effect is taken from positive source traces, while prediction/fit provenance retains the full shared source trace-ID manifest.
- **R2:** lossless deduplication of exact one-step source templates and the same R1 predictor. This world has one action per trace, so R2 cannot claim sequence/subsequence savings; it records source and unique-template counts.
- **R3:** exact source-derived decision table keyed by the five unary Booleans, in this fixed order: `key_is_key`, `target_is_target`, `target_closed`, `agent_adjacent`, `path_clear`. A feature vector observed with one source effect maps to that exact effect. Conflicting source effects for the same vector mark that row ambiguous; prediction abstains on an ambiguous row or any unseen vector. This bounded one-step grammar is not a general program synthesizer.
- **R4:** source rows are six-bit vectors over the five R3 predicates plus `key_unlocks_selected_target`. Conflicting labels for an identical vector are rejected. Compile the minimum-node binary decision tree consistent with all source rows; each predicate may be tested at most once per path. Minimize internal test nodes; among ties choose the lexicographically smallest recursive tree serialization using the declared feature order and false-branch before true-branch order. Leaves emit exact success or no-effect. This fixed tree grammar represents every Boolean function over the six predicates and classifies unseen feature vectors through its learned branches. Unknown required state and dangling relation references abstain before tree evaluation. The development-contrast fixture verifies the conjunction's source-only compilation over all 64 abstract feature vectors; it is a software competence check, not an S3 outcome.
- **I0:** direct typed relation evaluator: selected object is a key; selected object references the selected target; target is closed; actor is adjacent; path is clear. Fit validates source labels against that predeclared relation; prediction uses no fitted outcome table.

The development-fixture check establishes only that these implementations behave as declared. It is not an S3 context suite, does not set a source/held-out split, and cannot establish competence on any future S3 evaluation suite.

### Competence and freeze review

Before S3 execution, a reviewer independent of I0 construction must verify that R0–R4 implement their declared capabilities, share the same inputs and source manifest, use no target outcomes, and log all predictions/abstentions/costs. Freeze source manifests, code/config hashes, predicate grammar, arm outputs, selection rule, and the complete R0–R4 ladder before exposing held-out labels. Any necessary post-result upgrade requires a new S3 version and a fresh held-out suite.

## 5. S3.3 — Representation stress tests

The held-out suite should cross the same invariant with different surface realizations. Predeclare a finite transformation matrix with:

- **Identity shift:** all test object IDs are unseen/reassigned.
- **Appearance shift:** colors and shapes change independently of functional relations.
- **Role/layout shift:** object listing order and coordinates change while typed roles/relations remain visible.
- **Compositional shift:** combine transformations held out individually or jointly, if such combinations are part of the frozen suite.
- **Negative controls:** visually similar but relation-invalid object pairs; matching-looking distractors; and action precondition failures. Unknown-required-state cases are abstention-contract diagnostics only, not eligible scored contexts, because the no-hidden-state simulator returns no exact effect label for them.

Report exact prediction accuracy across all eligible contexts using S1 scoring (correct=1; wrong, abstain, invalid, or missing=0), together with per-transformation-cell denominators, coverage, and error types. Do not pick only favorable transformations after results. No composite score is allowed.

A predeclared relation-stripped I0 ablation may be included only if it does not multiply the S3 scope; if included, state exactly which component is removed and retain the same wrapper/resources. Otherwise defer it rather than adding it after the result.

## 6. S3.4 — Claim N preregistration template and decision rule

### Primary estimand

Use S1's single primary endpoint: **all-context exact one-step effect-prediction accuracy**, over the same fresh held-out contexts for I0 and R4. Every eligible context stays in the denominator; abstentions, invalid/missing predictions, and failures score zero. Report R0–R3 on the same contexts as the expressivity ladder, but the primary N contrast is **I0 vs R4**.

`Delta_N = Accuracy(I0) - Accuracy(R4)`

### Finite-suite decision rule

If the test set is an exhaustive, fully specified deterministic finite suite, classify:

- **N-PASS:** `Delta_N > 0` across that frozen suite.
- **N-FAIL:** `Delta_N <= 0` (tie or lower) across that suite.
- **N-BLOCKED:** baseline/arm changed after held-out exposure; source/target roles overlap; the comparator is invalid; required fields are unobservable; or integrity/protocol deviation prevents interpretation.

This is a finite-domain conclusion only. Any stochastic/population claim requires a separately frozen inferential criterion, uncertainty method, and meaningful-effect threshold. Alpha, effect margin, sample size/power, resource caps, and any stochastic sampling plan remain **UNSET**; do not guess them or treat the finite-suite result as an ARC population estimate.

### Preregistration checklist

Before any S3 run is authorized, freeze:

1. exact world transition function, state/effect schema, invariant relation, and object identity/normalization rules;
2. R0–R4 algorithms, the fixed predicate grammar, tie-breaks, source-only selection rule, and R4 competence review;
3. source/development/held-out transformation cells and leakage checks;
4. I0 fit/prediction procedure and freeze point;
5. S1 accuracy metric, full denominator, abstention/error scoring, and all per-cell reporting;
6. deterministic-suite or inferential decision rule and valid/inconclusive/blocked outcomes;
7. resource accounting and any caps (currently unset); and
8. explicit synthetic-only authorization, code/test scope, and stop rules.

## 7. S3.5 — Stop and decision conditions

- If R4 matches or exceeds I0, record N-FAIL for the frozen finite suite; do not upgrade the invariant claim or weaken R4 after outcomes.
- If I0 beats R0/R1 but not R3/R4, the evidence supports only ordinary parameterization/compression/program compilation, not invariant-specific value.
- If a baseline can represent the same relational rule with a bounded script, report the functional equivalence; do not claim the formal object itself adds predictive value.
- If I0 exceeds R4 only on a post-hoc subset, with more abstention counted away, or on transformation cells used for fit, mark the test invalid/inconclusive.
- If N remains blocked or fails across a valid S3, invoke the S1.1 outcome policy: narrow or terminate the current T2T direction. A B toy pass does not rescue N or establish a publishable boundary-only contribution under P1's prior-art decision.

## 8. Deliverables and current status

### Implementation package outputs

- `src/t2t_s3/` — deterministic world, minimum Boolean decision-tree R4, I0, deterministic surface recipes, per-context/per-cell scorer, and append-only event construction.
- `tests/t2t/test_t2t_s3_mechanism.py` — development-fixture software checks only; not an S3 evaluation suite.
- `docs/05_trace_to_transfer/s3/transformation_cells_v1.json` — recipe-level, finite cell/role definitions; no contexts or counts materialized.
- `docs/05_trace_to_transfer/s3/competence_review.md` — independent-review packet; reviewer remains unassigned.
- `docs/05_trace_to_transfer/s3/freeze_manifest.json` — implementation/protocol hashes and unresolved run-gate fields.
- `docs/05_trace_to_transfer/s3/s3_review_v1.md` — historical S3-R v1 BLOCKED finding.
- `docs/05_trace_to_transfer/s3/s3_ra_resolution.md` — focused R4/observability/scoring/cell-resolution record.

### Current authorization and status

S3-RA implementation-only work and development-fixture software checks are complete. Recipe-level source/development/held-out roles are defined, but no contexts, split IDs, sample sizes, or outcomes have been created. No S3 evaluation, held-out-context generation/exposure, outcome calculation, or Claim N decision has occurred or is authorized. Independent comparator review, final run-specific counts/config/resources, owner confirmation on unknown-required diagnostics, and separate execution authorization remain required. Claim N therefore remains **N-BLOCKED** based on S2; Claims C/D/E remain untested; the S2 finite B result remains narrowly scoped.
