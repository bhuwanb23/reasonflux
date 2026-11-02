Excellent. Phase 1E is where ASFT v1.1 starts attacking the biggest CGM problem discovered in Phase 14.

Phase 14E essentially concluded:

CGR exists

✅

CGR increases

✅

Capability growth proven

❌


The core problem was:

Internal metric

≠

External capability


So Phase 1E exists to answer a very simple but extremely important question:

"If capability scores go up, can the system actually do more things?"

ASFT v1.1
Phase 1E – Capability Validation Benchmark Specification

Phase ID

ASFT-V1.1-PHASE-1E


Package

ASFT-V1.1-PHASE-1E-CAPABILITY-VALIDATION-SPEC-V1

Primary Research Question
RQ4

Does a capability measure predict
future performance on independently
measured tasks beyond simpler
explanations?

Why This Phase Exists
v1.0 Problem

Phase 13E showed:

Positive CGR

Positive C_t


But Phase 14 showed:

Only one capability object existed.

Capability count remained stable.

External capability not measured.


Therefore:

Capability score increased

↓

Meaning unknown

Phase Goal

Create an independent benchmark where:

Capability metric

and

Capability behavior


can be compared.

Core Principle

Capability must be measured independently.

Forbidden:

CGR validates CGR

C_t validates C_t

IG validates capability


Required:

External behavioral capability

Phase Structure
1E.1 Capability Audit

1E.2 Capability Definition

1E.3 Capability Taxonomy

1E.4 Independent Capability Battery

1E.5 Capability Growth Framework

1E.6 Comparator Framework

1E.7 Evaluation Metrics

1E.8 Dataset & Split Design

1E.9 Preregistration Framework

1E.10 Readiness Review

1E.1 Capability Audit
Purpose

Understand why capability claims failed.

Inputs
Phase 13E

Phase 13F

Phase 14E

Phase 14H

Phase 14I

Phase 14J

Questions
What did CGR actually measure?

What did C_t actually measure?

What capability evidence was missing?

Why did construct validity fail?

Deliverable
capability_audit.md

Exit Criteria
All v1.0 capability limitations documented.

1E.2 Capability Definition
Purpose

Define capability before measuring it.

Working Definition

A capability must satisfy:

Persistence

Generality

Behavioral utility


Not merely:

Internal score increase

Candidate Requirements

A capability should:

Be reusable

Appear across tasks

Produce measurable benefit

Deliverable
capability_definition.md

Exit Criteria
Capability definition frozen.

1E.3 Capability Taxonomy
Purpose

Create capability categories.

C1
Single-Skill Capability

C2
Multi-Skill Capability

C3
Transfer Capability

C4
Compositional Capability

C5
Adaptive Capability

C6
Cross-Domain Capability

Goal

Avoid treating all capabilities as identical.

Exit Criteria
Capability taxonomy frozen.

1E.4 Independent Capability Battery

This is the heart of the benchmark.

Purpose

Measure capability externally.

Required Tests
Test A
Novel Task Success

Test B
Transfer Success

Test C
Task Breadth

Test D
Retention / Persistence

Test E
Compositional Performance

Test F
Adaptation Performance

Rule

None of these tests may use:

CGR

C_t

IG


as input.

Deliverable
capability_battery_spec.md

1E.5 Capability Growth Framework
Purpose

Define what growth means.

Growth must satisfy:

Behavior change


not merely:

Score change


Examples:

Valid Growth
More task families solved.

Valid Growth
Better transfer.

Invalid Growth
Internal metric rises.


alone.

Exit Criteria
Growth definition frozen.

1E.6 Comparator Framework
Purpose

Prevent circular validation.

Required Comparators
B1
Prior Performance

B2
Experience Count

B3
Memory Strength

B4
Frequency Statistics

B5
Capability Metric

Question

Can capability metrics predict something beyond:

Past performance

Experience

Memory


?

1E.7 Evaluation Metrics
Primary Endpoint

Must be frozen.

Examples:

Future Capability Success

Future Task Breadth

Future Transfer Performance

Secondary Endpoints
Retention

Adaptation

Composition

Cross-domain success

Diagnostics
Capability count

Capability size

Capability persistence

1E.8 Dataset & Split Design
Required Splits
Development

Confirmatory

Replication

Rule

Future capability tests must remain unseen.

Rule

No benchmark tuning using confirmatory tasks.

Deliverable
capability_dataset_protocol.md

1E.9 Preregistration Framework

Freeze:

Capability definition

Primary endpoint

Comparator set

Independent unit

SOI

Decision criteria

Replication plan

Outcomes
Supported

Contradicted

Inconclusive

Unavailable

1E.10 Readiness Review
Checklist
Capability Audit

✅

Capability Definition

✅

Capability Taxonomy

✅

Independent Battery

✅

Growth Definition

✅

Comparators

✅

Metrics

✅

Splits

✅

Preregistration

✅

Deliverables
capability_audit.md

capability_definition.md

capability_taxonomy.md

capability_battery_spec.md

capability_growth_framework.md

capability_comparator_spec.md

capability_metrics.md

capability_dataset_protocol.md

capability_preregistration_template.md

phase1E_readiness_report.md

Phase 1E Exit Decision

PASS only if:

Capability is behaviorally defined

Capability tests are independent

Growth requires behavior change

Capability metrics are not self-validating

Replication is planned

Primary endpoint is frozen

Most Important Outcome

At the end of Phase 1E, ASFT should finally be able to answer the question that Phase 14E could not:

"When a capability score increases, does the system demonstrably acquire broader, more persistent, or more transferable behavioral competence?"

If the answer is yes, CGR gains credibility.

If the answer is no, then one of the most important lessons of v1.1 may be:

Capability metrics were measuring
portfolio bookkeeping rather than
capability growth.


And that is exactly the kind of question a proper capability-validation benchmark is supposed to resolve.