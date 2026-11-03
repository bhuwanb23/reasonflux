# Phase 2H.4 — Alternative Candidate Source Assessment

## Architectural question

**Must IDT rank invariant candidates, or could it rank earlier objects?**

For the current Phase 1C question—whether transfer-aware IDT ranking selects useful transferable invariant hypotheses—the coherent target remains an invariant candidate. Earlier objects can be studied, but ranking them would change the estimand and should be registered as a distinct selection-layer study.

| Alternative source | Nonzero objects? | Can be ranked computationally? | Can it substitute for current R1 without redesign? | Main construct/measurement issue |
|---|---|---|---|---|
| Trace fragments | Yes | Technically, after a new identity/feature adapter | **No** | Many overlapping n-grams; support and identity are not semantic invariance; rankings may reward trace length/control flow. |
| Mined patterns | Relaxed support produces four generic recurring signatures in some conditions | Technically | **No** | Pattern mining explicitly stops before invariant validation; repeated operations can be generic scaffolding. |
| Aggregated structures | Two per relaxed condition | Technically | **No** | Structures are intermediates; the only audited proposals were rejected as universal noise. |
| Raw candidate proposals | Two per relaxed condition, zero accepted | Technically | **No, as-is** | Both proposals fail the existing frozen rejection policy; admitting them would change eligibility. |
| SkillCandidate / Skill | Zero on audited ARC path | Yes in other phases/domains | **No** | Downstream of invariant selection; ranking skills tests skill creation/utility, not IDT invariant ranking. |
| ARC search programs | Thousands of trial slots | Already ranked/searched by program solver | **No** | These are candidate solutions to tasks, not recurring knowledge objects; an IDT score would be a new model and target. |
| Capability objects | Zero ARC capabilities | Potentially after capabilities exist | **No** | Downstream aggregate of skills/evidence; not an invariant candidate. |

## Decision on alternatives

Do **not** adopt an alternative candidate layer in this phase. No alternative object has an accepted IDT semantic definition, pre-outcome eligibility rule, independent outcome estimand, or validated feature map. In particular, do not call patterns or structures “invariants” merely to obtain nonzero N.

If project leadership decides that Phase 3 should rank patterns, structures, skills, or traces, classify the decision as **F3: redesign Phase 3**. That would require a new research question, candidate taxonomy/identity/eligibility, comparator suite, outcome measure, pressure thresholds, and contracts, with no claim of direct comparability to Phase 1C R1.