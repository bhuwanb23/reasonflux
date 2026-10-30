Phase 9E: Paper Blueprint

This is one of the highest-leverage phases in the entire project.

A common mistake is:

Research
↓
Code
↓
Results
↓
Try to write paper


The stronger approach is:

Research
↓
Paper Blueprint
↓
Implementation
↓
Fill Paper With Results


After Phase 9E, every module you build should map directly to a section of the paper.

Paper Strategy

We are not writing a paper called:

"A New ARC Solver"

That would immediately place us into competition with:

Program synthesis
Neuro-symbolic methods
Recursive reasoning
Refinement loops
ARC leaderboard solutions

Instead, our paper should be positioned as:

A theory and framework for skill formation and capability growth.

This is much closer to the ARC philosophy of skill-acquisition efficiency described in On the Measure of Intelligence.

Candidate Paper Title
Option A (Research-Oriented)

Adaptive Skill Formation Theory: From Reasoning Traces to Reusable Capabilities

Option B (ARC-Oriented)

Beyond Task Solving: Skill Formation as a Mechanism for Capability Growth in ARC-AGI

Option C (Most Likely Winner Style)

Learning Skills, Not Solutions: Invariant Discovery and Capability Growth for ARC-AGI

Personally, Option C is strongest right now.

Paper Structure
1. Abstract
Purpose

State:

Problem
Contribution
Results
Impact

Template

Current AI systems primarily optimize task solutions but provide limited mechanisms for cumulative capability growth. We introduce Adaptive Skill Formation Theory (ASFT), a framework in which reusable skills emerge from recurring reasoning patterns through invariant discovery and skill creation triggers. We present three contributions: Invariant Discovery Theory, Skill Creation Trigger Theory, and Capability Growth Metrics. Experimental results demonstrate positive transfer, reduced reasoning cost, and measurable capability growth across task families.

2. Introduction
Goal

Introduce the central ARC problem.

Section Flow
2.1 Current AI
Good at solving tasks
Poor at accumulating capability

2.2 ARC Philosophy

Use:

On the Measure of Intelligence

and ARC principles.

2.3 Research Question

State:

If an agent solves Task A, how does that make Task B easier?

This becomes the central paper question.

2.4 Thesis

Introduce ASFT.

Figure 1
Motivation Diagram
Traditional AI

Task
↓
Solution
↓
Stop

ASFT

Task
↓
Skill Formation
↓
Future Tasks Easier

3. Related Work

This section positions us against prior art.

3.1 Program Synthesis

Discuss:

DSL methods
Program search
Evolutionary synthesis
Key Position

Program synthesis learns solutions.

ASFT studies skill formation.

3.2 Neuro-Symbolic Systems

Discuss:

Object-centric reasoning
Symbolic abstraction
Position

Neuro-symbolic systems use abstractions.

ASFT studies abstraction emergence.

3.3 DreamCoder

Most important subsection.

Position:

DreamCoder:

Program Compression


ASFT:

Skill Formation

3.4 Lifelong Learning

Discuss:

Voyager
Skill libraries
Continual learning

Position:

Most systems study skill reuse.

ASFT studies skill creation.

4. Adaptive Skill Formation Theory

This is the core theory section.

4.1 Definitions

Formal definitions.

Introduce:

Invariant
Concept
Skill
Capability

From Phase 3A.

Figure 2

Concept hierarchy:

Experience
↓
Invariant
↓
Concept
↓
Skill
↓
Capability

4.2 Invariant Discovery Theory

Contribution 1.

Formal claim.

Hypotheses.

Mathematical definition of:

IS

4.3 Skill Creation Trigger Theory

Contribution 2.

Introduce:

SCV


and:

Create skill if SCV > 0

Figure 3

Skill emergence diagram.

Repeated Trace
↓
Invariant
↓
SCV
↓
Skill

4.4 Capability Growth Metrics

Contribution 3.

Introduce:

TS
CGR
IG

5. ASFT Architecture

This is our system section.

Modules
Trace Logger
Invariant Detector
Skill Creation Trigger
Skill Library
Capability Monitor
Figure 4

Full architecture diagram.

Task
↓
Trace
↓
Invariant
↓
Skill
↓
Transfer
↓
Growth

6. Experimental Setup

Derived from Phase 8D.

Datasets

Reflection

Rotation

Counting

Transfer

ARC Validation

Baselines

No Learning

Skill Storage

DreamCoder-like

Random Skills

Ablations

A1-A5

Table 1

Experimental matrix.

7. Results

This is where implementation results go later.

7.1 Invariant Discovery

Metrics:

IS
Precision
Recall

Figure 5

Invariant discovery performance.

7.2 Skill Formation

Metrics:

SCV
SU
Reuse Count

Figure 6

Skill emergence timeline.

7.3 Transfer

Metrics:

TS

Figure 7

Transfer performance.

7.4 Capability Growth

Metrics:

CGR
IG

Figure 8

Growth curves.

8. Discussion

Very important for Paper Track.

Questions
Why did ASFT work?
When does it fail?
What does this imply for ARC?
What does this imply for AGI?
9. Limitations

Reviewers love honesty.

Examples:

Limited task families
Simplified concepts
Prototype-level implementation
Not a complete AGI architecture
10. Future Work

Future directions:

Concept Formation

Meta-Reasoning

ARC-AGI-3

Dynamic Skill Evolution

11. Conclusion

One key statement:

We argue that intelligence growth emerges not from solving more tasks, but from transforming reasoning experiences into reusable skills that improve future capability.

Paper Figures Master Plan
Figure	PurposeFig 1	Motivation
Fig 2	Theory hierarchy
Fig 3	Skill formation
Fig 4	Architecture
Fig 5	Invariant results
Fig 6	Skill emergence
Fig 7	Transfer results
Fig 8	Capability growth
Paper Tables Master Plan
Table	PurposeTable 1	Experiment matrix
Table 2	Baseline comparison
Table 3	Ablation results
Table 4	Transfer metrics
Table 5	Capability metrics
Most Important Outcome of Phase 9E

We now have something very powerful:

Research Question
↓
Contributions
↓
Theory
↓
Architecture
↓
Experiments
↓
Results Sections
↓
Paper Structure


This means implementation is no longer exploratory.

Every line of future code should trace back to:

Figure
or
Table
or
Claim


in this blueprint.

Phase 9 Status

✅ 9A: Claims & Hypotheses

✅ 9B: Evidence Mapping

✅ 9C: Experiment Matrix

✅ 9D: Baselines & Ablations

✅ 9E: Paper Blueprint

The final Phase 9 step is 9F: Reviewer Attack Simulation, where we deliberately act like harsh ARC reviewers and try to reject the paper. That phase often reveals hidden weaknesses before any implementation begins.