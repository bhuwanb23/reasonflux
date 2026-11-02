# ASFT v1.1 Phase 1C — Full Ranking-Pressure Audit

**Phase ID:** `ASFT-V1.1-PHASE-1C`  
**Package:** `ASFT-V1.1-PHASE-1C-RANKING-PRESSURE-SPEC-V1`  
**Audit scope:** retrospective Phase 13B/14 ranking-failure audit, new benchmark protocol, and synthetic contract harness.  
**Decision:** **PASS for design and synthetic contract validation; empirical ranking effectiveness UNTESTED.**  
**Experiments:** no real task runner, calibration study, confirmatory outcome evaluation, or replication was run.

## 1. Executive decision

Phase 1C now defines a controlled ranking benchmark designed so that transfer-aware IDT can disagree with frequency-only, reuse-only, compression-oriented, and random rankers. It requires the disagreement to be computed and logged before future truth is opened. The selected sets are evaluated against an independent future task suite and a paired no-candidate counterfactual. An analysis-only Oracle is isolated until after rank lists and pressure are sealed.

The contract runner passes **26/26** checks. Across 100 synthetic pressure panels (`N=40`, `K=8`) from one fixed feature/type recipe, all 100 pass the specified gate. Mean all-pair TopK-RDR is **0.8391** (minimum **0.7875**); mean normalized Kendall divergence is **0.4900** (minimum **0.4538**). The fixture metric can report an IDT loss, tie, or win against Frequency.

These are mechanical contract results. The 100 panels are not independent research batches; the data are not actual invariant/task outputs; and the outcome-response truth vectors are purpose-built arithmetic checks. No IDT benefit or deficit is estimated.

## 2. Phase 13B/14 failure audit

The corrected Phase 13B top-K=2 primary result was `0.095809` held-out TU for ASFT/transfer-aware, frequency-only, and no-transfer; paired differences were zero and the semantic order matched in each of five seeds. The frozen strict superiority gate failed. The lower random result (`0.063113`) was insufficient to meet the all-comparator gate. The documented pre-correction output-cost value (`0.1431299603`) differs in magnitude, but the relative policy tie/gate failure persists in both recorded versions.

The best-supported descriptive observation is **no ranking disagreement in the sampled top order**. The saved record does not identify whether that came from weak pressure, feature correlation, a narrow candidate pool, or no true transfer advantage. Lack of pressure is a design diagnosis to address, not a proven unique root cause.

EXP-IDT-14 inserted a frequent no-op after the original tie; it produced transfer-aware top-1 TU `0.164866` versus zero for frequency/no-transfer and `0.059557` random. This demonstrates sensitivity to that deliberately constructed confound only; it is exploratory and does not repair the original frozen gate. Corrected Phase 13D's IS–TS result (`r=-0.0424`, seed-cluster interval `[-0.1318, approximately 0]`) further warns against treating a ranking signal as validated predictive truth.

Full source mapping and limits: [`ranking_failure_audit.md`](ranking_failure_audit.md).

## 3. New Phase 1C design

### Candidate and pressure rules

- `N=40`, `K=8`, with hidden disjoint primary archetypes A4/B8/C8/D4/E4/F4/G4/H4. B (frequent-useless) and C (rare-useful) each make up 20% in the controlled generator.
- Candidate IDs are opaque; arrival order is randomized separately from hidden type. Future truth and labels never enter ranker cards.
- Rankers submit full deterministic orders and fixed Top-K sets over the exact same candidates.
- TopK-RDR is `1 − intersection/K`; normalized Kendall divergence reports full-order differences.
- Pre-outcome gates require R1 to diverge from Frequency, Reuse, Compression, and Random; require mean all-pair TopK-RDR and Kendall thresholds; pressure code accepts no truth argument.

### Frozen ranker family

R1 is the current operational transfer-aware IDT score, `F×C×G×T×R`, with calibration-only `T=ITS×TU` supplied by the pinned implementation. R2 is frequency-only; R3 reuse probability only; R4 compression score only; R5 seeded random. R6 Oracle is post-lock and excluded from competition and pressure. The historical Phase 13B score construction and current operational R1 are not silently conflated; any historical rescore must be registered before outcomes as a separate sensitivity, never substituted after results.

### Outcome and estimand

Primary endpoint is portfolio-level Future Net Transfer Utility at K (`FNTU@K`): the selected set's future task utility against a paired no-candidate baseline over common disjoint future families, less frozen cost, normalized per selected slot and task opportunity. It is distinct from R1's calibration score. SOI is `+0.10` normalized utility units per slot/opportunity, with Holm adjustment over four R1-vs-R2–R5 comparisons. The independent unit is a panel/family-seed cluster, not each candidate or task row.

The result categories are supported, contradicted, inconclusive, unavailable. A preregistration template requires exact N, hashes, cost conversion, analysis code, missingness and sealed-store/access fields before any confirmation.

## 4. Contract test audit

The executable files are `experiments/phase1c/ranking_benchmark.py` and `experiments/phase1c/run_contracts.py`. From repository root:

```bash
python experiments/phase1c/run_contracts.py reports/experiments/ASFT-V1.1-PHASE-1C-RANKING-PRESSURE-SPEC-V1
```

Twenty-six contract assertions cover class quotas and label separation, opaque IDs/order, common pool/budget, determinism/ties, ranker disagreement, pre-outcome RDR/Kendall pressure, Oracle isolation, outcome/rank separation, bounded feature schema, and synthetic loss/tie/win responses. The row-level record is [`phase1C_contract_test_results.csv`](phase1C_contract_test_results.csv).

The 100-panel summary is [`synthetic_pressure_validation.json`](synthetic_pressure_validation.json). The fixture-0 full pairwise matrix is [`pairwise_rank_divergence.csv`](pairwise_rank_divergence.csv).

## 5. Adverse interpretation and limitations

The fixture profile deliberately has orthogonal rank signals and fixed latent class proportions. The ranker disagreement is designed into the fixture means; it is not independently sampled pressure. This proves that the interface and pressure gate can mechanically represent differing orders, not that natural/prospective candidate pools will do so. The contract runner's loss/tie/win truth vectors are constructed **after** rankings from the selected-set differences (or equality), so they test only metric arithmetic and are not independent future-outcome cases. The formal independent-value protocol is specified, but the actual task-derived outcome runner is not implemented. The harness does **not** establish that:

- natural IDT candidate pools contain these proportions or this much disagreement;
- current calibration features predict future transfer;
- R1 outperforms any comparator in task utility;
- the synthetic cost model, SOI, or sample-size assumptions are empirically calibrated;
- future task-family leakage controls or a production sealed outcome store exist;
- memory, SCT, capability growth, or intelligence claims have been tested.

No pressure-failing panel is to be removed by observing its outcome. If a frozen prospective panel fails its pre-outcome gate, the confirmatory study remains blocked/unavailable under the specified protocol.

## 6. Readiness decision

**Phase 1C design and synthetic contract layer: PASS.** All ten design deliverables and 26/26 fixture checks are present. **Empirical RQ1 readiness: BLOCKED** pending real task generator/runner, calibration-derived costs, final N, production hashes, frozen analysis, sealed confirmatory truth store, and disjoint replication. No Phase 4 or SCT experiment is authorized by this Phase 1C package.

Phase 1B remains accepted at design/contract level, not as experimental evidence. Phase 1C closes the ranking-benchmark design task; it does not answer whether IDT's transfer-aware ranking works.