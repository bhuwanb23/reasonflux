# Investigation 1: ARC Philosophy

## Objective

Yes, we completely get the objective.

We're not trying to find a clever ARC trick. We're trying to understand the foundational theory behind ARC, because if we eventually propose a new architecture, it must be aligned with what ARC considers intelligence — otherwise even a high-scoring system may not be viewed as meaningful progress.

So for Investigation 1, let's ignore implementations and focus on the philosophy from François Chollet's *On the Measure of Intelligence*, ARC design principles, and ARC Prize technical reports.

---

## Executive Summary

After studying the ARC philosophy, the most important realization is:

> **ARC is not a benchmark for solving puzzles. ARC is a benchmark for measuring how efficiently a system can create new knowledge from limited experience.**

This sounds subtle, but it changes everything.

- **Most AI research asks:** Can the system solve task X?
- **ARC asks:** How efficiently can the system learn task X when task X has never existed before?

---

## Part 1: Chollet's Criticism of Modern AI

The entire ARC project starts from a criticism. According to François Chollet, most AI benchmarks confuse **Skill** with **Intelligence**.

### Example

- **System A** needs 1 million examples to learn chess.
- **System B** needs 10 examples to learn chess.

Traditional benchmarks:
- Both can play chess.
- Therefore: **Equal.**

ARC view:
- System B is much more intelligent, because it learns faster.

This is the first fundamental principle.

---

## Principle #1: Intelligence ≠ Skill

This may be the most important sentence in all ARC literature.

- Intelligence is **not**: what you know.
- Intelligence **is**: how efficiently you acquire new knowledge.

## Principle #2: Intelligence Depends On Generalization

A truly intelligent system should solve problems that are:

- Not anticipated
- Not trained
- Not memorized

Current AI succeeds mostly because:

```
Training Distribution ≈ Test Distribution
```

ARC intentionally breaks this assumption.

## Principle #3: Experience Is Not Intelligence

This is another deep idea.

- **Human:** 100 examples
- **AI:** 100 billion examples

If both solve the task: **same skill, different intelligence** — according to ARC theory.

---

## Chollet's Intelligence Formula

A simplified interpretation of the paper:

**Intelligence depends on:** Skill Acquisition Efficiency

**relative to:**
- Prior Knowledge
- Experience
- Task Difficulty
- Generalization Difficulty

---

## Why ARC Uses Grids

Many people misunderstand this.

- The grids are **not** the point.
- The grids are merely a **vehicle**.

ARC could have used:
- shapes
- sounds
- robots
- games

The important part is: **novel abstraction discovery**.

---

## Core Knowledge Theory

This is hugely important. ARC does **NOT** assume zero prior knowledge. Instead it assumes **Human Core Knowledge**.

Examples:

| Domain | Innate Priors |
|--------|---------------|
| Objects | Objects exist, objectness |
| Space | left, right, inside, outside |
| Counting | 1, 2, 3, ... |
| Geometry | rotation, reflection, symmetry |
| Causality | transformation, action, effect |

ARC assumes these innate priors. Why? Because humans also start with them.

---

## Massive Insights

### Massive Insight #1: ARC Is Not Testing Knowledge

It's testing **knowledge creation**. This distinction becomes crucial for our future idea.

### Massive Insight #2: ARC Rewards Abstraction

Consider:
- Red square
- Blue square
- Green square

Humans quickly abstract: **colored object**.

ARC tasks often require this leap. Systems that cannot form abstractions fail.

### Massive Insight #3: ARC Rewards Composition

Humans don't learn every skill separately. They do:

```
Rotation + Counting + Grouping = New Solution
```

ARC tasks are deliberately compositional.

### Massive Insight #4: ARC Is About Skill Acquisition

Notice something strange.

- ARC never asks: **Can you remember?**
- ARC asks: **Can you figure it out?**

This is a completely different benchmark philosophy.

---

## Why ARC-1 Was Not Enough

According to the ARC reports, researchers eventually learned ways to exploit ARC-AGI-1. This led to:

- Program Search
- DSL Search
- Benchmark-specific tricks
- Overfitting

The benchmark started rewarding **preparedness** rather than **adaptation**.

## Why ARC-2 Exists

ARC-2 increases emphasis on **novel compositional reasoning** and reduces exploitability.

## Why ARC-3 Exists

This is where things become extremely interesting. The ARC team concluded:

> **Static puzzle solving is insufficient.**

Intelligence also requires:
- Exploration
- Planning
- Memory
- Goal Discovery
- Interaction

---

## The Hidden ARC Roadmap

After reading everything, ARC's trajectory looks like:

| Version | Question |
|---------|----------|
| ARC-1 | Can you infer rules? |
| ARC-2 | Can you reason compositionally? |
| ARC-3 | Can you learn through interaction? |
| ARC-4 (speculative) | Can you continually acquire new skills? |

*(ARC-4 is my interpretation, not an official ARC statement.)*

---

## What ARC Researchers Currently Believe Is Working

From the 2024 and 2025 reports, successful themes:

- Test-Time Learning
- Program Synthesis
- Neuro-Symbolic Reasoning
- Refinement Loops
- Recursive Search

## What ARC Researchers Believe Is Still Missing

Reading between the lines of the reports, current systems still lack:

- Genuine Generalization
- Efficient Skill Acquisition
- Open-Ended Adaptation
- Continual Learning
- Interactive Learning

---

## The Most Important Research Gap

After this investigation, the single biggest unresolved question is:

> **How does an intelligent system transform a novel experience into a reusable skill?**

Notice how this differs from "How do we solve ARC?" — instead: **How do we create new capabilities?**

---

## Research Questions We Should Carry Forward

These are now our canonical questions.

| ID | Question |
|----|----------|
| RQ1 | How are new skills formed? |
| RQ2 | What is the smallest unit of a skill? |
| RQ3 | How should skills be represented? |
| RQ4 | How are skills composed? |
| RQ5 | How are skills compressed into abstractions? |
| RQ6 | How does an agent know when it needs a new skill? |
| RQ7 | How can reasoning itself improve? |
| RQ8 | How can learning continue after deployment? |

---

## Final Conclusion of Investigation 1

The deepest takeaway from *On the Measure of Intelligence* and the ARC philosophy is:

> **ARC is fundamentally a benchmark about the creation and acquisition of abstractions, not the retrieval of knowledge.**

That means our future project should probably not be framed as:

- **Better Solver**

but rather:

- **Better Skill Acquisition Mechanism**

because that is much closer to the core scientific question ARC was created to investigate.

From a research perspective, the strongest path is likely somewhere in the intersection of:

- Skill Creation
- Skill Composition
- Skill Compression
- Continual Adaptation

since those themes emerge directly from ARC's definition of intelligence rather than from any specific benchmark implementation.
