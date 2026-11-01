# Phase 14C — Contribution 2 (SCT) Critical Results Analysis

**Review ID:** `PHASE-14C-SCT-CRITICAL-ANALYSIS-V1`  
**Scope:** Contribution 2 only — Skill Creation Trigger Theory (SCT).  
**Method:** critical analysis of saved Phase 13C, 13F, 13G, and 13H evidence. No reruns, no threshold changes, and no edits to Phase 13 evidence.  
**Status:** complete.

## Executive verdict

Phase 13 demonstrates that ASFT can build and reuse **reflection and rotation skills** in controlled synthetic tasks, with positive measured step-cost savings in some applications. Phase 13C's skill composition pathway also completes one evaluable rotation→reflection composition case; Phase 13F's no-composition ablation supports a composition-related synthetic benefit on its own frozen outcomes. These are meaningful mechanism demonstrations, not evidence for broad skill emergence or generally superior skill selection.

The central selection-policy claim did **not** pass. In Phase 13C, the primary SCV cutoff was zero, all 44/44 confirmation candidates had positive SCV and were selected, and the calibration-derived random-create probability was 1.0. Consequently, SCT, ALWAYS_CREATE, and RANDOM_CREATE made equivalent creation choices and tied at mean net value `0.345`; the strict superiority gate failed. The benchmark supplied no primary-case rejection decision to test. This is the best-supported explanation for the tie, not proof that SCT is theoretically wrong.

SCV is associated with shadow future net value (`ρ=0.700`, 95% seed-cluster CI `[0.545,0.931]`), but frequency (`ρ=0.748`) and especially `p_reuse` (`ρ=0.884`) were at least as strongly associated numerically. Phase 13F's no-SCV and random-SCV arms also tie ASFT on the recorded outcomes. The evidence therefore does not establish SCV's incremental predictive or policy advantage. Separately, Phase 13C's MEMORY_ONLY policy scored `1.325` versus SCT's `0.345`, but Phase 13F's separately specified B2_MEMORY_SKILL_STORE baseline was below ASFT on that phase's joint task-utility/CGR criterion. These are distinct controls and metrics: the memory result is mixed across designs, not a universal memory-superiority conclusion.

**Revised claim:** “In controlled synthetic environments, ASFT can construct and reuse reflection and rotation skills from recurring trace structures, with measured simulator step-cost reductions in some cases. SCV is associated with future value in one synthetic candidate sample, but no incremental selection advantage over simple creation policies is demonstrated. Evidence for composition is limited to a small synthetic operation set, and skill emergence on ARC has not been demonstrated.”

## 14C-1 — Claim review

| Claim | Phase 14C judgment | Evidence boundary |
|---|---|---|
| SCT-1: skills emerge from validated invariants | **Supported narrowly in synthetic scope** | 44 Phase 13C skill instances across 10 confirmation seeds; all reflection/rotation. No counting/grouping births. |
| SCT-2: SCV predicts future value | **Partial association; policy validity unestablished** | SCV10 `ρ=.700` on 44 candidates/10 seed clusters; simpler signals are comparable or stronger; 13F no-SCV/random-SCV contrasts tie. |
| SCT-3: economically justified creation beats naive creation | **Failed on Phase 13C primary superiority gate** | SCT ties ALWAYS_CREATE and RANDOM_CREATE at `.345`; under the primary setting every candidate is selected. |
| Skill reuse reduces measured reasoning cost | **Supported within simulator, narrowly** | Positive-credit reuses and success-gated step reductions in synthetic tasks; not wall-clock/compute savings. |
| Composition adds value | **Promising but limited synthetic evidence** | One evaluable pair in 13C; 13F no-composition arm loses on selected frozen outcomes. No diverse composition coverage. |
| Lifecycle machinery has value | **Not demonstrated** | Dormancy/reactivation probes have mixed outcomes; no-lifecycle ablation ties on primary net value. |
| ARC skill emergence | **Not demonstrated by bounded adapter** | Zero skills/capabilities; low exact-fit coverage; not a general refutation of skill formation. |

## 14C-2 — SCT-1: skills emerge from validated invariants

### What happened

Phase 13C's confirmatory block used seeds 20–29; the calibration block used seeds 15–19. There were 44 eligible candidate rows and six unique signatures across the confirmation block. All 44 rows became skill instances: 22 reflection and 22 rotation. No counting or grouping skill was born under the frozen eligibility and minimum-quality gates. Terminal states were 22 `growing` and 22 `core`.

### Verdict

- **Supported narrowly:** the saved synthetic pipeline converts validated reflection/rotation candidates into represented skill objects. Skills are reused; all 44 created instances had at least one positive-credit reuse in the ledger.
- **Not supported broadly:** only two of the four intended families produced skills. The evidence does not show general-purpose skill emergence, a broad range of invariant-to-skill transformations, or ARC skill formation.
- **Causal wording limit:** the pipeline operationally constructs skills from its validated candidates; the experiment does not independently establish that invariant validation is necessary or uniquely responsible for useful skill emergence.

The cli completion line once displayed calibration seeds while reporting confirmation, but the saved `record.json` records seeds 20–29 as the confirmation block; the 13C evidence package documents this as a reporting-only CLI defect. No seed replacement is indicated.

## 14C-3 — SCT-2: SCV and future value

### Association evidence

Phase 13C reports SCV10 vs. shadow realized future net value Spearman `ρ=0.700427`, 95% seed-cluster bootstrap CI `[0.544724,0.930595]`, 44 candidate rows nested in 10 seed clusters. SU vs. future net value is more strongly associated (`ρ=0.936960`, CI `[0.896692,1.000000]`), as are SU vs. reuse count (`ρ=0.936960`) and SU vs. cross-family transfer (`ρ=0.921589`). These are synthetic candidate-level associations; the 44 rows are not 44 independent seed replications.

SCV is not uniquely strong among available predictors:

| Predictor of shadow future net value | Spearman ρ | 95% seed-cluster bootstrap CI |
|---|---:|---:|
| SCV10 | 0.700 | [0.545, 0.931] |
| Frequency | 0.748 | [0.709, 0.885] |
| `p_reuse` | 0.884 | [0.874, 0.937] |
| AG | -0.074 | [-0.110, 0.000] |
| TS | 0.000 | [0.000, 0.000] |

The numerical ordering does not establish a statistically significant difference between predictor correlations; no superiority test is reported. SU is also a repository-defined utility that shares synthetic task and shadow-value structure, so its high association should not be interpreted as independent validation of a general utility construct.

### Association is not selection advantage

Calibration had 22 eligible candidates, all with SCV10 > 0. The frozen primary cutoff was 0, so all 44 confirmation candidates were selected. Calibration also set random-create probability to 1.0. Thus the score carried candidate-level association information, but at the frozen operating point it did not create a meaningful accept/reject contrast. Phase 13F's no-SCV and random-SCV arms matched ASFT on task utility and CGR in the saved run matrix and constructed the same mean number of skills.

Threshold sensitivity is descriptive, not a replacement primary result: in 13C, q25 selected 28/44 and mean shadow net value was `.418`; q75 selected 4/44 and scored `.018`; the primary cutoff selected 44/44 and scored `.345`. These results show operating-point sensitivity. They do not license choosing a different cutoff after observing the outcomes.

**Verdict:** SCV has an association with future value in this synthetic sample. Predictive advantage over frequency or `p_reuse`, and an incremental creation-policy advantage, remain unestablished.

## 14C-4 — SCT-3: policy comparison and why the primary result failed

### Phase 13C primary net value

| Policy | Mean net value | 95% seed-bootstrap CI |
|---|---:|---:|
| SCT | 0.345 | [0.305, 0.385] |
| ALWAYS_CREATE | 0.345 | [0.305, 0.385] |
| RANDOM_CREATE | 0.345 | [0.305, 0.385] |
| NEVER_CREATE | 0.000 | [0.000, 0.000] |
| MEMORY_ONLY | 1.325 | [1.325, 1.325] |

SCT minus ALWAYS_CREATE and SCT minus RANDOM_CREATE are both exactly `0.000` (zero between-seed variance). SCT minus MEMORY_ONLY is `-0.980`, bootstrap CI `[-1.020,-0.940]`. The predeclared strict superiority criterion failed.

### Diagnosis: no primary selection pressure

The frozen primary threshold was 0 and all confirmation candidates had positive SCV; SCT selected all 44. Because calibration's all-positive score distribution also set random-create probability to 1.0, RANDOM_CREATE likewise became always-create. Accordingly, the primary comparison evaluated a non-selective SCT operating point. It did **not** evaluate the policy's ability to reject low-value candidates.

This is the strongest evidence for Hypothesis B (insufficient selective pressure in the tested candidate pool). It explains the observed equality but is not proof that SCT would succeed on another candidate distribution. The correct scientific outcome is still that the frozen primary gate failed; it must not be retroactively redefined as a pass.

### Phase 13F cross-check

In Phase 13F (seeds 70–79), the B3 random-skill-creation contrast failed/null on the joint task-utility-and-CGR gate. The A2_NO_SCV and A2_1_RANDOM_SCV arms match ASFT on saved task utility, SU, TS, CGR, IG and mean persistent-skill count. This adds cross-phase evidence that an incremental SCV/policy benefit was not demonstrated in those frozen settings. Phase 13F also includes a distinct baseline comparison described under the memory section below; metrics and arms are not interchangeable with Phase 13C.

## 14C-5 — Skill reuse and measured reasoning cost

Phase 13C recorded 440 eligible SCT opportunities: 223 applications, 201 correct positive-credit applications, 22 failures, and 217 no-matches. The mean raw step saving among applied rows was 1.000; the mean normalized reasoning reduction among correct applications was 0.227. Incorrect replays receive zero benefit in the saved accounting. This supports reuse and step-cost reduction in the simulator, but not wall-clock, FLOP, or real-world economic savings.

The matched memory-only arm applied all 440 opportunities, had 418 correct applications (0.950 correct/eligible) and 22 failures. SCT had 201 correct/eligible (0.457). In this design exact stored trace replay was more reliable on the recorded tasks. That supports a specific concern: when tasks recur closely, memory can capture much of the benefit attributed to reusable abstractions at lower measured net cost. It does not show that memory is universally superior, or that abstractions have no value in a distribution where exact replay cannot match.

## 14C-6 — Memory-only result: reconcile, do not overgeneralize

| Evidence | Result | Interpretation limit |
|---|---|---|
| Phase 13C `MEMORY_ONLY` vs SCT | Net value 1.325 vs 0.345; SCT-minus-memory `-0.980`; memory correct/eligible 0.950 vs 0.457 | Strong memory-only result on this matched synthetic primary metric and task stream. |
| Phase 13F `B2_MEMORY_SKILL_STORE` vs ASFT | Task utility 0.715 vs 0.789906; CGR 0.000 vs 0.287172; the frozen joint baseline criterion passes for ASFT | A different memory-skill-store arm, multi-arm setting, metric set, seeds, and protocol; not the same exact episodic MEMORY_ONLY control. |
| Phase 13F SCT-related controls | B3 random creation fails/null against ASFT; no-SCV/random-SCV arms tie ASFT | Does not show SCT selection advantage over naive creation; does not establish universal memory superiority. |

**Judgment:** “Memory beats abstraction” is too broad. The defensible result is that **Phase 13C's exact-replay MEMORY_ONLY policy outperformed SCT on that experiment's net-value outcome, while Phase 13F's distinct B2 memory-skill-store baseline did not outperform ASFT on its joint criterion**. Therefore, SCT has not established an advantage over memory-based alternatives, and memory has not established universal superiority.

## 14C-7 — Composition

In Phase 13C, only rotation→reflection was evaluable because counting/grouping component skills were absent. Across 100 paired tasks, ordered composition succeeded on 100%, the best single component on 0%, and the no-skill composition-capable solver also succeeded on 100%. Success-gated normalized reasoning reduction was 0.429; all 10/10 separately seeded composition-reuse tasks succeeded.

This demonstrates that the implemented pair can be invoked in order and can reduce measured reasoning steps on those generated tasks. Because the no-skill solver already had 100% task success, the success result does not show that composition was necessary to solve those tasks; the clearest incremental outcome is the measured reduction relative to the task baseline/best-single comparator. It is still one operation pair, not evidence for diverse skill chains.

Phase 13F's A2_3_NO_COMPOSITION arm had lower task utility than ASFT by `0.0773` and lower compose-task utility by `0.6188` in its frozen comparison. This supports a synthetic composition effect for that protocol, but does not expand the demonstrated component set or establish general composition. Counting-containing and broader multi-skill chains remain unavailable.

## 14C-8 — Lifecycle

The Phase 13C lifecycle probe recorded dormancy for 44/44 entries; 22/44 reactivation attempts succeeded and 22/44 did not. This is evidence that the implementation exercises dormancy and reactivation states, with mixed outcomes. It is not broad validation of the lifecycle theory. No retirement value or robust lifecycle benefit is established by this probe. Most decisively, the frozen no-lifecycle ablation tied the primary Phase 13C mean net value at `0.345`; Phase 13F's no-lifecycle contrast also showed zero differences in its recorded SCT outcomes.

**Verdict:** lifecycle machinery is operationally exercised; the claim that lifecycle control improves value or is needed remains unvalidated in these tests.

## 14C-9 — ARC interpretation

Phase 13G's bounded ARC adapter yielded zero accepted invariants, zero skills, and zero capabilities. Exact demonstration fit was only 3/600 discovery tasks, 5/200 transfer tasks, and 2/200 holdout tasks under a compact DSL; skill promotion required at least three applicable transfer tasks plus frozen qualification. Holdout exact task accuracy was `0.005` for the bounded system.

**Supported:** ARC skill emergence was not demonstrated by the current bounded adapter.  
**Not supported:** skill creation is impossible on ARC or the broader SCT theory is disproven.  
**Reason:** representation/DSL coverage and fit rates were too limited to provide a broad, adequately powered test of skill formation. Phase 13G's same-holdout rerun after an initial report-serialization failure is not pristine independent confirmation; preserve this caveat.

## 14C-10 — Threats to validity

The detailed register is [`threats_to_validity.csv`](threats_to_validity.csv). Principal threats:

1. **No selective pressure (high):** all 44 13C confirmation candidates were positive at the frozen zero cutoff; random-create probability was 1.0.
2. **Limited candidate/family diversity (high):** six signatures, 44 rows, but births in only two of four families; rows are nested within ten seed clusters.
3. **Memory-friendly repetition (high):** exact trace retrieval performs strongly in 13C's repeated synthetic task stream; this is not evidence about distributions with weak replay affordances.
4. **SCV construct and comparison limits (high):** candidate correlation is not policy benefit; simpler predictors have similar or higher numeric association, without pairwise correlation-superiority tests.
5. **Modelled costs (medium/high):** MC is a normalized simulator maintenance penalty; changing it from 0 to 0.12 changes 13C mean net value from 0.945 to -0.255. This is not observed compute cost.
6. **Composition/lifecycle scope (medium):** one pair and limited state transitions; the no-lifecycle ablation does not improve primary value.
7. **ARC adapter coverage (high):** very low exact-fit rates, no promoted skills, and no external replication.

## 14C-11 — What survives, what must be narrowed

### Survives

- Synthetic construction of reflection and rotation skills from validated trace candidates.
- Reuse of constructed skills and positive, success-gated simulator step-cost reductions in some cases.
- A narrow rotation→reflection composition implementation result, with additional synthetic support from the 13F no-composition contrast.
- An association between SCV10 and future shadow value in the Phase 13C candidate sample.

### Does not survive as a demonstrated general claim

- Broad skill emergence across families/domains.
- SCV as the best predictor or a selection policy with established incremental value.
- SCT superiority to ALWAYS_CREATE or RANDOM_CREATE on the primary Phase 13C criterion.
- A general advantage over memory-based retrieval.
- Broad lifecycle-policy value or general composition.
- ARC skill emergence or external validity.

### Reformulation guidance

Retain skill construction, reuse and narrow composition as synthetic mechanism results. Reformulate SCT from an established policy theory to a **candidate-value hypothesis**: SCV is one possible signal for future skill utility, but the present operating point did not discriminate. Separate the proposition “SCV correlates with future value” from “SCV improves creation decisions,” and from “the full skill policy adds value after creation and maintenance costs.” Do not change thresholds or reinterpret existing nulls in Phase 13.

## 14C-12 — Revised SCT claim

> **“In controlled synthetic environments, ASFT can construct and reuse reflection and rotation skills from recurring trace patterns, with measured simulator step-cost reductions in some cases. SCV is associated with future value in one synthetic candidate sample, but the evidence does not demonstrate an incremental selection advantage over simple creation policies. Composition is supported only for a limited synthetic operation pair, and skill emergence on ARC has not been demonstrated.”**

## 14C-13 — Final scorecard

| Claim | Status | Basis |
|---|---|---|
| Skills emerge from validated synthetic candidates | ✅ Supported narrowly | 44/44 Phase 13C instances are reflection/rotation. |
| General skill emergence across four families | ❌ Unsupported | Counting/grouping births are zero; only two families appear. |
| Skills are reused | ✅ Supported narrowly | 201 correct positive-credit SCT reuses; 44/44 skill instances reused at least once. |
| Skills reduce reasoning cost | ✅ Simulator evidence | Mean normalized reduction 0.227 on correct applications; not compute-time savings. |
| SCV is associated with future value | 🟡 Partial | `ρ=.700`, CI `[.545,.931]`, one synthetic sample; candidate-level association. |
| SCV is superior to simpler predictors | ❌ Not demonstrated | Frequency `.748`, `p_reuse` `.884`; no paired superiority test. |
| SCT beats ALWAYS_CREATE | ❌ Failed on primary gate | Exact tie at `.345`; all candidates selected. |
| SCT beats RANDOM_CREATE | ❌ Failed on primary gate | Exact tie; calibration probability was 1.0, so random arm degenerated. |
| SCT beats MEMORY_ONLY | ❌ Not in 13C; cross-phase general claim mixed | 13C MEMORY_ONLY wins net value; distinct 13F B2 memory-skill-store loses to ASFT on its joint metric. |
| Composition works | 🟡 Promising, limited | One rotation→reflection pair; 13F supports value in its synthetic task set. |
| Lifecycle theory adds value | ❌ Not demonstrated | Mixed 22/44 reactivation probe; no-lifecycle primary net value tie. |
| ARC skill emergence | ❌ Not demonstrated | Zero skills/capabilities in bounded, low-coverage adapter. |

**Exit decision: Phase 14C COMPLETE.** SCT survives as a synthetic skill-construction/reuse mechanism. SCT as a selective policy, an improvement over the primary naive creation controls, and a general improvement over memory remain unvalidated.

## Package contents

- [`memory_interpretation.md`](memory_interpretation.md) — matched Phase 13C memory-only result versus the distinct Phase 13F B2 comparator.
- [`composition_lifecycle_arc.md`](composition_lifecycle_arc.md) — focused analysis of composition, lifecycle, and ARC limitations.
- [`sct_scorecard.csv`](sct_scorecard.csv), [`scv_predictor_comparison.csv`](scv_predictor_comparison.csv), [`policy_failure_analysis.csv`](policy_failure_analysis.csv), and [`threats_to_validity.csv`](threats_to_validity.csv) — structured supporting tables.

## Evidence sources

- Phase 13C: [`evidence_package.md`](../PHASE-13C-SCT-V1/evidence_package.md), [`summary.md`](../PHASE-13C-SCT-V1/summary.md), [`correlations.json`](../PHASE-13C-SCT-V1/correlations.json), [`composition.csv`](../PHASE-13C-SCT-V1/composition.csv), [`lifecycle.csv`](../PHASE-13C-SCT-V1/lifecycle.csv), [`candidate_level.csv`](../PHASE-13C-SCT-V1/candidate_level.csv), [`matched_controls.csv`](../PHASE-13C-SCT-V1/matched_controls.csv).
- Phase 13F: [`evidence_package.md`](../PHASE-13F-BASELINE-ABLATION-V1/evidence_package.md), [`master_result_matrix.csv`](../PHASE-13F-BASELINE-ABLATION-V1/master_result_matrix.csv), [`candidate_selection.csv`](../PHASE-13F-BASELINE-ABLATION-V1/candidate_selection.csv), [`run_manifest.json`](../PHASE-13F-BASELINE-ABLATION-V1/run_manifest.json). Interrupted attempt 01 is preserved separately and excluded.
- Phase 13G: [`evidence_package.md`](../PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/evidence_package.md).
- Consolidated interpretation: [`Phase 13H Package B`](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/package_B_SCT.md), [`claim evidence matrix`](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/claim_evidence_matrix.csv), [`negative evidence register`](../PHASE-13H-EVIDENCE-CONSOLIDATION-V1/negative_evidence_register.csv).
- Provenance: [`source_manifest.json`](source_manifest.json) and [`source_hashes.csv`](source_hashes.csv) list the reviewed source artifacts and SHA-256 hashes.
