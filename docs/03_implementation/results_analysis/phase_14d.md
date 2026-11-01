Phase 14D: Transfer Analysis
Purpose

Phase 13D measured transfer.

Phase 14D answers the deeper question:

What exactly transferred, why did it transfer, where did transfer fail, and what does transfer actually tell us about ASFT?

This is arguably the most important analysis phase because:

IDT
↓
SCT
↓
Transfer
↓
CGM


Transfer is the bridge connecting the entire theory.

If transfer is weak, then:

Invariant Discovery
↓
Skill Formation


may simply be producing reusable artifacts without creating genuine capability growth.

14D-1 Original Transfer Thesis

The original ASFT transfer claims were:

TR-1
Skills transfer across tasks.

TR-2
Transfer reduces reasoning cost.

TR-3
Transfer contributes to capability growth.

TR-4
Transfer should outperform non-transfer baselines.

TR-5
Transfer should scale to ARC-like settings.

14D-2 What The Evidence Shows

Across Phase 13C, 13D, 13E, 13F, and 13G:

Strong Findings

✅ Reuse occurred repeatedly.

✅ Positive transfer events occurred.

✅ Reasoning cost reductions were observed.

✅ Reflection-based transfer worked.

✅ Rotation-based transfer worked.

✅ Cross-family synthetic transfer occurred.

Mixed Findings

⚠ Structural transfer incomplete.

⚠ Multi-skill transfer largely unavailable.

⚠ Transfer→Growth relationship unstable.

⚠ Baseline superiority inconsistent.

Failed Findings

❌ ARC transfer not demonstrated.

❌ Transfer-aware ranking superiority not demonstrated.

❌ Transfer did not consistently predict CGR.

14D-3 Analysis of TR-1
Claim
Skills transfer across tasks.

Evidence

Phase 13C:

201 positive-credit reuses


Phase 13D:

Positive:

Near Transfer

Moderate Transfer

Cross-Family Transfer


Observed:

Reflection
→
Reflection+Count

Reflection
→
Grouping variants

Rotation
→
Related rotation tasks

Interpretation

Transfer clearly exists inside the synthetic environment.

This is one of the strongest findings in the entire project.

Important distinction:

The evidence supports:

Transfer Events


not necessarily:

General Transfer Theory

Scientific Verdict

Status:

✅ Supported (synthetic scope)

14D-4 Analysis of TR-2
Claim
Transfer reduces reasoning cost.

Evidence

Phase 13C:

Mean normalized reduction ≈ 0.227


Phase 13D:

Positive:

Reasoning reduction

Search reduction

Reuse savings


Cost correction audits were performed and retained.

Importantly:

Incorrect replays
=
zero benefit

Interpretation

This is one of the strongest results.

Unlike some other claims:

Reasoning reduction


survived auditing.

Evidence remains positive even after:

Accounting correction

Scientific Verdict

Status:

✅ Strongly Supported (synthetic scope)

14D-5 Analysis of TR-3
Claim
Transfer contributes
to capability growth.


This is where things become difficult.

Supporting Evidence

Phase 13E:

Positive CGR

Positive IG


Suggests:

Transfer
may contribute
to growth.

Contradictory Evidence

Phase 13D posthoc:

Mean CGR = -0.060


Phase 13E:

TS → CGR

r = -0.503


with wide confidence interval.

Interpretation

The expected relationship:

More Transfer
↓
More Growth


does not appear reliably.

This is one of the most important findings in Phase 14.

Current evidence shows:

Transfer exists.


but does NOT show:

Transfer drives growth.

Scientific Verdict

Status:

❌ Not Established

14D-6 Analysis of TR-4
Claim
Transfer outperforms
non-transfer baselines.


Evidence is mixed.

Positive Findings

Phase 13D:

ASFT beat:

B1

B2

B3


Examples:

ASFT − B1

Positive

ASFT − B2

Positive

ASFT − B3

Strongly Positive

Negative Findings

Phase 13D:

ASFT − B4

Negative


B4 compression proxy slightly exceeded ASFT.

Interpretation

Transfer superiority is:

Comparator-dependent.


ASFT transfer:

>
No learning

>
Random transfer


But not clearly:

>
Compression-based reuse

Scientific Verdict

Status:

🟡 Partially Supported

14D-7 Structural Transfer Analysis

One of the original ambitions.

Expected
Reflection

+

Count

+

Grouping

↓

New Task

Actual

Many structural-transfer cells were unavailable.

Reason:

CountSkill absent

GroupingSkill absent


Therefore:

Required components
never existed.

Interpretation

This is not a negative result.

It is an:

Unavailable Result.


The experiment could not fully run.

Scientific Verdict

Status:

⚪ Unavailable

14D-8 Negative Transfer Analysis

An important success.

Evidence shows:

Rotation candidates

Negative TS


Incorrect transfer:

No reward

No utility


This means:

ASFT can distinguish:

Helpful Transfer

vs

Harmful Transfer


This is scientifically valuable.

Scientific Verdict

Status:

✅ Supported

14D-9 ARC Transfer Analysis

This is the most important external-validity result.

Phase 13G:

0 skills

0 capabilities

0 transfer chain


Therefore:

Transfer on ARC


cannot be evaluated.

Important distinction:

The result is NOT:

Transfer fails on ARC.


The result is:

Transfer never emerged
on ARC.


because:

Invariant Discovery
never emerged.


This points upstream.

Scientific Verdict

Status:

❌ Not Demonstrated

14D-10 Why Transfer Worked

Evidence suggests transfer succeeds when:

Condition 1

Shared operation vocabulary.

Condition 2

Shared trace structure.

Condition 3

Reusable reflection/rotation patterns.

Condition 4

Synthetic generator consistency.

Under these conditions:

Transfer is reliable.

14D-11 Why Transfer Failed

Transfer struggles when:

Missing Skills
CountSkill absent

GroupingSkill absent

Missing Invariants
ARC

Compression Competitors
Memory

Compression


match or exceed ASFT.

Growth Link
Transfer

↓

Capability Growth


remains weak.

14D-12 Transfer Taxonomy Revisited

After all evidence:

Transfer Type	StatusNear Transfer	✅ Supported
Moderate Transfer	✅ Supported
Cross-Family Transfer	✅ Supported
Structural Transfer	⚪ Unavailable
Multi-Skill Transfer	⚪ Unavailable
ARC Transfer	❌ Not Demonstrated
14D-13 What Survives?
Survives

✅ Reuse exists

✅ Transfer exists

✅ Cost reduction exists

✅ Negative transfer detectable

✅ Cross-family transfer exists

Does Not Survive

❌ Transfer predicts growth

❌ Structural transfer validated

❌ ARC transfer validated

❌ Universal baseline superiority

14D-14 Revised Transfer Claim

Original claim:

Skills transfer across tasks and drive capability growth.

Evidence-supported claim:

In controlled synthetic environments, reflection- and rotation-based skills can be reused across related tasks, producing measurable reductions in the repository's reasoning-cost proxy. Transfer events are consistently observed, but evidence does not establish that transfer drives capability growth, generalizes to ARC, or exceeds all competitive baselines.

14D-15 Transfer Final Scorecard
Transfer Claim	StatusTransfer exists	✅ Supported
Transfer reduces cost	✅ Supported
Cross-family transfer exists	✅ Supported
Negative transfer detectable	✅ Supported
Transfer drives growth	❌ Not established
Structural transfer	⚪ Unavailable
ARC transfer	❌ Not demonstrated
Universal superiority	❌ Not supported
14D Conclusion
Scientific Verdict
Transfer as a reuse mechanism
✅ Validated in synthetic environments

Transfer as a growth mechanism
❌ Not validated

Transfer on ARC
❌ Not demonstrated

Transfer superiority over all alternatives
❌ Not demonstrated

Deliverables of Phase 14D

✅ Transfer Claim Review

✅ Cost Reduction Analysis

✅ Baseline Interpretation

✅ Negative Transfer Analysis

✅ Structural Transfer Review

✅ ARC Transfer Analysis

✅ Transfer Taxonomy Update

✅ Revised Transfer Claim

✅ Final Transfer Scorecard

Exit Decision
Phase 14D
✅ COMPLETE


The strongest defensible conclusion is:

ASFT demonstrates reliable synthetic task-to-task transfer and reasoning-cost reduction through skill reuse, but the evidence does not establish that transfer drives capability growth, supports robust structural transfer, or generalizes to ARC environments.