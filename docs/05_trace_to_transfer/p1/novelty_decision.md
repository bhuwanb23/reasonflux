# P1.3 — Interim Novelty Decision and Required Follow-up

**Decision version:** P1-interim-2026-11-03-v1  
**Status:** proposed disposition only; **owner approval outstanding**. This is not an owner-approved novelty claim, systematic-review certification, or authorization to implement/run.

## 1. Proposed disposition

### Reject broad novelty

Do **not** claim any of the following as novel:

- inducing reusable skills from traces;
- parameterized or compressed procedural skills;
- adding explicit skill triggers, preconditions, applicability conditions, initiation sets or termination rules;
- refining/merging/creating skills after successes or failures;
- preventing negative transfer through selective skill retrieval/masking;
- prediction-before-action, replay verification, or halting after a prediction mismatch;
- counterexample-guided repair/refinement in general;
- transferring skills or abstractions across tasks/levels;
- generic auditing of whether a skill helped;
- skill creation/reuse cost amortization.

The surveyed prior art directly covers these components. Relevant anchors include Skill-Pro (activation conditions plus trajectory-driven refinement and gate), Skill-DisCo (trace-derived parameterized executable skills), SkillComposer/Trace2Skill (skill creation, merging/refinement and transfer), ASSAY (per-task causal utility/masking), options/CEGAR (initiation sets and counterexample-guided abstraction refinement), and Twin/OPINE/arc-skill (ARC-AGI-3 model verification, mismatch repair and prediction gating).

### Retain only a narrow research question, provisionally

> **For interactive ARC-like environments, can a cross-context invariant skill’s observable applicability boundary be learned from correctly classified counterexamples, and does that representation improve held-out effect prediction or behavior beyond a strong parameterized/compressed replay control at matched resources?**

This is a **question to investigate**, not a novelty assertion. The potential distinction is the unit and comparison: explicit skill applicability scope across contexts, compared against replay/compression and separated from within-environment world-model repair and task-level outcome masking.

## 2. Confidence and reasons

| Assessment | Current status | Rationale |
|---|---|---|
| Broad trace-to-skill idea is novel | **Rejected** | Multiple direct prior methods. |
| Counterexamples can refine some reusable knowledge | **Known in broad form** | CEGAR and ARC world-model systems establish counterexample-guided refinement/model repair; skill refinement papers use failure signals. |
| A skill boundary differs conceptually from a world-model transition repair | **Plausible distinction, needs operational test** | Different object: invocation/effect-transfer scope vs environment dynamics. But methods can implement both together, so terminology alone is insufficient. |
| The exact proposed combination is absent from known sources | **Unknown** | The initial review found no exact match, but it is not comprehensive; related work and concurrent ARC projects remain to inspect. |
| Invariant representation adds value beyond strong replay | **Untested** | Requires Claim N comparator and controlled study. |
| Counterexample-guided boundary improves transfer | **Untested** | Requires counterexample ablation and held-out validation. |

No numerical probability is assigned: the search is not a formal systematic review and the available coverage is not sufficient to calibrate confidence.

## 3. Required final-review work before calling P1 complete

1. **Citation chasing:** backward and forward citations for Skill-Pro, Skill-DisCo, SkillComposer, Trace2Skill, ASSAY, Twin, Tycho, OPINE-World, Schema and arc-skill.
2. **Full text and supplements:** inspect algorithms, data splits, negative results, cost accounting, artifact/code and exact definitions of activation, initiation set, counterexample and validation.
3. **ARC-specific methods/artifacts:** inspect the underlying SAGE lane and referenced implementation behind issue #14268 if stable primary sources can be located; the issue itself previously returned 404 and cannot support the claim.
4. **Search synonyms:** option initiation-set refinement; precondition learning from failed executions; counterexample-guided skill induction; transferable action/effect abstractions; conditional options; skill safety filters; replay-equivalent program controls.
5. **Independent reviewer:** ask a researcher who did not formulate T2T to challenge whether a strong skill library, option learner, or model-repair method already has the purported operation.
6. **Freeze disposition:** record the owner’s choice—retain narrow question, reframe, or abandon—by explicit approval/version. Do not imply it was approved here.

## 4. No-go conditions

Abandon the novelty claim or redesign the study if any of these holds:

- A prior method already learns an explicit cross-context skill boundary by classified counterexamples and tests it against a fair replay control.
- The proposed boundary is merely a manually written trigger or inferred task label, not learned from the stated evidence.
- Strong replay plus parameter binding reproduces the same behavior/predictions within matched resource budgets.
- The representation cannot distinguish boundary mismatch from a wrong transition model, bad goal hypothesis, execution fault or observation ambiguity.
- The only improvement is generic performance from extra context, code, compute, or action prediction checks.
- Scope gains are achieved by abstaining almost always; coverage-adjusted utility does not improve.

## 5. Claim-language guidance

Until the above work and owner review are done, use formulations such as:

- “We investigate whether counterexample-guided applicability-boundary learning adds value beyond strong replay.”
- “Our proposed mechanism is motivated by an unresolved comparison; related work already covers trace distillation, conditional skills, negative transfer, replay validation and model repair.”

Avoid “first,” “novel invariant skill,” “new counterexample-guided skill learning,” and any implication that current ARC-AGI-3 results support the proposal. Current claim ceiling remains unchanged: no ARC-AGI-3 results; no test of Claims N, B, C, D or E.

## 6. Next design dependency

If the owner accepts the narrow question, proceed to T2T-P2/P3 to formalize (i) an invariant-scope counterexample distinct from a dynamics mismatch, (ii) a strong replay arm and (iii) falsifiers. If prior-art follow-up finds equivalence, revise/stop before implementation. P1 completion itself grants no authorization.
