# Skill Event Log Schema

Store one JSON object per event in `skill_events.jsonl`. Keep event records append-only. Never store secrets, private user data, or prohibited hidden labels.

## Required event keys

```json
{
  "schema_version": "0.1",
  "run_id": "REQUIRED_BEFORE_RUN",
  "track": "agi2-or-agi3",
  "hypothesis": "H1_IDT-or-H2_SCT-or-H3_CGM",
  "variant_id": "REQUIRED_BEFORE_RUN",
  "seed": 0,
  "task_or_game_id": "REQUIRED_BEFORE_RUN",
  "episode_id": null,
  "step_or_task_index": 0,
  "event_type": "candidate_created | candidate_rejected | skill_promoted | skill_invoked | invocation_succeeded | invocation_failed | skill_retired",
  "timestamp_utc": "ISO-8601",
  "skill_id": "stable-versioned-id-or-null",
  "candidate_id": "stable-id-or-null",
  "source_experience_ids": [],
  "preconditions": null,
  "candidate_representation_hash": null,
  "evidence_available_at_decision": {},
  "estimated_benefit_at_decision": null,
  "estimated_cost_at_decision": null,
  "trigger_decision": null,
  "decision_reason_code": null,
  "actual_outcome": null,
  "actual_cost": null,
  "budget_remaining": null,
  "failure_mode": null
}
```

## Semantics

- `estimated_*_at_decision` must contain only information available before the target outcome; this permits checking hindsight leakage.
- `actual_outcome` is filled after evaluation, preferably by evaluator output; do not feed it back to the same decision.
- `candidate_representation_hash` identifies the executable code/macro without requiring large code duplication in every row. Archive the referenced immutable skill artifact separately.
- Use null only when genuinely not applicable; do not silently omit failed/rejected candidates.
- Each invocation must link to the skill version and task/game context. A changed skill gets a new version/ID.
