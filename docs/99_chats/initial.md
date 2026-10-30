# ARC Prize 2026 — Paper Track Deep-Dive

## Overview

After analyzing the competition, one thing is important:

> **This is NOT a leaderboard competition.**

The Paper Track is essentially a research-paper competition attached to your ARC-AGI-2 or ARC-AGI-3 submission. The judges care more about whether your idea pushes AGI research forward than whether you get the highest score.

---

## 1. What is ARC Prize 2026?

The ARC Prize 2026 is a **$2M AGI-focused competition** with three tracks:

- **ARC-AGI-2** — Static reasoning
- **ARC-AGI-3** — Interactive reasoning
- **Paper Prize / Paper Track** — Research writeup of your approach

The benchmark is based on ARC (Abstraction and Reasoning Corpus), created by François Chollet, intended to measure general intelligence and adaptation rather than memorization.

---

## 2. What Exactly Is the Paper Track?

You submit:
- A Kaggle Writeup (your paper)
- Linked ARC-AGI-2 or ARC-AGI-3 submission
- Optional notebooks
- Project links
- Media gallery resources

The paper must document the actual method used in your ARC submission.

The judges want:
- Your reasoning
- Your architecture
- Why it works
- Evidence
- Novel ideas

**Not just source code.**

---

## 3. Prize Pool

Paper Track total:

| Prize | Amount |
|-------|--------|
| 1st | $50,000 |
| 2nd | $20,000 |
| 3rd | $5,000 |
| Outstanding Papers Pool | $375,000 |
| Additional Top Paper Awards | Up to $75,000 |

**Total: $450,000 paper-focused awards.**

---

## 4. The Most Important Hidden Insight

Many people misunderstand this competition.

You do NOT necessarily need:
- SOTA score
- Top leaderboard rank
- 80%+ ARC score

Your paper can still win if:
- It introduces a genuinely new concept
- It advances AGI research
- It explains theory very well

Because the judging rubric is broader than leaderboard accuracy.

---

## 5. How Papers Are Evaluated

Each category is scored **0–5**.

### Accuracy
How well your linked submission performs. Judges use your actual ARC score.

### Universality
Can your method generalize beyond ARC?

- **Bad:** handcrafted ARC rules
- **Good:** general reasoning framework, skill acquisition architecture, agentic learning system

### Progress
Probably the most valuable category.

Question: Does this work move humanity closer to solving ARC-AGI?

Even if performance is mediocre.

### Theory
Huge importance.

Most competitors explain **HOW**. Judges want **WHY**:
- Why does the system learn?
- Why does it generalize?
- Why should it work on unseen tasks?

### Completeness
Must explain:
- Architecture
- Training
- Search
- Evaluation
- Limitations

Not just a vague idea.

### Novelty
Judges will compare against:
- LLM approaches
- Program synthesis
- Neuro-symbolic systems
- Search-based ARC solvers

Novel combinations matter.

---

## 6. Kaggle Submission Requirements

| Required | Optional |
|----------|----------|
| Kaggle Writeup | Public Notebook |
| Media Gallery | |
| Project Link | |

**Also Required:** Paper must be linked to an ARC-AGI-2 or ARC-AGI-3 solution.

---

## 7. Open Source Requirement

The entire ARC Prize ecosystem strongly emphasizes open source.

To receive prizes:
- Methods must be open
- Code must be reproducible
- Permissive licensing expected (MIT-0, CC0, etc.)

---

## 8. Timeline

| Event | Date |
|-------|------|
| Competition Start | March 25, 2026 |
| Paper Deadline | November 9, 2026 |
| Results | December 2026 |

Deadlines are UTC.

---

## 9. What Makes a Winning Paper?

After reading the rubric, a strong paper generally contains:

### Abstract
One paragraph: contribution, novelty, results.

### Introduction
Explain: ARC, AGI importance, problem statement.

### Related Work
Compare against: LLMs, Search, DSL systems, Program synthesis.

### Method
Most important section. Needs: diagrams, architecture, algorithms, reasoning cycle.

### Results
Show: Kaggle score, experiments, ablations.

### Theory
**This is where winners separate themselves.** Explain:
- Why learning occurs
- Why adaptation occurs
- Why generalization occurs

---

## 10. What Kind of Ideas Usually Win?

Looking at ARC history and judging philosophy:

**Strong:**
- **Neuro-symbolic systems** — Combining transformer, program synthesis, search
- **Test-time learning** — System learns during evaluation
- **Skill acquisition networks** — Build reusable skills
- **Agentic exploration** — Try → Observe → Update → Retry
- **World-model approaches** — Learn internal environment representations

These align closely with ARC's philosophy of intelligence.

---

## 11. What Will Probably Lose?

- **Pure LLM prompting** — "Let's ask GPT." Not novel.
- **Massive memorization** — ARC explicitly tries to prevent this.
- **Hardcoded rules** — Generalization score suffers.
- **Benchmark overfitting** — Universality score suffers.

---

## 12. Strategic Analysis

If I were entering today, I would NOT optimize for leaderboard first.

I would optimize for:
- **40%** Score
- **60%** Research contribution

Because the paper rubric enables high rewards even when the code is not first place.

A paper such as *"Hierarchical Skill Library with Online Skill Composition"* could potentially outperform a paper describing a marginally higher-scoring solver but providing little new insight.

---

## 13. Biggest Opportunity (My Assessment)

The highest-upside area is probably:

**ARC + Test-Time Compute**

Examples:
- DeepSeek-style reasoning
- MCTS
- Program synthesis
- Skill discovery
- Verifier loops
- Self-improvement during inference

**Why?**

Because ARC is fundamentally testing: *Can a system learn a new skill from very little data?*

That's exactly where current frontier models remain weak.

---

## Final Takeaway

This competition is less of a Kaggle leaderboard contest and more of an **AGI research contest disguised as a Kaggle competition**.

To maximize winning chances:

1. Build a real ARC-AGI-2 or ARC-AGI-3 submission
2. Open-source everything
3. Focus on a genuinely new reasoning architecture
4. Write a strong theory section explaining why it works
5. Demonstrate generalization, not memorization
6. **Treat the paper as the main product and the leaderboard score as supporting evidence**

Given your recent interest in running frontier reasoning models on limited hardware and AGI-style architectures, this Paper Track is actually much more aligned with proposing a novel reasoning system architecture than competing purely on raw compute. A clever test-time reasoning framework can be substantially more competitive here than simply scaling parameters.
