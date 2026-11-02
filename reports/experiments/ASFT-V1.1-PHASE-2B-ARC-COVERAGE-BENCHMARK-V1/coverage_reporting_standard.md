# Phase 2B.8 — Coverage Reporting Standard

Every coverage run must include the following fields, by split and condition, with ARC task ID as the independent unit:

| Required field | Definition / reporting rule |
|---|---|
| Tasks | Unique eligible task IDs; report split, exclusions, and denominator. |
| Coverage % | C1 found exact demo-fit tasks / eligible task IDs. State representation version, candidate order, parameter inference, budget, runtime cap, and exact-fit rule. |
| Trace % | C2 emitted trace records / eligible task IDs. Distinguish emission from validity and success. |
| Successful trace % | C3 independently valid exact-demo-fit traces / eligible task IDs. |
| Invariant % | C4 tasks with an available accepted invariant / eligible task IDs; also report successful discovery trace support, invariant policy, and zero-denominator conditional rate. |
| Skill % | C5 eligible task IDs with an available skill candidate / eligible task IDs; separately report conditional denominator C4. Use `not_estimable` if C4=0. |
| Transfer eligibility % | C6 eligible IDs / all eligible IDs; show conditional denominator C5 and whether transfer was merely eligible or actually tested. |
| Capability eligibility % | C7 eligible IDs / all eligible IDs; state independent capability criterion and conditional denominator. |
| Accuracy | Separate column/report only, with its own labels, denominator, exact-match rule, and authorization. If not evaluated, say `NOT_MEASURED`; never infer it from C1–C7. |
| Status | Use measured zero, unavailable, not run, blocked upstream, or not applicable distinctly. No blank-to-zero coercion. |

## Mandatory stratification and diagnostics

Report budgeted and fullscan modes separately; per-split and aggregate counts; numerator and denominator; missing-data/exclusion counts; trace validity; first-fit/program signature diversity; candidate trials and runtime; stage transition/conditional rates; source and code hashes; access-control statement; and all deviations. Fullscan is a diagnostic ceiling for the frozen finite implementation, not a performance claim.

## Separation rule

Coverage is an operational found-fit measure. Accuracy, transfer success, skill/capability formation, and theory validation are separate constructs. They may never be merged into one score or used as substitute evidence. Historical “no fit” means no fit found under that condition, not semantic impossibility. A hash verifies lineage only.