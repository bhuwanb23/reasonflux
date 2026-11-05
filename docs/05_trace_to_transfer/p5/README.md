# P5 Deliverables — Experimental Protocol Design

**Protocol:** `T2T-P5-Protocol-v1.0.0-draft`  
**P5 status:** complete for design/documentation scope, 2026-11-04.  
**Implementation status:** none. Per the clarified scope selection, this work produces no code/tooling.  
**Authority boundary:** not preregistration or approval; no code, experiments, benchmarks, ARC runs, split assignment, hidden/test access, or restricted-outcome access.

## Normative proposal

- [`protocol_v1.md`](protocol_v1.md) — claim-specific arms/estimands, data roles/cohort eligibility, budget and reset controls, outcome/failure metrics, analysis/falsifiers, exclusions, stop rules, unresolved freeze fields, and separate authorization gate.
- [`../experimental_protocol_design.md`](../experimental_protocol_design.md) — short entry point to this versioned proposal.
- [`../p3/fair_replay_controls_v1.md`](../p3/fair_replay_controls_v1.md) — controlling R0/R1/I0/I1 definitions and matched-resource conditions.
- [`../p4/boundary_algorithm_v1.md`](../p4/boundary_algorithm_v1.md) — controlling candidate, evidence-role, taxonomy, refinement, and fallback semantics.
- [`../claim_n_specification.md`](../claim_n_specification.md) and [`../../../reports/competition/arc_prize_2026_claim_evidence_map_v1.md`](../../../reports/competition/arc_prize_2026_claim_evidence_map_v1.md) — claim wording and evidence ceiling.

## Subphase records

- [P5.1 — Arms and estimands](../subphases/p5_1.md)
- [P5.2 — Data and budgets](../subphases/p5_2.md)
- [P5.3 — Metrics](../subphases/p5_3.md)
- [P5.4 — Analysis and falsifiers](../subphases/p5_4.md)

## P5.1–P5.4 results

- **P5.1 Arms and estimands:** candidate-generation and runtime arms are separated; each claim has a specified primary contrast, endpoint, unit, and interpretation. Claim N uses I0 vs R1; Claim B/C use I1 vs I0; full-method Claim E includes the meaningful baseline set. No claim is inferred from another.
- **P5.2 Data and budgets:** defines prospective source/development/validation/confirmatory roles, eligible target-unit criteria, common resource vector, reset/pairing constraints, and manifest fields. No task IDs, actual cohort, split, or budget values are assigned.
- **P5.3 Metrics:** defines official outcome, prediction coverage/risk, boundary errors, negative-transfer categories, action efficiency, costs, and all failure denominators. No unvalidated composite is introduced.
- **P5.4 Analysis and falsifiers:** fixes the proposed unit of analysis, clustered uncertainty approach, multiplicity method, inclusion/exclusion rules, effect-threshold fields, and safety/integrity stop conditions. Effect margins, alpha/confidence level, sample size, and power remain `UNSET` and block a run-ready preregistration.

## Acceptance and open choices

P5 is complete as a **reviewable protocol proposal**, not as a preregistration, run authorization, or executable study. Required unresolved fields include exact permissible manifests/cohort, randomization and reset feasibility, numerical resource caps, primary score/loss and abstention rule, harm adjudication, alpha/confidence level, minimum meaningful effects and regression margins, sample size/power, missingness method, and named roles. These must be prospectively frozen by the existing approval process; no threshold may be chosen after outcomes. Final document QA checked 58 Markdown files and 210 relative links with zero broken links; the four subphase statuses and protocol coverage were verified. This is documentation QA only. No implementation or empirical work was performed.
