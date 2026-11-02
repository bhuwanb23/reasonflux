Excellent. Phase 1G is the highest-impact benchmark in ASFT v1.1 from an ARC perspective.

If:

Phase 1B = SCT credibility

Phase 1C = IDT credibility

Phase 1D = Memory challenge

Phase 1E = Capability validation

Phase 1F = Intelligence validation


then:

Phase 1G
=
External validity benchmark.


This phase exists because Phase 14G and 14J identified the biggest reality check of v1.0:

The synthetic pipeline activated.

ARC pipeline did not.


And importantly:

ARC failure

≠

Theory failure


but also:

ARC failure

≠

Success.


So Phase 1G is designed to finally answer:

"Can the ASFT mechanism chain activate outside the synthetic ecosystem?"

ASFT v1.1
Phase 1G – ARC Generalization Benchmark Specification

Phase ID

ASFT-V1.1-PHASE-1G


Package

ASFT-V1.1-PHASE-1G-ARC-GENERALIZATION-SPEC-V1

Primary Research Question
RQ6

Can the invariant → skill → transfer →
capability chain activate on ARC under
a protocol-conformant representation
with measurable downstream benefit?

Why This Phase Exists
v1.0 ARC Findings

Observed:

Very low coverage

↓

Very few successful traces

↓

No invariants

↓

No skills

↓

No capability groups


Result:

Mechanism chain unavailable.


Phase 14 conclusion:

ARC did not falsify ASFT.

ARC did not validate ASFT.

ARC mostly failed upstream.

Phase Goal

Create an ARC benchmark that can separately evaluate:

Representation

Coverage

Invariants

Skills

Transfer

Capabilities

Accuracy


instead of collapsing them together.

Core Principle

Coverage is not accuracy.

Accuracy is not transfer.

Transfer is not capability.

Capability is not intelligence.

Every stage must be measured separately.

Phase Structure
1G.1 ARC Failure Audit

1G.2 Representation Requirements

1G.3 Coverage Benchmark

1G.4 Discovery Benchmark

1G.5 Invariant Benchmark

1G.6 Skill Formation Benchmark

1G.7 Transfer Benchmark

1G.8 Capability Benchmark

1G.9 ARC Accuracy Benchmark

1G.10 Protocol Integrity Framework

1G.11 Preregistration Framework

1G.12 Readiness Review

1G.1 ARC Failure Audit
Purpose

Audit exactly why v1.0 ARC failed.

Inputs
Phase 13G

Phase 14G

Phase 14H

Phase 14I

Phase 14J

Questions
What failed?

Where did it fail?

What remained untested?

What was unavailable?

Output
arc_failure_audit.md

Exit Criteria
Every ARC bottleneck documented.

1G.2 Representation Requirements
Purpose

Define minimum representation requirements.

v1.0 Problem
10 primitive operations


Potential gaps included:

Objects

Counting

Grouping

Relations

Composition

Patterns

Deliverable
representation_requirements.md

Rule

Do not assume:

More primitives
=
better.


Requirements must be justified.

1G.3 Coverage Benchmark

This is the most important redesign.

Purpose

Measure representation coverage.

Required Outputs
Coverage Rate
Tasks representable

Trace Rate
Successful traces

Candidate Rate
Invariant candidates

Skill Rate
Potential skills

Rule

Coverage must be reported separately from:

Accuracy.

Deliverable
coverage_benchmark_spec.md

1G.4 Discovery Benchmark
Purpose

Measure discovery independently.

Questions:

Can traces be generated?

Can structures be identified?

Can candidates be proposed?

Outputs
Discovery Yield

Candidate Yield

Trace Diversity

Goal

Separate:

Discovery failure

from

Transfer failure.

1G.5 Invariant Benchmark
Purpose

Measure invariant formation.

Questions:

Do recurring patterns exist?

Can they be discovered?

Do they survive validation?

Outputs
Invariant Count

Invariant Precision

Invariant Survival

Rule

Zero invariants must be reported as:

Zero invariants


not:

Theory failure.

1G.6 Skill Formation Benchmark
Purpose

Measure skill creation independently.

Questions:

Do skills form?

How many?

What support exists?

Outputs
Skill Count

Promotion Rate

Skill Survival

Rule

Skill formation must be measurable even if:

Transfer fails.

1G.7 Transfer Benchmark
Purpose

Measure transfer separately.

Questions:

Can skills transfer?

Do transferred skills help?

Outputs
Transfer Rate

Transfer Utility

Negative Transfer Rate

Rule

No skill denominator:

Transfer unavailable


not:

Transfer zero.

1G.8 Capability Benchmark
Purpose

Measure capability formation.

Questions:

Do capability groups form?

Do they persist?

Do they help?

Outputs
Capability Count

Capability Persistence

Capability Utility

Rule

Capability metrics follow Phase 1E definitions.

1G.9 ARC Accuracy Benchmark
Purpose

Measure task success.

Questions:

How many tasks solved?

How many transfer tasks solved?

How many holdout tasks solved?

Outputs
Exact Accuracy

Partial Accuracy

Family Accuracy

Rule

Accuracy must never be used as:

Coverage


or

Transfer


evidence.

1G.10 Protocol Integrity Framework

This is critical because of Phase 13G.

Required Controls
C1
Budget consistency


Config and code must match.

C2
Holdout integrity

C3
Evaluation isolation

C4
Coverage transparency

C5
Failure logging

Deliverable
protocol_integrity_framework.md

1G.11 Preregistration Framework

Must freeze:

Representation

Coverage metric

Discovery metric

Transfer metric

Capability metric

Accuracy metric

Baselines

Budgets

Splits

Decision rules

Outcomes
Supported

Contradicted

Inconclusive

Unavailable

1G.12 Readiness Review
Checklist
Failure Audit

✅

Representation Requirements

✅

Coverage Benchmark

✅

Discovery Benchmark

✅

Invariant Benchmark

✅

Skill Benchmark

✅

Transfer Benchmark

✅

Capability Benchmark

✅

Accuracy Benchmark

✅

Protocol Integrity

✅

Preregistration

✅

Deliverables
arc_failure_audit.md

representation_requirements.md

coverage_benchmark_spec.md

discovery_benchmark_spec.md

invariant_benchmark_spec.md

skill_benchmark_spec.md

transfer_benchmark_spec.md

capability_benchmark_spec.md

arc_accuracy_spec.md

protocol_integrity_framework.md

arc_preregistration_template.md

phase1G_readiness_report.md

Phase 1G Exit Decision

PASS only if:

Coverage can be measured

Discovery can be measured

Invariants can be measured

Skills can be measured

Transfer can be measured

Capabilities can be measured

Accuracy can be measured

All independently


and:

Config-code consistency checks exist

Holdout protocol exists

Coverage and accuracy are separated

Budgets are frozen

Most Important Outcome

The single most important result of Phase 1G is not:

Higher ARC score.


It is:

The ability to determine exactly where the ASFT mechanism chain succeeds or fails on ARC without confusing representation, coverage, discovery, transfer, capability formation, and accuracy.

That was the biggest lesson from Phase 14G. Before trying to improve ARC performance, v1.1 must ensure that an ARC result is scientifically diagnosable. Otherwise, another failure would tell us very little about what actually broke.