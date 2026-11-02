Excellent. Phase 2F is where we finally test the biggest surviving ARC hypothesis:

Current Representation
↓

Low Coverage
↓

No Mechanism Chain


Up to Phase 2E we have audited:

Representation

Coverage

Search

Trace Generation

Invariant Discovery


But we still do not know whether:

The representation itself


is the bottleneck.

Phase 2F exists to make that hypothesis scientifically testable.

ASFT v1.1 Phase 2F
Representation Alternatives Framework

Phase ID

ASFT-V1.1-PHASE-2F


Package

ASFT-V1.1-PHASE-2F-REPRESENTATION-ALTERNATIVES-V1

Phase Objective

Create a framework for comparing:

Current ARC Representation

vs

Alternative Representations

vs

Reference Conditions


without changing:

Search

Budgets

Evaluation

Downstream Mechanisms


The goal is not:

Find the best representation.


The goal is:

Determine whether representation
is actually limiting the ASFT pipeline.

Core Research Questions
R2F-1
Does representation choice
materially affect coverage?

R2F-2
Does representation choice
materially affect trace generation?

R2F-3
Does representation choice
materially affect invariant discovery?

R2F-4
Can downstream failures persist
despite improved coverage?

R2F-5
Is representation the primary bottleneck,
a contributing bottleneck,
or not supported as the main bottleneck?

Phase Structure
2F.1 Representation Hypothesis Audit

2F.2 Representation Registry

2F.3 Representation Taxonomy

2F.4 Coverage Comparison Framework

2F.5 Trace Comparison Framework

2F.6 Invariant Comparison Framework

2F.7 Downstream Activation Framework

2F.8 Bottleneck Attribution Framework

2F.9 Reporting Framework

2F.10 Readiness Review

2F.1 Representation Hypothesis Audit
Purpose

Audit all evidence supporting the representation hypothesis.

Sources
13G

14G

2A

2B

2C

2D

2E

Questions
What evidence supports representation limits?

What evidence weakens representation limits?

What remains unresolved?

Deliverable
representation_hypothesis_audit.md

2F.2 Representation Registry
Purpose

Freeze representation candidates.

R0
Historical ARC Representation


The exact Phase 13G representation.

R1
Current Production Representation

R2+
Alternative Representations


Each must be fully specified.

Required Fields
Primitive inventory

Object model

Relation model

Composition model

Search interface

Deliverable
representation_registry.csv

2F.3 Representation Taxonomy
Purpose

Classify representation differences.

T1
Primitive Expansion


More operations.

T2
Object-Centric

T3
Relation-Centric

T4
Hierarchical

T5
Compositional

T6
Hybrid

Goal

Avoid vague:

Representation improved.


claims.

Deliverable
representation_taxonomy.md

2F.4 Coverage Comparison Framework
Purpose

Compare coverage fairly.

Metrics:

Representable Tasks

Coverage %

Successful Traces

Coverage Yield

Rule

Same:

Tasks

Budgets

Splits


for all representations.

Deliverable
coverage_comparison_framework.md

2F.5 Trace Comparison Framework
Purpose

Measure trace effects.

Metrics:

Valid Traces

Successful Traces

Trace Diversity

Trace Yield

Questions
Does representation improve trace supply?

Deliverable
trace_comparison_framework.md

2F.6 Invariant Comparison Framework
Purpose

Measure invariant effects.

Metrics:

Candidate Invariants

Validated Invariants

Support Distribution

Invariant Yield

Questions
Does representation improve invariant discovery?

Deliverable
invariant_comparison_framework.md

2F.7 Downstream Activation Framework

This is the most important section.

Purpose

Determine whether improved representation activates the chain.

Stages:

Coverage

↓

Trace Generation

↓

Invariant Discovery

↓

Skill Eligibility

↓

Transfer Eligibility

↓

Capability Eligibility

Questions
Does improvement stop at coverage?

Or propagate downstream?

Deliverable
activation_comparison_framework.md

2F.8 Bottleneck Attribution Framework
Purpose

Classify outcomes.

B1
Representation Dominant


Coverage rises dramatically and downstream activation follows.

B2
Representation Contributing


Coverage rises but activation remains weak.

B3
Representation Weak


Coverage changes little.

B4
Mixed Bottlenecks


Multiple constraints.

B5
Unresolved

Rule

Representation never automatically declared root cause.

Deliverable
bottleneck_attribution_framework.md

2F.9 Reporting Framework

Every comparison must report:

Coverage

Trace Yield

Invariant Yield

Skill Eligibility

Transfer Eligibility

Capability Eligibility

Accuracy


Separately.

Rule

Coverage gains are not:

Transfer gains


and not:

Capability gains.

Deliverable
representation_reporting_standard.md

2F.10 Readiness Review
Questions
Q1
Representation registry frozen?

Q2
Alternative representations specified?

Q3
Coverage comparison possible?

Q4
Trace comparison possible?

Q5
Invariant comparison possible?

Q6
Activation comparison possible?

Q7
Representation hypothesis remains falsifiable?

Phase 2F Readiness Gates
Gate RA1
Representation registry complete.

Gate RA2
Alternative representations specified.

Gate RA3
Coverage comparison framework defined.

Gate RA4
Trace comparison framework defined.

Gate RA5
Invariant comparison framework defined.

Gate RA6
Activation framework defined.

Gate RA7
Bottleneck attribution framework frozen.

Deliverables
representation_hypothesis_audit.md

representation_registry.csv

representation_taxonomy.md

coverage_comparison_framework.md

trace_comparison_framework.md

invariant_comparison_framework.md

activation_comparison_framework.md

bottleneck_attribution_framework.md

representation_reporting_standard.md

phase2F_readiness_review.md

Phase 2F Exit Decision
PASS

Only if:

Representation alternatives specified

Comparisons fair

Coverage measurable

Trace effects measurable

Invariant effects measurable

Activation measurable

Bottleneck attribution possible

FAIL

If:

Representation remains vague

Alternatives undefined

Coverage improvements unmeasurable

Representation hypothesis unfalsifiable

Most Important Outcome

The single most important question Phase 2F should answer is:

"If ARC coverage improves substantially under an alternative representation, does the ASFT mechanism chain begin to activate, or do failures persist further downstream?"

That question sits at the center of the entire ARC debate.

If improved representations activate:

Coverage
→ Traces
→ Invariants
→ Skills


then the representation hypothesis gains support.

If coverage improves but:

Invariants remain zero

or

Skills remain zero


then the bottleneck likely lies elsewhere.

Phase 2F should make that distinction experimentally testable rather than speculative.