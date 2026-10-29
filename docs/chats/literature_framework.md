# Literature Framework

## Overview

Before reviewing papers, we need a research framework. Otherwise we'll read 100 papers and still not know what we're looking for.

---

## Phase 1: Define the Questions

I think there are actually three layers of questions.

---

## Layer A: ARC's Questions

These are the questions that François Chollet and the ARC team are trying to answer. If we don't align with these, the project may be interesting but not valuable to ARC.

### Q-A1: What is intelligence?
**ARC's answer:** Intelligence is skill-acquisition efficiency, not skill itself.

### Q-A2: How can a system learn a new skill from only a few examples?
This is the central ARC question.

### Q-A3: How can a system generalize outside training distribution?
Current AI performs well on known distributions but struggles with novel tasks.

### Q-A4: Can intelligence emerge without massive datasets?
ARC is specifically designed to minimize the advantage of brute-force training.

### Q-A5: Can an agent acquire skills during problem solving?
This becomes even more important with ARC-AGI-3's interactive environments.

---

## Layer B: Questions Current ARC Research Is Solving

These are the questions that winning teams are already attacking.

### ARC 2024 Observation

State-of-the-art jumped from about **33% to 55.5%**.

The major themes were:
- Deep-learning guided program synthesis
- Test-time training
- Search
- Neuro-symbolic methods

### ARC 2025 Observation

The defining theme was: **"Refinement Loops"**

Meaning:
```
Generate → Evaluate → Improve → Generate → Evaluate → Improve
```

Instead of one-shot reasoning.

**Research Question Being Solved:** How do we think longer?

Not: bigger model, but: better iterative reasoning.

---

## Layer C: Questions Nobody Has Solved Yet

This is where our opportunity lies.

The literature suggests several things are improving:
- ✅ Program synthesis
- ✅ Evolutionary search
- ✅ Test-time adaptation
- ✅ Refinement loops
- ✅ Neuro-symbolic reasoning

But some deeper questions remain largely unanswered:

### Candidate Open Problem 1: How Are New Skills Created?

Current systems mostly search, select, refine.

They don't truly explain: **How does a new cognitive capability emerge?**

I have not yet seen ARC work directly targeting this.

### Candidate Open Problem 2: How Should Skills Be Represented?

Current approaches use:
- Programs
- DSLs
- Latent vectors
- Reasoning traces

But there is no consensus.

### Candidate Open Problem 3: How Do Skills Compose?

Humans naturally do: `Reflection + Counting + Grouping = New Ability`

ARC tasks often require compositionality. Yet most systems still search over transformations rather than learning skill composition.

### Candidate Open Problem 4: Can Intelligence Compress Itself?

Humans don't store solutions. They store abstractions.

Question: `100 solved tasks → 5 reusable concepts`

Can AI do that? I see very little ARC work here.

### Candidate Open Problem 5: Can A System Learn Better Ways Of Reasoning?

Current systems learn:
- Answer
- Maybe: program

But not: **Reasoning Strategy**

This feels very underexplored.

---

## The Most Important Literature Questions

When reading every paper, winner, report, and solution, evaluate them against exactly these 12 questions:

### Intelligence
1. What is intelligence according to the paper?
2. What causes generalization?

### Learning
3. How are new skills acquired?
4. How are skills stored?
5. How are skills reused?

### Reasoning
6. How are hypotheses generated?
7. How are hypotheses verified?
8. How is compute allocated?

### Memory
9. Is there lifelong memory?
10. Does the system improve over time?

### AGI
11. Does the approach transfer beyond ARC?
12. If everyone adopted this idea, would AGI progress accelerate?

---

## Early Gap Analysis

Just from the technical reports, I already see a pattern:

| Year | Theme |
|------|-------|
| ARC 2024 | Search, Program Synthesis, Test-Time Training |
| ARC 2025 | Refinement Loops, Evolutionary Search, Tiny Recursive Models, Self-Improvement |
| ARC 2026 (predicted) | Agentic Learning, Interactive Exploration, Memory, Skill Acquisition |

Because ARC-AGI-3 explicitly introduces:
- Exploration
- Planning
- Memory
- Goal acquisition
- Interaction

As benchmark requirements.

---

## Research Plan Going Forward

Structure the literature review into five investigations:

### Investigation 1: ARC Philosophy
- Chollet papers
- ARC benchmark design
- What ARC considers intelligence

### Investigation 2: ARC Winners
- 2024 winners
- 2025 winners
- Architecture breakdowns

### Investigation 3: Program Synthesis Lineage
- DSL methods
- Evolutionary synthesis
- Search methods

### Investigation 4: Neuro-Symbolic Lineage
- Object-centric reasoning
- Compositional reasoning
- Symbolic abstraction

### Investigation 5: Future AGI Architectures
- Memory systems
- Skill libraries
- Continual learning
- Meta-reasoning
- Self-improving systems

---

## Current Hypothesis

After this first pass, the highest-value unsolved question is not:

> "How do we solve ARC?"

It's:

> **"How can an agent create, store, compress, and reuse skills learned while solving novel tasks?"**

That question directly aligns with:
- ARC philosophy
- ARC-AGI-3 direction
- Paper Track novelty
- AGI research value

And likely remains largely unsolved.

---

## Recommendation

Next, do Investigation 1 deeply: dissect François Chollet's intelligence theory and ARC design principles.

That's the foundation against which every future idea should be evaluated.
