# P1 Prior-Art Review — Working Packet

**Review snapshot:** 2026-11-03. **Status:** P1 complete for the owner-approved idea-stage scope; the owner selected the comparative ARC-specific reframe as the best direction. This is not novelty clearance or a systematic-review certification. No code, experiments, benchmarks, ARC runs, split assignments, or restricted-outcome access were performed.

## Findings at a glance

The current standalone novelty claim is **not supportable**. In addition to the published overlap in activation boundaries and boundary-aware skills, we found a near-exact public proposal for counterexample-qualified refinement of reusable skill guards (issue #6645). ARC-AGI-3 has close work on executable world models, replay verification, prediction-before-action and counterexample-driven repair.

Disposition: **no-go on the current standalone method novelty claim; owner-selected comparative ARC-specific reframe** to test whether structural cross-context state/action/effect invariants add value beyond outcome-based skill activation, explicit boundary records, guard refinement, failure-informed skill evolution, model/workspace repair and strong replay. The comparative question is not itself novelty-cleared.

## Documents

1. [`source_inventory.md`](source_inventory.md) — bibliography, source quality, and mechanism-level notes.
2. [`mechanism_comparison.md`](mechanism_comparison.md) — direct comparison against the proposed components.
3. [`novelty_decision.md`](novelty_decision.md) — owner-selected disposition, residual question, required claim-clearance checks, and falsifiers.
4. [`../prior_art_matrix.md`](../prior_art_matrix.md) — compact matrix linked from the main package.

## What this review did and did not do

- Reviewed primary source records and selected full-text methods/results for central works, including latest SkillApt v2; followed the directly linked #6645, #6661, #6796, #6800, #6804 and #6997 public artifacts. Source versions and access links are in the inventory.
- Added recent StateSkill, ReSkill, Defense-as-Skill, Skill Coverage and DreamTeam lines and recorded the targeted search/citation-chase scope.
- Did not inspect every repository commit, supplement, code path, citation graph, or all concurrent work; ARC3 SAGE primary pages remain inaccessible, and no independent human novelty challenge was performed.
- The owner accepted this bounded P1 disposition for idea-stage work. This is a research-prior-art assessment, not legal advice, a patentability opinion, systematic-review certification, or proof of priority.

## Decision status

**Recommendation and owner direction:** reject the current standalone novelty claim and retain only the narrow comparative research question as a provisional design direction. The owner selected this reframe on 2026-11-03; the question is still not novelty-cleared. See [`novelty_decision.md`](novelty_decision.md).
