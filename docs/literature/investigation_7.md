This is the investigation that may actually determine whether we discover a genuinely new ARC research direction.

Everything we've done so far has been converging toward one uncomfortable realization:

Nearly every ARC architecture explains how to solve tasks.

Very few explain how new capabilities come into existence.

That sounds philosophical, but it's actually an engineering problem.

Investigation 7: Skill Formation & Abstraction Formation

Let's forget ARC for a moment.

Let's ask the deepest question:

Where do new skills come from?


Not:

How do we use skills?


Not:

How do we store skills?


But:

How are skills born?

First Discovery

Most AI Research Doesn't Model Skill Formation

Most systems assume skills already exist.

Examples:

Program Synthesis

Assumes DSL primitives exist.

Rotate
Mirror
Count
Move


already available.

Neuro-Symbolic Systems

Assume:

Objects
Relations
Transformations


already available.

LLMs

Assume:

Knowledge
Patterns
Capabilities


already encoded.

Nobody asks:

Where did Rotate come from?

Q1: What Exactly Is A Skill?

This is surprisingly difficult.

Let's examine possible definitions.

Definition 1

A skill is a procedure.

Example:

Sort Numbers


Problem:

Too narrow.

Definition 2

A skill is a reusable solution.

Better.

Still incomplete.

Definition 3

A skill is a reusable transformation that reduces future reasoning cost.

This is the best definition I've found.

Example:

Before learning multiplication:

4+4+4+4+4


After learning multiplication:

5×4


The skill compresses reasoning.

First Important Insight

A skill is not knowledge.

A skill is:

Reasoning Compression


This aligns surprisingly well with ARC philosophy.

Because intelligence is efficient skill acquisition, not knowledge acquisition.

Q2: What Exactly Is An Abstraction?

Again, let's think carefully.

Raw experiences:

Red Square
Blue Square
Green Square


Abstraction:

Object


Raw experiences:

Rotate Triangle
Rotate Circle
Rotate Square


Abstraction:

Rotation


Observation:

An abstraction removes unnecessary detail.

Possible definition:

An abstraction is a compressed representation that preserves behavior while discarding irrelevant information.

This is extremely important.

Because skills seem to be built from abstractions.

Relationship Between Skills And Abstractions

I think we can formulate:

Experiences
↓
Abstractions
↓
Skills
↓
Capabilities


Example:

Experiences:

Mirror Shape A
Mirror Shape B
Mirror Shape C


Abstraction:

Reflection


Skill:

Apply Reflection


Capability:

Solve Reflection Problems

Q3: How Does An Abstraction Emerge From Experience?

This is where things become interesting.

Let's derive it.

Suppose agent solves:

Task 1
Move Red Object Right

Task 2
Move Blue Object Right

Task 3
Move Green Object Right


Human realization:

Color Doesn't Matter


New abstraction:

Move Object Right


This process appears to involve:

Step 1

Pattern Collection

Step 2

Invariant Detection

Find what stays constant.

Step 3

Variable Elimination

Remove irrelevant details.

Step 4

Abstraction Formation

Create reusable concept.

Massive Insight

Abstractions seem to emerge from:

Finding Invariants Across Experiences


This may become central to our future architecture.

Q4: Can New Primitives Be Invented Automatically?

This is one of the most important questions.

Current ARC systems mostly have:

Fixed Primitive Set


Examples:

Rotate
Move
Count
Reflect


But humans do something different.

Humans invent new concepts.

Example:

Initially:

Rotate
Scale
Translate
Reflect


separate concepts.

Later:

Geometric Transformation


becomes a new primitive.

This is abstraction-driven primitive invention.

Important Observation

DreamCoder partially moves in this direction.

It compresses frequently used programs into new library components.

However:

DreamCoder's primitives emerge from program compression.

Not necessarily from conceptual understanding.

This distinction is crucial.

Compression-Based Primitive Creation

Suppose we repeatedly observe:

A+B+C


System creates:

X = A+B+C


Future reasoning:

X


instead of:

A+B+C


This is computationally efficient.

But may not produce genuine abstractions.

Concept-Based Primitive Creation

Alternative:

System discovers:

A
B
C


all express:

Symmetry


Creates:

Symmetry


as a new primitive.

This is deeper.

Q5: What Creates Skill Boundaries?

One of the least discussed questions.

How do humans know:

This is one skill.


instead of:

Many unrelated actions.


Example:

Driving.

Contains:

Steering
Braking
Acceleration
Observation
Prediction


Yet we treat:

Driving


as one skill.

Hypothesis:

Skill boundaries emerge when a group of operations repeatedly co-occur toward a common goal.

Repeated cluster:

Observe
Predict
Steer


becomes:

Driving Skill


This suggests skills may emerge as:

Frequently Reused Reasoning Modules

Q6: How Does A System Know It Needs A New Skill?

This may be the most important question of all.

Current systems often do:

Failure
↓
More Search


Humans often do:

Failure
↓
Need New Concept


Huge difference.

Example

Imagine solving:

Task 1
Task 2
Task 3


using extensive search.

Eventually agent notices:

Same reasoning pattern repeatedly appears.


At that moment:

Search Cost > Skill Cost


New skill should be created.

Proposed Principle

A new skill should be invented when:

Cost of repeated reasoning
>
Cost of abstraction


This is one of the strongest hypotheses we've found so far.

Emerging Theory of Skill Formation

Combining everything:

Stage 1

Experience

Task
Task
Task

Stage 2

Pattern Discovery

Common Structure

Stage 3

Invariant Detection

What Never Changes?

Stage 4

Abstraction Creation

New Concept

Stage 5

Skill Formation

Executable Concept

Stage 6

Skill Library

Reusable Capability

The Most Important Gap We Found

After all seven investigations, I think the biggest gap in ARC research is not:

Search


Not:

Program Synthesis


Not:

Neuro-Symbolic Reasoning


The gap is:

How can a system autonomously detect recurring reasoning structures, convert them into abstractions, and promote those abstractions into reusable skills?

New Research Hypothesis (Version 1)

This is the first hypothesis I'd actually consider paper-worthy:

Intelligence grows when an agent continuously converts expensive reasoning traces into reusable abstractions, and reusable abstractions into executable skills.

In architecture form:

Task
↓
Reasoning Trace
↓
Invariant Detection
↓
Abstraction Generator
↓
Primitive Inventor
↓
Skill Library
↓
Future Tasks


Notice something important:

None of the major ARC paradigms we've studied explicitly center the Invariant Detection → Abstraction Generator → Primitive Inventor pipeline.

They focus on:

search,
programs,
refinement,
neuro-symbolic reasoning,
memory,

but not on the mechanism by which entirely new abstractions are born.

And that is the strongest lead we've uncovered so far.