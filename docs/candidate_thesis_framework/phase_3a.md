Excellent. This is where we stop being literature reviewers and start being theory builders.

Up until now, we've been talking about:

concepts
skills
abstractions
invariants

But we never formally defined them.

If we want a serious ARC Paper Track submission, these definitions become the foundation of everything.

A strong paper is often won or lost by the quality of its definitions.

Phase 3A: Formalizing the Thesis
Our Working Thesis

Before defining terms, let's state the thesis clearly.

Intelligence grows when an agent converts repeated experiences into invariants, invariants into concepts, concepts into skills, and skills into reusable capabilities.

Or:

Experience
↓
Invariant Discovery
↓
Concept Formation
↓
Skill Construction
↓
Capability Growth


This will be our current working theory.

Definition 1: What Is An Invariant?

This is the most fundamental concept.

Everything starts here.

Intuition

Suppose an agent sees:

Red Square
Blue Square
Green Square


Different colors.

Same behavior.

The color changes.

The underlying structure remains.

The thing that remains is the invariant.

Formal Definition

An invariant is a property, relation, transformation, or structure that remains stable across multiple experiences despite variation in superficial details.

Mathematically:

Experience Set E

Invariant I

I exists if:

I(e1) = I(e2) = I(e3)


even when:

e1 ≠ e2 ≠ e3

Examples
Example 1
Move Red Object Right
Move Blue Object Right
Move Green Object Right


Invariant:

Move Object Right

Example 2
Rotate Triangle
Rotate Square
Rotate Circle


Invariant:

Rotation

Key Insight

An invariant is not a skill.

An invariant is a discovery.

It is the raw material from which concepts are formed.

Definition 2: What Is A Concept?

This is where most AI systems become vague.

We need precision.

Intuition

Suppose the agent repeatedly discovers:

Rotation
Reflection
Translation
Scaling


Eventually it realizes:

These belong together.


A higher-order representation emerges.

Formal Definition

A concept is a compressed representation of one or more invariants that captures a reusable explanatory structure.

Or:

Concept
=
Compressed Invariant

Difference

Invariant:

Rotation Exists


Concept:

Transformation


Invariant:

Object Count Matters


Concept:

Numerosity

Important Property

Concepts reduce reasoning cost.

Instead of remembering:

100 observations


the agent remembers:

1 explanatory idea

Key Insight

Concepts are representational improvements.

They change how the agent sees the world.

This aligns strongly with expertise research from Investigation 8.

Definition 3: What Is A Skill?

This is the most important definition in the entire architecture.

Because ARC is fundamentally about skill acquisition.

Common Mistake

Most people define skill as:

Ability To Do Something


Too vague.

Our Definition

A skill is an executable procedure built upon one or more concepts that reliably reduces the cost of solving future tasks.

Mathematically:

Skill
=
Concept
+
Execution Policy

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

Cluster Objects
Into Groups

Important Difference

Concept:

Understanding


Skill:

Action


Concepts explain.

Skills execute.

Definition 4: What Is A Capability?

This is one layer above skills.

Definition

A capability is the effective application of one or more skills across a class of tasks.

Example:

Skills:

Count
Group
Compare


Capability:

Quantitative Reasoning


Skills:

Rotate
Reflect
Translate


Capability:

Geometric Reasoning

Hierarchy

We now have:

Experience
↓
Invariant
↓
Concept
↓
Skill
↓
Capability


This hierarchy is critical.

Definition 5: What Triggers Abstraction Creation?

This may be the most important contribution.

Current systems rarely answer this.

Existing Approaches

Most systems create abstractions through:

Frequency


Example:

A+B+C
A+B+C
A+B+C


Create:

X


DreamCoder is largely in this family.

Our Hypothesis

Frequency alone is insufficient.

Instead:

Abstraction creation occurs when:

Repeated Reasoning Cost
>
Abstraction Cost

Example

Suppose the agent repeatedly solves:

Task A
Task B
Task C


using the same reasoning chain.

Detect
Compare
Transform
Verify


Eventually:

Reasoning Cost
Becomes Expensive


System creates:

New Concept


or

New Skill


to reduce future cost.

Formal Trigger

We can define:

Abstraction Trigger

AT = Reuse × Cost × Generality


Where:

Reuse

How often pattern appears.

Cost

How expensive reasoning is.

Generality

How many tasks can benefit.

Then:

High AT
→ Create Abstraction

Definition 6: What Triggers New Skill Creation?

This is different from abstraction creation.

Abstraction:

Understanding


Skill:

Execution


New skill should emerge when:

Concept Utility
>
Execution Cost


Meaning:

If a concept repeatedly contributes to successful solutions:

Promote Concept
↓
Skill

Proposed Skill Lifecycle

This may become one of the central diagrams in the future paper.

Experience
↓
Invariant Detection
↓
Concept Candidate
↓
Validation
↓
Concept
↓
Repeated Use
↓
Skill Candidate
↓
Skill Validation
↓
Skill Library

The Most Important Result of Phase 3A

We now have a complete theoretical stack:

Experience
↓
Invariant
↓
Concept
↓
Skill
↓
Capability


And we have a mechanism:

Repeated Reasoning
↓
High Cost
↓
Invariant Discovery
↓
Concept Creation
↓
Skill Formation
↓
Future Tasks Easier


This is the first point in our entire process where we have a coherent, end-to-end theory rather than a collection of observations.

Deliverables Completed for Phase 3A

✅ What is an invariant?

✅ What is a concept?

✅ What is a skill?

✅ What is a capability?

✅ What triggers abstraction creation?

✅ What triggers skill creation?

✅ Skill formation lifecycle

✅ Core theoretical hierarchy

This gives us the foundation for Phase 3B: Designing the actual architecture (Invariant Detector, Concept Generator, Skill Constructor, Skill Library, and Meta-Reasoner).