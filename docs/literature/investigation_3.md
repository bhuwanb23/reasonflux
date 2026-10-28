This is probably the most important investigation so far.

Why?

Because if we don't understand the entire Program Synthesis lineage, we risk proposing an idea that was already attempted 5 years ago under a different name.

Many "novel" AGI ideas turn out to be:

Program Synthesis + New Branding


So our goal is not to learn program synthesis.

Our goal is to understand:

Why ARC researchers keep returning to it.
Why it works.
Why it fails.
What assumptions it makes.
What gaps remain.

Only then can we find a truly novel direction.

Executive Summary

After reviewing ARC reports and leading ARC synthesis approaches, I think the biggest insight is:

Program synthesis is currently the closest thing ARC has to a "working theory of intelligence", but it is still fundamentally missing skill acquisition and abstraction formation.

In other words:

Program Synthesis
=
Good at discovering rules

Poor at discovering concepts


That distinction may become our future opportunity.

Part 1: What Is Program Synthesis?

Program synthesis is:

Examples
↓
Infer Program
↓
Execute Program
↓
Generate Output


Instead of:

Input
↓
Neural Network
↓
Output


Example:

Input:

ABCD


Output:

DCBA


Program synthesis says:

Rule = Reverse String


not

Predict D C B A directly

Why ARC Naturally Favors Program Synthesis

ARC tasks are usually:

Few Examples
+
Hidden Rule


This is almost exactly a program synthesis problem.

Human reasoning often looks like:

Observe
↓
Infer Rule
↓
Apply Rule


Program synthesis tries to replicate this.

Historical Evolution

Let's examine the lineage.

Generation 1
Brute Force Program Search

Early approach:

Generate Every Possible Program
↓
Test Program
↓
Find Match


Advantages:

Guaranteed search

Problems:

Search Space Explosion


If there are:

100 operators


and

20 steps


search becomes impossible.

This immediately became the central problem.

Generation 2
DSL-Based Search

Researchers introduced:

DSL
=
Domain Specific Language


Example ARC DSL:

Rotate
Mirror
Move
Fill
Count
Group
Crop


Instead of searching all programs:

Search only valid ARC programs.

This reduced complexity enormously.

Why DSL Became Dominant

Because ARC grids naturally contain:

Objects
Colors
Shapes
Transformations


A DSL captures these naturally.

Most successful symbolic ARC systems use some form of DSL.

Hidden Problem #1

DSLs Hard-Code Intelligence

Suppose we add:

Mirror()


to the DSL.

Who discovered mirroring?

The system?

No.

The researcher.

This creates a subtle issue:

Human Intelligence
→ DSL
→ Solver


instead of:

Solver
→ Discover Intelligence


This criticism appears repeatedly in ARC discussions.

Generation 3
Neural Guided Program Search

Researchers realized:

Pure Search
=
Too Slow


New approach:

Neural Network
↓
Suggest Good Programs
↓
Search Nearby


Architecture:

Task
↓
Encoder
↓
Program Prior
↓
Search
↓
Verification


This became one of the strongest approaches in ARC.

Why It Works

Humans don't search uniformly.

Humans guess intelligently.

Neural guidance approximates that.

Generation 4
Latent Program Search

A major paper direction.

Instead of searching:

Explicit Programs


search:

Latent Representations


of programs.

Idea:

Program
→ Embedding


Search happens in embedding space.

Benefits:

Smaller search space
Better scalability

Problems:

Less interpretable
Harder verification
Generation 5
Evolutionary Program Synthesis

Major 2025 trend.

Inspired by biology.

Workflow:

Generate Population
↓
Evaluate
↓
Keep Best
↓
Mutate
↓
Generate New Population


Instead of:

One Search Path


use:

Many Competing Programs


This worked surprisingly well.

Why Evolution Works

ARC tasks often have:

Many Partial Solutions


Evolution gradually improves them.

The ARC report specifically highlights evolutionary synthesis as a major refinement-loop paradigm.

Refinement Loops

By 2025 the key concept became:

Program
↓
Evaluate
↓
Improve
↓
Repeat


rather than:

Generate Once

Important Observation

Notice the progression:

2019-ish
Find Program

2024
Find Better Program

2025
Continuously Improve Program


Still missing:

Learn New Skills

The Deep Assumptions Behind Program Synthesis

This is where we need to think critically.

Program synthesis assumes:

Assumption 1

Every task has a discoverable rule.

Generally true for ARC.

Assumption 2

Rules can be represented symbolically.

Often true.

Assumption 3

Search can find the rule.

Sometimes true.

Assumption 4

Intelligence is program discovery.

This is the controversial one.

Why Program Synthesis Works So Well On ARC

Because ARC tasks are often:

Transformation Problems


Example:

Rotate Object
Mirror Shape
Move Pattern
Count Elements


These naturally map to programs.

Why Program Synthesis Still Falls Short Of AGI

This is the critical section.

Limitation #1

No Skill Creation

System discovers:

Program


but not:

New Cognitive Primitive


Example:

If DSL lacks:

Symmetry Detection


the solver usually cannot invent it.

Limitation #2

No Lifelong Learning

Task ends.

Knowledge disappears.

Humans do:

Experience
↓
Skill
↓
Future Use


Most ARC solvers do:

Experience
↓
Solution
↓
Forget

Limitation #3

No Abstraction Formation

Humans learn:

Rotation
Reflection
Translation


and realize:

These are geometric transformations


Program synthesis usually lacks this level.

Limitation #4

No Concept Compression

Humans compress:

100 examples
↓
1 concept


Program synthesis generally stores:

100 programs

The Most Important Insight

After studying this lineage, I think ARC research has largely solved:

How do we search?


Partially solved:

How do we refine?


Still unsolved:

How do we create new abstractions?

Research Gap Matrix
Capability	Program SynthesisRule Discovery	✅ Strong
Search	✅ Strong
Verification	✅ Strong
Interpretability	✅ Strong
Adaptation	✅ Moderate
Self-Improvement	✅ Emerging
Skill Creation	❌ Weak
Skill Memory	❌ Weak
Concept Formation	❌ Weak
Skill Composition	❌ Weak
Lifelong Learning	❌ Weak
The Most Valuable Takeaway For Our Research

Investigation 1 taught us:

ARC cares about skill acquisition.

Investigation 2 taught us:

Winners are increasingly using refinement loops.

Investigation 3 teaches us:

Program synthesis is excellent at finding rules, but weak at building reusable intelligence.

That gives us our first truly concrete research hypothesis:

Current ARC systems learn solutions.
Future ARC systems may need to learn skills.

More specifically:

Program Synthesis
+
Skill Formation
+
Skill Memory
+
Skill Composition


looks much more aligned with the long-term ARC vision than pure program synthesis alone.

Key Research Question Emerging

Not:

How do we synthesize better programs?

But:

How do we transform synthesized programs into reusable cognitive skills that improve future reasoning?

That is the strongest gap I see after completing Investigation 3.