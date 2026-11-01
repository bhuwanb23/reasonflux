# Phase 14A — Evidence Integrity Review

**Review ID:** `PHASE-14A-EVIDENCE-INTEGRITY-REVIEW-V1`  
**Scope:** saved Phase 13A–13H records, protocols, run/freeze manifests, posthoc analyses, and claim mapping.  
**Work performed:** documentation/artifact audit only. No benchmark was run as part of Phase 14A; no Phase 13 result, threshold, formal metric definition, dataset, or success criterion was edited.  
**Verdict:** **PASS WITH LIMITATIONS** — sufficiently trustworthy to proceed to Phase 14B critical analysis, but not an unqualified certification of exact replayability or complete provenance.

## 1. Executive finding

The review found **no evidence in the available records** that a failed gate was reversed, a null/adverse result hidden, or a confirmatory result replaced by an exploratory result. It did find a material, disclosed Phase 13B post-result cost-accounting correction: the solver began charging a required family-output reasoning step, and saved baseline results changed relative to the local `HEAD` version. This did not improve the primary comparison—the informed arms still tie and the strict gate still fails—but the two measurement versions must not be described as unchanged. No recorded threshold change was found. Failed outcomes remain in the evidence packages, and later reporting corrections and the Phase 13G holdout exposure are disclosed. Protocol and run hashes, seed/task records, and source manifests provide useful audit trails for Phases 13C–13G; Phase 13H separately hashes its 31 cited source artifacts.

The integrity qualification matters:

- Reproducibility and provenance are **not complete**. Run manifests do not consistently capture Git SHA, dirty-tree state, or a full environment lock. Phase 13B has less run-specific hash provenance than later phases. The current checkout is dirty, so it cannot certify a clean replay.
- Several preflight documents are still frozen snapshots saying that a future confirmation run had not happened, while later run/evidence manifests show completed experiments. This is a stale-documentation inconsistency, not evidence of result manipulation; use the dated freeze/run manifests and final evidence packages as the later record. This report does not edit those historical preflights.
- Phase 13D’s corrected comparisons and Phase 13E/F posthoc reporting summaries are saved-record-only but were produced after execution. They are disclosed analysis corrections, not preregistered independent replications; preserve and cite the original frozen outputs alongside the correction.
- Phase 13G’s attempt 02 reused the same holdout after attempt 01 had generated predictions in memory. The recorded attempt says outcomes were not inspected during debugging, but this is not independent or pristine holdout confirmation.

**Decision:** Phase 14 may analyze the scientific meaning of these records, provided the above limitations travel with every affected claim. “PASS” here means integrity is adequate for critical results analysis; it does not mean the hypotheses passed or the results are externally valid.

## 2. Scope and method

Audited sources include Phase 13A governance/smoke artifacts; the original Phase 13B results and EXP-IDT-14; Phase 13C preregistration/freeze and evidence; Phase 13D preregistration hashes plus corrected saved-record analysis; Phase 13E/F frozen and completion manifests, seed summaries, and posthoc manifests; Phase 13G pre-run/run manifests and failure disclosure; and Phase 13H’s evidence package, claim matrix, and source manifest.

Checks were documentary and hash-based where hashes were already recorded: whether the protocol/seed/config/failure status is described; whether saved source digests are present; whether posthoc work states that it reused saved records; whether the claim-to-evidence chain can be traced; and whether exploratory material is kept distinct. This is not a fresh rerun, a forensic audit of every execution host, or proof that no unrecorded action ever occurred. No test suite or benchmark was run for Phase 14A.

Machine-readable audit tables are in this folder: [`protocol_audit.csv`](protocol_audit.csv), [`claim_traceability_audit.csv`](claim_traceability_audit.csv), [`exploratory_confirmatory_register.csv`](exploratory_confirmatory_register.csv), [`reproducibility_audit.csv`](reproducibility_audit.csv), [`evidence_risk_register.csv`](evidence_risk_register.csv), and [`integrity_scorecard.csv`](integrity_scorecard.csv). `source_manifest.json` records hashes of the reviewed files and the audit-time checkout state.

## 3. Phase 13A — governance and validation setup

**Finding: PASS for governance framework; not a formal experimental result.** The Phase 13A specification documents experiment governance, dataset tiers, seed policy, metric governance, statistical reporting, reproducibility requirements, and an experiment registry. The actual `phase13a_gates` artifacts are explicitly seed-0 `mode=smoke` checks. They report readiness successes, including a smoke end-to-end/baseline check, and explicitly state “readiness smoke checks, not formal multi-seed evidence.” Those smoke outputs are not used here as scientific support for ASFT claims.

**Provenance limitation:** the project’s governance requirements ask for strong reproducibility, but the Phase 13A artifacts do not establish universal per-run Git SHA, environment hash/lock, or dirty-tree capture. This is a low-severity paper-quality/provenance gap for interpreting later results, not evidence that the smoke checks were misreported.

## 4. Phase 13B — IDT integrity

**Finding: PASS.** The original `synthetic-v1`, seeds 0–4, remains explicit that ASFT top-k=2 ties frequency-only and no-transfer at held-out TU `0.095809`; its strict all-control/per-seed baseline gate remains **failed**. The report explains that the three informed policies select the same semantic ranking in every seed. EXP-IDT-14 is described separately as a post-tie, deliberately confounded stress test and is explicitly not a retrospective repair of Phase 13B.

The failure is preserved, and the later favorable stress-test outcome is not substituted for it. **A material version-lineage issue was found:** the working-tree `src/solver/executor.py` adds an explicit `count_objects`/`group_by_color` reasoning step when a reused macro omits the required output operation. The new Phase 13B report discloses this as a cost-accounting correction and says transfer utility fell. The working-tree Phase 13B baseline outputs also differ from local `HEAD`: the old `HEAD` summary records ASFT/frequency/no-transfer mean TU `0.143130`, while the current corrected summary records `0.095809`; both versions tie the informed arms and fail the strict gate. This looks like a disclosed measurement correction, not evidence of a success-driven threshold change, but the current run lacks a separate complete execution manifest and the current output files are modified/untracked relative to `HEAD`. Therefore, Phase 13B values are **not unchanged**; exact magnitude claims must identify which accounting version they use. Preserve both snapshots, the correction rationale, and the failed gate in Phase 14B.

The Phase 13B report identifies the governing config/threshold files and top-k rule, but run-level provenance is less complete than later phase-specific hash manifests. The report and saved artifacts support the gate status; they do not amount to a modern, fully hermetic replay record.

## 5. Phase 13C — SCT integrity

**Finding: PASS.** The pre-confirmation freeze records calibration seeds 15–19, confirmation seeds 20–29, frozen parameters unchanged, hashes for configuration/preregistration/runner/calibration, and contract-test results. The final evidence package preserves the strict SCT superiority failure: SCT `0.345`, ALWAYS_CREATE `0.345`, RANDOM_CREATE `0.345`, and MEMORY_ONLY `1.325`; it also preserves absent counting/grouping births and unavailable composition cells.

The post-run module reorganization and CLI completion-line seed-display defect are disclosed in the analysis/execution manifests; the confirmation record/hash is identified as unchanged, and no benchmark rerun is claimed. `phase_13c_preflight.md` still says that no validation run had been made and that the phase was not validated. That is a historical preflight snapshot now stale relative to the later freeze/record/evidence package. It should not be silently edited; cite it only as a pre-run document and use the later run evidence for status.

## 6. Phase 13D–13F — transfer, growth, baselines, and ablations

**Finding: PASS WITH POSTHOC-DISCLOSURE LIMITATIONS.**

- **13D:** `preregistration_hashes.json` stores a root hash and file-level hashes for 204 entries. The corrected posthoc analysis states that it reads saved task/seed records only, explains the aggregator key defect behind earlier `n=0` comparisons, and does not regenerate tasks, rerun a solver, change the frozen protocol, or alter outcomes. It also corrects a composition interpretation by checking source-component coverage and active composition applications. The correction is transparent and needed for interpretation; it remains a posthoc reporting/statistical correction, not a new independent confirmatory experiment. The preflight still says “hash freeze pending” and “no confirmation run”; later manifests and result artifacts supersede that snapshot.
- **13E:** the final run manifest records 10 completed seeds (60–69), config/preregistration/preflight hashes, source-tree hash, platform/Python, and a saved-record posthoc analysis with `benchmark_rerun=false`. Positive CGR/IG do not obscure the negative IE trend, adverse composition criterion, or B1 utility failure. The preflight’s “no confirmation seed has been run” status is historical and stale after the completed run.
- **13F:** frozen and completion manifests identify the replacement confirmation block 70–79, config/preregistration/source-tree hashes, contract-test record, and `prior_phase_evidence_modified=false`. The interrupted seed-0 attempt is preserved separately and excluded. Null ablations and failed B1/B3 joint comparisons remain reported. The posthoc figure-label correction is disclosed and did not rerun a benchmark.

**Integrity interpretation:** later reporting corrections are not evidence of hidden results when their scope, saved inputs, and non-rerun status are recorded; however, they must remain labeled posthoc. Any phase conclusion that depends on corrected 13D pairwise comparisons must cite the correction and retain the original reporter artifacts for audit.

## 7. Phase 13G — ARC integrity

**Finding: PASS WITH MEDIUM HOLDOUT-EXPOSURE LIMITATION.** The pre-run manifest records the ARC-AGI-2 commit, dataset-source and split hashes, 600/200/200 disjoint task-ID split, configuration/preregistration/source hashes, and a pre-holdout lock. The completion manifest says the official evaluation JSON was not extracted or scored. The temporary-archive transport deviation and pre-run structural schema audit are disclosed; this report does not state that no evaluation bytes were ever downloaded.

The attempt-01 serialization failure is preserved. Its manifest says outcome tables were not persisted and outcomes were not inspected during debugging, but predictions had been generated in memory. Attempt 02 reused the same holdout after a software-only serialization fix. The evidence package correctly labels this non-independent and not a pristine holdout. No attempt is made to reframe zero invariants/skills/capabilities or 0.5% exact task accuracy as success. These controls support honesty and traceability; the repeated holdout still limits future external-validity strength.

## 8. Phase 13H — consolidation integrity

**Finding: PASS for source traceability, with a schema improvement needed.** Phase 13H is a posthoc consolidation, not a new experiment. It separates claims by status, retains null/adverse/unavailable findings, cites corrected Phase 13D results, and records 31 source hashes. The cited hashes were checked against the source files during this review.

The existing `claim_evidence_matrix.csv` has 11 major claims and embeds experiments/metrics in free-text evidence fields, but does not provide dedicated `experiment_id`, `metric`, and `evidence_artifact` columns for every claim. This is a traceability-format weakness, not a missing result. The supplemental [`claim_traceability_audit.csv`](claim_traceability_audit.csv) normalizes those links without changing Phase 13H or any Phase 13 evidence.

## 9. Frozen-protocol and failed-gate review

| Integrity check | Finding |
|---|---|
| Criteria defined before confirmation | Strongly evidenced by 13C–13G freeze/preregistration hashes and seed blocks; 13B documents its frozen top-k/strict gate but has weaker run-level hashes. No recorded post-result criterion changes were found. |
| Failed gates remain failed | Yes: Phase 13B baseline gate, Phase 13C SCT superiority, corrected Phase 13D all-mandatory-baseline gate, and selected 13E/13F baseline/ablation decisions remain adverse/null in the consolidated record. |
| Exploratory work separated | Yes: EXP-IDT-14 is explicitly supplemental/exploratory; saved-record posthoc corrections are labeled; 13G attempt 02 is not called independent. |
| Negative/unavailable outcomes preserved | Yes: missing component skills, zero births, null ablations, adverse growth/composition results, the 13G bounded-DSL null, and software/reporting failures remain visible. |
| Evidence contamination | No record was found of thresholds, formal metric definitions, datasets, or criteria being changed to improve a result. However, the Phase 13B post-result executor cost-accounting correction changed measured values relative to local HEAD; it is disclosed, the strict gate still fails, and magnitude claims must name the corrected/pre-correction version. This is a documentary finding, not proof of all unlogged history. |

## 10. Traceability audit

All 11 Phase 13H claims were checked against an experiment/phase, a named metric, a saved evidence artifact, and the status used in the claim. The supplemental audit records mappings such as `IDT-3 → Phase 13B / EXP-IDT-10 baseline comparison / held-out TU, top-k=2 / failed`, and `SCT-2 → Phase 13C / SCV10 vs shadow future net value / candidate-level Spearman and matched-policy contrast / associative evidence but no policy superiority`.

**Result: PASS WITH FORMAT CAVEAT.** The evidence mapping is substantively present; Phase 13H’s original CSV does not make every link a separate machine-readable column. The 14A supplement closes that retrieval gap while preserving the original matrix unchanged.

## 11. Exploratory vs confirmatory separation

- **Confirmatory/frozen evidence:** Phase 13B `synthetic-v1`; Phase 13C confirmation seeds 20–29 after calibration seeds 15–19; Phase 13D frozen seed block 50–59; Phase 13E seeds 60–69; Phase 13F replacement block 70–79; Phase 13G preregistered bounded ARC protocol/split, with the same-holdout caveat.
- **Exploratory/supplemental:** EXP-IDT-14; posthoc Phase 13D corrected comparisons; Phase 13E/F saved-record reporting corrections; Phase 13H cross-phase synthesis; Phase 13G attempt-02 rerun as a software-recovery execution, not an independent replication.
- **Readiness only:** Phase 13A smoke checks and software contract tests are not benchmark evidence.

**Result: PASS.** None of the explicitly exploratory cases is used to erase an earlier confirmatory failure.

## 12. Reproducibility and provenance

Artifact-level reproducibility is good but uneven. Phase 13C has a pre-confirmation freeze and artifact hashes; 13D has a 204-file preregistration hash set; 13E/F have frozen/completion manifests and source-tree/config/preregistration hashes; 13G has data/split/config/source hashes, a pinned upstream commit, and attempt records; 13H verifies source hashes for its consolidation. Phase 13B has seeds, metrics, configs, and a clear gate but less complete run-bound provenance.

**Unresolved provenance gaps:** Git commit is not captured in the 13E/F/G run manifests; no environment lock/hash is recorded uniformly; dirty-tree-at-run-time state is not uniformly captured; and no remote/upstream could be verified at this audit. At audit start, before this Phase 14A output folder was created, `HEAD` was `8f0213878998e2cea492d564469d4ee1936fc5c5` on `main`, but the worktree was dirty (42 modified, 39 untracked, 21 deleted status entries). This current state cannot prove the state of the tree when earlier runs executed. Phase 13E preflight itself notes an existing uncommitted repository state. Frozen source-tree/config hashes improve identification but do not fully substitute for Git/environment provenance.

**Classification:** reproducible from saved artifacts with meaningful hash/seed traceability; exact clean-environment replay is not certified. This gap affects provenance and replay confidence more than the integrity of the reported saved outcomes.

## 13. Evidence risk register

The risk register contains the requested five risks plus provenance, posthoc-reporting, and Phase 13B measurement-version risks. Synthetic generator/vocabulary overlap and low ARC DSL coverage are validity risks, not evidence of manipulation. See [`evidence_risk_register.csv`](evidence_risk_register.csv) for severity, impact, and control.

## 14. Integrity scorecard

| Category | Status | Basis |
|---|---|---|
| Frozen protocols | ✅ with 13B provenance caveat | Strong freeze/hash trail from 13C onward; 13B criterion/report explicit but less run-bound hashing. |
| Failed gates preserved | ✅ | Failed 13B/13C/13D and adverse baseline decisions remain in packages. |
| Phase 13B measurement lineage | ⚠ disclosed; carry forward | Cost-accounting correction changed TU from local HEAD 0.143130 to corrected 0.095809; both tie informed controls and fail the gate. |
| Phase 13B measurement lineage | ⚠ disclosed; carry forward | Cost-accounting correction changed TU from local HEAD 0.143130 to corrected 0.095809; both tie informed controls and fail the gate. |
| Exploratory separated | ✅ | EXP-IDT-14, posthoc corrections, smoke tests, and 13G rerun are labeled. |
| Negative evidence preserved | ✅ | Null, adverse, failed, and unavailable outcomes remain visible. |
| Claim traceability | ✅ after 14A supplement | 13H matrix substantively maps claims; dedicated experiment/metric/artifact columns added in audit supplement. |
| Baseline transparency | ✅ | Named B1–B4 results and proxy caveats are retained. |
| Ablation transparency | ✅ | Null/effect/unavailable statuses retained; no general causal conclusion presumed. |
| ARC transparency | ✅ with medium exposure caveat | Bounded DSL, low coverage, archive transport, and same-holdout rerun are disclosed. |
| Reproducibility | ⚠ adequate for saved-record analysis, incomplete for exact replay | Frozen artifacts/hashes exist, but Git/environment/dirty-state provenance is not uniform. |
| Provenance completeness | ⚠ | Phase 13A/13B weaker; stale preflight status snapshots; current worktree is dirty. |

## 15. Formal verdict and exit decision

### Main question: Can Phase 13 evidence be trusted for Phase 14 analysis?

**Yes, with limitations.** There is sufficient traceability, retention of failed/null outcomes, and disclosure of posthoc corrections/holdout exposure to proceed to Phase 14B. Do not describe the evidence base as perfectly reproducible, universally frozen at the Git/environment level, or free of every conceivable unrecorded manipulation.

### Formal verdict

**PHASE 14A: PASS WITH LIMITATIONS.**  
**Exit decision: proceed to Phase 14B.**

The strongest integrity finding is that no failed hypothesis, baseline, ablation, or ARC outcome was found to have been hidden or replaced by the exploratory follow-up. The weakest area is provenance completeness, followed by Phase 13G holdout exposure and stale preflight status documents. These limitations constrain the strength and reproducibility of later conclusions but do not, on the available record, invalidate the saved Phase 13 evidence for critical analysis.

### Required carry-forward conditions for Phase 14B

1. Keep the original Phase 13B strict baseline gate failed; EXP-IDT-14 cannot repair it.
2. Cite Phase 13D’s corrected posthoc view as a disclosed correction and retain the frozen reporter for audit.
3. Keep Phase 13G bounded-DSL coverage and same-holdout reuse caveats attached to any ARC statement.
4. Treat Phase 13A smoke checks and contract tests as software/readiness evidence only.
5. Use the explicit claim→experiment→metric→artifact mappings in `claim_traceability_audit.csv`; do not rely solely on Phase 13H free-text cells.
6. Do not rerun, retune, or revise earlier criteria in Phase 14. Analyze the saved record and classify conclusions as supported, partial, unsupported, or unavailable.
7. For Phase 13B magnitude claims, preserve and identify both the pre-correction local-HEAD snapshot and the corrected working-tree result; explain the family-output cost-accounting correction. The strict baseline failure is common to both versions, but their absolute transfer-utility means differ.
