# T2T Local Implementation Step 1 — Event Validation and Append-Only Journal

**Plan ID:** `T2T-Impl-Step1-EventJournal-v1.0.0-draft`  
**Authorization:** user explicitly approved a local-only synthetic prototype for event-schema validation and an append-only journal. Scope is limited to this step.  
**Status:** COMPLETE for the narrow local/synthetic scope, 2026-11-04. M0–M4 outcomes and focused verification are recorded below.  
**Date:** 2026-11-04.

## 1. Objective

Create a minimal Python implementation that validates the P6 event contract and appends, reads, and verifies an immutable local event journal. This is engineering plumbing only; it is not the T2T method, a scientific result, or an ARC-AGI-3 agent.

## 2. Hard scope boundary

### Allowed in this step

- New isolated package under `src/t2t_eventlog/`.
- A machine-readable event schema derived from P6 and consistent with P2/P4 semantics.
- Local single-file append-only journal and integrity verification.
- Synthetic fixtures and tests in a new isolated test module.
- Minimal dependency declaration for JSON Schema validation, if needed.

### Explicitly out of scope

- Reading or modifying existing datasets, traces, task IDs, split files, hidden/test/confirmatory outcomes, evaluator receipts, or leaderboard material.
- Network, APIs, credentials, model calls, external evaluators, live environments, ARC runs, benchmarks, candidate/skill execution, or data assignment.
- Changes to Phase 2I, Phase 3B/3D, existing experiment code/results, global test behavior, or unrelated dirty working-tree files.
- A production storage/security claim, event-store deployment, multi-host writer support, cross-language hash compatibility, or scientific/competition result.

The current worktree contains numerous pre-existing modifications and untracked files. Do not clean, stage, revert, or edit anything outside this plan's explicit file list.

## 3. Implementation choices for this local prototype

These choices are deliberately **prototype-local** and do not resolve P2's production ID/canonicalization decisions or P6's deployment/security questions:

1. **Language:** Python, compatible with the repository's declared Python `>=3.10`.
2. **Schema:** JSON Schema Draft 2020-12, matching the existing P2 schema dialect; strict event envelope and payload fields.
3. **Validator:** `jsonschema` library, declared as a dependency so validation does not rely on an undeclared environment package.
4. **Journal format:** newline-delimited JSON, local path only, one process/writer at a time; append writes and `fsync`; no update/delete API. POSIX advisory file locking prevents concurrent writer races in this prototype. Multi-host/multi-process deployment is not supported.
5. **Event IDs:** generated UUIDs for local journal events; synthetic test references use obviously synthetic fixture strings. These do not define the project-wide P2 ID scheme.
6. **Digest profile:** `t2t-python-json-c14n-v1` is prototype-only: UTF-8 JSON with sorted object keys, compact separators, `ensure_ascii=False`, and `allow_nan=False`; SHA-256 digest is calculated over the envelope excluding its own `content_digest` but including the preceding journal digest when present. This profile is not claimed to be RFC 8785 or cross-language compatible and does not replace P2's unresolved canonicalization profile.
7. **Journal ordering:** `stream_seq` is monotone per stream. Journal hash chaining is global and append order is authoritative. Record timestamps are UTC; the writer produces strictly increasing timestamps within a stream for the pre-action ordering check. Source/environment timestamps remain separate payload values.
8. **Restricted outcomes:** the general journal rejects answer-bearing evaluator outcome events entirely; no restricted-outcome store or evaluator integration is implemented.

## 4. Milestones and acceptance criteria

### M0 — Freeze the prototype boundary

- [x] Record authorized scope, excluded data/actions, and isolated file set.
- [x] Select Python, JSON Schema dialect, local journal and prototype-only digest/ID profile with limitations.

### M1 — Machine-readable schema and validator

- [x] Add a strict `event_schema_v1.json` under P6 docs, including supported event types and tagged values.
- [x] Validate schema syntax/dialect and event fixtures using the declared validator.
- [x] Reject unknown types/versions, unexpected fields, malformed refs/digests, and restricted outcome event types in the general journal.
- [x] Preserve `UNKNOWN`, `NOT_APPLICABLE`, known false, and absent as distinct states.

### M2 — Append-only local journal

- [x] Implement `EventJournal` append, read, and verify operations only.
- [x] Validate every event before writing; assign event UUID, stream sequence, timestamp, digest profile and previous digest at append time.
- [x] Use append-only writes and fsync; detect/reject malformed lines, changed bytes, broken hash chain, duplicate IDs, missing causal parents and sequence regressions. POSIX advisory locking serializes local concurrent appends; it is not multi-host storage.
- [x] No update/delete method. Corrections are new events referencing the superseded event.
- [x] Keep journal code free of network, dataset, model and evaluator integrations.

### M3 — Synthetic contract tests

- [x] Valid/invalid schema parsing; unknown/absent/false/NA distinctions.
- [x] Deterministic digest for a fixed canonical envelope; content change causes digest change.
- [x] Append/read/reopen/verify; monotone sequence/timestamps and hash chain.
- [x] Tamper, truncation, invalid JSON, duplicate ID, missing parent, sequence regression, and concurrent writer serialization/monotone sequence cases.
- [x] Prediction event must precede dependent action dispatch; required missing and late prediction order are rejected. Equal timestamps are rejected.
- [x] Correction appends and does not mutate the original.
- [x] CandidateVersion event cannot carry executable policy; restricted evaluator outcome type is rejected.
- [x] All tests use only temporary directories and synthetic fixture strings; no global tests run.

### M4 — Documentation, audit and completion

- [x] Add module README/API notes, exact prototype limitations, and reproducible isolated test command.
- [x] Update this plan with actual files, exact focused test results, and unresolved issues.
- [x] Run only targeted tests for the new module plus static/schema consistency checks; do not run the repository-wide suite or any experiment.
- [x] Verify no unrelated working-tree files were intentionally edited by this task.

## 5. In-scope file list

Expected files, and no others unless this plan is amended:

- `docs/05_trace_to_transfer/implementation/step1_event_journal_plan.md`
- `docs/05_trace_to_transfer/p6/event_schema_v1.json`
- `src/t2t_eventlog/__init__.py`
- `src/t2t_eventlog/errors.py`
- `src/t2t_eventlog/schema.py`
- `src/t2t_eventlog/canonical.py`
- `src/t2t_eventlog/journal.py`
- `src/t2t_eventlog/README.md`
- `tests/t2t/test_t2t_eventlog.py`
- `pyproject.toml` and `requirements.txt` only for the explicitly declared validator dependency.
- `docs/05_trace_to_transfer/p6/README.md`, `p6/event_schema_v1.md`, `phases/p6.md`, `subphases/p6_2.md`, `subphases/p6_3.md`, `implementation_blueprint.md`, `README.md`, and `master_plan.md` only for narrow status/boundary notes. These were added to M4 on 2026-11-04 because prior statements that no local validator or tests existed became stale after the separately authorized implementation; no method or empirical design was changed.

No generated journal/test data is committed; tests use temporary directories. Do not alter P2's JSON schema or canonicalization text.

## 6. Completion definition and stop conditions

Complete Step 1 only if all M1–M4 checks pass, the exact test command is recorded, tests operate solely on synthetic fixtures/temp files, and scope remains confined to the file list. Any request to use live data, hidden outcomes, real task IDs/splits, an evaluator, network/model calls, or environment actions stops this step and requires a new authorization/review. Passing tests establishes engineering behavior only; it does not authorize experiments, benchmark claims, skill execution, or ARC-AGI-3 access.

## 7. Final result log

**M0–M4 complete, 2026-11-04, for local synthetic plumbing only.**

- Added `docs/05_trace_to_transfer/p6/event_schema_v1.json`, Draft 2020-12 schema with 22 event variants; added isolated package `src/t2t_eventlog/` (`__init__.py`, `errors.py`, `schema.py`, `canonical.py`, `journal.py`, `README.md`).
- Added `tests/t2t/test_t2t_eventlog.py` with synthetic fixtures and temporary paths; declared `jsonschema>=4.18,<5` in `pyproject.toml` and `requirements.txt`.
- `python -m pytest -q tests/t2t/test_t2t_eventlog.py` — **PASS: 19 passed**. Coverage includes every declared event type, invalid schema cases, tagged-value distinctions, ordering, append/reopen/verify, digest tampering, malformed/truncated logs, duplicate IDs, missing parents, sequence/timestamp regressions, corrections, restricted outcome rejection, and concurrent local appends serialized under lock.
- `python -m compileall -q src/t2t_eventlog tests/t2t/test_t2t_eventlog.py` — **PASS**.
- Draft 2020-12 meta-schema and pyproject/requirements dependency consistency — **PASS**; 22 variants confirmed.
- Focused relative-link QA across `docs/05_trace_to_transfer/` — **PASS**, 67 Markdown files and no missing relative targets.
- Package-source scan for network imports/calls/URLs — **PASS**, none found. No repository-wide test suite, experiment, benchmark, ARC task/data, split, model, evaluator, environment, or outcome access was used.

**Known limitations / unresolved:** this is a local POSIX prototype; `flock` serializes local appends but does not provide multi-host service guarantees. The head checkpoint and hash chain detect accidental corruption/truncation but are not tamper-proof against a writer who can rewrite both. `t2t-python-json-c14n-v1` is not RFC 8785 or cross-language compatible and does not resolve P2 production IDs/canonicalization. Journal event ordering does not load or validate the contents/timestamps of referenced external P2 records. Production storage, deployment, access control, retention, migrations, canonicalization, and security review remain unset. No T2T method implementation or scientific/competition evidence is produced by this step.

Only the files listed in §5 plus the explicitly amended M4 boundary/status documentation were written for this step. Pre-existing dirty/untracked worktree state was not cleaned, staged, or reverted.
