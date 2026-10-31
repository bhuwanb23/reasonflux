Phase 13B: Invariant Discovery Experiments

This is the first formal experimental phase of ASFT.

For the first time, we are no longer asking:

Can the Invariant Detector run?


We are asking:

Does Invariant Discovery Theory (IDT) hold up scientifically?


This phase is entirely focused on validating Contribution 1.

Phase 13B Objective

Validate the central IDT claim:

Transferable knowledge emerges from stable reasoning invariants discovered across experiences.

By the end of Phase 13B, you should be able to answer:

Can ASFT discover invariants?

Are the discovered invariants meaningful?

Do they predict transfer?

Are they better than random patterns?

Do they survive variation?

Phase 13B Structure

I would split it into:

13B-1
Experimental Questions

13B-2
Discovery Experiments

13B-3
Quality Experiments

13B-4
Transfer Validation Experiments

13B-5
Robustness Experiments

13B-6
Baseline Comparisons

13B-7
Statistical Validation

13B-8
Evidence Package

13B-1 Experimental Questions

Everything in this phase should answer one of these questions.

Q1

Can ASFT discover recurring reasoning structures?

Q2

Can ASFT separate useful invariants from noise?

Q3

Do stronger invariants predict higher transfer?

Q4

Do discovered invariants generalize beyond their original tasks?

Q5

Are invariants robust to task variation?

These become the backbone of the entire IDT evaluation.

13B-2 Discovery Experiments

These experiments validate invariant discovery itself.

EXP-IDT-01
Reflection Discovery

Purpose:

Can ASFT discover reflection invariants?

Dataset:

Reflection Tasks


Expected Invariant:

ReflectionInvariant


Measure:

Frequency

Consistency

IS


Success:

Reflection invariant appears in top-ranked discoveries.

EXP-IDT-02
Rotation Discovery

Purpose:

Can ASFT discover rotation invariants?

Dataset:

Rotation Tasks


Expected:

RotationInvariant


Success:

Top invariant corresponds to rotation structure.

EXP-IDT-03
Counting Discovery

Purpose:

Can ASFT discover counting structures?

Expected:

CountInvariant


Success:

Counting-related trace structures emerge.

EXP-IDT-04
Grouping Discovery

Purpose:

Can ASFT discover grouping structures?

Expected:

GroupingInvariant


Success:

Grouping patterns consistently discovered.

Output of Discovery Block

You should produce:

Top 10 Invariants

Rank

Frequency

IS

Confidence

13B-3 Quality Experiments

Now we evaluate whether discovered invariants are actually good.

EXP-IDT-05
Invariant Precision

Question:

How many discovered invariants are meaningful?


Formula:

IP=ValidInvariantsDetectedInvariantsIP = \frac {ValidInvariants} {DetectedInvariants}

Procedure:

Manually inspect top invariants.

Example:

Detected:

ReflectionInvariant ✅

RotationInvariant ✅

VerifyOutputInvariant ❌


Target:

IP > 70%


for MVP.

EXP-IDT-06
Invariant Recall

Question:

How many expected invariants were found?


Formula:

IR=DiscoveredExpectedInvariantsExpectedInvariantsIR = \frac {DiscoveredExpectedInvariants} {ExpectedInvariants}

Example:

Expected:

Reflection

Rotation

Counting

Grouping


Discovered:

Reflection

Rotation

Counting


Recall:

75%

EXP-IDT-07
Invariant Confidence

Question:

How confident is the system?


Track:

Evidence

Frequency

Consistency

Transfer Evidence


Output:

Confidence distribution.

13B-4 Transfer Validation Experiments

This is the most important part of Phase 13B.

EXP-IDT-08
IS vs TS Correlation

Core hypothesis:

Strong Invariants
↓
Higher Transfer


Measure:

Correlation between:

Invariant Strength (IS)

Transfer Score (TS)


Expected:

Positive correlation.

This is probably the strongest validation of IDT.

EXP-IDT-09
Cross-Family Transfer

Example:

Learn:

Reflection


Test:

Reflection+Count

Reflection+Grouping


Question:

Does invariant remain useful?


Expected:

Positive transfer.

EXP-IDT-10
Transfer Utility

Measure:

TU=TransferSuccess×Coverage×ReasoningReductionTU = TransferSuccess \times Coverage \times ReasoningReduction

Question:

Which invariants generate
the most transfer value?


Output:

Transfer-ranked invariants.

13B-5 Robustness Experiments

Now we attack the invariants.

EXP-IDT-11
Variation Survival Test

Previously defined:

VST=SuccessfulVariationsTotalVariationsVST = \frac {SuccessfulVariations} {TotalVariations}

Change:

Color

Shape

Position

Object Count


Question:

Does invariant survive?


Expected:

Strong invariants survive.

EXP-IDT-12
Noise Resistance

Inject:

Trace Noise


Question:

Does discovery remain stable?


Expected:

Top invariants remain largely unchanged.

EXP-IDT-13
Sparse Data Experiment

Provide:

Few Traces


Question:

Does system avoid premature abstraction?


Expected:

Confidence drops.

Promotion delayed.

13B-6 Baseline Comparisons

Mandatory.

Baseline B1

Random Pattern Selection

Question:

Do discovered invariants
beat random patterns?


Expected:

Large difference.

Baseline B2

Frequency Only

Question:

Is transfer-awareness useful?


Compare:

Frequency Ranking

vs

Transfer-Aware Ranking


Expected:

ASFT ranking superior.

Baseline B3

No Transfer Validation

Question:

What happens if transfer is ignored?


Expected:

More spurious invariants.

13B-7 Statistical Validation

Every experiment should run:

Seed 0

Seed 1

Seed 2

Seed 3

Seed 4


minimum.

For each metric:

Report:

Mean

Std Dev

95% CI


Metrics requiring statistics:

IS

IP

IR

TS

TU

VST

Example Reporting Format

Instead of:

IS = 12.3


Report:

IS = 12.3 ± 1.1

13B-8 Evidence Package

At the end of Phase 13B, you should produce a dedicated IDT evidence package.

Figure 1

Top discovered invariants.

Figure 2

Invariant Strength distribution.

Figure 3

IS vs TS correlation.

Figure 4

Transfer utility by invariant.

Table 1

Top 20 invariants.

Table 2

Precision & Recall.

Table 3

Baseline comparison.

Table 4

Robustness results.

Success Criteria

Phase 13B succeeds if:

✅ Reflection invariant discovered

✅ Rotation invariant discovered

✅ Counting invariant discovered

✅ Grouping invariant discovered

✅ Precision exceeds target

✅ Recall exceeds target

✅ IS positively correlates with TS

✅ Strong invariants survive variation

✅ ASFT outperforms invariant baselines

✅ Results stable across seeds

Failure Criteria

Phase 13B fails if:

❌ Random patterns dominate

❌ Transfer unrelated to invariant strength

❌ Precision poor

❌ Invariants collapse under variation

❌ Frequency-only baseline performs equally well

❌ Results highly seed-dependent

What I Would Focus On First

Given your current status report, I would prioritize these experiments:

EXP-IDT-08
IS vs TS Correlation

EXP-IDT-09
Cross-Family Transfer

EXP-IDT-11
Variation Survival Test

EXP-IDT-12
Noise Resistance


because these are the experiments most likely to convince a reviewer that Invariant Discovery Theory is discovering genuine transferable structure rather than simply counting frequent patterns.

Deliverables of Phase 13B

✅ Discovery validation

✅ Precision validation

✅ Recall validation

✅ Transfer validation

✅ Robustness validation

✅ Baseline comparison

✅ Statistical validation

✅ IDT evidence package

✅ Figures and tables for the paper

✅ Direct evidence supporting Contribution 1 (IDT)

Once this phase is complete, you should be able to defend the statement:

ASFT discovers invariants that are not merely frequent, but are stable, transferable, and predictive of future reasoning efficiency.