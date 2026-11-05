# P6 Deliverables — Implementation Blueprint

**Blueprint:** `T2T-P6-Blueprint-v1.0.0-draft`  
**Status:** complete for design/documentation scope, 2026-11-04.  
**Boundary:** P6 itself is a design package. After P7, a separate narrowly scoped local/synthetic Step 1 was authorized and implemented; it does not change P6's design-only status or authorize experiments, benchmarks, ARC runs, split assignment, or restricted-outcome access. See [`step1_event_journal_plan.md`](../implementation/step1_event_journal_plan.md).

## Normative design documents

- [`architecture_v1.md`](architecture_v1.md) — component architecture, trust boundaries, data flow, runtime/baseline interfaces, deployment alternatives and budget ledger proposal.
- [`event_schema_v1.md`](event_schema_v1.md) — design semantics for immutable events.
- [`event_schema_v1.json`](event_schema_v1.json) — machine-readable Draft 2020-12 schema instantiated for the separate synthetic prototype only; its local digest profile does not resolve P2 production canonicalization.
- [`contract_test_plan_v1.md`](contract_test_plan_v1.md) — synthetic contract-test design. The separately authorized Step 1 implements/runs a focused subset of event-journal tests; it does not execute the full P6 test plan.
- [`../implementation_blueprint.md`](../implementation_blueprint.md) — entry point to this versioned blueprint.

## P6.1–P6.3 results

- **P6.1 Architecture:** components and trust boundaries are defined; CandidateVersion cannot flow directly to runtime; runtime and baseline adapters share a wrapper/logging contract; evaluator outcomes are isolated from construction/refinement.
- **P6.2 Event schema:** event envelope/order/immutability semantics and event-specific required references are specified. P2 records remain authoritative; P4 fine-grained triage stays in its sidecar; unknown remains distinct from false/absent.
- **P6.3 Contract tests:** test requirements and synthetic fixtures are catalogued, including negative/security and budget-parity cases. They are not test results or scientific evidence.

## Open decisions and approval gate

The Step 1 prototype locally uses Python, JSON Schema Draft 2020-12, `jsonschema`, single-writer JSONL and a clearly labeled Python-only digest profile. These choices apply only to synthetic local tests. Production database/deployment, P2-compatible canonicalization and ID profile, schema registry/migration, security controls/retention, runtime/evaluator integration, numerical resource caps, and named engineering/security reviewers remain `UNSET` or require owner review. Broader implementation or any restricted evaluation still requires separate authorization and all upstream P1–P5/project controls.

P6 design-packet QA at completion checked 62 Markdown files and 232 relative links with zero broken links. The separate Step 1 later meta-validated the machine-readable schema and ran only `tests/test_t2t_eventlog.py` on synthetic fixtures; this does not turn the P6 plan into an ARC test, benchmark, or scientific result.
