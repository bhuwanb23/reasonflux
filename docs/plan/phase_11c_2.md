Phase 11C-2: Trace Mining Specification

This is where the ASFT pipeline truly begins to operate.

Phase 11C-1 defined:

What is an invariant?


Now we must answer:

How do we extract candidate invariants from thousands of reasoning traces?

This is not yet the ranking stage.

This is the knowledge extraction stage.

Position of Trace Mining in ASFT

Recall the full pipeline:

Task
↓
Reasoning Trace
↓
Trace Mining
↓
Invariant Candidates
↓
Invariant Validation
↓
Skill Creation Trigger
↓
Skill Library


Trace Mining sits exactly between:

Raw Experience


and

Abstraction Discovery

Goal of Trace Mining

Transform:

100 Traces


into:

10 Candidate Structures


Instead of:

100 Independent Experiences


the system should discover:

Shared Structure

Core Principle

Trace mining is NOT:

Pattern Counting


Trace mining IS:

Structure Discovery

What Enters Trace Mining?

Input:

Reasoning Traces


Example:

Trace 1

DetectObject
FindSymmetry
ApplyReflection
VerifyOutput


Trace 2

DetectObject
FindSymmetry
ApplyReflection
VerifyOutput


Trace 3

DetectObject
FindSymmetry
ApplyReflection
VerifyOutput


Trace 4

DetectObject
FindRotation
ApplyRotation
VerifyOutput


The miner's job is to identify:

Reflection Structure

Rotation Structure

Trace Mining Stages

I recommend a 6-stage pipeline.

Stage 1
Trace Collection

Stage 2
Trace Normalization

Stage 3
Trace Segmentation

Stage 4
Pattern Extraction

Stage 5
Pattern Aggregation

Stage 6
Candidate Generation

Stage 1: Trace Collection

Purpose:

Gather all reasoning experiences.

Input:

Reflection Tasks

Rotation Tasks

Counting Tasks

Transfer Tasks


Output:

Trace Repository


Important:

We mine traces.

Not task outputs.

Not task labels.

Stage 2: Trace Normalization

This is critical.

Without normalization:

Same Idea
=
Different Trace


Example

Trace A

LocateObject
FindMirrorAxis
Reflect
Verify


Trace B

DetectObject
FindSymmetry
ApplyReflection
VerifyOutput


Conceptually:

Same


Raw form:

Different


Normalization transforms both into:

DetectObject
FindSymmetry
ApplyReflection
Verify


Goal:

Reduce representation noise.

Stage 3: Trace Segmentation

One of the most important design decisions.

Question:

Should ASFT mine:

Entire Traces


or

Trace Fragments


?

Answer:

Trace Fragments.

Reason:

Skills emerge from substructures.

Example

Trace:

DetectObject
FindSymmetry
ApplyReflection
Verify


Segments:

DetectObject

FindSymmetry

ApplyReflection

Verify

FindSymmetry→ApplyReflection

DetectObject→FindSymmetry

ApplyReflection→Verify


This dramatically increases discovery power.

Stage 4: Pattern Extraction

Purpose:

Identify recurring fragments.

Example

Across traces:

FindSymmetry
ApplyReflection


appears repeatedly.

Extract:

Pattern P1


Another example:

FindRotation
ApplyRotation


Extract:

Pattern P2


Important:

Patterns are not invariants yet.

At this stage:

Pattern
≠
Invariant

Stage 5: Pattern Aggregation

Now we combine similar patterns.

Example

Pattern A

FindSymmetry
ApplyReflection


Pattern B

DetectObject
FindSymmetry
ApplyReflection


Pattern C

FindSymmetry
ApplyReflection
Verify


All may correspond to:

Reflection Structure


Aggregation groups them.

Purpose:

Move from:

Instances


to

Structures

Stage 6: Candidate Generation

Output:

Invariant Candidates


Example

Candidate 1

Reflection


Candidate 2

Rotation


Candidate 3

Counting


These now move into:

Invariant Validation


(Phase 11C-3)

Mining Units

This is an important specification.

What exactly can be mined?

Unit Type 1

Operation

Example:

FindSymmetry


Low-level.

Unit Type 2

Operation Pair

Example:

FindSymmetry
→
ApplyReflection


Most useful for MVP.

Unit Type 3

Procedure

Example:

DetectObject
↓
FindSymmetry
↓
ApplyReflection


Higher-value structure.

Unit Type 4

Trace Skeleton

Example:

Detect
↓
Transform
↓
Verify


Future version.

Not MVP.

Mining Constraints

To qualify for candidate generation:

A pattern must satisfy:

Constraint 1

Minimum Frequency

Example:

Appears ≥ 3 times

Constraint 2

Cross-Trace Occurrence

Cannot occur only in one trace.

Constraint 3

Successful Trace Bias

Prioritize successful traces.

Reason:

We want:

Reusable Reasoning


not:

Reusable Failure

Failure Trace Handling

Very important.

Question:

Should failed traces be discarded?

Answer:

No.

Failed traces provide:

Negative Evidence


Store:

Success Patterns

Failure Patterns


separately.

This becomes valuable for future meta-reasoning.

Trace Mining Outputs

The miner should produce:

Output A

Pattern Inventory

Example:

P1 Reflection

P2 Rotation

P3 Counting

Output B

Pattern Statistics

Example:

Frequency

Coverage

Task Families

Output C

Candidate Invariants

These move to Phase 11C-3.

What Trace Mining Must NOT Do

This is important.

Trace Mining should NOT:

❌ Create skills

❌ Rank transfer utility

❌ Decide promotion

❌ Manage memory

❌ Compute CGR

Those belong elsewhere.

Trace Mining only discovers structure.

Success Criteria

Trace Mining succeeds if:

✅ Reflection patterns emerge

✅ Rotation patterns emerge

✅ Counting patterns emerge

✅ Similar traces cluster naturally

✅ Candidate invariants become discoverable

Failure Criteria

Trace Mining fails if:

❌ Noise dominates

❌ Every pattern looks important

❌ Reflection and rotation become indistinguishable

❌ No reusable structures emerge

Relationship to Contribution 1

Contribution 1 (IDT) depends on:

Trace Mining
↓
Invariant Discovery


Without effective trace mining:

No Invariant Discovery Theory


can be validated.

Deliverables of Phase 11C-2

✅ Trace mining objective

✅ Mining pipeline

✅ Trace segmentation strategy

✅ Pattern extraction specification

✅ Pattern aggregation specification

✅ Candidate generation rules

✅ Mining constraints

✅ Failure-trace policy

✅ Outputs definition

✅ Success/failure criteria

Most Important Outcome

The key design decision of Phase 11C-2 is:

ASFT does not mine tasks, outputs, or solutions. It mines reasoning structures from traces and converts them into invariant candidates.

This is the first place where ASFT fundamentally diverges from many traditional task-solving systems and starts treating reasoning itself as the primary learning signal.

Next Recommended Subphase

Phase 11C-3: Invariant Ranking & Validation

This is where we answer:

Many candidate invariants exist.

Which ones are actually important?


and formally define:

invariant validation,
invariant confidence,
invariant strength computation,
promotion thresholds,
ranking policies,
false-positive handling,
and the bridge from candidate invariants to Skill Creation Trigger Theory.