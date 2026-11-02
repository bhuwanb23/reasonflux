Excellent. Under the brutal-honesty framework, Phase 2A is the foundation of the entire ARC program.

If Phase 1 asked:

Can ARC failure be diagnosed?


then Phase 2A asks:

What can the current ARC representation
actually express?


Before discussing skills, transfer, capabilities, or intelligence, we must know whether the representation is even capable of generating the structures those mechanisms need.

ASFT v1.1 Phase 2A
Representation Audit

Phase ID

ASFT-V1.1-PHASE-2A


Package

ASFT-V1.1-PHASE-2A-REPRESENTATION-AUDIT-V1

Objective

Create a complete audit of the ARC representation layer.

The goal is not:

Improve ARC performance


The goal is:

Understand exactly what the
representation can and cannot express.

Core Research Questions
R2A-1
What structures can the representation express?

R2A-2
What ARC phenomena cannot currently be expressed?

R2A-3
Which Phase 13G failures are plausibly
representation-related?

R2A-4
Which failures remain unexplained
by representation limits?

Phase Structure
2A.1 Historical Representation Audit

2A.2 Primitive Inventory

2A.3 Expressivity Analysis

2A.4 ARC Task Coverage Audit

2A.5 Missing Concept Audit

2A.6 Search Interaction Audit

2A.7 Representation Bottleneck Assessment

2A.8 Alternative Representation Requirements

2A.9 Readiness Review

2A.1 Historical Representation Audit
Purpose

Document exactly what existed in 13G.

Required Findings

Examples:

Primitive count

Search limits

Trace generation rates

Coverage rates

Successful fits

Questions
What representation was used?

What assumptions existed?

What coverage was achieved?

What evidence supports representation concerns?

Deliverable
historical_representation_audit.md

2A.2 Primitive Inventory

This is the most important section.

Goal

Inventory every representational primitive.

Geometry

Examples:

Translate

Rotate

Reflect

Crop

Object Operations

Examples:

Object detection

Grouping

Object counting

Attribute Operations

Examples:

Color

Size

Position

Relational Operations

Examples:

Above

Below

Adjacent

Contained

Composition Operations

Examples:

Chain

Nest

Compose

Deliverable
primitive_inventory.csv

Exit Criteria
100% primitive coverage.

2A.3 Expressivity Analysis
Purpose

Determine theoretical capability.

For every primitive:

What can it express?

What cannot it express?


Example

Primitive:

Rotate


Can express:

Rotational transforms


Cannot express:

Counting relations

Deliverable
expressivity_matrix.csv

2A.4 ARC Task Coverage Audit
Purpose

Map ARC task requirements.

Each ARC task family should be tagged:

Representable

Partially Representable

Not Representable

Unknown

Categories

Examples:

Object manipulation

Counting

Symmetry

Grouping

Relational reasoning

Composition

Deliverable
arc_coverage_audit.csv

Exit Criteria
Coverage map complete.

2A.5 Missing Concept Audit
Purpose

Identify concepts absent from representation.

Possible examples:

Object permanence

Hierarchies

Counting

Relations

Patterns

Recursion

Rule

Missing concepts must be evidenced.

Not guessed.

Deliverable
missing_concepts_audit.md

2A.6 Search Interaction Audit

This is critical.

Purpose

Separate:

Representation failure


from

Search failure.


Questions:

Representable but not found?

Or not representable?


Example

Coverage low


may mean:

Search failure


rather than:

Representation failure.

Deliverable
search_representation_interaction.md

2A.7 Representation Bottleneck Assessment
Purpose

Assess current evidence.

Possible outcomes:

B1
Strong evidence

B2
Moderate evidence

B3
Weak evidence

B4
Unresolved

Rule

Representation must not automatically be declared the cause.

Deliverable
representation_bottleneck_assessment.md

2A.8 Alternative Representation Requirements
Purpose

Specify future comparison conditions.

Must define:

Reference representation

Alternative representation

Comparison rules

Goal

Allow future testing of:

Representation hypothesis.

Deliverable
representation_requirements_v2.md

2A.9 Readiness Review
Required Questions
Q1
Primitive inventory complete?

Q2
Coverage map complete?

Q3
Missing concepts identified?

Q4
Search vs representation separated?

Q5
Representation bottleneck assessed?

Q6
Alternative comparison condition defined?

Readiness Gates
Gate R1
Primitive inventory complete.

Gate R2
Coverage audit complete.

Gate R3
Expressivity analysis complete.

Gate R4
Search interaction audit complete.

Gate R5
Alternative representation condition specified.

Gate R6
Representation hypothesis remains falsifiable.

Deliverables
historical_representation_audit.md

primitive_inventory.csv

expressivity_matrix.csv

arc_coverage_audit.csv

missing_concepts_audit.md

search_representation_interaction.md

representation_bottleneck_assessment.md

representation_requirements_v2.md

phase2A_readiness_review.md

Phase 2A Exit Decision
PASS

Only if:

Representation fully documented

Coverage mapped

Missing concepts identified

Search interactions analyzed

Alternative condition defined

FAIL

If:

Representation still treated as
an undefined explanation.

Coverage unknown.

Search and representation conflated.

Most Important Outcome

The single most important result of Phase 2A is not:

Representation is the bottleneck.


The most important result is:

We know whether representation
is even a plausible bottleneck.


Because Phase 14 only established:

Representation
=
leading hypothesis


not:

Representation
=
proven cause.


Phase 2A should be the phase that finally turns that hypothesis into something testable.