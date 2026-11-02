Excellent. Phase 1H is where we freeze the competition.

If Phase 1B–1G define the tests, then Phase 1H defines:

Who ASFT must beat

What components are being tested

What counts as a fair comparison


One of the biggest lessons from v1.0 was:

Baseline ambiguity

Comparator drift

Different implementations

Different opportunities

Different endpoints


often made interpretation difficult.

Phase 1H exists to prevent that.

ASFT v1.1
Phase 1H – Baseline & Ablation Framework

Phase ID

ASFT-V1.1-PHASE-1H


Package

ASFT-V1.1-PHASE-1H-BASELINE-ABLATION-SPEC-V1

Primary Goal

Create a frozen framework defining:

Baselines

Ablations

Fairness rules

Comparison rules

Interpretation rules


for all v1.1 experiments.

Why This Phase Exists
v1.0 Lessons

Phase 14F showed:

Memory survived

Compression survived

Frequency survived

Selection superiority failed

Ranking superiority failed


But some comparisons were difficult because:

Policies had different opportunities

Different candidate pools

Different activation paths

Different endpoint definitions

Core Principle

Every positive ASFT claim must answer:

Compared to what?

And:

Under identical conditions?

Phase Structure
1H.1 Baseline Audit

1H.2 Baseline Taxonomy

1H.3 Mandatory Baselines

1H.4 Ablation Taxonomy

1H.5 Mandatory Ablations

1H.6 Fairness Framework

1H.7 Comparator Activation Audit

1H.8 Interpretation Rules

1H.9 Preregistration Framework

1H.10 Readiness Review

1H.1 Baseline Audit
Purpose

Audit all v1.0 baselines.

Inputs
Phase 13B–13G

Phase 14F

Questions
Which baselines were informative?

Which survived?

Which were weak?

Which were unfair?

Which were unmatched?

Output
baseline_audit.md

Example Findings
Strong Baseline
MEMORY_ONLY


because it exposed a major alternative.

Weak Baseline
No Learning


because it is too easy to beat.

1H.2 Baseline Taxonomy
Purpose

Classify competitor explanations.

Every baseline belongs to a category.

B1
No Learning

B2
Memory / Retrieval

B3
Random

B4
Compression

B5
Frequency

B6
Heuristic

B7
Oracle


analysis only.

Goal

Map every surviving alternative explanation.

1H.3 Mandatory Baselines

These must exist across v1.1.

Baseline Set
BL1
No Learning

BL2
Memory

BL3
Random

BL4
Frequency

BL5
Compression

BL6
Hybrid Memory+Frequency

BL7
Oracle

Rule

No mechanism claim may be reported without comparison to the relevant baseline family.

1H.4 Ablation Taxonomy
Purpose

Define component removals.

A1
No IDT

A2
No SCT

A3
No SCV

A4
No Transfer

A5
No Capability Layer

A6
No Lifecycle

A7
No Composition

A8
No Memory

A9
No ARC Extension

1H.5 Mandatory Ablations
Purpose

Ensure every major claim is testable.

IDT Claim

Requires:

No IDT

SCT Claim

Requires:

No SCT

No SCV

Transfer Claim

Requires:

No Transfer

Capability Claim

Requires:

No Capability Layer

Memory Claim

Requires:

No Memory

Rule

No component may claim value without a corresponding removal test.

1H.6 Fairness Framework

This is the most important section.

Purpose

Ensure fair comparisons.

Required Equality

All competitors must receive:

Same tasks

Same candidates

Same budget

Same storage

Same compute constraints

Same evaluation horizon

Forbidden
Different opportunity counts

Different candidate pools

Different task exposure

Deliverable
fairness_framework.md

1H.7 Comparator Activation Audit
Purpose

Prevent v1.0-style dead comparisons.

Example:

44/44 selected


means:

Selector not really tested.


Every experiment must report:

Comparator divergence

Decision divergence

Activation rate

Rule

If all systems make identical decisions:

Comparison
=
non-informative


Not:

Mechanism wins.

1H.8 Interpretation Rules

These rules are frozen.

Rule 1

Tie means:

No demonstrated advantage.


Not:

Mechanism validated.

Rule 2

Unavailable means:

Unavailable.


Not:

Zero.

Rule 3

Score improvement means:

Metric improved.


Not:

Theory validated.

Rule 4

Ablation effect means:

Component contributed
under tested conditions.


Not:

Component universally necessary.

1H.9 Preregistration Framework

Freeze:

Baselines

Ablations

Budgets

Comparator rules

Decision rules

Interpretation rules

Outcomes
Supported

Contradicted

Inconclusive

Unavailable

1H.10 Readiness Review
Checklist
Baseline Audit

✅

Baseline Taxonomy

✅

Mandatory Baselines

✅

Ablation Taxonomy

✅

Mandatory Ablations

✅

Fairness Framework

✅

Comparator Audit

✅

Interpretation Rules

✅

Preregistration

✅

Deliverables
baseline_audit.md

baseline_taxonomy.md

mandatory_baselines.md

ablation_taxonomy.md

mandatory_ablations.md

fairness_framework.md

comparator_activation_audit.md

interpretation_rules.md

baseline_preregistration_template.md

phase1H_readiness_report.md

Phase 1H Exit Decision

PASS only if:

All major alternatives represented

All major components ablatable

Fairness rules frozen

Comparator divergence measurable

Interpretation rules frozen

Budgets standardized

Replication planned

Most Important Outcome

At the end of Phase 1H, ASFT v1.1 should be protected against the biggest criticism from Phase 14F:

"We don't know whether the observed effect came from the proposed mechanism, memory, frequency, compression, selection degeneracy, or benchmark design."

Phase 1H creates the framework needed to make future positive results scientifically attributable rather than merely observable.