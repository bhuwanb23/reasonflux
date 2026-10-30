Phase 11C-3: Invariant Ranking & Validation

This is arguably the most important specification in Contribution 1 (IDT).

Phase 11C-2 answered:

How do we generate invariant candidates?


Now we answer:

Which candidates deserve to survive?


Because after trace mining, the system will likely produce:

ReflectionCandidate

RotationCandidate

CountingCandidate

VerifyOutputCandidate

DetectObjectCandidate

RandomNoiseCandidate


Not all of them should become invariants.

This phase defines the "selection pressure" of ASFT.

Position in ASFT Pipeline
Reasoning Traces
↓
Trace Mining
↓
Candidate Invariants
↓
Ranking & Validation
↓
Validated Invariants
↓
Skill Creation Trigger


This phase acts as the gatekeeper.

Core Goal

Transform:

100 Candidate Invariants


into:

5-10 High-Value Invariants

Fundamental Principle

A candidate invariant is innocent until proven useful.

Meaning:

Pattern Found
≠
Invariant


It must earn promotion.

Validation Framework

Every candidate invariant must pass five tests.

Test 1
Frequency

Test 2
Consistency

Test 3
Generality

Test 4
Transfer Potential

Test 5
Reasoning Value

Validation Test 1
Frequency Validation
Question

How often does this structure occur?

Example

FindSymmetry
ApplyReflection


appears:

22 times


Candidate passes.

Another pattern:

BlueTriangleReflection


appears:

1 time


Candidate fails.

Principle

Rare patterns should not become invariants.

Output
Frequency Score

Validation Test 2
Consistency Validation
Question

Does the structure remain stable?

Example

Trace A:

FindSymmetry
ApplyReflection


Trace B:

FindSymmetry
ApplyReflection


Trace C:

FindSymmetry
ApplyReflection


Consistency:

High


Now consider:

Pattern appears
but changes every time


Consistency:

Low


Low consistency means:

Probably noise

Output
Consistency Score

Validation Test 3
Generality Validation

This is where ASFT starts becoming interesting.

Question

Can this invariant survive task variation?

Example

Appears in:

Reflection Task

Reflection + Counting

Reflection + Grouping

Reflection + Rotation


Generality:

High


Example

Appears only in:

Red Triangle Reflection


Generality:

Low

Principle

ASFT prefers:

Abstract Structures


over:

Task-Specific Structures

Output
Generality Score

Validation Test 4
Transfer Validation

This is the most important test.

Question:

Does this invariant help future tasks?


Without transfer:

Interesting Pattern


With transfer:

Reusable Knowledge

Example

Reflection invariant discovered.

Future task:

Reflect + Count


Performance improves.

Transfer exists.

Principle

Transfer is not an outcome.

Transfer is part of the invariant definition.

Output
Transfer Contribution Score

Validation Test 5
Reasoning Value Validation

This is unique to ASFT.

Question:

Does this invariant reduce reasoning cost?


Example

Without invariant:

12 reasoning steps


With invariant:

5 reasoning steps


Reduction:

7


Valuable.

Now consider:

VerifyOutput


appears frequently.

But reasoning reduction:

0


Not valuable.

Principle

Not every frequent structure deserves promotion.

Output
Reasoning Value Score

Invariant Ranking Formula

Now combine everything.

Candidate receives:

Frequency

Consistency

Generality

Transfer

Reasoning Value


Combined:

InvariantScore=F×C×G×T×RInvariantScore = F \times C \times G \times T \times R

Where:

F = Frequency

C = Consistency

G = Generality

T = Transfer

R = Reasoning Value

Interpretation

High score:

Promote


Low score:

Reject

Example Ranking

Candidate A

Reflection

F = High

C = High

G = High

T = High

R = High


Score:

Very High


Candidate B

VerifyOutput

F = High

C = High

G = High

T = Low

R = Low


Score:

Low


Exactly what we want.

Validation States

Every candidate moves through states.

State 1

Observed

Pattern Found

State 2

Candidate

Passed Frequency

State 3

Validated

Passed Consistency
+
Generality

State 4

Transfer Verified

Transfer Demonstrated

State 5

Promotable

Ready for SCT.

Lifecycle:

Observed
↓
Candidate
↓
Validated
↓
Transfer Verified
↓
Promotable

False Positive Handling

Critical.

Example

Suppose:

Blue Objects


appear often.

System might falsely detect:

BlueObjectInvariant


How do we stop this?

Rule:

Invariant must survive:

Color Changes

Shape Changes

Position Changes


If not:

Reject.

False Negative Handling

Also important.

Suppose:

Reflection


appears only 4 times.

Frequency may be low.

But:

Transfer Utility


is very high.

ASFT should retain it.

Principle:

Transfer
can rescue
rare but important invariants.

Invariant Confidence

Separate from ranking.

Confidence measures:

How sure are we?


Not:

How useful is it?


Example

Reflection

Confidence: 95%


Transfer:

70%


Both tracked independently.

Promotion Criteria

Invariant becomes SCT input if:

✅ Minimum Frequency

✅ Minimum Consistency

✅ Minimum Generality

✅ Positive Transfer

✅ Positive Reasoning Value

Only then:

Invariant
↓
Skill Candidate

Failure Modes

Invariant ranking fails if:

Failure 1

Frequency dominates.

Result:

VerifyOutput
wins.


Bad.

Failure 2

Transfer ignored.

Result:

Non-useful invariants promoted.

Failure 3

Task-specific patterns survive.

Result:

Poor generalization.

Failure 4

Over-aggressive filtering.

Result:

Useful invariants discarded.

Outputs of This Phase

Validated invariant should contain:

Identity

Pattern

Frequency

Consistency

Generality

Transfer Contribution

Reasoning Value

Confidence

Rank

Validation State


Example:

ReflectionInvariant

Frequency: 22

Consistency: 0.91

Generality: 0.78

Transfer: 0.72

Reasoning Value: 0.67

Confidence: 0.94

Rank: #1

State: Promotable

Deliverables of Phase 11C-3

✅ Validation framework

✅ Five validation tests

✅ Invariant ranking model

✅ Validation lifecycle

✅ False-positive handling

✅ False-negative handling

✅ Confidence model

✅ Promotion criteria

✅ Failure modes

✅ Final invariant specification

Most Important Outcome

The key architectural decision of Phase 11C-3 is:

ASFT does not promote invariants because they are frequent. It promotes invariants because they are frequent, stable, generalizable, transfer-relevant, and reasoning-efficient.

This is the final bridge between:

Trace Mining


and

Skill Creation Trigger Theory


and it ensures that only high-quality invariants enter the skill formation pipeline.

Recommended Next Subphase

Phase 11C-4: Transfer-Aware Invariant Discovery

This is where ASFT becomes genuinely differentiated.

We'll specify:

how transfer is measured during invariant discovery,
how Task A influences Task B,
transfer graphs,
transfer memory,
invariant-transfer coupling,
and why transfer is part of the invariant definition rather than a downstream metric.