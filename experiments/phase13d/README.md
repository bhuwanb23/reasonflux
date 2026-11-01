# Phase 13D implementation

Experiment-local modules only; global solver and historical metrics are unchanged. Run contract tests with `python -m pytest tests/test_phase13d_contracts.py`; run the frozen ten-seed benchmark only after contract checks and hash freeze with `python -m experiments.phase13d.cli --run`.

The transfer interpreter is a deterministic synthetic simulator. `solver_search_candidates` is deliberately null because the existing solver does not expose a canonical candidate-search counter. B4 is a repeated-trace compression proxy, not DreamCoder.
