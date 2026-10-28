Perfect.

This is the investigation that will determine whether we have a genuinely novel research direction or just a rebranded version of existing work.

The goal is not to find papers.

The goal is to build a capability map of intelligence architectures and identify exactly where the empty space exists.

Investigation 6: Existing Skill-Based Intelligence Systems
Core Evaluation Criteria

From our previous investigations, we derived the key dimensions:

Capability	MeaningSkill Creation	Can it create new capabilities?
Skill Storage	Can it remember skills?
Skill Composition	Can it combine skills?
Skill Compression	Can it abstract many experiences into one concept?
Continual Learning	Does it improve over time?
Meta-Reasoning	Does it reason about its own reasoning?
Generalization	Can it transfer to unseen problems?
ARC Alignment	Matches ARC's intelligence definition?
Category 1: Classical Cognitive Architectures
SOAR

One of the oldest AGI architectures.

Core idea:

Problem
↓
Production Rules
↓
Chunking
↓
New Rules

Strengths

✅ Stores learned rules

✅ Long-term memory

✅ Some skill accumulation

✅ Goal-directed reasoning

Weaknesses

❌ Poor abstraction creation

❌ Limited scalability

❌ Weak modern perception

Assessment

Interesting historically.

Not sufficient for ARC.

ACT-R

Human cognition inspired.

Modules:

Memory
Attention
Procedural Knowledge
Goals

Strengths

✅ Cognitive grounding

✅ Memory systems

✅ Skill reuse

Weaknesses

❌ Not open-ended

❌ Weak abstraction growth

Category 2: Program-Synthesis Intelligence
ARC Program Synthesis Systems

Examples:

Searching Latent Program Spaces
ARC DSL solvers
Evolutionary synthesis systems
Strengths

✅ Rule discovery

✅ Interpretable

✅ Good ARC performance

Weaknesses

❌ No persistent skill memory

❌ No capability growth

❌ No abstraction accumulation

Key Observation

They learn:

Program


not:

Capability

Category 3: Neuro-Symbolic Systems

Examples:

Compositional Neuro-Symbolic Reasoning
Neurosymbolic Program Synthesis for ARC using Vector Symbolic Algebras
Strengths

✅ Object reasoning

✅ Symbolic abstraction

✅ Better compositionality

Weaknesses

❌ Skills mostly handcrafted

❌ No skill evolution

❌ Weak lifelong learning

Observation

They manipulate abstractions.

They rarely create abstractions.

Category 4: Hierarchical Reinforcement Learning

This becomes extremely relevant.

Option-Critic

Core idea:

Primitive Actions
↓
Options
↓
Hierarchical Skills


Example:

Instead of:

Move Left
Move Right


learn:

Open Door


as a reusable skill.

Strengths

✅ Skill discovery

✅ Skill reuse

✅ Hierarchy

Weaknesses

❌ Mostly action-based

❌ Weak symbolic reasoning

❌ Limited abstraction

Important

This is the first category that genuinely learns reusable skills.

Category 5: DreamCoder

One of the most important systems for us.

DreamCoder

Core loop:

Solve Tasks
↓
Extract Programs
↓
Compress Programs
↓
Create New Primitives
↓
Future Tasks Easier


Read that again.

This is the closest thing we've found so far to our emerging hypothesis.

Strengths

✅ Skill extraction

✅ Skill compression

✅ New primitive creation

✅ Library growth

✅ Continual improvement

Weaknesses

❌ Mostly program-centric

❌ Limited meta-reasoning

❌ Not designed for ARC-3 style interaction

Critical Observation

DreamCoder may be the single most important prior art for us.

Any future proposal must clearly go beyond it.

Category 6: Voyager

One of the most interesting modern systems.

Voyager

Minecraft autonomous agent.

Core loop:

Task
↓
Solve
↓
Store Skill
↓
Reuse Skill
↓
Compose Skills

Strengths

✅ Skill library

✅ Lifelong learning

✅ Continual capability growth

✅ Automatic curriculum

Weaknesses

❌ LLM dependent

❌ Weak formal abstraction

❌ Skill quality varies

Observation

Voyager moves closer to cumulative intelligence.

Category 7: Generative Agents

Core concept:

Experience
↓
Reflection
↓
Memory
↓
Behavior

Strengths

✅ Reflection

✅ Memory

✅ Experience accumulation

Weaknesses

❌ Weak reasoning

❌ Weak skill formation

These are memory systems more than intelligence systems.

Category 8: World Models

Examples:

Dreamer
MuZero-style systems

Core idea:

Build Internal World
↓
Plan Within World

Strengths

✅ Planning

✅ Generalization

✅ Latent abstraction

Weaknesses

❌ Not explicit skill libraries

❌ Weak symbolic structure

Category 9: Meta-Learning

"Learning to Learn"

Core idea:

Many Tasks
↓
Learn Adaptation Strategy

Strengths

✅ Fast adaptation

✅ Generalization

Weaknesses

❌ Usually no explicit skill memory

❌ Little interpretability

Important

Meta-learning learns adaptation mechanisms.

Not necessarily reusable skills.

Category 10: ARC-Specific Self-Improving Systems

Examples:

Recursive Reasoning
Refinement Loops
Evolutionary Program Synthesis
Strengths

✅ Better solutions

✅ Better search

✅ Better refinement

Weaknesses

❌ Improvement stays inside task

❌ No cumulative intelligence

Master Comparison Matrix
System	Create Skills	Store Skills	Compose Skills	Compress Skills	Continual Growth	Meta-ReasoningSOAR	Partial	Yes	Partial	Partial	Partial	Partial
ACT-R	Partial	Yes	Partial	Partial	Partial	Weak
Program Synthesis	No	Weak	Weak	No	No	No
Neuro-Symbolic	Weak	Weak	Good	Weak	No	No
Hierarchical RL	Good	Good	Good	Weak	Partial	Weak
DreamCoder	Very Strong	Very Strong	Good	Very Strong	Strong	Weak
Voyager	Strong	Strong	Strong	Partial	Strong	Partial
World Models	Weak	Partial	Partial	Strong	Partial	Weak
Meta-Learning	Weak	Weak	Weak	Partial	Strong	Partial
ARC Refinement Loops	No	No	No	No	No	Weak
The Most Important Discovery

After this entire matrix, one architecture stands out:

DreamCoder

Because it explicitly does:

Task
↓
Program
↓
Compression
↓
New Primitive
↓
Library Growth


Which is astonishingly close to what we've been independently converging toward.

The Critical Question Now

If DreamCoder already exists, then:

Why hasn't DreamCoder solved ARC?

This is the question we need to investigate next.

Because the answer likely contains our opportunity.

Potential hypotheses:

Hypothesis 1

DreamCoder creates programs.

ARC may require creating abstractions.

Hypothesis 2

DreamCoder compresses solutions.

ARC may require compressing reasoning strategies.

Hypothesis 3

DreamCoder builds primitive libraries.

ARC-3 may require dynamic skill ecosystems.

Hypothesis 4

DreamCoder learns skills.

ARC may require learning when to invent skills.

Updated Novelty Landscape

After all six investigations, I would classify the research space like this:

Crowded

❌ Better search

❌ Better DSLs

❌ Better program synthesis

❌ Better refinement loops

❌ Better neuro-symbolic reasoning

Moderately Explored

⚠ Skill libraries

⚠ Continual learning

⚠ Meta-learning

⚠ Hierarchical skills

Still Wide Open

✅ Skill invention triggers

✅ Abstraction formation mechanisms

✅ Skill compression into concepts

✅ Meta-reasoning over skill creation

✅ Cumulative intelligence architectures

✅ Systems that improve themselves across tasks rather than within tasks

My Current Best Research Direction

After all six investigations, the most promising thesis is no longer:

"Build a better ARC solver."

It has evolved into:

Build an architecture that converts solved tasks into reusable abstractions, grows a skill library, and uses meta-reasoning to decide when new skills should be invented, compressed, or composed.

That is the first direction we've found that survives comparison against ARC philosophy, ARC winners, program synthesis, neuro-symbolic systems, DreamCoder, Voyager, and continual-learning architectures while still appearing meaningfully differentiated.