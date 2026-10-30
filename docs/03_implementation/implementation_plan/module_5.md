Phase 10E: Evaluation Engine Design

This is the scientific heart of ASFT.

Without the Evaluation Engine:

Invariant Detector Works?
Unknown

Skill Creation Works?
Unknown

Transfer Happens?
Unknown

Capability Grows?
Unknown


The Evaluation Engine is what transforms ASFT from:

Architecture


into

Research System

Phase 10E Goal

Answer:

How do we measure whether ASFT is actually working?

More specifically:

Contribution 1
↓
How do we know invariants are useful?

Contribution 2
↓
How do we know skills are useful?

Contribution 3
↓
How do we know capability is growing?

Evaluation Architecture
              Task Results
                    │

                    ▼

          ┌─────────────────┐
          │ Evaluation Hub  │
          └────────┬────────┘

                   │

     ┌─────────────┼─────────────┐

     ▼             ▼             ▼

 Invariant      Skill       Capability
 Metrics        Metrics      Metrics

     ▼             ▼             ▼

     IS           SU           CGR
     AG           TS            IG

Evaluation Layer 1
Invariant Evaluation

Contribution:

IDT

Question

Did we discover a useful invariant?

Not:

Did we discover a pattern?


but:

Did we discover something reusable?

Metric 1
Invariant Strength (IS)

Previously defined:

IS=Frequency×Consistency×GeneralityIS = Frequency \times Consistency \times Generality
Frequency

How often invariant appears.

Consistency

How stable across traces.

Generality

How many task families benefit.

Example

Reflection Invariant

Frequency = 18

Consistency = 0.9

Generality = 0.8


Result:

IS = 12.96

Metric 2
Invariant Precision

Formula:

Useful Invariants
/
Detected Invariants


Purpose:

Detect noise.

Example

Detected:

Reflection

Rotation

VerifyOutput


Useful:

Reflection

Rotation


Precision:

2 / 3

Metric 3
Invariant Transfer Correlation

This is extremely important.

Question:

Do strong invariants
actually improve transfer?


Measure correlation:

IS
↔
TS


High correlation:

Invariant Theory Supported

Evaluation Layer 2
Skill Evaluation

Contribution:

SCT

Question

Did skill creation actually help?

Metric 4
Skill Utility (SU)
SU=AccuracyGain×CostReduction×TransferabilitySU = AccuracyGain \times CostReduction \times Transferability

Interpretation:

High SU:

Valuable Skill


Low SU:

Bad Skill

Example

ReflectionSkill

Accuracy Gain = 1.2

Cost Reduction = 0.8

Transferability = 0.7


Result:

SU = 0.672

Metric 5
Skill Reuse Count

Simple but critical.

Formula:

Number Of Times Skill Used


Question:

Was this skill actually useful?


Example

ReflectionSkill

Reuse = 21


Strong evidence.

Metric 6
Skill Creation Efficiency

Measures:

Useful Skills
/
Created Skills


Example

Created:

20 skills


Useful:

16 skills


Efficiency:

80%

Why Important?

Protects against:

Skill Explosion

Evaluation Layer 3
Transfer Evaluation

This is the core ARC metric.

Question

Did Task A make Task B easier?

Metric 7
Transfer Score (TS)
TS=PerformanceAfter−PerformanceBeforeTS = PerformanceAfter - PerformanceBefore

Example

Before:

40%


After:

65%


TS:

25%

Metric 8
Reasoning Cost Reduction
RCR=RCbefore−RCafterRCR = RC_{before} - RC_{after}

Example

Before:

12 steps


After:

5 steps


Result:

7


This is one of our strongest metrics.

Evaluation Layer 4
Capability Evaluation

Contribution:

CGM

Question

Is the agent actually improving?

Metric 9
Capability Growth Rate (CGR)
CGR=Capabilityt−Capabilityt−1ΔtCGR = \frac {Capability_t-Capability_{t-1}} {\Delta t}

Capability:

Skills

Transfer

Utility


combined.

Example

Task 5

Capability = 10


Task 10

Capability = 16


Positive growth.

Metric 10
Intelligence Growth (IG)

Flagship metric.

Formula:

IG=f(IS,SU,TS,CGR)IG = f( IS, SU, TS, CGR )

Interpretation:

How much smarter
did the system become?

Evaluation Layer 5
Baseline Comparison Engine

We must compare against:

Baseline A

No Learning

Baseline B

Skill Storage

Baseline C

DreamCoder-like

Baseline D

Random Skill Creation

Experimental

ASFT

Comparison Object
ComparisonResult
{
    system,

    IS,

    SU,

    TS,

    CGR,

    IG
}

Example
{
    system:"ASFT",

    IS:12.9,

    SU:0.81,

    TS:0.65,

    CGR:0.42,

    IG:0.73
}

Evaluation Reports

The engine should automatically generate:

Report A

Invariant Report

Contains:

Top Invariants

IS Scores

Precision

Report B

Skill Report

Contains:

Created Skills

Reuse

Utility

Report C

Transfer Report

Contains:

TS

RCR

Task Families

Report D

Capability Report

Contains:

CGR

IG

Growth Curves

MVP Dashboard Structure

Not a UI.

Just logical output.

ASFT Evaluation

Invariants
-----------
Reflection IS = 12.9
Rotation IS = 10.2

Skills
------
ReflectionSkill SU = 0.81

Transfer
--------
TS = 0.65

Capability
----------
CGR = 0.42

IG = 0.73

Success Criteria

ASFT succeeds if:

✅ High IS

✅ Positive SU

✅ Positive TS

✅ Positive CGR

✅ Positive IG

Failure Criteria

ASFT fails if:

❌ IS unrelated to TS

❌ Skills never reused

❌ TS ≈ 0

❌ CGR flat

❌ IG stagnant

Engineering Interfaces

Input:

Traces

Invariants

Skills

Task Results


Output:

EvaluationReports

MetricScores

GrowthCurves

Deliverables of Phase 10E

✅ Invariant Evaluation System

✅ Skill Evaluation System

✅ Transfer Evaluation System

✅ Capability Evaluation System

✅ Baseline Comparison Framework

✅ Evaluation Reports

✅ Success Criteria

✅ Failure Criteria

✅ Evaluation Interfaces

Most Important Outcome

The key engineering decision is:

ASFT will not be evaluated primarily by task accuracy.

Instead, it will be evaluated by whether solving tasks creates reusable capabilities that improve future performance.

That decision aligns directly with the ASFT thesis and with the ARC philosophy of skill-acquisition efficiency rather than isolated task success. On the Measure of Intelligence and the ARC framework emphasize learning efficiency, transfer, and generalization.

Next Phase

Phase 10F: Implementation Roadmap

This will be the final engineering planning phase before actual coding.

We'll define:

exact build order,
milestone-by-milestone development,
repository structure,
testing strategy,
what to implement first,
what to postpone,
and how to reach a runnable ASFT v0.1 prototype with minimal risk.