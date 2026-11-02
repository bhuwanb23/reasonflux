# Phase 1H.2 — Baseline Taxonomy

Every competitor is assigned a primary family and an implementation subtype before outcomes. Multiple baselines from one family may be mandatory if they instantiate different surviving explanations.

| Family | Baseline type | Role and fairness requirement |
|---|---|---|
| B1 — No learning | No learned invariants/skills/update; same task inputs, fixed base solver, evaluation horizon, and allowed compute. | A floor/behavior control, not the only opponent. Freeze what is disabled and what base solver remains. Do not assume it is easy to beat: 13E/13F ASFT task utility is below B1. The Phase 13C `NEVER_CREATE` arm is a skill-creation floor in that specific simulator, not automatically the same implementation as every no-learning baseline. |
| B2 — Memory/retrieval | Episodic trace/example retrieval, exact memory, macro reuse, or structured skill store, each separately named. | Tests the surviving experience-retrieval explanation. Do not conflate raw trace exemplars with full solution replay or skill libraries. |
| B3 — Random | Random candidate ranking/selection/action from the same eligible pool. | Chance/control for selection; repeat across preregistered seeds and match number of decisions and budget. |
| B4 — Frequency | Occurrence/reuse/frequency-only ranking using training data only. | Strong simple heuristic; freeze count/recency/tie-breaking, no test leakage. |
| B5 — Compression | Exact trace compression, grammar induction, or other compression method, explicitly identified. | Surviving alternative; a proxy must not be called canonical DreamCoder or generalized compression. |
| B6 — Heuristic / hybrid | B6a declared non-learning domain heuristic; B6b hybrid memory+frequency (mandatory BL6). | Competes with simple hand-designed rules and combination explanations. Freeze feature access and weights. |
| B7 — Oracle | Uses latent labels, known task-generating rules, or held-out answer information only for offline upper-bound analysis. | Not a deployable baseline; must never choose candidates, tune thresholds, or count as an ASFT victory. |

## Mandatory registry IDs

- BL1 — No Learning
- BL2 — Memory/Retrieval
- BL3 — Random
- BL4 — Frequency
- BL5 — Compression
- BL6 — Hybrid Memory+Frequency (B6b)
- BL7 — Oracle (analysis only)

Heuristic B6a is included when relevant to the task family. The exact subtype, permitted information, candidate pool, budget, storage, and outcome endpoint are registered per experiment. A baseline family name alone is insufficient to claim comparability.