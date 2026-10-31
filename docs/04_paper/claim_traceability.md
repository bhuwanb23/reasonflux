# Claim Traceability (Phase 11F)

Every research claim must resolve to code, a metric, an experiment, and a paper
artifact. Machine-checked against
[`configs/modules.yaml`](../../configs/modules.yaml) by
`tests/test_spec_claim_traceability.py`.

## Chain

```
Claim → Modules → Metrics → Experiment → Paper artifact → Verifier
```

```mermaid
flowchart LR
  claim["Research claim"] --> mods["Modules"]
  mods --> metrics["Metrics (configs/metrics.yaml)"]
  metrics --> exps["Experiments (configs/experiments.yaml)"]
  exps --> artifacts["Table / figure"]
  artifacts --> verifier["Verifier test"]
```

## Layer 1 — FOUNDATION

**Claim:** reliable reasoning traces are the precondition for every downstream
claim.

| Element | Value |
| --- | --- |
| Modules | M01 Task System, M02 Reasoning Trace System, M03 Experience Memory |
| Metrics | TC, TFD |
| Experiment | `exp01_invariants` (consumes traces) |
| Artifact | table: dataset and trace inventory per task family |
| Verifier | `tests/test_spec_module_registry.py::test_partial_modules_own_a_stub` |

**Status: blocked.** No component produces or persists traces yet, so all
downstream evidence currently runs on synthetic scenario data
([`scenarios.py`](../../src/evaluation/harness/scenarios.py)) rather than on
learned experience.

## Contribution 1 — IDT

**Claim:** transferable knowledge emerges from invariants.

| Element | Value |
| --- | --- |
| Modules | M04 Trace Mining Engine, M05 Invariant Discovery Engine, M06 Invariant Ranking Engine, M07 Invariant Robustness System |
| Metrics | IS, VST, IER, TC |
| Experiment | `exp01_invariants` |
| Artifact | table: invariant inventory vs IS; figure: IS distribution by task family |
| Verifier | `tests/test_trace_miner.py::test_end_to_end_reflection_and_rotation_emerge` |

Anti-claim tested: frequent patterns are not invariants. Rejection lives in
[docs/invariants.md](../02_design/invariants.md) and
[docs/failure_modes.md](../02_design/failure_modes.md).

## Contribution 2 — SCT

**Claim:** skills should emerge only when economically justified.

| Element | Value |
| --- | --- |
| Modules | M08 Skill Candidate System, M09 Skill Economics Engine, M10 Skill Promotion Engine, M11 Skill Library, M12 Skill Lifecycle Manager, M13 Skill Composition Engine, M14 Skill Robustness Engine |
| Metrics | SCV, SU, ASU, PU, NTB |
| Experiment | `exp02_skills` |
| Artifact | table: SCV decision outcomes; figure: SU distribution before/after promotion |
| Verifier | `tests/test_skill_pipeline_e2e.py::test_reflection_promoted_verify_rejected` |

Anti-claim tested: more skills is not better. Explosion, duplicates, and negative
transfer are blocked by
[docs/skill_failure_modes.md](../02_design/skill_failure_modes.md).

## Transfer hypothesis

**Claim:** solving task A measurably improves task B through shared structure.

| Element | Value |
| --- | --- |
| Modules | T1 Transfer Engine |
| Metrics | TS, ITS, TU, NTR |
| Experiment | `exp03_transfer` |
| Artifact | table: TS/ITS per source-target family pair; figure: transfer graph |
| Verifier | `tests/test_transfer_aware_ranking.py::test_high_its_outranks_zero_transfer_despite_lower_frequency` |

Anti-claim tested: co-occurrence is not transfer. Transfer memory requires a
recorded attempt with benefit and reasoning reduction
([docs/transfer.md](../02_design/transfer.md)).

## Contribution 3 — CGM

**Claim:** intelligence growth can be measured through capability growth.

| Element | Value |
| --- | --- |
| Modules | M15 Capability Representation System, M16 Capability Growth Engine, M17 Intelligence Growth Engine, M18 Capability Robustness Engine, M19 Metrics Engine |
| Metrics | CGR, IG, AG, UG, PU |
| Experiment | `exp04_growth` |
| Artifact | figure: C_t and IG trajectories; table: CGR by phase with CI |
| Verifier | `tests/test_cgr_e2e.py::test_positive_zero_negative_cgr_and_ig` |

Anti-claim tested: fake growth. CF1–CF10 plus the multi-signal hard gate reject
skill-count-only and evidence-free growth
([docs/capability_failure_modes.md](../02_design/capability_failure_modes.md)).

## End-to-end — ASFT

**Claim:** the full pipeline beats baselines and degrades under ablation.

| Element | Value |
| --- | --- |
| Modules | M20 Benchmark Engine, M21 Baseline Engine, M22 Ablation Engine, M23 Reporting Engine |
| Metrics | CGR, IG, SU, TS |
| Experiment | `exp05_end_to_end` |
| Artifact | table: ASFT vs baselines A–D; table: ablations A1–A5 |
| Verifier | `tests/test_cap_robustness_e2e.py::test_flat_fails_hard_gate` (harness level) |

**Status: blocked.** Harness-level baselines and ablations are demonstrated on
synthetic scenarios, but `run_full_asft_pipeline` is still a stub, so no
paper-facing end-to-end run exists. See
[v0_1_readiness.md](../00_project/v0_1_readiness.md).

## Metric registry mapping

| Metric | Definition | Code home |
| --- | --- | --- |
| IS | frequency × consistency × generality | `src/invariants/strength.py` |
| SCV | reuse × AG × TS − creation cost | `src/core/skill.py` (`compute_scv`) |
| SU | (RCG+TV+CP+RV) − (CC+MC+NR) | `src/skills/utility.py` |
| TS | performance_after − performance_before | `src/evaluation/transfer_metrics.py` |
| CGR | (C_t − C_t−1) / Δt | `src/evaluation/growth_metrics.py` |
| IG | weighted AG/SU/TS/CGR/CP/AD | `src/evaluation/intelligence.py` |
| ITS / TU / NTR | transfer memory summaries | `src/transfer/metrics.py` |
| IER | invariants / traces | `src/invariants/robustness/explosion.py` |
| VST | surviving variations / total | `src/invariants/robustness/vst.py` |
| TC | consistent steps / total steps | `src/invariants/robustness/trace_quality.py` |
| TFD | unique families / tasks | `src/invariants/robustness/diversity.py` |

Full formula list: [configs/metrics.yaml](../../configs/metrics.yaml) and
[metrics.md](../02_design/metrics.md).

## Review rule

A claim may not appear in the paper unless its row above has a passing verifier
and its experiment is `enabled: true` in `configs/experiments.yaml`. Today only
`exp04_growth` is enabled.
