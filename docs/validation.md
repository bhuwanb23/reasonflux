# Invariant Ranking & Validation (Phase 11C-3)

Gatekeeper between trace mining and SCT. Code under `src/invariants/validation/`,
`ranking.py`, `promotion.py`, `validator.py`. Thresholds: `configs/thresholds.yaml`
(`validation:`).

**Rule:** ASFT does not promote invariants because they are frequent. It promotes
them because they are frequent, stable, generalizable, transfer-relevant, and
reasoning-efficient.

## Pipeline

```
Candidates (11C-2)
 → Five validation tests (F, C, G, T, R)
 → InvariantScore = F × C × G × T × R
 → Rank & filter
 → Promotion gate → SKILL_CANDIDATE (SCT input)
```

## Five tests

| Score | Question | Default gate |
| --- | --- | --- |
| F frequency | How often? | `min_f: 0.3` (`freq_norm: 10`) |
| C consistency | Remains stable? | `min_c: 0.6` |
| G generality | Survives task variation? | `min_g: 0.3` |
| T transfer | Helps future tasks? | `min_t: 0.1` |
| R reasoning value | Reduces reasoning cost? | `min_r: 0.1` |

## False positives / negatives

- **FP:** task-specific color/shape/position/count literals, `metadata.failed_variations`, or low VST (`low_vst`).
- **FN:** rare invariants with `T >= transfer_rescue_min_t` and
  `frequency >= transfer_rescue_min_frequency` are rescued on the frequency gate.

Phase 11C-5 adds the **hard promotion gate** and failure taxonomy — see
[docs/failure_modes.md](failure_modes.md).

## Promotion lifecycle

```
CANDIDATE → DETECTED → VALIDATED → TRANSFER_VERIFIED → SKILL_CANDIDATE
```

Doc “Promotable” maps to `InvariantState.SKILL_CANDIDATE`.

## File map (each ≤300 lines)

| Path | Role |
| --- | --- |
| `validation/scores.py` | `ValidationConfig`, `ValidationScores` |
| `validation/frequency.py` … `reasoning_value.py` | Five tests |
| `validation/false_positives.py` / `false_negatives.py` | FP/FN |
| `ranking.py` | product score + ordering |
| `promotion.py` | criteria + lifecycle |
| `validator.py` | `validate_and_rank` orchestrator |
| `specification/` | 11C-1 package (split from oversized module) |

## Must NOT

Create skills, compute SCV, build transfer graphs (those are 11D / 11C-4).
