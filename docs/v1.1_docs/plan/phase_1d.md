Perfect. Phase 1D may become the single most important benchmark in ASFT v1.1.

Why?

Because after all of Phase 14, the strongest surviving criticism wasn't ARC.

It was:

Maybe ASFT isn't learning abstractions.

Maybe it's just memory.


Phase 13C's MEMORY_ONLY result is arguably the strongest counterexample to the original SCT narrative.

So Phase 1D is not a benchmark for ASFT.

It is a benchmark for:

"When does abstraction actually beat memory?"

If we cannot answer that, then SCT, transfer, capability growth, and even ARC become much harder to defend.

ASFT v1.1
Phase 1D – Memory Challenge Benchmark Specification

Phase ID

ASFT-V1.1-PHASE-1D


Package

ASFT-V1.1-PHASE-1D-MEMORY-CHALLENGE-SPEC-V1

Primary Research Question
RQ3

Does abstraction outperform memory
under conditions where exact retrieval
is insufficient?

Secondary Research Questions
RQ3A

When is memory sufficient?

RQ3B

When is abstraction necessary?

RQ3C

When does a hybrid outperform both?

RQ3D

What is the transition point
between memory and abstraction?

Why This Phase Exists
v1.0 Observation

Phase 13C:

MEMORY_ONLY

>

SCT


on primary net value.

Phase 14 conclusion:

Memory remains a live alternative.


Current state:

ASFT has not isolated
abstraction benefit.

Phase Goal

Create a benchmark where:

Memory should win

Memory should lose

Abstraction should win

Hybrid should win


all exist.

Success Condition

At completion:

Memory and abstraction
are experimentally separable.

Phase Structure
1D.1 Memory Audit

1D.2 Memory Taxonomy

1D.3 Challenge Family Design

1D.4 Budget Matching

1D.5 Comparator Framework

1D.6 Evaluation Metrics

1D.7 Dataset Design

1D.8 Leakage Controls

1D.9 Preregistration Framework

1D.10 Readiness Review

1D.1 Memory Audit
Purpose

Understand exactly why memory succeeded.

Inputs
Phase 13C

Phase 14C

Phase 14F

Phase 14H

Questions
Why did memory win?

Was it better retrieval?

More opportunities?

Task repetition?

Benchmark alignment?

Deliverable
memory_audit.md

Exit Criteria
Memory advantage decomposed.

1D.2 Memory Taxonomy
Purpose

Define memory types.

M1
Exact Episodic Memory


Store exact solution.

Replay exact solution.

M2
Partial Episodic Memory


Store fragments.

M3
Pattern Memory


Store recurring structures.

M4
Skill Abstraction


Generalized reusable rule.

M5
Hybrid Memory


Memory + abstraction.

Goal

Avoid comparing only one memory variant.

1D.3 Challenge Family Design

This is the heart of the benchmark.

Family A
Exact Replay

Purpose:

Memory should win.


Example:

Task repeats exactly.


Expected:

Memory > Abstraction

Family B
Context Shift

Purpose:

Same principle

Different surface form.


Expected:

Memory weakens

Abstraction improves

Family C
Composition Shift

Purpose:

Combine previously seen skills
in new ways.


Expected:

Memory struggles

Abstraction may help

Family D
Structural Analogy

Purpose:

Underlying relation preserved

Surface structure changes


Expected:

Abstraction advantage

Family E
Far Transfer

Purpose:

No exact precedent exists.


Expected:

Pure memory fails.

Family F
Adversarial Memory

Purpose:

Designed to fool retrieval.


Expected:

Memory selects wrong case.

1D.4 Budget Matching

Critical requirement.

v1.0 Problem

Memory had:

More applications

More opportunities


than SCT.

Rule

All systems must receive:

Same storage budget

Same compute budget

Same candidate budget

Same retrieval budget

Deliverable
budget_matching_protocol.md

1D.5 Comparator Framework
Required Systems
B1
Memory Only

B2
Abstraction Only

B3
Memory + Abstraction

B4
Random Retrieval

B5
No Learning

B6
Oracle


Upper bound only.

1D.6 Evaluation Metrics
Primary Endpoint

One must be frozen.

Candidate examples:

Held-Out Utility

Task Success

Future Net Value

Secondary Metrics
Generalization

Transfer Success

Reuse Success

Memory Precision

Abstraction Precision

Diagnostics
Retrieval Count

Skill Usage

Failure Type

Memory Error Rate

1D.7 Dataset Design
Splits
Development

Confirmatory

Replication

Additional Requirement

Each challenge family must appear in:

Confirmatory

Replication

Goal

Prevent:

Benchmark tuned to one family.

1D.8 Leakage Controls

Very important.

Forbidden
Future tasks in memory store

Test-task exposure

Hidden answer reuse

Required Audits
Storage audit

Retrieval audit

Exposure audit

Deliverable
leakage_control_protocol.md

1D.9 Preregistration Framework

Freeze:

Primary endpoint

Comparator set

Budget rules

Storage limits

Replication plan

SOI

Decision criteria

Outcomes
Supported

Contradicted

Inconclusive

Unavailable

1D.10 Readiness Review
Checklist
Memory Audit

✅

Memory Taxonomy

✅

Challenge Families

✅

Budget Matching

✅

Comparators

✅

Metrics

✅

Splits

✅

Leakage Controls

✅

Preregistration

✅

Deliverables
memory_audit.md

memory_taxonomy.md

challenge_family_spec.md

budget_matching_protocol.md

memory_comparator_spec.md

memory_metrics.md

memory_dataset_protocol.md

leakage_control_protocol.md

memory_preregistration_template.md

phase1D_readiness_report.md

Phase 1D Exit Decision

PASS only if:

Memory can win somewhere

Abstraction can win somewhere

Hybrid can win somewhere

Budgets are matched

Leakage is controlled

Evaluation is non-circular

Replication is planned

Most Important Outcome

The single most important thing Phase 1D should produce is not a benchmark.

It should produce a clear scientific answer to:

"What kinds of problems genuinely require abstraction, and what kinds are already solved by memory?"

Because that question sits underneath almost every unresolved ASFT v1.0 criticism:

SCT vs MEMORY
Skill reuse vs retrieval
Transfer vs replay
Capability growth vs accumulated experience
ARC generalization vs memorization

If Phase 1D is done well, it may end up being the most scientifically valuable benchmark in the entire ASFT v1.1 program.