# P1.3 — Novelty Decision

**Decision record:** `P1-owner-disposition-2026-11-03-v3`  
**Review status:** bounded source-grounded P1 review complete to owner-approved idea-stage scope. **Owner direction (2026-11-03): pursue the comparative ARC-specific reframe as the best path.** This is not novelty clearance, comprehensive systematic-review certification, implementation approval, or experiment authorization.

## 1. Executive decision

### Recommendation: NO-GO for the current standalone novelty claim; REFRAME if the research question is retained

The proposed broad contribution—**counterexample-guided learning/refinement of an applicability boundary for reusable skills**—is not supportable as novel on the evidence now reviewed.

This conclusion follows from several distinct but converging overlaps:

1. **Boundary-aware skill representation/use:** BASM explicitly stores applicability, risk, avoidance and recovery conditions and uses them to apply, suppress or repair skills ([Lin et al., 2026](https://arxiv.org/html/2608.22339)).
2. **Evidence-conditioned activation-boundary learning:** latest SkillApt v2 collects matched WITH/WITHOUT executions for fixed skills and accumulates state-conditioned evidence to update LOAD/ABSTAIN without changing the procedure ([Guo et al., 2026](https://arxiv.org/html/2609.26863v2)). SelSkill learns local invoke/skip decisions from paired continuations ([Chen et al., 2026](https://arxiv.org/html/2606.00510v2)).
3. **Direct public disclosure and finite fixtures for counterexample-to-skill-guard refinement:** issue #6645 specifies versioned reusable skill guards refined from independently replayable, classified counterexamples, with a fixed predicate vocabulary, fallback/UNKNOWN, and dependent-cache invalidation ([issue](https://github.com/Unjuno/agent-interface/issues/6645)). Linked PRs report finite synthetic results: #6796 reports 0/7 harmful false admissions versus 7 unchanged-guard in its authored fixture; #6800 reports a five-row hidden-family coverage-gate T1; #6804 isolates the gate boolean in a five-row counterfactual; #6997 is an evidence-only independent audit with zero new candidate runs ([#6796](https://github.com/Unjuno/agent-interface/pull/6796), [#6800](https://github.com/Unjuno/agent-interface/pull/6800), [#6804](https://github.com/Unjuno/agent-interface/pull/6804), [#6997](https://github.com/Unjuno/agent-interface/pull/6997)). These are not ARC or population evidence, but they make the central guard-refinement mechanism publicly disclosed and concretely instantiated in finite fixtures.
4. **Failure-informed conditional skill evolution and structured state skills:** ReSkill revises conditional triggers from diagnosed rollout failures; StateSkill represents embodied experience as state-conditioned FSM skills and revises state gates/guidance from successful and failed trajectories ([ReSkill](https://arxiv.org/html/2606.01619v2), [StateSkill-Agent](https://arxiv.org/html/2610.14601v1)). They are not the proposed ARC invariant learner, but they block broad novelty claims for stateful reusable skills or failure-driven skill refinement.
5. **ARC-specific predictive verification/model/workspace repair:** DreamTeam, Twin, OPINE-World, Tycho, Schema and arc-skill cover executable model prediction, replay checks, mismatch routing/repair, or prediction-gated action in ARC-AGI-3. These prevent “first predictive gate / first counterexample repair” claims.
6. **Unresolved ARC3 SAGE collision:** a search-indexed secondary pointer describes an ARC3 SAGE action/effect world-model and generalized-skill lane, including promotion when preconditions/effects remain stable. The cited primary issue/merge pages are inaccessible, so exact overlap is unverified; it is an additional novelty risk, not evidence of absence.

Together, these overlaps mean the current T2T wedge cannot be presented as a new general method. Calling the T2T object an “invariant skill” does not by itself establish a distinction.

## 2. What remains potentially worth studying (not novelty-cleared)

A narrower **comparative question** remains plausible:

> In interactive ARC-like environments, does a cross-context structural state/action/effect representation provide incremental held-out predictive or behavioral value beyond (a) strong parameterized/compressed replay, (b) a SkillApt-like outcome-utility activation boundary, (c) explicit boundary-conditioned skill records, and (d) environment-specific executable-model repair?

This may support a useful controlled study if the distinction is operationally precise. It is not presently a novelty claim. Publicly searchable material reviewed here did not establish whether a method already performs this exact comparison; the inaccessible SAGE lane is an unresolved collision, not evidence of absence.

## 3. Components that must not be claimed as novel

Do not claim “first” or method novelty for:

- trace-to-skill distillation, parameterized skills, transferable abstractions, or skill libraries;
- skill preconditions, initiation sets, applicability/activation boundaries, or conditional invocation;
- adding risk/avoidance/recovery boundary fields to reusable skills;
- using outcome or counterfactual evidence to decide whether to invoke a skill;
- local invoke/skip preference learning;
- refining a skill guard from classified concrete counterexamples in general;
- verifying predicted effects before action, replaying observations, or repairing a model from mismatch;
- reducing negative transfer by selective masking, suppression, or abstention;
- broad candidate-generation/support-before-ranking framing or skill-use auditing.

## 4. Exact distinctions—and why they are insufficient alone

| Mechanism | Evidence signal | Updated object | Closest precedent | Possible T2T delta; still unproven |
|---|---|---|---|---|
| Counterfactual activation boundary | Matched skill/no-skill outcomes and cost | Whether to load/invoke a fixed procedure | SkillApt; SelSkill; ASSAY | T2T could use structural transition evidence rather than final utility, but must show added value under direct controls. |
| Boundary-aware skill record | Logged traces / extracted validity conditions | Conditions/risk/avoidance/recovery fields | BASM | T2T could formalize invariant/effect semantics and provenance; mere schema formalization is not enough. |
| Guard refinement | Independently replayed concrete counterexample against a skill guard | Versioned applicability guard, with fallback and dependency invalidation | Unjuno issue #6645 | Same broad mechanism is already publicly disclosed. A domain-specific instantiation alone is weak novelty absent new principle/evidence. |
| Dynamics-model repair | Prospective transition prediction differs from observed environment | Environment/game world model | Twin; OPINE-World; arc-skill | T2T could separate local model correctness from cross-context skill applicability, but must define this independently and compare it. |
| Replay/trace compression | Repeated action sequences/parameters across tasks | Compact macro/script/procedure | Skill-DisCo; DreamCoder; strong replay | T2T could establish that a relational invariant adds value beyond compression, but this is an empirical comparison, not novelty by definition. |

## 5. Critical prior-art caveats

- **Issue #6645:** direct fetch shows the issue closed and linked to #6997; its proposal is an offline finite GUI-interface guard-refinement method and explicitly limits its scope. #6661 is host construction evidence with formal-resource HOLD; #6796 is an authored finite T0-C replication; #6800 is a distinct five-row hidden-family coverage-gate T1; #6804 isolates the coverage gate in a separate five-row counterfactual; #6997 audits retained T1b artifacts without a new candidate run. Preserve the failures/UNKNOWN controls and scope caveats. None is ARC-science evidence. For prior art, the relevant fact is the public mechanism disclosure; fixture pass labels do not establish general effectiveness.
- **SkillApt:** the paper distinguishes utility-based activation from editing a skill; its boundary changes with accumulated paired evidence. T2T’s prediction mismatch signal differs, but it also targets a state-conditioned “use/abstain” boundary. The contrast must be tested, not asserted.
- **BASM:** explicit validity boundaries and execution-time enforcement already exist. It appears not to provide the same formal, counterexample-qualified invariant-learning algorithm, but that gap alone is insufficient given issue #6645.
- **SAGE:** search results point to an ARC-AGI-3 action/effect model and generalized skill-induction lane, but primary issue/PR pages returned 404 during this review. No mechanism details are relied on as verified facts. This collision must be resolved from an accessible source before any ARC-specific novelty statement.

## 6. Conditions before a later novelty claim or study

The owner selected the comparative question as the idea-stage direction. Before asserting a novelty contribution or designing any future study around it, retain these constraints:

1. State that the general method is not novel/cleared; position the paper as an ARC-specific evaluation or a carefully specified incremental contribution.
2. Define a “structural skill-scope counterexample” separately from a final task failure, SkillApt’s WITH/WITHOUT utility label, a BASM boundary field, and a world-model transition mismatch.
3. Compare directly to an outcome-utility activation baseline, a boundary-aware skill record, an unchanged-guard/guard-refinement analogue where feasible, per-game world-model repair, and strong parameterized replay.
4. Freeze source/target evidence, resource budgets and candidate semantics before any future authorized outcome access. No split assignment or run is authorized by P1.
5. Use falsifiers: if the strong replay or any direct applicability controller matches the invariant treatment at matched budgets, withdraw invariant-specific value; if the proposed scope cannot be inferred from permitted observations, report UNKNOWN/abstain.
6. Obtain independent novelty review. A bounded web search cannot prove global absence.

## 7. Final status for P1

- **P1.1 source inventory — complete for the owner-approved bounded scope:** expanded source set, targeted search/citation-chase record, primary-vs-secondary distinction, and updated finite-artifact evidence. Not exhaustive; ARC3 SAGE remains unverified.
- **P1.2 mechanism comparison — complete for the bounded scope:** differentiating objects/signals separated across activation, boundaries, guard refinement, state-conditioned skills, replay, model repair and ARC systems. The proposed standalone novelty center overlaps established work and a near-exact public guard-refinement proposal.
- **P1.3 decision — complete:** **NO-GO on the current standalone novelty claim; pursue the comparative ARC-specific question as provisional idea-stage direction.** The owner selected this route on 2026-11-03. The residual contribution remains a hypothesis, not novelty-cleared.

**Overall P1 status: COMPLETE for the owner-approved idea-stage scope.** It is not exhaustive prior-art clearance, a systematic-review certification, a legal opinion, or permission to implement/run. SAGE primary-source access and independent human novelty review remain future requirements before any submission-level novelty claim.

No experiment, benchmark, ARC run, implementation, split assignment or restricted-outcome access occurred. P1 completion does not change Phase 2I/Phase 3 restrictions and authorizes no execution.
