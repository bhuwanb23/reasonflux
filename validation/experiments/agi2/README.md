# ARC-AGI-2 Validation Plan

**Status:** Design draft; no runs/results recorded. This plan concerns static grid input/output tasks. Check the current ARC-AGI-2 rules, exact scoring schema, compute/runtime limits, notebook requirements, and artifact licensing before each release.

## Research question

Can invariants/program structures learned from source-task experience improve held-out ARC-2 solving accuracy or efficiency under the same fixed solver budget—and does SCT add benefit beyond simply making a library available?

## Required system interface

- Input: demonstrations for a task and test input(s), through the official competition contract.
- Candidate generation: exact solver/model/DSL version, search/ranking configuration.
- ASFT trace: task-local candidate programs/actions and their evidence; never record a test label the solver is not allowed to see.
- Skill record: executable transform/program plus preconditions, evidence count, source IDs, version, expected cost/benefit, and failure mode.
- Output: exact competition schema and at most the allowed attempts. Use the official evaluator.

## Minimum evaluation variants

`B0_NO_LEARNED_SKILLS`, `B1_STATIC_LIBRARY`, `V1_IDT_ONLY`, `V2_IDT_SCT`; add `V3_CGM_LOG_ONLY` for fixed probe checkpoints. All variants use identical models, test examples, seeds, and allowed budgets. Clearly distinguish public training tasks used to form a library from held-out tasks used only for evaluation.

## Split requirements

Create source/validation/held-out task ID lists and hashes. Prefer splits by transformation family/composition if labels or defensible family annotations exist. Record how labels were assigned. Never tune on the Kaggle hidden-test set or leaderboard result.

## Primary metrics to freeze

- Competition-native task score with evaluator version/hash.
- One preselected efficiency metric (wall time, GPU seconds, tokens, search nodes) under the same cap.
- Transfer delta: paired held-out change after source experience relative to a matched no-skill control.
- Candidate/skill quality metrics only if independently labeled; state annotation method and uncertainty.

Exact aggregation, `delta_min`, guardrail, task IDs, seeds, and confidence interval are `REQUIRED_BEFORE_RUN` in `HYPOTHESES.md` and `PROTOCOL.md`.

## ARC-2-specific risks

- A DSL can leak the target concept through operator names or trace labels; disclose hand-engineered primitives and test new compositions.
- Memorized task families or training answers can inflate transfer; split by family/composition and publish the split hash.
- Test-time adaptation using each task's demonstrations is not evidence of cross-task skill acquisition by itself.
- Two candidate outputs/attempt selection must match the current rule exactly.
- Ensure offline execution, exact submission schema, model provenance/license, and resource limits. Keep all model inference and solution code inside the permitted Kaggle environment.

## Before a run

Complete the experiment matrix, data/environment manifests, and protocol freeze. Run official-format unit tests and a no-ASFT baseline first. Label smoke checks separately from hypothesis results.
