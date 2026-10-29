# ARC Core Ideology

## Overview

This document explores what ARC (Abstraction and Reasoning Corpus) actually measures, why ARC-1 got "partially solved", why ARC-2 and ARC-3 were created, what existing approaches fail at, and what research gap remains.

---

## Phase 0: What Are We Actually Trying To Solve?

The first mistake many people make is thinking:

> ARC = Puzzle Solving

It is not.

**ARC is trying to measure:** Human-like General Intelligence

Specifically:
- Ability to learn a new skill from very little experience
- According to François Chollet, the creator of ARC

---

## ARC's Core Philosophy

Most AI benchmarks test: **What do you know?**

ARC tests: **Can you learn something new?**

### Traditional Benchmarks
- Examples: Math, Coding, QA, Translation
- Models can succeed by:
  - Memorization
  - Pattern matching
  - Huge pretraining

### ARC Approach
Instead:
1. 2-5 examples
2. Discover Rule
3. Apply Rule

**No internet. No retrieval. No huge dataset for that specific task.**

You must infer the underlying abstraction.

---

## ARC's Definition of Intelligence

A very important concept. ARC assumes intelligence is:

**Skill Acquisition Efficiency.**

```
Intelligence = How quickly you learn something unseen
```

NOT:
```
How much information you already know
```

---

## Why ARC Exists

ARC researchers believe current AI is mismeasured.

### Current benchmarks reward:
- Scale
- Data
- Compute
- Memorization

### ARC attempts to reward:
- Abstraction
- Adaptation
- Reasoning
- Compositionality
- Generalization

---

## ARC-AGI Evolution

### ARC-AGI-1
- Original benchmark
- Grid puzzles
- Example: Input → Find Rule → Output
- Researchers spent years improving results
- **Problem:** Researchers started discovering ARC-specific tricks instead of broader intelligence (benchmark overfitting)

### ARC-AGI-2
- Created to make memorization and handcrafted solutions harder
- Focus: Novel Compositional Reasoning
- Questions became harder
- More combinations, more abstraction, less pattern memorization

### ARC-AGI-3
- Even bigger shift
- Moves toward: **Interactive Intelligence**
- Instead of: Static Pattern Recognition
- Agents must interact with environments and learn through exploration

---

## Why ARC-3 Is Extremely Important

This reveals where ARC researchers think AGI research should go.

They believe:
> Solve Static Problems is insufficient.

Instead:
1. Observe
2. Act
3. Learn
4. Adapt

...is closer to intelligence.

---

## What ARC Researchers Want

After reading the competition goals and philosophy, they want systems that can:

- **Learn New Skills** — Not just recall
- **Transfer Skills** — Use old knowledge in new situations
- **Create Abstractions** — Identify hidden concepts
- **Adapt** — Improve while solving
- **Reason** — Multi-step discovery
- **Generalize** — Operate outside training distribution

---

## What Current Frontier Models Are Missing

Large models are good at:
- Language
- Code
- Knowledge

But weak at:
- True Out-of-Distribution Generalization
- Skill Creation
- Rapid Adaptation
- Abstract Rule Discovery
- Learning During Inference

These are areas ARC explicitly targets.

---

## Existing Solution Categories

Nearly every ARC solution belongs to one of these families:

### Family 1: Program Synthesis
- **Idea:** Find Rule → Convert Rule Into Program → Execute Program
- **Advantages:** Interpretable, Logical
- **Weaknesses:** Search explosion, doesn't scale well

### Family 2: DSL Search
- **Idea:** Special Language + Search
- **Example:** `rotate`, `mirror`, `fill`, `move`, `group` — search over combinations
- **Weakness:** Eventually becomes handcrafted

### Family 3: Neural Models
- **Idea:** Grid → Transformer → Grid
- **Advantages:** General
- **Weaknesses:** Poor abstraction, poor sample efficiency

### Family 4: Neuro-Symbolic
- **Most successful modern direction**
- **Idea:** Neural + Search + Symbolic Reasoning
- Gets benefits of both worlds

### Family 5: Test-Time Compute
- **Recently very popular**
- Think Longer → Generate Hypothesis → Verify → Refine
- Much closer to DeepSeek-style reasoning

---

## What Is Still Missing?

A lot of teams can solve tasks. Far fewer explain: **How intelligence develops.**

This appears to be the largest open research gap.

---

## The Research Problems Worth Exploring

Six fundamental AGI questions:

### PS-1: How Does A System Create New Skills?
Current systems mostly retrieve, reuse, search. Humans: **invent**.

### PS-2: How Should Skills Be Stored?
Current models: weights. Humans: abstractions, concepts, procedures.

### PS-3: How Should Skills Combine?
Humans do: `Skill A + Skill B = New Ability`. Current AI struggles.

### PS-4: How Does Reasoning Become More Efficient?
Humans: Practice → Compression → Fast Intuition. AI rarely does this.

### PS-5: How Should Compute Be Allocated?
Humans don't think equally hard about everything. Most AI still does.

### PS-6: How Does A System Learn To Reason Better?
Not: learn answers. But: **learn reasoning strategies**. This may be the deepest problem.

---

## Current Ranking of Research Opportunities

| Problem | Novelty | ARC Value |
|---------|---------|-----------|
| Skill Creation | 10/10 | 10/10 |
| Skill Composition | 10/10 | 10/10 |
| Reasoning Compression | 9.5/10 | 10/10 |
| Meta-Reasoning | 9.5/10 | 10/10 |
| Compute Allocation | 8.5/10 | 8/10 |
| Memory Design | 9/10 | 9/10 |

---

## Summary

### We now understand:

**ARC's Goal:**
> Measure skill acquisition efficiency rather than memorization.

**Paper Track's Goal:**
> Advance understanding of how to achieve strong ARC performance, not just obtain a high score.

**What Judges Reward:**
- Accuracy
- Universality
- Progress
- Theory
- Novelty
- Completeness

**Crowded Research Areas:**
- Pure LLMs
- Program synthesis
- Standard search
- Test-time compute only

**High-Value Open Problems:**
- Skill creation
- Skill composition
- Skill memory
- Reasoning compression
- Meta-reasoning
- Adaptive compute

### Most Promising Direction

A system that can:
1. Create Skills
2. Store Skills
3. Compose Skills
4. Compress Skills
5. Improve Future Reasoning

Because that directly attacks the central ARC question:

> **How can an agent continually acquire new capabilities from limited experience?**

---

## Next Step

Deep literature and ARC-winning-solution analysis, including:
- ARC Prize 2024 winners
- ARC Prize 2025 winners
- ARC-AGI-2 leading approaches
- Neuro-symbolic ARC papers
- Program synthesis systems
- DeepMind/OpenAI/Anthropic work on test-time learning
- Existing skill-learning and meta-reasoning architectures

Then we can identify exactly which of the six problem statements are genuinely unsolved and where a novel paper has the highest chance of standing out.
