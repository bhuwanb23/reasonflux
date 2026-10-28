Perfect. And I completely agree with your approach.

At this stage, Phase 11 is not about code.

Phase 11 is about creating the engineering specification document.

A good researcher should be able to hand this document to 5 different engineers and all 5 should build roughly the same system.

So for Phase 11B, we should not discuss classes, functions, or implementation syntax.

We should define:

Information Objects
Relationships
Contracts
State
Lifecycle
Data Flow


This phase is so important that I would split it into 6 sub-phases.

Phase 11B: Data Models & Interfaces
Goal

Define:

What information exists in ASFT?

Before:

How it is implemented

Phase 11B Structure
11B-1
Core Knowledge Objects

11B-2
State Models

11B-3
Interface Contracts

11B-4
Lifecycle Models

11B-5
System Memory Model

11B-6
Information Flow Architecture

Phase 11B-1
Core Knowledge Objects

This is the ontology of ASFT.

Meaning:

What entities exist?

Object 1
Task

Definition:

A problem instance presented to the system.

Contains:

Task ID

Task Family

Input State

Expected Outcome

Difficulty

Metadata


Examples:

Reflection Task

Rotation Task

Counting Task


Important:

A task is temporary.

It is not stored permanently as intelligence.

Object 2
Reasoning Trace

Definition:

A structured record of how a task was solved.

Contains:

Operations

Sequence

Cost

Outcome

Dependencies


Example:

Detect Object

Find Symmetry

Apply Reflection

Verify


Important:

Traces are the raw learning material of ASFT.

Object 3
Invariant

Definition:

A recurring reasoning structure discovered across traces.

Contains:

Pattern

Frequency

Consistency

Generality

Transfer Contribution

Strength


Example:

Reflection Pattern


Important:

Invariant ≠ Skill

Invariant = Observation

Object 4
Concept

Important note:

For MVP:

Concepts exist
but remain lightweight


Definition:

A semantic explanation connecting multiple invariants.

Example:

Reflection

Rotation

Translation

↓

Transformation


Important:

Concepts are mostly future-facing in v0.1.

Object 5
Skill Candidate

Definition:

An invariant currently being evaluated for promotion.

Contains:

Source Invariant

Expected Reuse

Expected Transfer

Creation Cost

SCV


Status:

Temporary

Object 6
Skill

Definition:

A reusable capability.

Contains:

Trigger Conditions

Execution Policy

Utility

Transfer History

Reuse History


Important:

Skill = Executable Knowledge

Object 7
Capability State

Definition:

Current intelligence state of the system.

Contains:

Skills

Transfer Metrics

Growth Metrics

Historical Progress


Important:

This is the object used by CGM.

Phase 11B-2
State Models

Now define:

What states can each object be in?

Skill States

Most important.

Lifecycle:

Candidate

↓

Promoted

↓

Active

↓

Dormant

↓

Retired


Meaning:

Candidate

Being evaluated.

Promoted

Passed SCT.

Active

Frequently reused.

Dormant

Not recently used.

Retired

Removed from active reasoning.

Invariant States
Detected

↓

Validated

↓

Strong

↓

Archived


Not every invariant survives.

Capability States

System-level state.

Examples:

Cold Start

Emerging Skills

Transfer Enabled

Capability Growth


Useful later for analysis.

Phase 11B-3
Interface Contracts

One of the most important sections.

Question:

What information can modules exchange?

Contract 1

Trace Logger → Invariant Detector

Provides:

Reasoning Traces


Only.

Invariant Detector should NOT see:

Raw Tasks


directly.

Reason:

Maintain modularity.

Contract 2

Invariant Detector → SCT

Provides:

Validated Invariants


SCT should not need:

Raw Traces

Contract 3

SCT → Skill Library

Provides:

Promoted Skills


Library should not decide:

Whether skill exists


Only store/manage.

Contract 4

Skill Library → Evaluation Engine

Provides:

Usage Statistics

Reuse Data

Transfer Data

Phase 11B-4
Lifecycle Models

How knowledge evolves.

Trace Lifecycle
Task

↓

Trace Created

↓

Stored

↓

Used For Mining

↓

Archived

Invariant Lifecycle
Trace Pattern

↓

Detected

↓

Validated

↓

Strong Invariant

↓

Feeds SCT

Skill Lifecycle
Invariant

↓

Candidate

↓

Promoted

↓

Active Skill

↓

Dormant

↓

Retired


This lifecycle is central to ASFT.

Phase 11B-5
System Memory Model

This is extremely important.

ASFT has 3 memory layers.

Layer 1
Experience Memory

Stores:

Tasks

Traces


Purpose:

Learning material.

Layer 2
Abstraction Memory

Stores:

Invariants

Concepts


Purpose:

Generalization.

Layer 3
Capability Memory

Stores:

Skills

Capability State


Purpose:

Future performance.

This hierarchy is one of the strongest architectural decisions we've made.

Phase 11B-6
Information Flow Architecture

Final system information flow.

Stage 1

Task arrives.

Produces:

Reasoning Trace

Stage 2

Trace enters:

Experience Memory

Stage 3

Invariant Detector discovers:

Invariant

Stage 4

Invariant enters:

Abstraction Memory

Stage 5

SCT evaluates:

Skill Creation

Stage 6

Promoted skill enters:

Capability Memory

Stage 7

Future task arrives.

System retrieves:

Relevant Skill

Stage 8

Reasoning cost decreases.

Stage 9

Capability grows.

Most Important Deliverable of Phase 11B

After all our investigations, architecture design, and engineering planning, I think the single most important specification we've arrived at is:

Experience Memory
↓
Abstraction Memory
↓
Capability Memory


Because it directly mirrors the ASFT thesis:

Experience
↓
Invariant Discovery
↓
Skill Formation
↓
Capability Growth


and gives us a clean information architecture for the entire system.

Next Recommended Split

Phase 11C is too large to do in one shot.

I would split it into:

11C-1
Invariant Discovery Specification

11C-2
Trace Mining Specification

11C-3
Invariant Ranking & Validation

11C-4
Transfer-Aware Invariant Discovery

11C-5
Failure Modes & Edge Cases


because Contribution 1 (IDT) is currently the highest-risk part of the entire project and deserves its own deep specification phase.