Excellent.

This is the point where we stop discussing ideas and start designing a real research architecture.

Up until now, our theory is:

Experience
↓
Invariant Detection
↓
Concept Formation
↓
Skill Formation
↓
Capability Growth


Now we need to convert that into a system architecture that could theoretically run on ARC-AGI-2, ARC-AGI-3, and become the foundation of a Paper Track submission.

Phase 3B: Adaptive Abstraction Architecture (AAA)
Core Goal

Current ARC systems optimize:

Task
↓
Solution


AAA optimizes:

Task
↓
Capability Growth


The output is not merely:

Answer


but also:

Improved Agent

High-Level Architecture
                    ┌──────────────────┐
                    │     ARC Task     │
                    └────────┬─────────┘
                             │
                             ▼
                  ┌────────────────────┐
                  │ Reasoning Engine   │
                  └────────┬───────────┘
                           │
                  Reasoning Trace
                           │
                           ▼
                ┌──────────────────────┐
                │ Invariant Detector   │
                └────────┬─────────────┘
                         │
                    Invariants
                         │
                         ▼
                ┌──────────────────────┐
                │ Concept Generator    │
                └────────┬─────────────┘
                         │
                     Concepts
                         │
                         ▼
                ┌──────────────────────┐
                │ Skill Constructor    │
                └────────┬─────────────┘
                         │
                      Skills
                         │
                         ▼
                ┌──────────────────────┐
                │ Skill Library        │
                └────────┬─────────────┘
                         │
                         ▼
                ┌──────────────────────┐
                │ Meta-Reasoner        │
                └────────┬─────────────┘
                         │
                    Future Tasks

Module 1: Reasoning Engine
Purpose

Solve current task.

Not novel.

Can use:

Program synthesis
Neuro-symbolic reasoning
Search
DSL
Recursive reasoning

We intentionally do not reinvent this.

Inputs
Task
Examples
Current Skill Library

Outputs
Solution
Reasoning Trace

Important

The key artifact is NOT:

Solution


The key artifact is:

Reasoning Trace


because that becomes learning material.

Reasoning Trace Structure

Example:

Step 1:
Find Objects

Step 2:
Identify Symmetry

Step 3:
Apply Reflection

Step 4:
Verify Output


This becomes the raw learning data.

Module 2: Invariant Detector

This is where our architecture starts becoming novel.

Purpose

Discover recurring structures across reasoning traces.

Input:

Reasoning Traces
Task Histories
Failures
Successes


Output:

Invariant Candidates

What Is An Invariant?

Examples:

Example 1
Red Object
Blue Object
Green Object


Common structure:

Object

Example 2
Rotate Triangle
Rotate Square
Rotate Circle


Common structure:

Rotation

Core Operation
Pattern Mining
+
Difference Elimination
+
Invariant Extraction

Novel Contribution

Most ARC systems search for:

Solutions


AAA searches for:

What remains constant across solutions

Module 3: Concept Generator

This may become the central paper contribution.

Purpose

Transform invariants into concepts.

Input:

Invariant Set


Output:

Concept Candidates

Example

Invariants:

Rotation
Reflection
Translation
Scaling


Generated Concept:

Transformation


Another Example

Invariants:

Counting
Comparing
Ordering


Generated Concept:

Numerical Reasoning

Internal Mechanism

Concept Score:

Concept Score

=
Frequency
×
Compression Gain
×
Transfer Utility


High-scoring concepts survive.

Why This Is Different From DreamCoder

DreamCoder:

Compress Programs


AAA:

Compress Meaning


This distinction may become one of our strongest claims.

Module 4: Skill Constructor

Purpose:

Convert concepts into executable procedures.

Input:

Concepts


Output:

Skills


Example

Concept:

Symmetry


Skill:

Detect Symmetry
Apply Symmetry
Verify Symmetry


Concept:

Grouping


Skill:

Identify Groups
Cluster Objects
Validate Groups

Skill Structure

Every skill contains:

Skill Name

Applicability Conditions

Execution Policy

Expected Outcome

Confidence


Example

Skill:
Reflection

Conditions:
Symmetry Detected

Policy:
Mirror Object

Expected:
Reflected Pattern

Module 5: Skill Library

This is the long-term memory system.

Purpose:

Store reusable capabilities.

Structure

Skill Library

├── Geometry
│   ├── Rotation
│   ├── Reflection
│   └── Scaling
│
├── Counting
│   ├── Count Objects
│   ├── Compare Counts
│
└── Grouping
    ├── Cluster
    └── Segment

Important Property

Library is hierarchical.

Not flat.

Humans organize knowledge hierarchically.

Skill Promotion Rule

A concept becomes a skill when:

Reuse Frequency
×
Transfer Utility
×
Success Rate


exceeds threshold.

Module 6: Meta-Reasoner

This is the AGI-oriented component.

Purpose

Reason about:

Reasoning
Concepts
Skills
Learning


Questions It Asks

Question 1
Why did this task fail?

Question 2
Missing skill?

Question 3
Bad concept?

Question 4
Need more search?

Question 5
Need a new abstraction?

This Is Critical

Current systems usually do:

Failure
↓
More Search


AAA can do:

Failure
↓
Missing Concept
↓
Create Concept


This is a fundamental difference.

Learning Loop

The complete system loop becomes:

Task
↓
Reasoning
↓
Solution
↓
Reasoning Trace
↓
Invariant Detection
↓
Concept Generation
↓
Skill Construction
↓
Skill Library Update
↓
Meta Analysis
↓
Future Tasks Easier

Example Walkthrough

Task A:

Mirror Shape


System discovers:

Reflection


Concept created.

Task B:

Mirror Different Shape


Reflection concept reused.

Task C:

Mirror Object Groups


Reflection + Grouping composed.

Result:

Task A
makes
Task B
and
Task C
easier


Which directly matches the ARC philosophy we have been optimizing for.

The Central Research Claim

The architecture can now be summarized in one sentence:

Intelligence emerges when reasoning traces are transformed into invariants, invariants into concepts, concepts into skills, and skills into reusable capabilities that reduce future reasoning cost.

Deliverables Completed in Phase 3B

✅ Complete architecture

✅ Invariant Detector

✅ Concept Generator

✅ Skill Constructor

✅ Skill Library

✅ Meta-Reasoner

✅ Learning loop

✅ Skill lifecycle

✅ Failure analysis mechanism

✅ ARC-aligned capability growth framework

At this point, the next phase should be Phase 3C: Mathematical Formulation, where we define formal metrics such as:

Reasoning Cost
Abstraction Gain
Concept Utility
Skill Utility
Transfer Score
Capability Growth Rate

Those metrics will determine whether AAA is a research thesis or a rigorous scientific framework.