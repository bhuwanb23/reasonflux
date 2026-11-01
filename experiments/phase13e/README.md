# Phase 13E runner

The preregistered configuration and protocol are `config.json` and `preregistration.md`. The independent confirmatory block is seeds 60–69. The runner calls the existing repository trace, invariant, skill, transfer, capability, composition, and growth APIs; Phase 13C/13D records are not reused as Phase 13E outcomes.

Before confirmation, run the contract tests:

```bash
PYTHONPATH=src:. python -m pytest -q tests/test_phase13e_contracts.py
```

After protocol/config/source review, start confirmation once:

```bash
PYTHONPATH=src:. python -m experiments.phase13e.cli --confirm
```

The CLI refuses to overwrite existing Phase 13E evidence. It writes source/config hashes before the first seed, checkpoints completed seeds in `partial_results.json`, and then creates the evidence package at `reports/experiments/PHASE-13E-CAP-GROWTH-V1/`. If a run stops partway, preserve the manifest and partial records; do not silently restart over them.

B4 is explicitly a compression-only synthetic proxy, not canonical DreamCoder. A5 is behavior-matched to ASFT but masks CGM outputs. EXP-CAP-21/22 are isolated copied-portfolio probes and never modify the primary benchmark portfolio.
