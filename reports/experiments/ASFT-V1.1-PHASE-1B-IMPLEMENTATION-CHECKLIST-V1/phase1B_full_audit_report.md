# ASFT v1.1 Phase 1B — Full Selection-Pressure Audit Report

**Phase ID:** `ASFT-V1.1-PHASE-1B`  
**Implementation package:** `ASFT-V1.1-PHASE-1B-IMPLEMENTATION-CHECKLIST-V1`  
**Scope:** Forensic audit of the v1.0 SCT selection failure, review and correction of the first v1.1 Phase 1B specification/harness, and execution of implementation-contract tests on synthetic fixtures.  
**Decision:** **CONTRACT HARNESS PASS; FULL BENCHMARK / CONFIRMATORY READINESS NOT YET PASSED.**  
**Experiments:** No SCT/SCV research experiment, calibration study, confirmatory data collection, or independent task benchmark was run.

## 1. Executive decision

Phase 1B exists to make SCT/SCV selection falsifiable. The v1.0 failure was not just a missing metric: the selector did not face meaningful accept/reject choices. Phase 13C selected 44/44 candidates; calibration made random-create probability 1.0; Phase 13F selected all four candidates in ASFT/no-SCV/random-SCV arms. Under those conditions, the selection policy could not demonstrate an incremental advantage.

The first Phase 1B response correctly specified a balanced pool, fixed capacity, independent value, selectors, and an SDR gate. It was **not yet sufficient as an implementation/readiness package**. The first harness only checked pre-outcome choice divergence, used type-ordered IDs/arrival order that exposed candidate class, and had no explicit outcome-response test proving the value pipeline could record SCV wins, ties, and losses. Those defects are corrected in the current package:

- Candidate IDs are now opaque and arrival order is seeded independently of latent class.
- The selector API receives only feature cards; labels and synthetic truth are separate records.
- The suite now has **26 contract checks**, including outcome-response tests for a known loss, a tie, and a win.
- **26/26 contracts pass** on the current synthetic contract harness.
- On 100 deterministic pressure fixtures using one fixed feature/type recipe, **100/100 pass**; mean contested SDR is **0.3682**, minimum **0.2500**, maximum **0.5000**.
- A post-decision synthetic adverse-value fixture shows SCV losing to Random, capacity-limited Always, and Never; it wins over Frequency and Reuse in that same fixture. These are tests of the evaluator's ability to expose a loss—not evidence about SCV performance.

**Brutal-honesty boundary:** the code under test is a small contract harness, not the full research benchmark. The synthetic truth is recipe-generated, not produced by the actual task solver on a frozen independent task set. The 100 panels reuse the same feature/type profile and vary panel/random seeds; they are not 100 independent experimental units. Cost conversion, statistical power, real split artifacts, production isolation, and the actual task/outcome runner remain unimplemented. Thus Phase 1B has passed its **fixture contract** stage but is **not ready to unlock confirmatory SCT testing**.

## 2. Source audit: why v1.0 did not test selection

### Phase 13C — primary SCT comparison

The saved Phase 13C confirmation reports 44 eligible candidate rows. All 44 had `SCV10 > 0` under the frozen zero cutoff, so SCT selected every candidate. `ALWAYS_CREATE` also selected all candidates. The calibration set had 22/22 positive candidates, making the frozen Bernoulli `RANDOM_CREATE` probability 1.0; that arm therefore became deterministic always-create. The primary net-value means were all 0.345 for SCT, always-create, and random-create. The primary gate failed; the tie is not evidence that the policy can never discriminate on a different pool.

The candidate-value correlations are not an alternative policy test: SCV10 rho was 0.700 against shadow realized net value, while frequency was numerically 0.748 and `p_reuse` 0.884; 44 candidate rows were nested in ten seed clusters, and no paired correlation-superiority test was reported. Candidate-level association does not establish that accepting/rejecting via SCV improves selected-set value.

### Phase 13F — selection ablations

The saved candidate-selection record has four qualified candidates per seed. ASFT, `A2_NO_SCV`, and `A2_1_RANDOM_SCV` each constructed all four, so their candidate sets could not differ. Their recorded task utility, SU, TS, CGR, and IG are tied. `B3_RANDOM_SKILL_CREATION` is a different 75%-of-pool policy and constructed three skills; it must not be conflated with the matched-k random-SCV arm. Its aggregate tie indicates outcome insensitivity or low leverage in that setting, not necessarily identical selected candidates.

### Phase 14C / 14F — critical interpretation

Phase 14C identifies the all-positive pool and degenerate random probability as the strongest supported explanation for the Phase 13C tie, and separates score association from selection advantage. Phase 14F concludes that SCV's incremental contribution is unsupported in the tested pools; this is local evidence, not a universal falsification. Its comparator names, endpoints, and candidate pools are phase-specific.

### Phase 1A design requirement

The Phase 1A redesign register required a fixed capacity below candidate count, positive/neutral/negative alternatives, a nondegenerate random policy, feature/label separation, matched budgets, and a pre-outcome divergence check. The present implementation package converts those requirements into runnable fixture assertions, but it does not yet instantiate the final independent task dataset.

## 3. Audit of the first Phase 1B implementation attempt

The earlier specification-only package was useful but was prematurely described as ready for implementation. The first contract harness also had two defects that this audit now records rather than hiding:

1. **Class information was encoded indirectly.** Candidate IDs contained class names and arrival order grouped candidate classes. Although the public card omitted a `latent_type` column, a selector could infer the class from IDs/order. The current harness replaces those IDs with opaque split/seed/candidate IDs and independently shuffles arrival order. CT-1C now checks the actual payload and positions across seeds.
2. **Only pressure was demonstrated.** Different selections do not prove the endpoint can register a loss. The earlier package had no outcome-response test. CT-9A/B/C and `outcome_response_sanity.csv` now verify loss/tie/win behavior using separately supplied fixture truth, while explicitly prohibiting those values from being treated as research evidence.

Other earlier limitations remain and are disclosed below: the values are fixed synthetic recipes; no actual solver/task runner, external cost calibration, statistical power simulation, operating system-level outcome store, or run-specific preregistration exists.

## 4. Contract test results

The test runner is `experiments/phase1b/run_contracts.py`; the selector/truth interfaces are in `experiments/phase1b/selection_benchmark.py`. Run from repository root:

```bash
python experiments/phase1b/run_contracts.py reports/experiments/ASFT-V1.1-PHASE-1B-IMPLEMENTATION-CHECKLIST-V1
```

### Full contract table

| ID | Requirement | Result |
|---|---|---|
| CT-1A | Five candidate classes present | PASS |
| CT-1B | Per-batch 4×A–E quotas and N=20 | PASS |
| CT-1C | Labels not exposed in selector fields, IDs, or deterministic arrival order | PASS |
| CT-2A | Future Net Value comes from the separate fixture outcome/cost record, not selection scores | PASS |
| CT-2B | Mutating SCV inputs does not change ground-truth value | PASS |
| CT-3A | Seven required policies operational; Oracle analysis-only | PASS |
| CT-3B | Same-seed deterministic replay | PASS |
| CT-3C | Tie-break ordering deterministic | PASS |
| CT-4A | Contested SDR ≥0.20 on each tested fixture | PASS |
| CT-4B | SCV Top-K differs from Frequency, Reuse, and Random | PASS |
| CT-4C | Pressure gate has no truth/outcome input | PASS |
| CT-5A | Creation/storage budget parity | PASS |
| CT-5B | Same candidate pool/opportunity IDs | PASS |
| CT-5C | Ten-opportunity fixture horizon parity | PASS |
| CT-5D | Same public card schema; no hidden fields | PASS |
| CT-6A | No outcome fields in selector payload | PASS |
| CT-6B | No taxonomy label in selector payload | PASS |
| CT-6C | Split namespaces generate disjoint fixture IDs | PASS |
| CT-7A | Oracle excluded from production competition | PASS |
| CT-7B | Oracle cannot enter candidate generation or pressure check | PASS |
| CT-8A | Cost constants fixed in fixture | PASS |
| CT-8B | Reward formula and horizon fixed | PASS |
| CT-8C | Labels robust to tested ±5% fixture cost-conversion shift | PASS |
| CT-9A | Adverse-value case reports SCV losing to Random, Always, and Never | PASS |
| CT-9B | Equal-value case reports a tie among K-sized selectors | PASS |
| CT-9C | Outcome pipeline can report SCV winning over Frequency and Reuse | PASS |

All row-level results are in [`contract_test_results.csv`](contract_test_results.csv); the separate summary is in [`phase1B_contract_checklist.csv`](phase1B_contract_checklist.csv).

## 5. Candidate taxonomy, label concealment, and value independence

The fixture generates four candidates in each type A–E: A positive, B neutral, C negative, D deceptive/negative over the full horizon, and E rare high-impact. Candidate type and outcomes are kept in a `TruthRecord`, separate from `CandidateCard`. The card is the only object passed to the production selector functions. IDs no longer contain the type, and arrival order is seeded separately from type assignment.

The value function sums ten paired utility deltas and subtracts creation and maintenance costs. It does not accept SCV, frequency, reuse probability, or compression score as arguments. CT-2A/2B mutate score inputs and verify that the stored fixture truth is unchanged.

**Limit:** this is an interface/separation contract, not an independent task outcome experiment. The truth recipes are deliberately synthetic and class-conditioned. A production generator must construct expected value from a frozen outcome process without selecting confirmatory items on observed outcomes; the test harness does not yet integrate that generator.

## 6. Pressure validation and pairwise divergence

### Frozen fixture gate

- 20 candidates; K=8; one equal storage unit per candidate and storage budget 8.
- S1–S5 select 8/20; S6 Never is the explicit 0% sentinel exception; S7 Oracle is excluded from pressure.
- Each panel requires `D(SCV,Frequency)`, `D(SCV,Reuse)`, and `D(SCV,Random)` ≥0.10.
- Contested SDR is the mean pairwise symmetric-difference rate across S1–S4 and must be ≥0.20.
- Pressure code receives only cards and policy choices; it cannot read the `TruthRecord`.

### Results across 100 fixture panels

| Diagnostic | Result | Gate |
|---|---:|---:|
| Fixtures tested | 100 | Contract fixtures only |
| Pressure-gate pass | 100/100 | All fixtures pass |
| Mean contested SDR | 0.3682 | ≥0.20 |
| Minimum contested SDR | 0.2500 | ≥0.20 |
| Maximum contested SDR | 0.5000 | — |
| Mean/min SCV–frequency divergence | 0.4000 / 0.4000 | ≥0.10 each |
| Mean/min SCV–reuse divergence | 0.4000 / 0.4000 | ≥0.10 each |
| Mean/min SCV–random divergence | 0.4590 / 0.3000 | ≥0.10 each |

These 100 generated panels reuse the same deterministic candidate feature/type recipe; seeds change IDs, independent arrival ordering, and random-selector draws. They are not a powered study or 100 independent populations.

### Pairwise divergence matrix, fixture seed 0

`D(a,b)=|S_a △ S_b|/N`.

| Selector | S1 SCV | S2 Frequency | S3 Reuse | S4 Random | S5 Always-cap | S6 Never |
|---|---:|---:|---:|---:|---:|---:|
| S1 SCV | 0.00 | 0.40 | 0.40 | 0.60 | 0.40 | 0.40 |
| S2 Frequency | 0.40 | 0.00 | 0.00 | 0.50 | 0.60 | 0.40 |
| S3 Reuse | 0.40 | 0.00 | 0.00 | 0.50 | 0.60 | 0.40 |
| S4 Random | 0.60 | 0.50 | 0.50 | 0.00 | 0.40 | 0.40 |
| S5 Always-cap | 0.40 | 0.60 | 0.60 | 0.40 | 0.00 | 0.40 |
| S6 Never | 0.40 | 0.40 | 0.40 | 0.40 | 0.40 | 0.00 |

Frequency and reuse tie in this particular fixture, while SCV differs from both. The gate does not demand that every baseline pair disagree; it prevents the v1.0 failure mode where SCV matches every serious comparison. Machine-readable matrix and aggregate are `pairwise_divergence_matrix.csv` and `pressure_validation.json`.

## 7. Outcome-response audit: can the benchmark expose an SCV loss?

After fixture choices are frozen, the separate synthetic truth record is evaluated. This is a deliberately adverse **unit-test scenario**, not observed research data.

| Policy | Selected types A/B/C/D/E | Mean net value per slot (TEU) | Difference vs SCV |
|---|---|---:|---:|
| S1 SCV | 4/0/0/4/0 | **−0.5500** | 0.0000 |
| S2 Frequency | 0/0/4/4/0 | −3.1750 | −2.6250 |
| S3 Reuse | 0/0/4/4/0 | −3.1750 | −2.6250 |
| S4 Random | 2/2/3/0/1 | **+1.2313** | +1.7813 |
| S5 Always-capacity | 3/2/1/1/1 | **+1.1688** | +1.7188 |
| S6 Never | 0/0/0/0/0 | **0.0000** | +0.5500 |
| S7 Oracle | 4/0/0/0/4 | +2.9500 | +3.5000 |

This fixture makes the failure mode visible: SCV selects all four deceptive D candidates and misses all four rare high-impact E candidates. It loses to random, capacity-limited always, and never-create; it wins over frequency and reuse in the same fixture. A separate equal-value fixture produces a tie. Thus, the scoring/aggregation path can express win/tie/loss rather than forcing SCV to appear successful.

See [`outcome_response_sanity_report.md`](outcome_response_sanity_report.md) and [`outcome_response_sanity.csv`](outcome_response_sanity.csv). **Do not cite these fixture numbers as an ASFT result or as validation that SCV is weak/strong.**

## 8. Fairness, leakage, Oracle, and validity audit

- **Budget:** K=8, equal unit storage, common card pool. S6 is the required zero-rate anchor. S7 is analysis-only.
- **Opportunity:** all policies reference the same candidate IDs and ten-opportunity truth fixtures; selected candidates are scored on the same synthetic value record.
- **Information:** equal card schema is available to all selectors; each method uses its defined signal. Opaque IDs/independent arrival order prevent direct label reading. Features can correlate with type; that is a signal-vs-truth question, not a label field leak.
- **Outcome separation:** the pressure gate does not accept truth. Ground-truth arithmetic is independent of the ranker scores. The separate records are in one process, however; this is logical API separation, **not** production security or OS-level sealing.
- **Oracle:** the Oracle function receives truth only after policy rankings are produced. It is not in the production selector registry and does not enter the pressure checker.
- **Cost/reward:** test fixture cost and reward arithmetic is frozen and sensitivity-tested at ±5%. No empirical resource conversion or real cost model has been calibrated.
- **Split isolation:** only deterministic namespace/ID separation is tested. No real calibration, development, confirmatory, or replication datasets have been generated.

## 9. Remaining hard gates

| Unlock gate | Current status | Required before confirmatory outcomes |
|---|---|---|
| Gate-1: contracts pass | **PASS, fixture scope** | Re-run after any selector/generator change. |
| Gate-2: pressure validated pre-outcome | **PASS, fixture scope** | Run on the actual frozen candidate generator and log all panels before truth access. |
| Gate-3: exact sample size frozen | **PENDING** | Generate calibration-only variance/power simulation, freeze N before confirmation. |
| Gate-4: full data/code/config hashes | **PARTIAL** | Hash production generator, candidate panels, task IDs, seeds, selector code, and cost config. |
| Gate-5: final analysis code frozen | **PENDING** | Freeze paired estimator, multiplicity, missingness, and report code before outcome unlock. |
| Gate-6: confirmatory store sealed | **PENDING** | Implement access control and audit log; confirm no outcome opened before decisions/RDR lock. |
| Outcome/task runner validity | **PENDING** | Integrate actual solver/task outputs; verify paired no-skill counterfactuals and fixed denominators. |
| Cost calibration and sensitivity | **PENDING** | Calibrate independently and test candidate class stability on calibration data only. |
| Candidate distribution validity | **PENDING** | Demonstrate required quotas from predeclared generator recipes without outcome-based curation. |

## 10. Final Phase 1B audit decision

**Pass:** v1.0 failure audit is preserved; 26/26 implementation contracts pass on synthetic fixtures; opaque IDs/order fix class-label leakage; pressure divergence is measurable and passes; outcome response can produce losses, ties, and wins.

**Not passed:** the full scientific benchmark is not implemented or ready to collect confirmatory outcomes. The existing tests do not validate real task ground truth, empirical cost conversion, independent sample size, production leakage controls, or out-of-sample replication.

Therefore the appropriate state is:

> **Phase 1B contract implementation: PASS. Full RQ2 benchmark readiness: BLOCKED pending actual task/data implementation and Gates 3–6. No Phase 4 SCT/SCV confirmation is authorized.**

This audit is the Phase 1B handoff. Phase 1C work is paused until Phase 1B is accepted and the remaining Phase 1B scope is explicitly decided.