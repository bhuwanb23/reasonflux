# Phase 1D.2 — Memory and Abstraction Taxonomy

## Systems under comparison

| Code | Representation | What is stored | Permitted operation | Main failure mode to test |
|---|---|---|---|---|
| M1 | Exact Episodic Memory | Training task key, observed input/context, and the demonstrated solution/action sequence. | Replay only on a valid exact-match rule; no applying a stored answer to a changed task. | No exact match; duplicate-task exposure can be mistaken for generalization. |
| M2 | Partial Episodic Memory | Bounded trace fragments, subproblem outputs, and provenance. | Reuse a fragment only when its required context is present; cannot invent missing steps. | Missing fragment/context; brittle fragment composition. |
| M3 | Pattern Memory | Repeated surface/sequence patterns, counts, and observed associations; no explicit general rule object. | Similarity/pattern-based retrieval under a fixed threshold. | Surface lure, spurious recurrence, poor structural generalization. |
| M4 | Skill Abstraction | Explicit rule/skill representation distilled from training episodes, with applicability conditions. | Apply a rule to a new instance only when predeclared preconditions match. | Overgeneralization, missing parameters, composition failure, abstraction cost. |
| M5 | Hybrid Memory + Abstraction | Both episodic records/fragments and explicit rules. | Exact/partial retrieval plus rule application under one shared total budget. | Budget dilution, conflict-resolution errors, leakage through memory. |

## Required policy arms

B1 is a **memory-only suite** with M1, M2, and M3 reported separately. B2 is M4 abstraction-only. B3 is M5 hybrid. B4 is a seeded random-retrieval control using the same eligible episodic store and retrieval cap as the relevant memory arms. B5 is the same base solver with no learned episodic or abstract store. B6 Oracle is an analysis-only upper bound after outcomes lock.

The historical Phase 13C `MEMORY_ONLY` implementation maps most closely to **M2/M3-like raw-trace-exemplar macro reuse**: it chooses a trace matching an invariant pattern, extracts a simple operation macro, and applies that macro. It is not automatically interchangeable with M1.

## Representation accounting

Every stored object has a canonical ID, type, source split/task, serialized byte count, creation compute, and allowed access mode. Hybrid stores count both types against one storage/candidate budget. No system receives a larger cap because its representation is called a “skill” or “memory.” Storage is measured from serialized artifacts, not object counts alone.

## Separation of predictor and truth

The taxonomy and arm identity are not outcome labels. Future task labels/answers are held in evaluator-only records. Memory/abstraction interfaces receive only training-derived objects and query inputs. Any arm whose memory includes a confirmatory answer outside the explicitly permitted Family A repeat condition is invalid.