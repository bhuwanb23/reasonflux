# Phase 1H.4 — Ablation Taxonomy

Ablations are controlled component removals. Each has a manipulation check, a specific claim, an estimand, and a local interpretation boundary. No component is presumed necessary.

| ID | Ablation | Claim tested | Manipulation/check |
|---|---|---|---|
| A1 | No IDT / no invariant discovery | Does invariant discovery/ranking add value beyond the same candidates/solver without IDT? | Disable proposal/ranking contribution; verify invariant layer inactive while candidate pool and downstream budgets are controlled. |
| A2 | No SCT / no skill trigger/formation policy | Does the SCT trigger/formation policy add value over a declared no-trigger alternative? | Disable trigger logic; separate skill storage/reuse if those remain. |
| A3 | No SCV / no SCV-based selection | Does SCV scoring change selection/outcomes beyond common-pool alternatives? | Hold eligible pool fixed; replace SCV ranking with declared no-SCV or matched random policy; log decision divergence. |
| A4 | No transfer mechanism | Does transfer-aware reuse/application add value on held-out transfer tasks? | Disable transfer-informed application, preserve an external transfer evaluator and matched no-transfer policy. |
| A5 | No capability layer | Does capability formation/measurement contribute to behavior or only internal scores? | Disable capability formation/metric computation; task behavior remains scored; metric fields become unavailable, not zero. |
| A6 | No lifecycle | Do persistence/retirement/reactivation rules add value? | Disable lifecycle transitions while preserving initial skill set; record whether any lifecycle decision would otherwise fire. |
| A7 | No composition | Does composing skills improve held-out composed tasks? | Disable skill composition; retain base/single-skill actions and same task set. |
| A8 | No memory | Does persistent episodic/retrieval memory add value beyond remaining learning mechanisms? | Disable the declared memory store/retrieval path; specify whether weights/skills or external state remain. |
| A9 | No ARC extension | Does the ARC-specific representation/parser/search extension add value? | Disable only the extension; compare on a common supported task subset and separately report coverage differences. |

## Claim map

- IDT/ranking → A1
- SCT/formation → A2
- SCV selection → A3
- Transfer → A4
- Capability layer → A5
- Lifecycle → A6
- Composition → A7
- Memory/retrieval → A8 (paired with BL2)
- ARC extension → A9 (Phase 1G only)

A2 and A3 are distinct: removing the trigger/formation mechanism is not the same as removing SCV-based selection. A5 can change or mask internal metrics without changing behavior; it is not a performance ablation unless external task outcomes differ.