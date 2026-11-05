# P3 Deliverables — Claim N and Fair Replay Controls

**Contract:** `T2T-P3-FairReplay-v1.0.0-draft`  
**P3 status:** complete for documentation/design scope, 2026-11-04.  
**Authorization boundary:** no code, experiments, benchmarks, ARC runs, split assignment, target-outcome tuning, or restricted-outcome access.

## Normative design

- [`fair_replay_controls_v1.md`](fair_replay_controls_v1.md) — versioned control definitions, the budget-matching vector and mismatch handling, ablation matrix, Claim N estimands, falsifiers, and unresolved decisions.
- [`../claim_n_specification.md`](../claim_n_specification.md) — Claim N wording and interpretation rules, reconciled to P3.
- [`../formal_skill_object.md`](../formal_skill_object.md) — P2 semantics of CandidateVersion, SkillVersion, applicability, PredictionRecord, and EffectAssessment.

## P3.1–P3.3 results

- **P3.1 Raw replay:** frozen source trace/script retrieval and exact ordered replay under recorded source-context assumptions; on mismatch, stop/abstain rather than repair or rebind.
- **P3.2 Strong replay:** competent trace-derived compression, retrieval, typed slot binding (including new IDs under fixed schema rules), and bounded source-derived control flow. It shares the prediction interface and may transport aligned source effects, but has no learned cross-context invariant boundary or counterexample-derived guard. It is the required primary comparator; it must not be weakened.
- **P3.3 Isolation and budget matching:** same permitted source events, observations, model access, retrieval interface, evaluation contexts/evaluator, and predeclared resource caps across methods; report actual creation, validation, invocation, and outcome costs separately. Define the primary predictive estimand and secondary intention-to-treat behavioral estimand; preserve abstentions and all assigned units.

## Acceptance and remaining choices

P3 is complete for the design/documentation scope. All three subphases link to the controlling contract. P3 specifies a conceptual fair comparison and falsifiers but does not certify baseline competence, novelty, likely effect, or feasibility. No endpoint margin, numerical budget, sample size, split, cohort, or statistical decision threshold is invented. Final document QA checked 53 Markdown files and 248 relative links with zero broken links, and verified the three subphase statuses and required control/estimand/falsifier sections. This is documentation QA only; no baseline was built or evaluated. See the normative document for the open choices and conditions under which a future comparison would be inconclusive rather than evidence for Claim N.
