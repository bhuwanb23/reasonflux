# P1.2 — Mechanism-by-Mechanism Comparison

**Status:** evidence-based first-pass comparison, 2026-11-03; exact full-text/code-level verification remains. This table evaluates mechanisms, not titles or broad slogans.

## T2T proposed mechanism under review

The current design hypothesis has six linked operations:

1. Mine multiple interaction traces for a repeated state–action–effect relation.
2. Separate stable relational structure from trace-specific values/parameters.
3. Represent the relation as a reusable invariant skill with explicit observable applicability predicates.
4. Compare prospective predicted effects to observed effects.
5. Use *classified* counterexamples to revise the skill's applicability boundary (or reject/split the skill), preserving immutable versions.
6. Test held-out cross-context prediction and action outcomes against raw and strong parameterized/compressed replay under matched resources.

Only the combination in that exact research question could be a candidate contribution; most individual components are known.

## Comparison matrix

| Prior-art family | Trace-derived? | Explicit skill / policy object? | Applicability or initiation conditions? | Counterexamples / failure evidence? | Cross-context transfer? | What remains differentiable? |
|---|---:|---:|---:|---:|---:|---|
| Options / LTL-Transfer / logical advice transfer | Often learned from tasks/experience | Yes: option/action advice | Yes; initiation sets, state conditions, transition constraints | Not the defining novelty in cited formulations | Yes | Learning an invariant boundary from failed transfer attempts may differ, but must be proven against this tradition. |
| DreamCoder / program library learning | Programs/solutions across tasks | Reusable abstractions/primitives | Usually through program types/semantics/search, not runtime skill activation predicate | Search failure is not necessarily a semantic counterexample boundary | Yes, across synthesis tasks | T2T must demonstrate a behavioral applicability object beyond abstraction/compression. |
| Skill-Pro | Interaction trajectories | Yes, executable procedural skill | Explicit activation and termination conditions | Trajectory-derived semantic gradients and verification gate | In-domain, cross-task and cross-agent | Does its refinement learn a counterexample-defined cross-context boundary? Read full method and test against it. |
| Skill-DisCo | Successful traces | Parameterized control-flow subgraphs compiled to skills | Parameter binding and executable conditions | Compilation/execution verification; primary distillation is successful-trace based | Across tasks/models in evaluated benchmarks | T2T may involve both positive and contradictory evidence to infer scope, not just cluster successful structure. Confirm through full paper. |
| SkillComposer / Trace2Skill / MUSE | Traces, success/failure patches or experience | Yes; documents/workflows and lifecycle | Trigger/selection and specialization in various forms | Improvements, error patches, validation/refinement | OOD/cross-model/tasks reported | Explicitly formalized, observable invariant boundary + matched replay control; not generic generation or lifecycle. |
| ASSAY / skill utility evaluation | Existing skill libraries and task outcomes | Skill records; not necessarily an executable invariant | Per-task masking / relevance prediction | Randomized intervention estimates positive/negative causal contribution | Across task types | T2T could learn state-level semantic preconditions from traces rather than infer task-level utility from development outcomes. But this is an important direct alternative. |
| CEGAR / counterexample-guided synthesis | Abstract models/programs and verification traces | Abstract model/program, not necessarily an agent skill | Refinement splits abstraction/predicate scope | Central: classify real/spurious counterexamples and refine | Across modeled states/properties | T2T must show new setting/objective (skill transfer under sparse interactive experience) and not merely apply CEGAR vocabulary. |
| Twin / OPINE-World / executable ARC models | Live interaction traces | Executable transition/world model | Model-defined state/action domain; checked before use | Central: mismatch is counterexample to repair model | Primarily within a game; transfer of modeling priors/knowledge may occur | Skill-level transferable boundary between contexts rather than repairing one game model. Strong closest ARC overlap. |
| Tycho / Schema / active world-model agents | Live observations/actions | Explicit world model + planning interface | Typed evidence/conditions and selective model use vary | Verification, replay, predictive checks and model repair | Across levels/observed task sequences; systems may carry knowledge | Need show T2T skill transfer is distinct from retaining/refining model mechanics or policy advice across levels. |
| arc-skill | Current state + action hypotheses | Predictive action gate/harness; general skill plus analysis tools | Per-action prediction gate, halts on mismatch | Prediction miss is explicit feedback | Across public games from one common method | Not first prediction-before-action or mismatch check. Could differ only in learned cross-context applicability policy and evaluation against replay. |
| ARC trace-reuse measurement | Agent artifacts/logs | Observed scripts/notes | Not learned as an algorithm | Contradictions are observed/settled against logs | Measures cross-level persistence/rewrite | T2T would be constructive mechanism, not a measurement study; cite as evidence of problem relevance, not a direct method comparator. |

## Construct distinctions that must remain precise

- **World-model counterexample:** observation falsifies a particular transition model `T(s,a)` in a given environment. Updating it repairs environmental dynamics.
- **Skill-scope counterexample:** evidence contradicts the claim that an existing skill should be invoked in a specified observable context, or that its predicted effect generalizes to that context.
- **Skill outcome failure:** task/level does not complete. This alone does not prove the skill's local dynamics or applicability condition was wrong; goal inference, planner, hidden state, execution and budget may cause failure.
- **Replay check:** verifies that an implementation reproduces logged transitions. It establishes historical fit, not generalization or skill-specific value.
- **Boundary learning:** selects/splits/refines observable preconditions based on evidence. It may increase precision while reducing coverage; report both.
- **Causal skill utility:** with-skill versus no-skill outcome change. ASSAY/Backtrace directly address this; distinct from a model prediction mismatch.

## What would count as a meaningful separation

All of the following would be required before advancing a novelty claim:

1. A task-independent, machine-checkable definition of invariant relation and skill-scope counterexample.
2. Same source events available to the invariant and replay arms; no hidden outcome leakage.
3. A competent parameterized/compressed replay control, reviewed and frozen before target evaluation.
4. A held-out context in which prediction and effect transfer can differ from replay; distinguish within-level, cross-level and cross-game claims.
5. Counterexample-boundary ablation, with generation/support held fixed as far as possible.
6. Matched memory/context, compute, model, action and retrieval budgets (or predeclared cost curves).
7. A claim that survives comparison to direct conditional skill masking/selection (ASSAY-like) and executable model repair (Twin/OPINE-like), not just no-skill controls.

## Synthesis

The broad method is an intersection of mature elements: options already have initiation sets; skill-learning papers learn activation conditions and refine skills; CEGAR uses counterexamples to refine abstractions; ARC world-model systems use mismatches to repair executable dynamics; skill-causality work estimates conditional utility. The open space is not yet an established novelty claim. It may be the **object-level distinction and controlled test**: boundary refinement for cross-context invariant skills versus (a) trace replay/compression, (b) per-game world-model repair, and (c) outcome-based per-task masking. This remains a hypothesis until full source review and exact comparator design.
