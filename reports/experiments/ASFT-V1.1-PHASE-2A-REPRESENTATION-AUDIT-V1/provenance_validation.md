# Phase 2A — Provenance and Package QA

## Validation results

- **Historical source records:** 36 selected implementation, configuration, saved-output, and prior-audit files covering Phase 13G, relevant Phase 14 reviews, selected Phase 1 specifications, the frozen ARC split manifest, and the generic grid helper.
- **Phase 2A artifacts fingerprinted:** 11 (the nine requested deliverables, README, and this report).
- **SHA-256:** all 47 records in `source_manifest.json` matched their recorded digests after package completion. `source_hashes.csv` carries the same 47 source/artifact records; the manifest and hash index are intentionally not self-hashed.
- **CSV/JSON parsing:** all four CSV files parsed (including the hash index); the manifest JSON parsed. The three audit tables have 24 primitive-inventory rows, 26 expressivity rows, and 20 coverage-audit rows.
- **Local Markdown links:** all 12 checked package-relative links resolve.
- **Coverage table arithmetic:** observed program-category counts sum to the reported bounded demo-fit totals: discovery 3/600, transfer 5/200, holdout 2/200. These are historical saved-output counts, not new task scoring.
- **Evidence scope:** read-only review of saved Phase 13G implementation and outputs. No task data were rerun/scored, no new ARC accuracy or coverage estimate was produced, and no official evaluation data were parsed or scored.

A file hash establishes lineage, not representational adequacy, causal attribution, or scientific validation. This QA pass validates package integrity and internal arithmetic, not ARC performance, the Phase 13G protocol, or the representation-bottleneck hypothesis.