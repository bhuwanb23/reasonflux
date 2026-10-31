# Docs

This folder is the project’s research, design, and status record. It is organized by concern, not by phase numbering alone.

## Layout

- [`00_project/`](00_project/) — project-level status and roadmap. Start with
  [`v0_1_readiness.md`](00_project/v0_1_readiness.md) for the honest go/no-go.
- [`01_research/`](01_research/) — research record: literature, thesis work, contributions, novelty checks, compression, prototype-design rationale, and experimental design.
- [`02_design/`](02_design/) — implementation design specs for the prototype.
  [`implementation_blueprint.md`](02_design/implementation_blueprint.md) is the
  module registry and build spec (Phase 11F).
- [`03_implementation/`](03_implementation/) — implementation planning material, including module plans and phase plans.
- [`04_paper/`](04_paper/) — paper-facing material: the experiment map and
  [`claim_traceability.md`](04_paper/claim_traceability.md).
- [`99_chats/`](99_chats/) — supporting chat transcripts.

## Rule

- Keep research docs in `01_research/`.
- Keep implementation design/docs in `02_design/` and `03_implementation/`.
- Keep paper-facing maps in `04_paper/`.
- Do not create two docs for the same topic. If something already exists, update it or point to it.
