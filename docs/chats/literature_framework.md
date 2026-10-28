Excellent. Before reviewing papers, we need a research framework. Otherwise we'll read 100 papers and still not know what we're looking for.

Phase 1: Define the Questions

I think there are actually three layers of questions.

Layer A: ARC's Questions

These are the questions that François Chollet and the ARC team are trying to answer. If we don't align with these, the project may be interesting but not valuable to ARC.

Q-A1

What is intelligence?

ARC's answer:

Intelligence is skill-acquisition efficiency, not skill itself.

Q-A2

How can a system learn a new skill from only a few examples?

This is the central ARC question.

Q-A3

How can a system generalize outside training distribution?

Current AI performs well on known distributions but struggles with novel tasks.

Q-A4

Can intelligence emerge without massive datasets?

ARC is specifically designed to minimize the advantage of brute-force training.

Q-A5

Can an agent acquire skills during problem solving?

This becomes even more important with ARC-AGI-3's interactive environments.

Layer B: Questions Current ARC Research Is Solving

These are the questions that winning teams are already attacking.

By reviewing 2024 and 2025 winners we can identify the dominant directions.

ARC 2024 Observation

State-of-the-art jumped from about 33% to 55.5%.

The major themes were:

Deep-learning guided program synthesis
Test-time training
Search
Neuro-symbolic methods
ARC 2025 Observation

The defining theme was:

"Refinement Loops"

Meaning:

Generate
→ Evaluate
→ Improve
→ Generate
→ Evaluate
→ Improve


instead of one-shot reasoning.

Research Question Being Solved

How do we think longer?

Not:

bigger model


but:

better iterative reasoning

Layer C: Questions Nobody Has Solved Yet

This is where our opportunity lies.

The literature suggests several things are improving:

✅ program synthesis

✅ evolutionary search

✅ test-time adaptation

✅ refinement loops

✅ neuro-symbolic reasoning

But some deeper questions remain largely unanswered.

Candidate Open Problem 1
How Are New Skills Created?

Current systems mostly:

Search
Select
Refine


They don't truly explain:

How does a new cognitive capability emerge?


I have not yet seen ARC work directly targeting this.

Candidate Open Problem 2
How Should Skills Be Represented?

Current approaches use:

programs
DSLs
latent vectors
reasoning traces

But there is no consensus.

Candidate Open Problem 3
How Do Skills Compose?

Humans naturally do:

Reflection
+
Counting
+
Grouping
=
New Ability


ARC tasks often require compositionality.

Yet most systems still search over transformations rather than learning skill composition.

Candidate Open Problem 4
Can Intelligence Compress Itself?

Humans don't store solutions.

They store abstractions.

Question:

100 solved tasks
↓
5 reusable concepts


Can AI do that?

I see very little ARC work here.

Candidate Open Problem 5
Can A System Learn Better Ways Of Reasoning?

Current systems learn:

Answer


Maybe:

Program


But not:

Reasoning Strategy


This feels very underexplored.

The Most Important Literature Questions

When reading every paper, winner, report, and solution, I think we should evaluate them against exactly these 12 questions:

Intelligence

What is intelligence according to the paper?

What causes generalization?

Learning

How are new skills acquired?

How are skills stored?

How are skills reused?

Reasoning

How are hypotheses generated?

How are hypotheses verified?

How is compute allocated?

Memory

Is there lifelong memory?

Does the system improve over time?

AGI

Does the approach transfer beyond ARC?

If everyone adopted this idea, would AGI progress accelerate?

Early Gap Analysis

Just from the technical reports, I already see a pattern.

ARC 2024 Theme
Search
Program Synthesis
Test-Time Training

ARC 2025 Theme
Refinement Loops
Evolutionary Search
Tiny Recursive Models
Self-Improvement

Likely ARC 2026 Theme

My prediction:

Agentic Learning
Interactive Exploration
Memory
Skill Acquisition


because ARC-AGI-3 explicitly introduces:

exploration
planning
memory
goal acquisition
interaction

as benchmark requirements.

Research Plan Going Forward

I would structure the literature review into five investigations:

Investigation 1

ARC philosophy

Chollet papers
ARC benchmark design
What ARC considers intelligence
Investigation 2

ARC winners

2024 winners
2025 winners
architecture breakdowns
Investigation 3

Program synthesis lineage

DSL methods
evolutionary synthesis
search methods
Investigation 4

Neuro-symbolic lineage

object-centric reasoning
compositional reasoning
symbolic abstraction
Investigation 5

Future AGI architectures

memory systems
skill libraries
continual learning
meta-reasoning
self-improving systems
My Current Hypothesis

After this first pass, the highest-value unsolved question is not:

"How do we solve ARC?"

It's:

"How can an agent create, store, compress, and reuse skills learned while solving novel tasks?"

That question directly aligns with:

ARC philosophy,
ARC-AGI-3 direction,
Paper Track novelty,
AGI research value,
and likely remains largely unsolved.

My recommendation is that next we do Investigation 1 deeply: dissect François Chollet's intelligence theory and ARC design principles. That's the foundation against which every future idea should be evaluated.