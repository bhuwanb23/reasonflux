# Phase 2C — Provenance and QA Validation

## Final package integrity

- **Source/artifact records:** 1,091 SHA-256 records in `source_manifest.json` and `source_hashes.csv`: 1,000 ARC task files, 65 Phase 2C protocol/runtime and historical-source records, and 26 Phase 2C package artifacts.
- **Hash integrity:** all recorded files matched their hashes. The 1,000 task-file raw-byte hashes matched both the ARC source manifest and frozen split manifest. Raw-file hashing is source-lineage QA; the Phase 2C runner parses only training demonstrations and does not parse/use task test-output fields.
- **R1–R4:** config and registry hashes match `run_manifest.json`; the R2 runtime hash covers the executed runner, Phase 13G implementation and invariant-miner dependencies, Python/platform; R3 matches the composite hashes of search, candidate-trial, and replay logs; R4 matches `budget_audit_record.json`.
- **Budget parity:** config, YAML registry, runtime-enforced values, and logs match for B1–B6 across primary and replay records. Runtime status is PASS; there is no `protocol_violation` artifact.
- **Search/replay counts:** 4,000 primary task-condition rows and 4,000 cold-cache deterministic replay rows; all 4,000 replay fingerprints match. Candidate-trial logs contain 28,918 ordered attempts and reconcile to primary counts. S3 and S4 produce identical task-level searches because the DSL contains ten unique programs.
- **Historical reconstruction:** Phase 13G primary discovery, stability, arm, transfer-probe, and coverage-scan reconstruction totals reconcile to 11,005 solver calls / 77,863 candidate trials, explicitly labeled reconstructed rather than original-run logs. The 600-task historical stability replay matched all saved primary trial costs and stability values; transfer probe reconstruction used training demonstrations only.
- **Format/count checks:** all 10 CSVs, 8 JSON files, and the YAML registry parse. Core row counts: search inventory 16; primary execution 4,000; candidate trials 29,918; replay 4,000; historical stability permutations 6,000; historical stability tasks 600; transfer probe summary 10; budget sensitivity summaries 4 aggregate / 16 split rows.
- **Local Markdown links:** all 39 package-relative links resolve.
- **Accuracy:** `NOT_MEASURED_BY_DESIGN`; no Phase 2C accuracy, leaderboard, or confirmatory mechanism claim was computed.

## Claim boundary

QA verifies lineage, declared/runtime/logged budget consistency, search-trial reconciliation, and deterministic behavior for this instrumented test-blind runner. It does not make Phase 13G historically budget-compliant, prove semantic representability limits, or establish representation or search as the sole/primary cause of ARC outcomes.