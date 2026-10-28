Phase 11E-2: Capability Growth Measurement

This is the centerpiece of Contribution 3 (CGM).

Everything before this point has been building toward one question:

How do we know the system is becoming more capable?

Not:

Did it solve Task 17?


Not:

Did accuracy improve?


But:

Did the system itself improve?


This is the exact place where ASFT attempts to align with the ARC philosophy:

Task Solving
≠
Intelligence

Capability Growth
≈
Intelligence Growth

Position in ASFT

We now have:

Experience
↓
Invariant
↓
Skill
↓
Capability


Now we add:

Capability
↓
Growth
↓
Intelligence Growth

Goal of Phase 11E-2

Formally define:

What grows?

How growth is measured?

What positive growth means?

What stagnation means?

What regression means?

What accelerated growth means?

How growth differs from performance?

Core Principle

The most important idea in this phase:

Performance is a snapshot.

Capability Growth is a trajectory.

Example:

System A

80% Accuracy

No Growth


System B

50% Accuracy

Rapid Capability Growth


ASFT cares much more about:

Growth Rate


than:

Current Score

What Actually Grows?

Before measuring growth we must define growth targets.

There are five growth layers.

Layer 1
Invariant Growth

Question:

How many useful invariants exist?


Example:

Initially:

Reflection


Later:

Reflection

Rotation

Counting

Grouping


Growth exists.

Layer 2
Skill Growth

Question:

How many useful skills exist?


Important:

Not raw count.

Example:

Bad Growth:

100 useless skills


Good Growth:

10 highly transferable skills

Layer 3
Transfer Growth

Question:

How much knowledge transfers?


Example:

Early:

Task A
helps
Task B


Later:

Task A
helps
B,C,D,E,F


Transfer network grows.

Layer 4
Capability Growth

Question:

How much of the task space can the system handle?


Example:

Initially:

Reflection Only


Later:

Reflection

Rotation

Counting

Grouping


Coverage expands.

Layer 5
Intelligence Growth

Highest level.

Question:

How quickly does solving one task improve future tasks?


This is the ultimate ASFT objective.

Growth Hierarchy

The full hierarchy becomes:

Invariant Growth
↓
Skill Growth
↓
Transfer Growth
↓
Capability Growth
↓
Intelligence Growth

Capability State

We need a measurable state.

At time tt:

Capability State contains:

Skills

Capabilities

Transfer

Utility

Coverage


Represented conceptually as:

CtC_t

Example:

Task 5

ReflectionSkill

Coverage = 1


Task 20

ReflectionSkill

RotationSkill

CountSkill

Coverage = 4


Clearly:

Capability Increased

Capability Growth Rate (CGR)

This becomes the primary metric.

Definition

Measures:

How much capability changes
over time.


Formula:

CGR=Ct−Ct−1ΔtCGR = \frac {C_t - C_{t-1}} {\Delta t}

Interpretation:

Positive:

Growth


Zero:

Stagnation


Negative:

Capability Loss

Expanded Capability Function

We need to define:

CtC_t

more carefully.

Capability should depend on:

Skill Utility

Transfer

Coverage

Composition


Conceptually:

Ct=w1SU+w2TS+w3CCov+w4CPC_t = w_1SU + w_2TS + w_3CCov + w_4CP

Where:

SU
=
Skill Utility

TS
=
Transfer Score

CCov
=
Capability Coverage

CP
=
Composition Potential

Why Weighted?

Because:

1 new skill


is not equivalent to:

1 new transfer pathway


Different contributions matter differently.

Capability Velocity

New concept.

Question:

How fast is capability growing?


This is:

First Derivative


of capability.

Equivalent to:

CGR

Capability Acceleration

Even more interesting.

Question:

Is growth speeding up?


Formula:

CA=CGRt−CGRt−1ΔtCA = \frac {CGR_t - CGR_{t-1}} {\Delta t}

Positive:

Learning Becoming More Efficient


Negative:

Learning Slowing Down


This may become an important paper metric.

Capability Saturation

Eventually:

Growth Slows


Question:

Why?


Possible reasons:

Task Space Covered

No New Invariants

Transfer Saturated


Need to measure.

Saturation Ratio

Conceptually:

CSR=NewCapabilityExistingCapabilityCSR = \frac {NewCapability} {ExistingCapability}

Low CSR:

Near Saturation

Transfer Growth

This deserves its own section.

Transfer is the bridge between:

Skill


and

Capability


Define:

TG=TSt−TSt−1TG = TS_t - TS_{t-1}

Positive TG:

Knowledge becoming more reusable.

Capability Coverage Growth

Coverage matters.

Question:

How much of the task space is covered?


Coverage:

CCov=SupportedFamiliesTotalFamiliesCCov = \frac {SupportedFamilies} {TotalFamilies}

Growth:

CCG=CCovt−CCovt−1CCG = CCov_t - CCov_{t-1}

Positive:

Capability Expanding

Composition Growth

Another unique metric.

Question:

Can skills combine in more ways?


Early:

Reflection


Later:

Reflection+Count

Reflection+Grouping

Reflection+Rotation


Composition network expands.

Define:

CompG=Compositionst−Compositionst−1CompG = Compositions_t - Compositions_{t-1}
Intelligence Growth (IG)

This is the flagship metric.

Definition:

How much smarter is the system becoming?

Not measured directly.

Derived from:

Capability Growth

Transfer Growth

Utility Growth

Coverage Growth


Conceptually:

IG=f(CGR,TG,UG,CCG)IG = f( CGR, TG, UG, CCG )

Where:

UG
=
Utility Growth

Growth States

The system should classify itself.

State 1

Emerging

Initial Learning

State 2

Growing

Positive CGR

State 3

Accelerating

Positive CA

State 4

Mature

Stable Growth

State 5

Saturated

Low CGR

State 6

Declining

Negative CGR

Growth Evidence Model

Every growth claim must have evidence.

Evidence Sources:

New Skills

Transfer Events

Coverage Expansion

Utility Improvement

Composition Growth


Without evidence:

No Growth Claim

Growth Dashboard

ASFT should maintain:

Current Capability

Growth Rate

Acceleration

Coverage

Transfer

Utility

Health


This becomes the central monitoring object.

Capability Growth Constraints

Valid growth must:

✅ Increase transfer

✅ Increase utility

✅ Increase coverage

✅ Improve future performance

✅ Be supported by evidence

Not merely:

More Skills

Failure Modes

Growth measurement can fail.

Failure 1

Skill Count Illusion

More skills.

No capability.

Failure 2

Transfer Illusion

Transfer appears positive.

Actually task similarity.

Failure 3

Coverage Inflation

Coverage increases on paper.

Not in practice.

Failure 4

Growth Without Utility

Capability expands.

Value does not.

Failure 5

Metric Gaming

System optimizes metrics.

Not intelligence.

Robustness Checks

Every growth metric should correlate with:

Transfer

Utility

Future Performance


Otherwise:

Metric Rejected

Success Criteria

Capability Growth Measurement succeeds if:

✅ Growth predicts future performance

✅ Growth predicts transfer

✅ Growth predicts utility

✅ Growth predicts coverage

✅ Growth reflects capability acquisition

✅ Growth remains interpretable

Failure Criteria

Capability Growth Measurement fails if:

❌ Growth unrelated to transfer

❌ Growth unrelated to utility

❌ More skills always imply growth

❌ Capability states become meaningless

❌ Growth cannot predict future behavior

Relationship to ASFT Thesis

This is where everything converges.

The complete chain now becomes:

Experience
↓
Invariant Discovery
↓
Skill Formation
↓
Skill Composition
↓
Capability Formation
↓
Capability Growth
↓
Intelligence Growth


This is the first complete measurable pathway from:

Task Experience


to

Intelligence Growth


inside ASFT.

Deliverables of Phase 11E-2

✅ Growth hierarchy

✅ Capability state model

✅ Capability Growth Rate (CGR)

✅ Capability function

✅ Capability velocity

✅ Capability acceleration

✅ Capability saturation

✅ Transfer growth

✅ Coverage growth

✅ Composition growth

✅ Intelligence Growth (IG)

✅ Growth states

✅ Evidence model

✅ Robustness checks

✅ Failure modes

✅ Success criteria

Most Important Outcome

The single most important decision of Phase 11E-2 is:

ASFT measures intelligence not by how many tasks have been solved, but by how rapidly the system's capabilities expand, transfer, compose, and improve future learning efficiency.

This gives us the mathematical foundation for Contribution 3 (CGM) and sets up the next phase:

Phase 11E-3: Intelligence Growth Model

where we formalize:

What is intelligence?

How does intelligence emerge from capabilities?

How do capability growth and intelligence growth differ?

Can intelligence growth be predicted?

What is the ASFT Intelligence Function?


This is likely the theoretical culmination of the entire framework.