# P1 Prior-Art Review — Working Packet

**Review snapshot:** 2026-11-03. **Status:** substantial first-pass review; not a completed systematic review and not owner-approved. No code, experiments, benchmarks, ARC runs, split assignments, or restricted-outcome access were performed.

## Findings at a glance

The broad project framing is not novel: skill induction from traces, parameterized/procedural skills, applicability or activation conditions, lifecycle refinement, negative-transfer management, and counterexample/prediction checks all have clear antecedents. ARC-AGI-3 now has close work on executable world models, prediction-before-action, replay verification, and counterexample-driven model repair.

A narrower candidate question remains worth checking: **does an explicit cross-context invariant representation, with applicability boundaries revised from correctly classified counterexamples, improve held-out transfer over a strong parameterized/compressed replay control under matched budgets?** The combined wedge is plausible as a question but is not yet established as novel. Existing results do not answer this exact comparison as identified so far; absence in this first-pass review is not proof of absence.

## Documents

1. [`source_inventory.md`](source_inventory.md) — bibliography, source quality, and mechanism-level notes.
2. [`mechanism_comparison.md`](mechanism_comparison.md) — direct comparison against the proposed components.
3. [`novelty_decision.md`](novelty_decision.md) — interim narrowing recommendation, required checks, and falsifiers.
4. [`../prior_art_matrix.md`](../prior_art_matrix.md) — compact matrix linked from the main package.

## What this review did and did not do

- Reviewed primary source pages / abstracts and selected full-text sections for central works; sources and access dates are linked in the inventory.
- Identified direct and adjacent overlaps; did not perform exhaustive backward/forward citation chasing for every source.
- Did not inspect every repository commit, supplementary artifact, or all concurrent work published near this date.
- This is a research-prior-art assessment, not legal advice, a patentability opinion, or proof of priority.

## Decision status

**Interim recommendation:** reject broad novelty claims; retain only the narrow comparative research question as a provisional hypothesis. Owner approval is outstanding. See [`novelty_decision.md`](novelty_decision.md).
