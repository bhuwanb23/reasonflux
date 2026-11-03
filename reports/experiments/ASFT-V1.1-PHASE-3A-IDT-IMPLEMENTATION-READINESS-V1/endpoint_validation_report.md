# Phase 3A — Independent Endpoint Validation

## Primary endpoint implementation

The engine implements the Phase 1C estimand:

`FNTU@K(m) = [Σ_t (U(S_m,t) − U(∅,t)) − λ C(S_m)] / (K × H)`.

`fntu_suite` requires the five competitive policies R1–R5, exactly K unique selections from the shared pool, exactly H unique and identical task IDs per policy, identical paired no-candidate utility per task, and one fixed finite portfolio cost across the horizon. It rejects Oracle as a comparator and does not accept ranking scores or ranker formulas. Policy deltas are computed from paired FNTU values. Outcomes are therefore mathematically separate from rank scores in the endpoint interface.

## Arithmetic/plumbing validation

Contracts CT-17–19 use separately supplied synthetic utility rows and exercise R1 loss, exact tie, and R1 win against the comparators. All pass. They test arithmetic response only; the fixture utilities were constructed to produce each relation and are not task-runner outcomes. CTs also verify same-task pairing, a common no-candidate baseline, K/H, and cost conditions.

## Blocking endpoint limitations

- No actual future-task runner, utility map, task-quality adjudicator, or independent task suite is present in the audited Phase 1C implementation.
- No calibration-derived cost conversion, validated cost components, or numerical `λ` is frozen. The code requires a frozen model ID and `λ`; supplied fixture values are placeholders, not calibration.
- The endpoint's future-task horizon and cross-family/family-template blocks are not instantiated.
- The outcome store is not sealed or access-audited in production.
- Phase 1C specifies unavailability when missingness exceeds 5% or differs by more than 2 percentage points, but does not provide an estimator for missing outcomes below those limits. The Phase 3A engine conservatively rejects any missing paired outcome rather than silently converting it to zero. This fail-closed behavior is a disclosed unresolved spec item that must be settled before calibration/preregistration; it is not presented as a completed reproduction of the missingness rule.

## Endpoint verdict

**Arithmetic contract: PASS on synthetic rows. Independent FNTU@K measurement: BLOCKED.** No endpoint result here supports or refutes IDT.