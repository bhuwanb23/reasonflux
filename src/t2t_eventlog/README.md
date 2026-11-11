# `t2t_eventlog` — Local Synthetic Prototype

This package is the authorized Step 1 implementation of the T2T P6 event-schema/journal plan. It is a **local engineering prototype**, not the T2T candidate/skill method, an ARC agent, a benchmark, or a scientific result.

## Scope and safety limits

- Synthetic/local references only; the writer requires `SYNTHETIC_FIXTURE` access classification.
- No network, dataset, model, evaluator, environment, task/split, or hidden-outcome integration exists in the package.
- Do not use this package with real ARC, validation, confirmatory, hidden/test, or restricted data.
- The journal is a single-machine, single-writer JSONL prototype using POSIX `flock`. It is not a production database, multi-host service, secure access boundary, or tamper-proof archive.
- `t2t-python-json-c14n-v1` is a local Python digest profile only. It does not resolve P2's project-wide identity/canonicalization decision or claim cross-language stability.
- `CandidateVersion` events are references to non-executable P2 objects. This package contains no candidate/skill executor.
- `EVALUATOR_OUTCOME_RECORDED` is intentionally excluded from the general event schema.

## Local API

`validate_event(event)` validates an in-memory event against the machine-readable Draft 2020-12 contract at `docs/05_trace_to_transfer/p6/event_schema_v1.json`.

`EventJournal(path).append(event_template)` validates and appends one synthetic event. The journal assigns a UUID event ID, schema version, monotonically increasing per-stream sequence and timestamp, and a SHA-256 digest linked to the preceding event. `read_all()` and `verify()` recheck the event schemas, references, semantic ordering, digest chain, and local head checkpoint. Ordering checks establish event-journal order for referenced prediction/action records; they do not resolve or validate the contents/timestamps of external P2 record blobs. No update/delete API exists; a correction is a new event referencing the prior event.

The journal creates a `.head.json` checkpoint to detect accidental valid-prefix truncation and a `.lock` file for local process coordination. The checkpoint is mutable integrity metadata, not part of the event stream and not a cryptographic anti-tamper control. A determined writer who can alter both log and checkpoint can recompute both; protect the directory separately in any later authorized deployment.

The append template should use `stream_id`, `activity_ref`, and all artifact/producer references namespaced as `synthetic:` or `local:`. `access_class_ref` must be `SYNTHETIC_FIXTURE` or `synthetic:access:SYNTHETIC_FIXTURE`; optional `data_role_ref` must be synthetic/local. `event_id`, `recorded_at`, `stream_seq`, schema version, and integrity are journal-controlled and must not be supplied.

## Focused tests

From the repository root, run only:

```bash
python -m pytest -q tests/t2t/test_t2t_eventlog.py
```

This command targets synthetic temporary-file contract tests only. Do not infer that these tests authorize or validate empirical work. No repository-wide suite or experiment is invoked by the command above.
