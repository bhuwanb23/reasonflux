# Phase 2I — Candidate Production Protocol

## Objective

Determine whether the **current frozen invariant-candidate construct** can be produced and qualified in nonzero quantity by the ARC reasoning pipeline, and whether the Phase 2F object-centric R3 representation changes that yield. This is an upstream production/readiness study—not an IDT ranking, transfer-efficacy, or FNTU experiment.

## Research questions

- **Q1:** Does the current R1 production representation produce accepted invariant-candidate objects without changing the candidate definition?
- **Q2:** Can the frozen support/stability/family rules be met on the permitted discovery material?
- **Q3:** Do accepted proposals pass the pre-outcome structural candidate checks and populate a nonzero candidate registry?
- **Q4:** Does the preregistered R3 object-centric representation change trace/candidate yield under the same downstream miner and resource budget?

## Registered conditions

| Arm | Definition | Purpose |
|---|---|---|
| R1 | Current ten-program production reference executed under Phase 2C S4 protocol | Faithful baseline candidate-production yield |
| R3 | Phase 2F object-centric finite grammar, same search cap and downstream pipeline | Test whether representation change changes invariant yield while retaining the ranked object |
| HCC | Phase 2F synthetic known-rule positive control, if implemented | Validate pipeline/trace plumbing only; never count as ARC evidence or candidate population |

R2/R4–R7 are not needed for this candidate-yield question. They must not be substituted post hoc if R3 is difficult to implement.

## Data, split, and outcome boundary

- Use only the 600 historical `discovery` task IDs for a **development-only diagnostic**; every ID has prior Phase 2B/2C audit exposure. This set is not confirmatory or pristine.
- Use task training demonstrations only. Do not parse/use task test outputs, score generalization, compute transfer utility, or inspect hidden future value.
- Use identical task IDs, input validation, search budget, trace schema, miner, candidate policy, and downstream candidate checks in R1 and R3.
- Phase 2F specifies maximum 10 complete candidate trials/task, one-level deterministic enumeration, one trace/task/condition with at most four high-level steps, 30-second search limit, and 2,048 MiB memory cap. Actual usage and stopping cause must be logged.
- Freeze independent semantic task-family annotations before the candidate run. Existing program-derived family labels are not independent; if annotations cannot be produced, cross-family qualification is unavailable and candidate yield cannot pass that gate.

## Candidate-production stages to log separately

For each representation, report task/task-family denominators and per-stage counts:

1. eligible task demonstrations;
2. candidates generated and evaluated under the fixed cap;
3. exact demonstration fits;
4. traces emitted, structurally valid, and successful;
5. trace fragments and distinct-signature support;
6. mined patterns and aggregated structures;
7. invariant proposals before rejection;
8. rejected proposals by frozen reason;
9. accepted invariant candidates;
10. canonical deduplicated candidate IDs;
11. candidates meeting pre-outcome structural qualification;
12. feature-ready/rankable candidates and unavailable feature reasons (reported descriptively only).

No-fit, invalid-input, parser-failure, budget-exhausted, no-trace, no-pattern, rejected-candidate, and unavailable-family states remain distinct. Do not collapse missing denominators to zero.

## Frozen candidate-policy floor

Retain the Phase 2F downstream configuration and current candidate rejection policy; do not lower thresholds to obtain nonzero yield. The audited target floors are `min_frequency=5`, `min_cross_trace=5`, `min_consistency=1.0`, and at least two independently assigned task families, with the same candidate rejection rules. Before execution, pin one exact code/config pair because current library defaults differ from the Phase 2F audited configuration. Any discrepancy must be reconciled before the run, not changed during it.

## Candidate identity and deduplication

Use the frozen invariant canonical identity, retain all source trace/task IDs and family evidence, and report within-arm unique candidates. Do not pool R1/R3 proposals to inflate N. If the same canonical invariant appears in both arms, record the shared ID and both provenance paths; representation arm is a source attribute, not future-value information. Resolve the existing identity implementation's family-omission risk before freezing the manifest.

## Analysis boundary

The primary report is descriptive candidate yield and stage attrition by representation. Any paired R1–R3 coverage/yield interval is development-only and cannot establish IDT efficacy. No FNTU, pressure gate, comparator win, or future utility is computed. A nonzero candidate yield is necessary for later Phase 3 readiness but is not sufficient: Phase 3A-R must still validate actual pool diversity/pressure, feature lineage, endpoint, and outcome controls.