# Capability Failure Modes & Robustness (Phase 11E-5)

Hardens Contribution 3 so **fake growth is rejected**. Code under
`src/capability/robustness/`. Thresholds: `configs/thresholds.yaml`
(`capability_robustness:`).

Wraps existing representation / growth / intelligence audits; does **not**
re-derive CapU, CGR, or IG.

## Taxonomy CF1–CF10

| ID | Kind | Signal | Typical recovery |
| --- | --- | --- | --- |
| CF1 | Growth illusion | Skill-count / CGR without utility | Reject claim |
| CF2 | Fragmentation | High caps/skills (FR) / tiny caps | Archive tiny |
| CF3 | Inflation | Claimed ≫ observed coverage / ghosts | Archive inflated |
| CF4 | Transfer collapse | TS drop or high NTR | Retire harmful |
| CF5 | Saturation | Low CSR (new vs existing) | Monitor |
| CF6 | Regression | Sustained negative CGR | Restore declining |
| CF7 | Metric gaming | CGR without evidence | Reject claim |
| CF8 | Benchmark overfitting | Train success ≫ ARC holdout | Reject / archive |
| CF9 | Intelligence illusion | IG up without evidence / stagnation | Monitor |
| CF10 | Capability collapse | Repeated deep negative CGR | Restore core |

Severity uses existing `FailureLevel` (ok → warning → restricted → rejected → blacklisted).

## Health and stability

- **CHS** (Capability Health Score): weighted utility / transfer / coverage /
  growth / confidence.
- **CS** (Capability Stability): `1 − normalized variance` of a metric series.
- Bands: `excellent` ≥ 0.8 · `healthy` ≥ 0.6 · `stable` ≥ 0.4 · `weak` ≥ 0.2 ·
  else `critical`.

## Hard validation rules

`validate_growth_claim` accepts a growth claim **only if** all of:

1. transfer Δ > 0  
2. utility Δ > 0  
3. coverage Δ > 0  
4. evidence support (`GrowthEvidence.has_support()`)

Skill-count-only growth is rejected. Harness `gate_run` uses this when
`HarnessConfig.hard_validation=True` (default) and does **not** soft-filter
gaming / illusion kinds.

## Recovery loop

Detect → Diagnose → `plan_recovery` → `apply_recovery` → Monitor.

Prefer archive / retire of harmful capabilities and restore of declining /
dormant / core members via lifecycle + metadata flags — **no** DreamCoder
rebuild.

## Ecosystem audit

```text
audit_capability_ecosystem(cap_lib, skill_lib, snapshots=None, *, config)
  → EcosystemAuditResult(ok, failures, health, growth_claim, metrics)
```

## File map

| Module | Role |
| --- | --- |
| `robustness/config.py` | `CapabilityRobustnessConfig` |
| `robustness/taxonomy.py` | CF1–CF10, `FailureDiagnosis` |
| `robustness/metrics.py` | FR, CSR, CHS, CS helpers |
| `robustness/detectors.py` | CF1–CF4 / CF7 / CF9 wrappers |
| `robustness/detectors_series.py` | CF5 / CF6 / CF8 / CF10 |
| `robustness/gates.py` | `validate_growth_claim` |
| `robustness/health.py` | per-cap + portfolio bands |
| `robustness/recovery.py` | plan / apply recovery |
| `robustness/audit.py` | `audit_capability_ecosystem` |

## Non-goals

- Replacing skill SF7 / IDT F-suite
- Interactive dashboard
- New CapU / CGR / IG formulas
