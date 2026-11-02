# 1B.3 — Candidate Value Definition

## Unit and primary horizon

The value unit is a **task-equivalent utility unit (TEU)**: one exact additional task solution over the matched no-skill solver is 1 TEU; an exact solution lost relative to no-skill is −1 TEU. Partial credit is not used in the primary endpoint. If a later task battery requires graded reward, its mapping must be externally specified and frozen before this benchmark; it cannot be tuned from SCV or confirmatory results.

The common candidate horizon is ten eligible opportunities. Reuse, future task utility, and transfer are not three additive rewards for the same solve. They are decompositions of one held-out outcome stream: every task contributes once to utility, with source-family reuse, transfer, and context-shift subsets reported separately.

## Candidate-level latent and realized value

For candidate `i`, let `R_it(1)` be exact task reward on its held-out task when the skill is available and `R_it(0)` be the paired no-skill solver reward on the same task. Let `C_i^create` and `C_it^maint` be independently instrumented creation and maintenance resources, translated into TEU using a fixed conversion rate `lambda` estimated on the calibration resource/task set before development and confirmation.

`FNV_i = sum(t=1..10) [R_it(1) - R_it(0)] - lambda_create * C_i^create - lambda_maint * sum(t=1..10) C_it^maint`

- **Creation cost:** incremental resources to construct, validate, and install the candidate, recorded once.
- **Maintenance cost:** fixed-horizon storage, compatibility checks, lifecycle bookkeeping, and other preregistered per-opportunity maintenance resources.
- **Reuse value:** additional correct task solves in the source-family opportunities; already included in the utility sum.
- **Transfer value:** additional correct solves on the prespecified transfer slots; already included in the utility sum and reported as a subset.
- **Future utility:** all ten paired task outcomes; task outcomes are separate from any predictor score.

Resource units and the conversion rate are calibration-only. If resource instrumentation is missing or the conversion cannot be locked without outcome-dependent choices, report gross task utility and costs separately and mark cost-adjusted FNV **unavailable**; do not invent a favorable conversion after confirmation.

## Balanced latent types

The generator has known latent expected net value `theta_i` under the frozen task distribution and resource conversion. Type A/B/C/D/E is assigned from that generator mechanism, not from the SCV score. Thresholds: positive `theta >= +0.10 TEU`, neutral `-0.10 < theta < +0.10`, negative `theta <= -0.10`; Type D adds the early-positive/full-horizon-negative condition; Type E is rare opportunity probability `<=0.10` and `theta>=+0.50 TEU`. Realized FNV may differ from `theta`; both are reported, and type is not relabeled based on a noisy outcome.

## SCV selector — frozen legacy equation

To test the existing SCV decision signal rather than a newly optimized replacement, the primary selector uses the Phase 13C mapping:

`SCV10_i = 10 * p_reuse_i * AG_i * TS_i - CC_i - 10 * MC_i`

`p_reuse = clip01(reuse if nonzero else expected_reuse)`; `AG=clip01(abstraction_gain)`; `TS=clip01(transfer_score if nonzero else expected_transfer)`; `CC=max(0, creation_cost estimate)`; `MC=base_maintenance+0.01` under the frozen default; `clip01(x)=min(1,max(0,x))`. All mappings, imputations, raw values, and source fields are versioned. No value label or held-out outcome enters this score. This definition is frozen for the Phase 1B/Phase 4 RQ2 test; a changed SCV requires a new protocol and independent confirmation.

The score is a **selection predictor**, not the value definition. Observed cost in FNV is instrumented separately, even when the score uses an estimated cost field.

## Portfolio value (primary endpoint)

For batch `b` and selector `s`, install the selector's chosen set `S_bs` into an isolated evaluation clone. Run the same ten opportunities per candidate lane and same no-skill paired baseline for every selector. With capacity `K=8`:

`Y_bs = [sum_i in S_bs FNV_i] / K`

This is mean selected-set net future value per available creation slot. The matched no-create policy has `Y=0`; it incurs no creation/maintenance cost. Because the protocol gives each candidate a disjoint task lane and equal horizon, one selected candidate cannot consume another's opportunity denominator. Portfolio output, task success, costs, and failed/missing candidate lanes are retained separately.

This experiment isolates candidate selection. It does not claim cost calibration is real-world compute or economic cost; any such claim needs separate instrumented evidence.