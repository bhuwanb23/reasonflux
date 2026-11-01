# ARC-AGI-3 Validation Plan

**Status:** Design draft; no runs/results recorded. ARC-3 is an interactive perception/action environment; follow current official agent API, episode/game boundaries, scoring, runtime, and action constraints.

## Research question

Does converting verified interaction experience into reusable skills improve later held-out game performance, action efficiency, or both, compared with the same agent without those learned skills—and does SCT avoid useless/negative-transfer skills better than always-store?

## Required system interface

For each step log: episode/game ID, observation reference/hash, available action set, selected action, agent/model response, environment transition/reward/score, step cost, and whether a skill was invoked. Redact sensitive or disallowed data; store no credentials.

A skill must have explicit preconditions, action sequence/policy, termination condition, expected state change, evidence count, game/source IDs, version, invocation cost, failure/rollback behavior, and success criterion. Do not promote a one-off action sequence as a general skill without a validation rule.

## Minimum evaluation variants

`B0_NO_LEARNED_SKILLS`, `B1_STATIC_OR_SIMPLE_MACROS`, `V1_IDT_ONLY`, `V2_IDT_SCT`; add `V3_CGM_LOG_ONLY` with the agent's decisions unchanged. Keep model checkpoint, prompts, tools, observation formats, action budget, and time budget fixed.

## Split and episode design

Define whether learning occurs within an episode, across episodes, or across games, and which information persists. Create source and held-out game/level lists by game mechanics where possible; hash them. Record reset policy and any reliance on public-game feedback. Do not use hidden holdout outcomes for trigger tuning.

## Metrics to freeze

- Official ARC-3 score/aggregate using the official evaluator version.
- One preselected efficiency metric (actions to progress, model tokens, wall time, or compute) with fixed budget.
- Transfer delta on held-out games after source experience vs matched control.
- Skill reuse, success/failure, negative-transfer events, and memory/latency cost.

Define game aggregation, seeds, `delta_min`, safety/negative-transfer guardrail, and CI method before runs.

## ARC-3-specific risks

- Visual ambiguity, invalid actions, game reset behavior, stochastic transitions, and long episodes can dominate score.
- A hand-crafted game-specific macro may solve one level but not be a transferable skill; report per-game and cross-game results.
- One agent's exploration schedule can change experience quality; hold it fixed across variants or explicitly test it as a separate factor.
- A model change, context/memory policy, tool change, or GPU/runtime difference confounds an ASFT ablation.
- Verify offline inference, agent API contract, model/data licensing, and compute/runtime rules.

## Before a run

Smoke-test the official interface and baseline agent; record game seeds, complete transition logs, and ensure each variant can be restarted from the same allowed state. Only call results confirmatory after the split, budget, and analysis are frozen.
