# ASFT v1.1 — Phase 2I-A Candidate Production Enablement

**Package ID:** `ASFT-V1.1-PHASE-2I-A-CANDIDATE-PRODUCTION-ENABLEMENT-V1`  
**Status:** WP0-WP2 core implementations complete with effect-based reflection aliases; WP3 rubric and 600 train-only annotation packets prepared, with a separate 12-task non-qualifying AI pilot; genuine coding remains on hold; WP4 candidate policy/identity config is owner-approved and tested; WP5 synthetic HCC plumbing control implemented/tested; WP6 paired runner, train-only source, search adapters, resource bounds, and synthetic artifact audits implemented/tested; real ARC run remains blocked  
**Purpose:** Make the already specified Phase 2I experiment executable—without running it, producing candidates, or opening Phase 3.

This is an engineering work order, **not another readiness phase** and not an empirical result. It preserves the Phase 1C ranked object (`Invariant` candidate), Phase 2I's R1-vs-R3 diagnostic design, discovery-only data boundary, and frozen thresholds. It neither changes the candidate construct nor interprets Phase 2H's zero yield as impossibility.

## Decision recorded

- **HCC:** BUILD as a separate, synthetic plumbing control, because Phase 2F's framework requires a positive-control generator/oracle check before representation comparison. HCC records must be technically isolated and excluded from every ARC numerator, denominator, registry, and claim.
- **ARC candidate run:** NOT AUTHORIZED by this work package. Finish implementation, annotation, tests, hash/config freeze, and a run-specific protocol first. No ARC demonstrations or test outcomes were processed here.
- **WP3 AI pilot:** a 12-task, train-only, rubric-conditioned AI pilot is stored in `wp3_ai_pilot_v1/`. It is explicitly exploratory and nonqualifying: same AI assistant made both passes and adjudication, so no independent annotations, family eligibility labels, or WP3 completion are claimed.
- **Synthetic HCC control:** `ASFT-2I-HCC-SYNTH-V1`: 120 in-memory synthetic tasks, six known rules (20 each), three synthetic layout cohorts (40 each), 240 train-demo equivalence checks per arm, six matching generator-accepted and structurally eligible candidates per arm. This validates plumbing only; it is not an ARC HCC, candidate-yield estimate, or scientific result. Candidate mining uses explicit oracle-selected one-action fixtures to isolate the miner; it does not validate R1/R3 search coverage or the complete production trace integration.
- **Repository safety:** The working tree already contains unrelated pending changes. This work package adds files only; implementers must not revert, stage, or rewrite unrelated work.

## Contents

- `implementation_work_package.md` — scope, dependency order, owners/outputs, and completion criteria.
- `wp0_wp6_end_to_end_summary.md` — plain-language status and evidence for each WP0–WP6, including the remaining WP3 blocker.
- `r3_grammar_addendum_v1.md` — owner-approved, frozen R3 grammar semantics for WP1.
- `r3_implementation_contract.md` — R3 specification carried forward from Phase 2F plus semantic ambiguities that must be resolved and frozen before code.
- `semantic_trace_adapter_contract.md` — common event interface, leakage controls, and validation status.
- `family_annotation_protocol.md` — primary family ontology, blind coding rubric, agreement/adjudication plan.
- `annotation_packets/` — two blank train-only packets for the 600 discovery IDs plus packet manifest; independent coding is held pending coders.
- `wp3_ai_pilot_v1/` — 12-task AI-only pilot, descriptive agreement, and rubric debugging notes; explicitly not independent, not eligible, and not a WP3 label map.
- `wp4_policy_identity_resolution.md` / `wp4_runtime_config_v1.json` — owner-approved candidate-stage, taxonomy, identity, and runtime settings; frozen for WP4.
- `experiments/phase2ia/hcc_control.py` — in-memory, namespace-isolated six-rule synthetic control generator/oracle/miner plumbing; no ARC task loader or registry writes.
- `tests/test_phase2ia_hcc_control.py` — deterministic control/equivalence and negative namespace-contamination tests.
- `experiments/phase2ia/runner.py`, `search_adapters.py`, and `train_only_source.py` — paired R1/R3 runner, registered bounded search callbacks, and path-confined streaming train-only loader.
- `tests/test_phase2ia_runner.py` and `test_phase2ia_train_only_source.py` — synthetic file-to-search-to-trace-to-audit replay, forbidden-sentinel, resource/path bounds, HCC exclusion, and no-authorization tests.
- `task_breakdown.csv` — sequenced implementation tasks and acceptance evidence.
- `ambiguity_register.csv` — decisions that cannot be silently guessed from the current R3 specification.
- `package_manifest.json` — package status, scope locks, and integrity summary.

The authoritative scientific protocol remains Phase 2I: `../ASFT-V1.1-PHASE-2I-INVARIANT-CANDIDATE-PRODUCTION-V1/`. This package only addresses its execution prerequisites.
