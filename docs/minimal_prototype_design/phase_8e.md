Phase 8E: Success Metrics & MVP Definition

This phase is where we answer the most important engineering question:

What is the smallest thing we can build that, if successful, would validate ASFT?

A surprising number of research projects fail because the MVP is too large.

Our goal is:

Smallest Build
Maximum Evidence


Not:

Maximum Build
Small Evidence

Phase 8E Objective

At the end of Phase 8E, we should know:

✅ What exactly we are building

✅ What we are NOT building

✅ What counts as success

✅ What counts as failure

✅ What is required for the ARC Paper Track

✅ What can be postponed

MVP Definition
ASFT v0.1

The MVP is NOT:

AAA


The MVP is:

ASFT Core Validation System


Focused only on validating:

Invariant Discovery Theory (IDT)
Skill Creation Trigger (SCT)
Capability Growth Metrics (CGM)
MVP Research Question

The entire MVP should answer only one question:

Can a system automatically discover reusable reasoning patterns and convert them into skills that reduce future reasoning cost?

Everything else is secondary.

MVP Architecture

Only five components.

Task Set
↓
Reasoning Trace Logger
↓
Invariant Detector
↓
Skill Creation Trigger
↓
Skill Library


That's it.

Explicitly Excluded

Do NOT build these in v0.1:

❌ Full Concept Generator

❌ Meta-Reasoner

❌ Autonomous Goal Formation

❌ ARC-AGI-3 Agent

❌ Multi-Agent System

❌ World Model

❌ Recursive Self-Improvement

❌ LLM-Based Planning

❌ Dynamic Skill Evolution

MVP Deliverable 1
Invariant Discovery

Input:

Reasoning Traces


Output:

Detected Invariants


Example:

Trace 1:
Detect
Reflect
Verify

Trace 2:
Detect
Reflect
Verify

Trace 3:
Detect
Reflect
Verify


Detected:

Reflection Invariant

Success Metric 1
Invariant Precision

Formula:

Correct Invariants
/
Detected Invariants


Target:

>70%


for synthetic tasks.

MVP Deliverable 2
Skill Formation

Input:

Invariant


Output:

ReflectionSkill


created automatically.

Success Metric 2
Skill Utility

We already defined:

SU=AccuracyGain×CostReduction×TransferabilitySU = AccuracyGain \times CostReduction \times Transferability

Target:

SU > 0


for most created skills.

MVP Deliverable 3
Transfer Validation

This is the most important metric.

Question:

Does Task A help Task B?


Example

Learn:

Reflection


Then solve:

Reflection + Counting


Measure:

Transfer Score


Success:

TS>0TS > 0
MVP Deliverable 4
Reasoning Cost Reduction

Question:

Do skills save reasoning?


Before skill:

12 reasoning operations


After skill:

5 reasoning operations


Metric:

AG=RCbefore−RCafterAG = RC_{before} - RC_{after}

Success:

Positive AG.

MVP Deliverable 5
Capability Growth

Question:

Is the agent improving?


Track:

Skills
Transfer
Reasoning Cost


across tasks.

Metric:

CGR=Capabilityt−Capabilityt−1ΔtCGR = \frac {Capability_t-Capability_{t-1}} {\Delta t}

Success:

CGR > 0


throughout experiment.

MVP Success Levels

We should define tiers.

Tier 1
Proof of Concept

Can discover invariants.

Can create skills.

This already validates:

IDT
+
SCT

Tier 2
Transfer Demonstration

Skills help future tasks.

Validates:

Task A
↓
Task B Easier

Tier 3
Capability Growth

Agent measurably improves.

Validates:

CGM

Tier 4
ARC Validation

Works on selected ARC tasks.

This is ideal but not required for the MVP.

What Would Be Strong Enough For A Paper?

Honestly, for a Paper Track submission, you do NOT need:

Top ARC Score


You need evidence.

A strong result would be:

Invariant Discovery: Works

Skill Creation: Works

Transfer: Positive

Capability Growth: Positive


Even if ARC accuracy remains modest.

This aligns with the Paper Track's emphasis on theory, novelty, progress, and explanation, not just leaderboard position.

MVP Dataset Size

Keep it small.

Synthetic Layer

Reflection Tasks:

20


Rotation Tasks:

20


Counting Tasks:

20


Transfer Tasks:

20


Total:

~80 tasks


Enough to validate theory.

Not enough to become a research project by itself.

MVP Timeline of Learning (Conceptual)
Task 1
No Skill

Task 2
No Skill

Task 3
Invariant Appears

Task 4
Skill Created

Task 5
Skill Reused

Task 6
Transfer Observed


This is exactly the story we want the experiments to demonstrate.

Phase 8 Completion Status
8A

✅ Scope Definition

8B

✅ Data & Task Design

8C

✅ Architecture & Data Structures

8D

✅ Experimental Design

8E

✅ Success Metrics & MVP Definition

End Result of Phase 8

We now have a complete prototype design package:

Theory
✅

Architecture
✅

Metrics
✅

Experiments
✅

Success Criteria
✅

MVP Scope
✅


At this point, the next logical phase is Phase 9: Research Evaluation Plan & Paper Blueprint, where we convert all of this into:

Exact experimental protocol
Figures and diagrams needed
Paper structure
Claims-to-evidence mapping
What results would support or falsify each contribution

Before writing code, that phase will ensure every implementation task is tied directly to a research claim.