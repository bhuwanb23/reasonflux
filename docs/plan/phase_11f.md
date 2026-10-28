Phase 11F: Implementation-Ready Build Checklist

This is the final specification phase.

After this phase, there should be zero ambiguity about:

What to build

Why it exists

What research claim it supports

How it will be validated

What success looks like


At this point we are transitioning from:

Research
↓
Specification


to

Engineering
↓
Experiments

Phase 11F Objective

Produce a complete implementation-ready blueprint for:

ASFT v0.1


focused on validating:

Contribution 1
IDT

Contribution 2
SCT

Contribution 3
CGM

ASFT Build Hierarchy

Everything in the system belongs to one of five layers:

Layer 1
Experience Layer

Layer 2
Invariant Layer

Layer 3
Skill Layer

Layer 4
Capability Layer

Layer 5
Evaluation Layer

MASTER IMPLEMENTATION CHECKLIST
Layer 1: Experience Layer
Objective

Convert task solving into structured learning data.

Module 1
Task System

Purpose:

Represent tasks.

Checklist:

✅ Task identity

✅ Task family

✅ Task metadata

✅ Task difficulty

✅ Task grouping

✅ Synthetic task support

✅ ARC task support

Output:

Task Object


Research Support:

Foundation for everything

Module 2
Reasoning Trace System

Purpose:

Capture reasoning.

Checklist:

✅ Reasoning step representation

✅ Operation taxonomy

✅ Trace storage

✅ Trace normalization

✅ Trace indexing

✅ Trace retrieval

✅ Trace versioning

✅ Trace validation

Output:

Reasoning Trace


Research Support:

IDT

Module 3
Experience Memory

Purpose:

Store historical experiences.

Checklist:

✅ Trace repository

✅ Task repository

✅ Episode history

✅ Experience indexing

✅ Historical lookup

Output:

Experience Memory

Layer 2: Invariant Layer

Supports:

Contribution 1

Module 4
Trace Mining Engine

Checklist:

✅ Trace segmentation

✅ Pattern extraction

✅ Pattern aggregation

✅ Candidate generation

✅ Candidate storage

Output:

Invariant Candidates

Module 5
Invariant Discovery Engine

Checklist:

✅ Frequency analysis

✅ Consistency analysis

✅ Generality analysis

✅ Transfer-awareness

✅ Confidence estimation

✅ Evidence accumulation

Output:

Validated Invariants

Module 6
Invariant Ranking Engine

Checklist:

✅ Invariant scoring

✅ Ranking

✅ Filtering

✅ Promotion eligibility

✅ False positive rejection

✅ Noise handling

Output:

Promotable Invariants

Module 7
Invariant Robustness System

Checklist:

✅ Variation survival testing

✅ Spurious invariant detection

✅ Transfer validation

✅ Negative transfer detection

✅ Invariant explosion monitoring

Output:

Trusted Invariants

Layer 3: Skill Layer

Supports:

Contribution 2

Module 8
Skill Candidate System

Checklist:

✅ Candidate creation

✅ Candidate tracking

✅ Candidate evidence

✅ Candidate confidence

Output:

Skill Candidates

Module 9
Skill Economics Engine

Checklist:

✅ SCV computation

✅ Utility computation

✅ Cost estimation

✅ Benefit estimation

✅ Reuse estimation

✅ Transfer estimation

Output:

Economic Decision

Module 10
Skill Promotion Engine

Checklist:

✅ Promotion rules

✅ Threshold checks

✅ Duplicate detection

✅ Promotion history

✅ Promotion evidence

Output:

Active Skills

Module 11
Skill Library

Checklist:

✅ Skill storage

✅ Skill retrieval

✅ Skill indexing

✅ Skill search

✅ Skill ranking

✅ Skill statistics

Output:

Skill Memory

Module 12
Skill Lifecycle Manager

Checklist:

✅ Active state

✅ Growing state

✅ Core state

✅ Dormant state

✅ Retired state

✅ Archived state

✅ Reactivation state

Output:

Skill State Updates

Module 13
Skill Composition Engine

Checklist:

✅ Sequential composition

✅ Composition candidates

✅ Composition utility

✅ Composition confidence

✅ Composition evidence

✅ Composition reuse tracking

Output:

Composed Capabilities

Module 14
Skill Robustness Engine

Checklist:

✅ Skill explosion detection

✅ Negative transfer detection

✅ Retrieval failure detection

✅ Duplicate detection

✅ Composition failure detection

✅ Health scoring

Output:

Healthy Skill Ecosystem

Layer 4: Capability Layer

Supports:

Contribution 3

Module 15
Capability Representation System

Checklist:

✅ Capability identity

✅ Capability membership

✅ Capability hierarchy

✅ Capability graph

✅ Capability portfolio

✅ Capability evidence

Output:

Capability Objects

Module 16
Capability Growth Engine

Checklist:

✅ Capability state

✅ Capability growth tracking

✅ Capability coverage

✅ Capability utility

✅ Growth history

✅ Growth trends

Output:

Capability Growth Signals

Module 17
Intelligence Growth Engine

Checklist:

✅ Intelligence state

✅ Intelligence function

✅ IGR computation

✅ Intelligence efficiency

✅ Intelligence elasticity

✅ Intelligence maturity stage

Output:

Intelligence Metrics

Module 18
Capability Robustness Engine

Checklist:

✅ Growth illusion detection

✅ Fragmentation detection

✅ Inflation detection

✅ Saturation detection

✅ Collapse detection

✅ Recovery monitoring

Output:

Reliable Capability Metrics

Layer 5: Evaluation Layer

This validates the paper.

Module 19
Metrics Engine

Checklist:

✅ IS

✅ SU

✅ TS

✅ CGR

✅ IGR

✅ Coverage

✅ Utility

✅ Confidence

✅ Health

Output:

Research Metrics

Module 20
Benchmark Engine

Checklist:

✅ Synthetic benchmark

✅ Transfer benchmark

✅ Capability benchmark

✅ ARC validation benchmark

Output:

Benchmark Results

Module 21
Baseline Engine

Checklist:

✅ No Learning

✅ Skill Storage

✅ Random Skill Creation

✅ DreamCoder-like

Output:

Baseline Comparisons

Module 22
Ablation Engine

Checklist:

✅ Remove IDT

✅ Remove SCT

✅ Remove Transfer

✅ Remove Skill Library

✅ Remove CGM

Output:

Contribution Validation

Module 23
Reporting Engine

Checklist:

✅ Invariant reports

✅ Skill reports

✅ Transfer reports

✅ Capability reports

✅ Intelligence reports

✅ Experiment summaries

Output:

Paper Tables
Paper Figures

MVP PRIORITY ORDER

This is extremely important.

Build in this exact order.

Phase A

Foundation

Task System

Trace System

Experience Memory


Goal:

Generate Reliable Traces

Phase B

IDT

Trace Mining

Invariant Discovery

Invariant Ranking


Goal:

ReflectionInvariant
RotationInvariant
CountingInvariant

Phase C

SCT

Skill Candidate

Skill Economics

Skill Promotion

Skill Library


Goal:

ReflectionSkill


created automatically.

Phase D

Transfer

Skill Retrieval

Skill Reuse

Transfer Measurement


Goal:

Task A
helps
Task B

Phase E

CGM

Capability Representation

Capability Growth

Intelligence Growth


Goal:

Positive CGR

Positive IGR

Phase F

Evaluation

Benchmarks

Baselines

Ablations

Reports


Goal:

Research Evidence

RESEARCH CLAIM MAPPING

Every module must justify its existence.

IDT Claim
Transferable knowledge
emerges from invariants.


Modules:

4
5
6
7

SCT Claim
Skills should emerge
when economically justified.


Modules:

8
9
10
11
12
13
14

CGM Claim
Intelligence should be measured
through capability growth.


Modules:

15
16
17
18
19

MVP SUCCESS CHECKLIST

ASFT v0.1 is successful if all are true:

IDT

✅ Reflection invariant discovered

✅ Rotation invariant discovered

✅ Invariant ranking works

✅ Transfer-aware invariants emerge

SCT

✅ Reflection skill created

✅ Skill reused

✅ Utility positive

✅ Transfer positive

CGM

✅ Capability represented

✅ Capability grows

✅ Positive CGR

✅ Positive IGR

Evaluation

✅ Baselines beaten

✅ Ablations show degradation

✅ Evidence supports claims

PAPER READINESS CHECKLIST

Before writing final paper:

✅ All three contributions implemented

✅ All metrics operational

✅ Baselines completed

✅ Ablations completed

✅ Failure modes tested

✅ Transfer demonstrated

✅ Capability growth demonstrated

✅ Intelligence growth demonstrated

✅ Results reproducible

✅ Figures generated

✅ Tables generated

What Should NOT Be Built In v0.1

This is just as important.

Do NOT build:

❌ LLM planner

❌ Autonomous agent

❌ Meta-reasoner

❌ World model

❌ Recursive self-improvement

❌ Concept graph engine

❌ Neural skill embeddings

❌ ARC leaderboard optimizer

❌ Multi-agent architecture

❌ AGI framework

These belong to:

ASFT v0.2
ASFT v1.0


not the research MVP.

Final Outcome of Phase 11F

You now have a complete chain:

Research
✅

Theory
✅

Architecture
✅

Mathematics
✅

Novelty Validation
✅

Prototype Design
✅

Experiment Design
✅

Paper Blueprint
✅

Engineering Specification
✅

Implementation Checklist
✅


The most important conclusion is:

Do not build ASFT as an AGI system. Build ASFT as a scientific instrument whose purpose is to validate three claims:

Invariants can be discovered.
Skills can emerge from invariants through economic triggers.
Capability growth can be measured and used as a proxy for intelligence growth.

If you keep that constraint, the project remains focused, publishable, and experimentally defensible.