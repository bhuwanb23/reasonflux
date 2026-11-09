# BL1 Protocol Draft v1 — Counterexample-Guided Applicability Boundaries

**Status:** non-preregistered design draft; no contexts generated and no execution authorized.  
**Purpose:** identify protocol decisions needed to test BL1-P. This document is not an implementation or run plan.

## 1. Primary question

Does counterexample evidence improve held-out applicability precision while preserving useful coverage?

The test must isolate boundary feedback. It must not retest Claim N, compare I0 with R4, or claim that invariants outperform replay.

## 2. Candidate treatment contrast

A prospective design may compare:

- **BL1-CE:** a fixed candidate skill/initial boundary receives permitted labeled counterexamples and updates its applicability boundary using a frozen update rule.
- **BL1-Control:** the identical candidate/initial boundary uses the same source evidence and frozen inference interface, but counterexample labels cannot update its boundary.

The protocol must define whether the control receives matched unlabeled context exposure or another suitable exposure control. The arms must otherwise match candidate skill, initial boundary, observation/action schema, source examples, held-out contexts, model/tool access, and declared resource opportunities. No arm may use held-out outcomes for updates.

This is a design sketch only. The specific algorithm, exposure control, candidate skill, and domain remain unset.

## 3. Data roles and leakage prevention

A future protocol must prospectively define disjoint roles for:

1. positive/source experience used to define the candidate skill and initial boundary;
2. counterexample evidence available to BL1-CE (and the specified exposure control for BL1-Control);
3. held-out applicability contexts used only for evaluation.

Freeze context identities, role map, labels, transformation/domain coverage, and hashes before evaluation. Keep held-out applicability labels inaccessible to both update procedures until predictions are committed. Do not reuse S3 contexts, labels, or outcomes as BL1 held-out data.

The unit of evaluation, domain, context-generation rules, counts, exclusions, resource caps, and custody procedure are all **UNSET**.

## 4. Outcomes and reporting candidates

For every held-out context and arm, record the pre-outcome applicability prediction (permit, reject, or abstain), then attach the applicability target only after predictions are committed. Report:

- TP, FP, FN, TN, abstain, invalid, and missing counts;
- applicability precision `TP/(TP+FP)` and its undefined case;
- useful coverage candidate `TP/(TP+FN)`;
- all-context denominators and per-cell/domain-stratum counts;
- boundary update lineage and resource use.

The owner must decide what coverage is “useful,” how precision and coverage jointly determine success, whether uncertainty is needed, and what constitutes a meaningful effect. No threshold, count, sample size, power target, or statistical method is selected in this draft.

## 5. Prospective decision and stop requirements

Before any held-out labels are exposed, freeze:

- the domain/world and candidate skill;
- the initial applicability boundary and counterexample definition;
- the update rule and treatment/control exposure;
- the primary precision/coverage endpoint and decision rule;
- context counts, inclusion/eligibility rules, and denominators;
- equal resource opportunities and actual resource accounting;
- prediction-before-label event order, hashes, and stop conditions;
- independent review and explicit owner authorization.

Stop and classify the BL1 attempt as invalid/inconclusive if held-out labels inform updates, the held-out suite or comparator changes after exposure, the treatment receives extra information/resources outside the frozen contrast, coverage is suppressed without meeting the predeclared criterion, or integrity checks fail. Do not reinterpret an invalid run as support.

## 6. Non-goals and authorization boundary

This draft does not include Claim C harm reduction, Claim D action efficiency, Claim E end-to-end superiority, Claim N, ARC evaluation, a paper claim, or implementation details beyond the candidate contrast. It authorizes **no** context generation, model fitting, code changes, experiment, or external data access. Any of those requires a separate owner decision after this draft is reviewed and completed.
