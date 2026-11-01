Phase 14C: Contribution 2 (SCT) Critical Results Analysis
Purpose

Phase 13C answered:

What happened when SCT was tested?


Phase 14C answers:

Did SCT actually demonstrate its core theory?

What worked?

What failed?

What survives scientifically?

What should be removed, narrowed, or reformulated?


This phase evaluates Contribution 2: Skill Creation Trigger Theory (SCT).

14C-1 Original SCT Thesis

The original SCT theory contained three major claims:

SCT-1
Skills emerge from validated invariants.

SCT-2
Skill creation should be governed
by expected future value.

SCT-3
Economically justified skill creation
outperforms naive creation policies.


Everything in Phase 14C revolves around these claims.

14C-2 What The Evidence Actually Shows

From Phase 13C, 13F, and 13H:

Strong Findings

✅ Reflection skills emerged

✅ Rotation skills emerged

✅ Skills were reused

✅ Skills reduced measured reasoning cost

✅ Utility strongly correlated with future value

✅ Composition worked for rotation→reflection

✅ SCV correlated with future value

Weak Findings

⚠ Counting skills never emerged

⚠ Grouping skills never emerged

⚠ Composition evidence is limited

⚠ Lifecycle evidence is narrow

Failed Findings

❌ SCT did not outperform Always Create

❌ SCT did not outperform Random Create

❌ SCT lost badly to Memory Only

❌ No-SCV ablation often tied SCT

14C-3 Analysis of SCT-1
Claim
Skills emerge from validated invariants.

Evidence

Phase 13C:

44 skill instances

Reflection

Rotation


Across:

10 confirmation seeds


Observed:

Reflection → ReflectionSkill

Rotation → RotationSkill


Not observed:

CountSkill

GroupingSkill

Interpretation

The evidence clearly supports:

Skill emergence


within the synthetic environment.

The evidence does NOT support:

General skill emergence


because:

Only 2 of 4 families emerged.

Scientific Verdict
Strong Version
ASFT can generate skills broadly.


Status:

❌ Unsupported

Narrow Version
ASFT can generate reusable
reflection and rotation skills
within the synthetic environment.


Status:

✅ Supported

14C-4 Analysis of SCT-2
Claim
SCV predicts future value.

Evidence

Phase 13C:

SCV10

ρ = 0.700


with:

CI = [0.545, 0.931]


Utility correlations:

SU ↔ Future Net Value

ρ = 0.937

Interpretation

SCV is not random.

There is a meaningful association between:

SCV


and

Future Value


However:

Other predictors perform similarly or better.

Examples:

Frequency

ρ = 0.748

p_reuse

ρ = 0.884


This is critical.

The evidence supports:

SCV carries signal.


The evidence does NOT support:

SCV is the best signal.

Scientific Verdict

Status:

🟡 Partially Supported

Revised claim:

SCV is associated with future value in the synthetic environment, but its predictive advantage over simpler signals has not been demonstrated.

14C-5 Analysis of SCT-3
Claim
SCT policy
outperforms naive policies.


This is the core SCT claim.

Evidence

Phase 13C:

Policy	Mean Net ValueSCT	0.345
Always Create	0.345
Random Create	0.345
Never Create	0.000
Memory Only	1.325

Critical observation:

SCT

=

Always Create

=

Random Create

Why?

All eligible candidates had:

SCV > 0


Therefore:

SCT selected everything.


Meaning:

No real selection pressure occurred.

Interpretation

The experiment did NOT test:

Which candidates should be rejected.


because:

No candidate was rejected.


This is extremely important.

The result is NOT:

SCT is wrong.


The result is:

The benchmark never forced SCT
to make difficult decisions.

Scientific Verdict

Status:

❌ Not Supported

14C-6 The Memory-Only Result

This is arguably the most important SCT finding.

Evidence
Memory Only

1.325

vs

SCT

0.345


Large difference.

Interpretation

Inside the synthetic environment:

Retrieval
>
Abstraction


Why?

Most likely:

Tasks are highly repetitive.

Exact replay is cheaper than
constructing abstractions.


This is a major challenge to SCT.

Scientific Meaning

Current evidence suggests:

Memory may explain much of
the observed benefit.


This does not kill SCT.

But it severely weakens:

Skill superiority claims.

14C-7 Composition Analysis
Evidence

Evaluable pair:

Rotation → Reflection


Results:

Best Single Skill

0%

Composed Pair

100%


Reasoning reduction:

0.429

Interpretation

Composition works.

But:

Only one pair.


Missing:

Count + Reflection

Group + Count

Multi-skill chains

Verdict

Status:

🟡 Promising but Limited

14C-8 Lifecycle Analysis

Lifecycle states observed:

Growing

Core


Evidence for:

Dormant

Retired

Reactivated


is limited.

Therefore:

Lifecycle machinery exists.

Lifecycle theory remains largely untested.

Verdict:

🟡 Incomplete Validation

14C-9 Why SCT Failed

This is the most important analysis.

Hypothesis A

SCT theory is fundamentally wrong.

Evidence:

Weak.

Hypothesis B

Synthetic benchmark lacks selective pressure.

Evidence:

Strong.

Observed:

All candidates

SCV > 0


Therefore:

SCT never needed to reject anything.


This perfectly explains:

SCT = Always Create

14C-10 ARC Evidence

Phase 13G:

0 skills

0 capabilities


Therefore:

ARC skill emergence


was not demonstrated.

Status:

❌ External validity not demonstrated

14C-11 Threats to Validity
Threat SCT-01

Small candidate diversity.

Severity:

High

Threat SCT-02

All-positive SCV population.

Severity:

High

Threat SCT-03

Memory-friendly environment.

Severity:

High

Threat SCT-04

Missing counting/grouping skills.

Severity:

Medium

Threat SCT-05

No ARC skill formation.

Severity:

High

14C-12 What Survives?
Survives

✅ Skill emergence

✅ Skill reuse

✅ Reasoning reduction

✅ Utility tracking

✅ SCV signal

✅ Limited composition

Does Not Survive

❌ SCT superiority

❌ SCV superiority

❌ Memory superiority

❌ ARC skill emergence

❌ Broad lifecycle validation

14C-13 Revised SCT Claim

Original claim:

Skills should be created when expected future value exceeds lifecycle cost, and SCT should outperform naive creation policies.

Evidence-supported claim:

In controlled synthetic environments, ASFT can construct reusable reflection and rotation skills from discovered trace patterns. Skill utility and SCV are associated with future value, but the evidence does not demonstrate that SCT provides a selection advantage over always-create, random-create, or memory-based alternatives.

14C-14 SCT Final Scorecard
SCT Claim	StatusSkills emerge	✅ Supported (synthetic scope)
Skills reused	✅ Supported
Skills reduce reasoning cost	✅ Supported
SCV correlates with value	🟡 Partial
SCT superiority	❌ Not supported
SCV superiority	❌ Not supported
Memory superiority	❌ Not supported
ARC skill emergence	❌ Not demonstrated
General lifecycle theory	❌ Not demonstrated
14C Conclusion
Scientific Verdict
SCT as a skill-construction mechanism
✅ Works in synthetic environments

SCT as a selective decision policy
❌ Not validated

SCT as an improvement over memory
❌ Not demonstrated

SCT on ARC
❌ Not demonstrated

Deliverables of Phase 14C

✅ SCT Claim Review

✅ SCV Analysis

✅ Policy Failure Analysis

✅ Memory-Only Interpretation

✅ Composition Analysis

✅ Lifecycle Analysis

✅ ARC Interpretation

✅ Threats-to-Validity Assessment

✅ Revised SCT Claim

✅ Final SCT Scorecard

Exit Decision
Phase 14C
✅ COMPLETE


The strongest defensible conclusion is:

ASFT demonstrates synthetic skill construction, reuse, and limited composition, but the evidence does not support SCT as a superior skill-selection policy, does not show advantages over memory-based retrieval, and does not demonstrate skill emergence on ARC.