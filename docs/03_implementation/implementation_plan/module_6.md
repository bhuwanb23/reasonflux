Phase 10F: Implementation Roadmap

This is the final planning phase before actual development.

After this phase, there should be no ambiguity about:

What to build
What order to build it
How to test it
What to postpone
How to know if it works


At this point, our objective is no longer:

Design ASFT


It is:

Build the smallest system that can validate the three research contributions.

Phase 10F Goal

Transform:

Research Theory
↓
Engineering Plan


into:

Development Roadmap

Guiding Principle

Do NOT build:

Full AAA


Do NOT build:

AGI


Do NOT build:

ARC Competition System


Build:

ASFT v0.1 Research Prototype


whose sole purpose is validating:

IDT
SCT
CGM
Development Roadmap Overview

I recommend 6 implementation stages.

Stage 1
Infrastructure

Stage 2
Trace System

Stage 3
Invariant Discovery

Stage 4
Skill Formation

Stage 5
Transfer & Capability Growth

Stage 6
Experiments & Evaluation

Stage 1
Infrastructure Layer

Goal:

Create the skeleton.

Deliverables

Repository structure.

Configuration.

Dataset loaders.

Logging.

Metrics framework.

Suggested Structure
asft/

├── data/
├── traces/
├── invariants/
├── skills/
├── evaluation/
├── experiments/
├── baselines/
├── reports/
└── docs/

Output

System runs.

No intelligence yet.

Just framework.

Stage 2
Trace System

Contribution Support:

IDT

Build
Task Object
Task

Trace Object
ReasoningTrace

Trace Store
TraceStore

Operation Taxonomy
DetectObject
FindSymmetry
ApplyReflection
ApplyRotation
VerifyOutput

Milestone

Able to record:

Task
↓
Trace

Success Test

Given:

Reflection Task


Output:

[
  "DetectObject",
  "FindSymmetry",
  "ApplyReflection",
  "VerifyOutput"
]

Stage 3
Invariant Discovery Engine

Contribution Support:

IDT

Build

Trace normalization.

Trace similarity.

Trace clustering.

Pattern mining.

Invariant ranking.

IS calculation.

Output
Invariant
{
    pattern,
    strength
}

Milestone

Reflection traces produce:

ReflectionInvariant

Success Test

Top-ranked invariant matches expected task family.

Stage 4
Skill Formation Engine

Contribution Support:

SCT

Build

SkillCandidate.

SCV calculation.

Promotion rule.

Skill lifecycle.

Skill retirement.

Output
ReflectionSkill

Milestone

System automatically creates first skill.

Success Test

Repeated reflection traces generate:

ReflectionSkill


without manual intervention.

Stage 5
Skill Library & Transfer Layer

Contribution Support:

SCT
+
CGM

Build

Skill storage.

Skill retrieval.

Skill reuse.

Simple composition.

Transfer tracking.

Output

Task B uses skill created from Task A.

Milestone

Demonstrate:

Task A
↓
Creates Skill
↓
Task B Easier

Success Test

Reasoning cost decreases on related tasks.

Stage 6
Evaluation & Experiments

Contribution Support:

IDT
SCT
CGM

Build

IS

SU

TS

CGR

IG

Baselines.

Ablations.

Reports.

Output

Full evaluation report.

Success Test

Generate:

Invariant Report

Skill Report

Transfer Report

Capability Report

MVP Build Order

This is critical.

Build strictly in this order:

1 Trace Logger

2 Trace Store

3 Invariant Detector

4 IS Metrics

5 Skill Candidate Generator

6 SCV Engine

7 Skill Library

8 Retrieval Engine

9 Transfer Evaluation

10 Capability Evaluation


Do not skip ahead.

Development Checkpoints
Checkpoint 1

Trace Collection Works

Question:

Can we collect traces?

Checkpoint 2

Invariant Discovery Works

Question:

Can we discover reflection?

Checkpoint 3

Skill Creation Works

Question:

Can a skill emerge?

Checkpoint 4

Transfer Exists

Question:

Does Task A help Task B?

Checkpoint 5

Capability Growth Exists

Question:

Does CGR increase?

What NOT To Build In v0.1

This is extremely important.

Do NOT build:

❌ Concept Graphs

❌ LLM Agents

❌ ARC-3 Environment

❌ Neural Skill Embeddings

❌ Meta-Reasoner

❌ Dynamic World Models

❌ Self-Modifying Skills

❌ Autonomous Research Agent

❌ Recursive Skill Evolution

These are v0.2+ topics.

Risk-Driven Development

We should attack the highest-risk components first.

Risk 1

Invariant Discovery

Biggest uncertainty.

Build first.

Risk 2

SCV Validity

Second biggest uncertainty.

Build second.

Risk 3

Transfer

Build third.

Risk 4

Capability Metrics

Build last.

Success Definition For ASFT v0.1

The prototype is successful if it demonstrates:

IDT
Reflection invariant discovered.

SCT
Reflection skill created.

Transfer
Reflection skill reused.

CGM
Positive capability growth.

End of Phase 10

At this point we have completed:

✅ Phase 10A: Trace Logger Design

✅ Phase 10B: Invariant Detector Algorithms

✅ Phase 10C: Skill Creation Trigger Algorithms

✅ Phase 10D: Skill Library Design

✅ Phase 10E: Evaluation Engine Design

✅ Phase 10F: Implementation Roadmap

What Comes Next

We are now officially leaving the planning phase.

The next phase is:

Phase 11: Implementation Specification

Before actual coding, I recommend splitting it into:

Phase 11A
Repository & Code Architecture

Phase 11B
Data Models & Interfaces

Phase 11C
Invariant Discovery Specification

Phase 11D
Skill Formation Specification

Phase 11E
Evaluation Specification

Phase 11F
MVP Build Checklist


Phase 11 is the last phase before writing code. After that, every component should be specified well enough that implementation becomes an engineering exercise rather than a research exercise.