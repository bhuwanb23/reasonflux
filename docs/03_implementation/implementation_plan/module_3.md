Phase 10C: Skill Creation Trigger Algorithms

This is the heart of ASFT.

After all 10 phases so far, this is the contribution that survived every review attack, novelty challenge, and architecture simplification.

If I had to bet on one contribution carrying the paper, it would be:

Skill Creation Trigger Theory (SCT)

Because almost every system studies:

How to use skills


Very few study:

When should a skill be created?

Phase 10C Goal

Answer:

Given a discovered invariant, how does ASFT decide whether it deserves to become a reusable skill?

Not:

Can it become a skill?


But:

Should it become a skill?


That distinction is crucial.

First Principle

Most naive systems do:

Pattern Appears
↓
Create Skill


This creates:

Thousands of useless skills


which becomes:

Memory Explosion


and

Transfer Collapse

ASFT Principle

Skills should be:

Earned


not

Created Automatically

Skill Lifecycle

Every skill goes through stages.

Invariant
↓
Candidate Skill
↓
Evaluation
↓
Promotion
↓
Reusable Skill
↓
Retirement (optional)

Stage 1
Skill Candidate Generation

Input:

Invariant


from Phase 10B.

Example:

FindSymmetry
+
ApplyReflection


Detected as:

ReflectionInvariant


Now create:

SkillCandidate
{
    candidate_id

    source_invariant

    frequency

    transfer_score

    abstraction_gain

    creation_cost
}


Example

{
    candidate_id: "SC_01",

    source_invariant:
        ReflectionInvariant,

    frequency: 15,

    transfer_score: 0.63,

    abstraction_gain: 0.72,

    creation_cost: 4
}

Stage 2
Skill Creation Value (SCV)

This becomes the core decision function.

Design Requirement

SCV should answer:

Will this skill save
more reasoning
than it costs?

Formula v1
SCV=Reuse×Transfer×AbstractionGain−CreationCostSCV = Reuse \times Transfer \times AbstractionGain - CreationCost

Expanded:

SCV=R×TS×AG−CCSCV = R \times TS \times AG - CC

where:

R
=
Expected Reuse

TS
=
Transfer Score

AG
=
Abstraction Gain

CC
=
Creation Cost

Interpretation

High:

Create Skill


Low:

Do Not Create

Example

Suppose:

Reuse = 10

TS = 0.7

AG = 0.8

CC = 3


Then:

SCV

=
10 × 0.7 × 0.8 − 3

=
2.6


Positive.

Create skill.

Stage 3
Promotion Rule

This is where candidates become skills.

Rule
If

SCV > Threshold

Promote


Example

Threshold:

2.0


Skill:

SCV = 2.6


Result:

ReflectionSkill


created.

Why Threshold Exists

Without threshold:

Every Invariant
Becomes Skill


which is bad.

Stage 4
Skill Representation

After promotion:

Skill
{
    skill_id

    source_invariant

    trigger_conditions

    execution_policy

    utility

    reuse_count

    status
}


Example

{
    skill_id:"ReflectionSkill",

    trigger_conditions:
        SymmetryDetected,

    execution_policy:
        ApplyReflection,

    utility:0.81,

    reuse_count:19,

    status:"Active"
}

Stage 5
Skill Utility Update

Skills should evolve.

Every reuse updates:

Utility


Formula

SU=AccuracyGain×CostReduction×TransferabilitySU = AccuracyGain \times CostReduction \times Transferability

High SU:

Important Skill


Low SU:

Candidate Retirement

Stage 6
Skill Retirement

This is surprisingly important.

Without retirement:

Library Grows Forever


Eventually:

Thousands of Dead Skills

Retirement Rule

Retire if:

Reuse Count Low

AND

Transfer Score Low

AND

Utility Low


Example

Never Used
For 50 Tasks


Retire.

Skill States

Every skill has a state machine.

Candidate
↓
Promoted
↓
Active
↓
Dormant
↓
Retired

Why This Matters

Human memory behaves similarly.

Not every skill remains active forever.

Skill Categories

For MVP.

Reflection Skills
ApplyReflection

Rotation Skills
ApplyRotation

Counting Skills
CountObjects


These become the first reusable capabilities.

Skill Reuse Mechanism

Suppose:

Task:

Reflect Object Group


System checks:

Skill Library


Finds:

ReflectionSkill


Instead of:

Full Search


it executes:

ReflectionSkill


Reasoning Cost drops.

Why This Is Different From Memory

Reviewer attack:

Isn't this just memory?

Memory:

Store Solution


ASFT:

Store Reusable Procedure


Important distinction.

Why This Is Different From DreamCoder

DreamCoder:

Program Compression


ASFT:

Skill Emergence Decision


The key novelty is not:

Skill Exists


but:

Why Skill Exists

Skill Trigger Algorithm (Pseudo Flow)
New Trace
↓
Invariant Detector
↓
Invariant Candidate
↓
Compute SCV
↓
SCV > Threshold ?
↓
YES → Create Skill

NO → Observe More

MVP Algorithm

Keep simple.

for invariant in invariants:

    scv =
        reuse *
        transfer *
        abstraction_gain \
        - creation_cost

    if scv > threshold:
        create_skill()


No ML required initially.

No neural networks.

No LLMs.

Pure research validation.

Success Criteria

SCT succeeds if:

✅ Useful skills emerge

✅ Skills are reused

✅ Transfer improves

✅ Reasoning cost drops

✅ Library remains manageable

Failure Criteria

SCT fails if:

❌ Every invariant becomes skill

❌ Skills never reused

❌ Transfer remains flat

❌ Reasoning cost unchanged

❌ Library explodes

Deliverables of Phase 10C

✅ Skill candidate generation

✅ SCV definition

✅ Promotion rules

✅ Skill representation

✅ Skill utility updates

✅ Skill retirement policy

✅ Skill lifecycle

✅ Skill reuse mechanism

✅ SCT algorithm

✅ MVP implementation logic

Most Important Outcome

The central engineering decision is:

ASFT does not create skills because patterns exist.

Instead:

ASFT creates skills only when the expected future reasoning savings exceed the cost of creating and maintaining the skill.

This is the concrete implementation of Skill Creation Trigger Theory, and it remains the most novel and defensible contribution in the entire project.

Next Phase

Phase 10D: Skill Library Design

There we will define:

library architecture,
indexing,
retrieval algorithms,
skill composition,
memory management,
transfer mechanisms,
and how Task A skills become available to Task B and Task C.

That phase connects SCT to actual capability growth.