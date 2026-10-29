# Investigation 7: Skill Formation & Abstraction Formation

## Objective

This is the investigation that may actually determine whether we discover a genuinely new ARC research direction.

Everything we've done so far has been converging toward one uncomfortable realization:

- Nearly every ARC architecture explains **how to solve tasks**.
- Very few explain **how new capabilities come into existence**.

That sounds philosophical, but it's actually an engineering problem.

> Let's forget ARC for a moment. Let's ask the deepest question: **Where do new skills come from?**

Not: how do we use skills? Not: how do we store skills? But: **how are skills born?**

---

## First Discovery: Most AI Research Doesn't Model Skill Formation

Most systems assume skills already exist.

**Program Synthesis** assumes DSL primitives exist — `Rotate`, `Mirror`, `Count`, `Move` — already available.

**Neuro-Symbolic Systems** assume objects, relations, transformations — already available.

**LLMs** assume knowledge, patterns, capabilities — already encoded.

Nobody asks: **Where did Rotate come from?**

---

## Q1: What Exactly Is A Skill?

This is surprisingly difficult. Let's examine possible definitions.

| Definition | Statement | Assessment |
|-----------|-----------|------------|
| 1 | A skill is a procedure. Example: Sort Numbers. | Too narrow. |
| 2 | A skill is a reusable solution. | Better. Still incomplete. |
| 3 | A skill is a reusable transformation that reduces future reasoning cost. | **The best definition I've found.** |

Example:

- **Before learning multiplication:** 4+4+4+4+4
- **After learning multiplication:** 5×4

The skill compresses reasoning.

### First Important Insight

> **A skill is not knowledge. A skill is reasoning compression.**

This aligns surprisingly well with ARC philosophy, because intelligence is efficient skill acquisition, not knowledge acquisition.

---

## Q2: What Exactly Is An Abstraction?

Again, let's think carefully.

**Raw experiences:** Red Square, Blue Square, Green Square → **Abstraction:** Object

**Raw experiences:** Rotate Triangle, Rotate Circle, Rotate Square → **Abstraction:** Rotation

**Observation:** An abstraction removes unnecessary detail.

**Possible definition:**

> **An abstraction is a compressed representation that preserves behavior while discarding irrelevant information.**

This is extremely important, because skills seem to be built from abstractions.

### Relationship Between Skills And Abstractions

We can formulate:

```
Experiences → Abstractions → Skills → Capabilities
```

**Example:**

- **Experiences:** Mirror Shape A, Mirror Shape B, Mirror Shape C
- **Abstraction:** Reflection
- **Skill:** Apply Reflection
- **Capability:** Solve Reflection Problems

---

## Q3: How Does An Abstraction Emerge From Experience?

This is where things become interesting. Let's derive it.

Suppose agent solves:

1. Task 1: Move Red Object Right
2. Task 2: Move Blue Object Right
3. Task 3: Move Green Object Right

**Human realization:** Color doesn't matter.
**New abstraction:** Move Object Right.

This process appears to involve:

| Step | Name | Description |
|------|------|-------------|
| 1 | Pattern Collection | Gather experiences |
| 2 | Invariant Detection | Find what stays constant |
| 3 | Variable Elimination | Remove irrelevant details |
| 4 | Abstraction Formation | Create reusable concept |

### Massive Insight

> **Abstractions seem to emerge from finding invariants across experiences.**

This may become central to our future architecture.

---

## Q4: Can New Primitives Be Invented Automatically?

This is one of the most important questions.

Current ARC systems mostly have a **fixed primitive set** — examples: `Rotate`, `Move`, `Count`, `Reflect`.

But humans do something different: humans invent new concepts.

**Example:**

- **Initially:** Rotate, Scale, Translate, Reflect — separate concepts.
- **Later:** *Geometric Transformation* becomes a new primitive.

This is abstraction-driven primitive invention.

### Important Observation

DreamCoder partially moves in this direction. It compresses frequently used programs into new library components. However:

- DreamCoder's primitives emerge from **program compression**, not necessarily from **conceptual understanding**.

This distinction is crucial.

### Compression-Based Primitive Creation

Suppose we repeatedly observe `A+B+C`. System creates `X = A+B+C`. Future reasoning uses `X` instead of `A+B+C`.

- This is computationally efficient, but may not produce genuine abstractions.

### Concept-Based Primitive Creation

Alternative: System discovers `A`, `B`, `C` all express **symmetry**, and creates **Symmetry** as a new primitive.

- This is deeper.

---

## Q5: What Creates Skill Boundaries?

One of the least discussed questions. How do humans know: **"this is one skill"** instead of **"many unrelated actions"**?

**Example:** Driving contains steering, braking, acceleration, observation, prediction — yet we treat **driving** as one skill.

**Hypothesis:**

> **Skill boundaries emerge when a group of operations repeatedly co-occur toward a common goal.**

Repeated cluster: `Observe → Predict → Steer` becomes the **driving skill**.

This suggests skills may emerge as **frequently reused reasoning modules**.

---

## Q6: How Does A System Know It Needs A New Skill?

This may be the most important question of all.

- **Current systems often do:** Failure → More Search
- **Humans often do:** Failure → Need New Concept

Huge difference.

### Example

Imagine solving Task 1, Task 2, Task 3 using extensive search. Eventually the agent notices:

> **Same reasoning pattern repeatedly appears.**

At that moment: `Search Cost > Skill Cost`. New skill should be created.

### Proposed Principle

> **A new skill should be invented when: cost of repeated reasoning > cost of abstraction.**

This is one of the strongest hypotheses we've found so far.

---

## Emerging Theory Of Skill Formation

Combining everything:

| Stage | Name | Output |
|-------|------|--------|
| 1 | Experience | Task, Task, Task |
| 2 | Pattern Discovery | Common Structure |
| 3 | Invariant Detection | What Never Changes? |
| 4 | Abstraction Creation | New Concept |
| 5 | Skill Formation | Executable Concept |
| 6 | Skill Library | Reusable Capability |

---

## The Most Important Gap We Found

After all seven investigations, the biggest gap in ARC research is **not**:

- ❌ Search
- ❌ Program Synthesis
- ❌ Neuro-Symbolic Reasoning

**The gap is:**

> **How can a system autonomously detect recurring reasoning structures, convert them into abstractions, and promote those abstractions into reusable skills?**

---

## New Research Hypothesis (Version 1)

This is the first hypothesis we'd actually consider paper-worthy:

> **Intelligence grows when an agent continuously converts expensive reasoning traces into reusable abstractions, and reusable abstractions into executable skills.**

In architecture form:

```
Task
  ↓
Reasoning Trace
  ↓
Invariant Detection
  ↓
Abstraction Generator
  ↓
Primitive Inventor
  ↓
Skill Library
  ↓
Future Tasks
```

Notice something important:

**None of the major ARC paradigms we've studied explicitly center the Invariant Detection → Abstraction Generator → Primitive Inventor pipeline.**

They focus on:

- search,
- programs,
- refinement,
- neuro-symbolic reasoning,
- memory,

…but **not** on the mechanism by which entirely new abstractions are born.

And that is the strongest lead we've uncovered so far.
