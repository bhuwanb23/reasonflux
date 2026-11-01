Phase 14B: Contribution 1 (IDT) Critical Results Analysis
Purpose

Phase 13B answered:

What happened?


Phase 14B answers:

Why did it happen?

What does it mean?

What survives scientifically?

What fails scientifically?


This phase is exclusively about Contribution 1: Invariant Discovery Theory (IDT).

14B-1 Original IDT Thesis

The original IDT claims were:

IDT-1
Useful invariants emerge from experience.

IDT-2
Invariant strength predicts future transfer.

IDT-3
Transfer-aware discovery
outperforms frequency-only discovery.


Phase 14B evaluates each independently.

14B-2 What The Evidence Actually Shows

From the consolidated evidence:

Strong findings

✅ Recurring trace structures exist.

✅ Reflection-related patterns repeatedly emerge.

✅ Rotation-related patterns repeatedly emerge.

✅ Discovery is repeatable across seeds.

✅ Candidate generation is stable.

✅ Noise robustness is reasonably strong.

Weak findings

⚠ Correlations depend on tiny candidate populations.

⚠ Discovery is operation-level, not abstract-concept-level.

⚠ Same generator supplies tasks, labels, and evaluation structure.

Failed findings

❌ Transfer-aware ranking does not outperform frequency-only ranking on the primary benchmark.

❌ IS does not consistently predict transfer across later experiments.

14B-3 Analysis of IDT-1
Claim
Useful invariants emerge from experience.

Evidence

Phase 13B discovered:

apply_reflection

find_symmetry

apply_rotation

find_rotation

count_objects

group_by_color


repeatedly across seeds.

Metrics:

IP = 1.0

IR = 1.0


within the synthetic framework.

Critical Interpretation

The evidence clearly shows:

Recurrence Detection


works.

The evidence does NOT show:

Open-ended Concept Discovery


because:

Task generator

Solver

Labels


all share the same vocabulary.

Therefore:

Strong Version
ASFT discovers general invariants.


Status:

❌ Unsupported

Narrow Version
ASFT discovers recurring operation-level
structures in synthetic traces.


Status:

✅ Supported

14B-4 Analysis of IDT-2
Claim
Invariant strength predicts transfer.

Early Evidence

Phase 13B:

Pearson ≈ 1.0

Spearman ≈ 1.0


Initially this looked extremely strong.

Later Evidence

Phase 13D:

IS vs TS

r = -0.042


with confidence interval touching zero.

This is the critical result.

Interpretation

The original correlation:

r = 1.0


came from:

≈ 4.4 promoted candidates per seed


and largely separated:

Reflection

vs

Rotation


rather than many independent invariant classes.

Therefore:

The original correlation
was fragile.

Scientific Conclusion

Current evidence supports:

IS can be associated with transfer
in small synthetic settings.


Current evidence does NOT support:

IS reliably predicts transfer.


Status:

❌ Not Established

14B-5 Analysis of IDT-3
Claim
Transfer-aware discovery
beats frequency-only discovery.


This is the most important IDT result.

Primary Evidence

Phase 13B:

ASFT
=
Frequency
=
No-transfer


Mean TU:

0.095809


for all three.

Difference:

0.000000


Strict gate:

FAILED

Why This Matters

IDT's biggest novelty claim was:

Transfer-awareness matters.


The primary benchmark showed:

Transfer-awareness changed nothing.


Therefore:

The benchmark does not support
the superiority claim.

14B-6 What About EXP-IDT-14?

This requires careful handling.

EXP-IDT-14 introduced:

Frequent useless pattern

normalize_grid


Results:

Transfer-aware > Frequency

Interpretation

EXP-IDT-14 proves:

The ranking mechanism
can respond to confounds.


EXP-IDT-14 does NOT prove:

Transfer-aware ranking
is generally superior.


Reason:

Confound deliberately inserted.


after observing the original tie.

Classification:

Exploratory Evidence


only.

14B-7 Why Did IDT-3 Fail?

This is the most important analysis question.

Hypothesis A

Transfer-awareness is useless.

Evidence:

Insufficient.

Hypothesis B

Benchmark incapable of distinguishing rankings.

Evidence:

Strong.

Why?

Because:

Useful
=
Frequent


inside synthetic-v1.

Therefore:

Frequency ranking

and

Transfer ranking

choose the same candidates.


This explanation fits all observed data.

14B-8 Robustness Analysis
Noise

Rank overlap:

≈72%


Interpretation:

Moderately robust.

Not perfectly stable.

Variation Survival
VST = 1.0


Interpretation:

Patterns survive generator-level perturbations.

Limitation:

Still within same synthetic family.

14B-9 ARC Evidence

Phase 13G:

0 invariants

0 skills

0 capabilities


This is the strongest external-validity result.

Interpretation:

Current IDT implementation depends heavily on:

Known operation vocabulary

Known DSL

Known trace structure


IDT has not demonstrated:

ARC-level invariant discovery.


Status:

❌ External validity not demonstrated

14B-10 Threats to Validity
Threat 1

Shared Generator Vocabulary

High Severity

Threat 2

Operation-Level Labels

Medium Severity

Threat 3

Tiny Candidate Population

High Severity

Threat 4

Synthetic Dependence

High Severity

Threat 5

No ARC Discovery Success

High Severity

14B-11 What Survives?

After all evidence:

Survives

✅ Trace recurrence detection

✅ Candidate invariant generation

✅ Ranking infrastructure

✅ Robust synthetic discovery

✅ Repeatability across seeds

✅ Mechanism sensitivity (EXP-IDT-14)

Does Not Survive

❌ Transfer-aware superiority

❌ General IS predictive validity

❌ ARC invariant discovery

❌ Broad external validity

14B-12 Revised IDT Claim

Original claim:

Transfer-aware invariant discovery identifies reusable knowledge and outperforms frequency-based discovery.

Evidence-supported claim:

In controlled synthetic environments, ASFT can identify recurring operation-level structures from reasoning traces. These structures are stable across seeds and perturbations, but evidence does not currently establish that transfer-aware ranking outperforms frequency-based ranking or that discovered invariant strength reliably predicts future transfer.

14B-13 IDT Final Scorecard
IDT Claim	StatusInvariants emerge	✅ Supported (synthetic scope)
Discovery repeatable	✅ Supported
Discovery robust	✅ Supported
IS predicts transfer	❌ Not established
Transfer-aware > frequency	❌ Failed primary gate
ARC invariant discovery	❌ Not demonstrated
External validity	❌ Not demonstrated
14B Conclusion
Scientific Verdict
IDT as a discovery mechanism
✅ Works in synthetic environments

IDT as a transfer-predictive theory
❌ Not validated

IDT as an ARC-relevant discovery theory
❌ Not demonstrated

Deliverables of Phase 14B

✅ IDT Claim Review

✅ Failure Analysis

✅ EXP-IDT-14 Interpretation

✅ Robustness Interpretation

✅ ARC Interpretation

✅ Threats-to-Validity Assessment

✅ Revised Claim Statement

✅ Final IDT Scorecard

Exit Decision
Phase 14B
✅ COMPLETE


The strongest defensible conclusion is:

ASFT demonstrates repeatable synthetic invariant discovery, but the evidence does not support transfer-aware ranking superiority, reliable transfer prediction from invariant strength, or ARC-level invariant discovery. The core discovery mechanism survives; the strongest theoretical claims do not.