# Implementation Blueprint — Entry Point

**Controlling design proposal:** [`T2T-P6-Blueprint-v1.0.0-draft`](p6/README.md)  
**P6 status:** complete for design/documentation scope. The P6 document itself is not a broad implementation or execution authorization.

The versioned P6 packet maps the P2–P5 contracts to logical modules and trust boundaries, data flow, runtime/baseline interfaces, a typed immutable event contract, synthetic contract-test requirements, and a P3/P5-aligned cost ledger. P2 record definitions, P3 arm fairness, P4 candidate/triage behavior and P5 data/run restrictions remain controlling; P6 does not extend or override them.

## Separately authorized follow-on

After P7, the user separately authorized [Local Implementation Step 1](implementation/step1_event_journal_plan.md): event-schema validation and a local append-only journal using synthetic fixtures only. Its implementation lives under `src/t2t_eventlog/`; its focused tests are `tests/test_t2t_eventlog.py`. It has no network, ARC data, model, evaluator, task/split or restricted-outcome integration. The prototype digest/ID/storage choices are local and do not settle production P2/P6 decisions.

This narrow authorization does not permit building/running the T2T method, candidate/skill execution, live-system tests, data access, benchmarks, ARC runs, split assignment or restricted outcomes. Any expansion requires a new scoped authorization and existing project/data/competition gates.
