Phase 14G: ARC Failure Analysis
Purpose

This is arguably the most important analysis phase in the entire project.

Why?

Because until Phase 13G, every major weakness could be explained away as:

Synthetic benchmark issue

Small candidate population

Weak baseline separation

Generator bias


ARC is different.

ARC was the first attempt to answer:

Does ASFT survive outside its synthetic ecosystem?

The answer from Phase 13G was:

No, not in its current form.


The purpose of Phase 14G is not to explain away the failure.

The purpose is to determine:

Why did ARC fail?

What failed first?

Was it a theory failure?

A representation failure?

A DSL failure?

A benchmark mismatch?

An implementation limitation?

14G-1 ARC Outcome Summary

From the consolidated evidence:

Discovery split:
600 tasks

Transfer split:
200 tasks

Holdout split:
200 tasks


Observed:

Discovery fit:
3/600

Transfer fit:
5/200

Holdout fit:
2/200


Pipeline outcome:

Invariants:
0

Skills:
0

Capabilities:
0

IG:
Unavailable


Holdout accuracy:

ASFT:
1/200

Baselines:
1/200


Most important observation:

Every major mechanism
failed to activate.

14G-2 The Failure Cascade

The biggest mistake would be analyzing:

Transfer failed.


or

Capability growth failed.


directly.

Instead we must locate the first broken link.

Expected chain:

ARC Task
↓
Trace
↓
Invariant
↓
Skill
↓
Transfer
↓
Capability
↓
IG


Observed chain:

ARC Task
↓
Trace
↓
NO INVARIANTS


Everything downstream collapsed automatically.

Therefore:

ARC failure
=
upstream failure


not:

Transfer failure


or:

CGM failure

14G-3 Root Cause Analysis

Let's evaluate the major hypotheses.

Hypothesis A
IDT Is Fundamentally Wrong

Expected evidence:

Synthetic failure

ARC failure


Observed:

Synthetic discovery exists.

ARC discovery absent.


Interpretation:

The evidence does NOT support:

IDT fundamentally wrong.


Verdict:

Weak support.

Hypothesis B
Trace Representation Failure

Question:

Did ARC produce useful traces?

Observed:

Only 3 discovery traces fit DSL.


Meaning:

Most ARC tasks never entered the trace-discovery process.

Interpretation:

The invariant miner never saw meaningful candidate structures.

Verdict:

Strong support.

Hypothesis C
DSL Coverage Failure

This is the strongest explanation.

Observed:

10-program symbolic adapter


covered:

3/600


discovery tasks.

Coverage:

0.5%


or lower depending on split.

Interpretation:

The representation language was dramatically smaller than the ARC task space.

This means:

ARC


was not actually being analyzed.

Only a tiny subset was.

Verdict:

✅ Strongly Supported

Hypothesis D
ARC Is Too Hard

Common explanation.

Evidence:

Insufficient.

Because:

ASFT never reached the point
where ARC difficulty mattered.


The system failed before:

Invariant Discovery


could begin.

Therefore:

Difficulty


is not the primary explanation.

Verdict:

Weak support.

14G-4 What Actually Failed?

The evidence suggests:

Reasoning Layer


did not fail.

Skill Layer


did not fail.

Transfer Layer


did not fail.

Instead:

Representation Layer


failed.

Meaning:

The system could not translate:

ARC Task


into:

ASFT-compatible experience.


This distinction is critical.

14G-5 ARC Coverage Analysis

Let's quantify the bottleneck.

Discovery:

3/600


Transfer:

5/200


Holdout:

2/200


Interpretation:

More than:

99%


of ARC tasks never entered the ASFT pipeline.

Therefore:

The observed result:

0 invariants

0 skills

0 capabilities


is unsurprising.

The system effectively experienced:

No meaningful data.

14G-6 Why Synthetic Tasks Worked

This comparison is revealing.

Synthetic tasks:

Generator
↓
Solver
↓
Trace Vocabulary
↓
Invariant Vocabulary


all aligned.

ARC:

Task Distribution


vastly exceeds:

DSL Coverage


Therefore:

Synthetic success may be explained by:

Representation Alignment.


ARC exposed the lack of that alignment.

14G-7 What ARC Actually Validated

A common mistake would be saying:

ARC disproved ASFT.


That is not what happened.

ARC validated:

Current DSL insufficient.


ARC did NOT validate:

IDT false

SCT false

Transfer false

CGM false


Those mechanisms never activated.

Therefore:

ARC outcome is:

Representation Failure


more than:

Theory Failure.

14G-8 ARC and IDT

Phase 13B:

Synthetic recurrence


exists.

Phase 13G:

No recurrence detected.


Interpretation:

IDT currently requires:

Recognizable operation structure.


ARC traces did not provide that.

Result:

Invariant Discovery
never started.

14G-9 ARC and SCT

Phase 13C:

Skills emerged.


Phase 13G:

0 skills.


Reason:

No invariants.


Therefore:

ARC provides:

No direct evidence
for or against SCT.


Important distinction.

14G-10 ARC and CGM

Phase 13E:

Positive CGR

Positive IG


Phase 13G:

Unavailable.


Reason:

No capabilities formed.


Again:

No evidence against CGM.

No evidence supporting CGM.


Simply:

CGM never activated.

14G-11 What Would Have Needed To Happen?

For a valid ARC test:

Minimum chain:

ARC
↓
Trace
↓
Invariant


must occur.

Observed:

ARC
↓
Trace
↓
Stop


Therefore:

Phase 13G primarily tested:

DSL Coverage


not:

ASFT Theory.

14G-12 Threats to Validity
ARC-01

Bounded symbolic DSL.

Severity:

Critical

ARC-02

Extremely low task coverage.

Severity:

Critical

ARC-03

Repeated holdout exposure.

Severity:

Medium

ARC-04

No operationalized counting/grouping/object concepts.

Severity:

High

ARC-05

No invariant population.

Severity:

Critical

14G-13 What Survives?
Survives

✅ ARC identified a major bottleneck.

✅ ARC exposed DSL limitations.

✅ ARC demonstrated lack of coverage.

✅ ARC provided useful negative evidence.

Does Not Survive

❌ ARC validation claim.

❌ ARC transfer claim.

❌ ARC capability-growth claim.

❌ ARC intelligence-growth claim.

❌ ARC replication claim.

14G-14 Revised ARC Claim

Original expectation:

ASFT mechanisms should replicate on ARC.

Evidence-supported statement:

The current ARC implementation did not demonstrate invariant discovery, skill formation, transfer, capability growth, or intelligence-growth mechanisms. The dominant observed limitation was extremely low DSL coverage, which prevented the ASFT pipeline from activating on most ARC tasks.

14G-15 ARC Failure Scorecard
Question	StatusARC invariant discovery?	❌ No
ARC skill formation?	❌ No
ARC transfer?	❌ No
ARC capability growth?	❌ No
ARC intelligence growth?	❌ No
DSL coverage adequate?	❌ No
Theory disproven?	❌ No
Representation bottleneck identified?	✅ Yes
14G Conclusion
Scientific Verdict
ARC did not validate ASFT.

ARC did not falsify ASFT.

ARC primarily exposed a severe
representation and DSL-coverage bottleneck.

Most Important Finding

The single most important result of Phase 14G is:

The first broken link in the ARC pipeline is not transfer, capability growth, or intelligence growth. It is the inability of the current symbolic representation layer to convert most ARC tasks into ASFT-compatible experiences.

Deliverables of Phase 14G

✅ ARC Root-Cause Analysis

✅ Failure Cascade Analysis

✅ DSL Coverage Analysis

✅ Representation Analysis

✅ Theory-vs-Implementation Separation

✅ ARC Threats-to-Validity Assessment

✅ Revised ARC Claim

✅ ARC Failure Scorecard

Exit Decision
Phase 14G
✅ COMPLETE


The strongest defensible conclusion is:

Phase 13G does not provide evidence for ASFT's higher-level mechanisms because the pipeline rarely progressed beyond task representation. The dominant finding is a representation bottleneck caused by extremely limited DSL coverage, not a direct falsification of IDT, SCT, transfer, or CGM.