# Phase 1D.5 — Memory Comparator Framework

## Required systems

| Arm | Definition | Role |
|---|---|---|
| B1a — M1 Exact Episodic | Keyed task/solution exemplars; exact replay only when the predeclared match rule passes. | Memory sufficiency control / Family A positive control. |
| B1b — M2 Partial Episodic | Bounded trace fragments and subproblem outputs with context requirements. | Tests whether partial examples suffice without generalized rules. |
| B1c — M3 Pattern Memory | Repeated patterns and associations retrieved by frozen similarity rule; no explicit rule abstraction. | Stronger memory-only comparator than a single exact-match arm. |
| B2 — M4 Abstraction Only | Explicit generalized skills/rules extracted from training; no episodic examples or answer cache. | Primary abstraction arm. |
| B3 — M5 Hybrid | M1/M2-style evidence plus M4 rules under the same total budgets. | Tests complementarity. |
| B4 — Random Retrieval | Uniform seeded retrieval from the same eligible episodic candidate pool under the same retrieval limit. | Retrieval-policy control. |
| B5 — No Learning | Frozen base solver; no learned task store or abstraction store. | Baseline. |
| B6 — Oracle | Evaluator knows the hidden task program/gold answer after lock. | Analysis-only upper bound; excluded from tuning, primary contrasts, and budget parity. |

## Primary comparisons

The primary outcome is the macro-average over challenge families B–F (the non-exact families), with each family equally weighted. Compare B2 Abstraction against each B1 memory-only variant (B1a, B1b, B1c) using paired panel-level differences and multiplicity control. This prevents selecting a favorable memory baseline after outcomes. Family A is a predeclared positive-control stratum and is not included in the primary abstraction-necessity average.

B3 Hybrid is compared secondarily against B2 and all B1 variants; report the Family C composition interaction separately. B4 and B5 are mandatory context controls. B6 is never a feasible comparator. Report all arm results, even if the predeclared primary claim fails.

## Isolation rules

M4 receives no raw episodic examples beyond the common training episodes used to build its abstract rule store. M1–M3 receive only their specified representations. B3 combines allowed representations but shares all caps. Random retrieval differs only in retrieval choice, not store size, candidate pool, or exposure. No arm receives more future tasks or evaluation retries.