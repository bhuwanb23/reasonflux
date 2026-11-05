# T2T-S3-R v1 — Implementation Readiness Review

**Review date:** 2026-11-04  
**Package reviewed:** `T2T-S3-I-v0.1.0`  
**Review type:** static implementation/specification review; no S3 run or context scoring  
**Disposition:** **BLOCKED for execution readiness**  
**Claim N:** remains **N-BLOCKED from S2; S3 undecided**

## Executive finding

The world and I0 implementation closely match the stated relational rule, and the R0–R3 components largely match the *current as-implemented* plan. The package is internally hash-consistent. However, **R4 competence and fairness as the strongest primary comparator are not established**. R4 is a six-Boolean exact source-row lookup: it predicts only feature vectors observed during fitting and abstains on every unseen or conflicting vector. The two-trace development fixture shows it can distinguish one relation-valid row from one relation-invalid row; it does not establish that R4 is a competent strongest compiler for a future suite, nor that the future suite's eligible feature vectors are source-covered.

The source/development/held-out cells and role manifest are also not defined, the independent competence reviewer is unassigned, and the package has no aggregate all-context/per-cell scoring implementation. Thus this is **not READY**. Since the primary-comparator question is central to Claim N, the overall disposition is **BLOCKED**, not merely a routine implementation pass with execution approved. No execution is authorized by this review.

## Review boundary and method

This was a code-and-document inspection of the frozen implementation candidate, test file, plan, review packet, and freeze manifest. It did not generate or inspect held-out contexts, call the S3 predictors on an S3 suite, calculate outcomes, or decide Claim N. The reported `7 passed` is the previously recorded development-fixture software test result only; repository-wide tests were not run.

**Reviewer independence:** this review was performed by the same Arena agent that authored the implementation. It is an explicit self-review, **not** the independent competence review required by the plan. R5 therefore remains unsatisfied.

## R1 — World fidelity: PASS, with bounded caveats

**Evidence:** `src/t2t_s3/world.py` and development-fixture tests.

- State and action use visible object records, typed roles, explicit key-to-target references, target closed/open state, coordinates, agent position, and path-clear status. No hidden simulator state is present in the transition path.
- A complete state with a known failed precondition yields exact no-effect. An incomplete required field makes `step` return `None`; I0 abstains. The tests distinguish unknown path status from known absence of a key.
- The success condition is the planned conjunction: selected object is a key, its reference names the selected target, selected target is closed, agent is adjacent, and path is clear.
- Partial outcomes are rejected; the interface supports success and exact no-effect only.

Caveats to retain for future protocol review: color/shape are stored but not transition-required; invalid/dangling relations are treated as known non-success by the simulator and rejected in source-trace validation. Also, `context_id` is present in `UnlockState` and R0's exact signature, but the plan does not say whether that identifier is an observable input or logging-only metadata. If it is logging-only, R0 currently uses a hidden context-identity side channel and must be changed to compare only permitted observations. The transition function itself does not use `context_id`. The transformation utility also permits arbitrary color/shape mappings rather than enforcing a bijective permutation (see R4 Freeze/Transform notes).

## R2 — Replay ladder fidelity: PARTIAL

| Arm | Finding | Review status |
|---|---|---|
| R0 | Uses literal context ID, ordered state signature, and action IDs; mismatches abstain. This is consistent with exact raw replay only if `context_id` is an observable source-context check; otherwise it is a metadata side channel. Duplicate exact records are collapsed to one stored source ID. | CONDITIONAL; observability must be specified. Tighten source-manifest accounting. |
| R1 | Rebinds typed key/target IDs, checks target-closed, adjacency, and path-clear, and deliberately omits the unlock relation. This is consistent with the declared parameterized macro. It fits its expected success from positive traces only and stores only those positive trace IDs, even though `fit` receives all traces. | PARTIAL: behavior matches the declared weak arm, but provenance/source-manifest accounting is incomplete. |
| R2 | Deduplicates exact state/action/effect signatures and records unique/source counts; it delegates predictions to R1. The one-action world has no subsequences to compress, as documented. | PASS for the declared one-step scope; source IDs inherit R1's positive-only limitation. |
| R3 | Exact lookup by the five unary Boolean features; conflicting rows and unseen rows abstain. | PASS against the current as-implemented specification; it is a bounded table, not a general action/control-flow synthesizer. |
| R4 | Exact lookup by the six unary-plus-relational Boolean features; conflicting/unseen rows abstain. | **BLOCKED on competence/fairness**; see R5. |

`validate_trace` rejects non-synthetic provenance and incomplete/dangling traces, but it does not bind a trace to a `SOURCE` versus `DEVELOPMENT` role or prove that an observed label was emitted by the frozen world. The eventual run harness needs explicit role/provenance enforcement and one shared manifest across arms.

## R3 — I0 fidelity: PASS

**Evidence:** `I0Invariant` in `src/t2t_s3/arms.py` and the world rule in `world.py`.

I0 uses the planned typed relation and required visible context; it does not fit an outcome table. It independently checks the relation, target state, adjacency, and path condition, and its fit step rejects source labels inconsistent with the predeclared relation. Unknown required state is handled as abstention. No extra predictive predicate beyond the planned relation/preconditions was found. The development test verifies only a tiny software fixture, not general correctness over any evaluation suite.

## R4 — Freeze integrity and scoring: PARTIAL for implementation; NOT READY for execution

- Recomputed SHA-256 values match **12/12** files listed in `freeze_manifest.json`. The list includes the S3 package modules, focused test, and main S3 protocol/review/index documents. The manifest explicitly excludes its own hash.
- `eventlog.py` is hashed and includes prediction, per-context score, fit, and deviation event constructors. Prediction logging omits observed outcomes, and scoring treats wrong/abstain/invalid/missing as zero.
- The package does **not** implement an aggregate all-context denominator/accuracy calculator, per-cell denominator/coverage/error report, or a run-level integrity/role gate. A single `score_event` is not the complete S1 reporting procedure. Those specifications remain in documents, not executable scoring code.
- Source/development/held-out manifests, transformation-cell assignments, run configuration, resource vector/caps, and authorization record are explicitly unset. This is honest and correct for no-run scope, but it means the manifest is an **implementation candidate freeze**, not an execution freeze.
- The transformation code supports ID maps, appearance maps, isometric layout changes, order reversal, and distractors. It does not enforce that color/shape maps are permutations, and it has no explicit general coordinate-permutation map. Its present test checks one isometry and fresh IDs, not all transformation categories.
- There is a small document inconsistency: S3 plan §4 says no learned R3/R4 tie-break is needed for the truth-table implementation, while §6 checklist item 2 still asks to freeze tie-breaks. Resolve that before any preregistration/run package is finalized.

## R5 — Competence review: NOT PASSED

The existing fixture establishes a narrow positive capability: R4 can use the relation feature to distinguish two source rows that have identical unary features. It also correctly abstains on an unseen six-feature row. That is useful software evidence, but it is not an independent review or evidence that R4 is the strongest fair source-derived comparator for the future evaluation.

The key limitation is structural: R4 has no rule induction or generalization across Boolean rows. It can store arbitrary labels for rows it has seen, but on any unseen six-bit row it abstains. Because abstentions score zero, the future source opportunity and eligible held-out cells determine whether this creates a competent comparator or a systematic baseline coverage penalty. Those cells are not assigned. Therefore, the answer to “Can R4 express everything it is supposed to express?” is currently **only for source-observed rows; not established for the planned Claim N domain**.

This limitation is not a reason to weaken R4 or tune it toward an N pass. If a fair, competent R4 reproduces I0, that is a valid N-FAIL under the plan. The unresolved issue is whether this particular table lookup is the fair, strongest comparator, not whether it is sufficiently weak or strong to produce a preferred result.

## R6 — Holdout design: NOT FROZEN; no exposure occurred

No source, development, or held-out transformation cells or role manifest exist in the package. No held-out contexts were generated or exposed, so no S2-style reuse is identified. However, disjointness, eligible contexts, denominator, feature-row coverage, and leakage checks cannot yet be verified. This gate remains open by design and blocks execution.

## Readiness matrix

| Gate | Result | Consequence |
|---|---|---|
| R1 World fidelity | **PASS** | No world rewrite indicated by this review. |
| R2 Replay ladder fidelity | **PARTIAL** | R0–R3 match the as-implemented spec; improve complete source-manifest/provenance accounting before run. |
| R3 I0 fidelity | **PASS** | I0 matches the stated typed relation. |
| R4 Freeze/scoring | **PARTIAL / NOT RUN-READY** | Hashes are valid; suite, role gates, aggregation/reporting and some transform constraints remain absent. |
| R5 Competence review | **NOT PASSED** | Independent reviewer unassigned; R4 generalization/fairness unresolved. |
| R6 Holdout design | **NOT FROZEN** | No source/development/held-out manifest or cells. No exposure occurred. |
| **Overall** | **BLOCKED** | Do not authorize S3 execution. |

## Required resolution before a new readiness decision

1. Have a reviewer independent of the implementation assess whether the six-feature R4 table is a fair strongest comparator for the prospectively eligible suite. If not, revise R4 prospectively (for example, to a frozen source-only Boolean-script/compiler with a deterministic complexity/tie rule) or revise the estimand/suite under explicit owner review; do not choose based on any S3 outcome.
2. If retaining the current exact-row lookup, prospectively define source opportunity and eligible test cells so R4 competence/coverage is assessable; define how unseen rows are handled and keep every abstention in the denominator. Do not silently exclude unseen rows.
3. Bind every arm to the same immutable source manifest and explicit source/development/test roles; preserve all source trace IDs in fit/provenance logs, not only positive traces.
4. Freeze the actual finite transformation cells and leakage checks, including whether appearance maps are bijective and the exact layout transformations. Do not assign counts or caps by guess.
5. Complete the executable all-context and per-cell scoring/reporting path, or formally designate and verify a separate scorer; test score-event handling without creating an S3 evaluation suite.
6. Resolve the plan's tie-break checklist inconsistency, refresh code/config/test hashes for any revision, and obtain independent sign-off.
7. Only after these gates pass, request a separate explicit S3 run authorization.

**Current stop:** review complete; execution remains unauthorized. No S3 data or outcomes were generated in this review.
