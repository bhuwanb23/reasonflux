# BL1 — Boundary Learning Program Charter v1

**Status:** planning package only; not preregistered, implemented, or executed.  
**Owner authorization:** create this planning package only. No implementation, context generation, experiment, ARC work, or execution is authorized.

## Objective

Evaluate one narrow question:

> **Does counterexample evidence improve held-out applicability precision while preserving useful coverage?**

BL1 is a distinct research question following closure of Claim N v1. It is not an N-v2, an S3 rerun, or a reinterpretation of the S3 result.

## Motivation and evidence ceiling

- Claim N v1 failed on the frozen S3 predictive estimand: I0 and R4 each scored 105/105, `Delta_N=0`.
- The only current boundary-learning signal is the S2 deterministic toy-fixture observation: false activations fell 2/4→0/4 while applicable-context coverage remained 2/2.
- That observation is not decision-grade evidence of general boundary learning. BL1 is untested.
- No novelty or publication claim is cleared by this charter. A focused prior-art assessment is a prerequisite to any eventual novelty claim.

## Scope

BL1 is limited to the causal/mechanistic effect of counterexample feedback on an applicability boundary. A future test should compare the same candidate skill, initial boundary, source experience, observable schema, held-out contexts, predictor interface, and resource opportunities, varying only whether counterexample labels can update the boundary.

Primary outcomes concern held-out applicability precision and useful coverage, with false activations, missed valid applications, abstentions, and denominators reported explicitly.

## Non-goals

BL1 does not test or claim:

- invariant representation value beyond replay (Claim N v1 is closed);
- capability growth, CGM, transfer scores, intelligence growth, or SCV;
- reduced harmful transfer (Claim C), action-efficiency gains (Claim D), or end-to-end superiority (Claim E);
- ARC-AGI-3 transfer or a winning paper outcome;
- broad skill discovery or general agent improvement.

## Research integrity constraints

- Preserve the S3 negative result and all frozen S3 artifacts.
- Do not reuse S3 held-out contexts/outcomes as BL1 evaluation data.
- Do not tune a boundary, threshold, metric, or claim after seeing held-out outcomes.
- Do not treat the S2 toy fixture as confirmatory evidence.
- Separate boundary precision from useful coverage; a boundary that suppresses nearly all use is not a success.
- No implementation, context materialization, model fitting, or evaluation without a separately approved BL1 protocol and explicit authorization.

## Open decisions (unset)

The following must be resolved before a confirmatory protocol can be frozen: task/world domain; candidate skill and initial boundary; operational definition of a counterexample; control/treatment exposure; held-out applicability labels and custody; useful-coverage criterion; precision effect threshold; aggregation/uncertainty method; context counts; resource vector; and novelty/prior-art review. This charter does not guess these values.

## Current decision state

BL1 is a **possible future program**, not an active experiment. Only this planning package is authorized. Further work requires a separate owner decision after review of the open decisions and novelty ceiling.
