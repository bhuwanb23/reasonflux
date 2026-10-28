Phase 10B: Invariant Detector Algorithms

This is the single highest-risk technical component in ASFT.

If Phase 10A was:

How do we capture reasoning?


then Phase 10B is:

How do we discover reusable structure from reasoning?


Everything depends on this.

No Invariants
↓
No Skill Formation
↓
No Transfer
↓
No Capability Growth

Phase 10B Goal

Answer:

Given hundreds of reasoning traces, how does ASFT discover invariants?

Not philosophically.

Algorithmically.

First Principle

Most people would start with:

Find Frequent Patterns


This is dangerous.

Why?

Because:

Frequent
≠
Important


Example:

VerifyOutput


may appear in every trace.

But:

VerifyOutput


is not the abstraction we care about.

What Is An Invariant?

For ASFT v0.1:

An invariant is:

A reasoning structure that repeatedly appears across successful traces and contributes to transfer.

Notice the last part:

Contributes To Transfer


This distinguishes invariants from noise.

Design Philosophy

We will build:

MVP Algorithm

Simple

Reliable

Explainable

Future Algorithm

More sophisticated

Concept-level

Graph-based

MVP Invariant Detector Pipeline
Trace Store
↓
Normalize Traces
↓
Cluster Similar Traces
↓
Mine Recurring Patterns
↓
Compute Invariant Strength
↓
Rank Invariants
↓
Output Candidates

Stage 1
Trace Normalization

Problem:

Different traces may use slightly different operations.

Example:

Trace A

DetectObject
FindSymmetry
ApplyReflection
Verify


Trace B

LocateObject
FindSymmetry
ApplyReflection
Verify


Raw comparison:

Different


Conceptually:

Same

Solution

Operation Mapping Table

LocateObject
→
DetectObject

FindMirrorAxis
→
FindSymmetry


Normalized Trace:

DetectObject
FindSymmetry
ApplyReflection
Verify

Output

Standardized traces.

Stage 2
Trace Clustering

Goal:

Group similar traces together.

Example

Cluster 1

Reflection Tasks


Cluster 2

Rotation Tasks


Cluster 3

Counting Tasks

MVP Similarity Metric

Simple overlap score.

Given:

Trace A

Detect
Symmetry
Reflect
Verify


Trace B

Detect
Symmetry
Reflect
Verify


Similarity:

4/4 = 1.0


Trace C

Detect
Rotate
Verify


Similarity:

2/4 = 0.5


Formula

Similarity
=
Shared Operations
/
Total Operations

Why Clustering?

Invariants should emerge inside clusters.

Not across unrelated traces.

Stage 3
Pattern Mining

Now we search for recurring structures.

Example Cluster

Trace 1

Detect
Symmetry
Reflect
Verify


Trace 2

Detect
Symmetry
Reflect
Verify


Trace 3

Detect
Symmetry
Reflect
Verify


Recurring Pattern

Symmetry
Reflect


Candidate Invariant

Reflection

MVP Algorithm

Frequent Subsequence Mining.

Example

Count:

[FindSymmetry, ApplyReflection]


across traces.

Frequency:

17


Store as candidate.

Stage 4
Invariant Strength Calculation

This is Contribution 1.

Previously we defined:

IS=Frequency×Consistency×GeneralityIS = Frequency \times Consistency \times Generality

Let's formalize.

Frequency

How often pattern appears.

Example:

17 traces


Frequency:

17

Consistency

How stable pattern is.

Example:

Appears in 17/18 reflection traces


Consistency:

0.94

Generality

How many task families use it.

Example:

Reflection only

0.3


Reflection + grouping

0.7


Reflection + grouping + composition

0.9

Final Score
IS=F×C×GIS = F \times C \times G

Example

17 × 0.94 × 0.7
=
11.18

Stage 5
Noise Filtering

Critical step.

Problem:

Many recurring patterns are useless.

Example:

VerifyOutput


appears everywhere.

Without filtering:

VerifyOutput
=
Strong Invariant


which is nonsense.

Filter Rule 1

Low Transfer Contribution

If pattern does not improve transfer:

Discard.

Filter Rule 2

Low Compression Value

If pattern saves no reasoning:

Discard.

Filter Rule 3

Trivial Operations

Operations like:

Verify


receive penalty.

Stage 6
Invariant Ranking

After filtering:

Sort by:

Invariant Strength


Output:

Reflection

Rotation

Counting


ordered by importance.

Invariant Object Structure

Output should be:

Invariant
{
    invariant_id

    pattern

    frequency

    consistency

    generality

    transfer_contribution

    strength
}


Example

{
    invariant_id:"INV_01",

    pattern:
    [
      FindSymmetry,
      ApplyReflection
    ],

    frequency:17,

    consistency:0.94,

    generality:0.72,

    transfer_contribution:0.66,

    strength:11.18
}

Why This Is Not Frequency Counting

A reviewer will ask:

Isn't this just frequent pattern mining?

Good question.

Frequency Mining:

Pattern appears often


ASFT:

Pattern appears often
+
Stable
+
Generalizable
+
Transfer Useful


That additional structure is important.

Future Version (v0.2)

Later we can move beyond sequence mining.

Graph Invariants

Instead of:

Operation Sequence


use:

Reasoning Graph


Example:

Object
↓
Symmetry
↓
Reflection

Concept Invariants

Eventually:

Reflection
Rotation
Translation


↓

Transformation


But NOT in MVP.

Computational Complexity

For MVP:

Keep it simple.

Trace Count

~100


Operations per Trace

5-20


Simple pattern mining is enough.

No need for:

Graph Neural Networks

Transformers

LLMs

Success Criteria

Invariant Detector succeeds if:

✅ Reflection invariants emerge

✅ Rotation invariants emerge

✅ Counting invariants emerge

✅ High IS correlates with transfer

✅ Useful invariants rank above trivial ones

Failure Criteria

Invariant Detector fails if:

❌ Trivial patterns dominate

❌ Transfer correlation is absent

❌ Random patterns rank highly

❌ Invariants are unstable

Deliverables of Phase 10B

✅ Invariant definition

✅ Invariant detection pipeline

✅ Trace normalization

✅ Trace clustering

✅ Pattern mining

✅ Invariant strength computation

✅ Noise filtering

✅ Invariant ranking

✅ Invariant data structure

✅ MVP algorithm

✅ Future roadmap

Most Important Outcome

The biggest decision we made is:

ASFT will not treat an invariant as "something frequent."

Instead:

ASFT treats an invariant as a recurring reasoning structure that is stable, reusable, and predictive of transfer.

That distinction is the foundation of Contribution 1 (Invariant Discovery Theory).

Next Phase

Phase 10C: Skill Creation Trigger Algorithms

This is where we implement the strongest contribution discovered throughout the entire research process:

When should a new skill be created?


We'll define:

skill candidate generation,
SCV computation,
promotion rules,
skill lifecycle,
skill retirement,
and how ASFT differs from simple memorization or skill storage.