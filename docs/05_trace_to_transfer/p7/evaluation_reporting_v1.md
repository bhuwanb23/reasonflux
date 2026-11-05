# T2T-P7 Evaluation and Reporting Plan

**Plan ID:** `T2T-P7-EvalReport-v1.0.0-draft`  
**Status:** complete for design/documentation scope, 2026-11-04.  
**Authority:** not code/implementation approval, preregistration, experiment/benchmark/ARC-run approval, split assignment, or permission to access restricted outcomes.

## 1. Purpose and controlling inputs

This plan provides a claim-linked decision vocabulary, result-table shell, failure/cost accounting, and reproducibility/submission checklist. Its aim is transparent reporting of evidence **if** a future, separately approved run exists. It reports no new results.

Controlling inputs: [claim-evidence map](../../../reports/competition/arc_prize_2026_claim_evidence_map_v1.md); [P2 skill-object contract](../formal_skill_object.md); [P3 fair-replay contract](../p3/fair_replay_controls_v1.md); [P4 boundary algorithm](../p4/boundary_algorithm_v1.md); [P5 protocol proposal](../p5/protocol_v1.md); [P6 architecture/event/test design](../p6/README.md); and [current evidence ceiling](../current_evidence.md). Existing Phase 2I, Phase 3B/3D, hidden-outcome, candidate-yield, data-integrity, and no-run restrictions remain controlling.

The current ceiling is unchanged: Claim A has limited known-generator synthetic support, not ARC-AGI-3 evidence; Claims N/B/C/D/E are untested for the proposed ARC-AGI-3 method. P1's standalone novelty no-go remains; the comparative reframe is provisional and not novelty-cleared. Synthetic, ARC-AGI-2, Phase 13/14, contract/schema/test, and readiness results must not be represented or pooled as ARC-AGI-3 evidence.

## 2. Decision states and evidence gate (P7.1)

Keep **run validity** separate from **claim decision**. A report includes both; no single label can hide an invalid run or the absence of evidence.

### 2.1 Run validity

| State | Meaning | Reporting consequence |
|---|---|---|
| `NOT_RUN` | No matching authorized run artifact exists. | No empirical result or claim language; retain the design-only status. |
| `VALID` | Required protocol, data-role, arm, evaluator, assignment and audit artifacts resolve and no material invalidating deviation is found. | Eligible for claim-specific decision under the frozen protocol; not automatically supportive. |
| `DEVIATION_REVIEW` | Deviation/integrity issue requires independent review before analysis status can be determined. | Publish/log the issue; no confirmatory claim until disposition. |
| `INVALID` | Material leakage, unauthorized access, arm/evaluator mismatch, unrecoverable provenance failure, or other frozen invalidation rule applies. | Preserve artifacts and report invalidity; do not reinterpret as a valid null or replace units silently. |

### 2.2 Claim decision state

| State | Assignment rule |
|---|---|
| `UNTESTED` | No eligible authorized test addresses that claim/estimand. This includes design-only status and claims affected by an invalid run without an independently valid analysis subset. It is not a null result. |
| `INCONCLUSIVE` | A relevant run is valid, but uncertainty, missingness, precision, coverage, baseline validity, or scope prevents a decision under frozen criteria. Do not lower thresholds or promote a secondary endpoint. |
| `WEAKENED` | A valid run meets a prospectively defined weakening/falsifier condition or its uncertainty excludes the preregistered meaningful support region. State the tested scope and exact weakening result; do not imply universal falsification. |
| `SUPPORTED_WITHIN_SCOPE` | A valid authorized run meets every claim-specific primary criterion, meaningful-effect/coverage condition, multiplicity rule, resource guardrail and protocol-integrity requirement frozen before outcomes. This is conditional support only for the tested scope. |

An `INVALID` run is reported under run validity and leaves the claim `UNTESTED` (unless a prospectively defined, independently valid subset exists). P5/P6's phrase `NOT_TESTED` maps to P7's canonical report state `UNTESTED`; use `UNTESTED` in the results shell to avoid duplicate labels. A statistically uncertain result is `INCONCLUSIVE`, not “no effect.” The exact alpha/confidence level, minimum effects, coverage margins, sample size/power, missingness rules, and thresholds remain `UNSET` in P5 and are not assigned here.

### 2.3 Claim decision matrix

| Claim | Primary outcome/contrast from P5 | Conditions for `SUPPORTED_WITHIN_SCOPE` | Weakening/falsifier patterns | Current AGI-3 status and mandatory boundary |
|---|---|---|---|---|
| **A — Candidate generalization** | `Ginv` vs `Grec` on the same permitted source experience; held-out relation/effect-prediction quality at reported coverage, with every proposal/rejection/abstention and source/game cluster accounted for. Candidate yield is secondary. | Frozen candidate nontriviality and prediction criteria met on eligible held-out contexts; coverage and all denominators reported; no source/target leakage; recurrence/replay comparison valid. Numerical criterion remains `UNSET`. | Candidates remain source-specific, fail held-out effect prediction, or do no better than the frozen recurrence/replay control; apparent success is only candidate count or support frequency. | Limited known-generator synthetic evidence only; **AGI-3 untested**. Synthetic result cannot promote A for AGI-3. |
| **N — Invariant value beyond replay** | Primary `I0` vs competent `R1`, boundary updates fixed; prediction coverage/selective risk at frozen common operating point or abstention-accounting loss. `R0` is diagnostic, relation ablation tests semantics. | All P3/P5 information/resource parity and R1 competence review pass; I0 meets frozen predictive criterion at comparable coverage; relation ablation and behavioral endpoint (if claimed) are reported separately. | R1 matches/beats I0 at comparable coverage/resources; relation ablation matches; gain disappears at parity or is explained by compression/retrieval; only abstention differs. | **Untested.** Raw replay alone is not an adequate comparator; prediction-only support is not behavioral benefit. |
| **B — Counterexamples improve scope** | `I1` vs `I0` on separately adjudicated held-out contexts; false activation/error, coverage, abstention, false rejection where adjudicable. | Frozen boundary-error criterion improves without coverage collapse; P4 triage maps to P2 enum; evidence role and version lineage pass. Numerical criterion remains `UNSET`. | No boundary improvement, or fewer false activations result only from suppressing nearly all use/abstaining. | **Untested.** Claim B cannot be inferred from N or from a lower invocation count. |
| **C — Better boundary reduces harm** | Primary `I1` vs `I0`; ITT probability of a predeclared harmful-transfer event per assigned task/episode, plus separate category rates. | Harm incidence improves under the frozen rule with complete assigned-unit denominator and local P4 evidence; coverage, score and categories disclose trade-offs. If the claim wording asserts superiority over raw replay/no-skill, the corresponding baseline contrast must also be prospectively specified and reported; I1-vs-I0 alone cannot establish that broader statement. | No harm reduction; harm falls only through low invocation/abstention; harm reduction offset by lost useful coverage or recovery burden. | **Untested.** Invocation-conditional rates are descriptive; do not claim safety from nonuse. |
| **D — Reduced harm improves efficiency** | Separate ITT contrasts in official task score/progress and actions-to-progress/completion per assigned unit; compare `I1`/`I0` and any predeclared common controls. | Predeclared efficiency endpoint improves and score/regression/cost guardrails pass; game/episode is the unit; no post-treatment conditioning. | Harm declines without an action-efficiency or official-score improvement; apparent gain vanishes under matched budgets or full denominators; regression exceeds frozen margin. | **Untested.** Harm reduction does not imply efficiency. Report score and action cost separately. |
| **E — Full method at acceptable cost** | Full `I1` versus `B0`, `R0`, `R1`, and frozen simple recurrence comparator; official AGI-3 evaluator outcome and separate cost vector. | All required meaningful baselines, official method-bearing artifact, frozen score/cost rules, complete run receipt and P5 primary contrasts pass. Multiple required baselines remain in the frozen family. | No improvement over required baseline family, costs erase the acceptable benefit under frozen criteria, tested method absent from linked entry, or target/cohort/failure reporting incomplete. | **Untested.** Reuse count or a paper direction is not end-to-end evidence; submission linkage remains unresolved. |

All thresholds, effect margins, operating points, confidence/multiplicity values and minimum meaningful effects are fields for a future P5 freeze; this matrix supplies none. A claim only advances when its corresponding outcome and exact run artifacts exist. Do not infer downstream claims from upstream success.

## 3. Reporting-table shell and denominator rules (P7.2)

The [blank results shell](results_shell_v1.md) carries the field layout. No cells are populated with invented values. At a future run, publish a flow/denominator table before claim summaries and retain every assigned/eligible unit, including no candidate, rejection, abstention, failure, timeout, fallback and missing evaluator value. Report unknown/unresolved separately from false. Report deviations and exclusions with reason/provenance; no outcome-dependent exclusions or imputation.

Minimum tables:

1. **Protocol/run integrity:** protocol/version, approvals, code/config/arm/evaluator hashes, environment, permitted manifests/roles, assignment, units, declared and realized budgets, run validity, deviations and exclusions.
2. **Candidate formation (A):** eligible source traces/contexts, alignments, all Ginv/Grec proposals, holds/rejections, support-role counts, candidate yields, held-out prediction coverage/error and all denominators.
3. **Claim N:** I0 vs R1 primary predictive endpoint/coverage/abstention, R0 diagnostic, relation ablation, ITT behavioral endpoint if preregistered, resource vector and uncertainty.
4. **Claim B:** I1 vs I0 boundary error/false activation, coverage, abstention/unknowns, false rejection where adjudicated, evidence class/denominators.
5. **Claims C/D:** per-assigned-unit harm incidence and category; official score/progress and action efficiency separately; invocation-conditional mechanism rates labelled descriptive; fallback/recovery and cost.
6. **Claim E:** official score per assigned unit and full-cohort aggregate; all required baseline contrasts; run-validity/missingness; construction/validation/invocation costs and cost vector. No composite utility.
7. **Failure and integrity ledger:** missing/corrupt artifacts, unknowns, mismatches, counterexamples, crashes/timeouts, rejected/invalid actions, abstentions, fallback, quarantines, resource breaches, access/protocol deviations and report corrections.
8. **Reproducibility and linkage:** version/hash inventory for the submitted method, notebook/entry, team linkage, evaluator/score receipt, source manifests/permissions, analysis artifacts and paper claim references.

Every rate names numerator, denominator, inclusion rule, unit, role, missingness, and provenance. For clustered data, display per-game/episode distributions; do not treat actions/candidate rows as independent samples. Use P5's predeclared uncertainty, multiplicity and ITT rules only after they are frozen. If a metric, arm or evaluator does not exist, mark it `NOT_RUN`/`NOT_AVAILABLE` with reason; never insert zero.

### 3.1 Failure and cost accounting

The flow table must account for: eligible source inputs; considered alignments; candidates proposed/held/rejected; skill versions specified/validated/active (if authorized); eligible invocations; applicable/reject/abstain outcomes; predictions issued/unknown; tasks/episodes assigned and attempted; completed/failed/timeouts; fallback events; and evaluator outputs. Keep denominators stage-specific.

Costs follow the P3/P5/P6 vector: source exposure and preprocessing; creation/review/validation; persistent storage and retrieval; model/tool calls/tokens; CPU/GPU/compute and wall time; environment actions/retries/resets; fallback/recovery; evaluator/analysis where measurable. Report unit, method, scope, cap and realized value separately. Missing cost is `UNKNOWN`, not zero. No weighted cost scalar is defined.

## 4. Reproducibility and paper/competition alignment (P7.3)

### 4.1 Minimum run artifact bundle (future, only if authorized)

For any future result report, the reproducibility archive must, as allowed by policy, contain or point to:

- frozen protocol and claim/metric decision version, approval/access references, deviation/exclusion ledger;
- source/data-role manifests and integrity hashes or controlled-access references (no restricted payloads in public artifacts);
- code commit/tag and clean working-tree state, dependency lock/environment/container description, build instructions, model/checkpoint and prompt/tool/config hashes, and arm artifact hashes;
- event logs and P2/P4 records with prediction-before-action and evidence lineage, all attempted units and failures, budget/cost ledgers;
- evaluator name/version, allowed evaluation command/interface, native submission/output artifact, official result/score receipt, and timestamps;
- analysis scripts/notebooks, immutable raw per-unit result tables, transformations, uncertainty/multiplicity configuration, and rendered report tables;
- software and data licenses, known provenance limitations, secret scan/redaction record, and instructions to reproduce permitted analyses without restricted data.

If an artifact is missing, inaccessible, or cannot be lawfully shared, say so and state the reproducibility limitation; do not imply exact reproduction. Do not include credentials, private leaderboard data, hidden/test labels, restricted outcome payloads, or another party's nonpublic artifact.

### 4.2 Submission and paper linkage checklist

A future competition/paper linkage is reportable only when each applicable item resolves:

| Artifact/link | Required record | Current state |
|---|---|---|
| **Method in code** | Versioned code commit and arm/build identity showing the method described in the paper is the method actually submitted. | `NOT_AVAILABLE` — P6 is a plan; no P6 implementation artifact. |
| **Notebook/submission** | Official platform notebook/entry identifier, immutable submitted output/artifact digest, submission timestamp and track. | `NOT_AVAILABLE` — no linked AGI-3 entry/score receipt in current evidence record. |
| **Team association** | Entry/receipt proving the submitted notebook is linked to the relevant team/account under current rules. | `UNRESOLVED` — must be verified from the live platform record; no assumption from reported membership. |
| **Evaluator and score receipt** | Official evaluator/version, permitted receipt/result artifact, score status and exact run/entry mapping. | `NOT_AVAILABLE` — no AGI-3 run/result is recorded. |
| **Live competition compliance** | Current offline/runtime/schema/license/data/model/team/track and paper-prize/late-entry eligibility review, with date and source. | `UNRESOLVED` — rules must be checked at submission time; P7 does not interpret or authorize an entry. |
| **Scientific evaluation** | Separate frozen protocol, authorized manifest/cohort, run logs, analysis and claim-specific tables. | `NOT_RUN` — P5 is a proposal only; no split, run, or result. |
| **Paper artifacts** | Claim-evidence map, method matching the linked entry, full positive/null/failure/cost results, limitations, reproducibility materials and author/reviewer sign-off. | `NOT_READY` — depends on valid implementation and authorized evidence; a concept paper may not state empirical AGI-3 results. |

Competition score alone does not prove a causal method claim. A working entry alone does not establish novelty, transfer, boundary value or acceptable cost. The paper must distinguish official competition evaluation from controlled research evaluation and must report the exact method present in the linked submission.

### 4.3 Language and evidence rules

- Do not use result language (“improves,” “reduces,” “outperforms,” “generalizes,” “safe,” “validated”) absent a matching, authorized run artifact and claim decision under §2.
- Report design, contract, synthetic, ARC-AGI-2, and Phase 13/14 findings with their exact provenance and ceiling; never transfer them into an AGI-3 result row or pool their scores.
- Describe N as provisional and comparative, not novelty-cleared. Do not claim “intelligence growth” or infer the full chain from a reuse count, candidate object or competition score.
- Preserve null/negative findings and failed baselines. State `INCONCLUSIVE` when warranted; do not silently narrow the cohort, switch endpoints or omit costs.
- Distinguish source, development, validation, confirmatory and restricted data. A version refined using an outcome cannot be validated by that outcome or its descendants.

## 5. Freeze fields and unresolved questions

P7 does not choose: alpha/confidence level; effect and regression margins; sample size/power; cohort/task IDs/splits; metric operating points/abstention cost; resource caps/cost units; missingness/sensitivity method; baseline competence-review owner; assignment/reset feasibility; official entry/team/late-entry eligibility; code/notebook/evaluator/version artifacts; named protocol, evaluation, security and paper reviewers; or public/private artifact-sharing permissions. These remain unset or not available as indicated and must be resolved under existing P5/project gates before a future preregistration, implementation, submission, or run.

## 6. Completion and authorization boundary

P7 closes the reporting/evaluation design package only. It does not authorize P6 implementation, software tests against live systems, Phase 2I, Phase 3B/3D, benchmarks, ARC runs, split assignment, hidden/test/confirmatory access, result-based tuning, submission, or restricted-outcome access. If the owner later requests code work, scope and authorization must be stated separately; engineering permission would still not override the remaining data/phase/competition gates.
