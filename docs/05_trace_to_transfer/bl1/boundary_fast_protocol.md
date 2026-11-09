# BL1-P0 — Smallest Feasible Fast Protocol (Design Only)

**Status:** protocol sketch for the P0 package; not preregistered, implemented, or authorized. No contexts have been generated. BL1 is terminated at P0 because the proposed contribution is already substantially covered; this document is not permission to execute or to create BL1-P1.

## Purpose and result scope

If an owner ever separately authorized a genuinely distinct boundary-learning question, this is the smallest bounded design considered capable of producing an interpretable **PASS / FAIL / BLOCKED** for the one-chain question:

> On a frozen suite, do counterexample labels improve applicability precision while preserving useful coverage and controlling false activation?

It can only answer that question for a narrow synthetic domain and the tested skill(s). It cannot establish transfer to ARC, real-world robotics, or general agents. It is not a year-long research program: one compact simulator/fixture, one frozen learner pair, one held-out suite, and one analysis. The present P0 terminates before any of those are built or run.

## Minimal prospective design

1. **Freeze one bounded domain and skill.** Select one deterministic, enumerable synthetic task with a fixed candidate skill/policy and an oracle or independently auditable applicability label. Define success/failure, contexts, allowed transforms, and domain strata before data creation. Do not use S3 material or outcomes.
2. **Freeze the two arms.** Start both arms from the identical initial boundary and source examples. Treatment receives a frozen set of permitted, training-only counterexample labels and a fixed boundary update rule. Control receives matched context exposure and compute but cannot use those labels to update its boundary. Keep model, schema, prompts/tools if any, seeds, and resource caps equal. The single intended difference is access to counterexample labels for boundary updates.
3. **Partition before fitting.** Create disjoint source/training, counterexample-update, and held-out evaluation partitions. A custodian seals held-out applicability labels. No held-out outcomes may influence updates, thresholds, exclusions, or protocol changes.
4. **Small fixed suite.** A minimal feasibility suite should contain both positive and negative examples in multiple predeclared boundary strata, with enough independent contexts to make endpoint denominators meaningful. A prospective owner/protocol must set exact counts and justify them with a precision/coverage uncertainty calculation before materialization; a tiny handful of examples like S2's 4 negatives is not adequate. Use identical held-out contexts for both arms and pair predictions by context.
5. **Commit, then score.** Log code/config/version hashes, exposure and update lineage, resource use, and each arm's permit/reject/abstain prediction. Commit predictions before label release. The custodian then reveals targets; compute the endpoints in `boundary_endpoint_spec.md`, including TP/FP/FN/TN, abstentions, precision, useful coverage, FAR, and predeclared uncertainty intervals.
6. **One analysis, no rescue.** Analyze the frozen suite once with the predeclared aggregation and decision rules. No post-hoc subset search, threshold tuning, seed replacement, reruns, or change of comparator. Any later exploratory work is not confirmatory evidence.

## Prospective decision rule

Before any held-out label is revealed, the authorized protocol must freeze numeric values and interval method. The logical outcomes are:

- **PASS:** treatment precision exceeds control by at least the predeclared meaningful margin, the uncertainty criterion for that contrast is met, and treatment useful coverage and FAR both satisfy their predeclared floors/ceilings; predictions, data partitions, and resource matching pass integrity audit.
- **FAIL:** valid execution and denominators, but the primary precision margin is not met, or either coverage/FAR guardrail fails. A precision gain achieved by suppressing useful activations is FAIL.
- **BLOCKED:** no valid decision is possible because an integrity or feasibility gate fails (e.g., labels leak, insufficient independent denominators, comparator/resources mismatch, undefined endpoints, corrupted artifacts, or task/skill labels cannot be independently established). BLOCKED is not a pass and must not be converted into a positive result by changing the suite or rerunning selectively.

The numeric margin, coverage floor, FAR ceiling, sample size, interval method, and exact stop rule are deliberately not fabricated here: they depend on the task's applicable-success oracle and a prospectively approved effect/uncertainty calculation. Until frozen, this protocol cannot yield an authorized PASS/FAIL result.

## Stop and integrity gates

Stop before execution if no independent applicability oracle exists, a nontrivial held-out suite cannot be generated and sealed, the arms cannot be matched except for counterexample-label access, or a distinct contribution cannot be stated in light of prior art. Stop and classify BLOCKED if held-out labels leak, a comparator or evaluation set changes after exposure, resource imbalance is material, required denominators are absent, or prediction/update lineage is incomplete. Do not reuse S3 contexts, labels, or outcomes; do not alter R4 or any S3 artifact; do not rerun S3.

## Feasibility conclusion for BL1-P0

A small controlled fixture is technically plausible, but it would be an application/replication of a well-established learning setup and would not cure the prior-art overlap identified in `boundary_prior_art_review.md`. A small fixture also cannot justify a broad generalization claim. The stated P0 stop rule is therefore triggered by prior art: terminate BL1 now, do not implement this protocol, and do not create BL1-P1.
