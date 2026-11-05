# T2T-P7 Claim-Linked Results Shell

**Shell ID:** `T2T-P7-ResultsShell-v1.0.0-draft`  
**Status:** blank design artifact; no run data or result values are present.  
**Use:** populate only from matching, authorized run artifacts under a frozen protocol. Do not treat blanks/placeholders as zero or as evidence.

## Placeholder vocabulary

- `NOT_RUN` — no matching authorized run/artifact.
- `UNSET` — design/protocol choice not frozen (e.g. threshold, alpha, budget).
- `NOT_AVAILABLE` — required code, receipt, score or record does not exist or cannot be lawfully shared.
- `NOT_APPLICABLE` — field does not apply, with reason.
- `UNKNOWN` — relevant fact/outcome is unavailable or uncertain; retain reason and provenance.
- `PENDING_REVIEW` — deviation/access/integrity issue not yet adjudicated.

**Do not replace these placeholders with `0`, an empty string, or an inferred result.** Use P7 run-validity and claim-decision states; preserve per-unit denominators and reasons.

## 1. Run identity and validity

| Field | Value | Artifact/reference |
|---|---|---|
| Report/version | `NOT_RUN` | `NOT_AVAILABLE` |
| P5 protocol ID/hash | `UNSET` | `NOT_AVAILABLE` |
| P6 build/schema/test-plan IDs | `T2T-P6-Blueprint-v1.0.0-draft` (design only) | No implementation commit; no test run |
| Written approvals and scope | `NOT_AVAILABLE` | `NOT_AVAILABLE` |
| Track/evaluator/version | `UNSET` | `NOT_AVAILABLE` |
| Data/manifest roles and access refs | `UNSET` | No manifest/split assignment |
| Cohort/assignment/unit | `UNSET` | No task IDs or cohort assigned |
| Arm/model/config hashes | `NOT_AVAILABLE` | No P6 arm artifacts |
| Environment/hardware/runtime | `UNSET` | `NOT_AVAILABLE` |
| Run validity | `NOT_RUN` | Apply P7 §2.1 only if a run exists |
| Run deviations/exclusions | `NOT_RUN` | Preserve even if empty in a future run |
| Report preparer/reviewer/date | `UNSET` | No owner/reviewer assigned |

## 2. Claim decisions

| Claim | Run validity | Claim state | Primary contrast/artifact | Frozen criterion ref | Estimate + interval | Coverage/denominator | Multiplicity family/adjustment | Cost/guardrail | Decision rationale |
|---|---|---|---|---|---|---|---|---|
| A — Candidate generalization | `NOT_RUN` | `UNTESTED` | Ginv vs Grec, `NOT_RUN` | `UNSET` | `NOT_RUN` | `NOT_RUN` | `UNSET` | `UNSET` | No authorized AGI-3 result; synthetic evidence is separate. |
| N — Beyond replay | `NOT_RUN` | `UNTESTED` | I0 vs R1, `NOT_RUN` | `UNSET` | `NOT_RUN` | `NOT_RUN` | `UNSET` | `UNSET` | No authorized AGI-3 result; R0 alone would not suffice. |
| B — Boundary quality | `NOT_RUN` | `UNTESTED` | I1 vs I0, `NOT_RUN` | `UNSET` | `NOT_RUN` | `NOT_RUN` | `UNSET` | `UNSET` | No boundary evaluation. |
| C — Harm reduction | `NOT_RUN` | `UNTESTED` | I1 vs I0, `NOT_RUN` | `UNSET` | `NOT_RUN` | `NOT_RUN` | `UNSET` | `UNSET` | No assigned-unit harm outcome. |
| D — Action efficiency | `NOT_RUN` | `UNTESTED` | I1/I0 vs frozen common control(s), `NOT_RUN` | `UNSET` | `NOT_RUN` | `NOT_RUN` | `UNSET` | `UNSET` | No official outcome/action comparison. |
| E — Full method/cost | `NOT_RUN` | `UNTESTED` | I1 vs B0/R0/R1/Grec, `NOT_RUN` | `UNSET` | `NOT_RUN` | `NOT_RUN` | `UNSET` | `UNSET` | No linked method-bearing AGI-3 entry, official score or cost ledger. |

### 2.1 Analysis, uncertainty and multiplicity settings

| Setting | Frozen value/reference | Status |
|---|---|---|
| Confirmatory claim/contrast family | `UNSET` | `UNSET` |
| Alpha and confidence level | `UNSET` | `UNSET` |
| Uncertainty method and game/episode resampling unit | `UNSET` | `UNSET` |
| Pairing/cluster/blocking basis | `UNSET` | `UNSET` |
| Resample count/seed or alternative inference rule | `UNSET` | `UNSET` |
| Minimum meaningful effects and regression/harm margins | `UNSET` | `UNSET` |
| Power/sample-size justification | `UNSET` | `UNSET` |
| Multiplicity procedure and adjusted result | `UNSET` | `UNSET` |
| Missingness/sensitivity method | `UNSET` | `UNSET` |
| Interim analysis/early-stop policy | `UNSET` | `UNSET` |

## 3. Integrity and data-flow table

| Stage | Role/manifest ref | Eligible | Assigned | Attempted | Complete | Failed/timeout | Abstain/unknown | Missing artifact/outcome | Exclusions/deviations and reasons |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| Source/formation | `UNSET` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |
| Candidate evaluation | `UNSET` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |
| Validation | `UNSET` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |
| Confirmatory/target | `UNSET` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |
| Restricted evaluator | `UNSET` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |

Do not populate restricted rows without the controlling authorization. Show outcome-store separation and access approval. Units used for construction/refinement must not reappear as held-out validation for that version or descendants.

## 4. Claim A — candidate formation and held-out prediction

| Arm/generator | Source opportunities | Proposals | Holds | Rejects | Unique source contexts | Held-out prediction issued | Coverage | Error/loss + interval | Denominator/provenance |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|
| Ginv | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |
| Grec | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |

Candidate support counts are descriptive; candidate yield alone is not validation. Report every proposal/rejection/no-prediction and the frozen held-out evaluation interface.

## 5. Claim N — invariant vs replay

| Arm | Prediction coverage | Selective risk/error | Operating point or abstention-aware loss | Relation/ablation result | ITT official outcome (secondary) | Resource vector |
|---|---|---|---|---|---|---|
| R0 diagnostic | `NOT_RUN` | `NOT_RUN` | `UNSET` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |
| R1 primary comparator | `NOT_RUN` | `NOT_RUN` | `UNSET` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |
| I0 primary treatment | `NOT_RUN` | `NOT_RUN` | `UNSET` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |
| I−rel ablation | `NOT_RUN` | `NOT_RUN` | `UNSET` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |
| Contrast/uncertainty | `NOT_RUN` | `NOT_RUN` | `UNSET` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |

R1 competence review, identical source/target/context, coverage relationship, score/loss and multiplicity references: `UNSET`.

## 6. Claim B — boundary quality

| Arm | Eligible adjudicated contexts | Admitted/applicable | False activation | False rejection | Unknown/abstain | Coverage | Denominator/adjudication ref |
|---|---:|---:|---:|---:|---:|---:|---|
| I0 | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |
| I1 | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |
| Contrast/uncertainty | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |

P4 triage subtype, P2 coarse class, version lineage and evidence-use roles: `NOT_RUN`. False activation, false rejection, unknown and non-applicability are not interchangeable.

## 7. Claims C/D — harm, action efficiency and official outcomes

| Arm/contrast | Assigned units | Units with any predeclared harm | Harm categories by assigned unit | Harm per invocation (descriptive) | Official score/progress | Actions/invalid/retry/fallback | Missingness/interval |
|---|---:|---:|---|---:|---|---|---|
| I0 | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |
| I1 | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |
| Frozen common control(s) | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |
| ITT contrast/uncertainty | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `DESCRIPTIVE_ONLY` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |

Report score/progress and action efficiency separately. Main causal comparison is by assigned game/episode; do not condition on invocation or success.

## 8. Claim E — full method, baselines and costs

| Arm | Official per-unit outcome | Assigned/attempted denominator | Score contrast + interval | Resource-vector costs | Required artifact/receipt |
|---|---|---|---|---|---|
| B0 no learned skills | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_AVAILABLE` |
| R0 raw replay | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_AVAILABLE` |
| R1 strong replay | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_AVAILABLE` |
| Grec/simple recurrence | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_AVAILABLE` |
| I1 full method | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_AVAILABLE` |
| Required contrast family/multiplicity | `UNSET` | `NOT_RUN` | `UNSET` | `UNSET` | `NOT_AVAILABLE` |

No cost scalar or reuse count replaces official score, denominator, uncertainty or baseline comparison.

## 9. Failures, costs, exclusions and deviations

| Record type | Count/rate | Unit and denominator | Reason/category | P2/P4 refs | Cost impact | Disposition |
|---|---|---|---|---|---|---|
| Unknown/unresolved | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |
| Mismatch/counterexample | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |
| Invalid/rejected action | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |
| Timeout/crash | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |
| Abstention/fallback/recovery | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |
| Resource cap breach | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |
| Missing/corrupt artifacts | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |
| Access/protocol deviation | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |
| Exclusion/missing outcome | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` | `NOT_RUN` |

### Cost vector (no composite)

| Resource dimension | Arm | Declared cap/unit | Realized use/unit | Measurement method | Stage/scope | Missingness/provenance |
|---|---|---|---|---|---|---|
| Source exposure/preprocessing | `NOT_RUN` | `UNSET` | `NOT_RUN` | `UNSET` | `NOT_RUN` | `NOT_RUN` |
| Creation/review/validation | `NOT_RUN` | `UNSET` | `NOT_RUN` | `UNSET` | `NOT_RUN` | `NOT_RUN` |
| Storage/retrieval | `NOT_RUN` | `UNSET` | `NOT_RUN` | `UNSET` | `NOT_RUN` | `NOT_RUN` |
| Model/tools/tokens/compute/time | `NOT_RUN` | `UNSET` | `NOT_RUN` | `UNSET` | `NOT_RUN` | `NOT_RUN` |
| Environment actions/retries | `NOT_RUN` | `UNSET` | `NOT_RUN` | `UNSET` | `NOT_RUN` | `NOT_RUN` |
| Fallback/recovery/evaluation | `NOT_RUN` | `UNSET` | `NOT_RUN` | `UNSET` | `NOT_RUN` | `NOT_RUN` |

## 10. Reproducibility and paper linkage

| Required artifact | Version/hash or receipt | Access/sharing status | Claim/table linkage | Completeness |
|---|---|---|---|---|
| Code commit / arm build | `NOT_AVAILABLE` | `NOT_AVAILABLE` | `NOT_RUN` | `NOT_RUN` |
| Environment/dependency lock | `NOT_AVAILABLE` | `NOT_AVAILABLE` | `NOT_RUN` | `NOT_RUN` |
| Data/role manifest | `UNSET` | `UNSET` | `NOT_RUN` | `NOT_RUN` |
| Event log/P2/P4 records | `NOT_AVAILABLE` | `UNSET` | `NOT_RUN` | `NOT_RUN` |
| Evaluator version/output | `NOT_AVAILABLE` | `UNSET` | `NOT_RUN` | `NOT_RUN` |
| Notebook/submission/team link | `NOT_AVAILABLE` | `UNRESOLVED` | `NOT_RUN` | `NOT_RUN` |
| Official score receipt | `NOT_AVAILABLE` | `NOT_AVAILABLE` | `NOT_RUN` | `NOT_RUN` |
| Analysis script/per-unit table | `NOT_AVAILABLE` | `UNSET` | `NOT_RUN` | `NOT_RUN` |
| Paper claim/limitation/reviewer sign-off | `NOT_RUN` | `UNSET` | `NOT_RUN` | `NOT_RUN` |

## 11. Review sign-off and report release

| Check | State | Reviewer/reference |
|---|---|---|
| Matching authorized run artifact exists | `NOT_RUN` | `NOT_AVAILABLE` |
| P5 criteria and claim family were frozen before outcomes | `UNSET` | `NOT_AVAILABLE` |
| Run validity and data-role separation reviewed | `NOT_RUN` | `NOT_AVAILABLE` |
| All assigned/attempted units and failures reconciled | `NOT_RUN` | `NOT_AVAILABLE` |
| Claim state assigned using P7 rules | `UNTESTED` | `NOT_AVAILABLE` |
| Costs and deviations included | `NOT_RUN` | `NOT_AVAILABLE` |
| Competition/track rules and linked entry verified live | `UNRESOLVED` | `NOT_AVAILABLE` |
| Independent review/report release approval | `UNSET` | `NOT_AVAILABLE` |
