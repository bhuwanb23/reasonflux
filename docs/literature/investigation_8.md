# Investigation 8: Human Learning & Cognitive Science

## Objective

This investigation is probably the most undervalued one for ARC.

Up until now, we've mostly analyzed what AI researchers built. Now we need to analyze what **evolution** built.

Because ARC itself is fundamentally inspired by **human intelligence**, not benchmark optimization. François Chollet's definition of intelligence is heavily grounded in human skill acquisition and generalization rather than task performance.

### The Core Question

Instead of asking:

> "How do AI systems solve ARC?"

We ask:

> **"How do humans become capable of solving ARC?"**

This sounds similar. It is not. One studies **solutions**. The other studies **capability formation**.

---

## The First Big Discovery: Humans Do Not Learn Like Current AI

**Most modern AI:**

```
Data → Training → Weights → Capability
```

**Humans:**

```
Experience → Abstraction → Skill → Transfer → New Capability
```

Notice the extra layers. This difference appears repeatedly across cognitive science.

---

## Area 1: Concept Formation

This may be the most important topic.

### What Is A Concept?

Humans never store raw experiences.

**Example:** A child sees Dog A, Dog B, Dog C, Dog D. They do not memorize every dog. Instead they create **DOG** as a concept.

### Cognitive Science View

Concepts emerge through:

```
Similarity + Differences + Repeated Exposure
```

Humans appear to search for: **"What stays invariant?"** across experiences.

### Connection To Investigation 7

We discovered: `Abstraction = Invariant Detection`.

This aligns remarkably well with concept formation research.

### Emerging Principle

> **A concept may simply be a stable invariant extracted from multiple experiences.**

---

## Area 2: Chunking

This is one of the most important discoveries in cognitive psychology.

### What Is Chunking?

Suppose a **novice** sees: A, B, C, D, E — five independent elements.

An **expert** sees: ABCDE — one chunk.

**Example:** Chess masters. Research repeatedly shows experts do not analyze every piece separately. They recognize patterns. They compress:

```
Many Elements → Single Unit
```

### Why This Matters

Chunking is basically **compression of reasoning**.

This sounds very similar to what we observed in:

- Skill formation
- Primitive invention
- DreamCoder-style compression

### New Hypothesis

> **Skills may emerge when frequently co-occurring reasoning operations become a chunk.**

**Example:** `Detect Object → Count Object → Move Object` becomes the **object tracking skill**.

---

## Area 3: Transfer Learning In Humans

This is where ARC becomes extremely relevant.

Humans are extraordinary at transfer.

**Example:**

- Learn: ride bicycle
- Later: ride motorcycle becomes easier

Why? Humans transfer **balance**, not **bicycle**.

This is a huge insight. **Humans transfer abstractions, not experiences.**

- Current AI often transfers: **patterns**
- Humans transfer: **underlying principles**

### ARC Connection

ARC tasks frequently require **transfer principle** instead of **transfer example**. This is exactly why ARC is difficult.

---

## Area 4: Analogical Reasoning

This is one of the strongest opportunities for us.

Humans constantly reason by analogy.

**Example:**

- Solar System understood as planetary orbit
- Then: Atom understood as "mini solar system" *(not scientifically accurate today, but cognitively illustrative)*

Humans do:

```
Known Structure → Map Structure → Apply Structure
```

Not: memorize.

### Important Observation

- Most ARC systems perform: **search**
- Humans often perform: **analogy**

Potentially a huge research gap.

---

## Area 5: Skill Acquisition Psychology

Psychology has a surprisingly consistent model.

| Stage | Name | Description |
|-------|------|-------------|
| 1 | Declarative | Think about every step |
| 2 | Procedural | Pattern appears |
| 3 | Automatic | Skill executes automatically |

**Example:** Driving. Initially: conscious effort. Eventually: automatic skill.

### Critical Observation

> **Humans convert reasoning into skills.**

This is almost exactly our Investigation 7 hypothesis. Current ARC systems rarely do this.

---

## Area 6: Expertise Development

This may be the biggest surprise.

- Experts are **NOT** merely people who know more.
- Experts are **people with better representations**.

**Examples:**

- **Medical experts:** they don't memorize symptoms; they recognize structures.
- **Chess experts:** they don't calculate everything; they recognize patterns.
- **Mathematicians:** they don't remember every proof; they recognize abstractions.

### Insight

> **Expertise seems to emerge through representation improvement, not knowledge accumulation.**

---

## A Unified Model Of Human Learning

Combining all cognitive science findings:

```
Experience
  ↓
Pattern Detection
  ↓
Invariant Detection
  ↓
Concept Formation
  ↓
Chunking
  ↓
Skill Formation
  ↓
Skill Composition
  ↓
Transfer
  ↓
Expertise
```

---

## Compare Humans vs Current ARC Systems

**Current ARC Systems:**

```
Task → Search → Solution
```

**Human Learning:**

```
Task → Search → Pattern → Concept → Skill → Future Advantage
```

Notice the extra stages. Those stages are mostly missing in current ARC architectures.

---

## Most Important Discovery Of Investigation 8

We've identified something significant:

> **Human intelligence appears to grow primarily through representation change rather than solution optimization.**

- Current ARC systems optimize: **solution**
- Humans optimize: **representation**

---

## Updated Research Gap

After Investigations 1–8, the strongest unresolved question becomes:

> **How can an agent autonomously improve its internal representations by discovering concepts, chunking recurring reasoning patterns, and converting them into transferable skills?**

Notice how different this is from: *"How can an agent solve ARC?"*

---

## New Candidate Research Thesis

Version 2 of our emerging theory:

> **Intelligence grows when repeated reasoning traces are compressed into concepts, concepts are chunked into skills, and skills are transferred across novel situations through analogical reasoning.**

This is substantially deeper than:

- program synthesis,
- refinement loops,
- neuro-symbolic reasoning,
- memory systems,

…because it attempts to model the mechanism by which human capabilities themselves are formed.

---

## Where We Are Now

After Investigations 1–8, we have narrowed the space dramatically.

The remaining critical investigation before architecture design is:

> **Investigation 9: DreamCoder Deep Dive**

Because DreamCoder is the closest existing system to:

```
Experience → Compression → New Primitive → Growing Capability
```

We need to understand exactly:

- What DreamCoder actually does.
- What it gets right.
- What it gets wrong.
- Why it hasn't become the dominant ARC solution.
- Whether our emerging theory genuinely goes beyond it.

That investigation will likely determine whether we have a truly novel ARC Prize research direction or merely a variation of existing work.
