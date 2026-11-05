# T2T-P7 Reproducibility and Submission Artifact Checklist

**Checklist ID:** `T2T-P7-SubmissionChecklist-v1.0.0-draft`  
**Status:** design/documentation only; all current execution/submission artifacts are `NOT_AVAILABLE`, `UNSET`, or `UNRESOLVED` as shown. This checklist authorizes no code, run, split, evaluator access, or submission.

## 1. Scope and release gate

Use this checklist only if a future implementation, authorized evaluation and/or competition entry exists. Mark each item with `PRESENT`, `MISSING`, `NOT_APPLICABLE` plus reason, `RESTRICTED_REFERENCE` plus access owner, or `UNRESOLVED`. A missing required item blocks the corresponding reproducibility/claim/submission statement; it must not be silently inferred.

- **Current project state:** No linked ARC-AGI-3 run/score receipt is recorded; P6 is a design blueprint, not code; P7 has no result data. The current claim map says A has limited known-generator synthetic evidence only and N/B/C/D/E are untested for the proposed AGI-3 method.
- **Rule check:** competition, track, notebook, runtime, offline, team, data/model/license, entry, and Paper Prize rules must be checked against the live official rules at the time of any intended submission. This plan does not determine current eligibility or resolve late-entry questions.
- **Authorization:** any code, access, split assignment, benchmark/run, evaluator connection or restricted outcome requires separate written authorization under the existing controlling project gates. Phase 2I, Phase 3B/3D and no-run restrictions remain in force unless separately changed by their controlling authority.

## 2. Protocol, implementation and environment bundle

| Item | Required evidence | Current state |
|---|---|---|
| Scientific protocol | Frozen P5 protocol version/hash, claim set, estimands, criteria, analysis/multiplicity, exclusions, stop rules, owners/reviewers and approval refs. | `UNSET`; P5 is a proposal, not preregistration. |
| Code identity | Git commit/tag, source archive/hash, branch/working-tree state, arm/build mapping and change history. | `NOT_AVAILABLE`; P6 contains no code. |
| Build/runtime environment | Language/runtime, dependency lockfile, OS/container image, hardware/runtime description, build command and provenance. | `UNSET`. |
| Arm identities | Immutable B0/R0/R1/Grec/I0/I1/I−rel configurations and artifact/checkpoint/prompt/tool/retrieval hashes, with role and control mapping. | `NOT_AVAILABLE`. |
| P2/P4/P6 data contracts | P2/P4 record schema versions, P6 event schema/test-plan versions, migrations, validation status, and compatibility notes. | Design specs exist; no implementation/schema-validator status. |
| Model/data provenance | Model/checkpoint and permitted pretraining/source-data provenance, licenses, known overlap and uncertainty. | `UNSET`; must be resolved and disclosed. |
| Security and access review | Approved credentials handling, secret scan/redaction, access control, threat review, role-separated stores and audit owner. | `UNSET`; no secrets or restricted data should be attached to a public artifact. |
| Resource contract | Frozen P5 cap refs/units and ledger definitions for source, creation, review, storage, retrieval, tokens/calls, compute/time, actions, fallback and evaluation. | `UNSET`; P5 supplies no numerical caps. |

## 3. Dataset and source/target provenance (if authorized)

- Immutable manifest version and digest; data owner/access/licensing and permitted use.
- Prospective role for each event/artifact: source/formation, development/refinement, validation, confirmatory/target, or restricted evaluation.
- Source/target disjointness and task-family/generating-rule rationale where known; episode/reset boundaries and persistence rules.
- Allowed fields, normalization/representation versions, deduplication, label provenance, manual annotation and adjudication record.
- Authorized assignment/split mechanism, seed/order, complete eligible/assigned/attempted denominators and reason-coded exclusions; no IDs or splits are created by this checklist.
- Artifact ref/digest and verification/access procedure; restricted payloads are not copied into a public artifact.
- P2/P4 lineage proving an outcome used to refine a version is not counted as validation for that version or its descendants.
- Explicit leakage checks covering future outcomes, private leaderboard feedback, hidden/test labels, cross-arm memory, prompts, logs and shared artifacts.

If a source, task, outcome or permission is unknown, label it `UNKNOWN` with provenance; do not infer permission from file presence or a prior result.

## 4. Run receipt and official evaluation evidence

For each future authorized run, retain:

| Item | Requirement |
|---|---|
| Run/protocol identity | Unique run and activity IDs linked to exact frozen protocol and code/arm hashes. |
| Cohort/assignment | Authorized manifest/split ref, assignment unit/order, seed refs where applicable, and full attempted-unit list in protected storage. |
| Environment | Environment/evaluator/runtime version, permitted configuration, hardware/service details, and reset/retry behavior. |
| Event/audit log | P6 event streams with ordering/integrity, P2 predictions before action, separate observed transitions, P4 triage, lifecycle, costs, failures and corrections. |
| Native output | Exact submission/notebook output artifact and digest, linked to run and arm; never replace with a reconstructed file. |
| Evaluator receipt | Official evaluator/version, invocation/receipt/time, raw result reference and per-unit results as permitted. Restricted results remain segregated. |
| Completeness | Every eligible/assigned/attempted/failure/timeout/abstention/fallback unit reconciled; missing artifacts reason-coded. |
| Deviations | Complete deviation/exclusion/integrity register, review disposition and protocol version changes; no silent replacement. |
| Analysis | Versioned analysis scripts/notebooks, immutable per-unit result tables, uncertainty/multiplicity configuration, outputs and environment. |
| Cost | Declared versus realized resource-vector ledger with units, methods, scope, arm, missingness and provenance. |

A score screenshot alone is insufficient for reproducibility or causal claim support. A valid official score does not establish a controlled comparison, novelty, transfer, or cost-effectiveness by itself.

## 5. Competition entry, notebook and team linkage

Before making a competition-linked paper statement, verify and archive—subject to rules—the following from the official live platform:

- exact track/competition, entry/notebook ID and immutable submitted version/output hash;
- team ID/name and account linkage tying the entry to the authors/team, with date and proof reference;
- submission, evaluation and score receipt identifiers/status, linked to the same immutable notebook/output;
- compliance with current execution/offline/runtime/schema, resource, license, model and data rules;
- eligibility for the intended award/category and whether any late-entry or code-prize restriction affects Paper Prize linkage/accuracy;
- method/code consistency: the notebook contains the method described in the paper, not an unlinked or materially different version; and
- archived live-rule page/version/date and independent compliance reviewer.

Current state for entry ID, team linkage, evaluator receipt, score and eligibility: `NOT_AVAILABLE`/`UNRESOLVED`. Do not imply a successful submission or prize eligibility based only on user-reported team membership or historical rules.

## 6. Paper/release artifacts and claim alignment

A future paper/release should include or reference:

- claim-evidence map with P7 state for A/N/B/C/D/E and exact scope;
- method/arm definitions and the method-to-code-to-notebook crosswalk;
- per-claim results tables, denominators, confidence/uncertainty and multiplicity decisions, costs, failures, deviations and null/negative results;
- distinction between official competition results and controlled research evaluation;
- data/model/code availability statements and lawful access instructions; no restricted outcomes or secrets in public materials;
- synthetic/ARC-AGI-2/Phase 13/14 evidence labeled by provenance and ceiling, never reported as ARC-AGI-3 support;
- limitations covering cohort, source/target separation, baseline competence, novelty status, missingness, power, generalization and protocol deviations;
- exact reference/citation list, report-generation version and artifact manifest; and
- author, protocol, data/security and independent analysis review sign-offs.

Do not write empirical result language before matching run artifacts exist. A concept/paper direction may be discussed as a proposal, with no claim that the AGI-3 method was validated or that a competition score exists.

## 7. Artifact publication and privacy review

For each artifact mark public, private, restricted-reference-only, or not-shareable under the controlling license/rules. Before release, review for credentials, private leaderboard details, hidden/test labels, participant identifiers, nonpublic task payloads, third-party confidential artifacts, and access tokens embedded in logs/notebooks. Do not make a restricted artifact public to improve reproducibility; provide an approved metadata/hash/access description instead. Retention, redaction and archival policy require separate security/legal review.

## 8. Final sign-off fields

| Sign-off | Owner/reviewer | Version/date | Status |
|---|---|---|---|
| Scientific protocol freeze and authorization | `UNSET` | `UNSET` | `NOT_READY` |
| Data/access/manifest review | `UNSET` | `UNSET` | `NOT_READY` |
| Engineering/build reproducibility | `UNSET` | `UNSET` | `NOT_READY` |
| Evaluator/competition-rule compliance | `UNSET` | `UNSET` | `NOT_READY` |
| Statistical analysis and claim decisions | `UNSET` | `UNSET` | `NOT_READY` |
| Security/privacy/license review | `UNSET` | `UNSET` | `NOT_READY` |
| Paper-to-entry linkage | `UNSET` | `UNSET` | `NOT_READY` |

Checklist completion does not grant authorization. All required gates are separate, and an unresolved gate remains unresolved.
