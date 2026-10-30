Phase 11D-3: Skill Lifecycle Management

This is the phase where SCT becomes a living system instead of a one-time skill creator.

Until now we have defined:

Invariant Discovery
↓
Skill Candidate
↓
Economic Evaluation
↓
Skill Creation


But a real intelligence system cannot stop there.

Humans don't just create skills.

They:

Learn Skills
↓
Use Skills
↓
Improve Skills
↓
Forget Skills
↓
Revive Skills
↓
Combine Skills


This phase defines the complete lifecycle of a skill from birth to retirement.

Goal of Phase 11D-3

Answer:

What happens to a skill after it is created?

More specifically:

How does a skill grow?

How does a skill become important?

How does a skill decay?

When should it be retired?

Can it return later?

How does capability evolve over time?

Core Principle

Traditional systems:

Create Skill
↓
Store Skill
↓
Done


ASFT:

Create Skill
↓
Monitor Skill
↓
Evaluate Skill
↓
Promote Skill
↓
Retire Skill
↓
Possibly Reactivate Skill

Complete Skill Lifecycle

The complete lifecycle should be:

Candidate
↓
Promoted
↓
Active
↓
Growing
↓
Core Skill
↓
Dormant
↓
Retired
↓
Archived

(Optional)

Archived
↓
Reactivated

Stage 1
Candidate

Origin:

Validated Invariant


Status:

Under Evaluation


Characteristics:

✅ Not executable yet

✅ Utility unknown

✅ Transfer partially known

✅ Economic value estimated

Question:

Should this become a skill?

Entry Conditions

Must satisfy:

✅ Validated invariant

✅ Positive transfer

✅ Positive SCV

✅ Sufficient evidence

Exit Conditions

Either:

Promoted


or

Rejected

Stage 2
Promoted

This is the birth of a skill.

Definition:

Skill now enters capability memory.


Characteristics:

✅ Skill ID assigned

✅ Utility tracking begins

✅ Retrieval enabled

✅ Transfer tracking enabled

Important:

A promoted skill is NOT yet trusted.

It must prove itself.

Stage 3
Active Skill

Definition:

A skill currently being used.

Characteristics:

✅ Reuse observed

✅ Transfer observed

✅ Positive utility

Metrics tracked:

Reuse Count

Transfer Score

Utility

Cost Reduction


Example:

ReflectionSkill


used repeatedly.

Stage 4
Growing Skill

Definition:

A skill demonstrating increasing value.

Characteristics:

Reuse Increasing

Transfer Increasing

Utility Increasing


Formula:

UG=Utilityt−Utilityt−1UG = Utility_t - Utility_{t-1}

Where:

UG
=
Utility Growth


Positive UG:

Skill Growing


Negative UG:

Skill Declining

Why This Matters

Not all skills evolve equally.

Some become foundational.

Some disappear.

Stage 5
Core Skill

This is the highest status.

Definition:

A skill repeatedly used across many task families.

Examples:

Reflection

Rotation

Counting

Grouping


Characteristics:

✅ High utility

✅ High transfer

✅ High reuse

✅ Low negative transfer

✅ Frequently composed

Core Skill Criteria

Must satisfy:

SU>SUcoreSU > SU_{core} TS>TScoreTS > TS_{core} Reuse>RcoreReuse > R_{core}

Core skills become:

Capability Anchors

Capability Anchors

New concept.

These are skills responsible for most transfer.

Example:

ReflectionSkill


may contribute to:

20+
 future tasks


ASFT should explicitly identify these.

Stage 6
Dormant Skill

Definition:

A skill not recently used but not yet useless.

Characteristics:

Low Recent Reuse

Potential Future Value


Example:

GroupingSkill


not used for:

10 tasks


But historically useful.

Dormant skills remain in memory.

Why Dormancy Exists

Without dormancy:

Unused
↓
Delete


Too aggressive.

Humans do not work like this.

Many skills remain dormant for long periods.

Stage 7
Retired Skill

Definition:

A skill no longer producing sufficient utility.

Characteristics:

Low Utility

Low Transfer

Low Reuse


Retirement Criteria

Example:

SU<SUminSU < SU_{min}

for extended periods.

and

Reuse≈0Reuse \approx 0

and

TS≈0TS \approx 0

Then:

Active
↓
Retired

Important

Retired ≠ Deleted

Retired means:

Not available
for normal retrieval


but still stored.

Stage 8
Archived Skill

Definition:

Historical skill.

Characteristics:

✅ Stored

✅ Not retrieved

✅ Not evaluated

✅ Historical evidence preserved

Purpose:

Maintain learning history.

Stage 9
Reactivated Skill

One of the most interesting concepts.

Question:

Can a retired skill return?


ASFT answer:

Yes


Example

Skill:

GroupingSkill


retired.

Many future grouping tasks appear.

System detects:

New Evidence


Skill becomes:

Active Again

Reactivation Criteria

Must satisfy:

Evidence Reappears

Transfer Potential Exists

Utility Expected Positive

Skill Health Model

Every skill should maintain a health score.

Purpose:

Continuous monitoring.

Components:

Utility

Reuse

Transfer

Confidence


Conceptually:

Health=f(Utility,Reuse,Transfer,Confidence)Health = f( Utility, Reuse, Transfer, Confidence )

States:

Healthy

Stable

Weak

Critical

Skill Aging

Important for long-term systems.

Question:

Should old skills be trusted forever?


Answer:

No.

Evidence should age.

Old evidence becomes less important than recent evidence.

Recency Weight
RW=e−λtRW = e^{-\lambda t}

Where:

t
=
time since use


This prevents:

Ancient Skills
dominating forever

Skill Monitoring System

Every skill should continuously track:

Reuse History
When used?

Transfer History
Where did it help?

Failure History
Where did it hurt?

Utility History
How valuable was it?


This creates a complete skill biography.

Skill Biography

New concept.

Every skill should have:

Birth

Growth

Peak Utility

Transfer Events

Failures

Retirement


This is valuable for explainability.

Lifecycle Metrics

ASFT should monitor:

Skill Age
SASA
Skill Utility
SUSU
Utility Growth
UGUG
Reuse Frequency
RFRF
Transfer Score
TSTS
Health Score
HSHS
Failure Modes

Lifecycle system can fail.

Failure 1

Immortal Skills

Nothing retires.

Result:

Memory Explosion

Failure 2

Premature Retirement

Useful skills removed.

Result:

Lost Capability

Failure 3

Dormancy Trap

Too many dormant skills.

Result:

Retrieval Noise

Failure 4

Zombie Skills

Retired skills repeatedly reactivated without value.

Result:

Instability

Success Criteria

Lifecycle Management succeeds if:

✅ Useful skills survive

✅ Core skills emerge

✅ Weak skills retire

✅ Dormancy works

✅ Reactivation works

✅ Capability memory remains stable

✅ Transfer remains positive

Relationship To Capability Growth

This is extremely important.

Capability growth is not:

More Skills


Capability growth is:

Healthier Skill Ecosystem


Meaning:

Useful Skills Grow

Weak Skills Leave

Core Skills Stabilize

Transfer Improves

Deliverables of Phase 11D-3

✅ Complete skill lifecycle

✅ Lifecycle states

✅ Promotion model

✅ Growth model

✅ Core skill model

✅ Dormancy model

✅ Retirement model

✅ Archive model

✅ Reactivation model

✅ Skill health framework

✅ Aging model

✅ Skill biography concept

✅ Lifecycle metrics

✅ Failure modes

✅ Success criteria

Most Important Outcome

The single most important decision of Phase 11D-3 is:

Skills are not static objects. They are living capability assets that continuously evolve through growth, reuse, transfer, dormancy, retirement, and reactivation.

This transforms SCT from:

Skill Creation Theory


into:

Skill Evolution Theory


and creates the foundation for the next phase:

Phase 11D-4: Skill Composition

where we define how:

ReflectionSkill
+
CountingSkill
↓
New Capability


which is likely the mechanism through which ASFT scales from simple transfer to genuine capability growth.