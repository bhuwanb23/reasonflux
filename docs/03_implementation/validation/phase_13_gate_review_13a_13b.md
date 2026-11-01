# Phase Gate Review — Phases 13A and 13B

**Review date:** 2026-10-31  
**Evidence basis:** current workspace after the Phase 13B cost-accounting correction; synthetic dataset `synthetic-v1`; Phase 13B seeds 0–4.  
**Decision:** Phase 13A passes as a *one-seed readiness smoke check*. Phase 13B evidence has been run and reported, but **does not pass closure** because transfer-aware ranking ties frequency-only and no-transfer ranking on every seed. I do not recommend treating Contribution 1 as validated or moving to 13C as though this gate passed.

## Phase 13A — experimental foundation

### A. Experiment registry

Source: `configs/experiments.yaml`.

| ID | Registered experiment | Status | Entry |
|---|---|---|---|
| EXP-01 | Invariant Discovery Theory (IDT) | Enabled | `experiments/exp01_invariants/run.py` |
| EXP-02 | Skill Creation Trigger Theory (SCT) | Enabled | `experiments/exp02_skills/run.py` |
| EXP-03 | Task A → Task B transfer | Enabled | `experiments/exp03_transfer/run.py` |
| EXP-04 | Capability Growth Metrics (CGM) | Enabled | `experiments/exp04_growth/run.py` |
| EXP-05 | Full ASFT pipeline / end-to-end | Enabled | `experiments/exp05_end_to_end/run.py` |
| EXP-06 | Baseline comparisons | Enabled | `evaluation.harness.runner` |
| EXP-07 | Ablations | Enabled | `evaluation.harness.runner` |
| EXP-08 | ARC external validation | Disabled; planned | `experiments/exp08_arc/run.py` |
| EXP-IDT-14 | Frequent non-transfer confound stress test | Enabled, exploratory only | `experiments/exp14_confounded_idt.py` |

Phase 13B additionally runs the IDT sub-experiments for reflection, rotation, counting, grouping; quality; transfer; robustness; and baselines. These are recorded as EXP-IDT-01…13 and EXP-IDT-BASELINES. EXP-IDT-14 is supplemental; it does not alter the original Phase 13B gate.

### B. Seed policy

`configs/experiments.yaml` sets:

- Minimum seed set: **5 seeds, `[0,1,2,3,4]`**.
- Preferred set: **10 seeds, `[0,…,9]`**.
- Confidence level: **0.95**.
- Discovery seed offset: 0; transfer offset: 1000.

The Phase 13B evidence runner uses the five minimum seeds. Phase 13A's readiness gate intentionally uses **seed 0 only** and records `mode: smoke`; it is not a five-seed evidence run. Thus the project has a shared default policy, but not every run uses the same number of seeds. The Phase 13B transfer baseline uses discovery seed `s`, a calibration task batch starting at seed `1000+s`, and evaluation tasks starting at `2000+s`.

### C. Dataset and split policy

`configs/experiments.yaml` declares `synthetic-v1`:

- **Discovery:** Tier 1; reflection, rotation, counting, grouping; six generated traces/tasks per family for IDT discovery.
- **Transfer:** Tier 2; same four families; configured at two tasks per family with a disjoint seed offset of 1000.
- **ARC:** Tier 3, planned; `datasets/arc/` contains only a `.gitkeep`, not an actual dataset.
- **Holdout:** there is no separately stored, locked holdout dataset. Phase 13B generates calibration and evaluation tasks from the same task generator using different seed ranges (1000 and 2000). This is a deterministic seed-level separation, not a distributionally independent benchmark.

The Phase 13B transfer runner itself specifies three tasks per family and adds symmetric counting/grouping cases; this is an experiment-specific override of the general Tier-2 `per_family: 2` policy. The override is visible in the runner record but should be moved into the governed config before the next confirmatory run. Likewise, the configured `noise_level: 0.10` is not currently used by the noise helper: the code inserts one noise step with probability 0.8 per trace. That policy/config discrepancy needs correction before claiming a governed noise-dose experiment.

### D. Metrics registry

`src/evaluation/metrics_registry.py` contains **39 governed metric names**:

- **Core theory/growth:** `IS`, `SCV`, `SU`, `TS`, `TU`, `NTR`, `CGR`, `IG`, `IGR`, `COVERAGE`.
- **IDT quality/robustness:** `IP`, `IR`, `VST`, `PEARSON`, `SPEARMAN`, `RANK_STABILITY`, `DISCOVERY`, `RANK`, `CONFIDENCE`.
- **Sparse-data checks:** `SPARSE_MEAN_IS`, `CLEAN_MEAN_IS`, `SPARSE_CANDIDATES`, `CLEAN_CANDIDATES`, `SPARSE_STRONG_FRACTION`, `CLEAN_STRONG_FRACTION`, `SPARSE_PRECISION`, `SPARSE_RECALL`.
- **Baseline comparisons:** `ASFT`, `FREQUENCY_ONLY`, `NO_TRANSFER`, `RANDOM_PATTERN`, `ASFT_ADVANTAGE`, `ASFT_MINUS_NO_TRANSFER`, `ASFT_MINUS_RANDOM`, `ASFT_VALID_TOP_RATE`, `FREQUENCY_VALID_TOP_RATE`.
- **Transfer diagnostics:** `CROSS_FAMILY_REUSE`, `CROSS_FAMILY_REUSE_RATE`, `CORRELATION_N`.

This is the code registry, not proof that every registered metric has a valid operationalization or is used by every experiment. Some formulas/policies are repeated in YAML and runner code; those should be made a single source of truth.

### E. Reporting template

The common writer in `experiments/_common.py` stores JSON and Markdown reports. The auditable record includes:

```text
experiment_id
seed / seeds
 dataset_version
configuration
thresholds
metrics + metric definitions
raw_results and aggregate statistics (for multi-seed runs)
artifacts
failure_cases
observations
timestamp_utc
record_schema
```

A concrete Phase 13A example is `reports/experiments/phase13a_gates/record.json`. A Phase 13B example is `reports/experiments/EXP-IDT-08-10/record.json`; the evidence tables are under `reports/experiments/idt_evidence/`.

### F. Reproducibility check

Saved: the dataset version, seed(s), configuration, thresholds, metrics, metric definitions, raw/aggregate results, artifact paths and UTC timestamp. The Phase 13A gate nests its seed in `configuration` (`seed: 0`, `mode: smoke`); multi-seed IDT records carry a `seeds` list and raw results by seed.

**Missing for full reproducibility:** records do not save the Git commit SHA/dirty-tree state or an environment lock/hash. Also, the generic writer currently labels Phase 13B records `record_schema: phase-13a-v1`; the schema label should be generalized/versioned. The record foundation is useful but not yet complete provenance.

### Current Phase 13A gate output

Refreshed after the macro cost-accounting fix: **6/6 readiness checks pass** on seed 0. IDT readiness: 4 validated, mean IS 7.875; SCT: 4 admitted, mean SCV 0.0583; transfer: 5 records, mean benefit 0.23; CGM: CGR 0.1674, IG 0.2725; end-to-end beats all listed baselines; four baselines present. The report explicitly says “readiness smoke checks, not formal multi-seed evidence.”

Artifact: `reports/experiments/phase13a_gates/record.json`.

## Phase 13B — IDT evidence package

### 1–2. Discovered invariants and ranking

The global seed-0 run has **six unique candidate signatures**, so there are not ten distinct global invariants to list. Per-family Table 1 contains repeated signatures/IDs across family views; those repeats are not independent invariants. The table below reports the actual global candidate pool. “Reflection/rotation” labels describe operation components, not manually verified abstract concepts.

| Rank | Candidate signature | Frequency | Consistency | Generality | IS | TS | TU | Transfer attempts |
|---:|---|---:|---:|---:|---:|---:|---:|---:|
| 1 | `apply_reflection` | 12 | 1.00 | 0.75 | 9.00 | 0.0643 | 0.1661 | 7 |
| 2 | `find_symmetry` | 12 | 1.00 | 0.75 | 9.00 | 0.0643 | 0.1661 | 7 |
| 3 | `find_rotation` | 9 | 1.00 | 0.75 | 6.75 | −0.0278 | 0.0278 | 3 |
| 4 | `apply_rotation` | 9 | 1.00 | 0.75 | 6.75 | −0.0278 | 0.0278 | 3 |
| 5 | `count_objects` | 6 | 1.00 | 0.25 | 1.50 | 0.0000 | 0.0000 | 0 |
| 6 | `group_by_color` | 6 | 1.00 | 0.25 | 1.50 | 0.0000 | 0.0000 | 0 |

The reflection pair is semantically redundant at this level: `find_symmetry` maps to the same reusable reflection macro as `apply_reflection`. The rotation pair is similarly redundant. Count/group candidates had no applicable executable skill/transfer attempts in this transfer run; zero is not a measured failed replay.

### 3–4. Precision and recall

- **Expected labels:** 4 family-level concepts: reflection, rotation, counting, grouping.
- **Seed 0:** 6 detected candidates, 6 judged valid by the current code's label-overlap rule; IP = 6/6 = **1.00**. All four expected family labels found; IR = 4/4 = **1.00**.
- **Across seeds:** detected/valid counts are `[6/6, 6/6, 6/6, 8/8, 6/6]`; expected labels = 4 each; mean IP = **1.00**, mean IR = **1.00**.

Important qualification: “valid” is not manual inspection. It is computed from overlap between mined operation tokens and the expected-signature labels in `configs/invariants_labels.yaml`. Recall likewise checks whether expected operation components appear. These are synthetic label-based/component-level checks, not independent semantic annotation of full invariants.

### 5. IS ↔ TS correlation

Across five seeds:

- Pearson mean **r = 1.000**; Spearman mean **ρ ≈ 1.000**.
- Correlation sample sizes by seed: **4, 4, 4, 6, 4** (mean 4.4).
- The seed-level correlation SD is effectively zero, but that does not make the estimate precise: candidates are repeated operation components. The effective semantic variation is mainly two classes—reflection (higher IS and positive TS) versus rotation (lower IS and negative TS). This is not a persuasive independent predictive-validation sample.

The perfect correlation is therefore a **fragile synthetic association**, not strong evidence that IS predicts future transfer generally.

### 6. Cross-family transfer

Seed-0 calibration batch; two reflection-component skills (`apply_reflection` and `find_symmetry`, which map to the same macro) are each evaluated on the symmetric cross-family cases:

| Source skill | Target family | Attempts per skill | Correct/credited | Baseline → reused steps | Mean reduction | TS per target family |
|---|---|---:|---:|---:|---:|---:|
| Reflection component | Counting, symmetric grids | 2 | 2/2 | 5 → 4 | 0.20 | 0.050 |
| Reflection component | Grouping, symmetric grids | 2 | 2/2 | 5 → 4 | 0.20 | 0.050 |

These are genuine synthetic cross-family reuses, with cost now charged for the required count/group output step. They are narrow, hand-designed symmetry cases. In the same seed-0 batch, rotation candidates have 2 correct replays out of 3; their aggregate TS is negative (−0.0278), so negative/ineffective transfer is present and should be reported rather than hidden.

Across seeds, cross-family reuse mean = **10.8 events** (SD 4.38; 95% normal CI 6.96–14.64); cross-family reuse rate = **0.4848** (SD 0.0553; CI 0.4364–0.5333). The event count includes duplicate semantic candidate skills and is not a count of independent discoveries.

### 7–8. Variation survival and noise resistance

- **VST:** reflection = 1.00, rotation = 1.00, counting = 1.00, grouping = 1.00 in every seed; overall 1.00. Each family is tested under color, shape, position and count variations. This is still same-generator operation-label survival, not blinded semantic survival.
- **Noise/top-5 rank overlap:** per seed `[0.80, 0.80, 0.80, 0.60, 0.60]`; mean **0.72**, SD 0.110, 95% normal CI 0.624–0.816. So the top five were not fully unchanged in any claimable “90% stable” sense; average overlap is 72%.
- **Dose caveat:** `_noisy_traces` inserts one `noise_operation` with probability 0.8 per trace, while the config declares `noise_level: 0.10`. The noise test is reproducible from source but not currently governed by the declared config value.

### 9. Baseline comparison — blocking failure

Predeclared top-k = 2; shared validated/deduplicated pool and held-out evaluation tasks.

| Ranking | Mean TU | SD | 95% normal CI |
|---|---:|---:|---:|
| Transfer-aware ASFT | 0.095809 | 0.000736 | 0.095163–0.096454 |
| Frequency-only | 0.095809 | 0.000736 | 0.095163–0.096454 |
| No-transfer / IS-only | 0.095809 | 0.000736 | 0.095163–0.096454 |
| Random pattern | 0.063113 | 0.007712 | 0.056354–0.069873 |

Paired mean differences: ASFT − frequency = **0.000000**; ASFT − no-transfer = **0.000000**; ASFT − random = **0.032695** (95% normal CI 0.025800–0.039590). Transfer-aware, frequency-only and no-transfer rankings are identical on every seed. The random baseline is worse, but the mandatory informed-baseline comparison fails. The Phase 13B gate correctly remains false.

### 10. Multi-seed summary

| Metric | Mean ± SD | 95% normal CI | n seeds |
|---|---:|---:|---:|
| Quality-set mean IS | 5.856 ± 0.238 | 5.648–6.064 | 5 |
| Pearson IS–TS | 1.000 ± ~0 | ~1.000–1.000 | 5 |
| Spearman IS–TS | ~1.000 ± ~0 | ~1.000–1.000 | 5 |
| TS | 0.017619 ± 0.000869 | 0.016857–0.018381 | 5 |
| TU | 0.065726 ± 0.003188 | 0.062931–0.068520 | 5 |
| VST | 1.000 ± 0 | 1.000–1.000 | 5 |
| Noise rank overlap | 0.720 ± 0.110 | 0.624–0.816 | 5 |

CIs are repository normal-approximation intervals over five seed-level aggregates. They are descriptive, not task-level inferential intervals.

## Supplemental follow-up: EXP-IDT-14

A separate, explicitly controlled frequent-no-op stress test was run on held-out run seeds 10–14 after freezing `configs/idt_confounded_benchmark.yaml`. It inserts a zero-cost `normalize_grid` marker into discovery traces from three of four families; this is an adversarial intervention, not natural data. The final run had ASFT top-1 TU **0.164866 ± 0.001100** (95% normal CI 0.163902–0.165831), versus **0** for frequency-only and IS-only, and **0.059557 ± 0.017642** for random. ASFT won top-1 on every seed; the nuisance occurred 30 times per run, more than the useful reflection component (25–27). At top-2, ASFT also beat the controls; at top-3, curves tie.

This indicates the ranking mechanism can respond to a known frequent-no-op confound in the simulator. Because this benchmark was designed after the original tie and the nuisance was deliberately injected, it is **exploratory stress-test evidence**, not a pass of the original `synthetic-v1` Phase 13B gate and not general proof of IDT. The original closure remains false. Full protocol and results are in `phase_13b_exp14_protocol.md` and `reports/experiments/EXP-IDT-14/`.

## Claim-level decision

| IDT claim | Review decision | Reason |
|---|---|---|
| 1. Useful invariants emerge | **Limited support only in this synthetic mechanism** | Operation-level patterns recur, but the generator supplies family and canonical operation structure; quality labels are not independent manual judgments. |
| 2. IS predicts transfer | **Not established** | r≈1 is based on 4–6 candidate rows per seed, with duplicated operation components and effectively two semantic classes; rotation has negative TS. |
| 3. Transfer-aware discovery beats frequency-only | **No** | Exact tie in every seed; zero paired advantage. |
| Statistical robustness | **Descriptive within this generator; not broad validation** | Five seeds, small candidate population, fixed generator, normal CIs. |

## Reviewer risks and what is missing

1. The synthetic generator and solver encode the family/rule vocabulary used as discovery “ground truth”; this risks circular validation.
2. Precision/recall are label-overlap metrics, not blinded manual semantic evaluation.
3. Table 1's family rows duplicate candidate signatures; six global signatures, not ten independent invariants. Reflection/rotation each appear as two redundant operation components.
4. IS–TS correlation treats component candidates as rows; candidates are not independent, and the observed relation mainly separates reflection from rotation.
5. The baseline ranking cannot distinguish transfer-aware from frequency/IS ranking. This is the principal blocking evidence.
6. Config/runner mismatch for transfer per-family count and noise dose; some thresholds/seed offsets are hard-coded instead of loaded from config. Metric meanings also need one source of truth: `configs/metrics.yaml` defines `NTR` as failed/total transfer attempts, while the code registry calls it normalized reasoning reduction.
7. Experiment records lack Git commit/environment provenance and use `phase-13a-v1` schema on 13B records.
8. No ARC dataset, ARC adapter, or external evaluation exists; Phase 13G remains future work.

## Gate recommendation

**13A:** pass only as a smoke/readiness gate; improve provenance and enforce config consistency before calling the experimental foundation fully governed.  
**13B:** do not close as a successful IDT validation. The original baseline tie remains visible. EXP-IDT-14 is a positive, controlled stress-test result, but it does not replace the original gate. Before 13C is treated as theory validation, run an independently justified and preregistered confirmatory benchmark or narrow the claim. Do not change thresholds or retroactively pass the original comparison.

## Evidence paths

- Registry/policy: `configs/experiments.yaml`
- Metrics: `src/evaluation/metrics_registry.py`
- Phase 13A record: `reports/experiments/phase13a_gates/record.json`
- Phase 13B aggregate: `reports/experiments/idt_evidence/summary.json`, `summary.md`
- Top-invariant table: `reports/experiments/idt_evidence/table_1_top_invariants.json`
- Precision/recall: `reports/experiments/idt_evidence/table_2_precision_recall.json`
- Baselines and per-seed ranking diagnostics: `table_3_baselines.json`, `table_3_baselines_by_seed.json`
- Robustness: `table_4_robustness.json`
- Transfer: `table_5_transfer.json`
- Closure: `reports/experiments/idt_evidence/closure.json`
- Phase 13B results narrative: `docs/03_implementation/validation/phase_13b_results.md`
