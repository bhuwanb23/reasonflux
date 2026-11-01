Phase 14F: Baselines & Ablations Critical Results Analysis
Purpose

Phase 13F asked:

How does ASFT compare to alternatives?

What happens when components are removed?


Phase 14F asks:

What do the baseline and ablation results actually mean?

What is the real causal story?

Which components matter?

Which components do not appear to matter?

What alternative explanations survive?


This is arguably the most important analysis phase because it determines whether ASFT's observed behavior is actually caused by:

IDT

SCT

Transfer

CGM


or whether simpler explanations are sufficient.

14F-1 Original Purpose of Baselines

The baseline suite was intended to reject four competing explanations.

Baseline	Alternative ExplanationB1 No Learning	Learning is unnecessary
B2 Memory Only	Memory explains everything
B3 Random Skills	Any skill creation works
B4 Compression Proxy	Compression explains everything
14F-2 Original Purpose of Ablations

The ablations were intended to test:

Remove IDT
↓
Performance Drops

Remove SCT
↓
Performance Drops

Remove Transfer
↓
Performance Drops

Remove CGM
↓
Growth Interpretation Breaks

14F-3 High-Level Evidence Summary

Across 13B-13G:

Strong Results

✅ ASFT often beats No Learning

✅ ASFT often beats Random baselines

✅ Some growth metrics disappear when components are removed

✅ Some transfer metrics decline when invariants are removed

Weak Results

⚠ Component importance varies by phase

⚠ Results depend heavily on generator

⚠ Several effects disappear under alternate metrics

Failed Expectations

❌ ASFT does not consistently beat all baselines

❌ Memory-only frequently performs better

❌ No-SCV often ties SCT

❌ Random-SCV often ties SCT

❌ No-SCT often produces little degradation

14F-4 Analysis of Baseline B1 (No Learning)
Original Expectation
ASFT >> No Learning

Actual Results

Mixed.

Positive

13D:

ASFT > B1


on transfer utility.

Negative

13E:

ASFT fails B1


on task utility.

13F

Again:

ASFT utility < B1

Interpretation

This is one of the most surprising results.

The original theory assumed:

Learning
↓
Improves Performance


Observed:

Learning
↓
Improves Some Metrics
↓
Does Not Always Improve Utility

Verdict

Status:

🟡 Mixed

14F-5 Analysis of Baseline B2 (Memory Only)

This is the most important baseline.

Original Expectation
ASFT > Memory

Actual Results

Phase 13C:

Memory Only = 1.325

SCT = 0.345


Large advantage.

Interpretation

The strongest alternative explanation surviving Phase 13 is:

Memory explains much of the observed behavior.


Current evidence suggests:

Exact retrieval


may outperform:

Skill abstraction


inside the synthetic environment.

This is the single largest challenge to SCT.

Verdict

Status:

❌ Alternative Explanation Survives

14F-6 Analysis of Baseline B3 (Random Skills)
Original Expectation
ASFT >> Random

Actual Results

Mixed.

Phase 13B

ASFT > Random

Phase 13D

ASFT > Random

Phase 13C

Random Create

=

SCT

because:

All candidates promoted.

Interpretation

The random baseline only becomes weak when:

Selection pressure exists.


When:

Everything gets promoted


random and SCT collapse together.

Verdict

Status:

🟡 Partially Supports SCT

14F-7 Analysis of Baseline B4 (Compression Proxy)
Original Expectation
ASFT > Compression

Actual Results

13D:

ASFT < B4


Mandatory criterion failed.

Interpretation

This is a serious result.

The original theory proposed:

Transfer-Aware Discovery


as a novel advantage.

Current evidence shows:

Compression-based reuse


remains highly competitive.

The novelty claim is therefore weakened.

Verdict

Status:

❌ Not Supported

14F-8 What Do The Baselines Tell Us?

After all evidence:

Rejected Explanations
Randomness

Mostly rejected.

Reason:

ASFT often beats random systems.

Surviving Explanations
Memory

Strongly survives.

Compression

Partially survives.

Simple Retrieval

Strongly survives.

This is extremely important.

14F-9 Ablation Analysis: IDT
No IDT

Original expectation:

Large degradation.


Observed:

Some positive degradation.

But not universally.

Interpretation

IDT contributes.

But:

Not always critically.

Verdict

Status:

🟡 Partial Support

14F-10 Ablation Analysis: SCT
No SCT

Original expectation:

Major collapse.


Observed:

Often:

No measurable change.


Reason:

All candidates selected anyway.


Meaning:

SCT never exercised discretion.

Interpretation

Current experiments do not strongly validate SCT's necessity.

Verdict

Status:

❌ Not Established

14F-11 Ablation Analysis: SCV

This is especially important.

No SCV

Observed:

Tie

Random SCV

Observed:

Tie

Interpretation

The strongest SCT-specific mechanism:

SCV


currently contributes little measurable value.

This is one of the strongest negative findings in the project.

Verdict

Status:

❌ Unsupported

14F-12 Ablation Analysis: Lifecycle

Observed:

Lifecycle Off

≈

Lifecycle On


Interpretation:

Lifecycle machinery exists.

Its necessity remains unproven.

Verdict:

❌ Not Established

14F-13 Ablation Analysis: Composition

Results differ by phase.

Phase 13C

Positive.

Phase 13D

Unavailable.

Phase 13E

Negative.

Phase 13F

Positive in composition stream.

Interpretation:

Evidence inconsistent.

Verdict:

🟡 Mixed

14F-14 Why So Many Ablations Failed?

This is the most important question.

Evidence suggests:

Synthetic environment


contains:

Too few difficult decisions.


Examples:

IDT

Same ranking chosen.

SCT

All candidates selected.

SCV

Never rejects candidates.

Lifecycle

Never faces meaningful pressure.

Therefore:

Component Removal


often changes little.

This is a benchmark property.

Not necessarily a theory property.

14F-15 Threats to Validity
Threat BLA-01

Memory-friendly task distribution.

Severity:

High

Threat BLA-02

All-positive candidate population.

Severity:

High

Threat BLA-03

Low selection pressure.

Severity:

High

Threat BLA-04

Generator-specific effects.

Severity:

High

Threat BLA-05

Weak ARC coverage.

Severity:

High

14F-16 What Survives?
Survives

✅ ASFT is not random

✅ Invariants contribute some value

✅ Synthetic transfer exists

✅ Growth metrics are sensitive to some removals

Does Not Survive

❌ SCT superiority

❌ SCV necessity

❌ Lifecycle necessity

❌ Universal baseline superiority

❌ Memory alternative explanation

❌ Compression alternative explanation

14F-17 Revised Baseline Interpretation

Original intended conclusion:

ASFT outperforms memory, random creation, compression, and no-learning systems.

Evidence-supported conclusion:

ASFT frequently outperforms no-learning and random alternatives, but memory-based retrieval and compression-oriented approaches remain strong competing explanations. Current evidence does not establish universal superiority of ASFT components.

14F-18 Final Baseline & Ablation Scorecard
Question	StatusBetter than No Learning?	🟡 Mixed
Better than Random?	✅ Mostly Supported
Better than Memory?	❌ Not Supported
Better than Compression?	❌ Not Supported
IDT Necessary?	🟡 Partial
SCT Necessary?	❌ Not Established
SCV Necessary?	❌ Not Supported
Lifecycle Necessary?	❌ Not Supported
Composition Valuable?	🟡 Mixed
Alternative Explanations Eliminated?	❌ No
14F Conclusion
Scientific Verdict
Baselines reveal that
memory and compression remain
the strongest competing explanations.

Ablations reveal that several
core ASFT mechanisms do not yet
demonstrate clear causal necessity.

Most Important Finding

The single most important result of Phase 14F is:

The current evidence supports ASFT as a functioning synthetic learning framework, but does not yet support the claim that its key mechanisms are necessary or superior to simpler retrieval- and compression-based alternatives.

Deliverables of Phase 14F

✅ Baseline Interpretation Report

✅ Alternative-Explanation Analysis

✅ Ablation Interpretation Report

✅ Component-Importance Assessment

✅ Threats-to-Validity Assessment

✅ Revised Baseline Claims

✅ Final Baseline & Ablation Scorecard

Exit Decision
Phase 14F
✅ COMPLETE


The strongest defensible conclusion is:

ASFT demonstrates non-random synthetic learning behavior, but the current evidence does not eliminate memory, retrieval, or compression as competing explanations, nor does it establish the causal necessity of several core ASFT mechanisms.