Phase 13E: Capability Growth Experiments

This is the phase that validates Contribution 3 (CGM: Capability Growth Metrics).

If Phase 13B proved:

Invariants Exist


and Phase 13C proved:

Skills Emerge


and Phase 13D proved:

Transfer Exists


then Phase 13E must prove:

Capabilities Actually Grow


This is one of the most important distinctions in the entire ASFT framework.

Most systems can show:

Task Solved


Very few can show:

System Became More Capable

Phase 13E Objective

Validate the central CGM hypothesis:

Capability is not static. Through invariant discovery, skill formation, transfer, and composition, the system develops an increasingly powerful capability portfolio.

At the end of Phase 13E, you should have evidence for:

✅ Capability growth

✅ Capability coverage expansion

✅ Capability utility growth

✅ Composition-driven growth

✅ Intelligence growth

✅ Positive CGR

✅ Positive IGR

✅ Growth beyond simple skill accumulation

Phase 13E Structure
13E-1
Research Questions

13E-2
Capability Formation Experiments

13E-3
Capability Growth Experiments

13E-4
Capability Coverage Experiments

13E-5
Capability Utility Experiments

13E-6
Composition-Driven Growth Experiments

13E-7
Intelligence Growth Experiments

13E-8
Growth Robustness Experiments

13E-9
Baseline & Ablation Experiments

13E-10
Statistical Validation

13E-11
Capability Growth Evidence Package

13E-1 Research Questions

Everything in this phase should answer:

Q1

Do capabilities emerge?

Q2

Do capabilities grow?

Q3

Do capabilities become more transferable?

Q4

Does coverage increase?

Q5

Does composition accelerate growth?

Q6

Does capability growth predict future performance?

Q7

Can intelligence growth be measured?

Capability Measurement Framework

Before experiments:

Remember:

Skills
≠
Capabilities


Capability is:

Transfer

Coverage

Utility

Composition

Reuse


combined.

13E-2 Capability Formation Experiments

First validate capability emergence.

EXP-CAP-01
First Capability Emergence

Question:

Does a capability appear
once enough skills exist?


Procedure:

Allow:

ReflectionSkill

RotationSkill

CountSkill


to accumulate.

Expected:

GeometricCapability


or equivalent capability cluster emerges.

Metrics:

Capability Count

Capability Confidence

Capability Utility


Success:

At least one stable capability emerges.

EXP-CAP-02
Capability Membership Validation

Question:

Do capabilities contain meaningful skills?


Example:

ReflectionSkill

RotationSkill


inside:

Geometry Capability


Evaluate:

Membership Coherence


Expected:

Related skills cluster together.

13E-3 Capability Growth Experiments

The core experiment block.

EXP-CAP-03
Capability Trajectory

Question:

Does capability increase over time?


Track:

Round 1

Round 2

Round 3

Round 4


Measure:

CtC_t

Expected:

Monotonic growth.

Example:

1.05

1.17

1.21

1.23


like your current result.

EXP-CAP-04
Capability Growth Rate

Measure:

CGR=Ct−Ct−1ΔtCGR = \frac {C_t-C_{t-1}} {\Delta t}

Question:

Is growth positive?


Expected:

CGR>0CGR > 0

This directly validates CGM.

EXP-CAP-05
Growth Consistency

Question:

Is growth stable across seeds?


Run:

Seed 0-9


Measure:

Variance

Confidence Interval


Expected:

Positive mean CGR.

13E-4 Capability Coverage Experiments

Very important.

EXP-CAP-06
Coverage Expansion

Question:

How much of the task space
can the system support?


Measure:

CCov=SupportedFamiliesTotalFamiliesCCov = \frac {SupportedFamilies} {TotalFamilies}

Track over time.

Expected:

Coverage increases.

EXP-CAP-07
Cross-Family Capability

Question:

Can one capability support
multiple task families?


Example:

Geometry capability supports:

Reflection

Rotation

Reflection+Count


Expected:

Coverage grows.

EXP-CAP-08
Coverage Growth Rate

Measure:

CCG=CCovt−CCovt−1CCG = CCov_t - CCov_{t-1}

Expected:

Positive.

13E-5 Capability Utility Experiments

Capabilities must generate value.

EXP-CAP-09
Capability Utility Growth

Question:

Are capabilities becoming
more useful?


Track:

CUtCU_t

over time.

Expected:

Increasing utility.

EXP-CAP-10
Capability Utility vs Transfer

Question:

Do valuable capabilities
transfer more?


Measure:

CU

TS


Expected:

Positive correlation.

EXP-CAP-11
Capability Utility vs Reuse

Question:

Do useful capabilities
get reused?


Expected:

Positive correlation.

13E-6 Composition-Driven Growth Experiments

One of the most novel parts.

EXP-CAP-12
Composition Growth

Question:

Do compositions create
new capabilities?


Track:

Compositions

Capabilities


Expected:

Capability count grows after successful compositions.

EXP-CAP-13
Composition Utility

Question:

Do composed capabilities
outperform atomic capabilities?


Example:

Reflection+Count


vs

Reflection only


Expected:

Higher utility.

EXP-CAP-14
Capability Emergence

Question:

Can repeated compositions
create higher-order capabilities?


Expected:

Emergent capability clusters.

13E-7 Intelligence Growth Experiments

This validates the highest level.

EXP-CAP-15
Intelligence Growth

Measure:

IG=f(CGR,TS,SU,Coverage)IG = f( CGR, TS, SU, Coverage )

Question:

Does intelligence increase?


Expected:

Positive IG.

EXP-CAP-16
Intelligence Growth Rate

Measure:

IGR=IGt−IGt−1ΔtIGR = \frac {IG_t-IG_{t-1}} {\Delta t}

Expected:

Positive.

EXP-CAP-17
Intelligence Efficiency

Measure:

IE=IGExperiencesIE = \frac {IG} {Experiences}

Question:

How efficiently does
experience become intelligence?


Expected:

Positive trend.

EXP-CAP-18
Growth Prediction

One of the strongest experiments.

Question:

Does current capability
predict future performance?


Expected:

Strong predictive relationship.

13E-8 Growth Robustness Experiments

Attack the framework.

EXP-CAP-19
Capability Fragmentation Test

Question:

Do capabilities become
too fragmented?


Measure:

FR=Capabilities/SkillsFR = Capabilities/Skills

Expected:

Controlled growth.

EXP-CAP-20
Saturation Test

Question:

Does growth eventually slow?


Expected:

Natural saturation.

EXP-CAP-21
Regression Test

Question:

Can capability decrease?


Simulate:

Skill retirement

Transfer loss


Expected:

CGR detects decline.

EXP-CAP-22
Growth Illusion Test

Question:

Can metrics be fooled?


Add:

Many useless skills


Expected:

Capability score remains mostly unchanged.

13E-9 Baseline & Ablation Experiments

Mandatory.

Baseline B1

No Learning

Expected:

CGR ≈ 0
IG ≈ 0

Baseline B2

Skill Storage Only

Expected:

Some growth.

Limited capability formation.

Baseline B3

Random Skill Creation

Expected:

Weak utility.

Weak growth.

Baseline B4

DreamCoder-like

Expected:

Compression-driven growth.

Compare against:

ASFT

Ablation A1

No IDT

Expected:

Lower capability growth.

Ablation A2

No SCT

Expected:

Few reusable capabilities.

Ablation A3

No Skill Library

Expected:

Transfer collapse.

Ablation A4

No Composition

Expected:

Reduced capability emergence.

Ablation A5

No CGM

Expected:

Growth becomes unmeasurable.

13E-10 Statistical Validation

Run:

Seed 0-9


recommended.

Report:

Mean

Std Dev

95% CI


for:

CGR

IG

IGR

Coverage

Utility


Example:

Instead of:

CGR = 0.020


report:

CGR = 0.020 ± 0.004

Correlation Studies

Very important.

Study:

TS ↔ CGR

SU ↔ CGR

Coverage ↔ IG

Composition ↔ IG


Expected:

Positive relationships.

13E-11 Capability Growth Evidence Package

Paper-ready outputs.

Figure 1

Capability trajectory.

Figure 2

CGR across rounds.

Figure 3

Coverage growth.

Figure 4

Capability utility growth.

Figure 5

Composition-driven growth.

Figure 6

IG and IGR curves.

Table 1

Capability evolution.

Table 2

Coverage statistics.

Table 3

Utility statistics.

Table 4

Baseline comparison.

Table 5

Ablation comparison.

Table 6

Correlation results.

Success Criteria

Phase 13E succeeds if:

✅ Capabilities emerge

✅ Capability trajectory increases

✅ Positive CGR

✅ Positive coverage growth

✅ Positive utility growth

✅ Composition creates value

✅ Positive IG

✅ Positive IGR

✅ ASFT beats baselines

✅ Ablations reduce growth

✅ Results stable across seeds

Failure Criteria

Phase 13E fails if:

❌ Capability count increases but utility does not

❌ CGR ≈ 0

❌ Coverage stagnant

❌ Composition useless

❌ IG unrelated to capability

❌ Baselines perform equally well

❌ Growth metrics fail to predict future performance

Most Important Experiments

If I had to pick the 5 most important experiments for the paper:

EXP-CAP-03
Capability Trajectory

EXP-CAP-04
Capability Growth Rate

EXP-CAP-12
Composition Growth

EXP-CAP-15
Intelligence Growth

EXP-CAP-18
Growth Prediction


Together they validate the complete ASFT thesis:

Experience
↓
Invariant Discovery
↓
Skill Formation
↓
Transfer
↓
Capability Formation
↓
Capability Growth
↓
Intelligence Growth


which is the ultimate scientific claim of the entire framework.