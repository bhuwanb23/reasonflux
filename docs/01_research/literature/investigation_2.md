# Investigation 2: ARC Winners (2024–2025)

## Objective

Excellent. Now we stop thinking like researchers reading ARC and start thinking like investigators studying the evolution of ideas.

For Investigation 2, the goal is **not**:

> "Who won?"

The goal is:

> "What ideas actually moved the frontier, what trends emerged, what failed, and where is the remaining gap?"

That's the information we need to find a novel research direction.

---

## Executive Summary

After analyzing the winner reports and technical reports, there is a very clear evolution:

| Year | Theme |
|------|-------|
| 2024 | Program Discovery |
| 2025 | Refinement Loops |
| 2026 | Interactive Learning (ARC-3) |
| Future | Skill Acquisition Systems |

This is the biggest insight from the winner analysis.

---

## Part 1: ARC Prize 2024

The most important number:

> **State-of-the-art moved from roughly 33% to 55.5%.**

That is an enormous jump. Meaning: **something fundamental changed**.

### What Actually Won In 2024?

Top ideas were **not**:
- Bigger LLMs
- More Data
- More Parameters

Instead:
- Program Synthesis
- Test-Time Training
- Neural Guidance
- Search

### Winning Theme #1: Program Synthesis

The system does not directly predict the answer. Instead:

```
Input
  ↓
Infer Program
  ↓
Execute Program
  ↓
Output
```

Think:
- **Learn rule** instead of **predict answer**

This aligns much better with ARC philosophy.

**Why It Worked:** ARC tasks often contain **hidden algorithm**, not statistical pattern. Humans solve ARC by discovering rules. Program synthesis mimics that process.

### Winning Theme #2: Neural-Guided Search

- Pure symbolic search explodes.
- Pure neural systems hallucinate.
- The best systems used: **neural prior + symbolic search** to guide exploration.

### Winning Theme #3: Test-Time Training

This was one of the biggest breakthroughs.

Instead of:

```
Train → Deploy → Done
```

they did:

```
See Task → Adapt → Solve
```

This was recognized in the 2024 paper awards.

### Important Observation

The winning papers were:

1. *Combining Induction and Transduction for Abstract Reasoning*
2. *The Surprising Effectiveness of Test-Time Training for Abstract Reasoning*
3. *Searching Latent Program Spaces*

Notice the pattern. All three focus on **learning during solving** rather than **learning before solving**.

### What 2024 Taught The Community

By end of 2024, the community learned:

- **More Parameters ≠ More Intelligence**
- ARC could be improved through:
  - Better Search
  - Better Adaptation
  - Better Reasoning

---

## Part 2: ARC Prize 2025

Then ARC-AGI-2 arrived. Everything changed.

### Critical Observation

Best score dropped dramatically. Top private score: **~24%**.

Why? ARC-AGI-2 was intentionally harder. Designed to resist:

- Memorization
- ARC-specific tricks
- Dataset exploits

### Defining Theme Of 2025

The ARC report explicitly identifies **refinement loops** as the dominant theme.

**What is a refinement loop?** Instead of one attempt, systems do:

```
Generate → Evaluate → Modify → Generate → Evaluate
```

This is closer to **human thinking** than a **single forward pass**.

### Major Winning Idea #1: Recursive Reasoning

Paper winner: *Less is More: Recursive Reasoning with Tiny Networks.*

Key message:

```
Small Network + Recursive Thinking > Large Network
```

for many ARC settings.

**Why This Matters:** This is an attack on scaling laws. ARC researchers increasingly believe: **thinking better > thinking bigger**.

### Major Winning Idea #2: Evolutionary Program Synthesis

Paper: *Self-Improving Language Models for Evolutionary Program Synthesis.*

Idea:

```
Generate Programs → Evaluate Fitness → Mutate → Improve
```

Very similar to biological evolution.

### Major Winning Idea #3: Self-Improvement

Huge trend. Many top papers included:

- Self-Refinement
- Self-Improvement
- Iterative Optimization

### Hidden Insight

- Nobody really won by: **knowledge**
- Everyone won by: **optimization process**

---

## Architecture Breakdown

Let's classify everything.

| Family | Representation | Strengths | Weaknesses |
|--------|---------------|-----------|------------|
| A: Program Synthesis | Program (search over programs) | Interpretable, logical | Search cost |
| B: Neuro-Symbolic | Objects, rules, relations — neural for guidance, symbolic for verification | Strong generalization | DSL limitations |
| C: Recursive Models | Repeated thinking (not larger networks) | Efficient | Limited world model |
| D: Evolutionary Search | Population of solutions (evolve over time) | Open-ended exploration | Compute intensive |

---

## The Most Important Meta-Trend

This is perhaps the most valuable insight:

| Year | Focus |
|------|-------|
| 2024 | Find Better Program |
| 2025 | Find Better Refinement Process |
| 2026 | Find Better Learning Process (ARC-3 direction) |

---

## What Nobody Is Solving Yet

After reading the winners, a key observation:

- Every top approach focuses on **solving current task**.
- Even self-improving systems mostly do **improve inside task**.
- But almost nobody addresses: **how does knowledge survive after task completion?**

This is extremely important. Humans do:

```
Solve Problem → Extract Principle → Reuse Later
```

ARC systems rarely do this.

---

## The Largest Research Gap Revealed By Winners

Current winner architectures **can**:

- ✅ Search
- ✅ Refine
- ✅ Adapt
- ✅ Verify
- ✅ Generate Programs
- ✅ Evolve Solutions

But they generally **cannot**:

- ❌ Create reusable skills
- ❌ Build abstractions from experience
- ❌ Compress lessons into concepts
- ❌ Accumulate intelligence across tasks
- ❌ Grow a cognitive repertoire

---

## Winner Analysis Conclusion

If we had to summarize 2024-2025 ARC progress in one sentence:

> **ARC research has become very good at improving solutions, but is still weak at improving the solver itself.**

That distinction is critical.

Current systems mostly learn: **task solution**.

The next frontier appears to be:

- Skill Formation
- Skill Memory
- Skill Composition
- Continual Capability Growth

…which aligns extremely closely with the ARC definition of intelligence and the direction implied by ARC-AGI-3.

---

## Refined Research Questions After Investigation 2

We should now focus the rest of the literature review around:

1. How do humans convert solved tasks into reusable skills?
2. How can an agent discover that a new skill is needed?
3. How should skills be represented?
4. How should skills be composed?
5. How can skills survive across tasks?
6. Can intelligence itself become cumulative?

Those questions appear much less explored than search, refinement, program synthesis, or neuro-symbolic reasoning, and therefore have the highest potential for a novel ARC Prize paper.
