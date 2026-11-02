# Phase 2C.4 — Runtime Integrity Framework

## Objective

For every future search run, make **declared budget = runtime-enforced budget = logged budget** a machine-checked acceptance condition. A run with a mismatch is a protocol violation; it must not be interpreted as valid evidence.

## Required fingerprints (R1–R4)

1. **R1 — Config hash:** SHA-256 of frozen JSON/YAML config and budget registry, captured before runtime; copy hashes into every run manifest and budget audit.
2. **R2 — Runtime hash:** SHA-256 over the executed runner, imported search/representation/miner source files, Python version, and platform/environment identity. A change requires a new run ID.
3. **R3 — Search-log hash:** SHA-256 of task-condition search log, per-candidate trial log, replay log, and their canonical composite. Append-only logs must be finalized before analysis.
4. **R4 — Budget audit record:** machine-readable per-condition record comparing config, registry, runtime-enforced values, observed usage, and logged values for B1–B6.

The Phase 2C benchmark creates `runtime_integrity_record.json`, `budget_audit_record.json`, `run_manifest.json`, and hashed logs implementing these checks.

## Budget parity fields

| ID | Required declared/runtime/logged fields | Fail condition |
|---|---|---|
| B1 Candidate budget | Requested candidate cap, enforced cap, unique candidate pool, actual evaluated trials, and unused cap slots | Config/registry cap mismatch, trial count above cap, or unreported finite-pool truncation |
| B2 Search depth | Search depth, composition flag, and runtime value | Any depth/composition mismatch |
| B3 Trace budget | Trace count cap, max steps, actual emitted/valid/successful/pruned counts | Trace count/steps above declared ceiling or count mismatch |
| B4 Runtime | Wall-clock ceiling and observed per-search elapsed time | Missing/nonmatching cap or any search over cap |
| B5 Memory | OS-enforced address-space/memory ceiling and observed peak memory | Missing/nonmatching cap or cap exceeded |
| B6 Evaluation | Primary/replay task IDs, split counts, total search invocations, and task-ID manifest hash | Duplicate/missing task, split mismatch, unregistered extra run, or log-count mismatch |

## Runtime protocol

- Load one frozen registry; do not duplicate hand-entered budgets in solver call sites.
- Before first task, hash config, registry, runtime code, dataset split manifest, and training-source manifest.
- Log a row before/after every task-condition search with run ID, task ID, split, condition, B1–B6 values, candidates available/generated/evaluated, trace ID/status, runtime, and selected candidate.
- Log candidate-level ordinal/program/context/result; distinguish candidates omitted by the configured budget, skipped after first-fit stopping, and actually pruned. Never conflate these.
- On any budget inconsistency, timeout, memory violation, data-access violation, trace-validation failure, or replay mismatch: set `protocol_violation`, preserve logs, stop analysis, and do not report a coverage/accuracy result as valid.
- Verify deterministic replay on the same task IDs before outcome interpretation. A replay is an integrity check, not an independent sample.
- Keep coverage-only and accuracy evaluation paths separate. Any test-label evaluation must be independently authorized, sealed, and recorded under its own evaluation budget.

## Phase 13G status versus Phase 2C status

Phase 13G did not implement these four fingerprints as a unified runtime gate. The Phase 2C run does: config/registry and source hashes are recorded; candidate logs are hashed; budget parity and deterministic replay are machine checked. This framework is enforceable for the instrumented runner, but does not retroactively make Phase 13G protocol-compliant.