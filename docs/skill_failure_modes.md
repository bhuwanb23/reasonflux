# Skill Failure Modes & Robustness (Phase 11D-5)

Final hardening of SCT. Skills are not assumed beneficial: every skill must keep
justifying itself through utility, transfer, reuse, and capability contribution.
Code under `src/skills/robustness/`. Thresholds: `configs/thresholds.yaml`
(`skill_robustness:`).

## Failure taxonomy (SF1–SF8)

| ID | Failure | Detection | Safeguard |
| --- | --- | --- | --- |
| SF1 | Premature creation | evidence / confidence floors | Block promotion; demote to `candidate` |
| SF2 | Skill explosion | SER = skills / validated invariants | Restrict at `ser_restrict`; capacity sweep |
| SF3 | Duplicate skills | trigger similarity ≥ `duplicate_similarity` | Merge into stronger skill |
| SF4 | Negative transfer | NTR = failed transfers / attempts | warn → demote retrieval → dormant → retire |
| SF5 | Retrieval failure | RR = retrieved / applicable | Boost missed skills, raise weights |
| SF6 | Composition failure | CU < `cu_min_composition` or NCR high | Reject and raise future composition cost |
| SF7 | Capability collapse | CGR < `cgr_collapse` for `collapse_periods` | Prune harmful skills, rebuild portfolio |
| SF8 | Adversarial formation | TFD < `tfd_min_promote` | Require cross-family evidence |

## Edge cases (EC1–EC4)

- **EC1** Rare high-value: transfer ≥ `transfer_override_min` overrides frequency floors.
- **EC2** Ancient core: age ≥ `ancient_core_min_age` with strong history → protected from retirement.
- **EC3** Zombie: repeated reactivations without utility gain → permanent archive.
- **EC4** Cannibalization: weaker overlapping skill denied the retrieval slot.

## Metrics

| Metric | Formula |
| --- | --- |
| SER | skills / validated invariants |
| NTR | failed transfers / transfer attempts |
| RR | retrieved useful / available useful |
| CGR | ASU_t − ASU_{t−1} |
| TFD | unique families / total tasks |
| HS | existing lifecycle health score (11D-3) |

## Robust gates

**Promotion** (`evaluate_skill_promotion_gate`) requires evidence, transfer,
utility, NTR below limit, similarity check, diversity check, and SER not restricted.

**Retirement** (`evaluate_skill_retirement_gate`) requires low utility AND low
transfer AND low reuse AND no positive reactivation signal. EC2 overrides.

## FSM change note

Demotion (SF1 recovery) uses existing-and-new transitions:

```
active-tier (ACTIVE/GROWING/CORE) → PROMOTED → CANDIDATE
```

`PROMOTED → CANDIDATE` and active-tier → `PROMOTED` are legal in
`SKILL_TRANSITIONS`; `demote_skill()` walks the two hops so no shortcut exists.

## Recovery architecture

```
Detect → Diagnose → Recover → Monitor
```

`plan_recovery(diagnosis)` maps each failure to `RecoveryAction`
(demote / dormant / retire / archive / boost / monitor); `apply_recovery()` executes it.
Retirement never deletes: skills stay in the library and archive instead.

## File map

| Module | Role |
| --- | --- |
| `robustness/config.py` | `SkillRobustnessConfig` |
| `robustness/taxonomy.py` | `SkillFailure`, `FailureDiagnosis` |
| `robustness/metrics.py` | SER, NTR, RR, CGR, TFD |
| `robustness/sf_creation.py` | SF1, SF2, SF3 |
| `robustness/sf_transfer.py` | SF4 |
| `robustness/sf_retrieval.py` | SF5 |
| `robustness/sf_composition.py` | SF6 |
| `robustness/sf_capability.py` | SF7, SF8 |
| `robustness/edge_cases.py` | EC1–EC4 |
| `robustness/gates.py` | Robust promotion / retirement gates |
| `robustness/recovery.py` | Recovery planning + application |
| `robustness/audit.py` | `audit_library` |

## Non-goals

Capability growth metrics (11E), parallel/conditional/recursive composition,
re-deriving SU (11D-2) or CU (11D-4).
