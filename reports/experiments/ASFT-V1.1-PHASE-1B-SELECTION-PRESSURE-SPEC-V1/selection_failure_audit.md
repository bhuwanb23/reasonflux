# 1B.1 — Selection Failure Audit

**Purpose.** Explain the v1.0 SCT/SCV nulls without either excusing a failed primary comparison or overgeneralizing it into a theory-wide falsification. Sources: Phase 13C, Phase 13F, Phase 14C, and Phase 14F. These records were audited, not rerun.

## Findings by question

### Why were all 13C candidates selected?

The frozen primary decision was `SCV10 > 0`. On the 22 calibration candidates, all 22 had SCV10 above zero; the frozen cutoff therefore selected all 44/44 confirmation candidates. The policy operated on a candidate pool without a non-positive SCV tail and had no capacity constraint. The confirmation result is a real failure of the prespecified superiority gate, but it cannot identify whether SCV would reject bad candidates in a pool containing them. The q25/q50/q75 analyses are sensitivity results, not a license to substitute a post-hoc cutoff for the frozen primary rule.

### Why did SCV not matter?

In 13C, SCT, ALWAYS_CREATE, and RANDOM_CREATE all produced mean net value .345. The policy did not reject any candidate, so it was operationally the same as always-create. In 13F, the candidate-selection record shows four qualified candidates per seed; ASFT, A2_NO_SCV, and A2_1_RANDOM_SCV constructed four. Thus the random-SCV arm sampled all four available candidates and could not create a different selected set. Their task utility, SU, TS, CGR, and IG were identical in the saved result matrix. This is evidence of no incremental SCV effect in the tested pools, not proof SCV is irrelevant in a pressure-rich pool.

### Why did random creation tie SCT?

Two distinct degeneracies must not be conflated:

1. **13C RANDOM_CREATE:** calibration-frozen Bernoulli creation probability was 1.0; the random policy was deterministic always-create, so its tie is not evidence that random choice works as well as SCV.
2. **13F A2_1_RANDOM_SCV:** matched random selection was requested to choose `k = ASFT births`; with the whole four-candidate pool selected, `k=4` and the random sample necessarily contained all four.

13F B3_RANDOM_SKILL_CREATION is a separate 75%-of-pool baseline. It created three rather than four skills on the four-candidate pool yet tied on several aggregate task/growth endpoints. That suggests outcome insensitivity, candidate redundancy, or low leverage in this test; it does **not** mean the selected candidates were identical. The phases use different random policies and must not be pooled.

### What pressure was missing?

- No fixed capacity below candidate count.
- No required mixture of positive-, neutral-, and negative-value candidates; the frozen SCV operating point had only positive scores.
- No enforced disagreement diagnostic between SCV and frequency/reuse/random policies.
- Random policies could collapse to always-create or sample the entire pool.
- 13C had 44 rows but only six signatures and births in two families; rows were nested in ten seed clusters.
- Candidate-level predictor association was mistaken easily for policy value: SCV10 had Spearman rho .700 against shadow value, below frequency .748 and p_reuse .884 numerically; no direct correlation-superiority test was reported.
- 13F’s four-candidate selection pool was too small to create real choice. Its equal task utility for no-SCV/random-SCV arms is a local null, not evidence from a rich choice set.

## Cross-phase interpretation to preserve

| Record | What it shows | What it does not show |
|---|---|---|
| 13C | SCT built/reused synthetic skills; exact policy tie with always/random; memory-only was stronger on this repetitive stream and net-value definition. | That SCT cannot select; that memory is universally superior; or that step-proxy savings are compute savings. |
| 13F | ASFT/no-SCV/random-SCV selected all four; those arms tied on named outcomes. A distinct 75% random arm also tied on aggregate outcomes. | That every selector pair chose the same set; B3 is not the same policy as A2_1; no universal null. |
| 14C | Identifies all-positive pool and p=1 random policy as strongest supported explanation; separates SCV association from policy advantage. | A causal proof that pressure alone explains every null. |
| 14F | Concludes SCV/SCT incremental value is not supported in tested pools; distinguishes frequency, memory, compression proxy, and endpoint-specific baselines. | That a redesigned, decision-divergent benchmark should be expected to favor SCV. |

## Design consequences adopted in Phase 1B

1. Use a shared pool with a fixed capacity of 8 slots for 20 candidates.
2. Generate four candidates in each of five frozen challenge types; latent type is not exposed to selectors.
3. Define future value from held-out outcomes and measured costs, not SCV or the SCV inputs.
4. Freeze the Phase 13C SCV10 formula for the primary SCV selector; do not tune its threshold on confirmatory outcomes.
5. Enforce a pre-outcome selection-divergence gate and log the chosen set for every selector.
6. Give random creation a fixed number of slots drawn uniformly without replacement; never set its probability from the calibration positive rate.
7. Treat always-create as capacity-limited and never-create as an intentional zero-rate sentinel; neither is used to satisfy the active-selector nondegeneracy check.
8. Keep task outcome labels sealed until selector decisions and pressure checks are locked.

**Audit conclusion:** v1.0 did not test whether SCV discriminates among candidate values under genuine choice. It did test fixed policies on the pools supplied, and the primary superiority claims failed or remained unestablished there. The redesigned benchmark below is intended to make that distinction testable.