# Failure Modes and Edge Cases (Phase 11C-5)

Final IDT hardening before SCT. Code under `src/invariants/robustness/`.
Thresholds: `configs/thresholds.yaml` (`robustness:`).

**Principle:** An invariant is not trusted because it exists. It must survive
variation, meaningful transfer, noise, conflicts, and negative-transfer checks.

## Failure taxonomy (F1–F7)

| ID | Category | Detection | Safeguard |
| --- | --- | --- | --- |
| F1 | Spurious invariants | VST from variation metadata | Reject below `min_vst` |
| F2 | Invariant explosion | IER = invariants / traces | Restrict when IER ≥ `ier_restrict` |
| F3 | Transfer illusions | Transfer taxonomy | WTS = TS × difficulty (near discounted) |
| F4 | Conflicting invariants | Compatibility matrix | Score below `min_compatibility` blocks |
| F5 | Sparse experience | Evidence count | `min_evidence` for hard gate |
| F6 | Noisy traces | TC = consistent / total steps | `trace_weight` down-weights low TC |
| F7 | Adversarial sequences | TFD on task stream | Multi-family + `min_tfd` warning |

## Edge cases (E1–E5)

- **E1:** High frequency / low transfer (VerifyOutput) — penalized via ranking + low TU.
- **E2:** Rare high transfer — `can_rescue_by_transfer` (11C-3) when VST + evidence hold.
- **E3:** Skill cannibalization — Jaccard similarity ≥ `similarity_merge` merge hint (11D executes merge).
- **E4:** Transfer saturation — `diminishing_transfer_utility` after `saturation_k` successes.
- **E5:** Negative transfer — NTR gate + escalation to reject/blacklist.

## Robustness metrics

| Metric | Formula |
| --- | --- |
| IER | invariants / traces |
| VST | successful variations / total variations |
| TC | consistent steps / total steps |
| TFD | unique families / total tasks |
| NTR | failed transfers / attempts (11C-4) |

## Hard promotion gate

Before SCT, `evaluate_hard_gate` requires:

- 11C-3 F / C / G / T / R passes
- 11C-4 transfer gate (ITS, attempts, NTR)
- VST ≥ `min_vst`
- Evidence ≥ `min_evidence`
- Task families ≥ `min_task_families_hard`
- Not blacklisted; optional IER restrict

`validate_and_rank(..., use_hard_gate=True)` filters promotable through the hard gate.

## Escalation (L1–L4)

| Level | Name | Example |
| --- | --- | --- |
| L1 | WARNING | Low frequency, IER warn |
| L2 | RESTRICTED | Weak transfer, IER restrict |
| L3 | REJECTED | High NTR, low VST |
| L4 | BLACKLISTED | Repeated NTR violations |

Stored in `invariant.metadata["failure_level"]` and `["failure_reasons"]`.

## File map

| Module | Role |
| --- | --- |
| `robustness/config.py` | `RobustnessConfig` |
| `robustness/metrics.py` | IER, VST, TC, TFD |
| `robustness/vst.py` | F1 |
| `robustness/explosion.py` | F2 |
| `robustness/illusions.py` | F3 WTS |
| `robustness/compatibility.py` | F4 |
| `robustness/trace_quality.py` | F6 |
| `robustness/diversity.py` | F7 |
| `robustness/saturation.py` | E4 |
| `robustness/similarity.py` | E3 |
| `robustness/escalation.py` | L1–L4 |
| `robustness/hard_gate.py` | Unified pre-SCT gate |

## Non-goals

Skill creation, SCV, skill library (11D). Skill-side failure modes and robust
gates are implemented in 11D-5: [skill_failure_modes.md](skill_failure_modes.md).
