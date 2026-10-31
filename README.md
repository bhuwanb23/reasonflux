# ASFT — Adaptive Skill Formation Theory

Research prototype for the ARC Prize Paper Track.

**Core claim:** Intelligence grows by converting repeated reasoning traces into reusable skills that reduce future reasoning cost.

```
Reasoning Trace → Invariant Discovery → Concept Formation → Skill Creation → Future Cost Reduction
```

## Research contributions

1. **Invariant Discovery Theory (IDT)** — transferable knowledge as invariants across reasoning experiences (`src/traces`, `src/invariants`)
2. **Skill Creation Trigger Theory (SCT)** — create a skill when Skill Creation Value (SCV) > threshold (`src/skills`)
3. **Capability Growth Metrics (CGM)** — measure transfer and capability growth, not only task accuracy (`src/evaluation`)

## Run

```bash
pip install -e .
# or
pip install -r requirements.txt

# end to end: tasks → traces → invariants → skills → reuse → capability growth
python -c "from pipelines.full_asft_pipeline import run_full_asft_pipeline; print(run_full_asft_pipeline().summary)"

# experiments (write reports/ + figures/)
python experiments/exp05_end_to_end/run.py

pytest tests/
```

All pipelines are implemented; nothing under `src/` raises `NotImplementedError`.

## Architecture

Repository layout maps directly to research contributions. See [docs/architecture.md](docs/architecture.md), [docs/metrics.md](docs/metrics.md), [docs/experiments.md](docs/experiments.md), and [docs/roadmap.md](docs/roadmap.md).

```
Task → Trace Logger → Trace Store → Invariant Detector → Skill Trigger
    → Skill Library → Transfer Engine → Evaluation Engine → Reports
```

## What is not in v0.1

LLMs, neural networks, meta-reasoner, concept graphs, ARC-3 agents, world models, autonomous planning.

## Research docs

Detailed research phases live under [`docs/`](docs/) (literature, thesis, prototype design, paper blueprint, implementation plans).
