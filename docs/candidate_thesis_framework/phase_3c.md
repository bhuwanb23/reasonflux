Excellent.

This is where we move from:

Interesting Idea


to

Research Framework


A lot of papers stop at architecture diagrams.

The strongest papers usually introduce new measurable quantities.

If we can define proper metrics, then:

We can evaluate AAA.
We can compare against DreamCoder.
We can compare against ARC baselines.
We can create experiments.
We can make falsifiable claims.
Phase 3C: Mathematical Foundation of AAA
Philosophy

Current ARC systems optimize:

Accuracy


AAA optimizes:

Capability Growth


Therefore our mathematics must measure:

Reasoning
Abstraction
Skill Creation
Transfer
Capability Growth


not just task accuracy.

Layer 1: Reasoning Cost
Definition

Reasoning Cost measures how much cognitive effort is required to solve a task.

Intuition

Task A:

Recognize Reflection


Cost:

10 units


Task B:

Search 1000 possibilities


Cost:

100 units


A more intelligent system should reduce future cost.

Formal Definition

Let:

T = Task

R(T) = reasoning trace

Length(R) = number of reasoning operations

Depth(R) = reasoning depth

Search(R) = search effort


Then:

RC(T)=αL+βD+γSRC(T)=\alpha L+\beta D+\gamma S

where:

L = reasoning length
D = reasoning depth
S = search effort

Example

Task 1

5 operations
depth 2
search 10


Result:

RC = 5α + 2β +10γ

Why Important?

AAA claims:

Skills reduce RC


This becomes testable.

Layer 2: Invariant Strength

This metric is new.

Definition

How strongly does a pattern remain stable across experiences?

Suppose:

100 tasks


and:

Rotation


appears in:

80 tasks


Then invariant strength is high.

Formula
IS(I)=Frequency(I)×Consistency(I)×Generality(I)IS(I)= Frequency(I) \times Consistency(I) \times Generality(I)

where:

Frequency

How often observed.

Consistency

How stable.

Generality

Across how many task families.

Interpretation

High IS:

Good abstraction candidate


Low IS:

Noise

Layer 3: Abstraction Gain

This may become our most important metric.

Definition

How much reasoning reduction is achieved by introducing an abstraction?

Example

Without abstraction:

Rotate
Reflect
Scale
Translate


stored separately.

With abstraction:

Transformation


Reasoning becomes simpler.

Formula
AG(A)=RCbefore−RCafterAG(A) = RC_{before} - RC_{after}

Alternative normalized version:

AG(A)=RCbefore−RCafterRCbeforeAG(A) = \frac {RC_{before}-RC_{after}} {RC_{before}}

Range:

0 = no gain

1 = massive gain

Interpretation

Higher AG means:

Better abstraction

Layer 4: Concept Utility

Not all concepts are useful.

Example:

Concept:

Blue Triangle On Tuesdays


Worthless.

Concept:

Symmetry


Useful.

Formula
CU(C)=Reuse×Transfer×CompressionCU(C) = Reuse \times Transfer \times Compression

where:

Reuse

How often used.

Transfer

Across tasks.

Compression

Reasoning reduction.

Interpretation

High CU:

Promote concept


Low CU:

Discard concept

Layer 5: Skill Utility

One of the core metrics.

Definition

How valuable is a skill?

Skill should:

Reduce Cost
Increase Accuracy
Transfer Widely

Formula
SU(S)=AccuracyGain×CostReduction×TransferabilitySU(S) = AccuracyGain \times CostReduction \times Transferability

Expanded:

SU(S)=ΔAcc×AG×TSSU(S) = \Delta Acc \times AG \times TS

where:

TS = Transfer Score

Interpretation

High SU:

Keep Skill


Low SU:

Retire Skill

Layer 6: Transfer Score

This is directly aligned with ARC philosophy.

Definition

How much does solving Task A help Task B?

This is perhaps the most important metric in the entire framework.

Formula

Let:

B_before
=
Performance before skill

B_after
=
Performance after skill


Then:

TS=Bafter−BbeforeTS = B_{after} - B_{before}

Normalized:

TS=Bafter−BbeforeBbeforeTS = \frac {B_{after}-B_{before}} {B_{before}}
Example

Before Reflection Skill:

Reflection Tasks
40%


After Reflection Skill:

Reflection Tasks
70%


Transfer Score:

75%
improvement

Key Insight

ARC is fundamentally about:

Transfer


not memorization.

Layer 7: Skill Creation Value

This metric decides:

Should a new skill exist?

Formula
SCV=Reuse×AG×TS−CreationCostSCV = Reuse \times AG \times TS - CreationCost

Interpretation:

If:

SCV > 0


Create skill.

If:

SCV < 0


Do not create.

This gives a mathematically grounded trigger.

Layer 8: Capability Growth Rate

This may become the flagship metric.

Definition

How fast is the agent becoming better?

Current ARC systems optimize:

Task Performance


AAA optimizes:

Capability Growth

Formula
CGR=Capabilityt−Capabilityt−1ΔtCGR = \frac {Capability_t-Capability_{t-1}} {\Delta t}

where capability may be:

Skill Count
+
Transfer Score
+
Abstraction Gain


weighted together.

Expanded Capability Function
Capability=w1(Skills)+w2(Transfer)+w3(Abstractions)Capability = w_1(Skills) + w_2(Transfer) + w_3(Abstractions)
Layer 9: Intelligence Growth Function

This may become our paper's central equation.

Current AI:

Performance


AAA:

Growth


Define:

IG=f(AG,SU,TS,CGR)IG = f( AG, SU, TS, CGR )

Meaning:

Intelligence Growth depends on:

Abstraction Gain
Skill Utility
Transfer Score
Capability Growth Rate
Complete AAA Metric Hierarchy
Reasoning Cost (RC)
↓
Invariant Strength (IS)
↓
Abstraction Gain (AG)
↓
Concept Utility (CU)
↓
Skill Utility (SU)
↓
Transfer Score (TS)
↓
Skill Creation Value (SCV)
↓
Capability Growth Rate (CGR)
↓
Intelligence Growth (IG)

The Most Important Contribution

Most ARC systems measure:

Accuracy


AAA measures:

How much smarter
the agent became
after solving a task.


That is a fundamentally different objective.

Deliverables Completed in Phase 3C

✅ Reasoning Cost (RC)

✅ Invariant Strength (IS)

✅ Abstraction Gain (AG)

✅ Concept Utility (CU)

✅ Skill Utility (SU)

✅ Transfer Score (TS)

✅ Skill Creation Value (SCV)

✅ Capability Growth Rate (CGR)

✅ Intelligence Growth Function (IG)

✅ Complete mathematical hierarchy

At this point, the next logical step is Phase 3D: Mapping AAA to ARC-AGI-2 and ARC-AGI-3, where we define:

how AAA would operate on ARC tasks,
what experiments validate the theory,
what baselines to compare against,
and how to prove that "solving Task A makes Task B easier" quantitatively.