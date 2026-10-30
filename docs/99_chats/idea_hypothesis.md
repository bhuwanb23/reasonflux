# Idea Hypothesis

## Overview

This document explores how to approach ARC Prize 2026 Paper Track by understanding what ARC researchers want, identifying unsolved gaps, and generating ideas specifically targeting those gaps.

---

## The Right Approach

Most teams will start with an idea and then try to fit it into ARC.

**We should do the opposite:**
1. Understand what ARC researchers actually want
2. Understand what the paper judges reward
3. Identify unsolved gaps
4. Generate ideas specifically targeting those gaps

That's how you maximize both:
- ARC score
- Paper Track score
- Research impact

---

## Step 1: What ARC Is Actually Trying To Solve

The core ARC philosophy is:

> **Intelligence is the efficient acquisition of new skills.**

NOT:
- Memorization
- Bigger models
- More training data

ARC wants systems that can see a new task and figure it out with very few examples.

Therefore any project should improve one or more of:
- Generalization
- Reasoning
- Adaptation
- Skill Acquisition
- Transfer Learning
- Compositionality
- Abstraction

---

## Step 2: Constraints From The Paper Judging Rubric

The official categories are:
- Accuracy
- Universality
- Progress
- Theory
- Completeness
- Novelty

Let's convert these into engineering requirements:

### Constraint 1: Accuracy
Must actually work. Not just philosophy.

Need:
- Code
- Experiments
- Leaderboard score

### Constraint 2: Universality
Huge. Idea should work beyond ARC.

- **Bad:** ARC-specific tricks
- **Good:** General reasoning framework

### Constraint 3: Progress
Most important.

Ask: If everyone copied this idea, would AGI research move forward?

If answer is yes: good paper.

### Constraint 4: Theory
Need a WHY.

Most Kagglers write: "Here is my model."

Judges want:
- Why does learning happen?
- Why does transfer happen?
- Why does abstraction emerge?

### Constraint 5: Novelty
This is where most submissions fail.

Need something genuinely different.

---

## Step 3: Additional Hidden Constraints

Not explicitly written, but important:

- **Constraint 6: Reproducibility** — Must be open source
- **Constraint 7: Limited Compute** — ARC intentionally favors intelligence over scale
  - 40B smarter model is often more interesting than 600B brute force model
- **Constraint 8: Test-Time Adaptation** — Key ARC theme. Can system improve after seeing a task?
- **Constraint 9: Human-Like Learning** — ARC is fundamentally inspired by human cognitive flexibility

---

## Step 4: Things Everyone Else Will Likely Do

Expect many teams to build:

### Category A: LLM + Prompting
```
Task → Prompt → Solution
```

### Category B: LLM + Search
```
Task → LLM → Search → Answer
```

### Category C: Program Synthesis
```
Task → Generate DSL → Execute
```

### Category D: Test-Time Compute
```
Task → Tree Search → Best Answer
```

These are likely crowded areas.

---

## Step 5: Research Gaps I Think ARC Still Has

### Gap #1: How New Skills Form
Current systems retrieve, search, reason. But: "How does a new skill get created?" is largely unsolved.

### Gap #2: Transfer Of Skills
Humans solve: `Skill A + Skill B = New Skill`. LLMs struggle.

### Gap #3: Reasoning Cost Allocation
Humans don't spend equal effort on every problem. AI systems mostly do. A frontier topic.

### Gap #4: Reasoning Compression
After solving 100 tasks: Can intelligence get smaller? Very unexplored.

### Gap #5: Meta-Learning of Reasoning Strategies
Not: learning answers. But: **learning how to reason**. Very important.

---

## Step 6: High-Potential Research Directions

### Idea 1: Dynamic Skill Creation Engine
**Novelty: 9/10**

**Concept:** Instead of retrieve skill, system can **invent** new skill.

**Workflow:**
```
Task → Failure → Analyze failure → Create skill → Store skill → Reuse later
```

**Research question:** How does a system autonomously manufacture new cognitive tools?

Very ARC-aligned.

### Idea 2: Cognitive Genome
**Novelty: 10/10**

Represent intelligence as tiny primitives.

**Example primitives:** `compare`, `rotate`, `group`, `mirror`, `repeat`, `count`

Each task becomes temporary genome assembled from primitives.

**Paper thesis:** Intelligence emerges through assembly rather than storage.

Extremely aligned with ARC.

### Idea 3: Adaptive Compute Router
**Novelty: 8/10**

Current systems: easy task = 100 tokens, hard task = 100 tokens

Humans: easy = 2 seconds, hard = 2 hours

System learns: **How much thinking is needed?** before solving.

Could transfer beyond ARC.

### Idea 4: Self-Evolving Reasoning Graph
**Novelty: 9.5/10**

Instead of weights learning, **reasoning structure learns**.

Nodes + Strategies + Tools change over time.

Think: Neural Architecture Search for reasoning.

### Idea 5 (My Favorite): Skill Distillation From Experience
**Novelty: 9.5/10**

Imagine:
- 100 ARC tasks → System discovers 7 universal skills → Compress into 7 reusable abstractions

**Research question:** Can intelligence become more efficient as experience accumulates?

This is extremely close to how humans learn.

---

## Step 7: My Ranking

| Idea | Novelty | Research Impact | ARC Fit |
|------|---------|-----------------|---------|
| Dynamic Skill Creation | 9 | 10 | 10 |
| Cognitive Genome | 10 | 9 | 10 |
| Skill Distillation | 9.5 | 10 | 10 |
| Self-Evolving Graph | 9.5 | 9 | 9 |
| Adaptive Compute Router | 8 | 8 | 8 |

---

## What I Would Personally Explore

A combination of:
1. **Dynamic Skill Creation**
2. **Skill Distillation**
3. **Cognitive Genome**

### Core Hypothesis

> Intelligence is not stored in parameters. Intelligence emerges when an agent can create, compress, and recombine reusable cognitive skills.

That is a strong, non-standard AGI hypothesis, directly relevant to ARC Prize 2026, likely useful beyond ARC, explains a path to generalization, and gives plenty of material for a high-scoring paper on Universality, Progress, Theory, and Novelty.

---

## Next Step

Research-landscape analysis to identify which of these ideas are truly novel versus existing work in:
- ARC winners (2024-2026)
- DeepMind
- Anthropic
- OpenAI
- Test-time compute papers
- Neuro-symbolic research
- Program synthesis literature

Then we can narrow it down to 2-3 ideas with the highest chance of being both novel and implementable.
