# ASFT v1.1 Phase 3A — Historical IDT Audit

**Package:** `ASFT-V1.1-PHASE-3A-IDT-IMPLEMENTATION-READINESS-V1`  
**Audit scope:** saved Phase 13B results, the corrected production R1 definition, and the retrospective Phase 14B analysis. No historical result was rerun, replaced, or promoted to confirmatory evidence.

## Decision-relevant historical record

### Phase 13B corrected `synthetic-v1` run

The saved record uses five seeds (0–4), top-K=2, a shared semantically deduplicated candidate pool, and the same held-out task batch across transfer-aware, frequency-only, no-transfer, and random policies. The strict closure gate required transfer-aware to strictly beat each informed control on every seed. It failed.

| Policy | Mean held-out TU | SD | Paired difference vs transfer-aware |
|---|---:|---:|---:|
| Transfer-aware | 0.095809 | 0.000736 | — |
| Frequency-only | 0.095809 | 0.000736 | 0.000000 (SD 0; CI 0–0) |
| No-transfer | 0.095809 | 0.000736 | 0.000000 (SD 0; CI 0–0) |
| Random pattern | 0.063113 | 0.007712 | +0.032695 for transfer-aware (SD 0.007866) |

The semantic ranking was identical for transfer-aware, frequency-only, and no-transfer on all five seeds: reflection, rotation, counting, grouping. Transfer-aware therefore showed no discriminative ranking pressure against the informed baselines in that saved setup. The Phase 13B closure checker correctly remains false; its recorded failure is that transfer-aware did not strictly beat all controls for every seed.

Phase 13B also found a cross-family cost-accounting omission, repaired it, and reran the corrected analysis. The repair reduced utility; the baseline tie remained. The metric was still simulator step-count cost, not calibrated wall-clock or compute cost for a general ARC agent.

### Phase 13D and EXP-IDT-14

The historical Phase 13D corrected IS–TS correlation was `r=-0.0424` with a seed-cluster interval `[-0.1318, approximately 0]`. Predictive validity and superiority were not established.

EXP-IDT-14 was an explicitly exploratory, post-tie stress test that inserted a frequent no-op marker into successful traces. On its final seeds 10–14, transfer-aware top-1 TU was 0.164866 versus 0 for frequency-only and no-transfer; from top-3 onward the curves tied. The protocol itself characterizes this as a deliberately constructed confound in a simulator, not an independent or natural-data confirmation. It does not repair or replace the original Phase 13B result.

## Interpretation to preserve

- **Superiority not established.** The Phase 13B tie with informed controls remains the primary historical comparison.
- **IDT falsified not established.** A tie in this benchmark is not universal falsification; the evidence is insufficient to establish predictive validity or broad effectiveness.
- A deliberately engineered EXP-IDT-14 win is a stress-test capability demonstration only. Do not generalize it to natural candidate pools or ARC.
- Phase 3A is an implementation-fidelity/readiness review, not the first efficacy result. Its synthetic contract outcomes, score correlations, and pressure fixtures cannot be represented as efficacy evidence.

## Sources audited

- `docs/03_implementation/validation/phase_13b_results.md`
- `docs/03_implementation/validation/phase_13b_exp14_protocol.md`
- `reports/experiments/PHASE-14B-IDT-CRITICAL-ANALYSIS-V1/phase14b_idt_analysis.md`
- `docs/03_implementation/validation/phase_13b.md` (historical plan; distinguished from results)
- Phase 1C ranking competition, outcome, and pressure specifications.

**Audit disposition:** Historical record reviewed and preserved; it supplies motivation and null-result context, not Phase 3A candidate-pool or endpoint validation.