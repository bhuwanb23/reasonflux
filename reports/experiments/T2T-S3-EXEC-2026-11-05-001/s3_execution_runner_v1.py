from __future__ import annotations

"""One-shot S3 execution runner for the owner-authorized frozen package.

Prediction events are committed to disk before any held-out world access.
This file does not alter arms, scoring, manifests, or transformation recipes.
"""

import hashlib
import json
import os
import sys
import traceback
from dataclasses import asdict
from datetime import datetime
from fractions import Fraction
from pathlib import Path
from zoneinfo import ZoneInfo

from jsonschema import Draft202012Validator

from t2t_s3.arms import (
    I0Invariant, R0RawReplay, R1ParameterizedReplay, R2CompressedReplay,
    R3GrammarReplay, R4ReplayMax, Prediction,
)
from t2t_s3.eventlog import prediction_event, score_event
from t2t_s3.scoring import (
    EligibleContext, PredictionRecord, aggregate_all_context_scores,
)
from t2t_s3.world import (
    Effect, ObjectKind, RelationalUnlockWorld, UnlockAction, UnlockObject,
    UnlockState, UnlockTrace,
)

ROOT = Path(__file__).resolve().parents[3]
S3 = ROOT / "docs/05_trace_to_transfer/s3"
RUN_DIR = Path(__file__).resolve().parent
RUN_ID = "T2T-S3-EXEC-2026-11-05-001"
PACKAGE_VERSION = "T2T-S3-RA-v0.2.0"
ARM_IDS = ("R0", "R1", "R2", "R3", "R4", "I0")
OUTPUT_NAMES = (
    "prediction_events.jsonl", "prediction_commit.json", "score_events.jsonl",
    "all_context_report.json", "per_cell_report.json", "delta_n_report.json",
    "claim_n_decision.md", "s3_execution_record.json",
)

phase = "PREFLIGHT"
source_labels_generated = False
source_labels_generated_count = 0
heldout_outcomes_attached = False
predictions_committed = False


def now():
    return datetime.now(ZoneInfo("Asia/Kolkata")).isoformat()


execution_started_at = now()


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compact_bytes(obj) -> bytes:
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def write_json(path: Path, obj):
    data = compact_bytes(obj)
    path.write_bytes(data)
    return hashlib.sha256(data).hexdigest()


def load_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def state_from(record):
    raw = record["state"]
    objects = tuple(
        UnlockObject(
            object_id=o["object_id"], kind=ObjectKind(o["kind"]), x=o["x"], y=o["y"],
            color=o["color"], shape=o["shape"], opens_target_id=o["opens_target_id"],
            closed=o["closed"],
        ) for o in raw["objects"]
    )
    return UnlockState(raw["context_id"], objects, raw["agent_x"], raw["agent_y"], raw["path_clear"])


def action_from(record):
    return UnlockAction(record["action"]["key_id"], record["action"]["target_id"])


def effect_payload(effect: Effect):
    return {"target_opened": effect.target_opened, "agent_advanced": effect.agent_advanced}


def summary_payload(summary):
    return asdict(summary)


def validate_no_outcome_fields(value):
    forbidden = {"observed_effect", "expected_effect", "effect", "outcome", "prediction", "accuracy", "score", "label"}
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in forbidden:
                raise ValueError(f"forbidden outcome-like input field: {key}")
            validate_no_outcome_fields(child)
    elif isinstance(value, list):
        for child in value:
            validate_no_outcome_fields(child)


def record_n_blocked(error: BaseException):
    """Persist a single failed attempt; never retry or continue to outcome access."""
    message = f"N-BLOCKED: {type(error).__name__}: {error}"
    for name in ("all_context_report.json", "per_cell_report.json"):
        path = RUN_DIR / name
        write_json(path, {"run_id": RUN_ID, "status": "N-BLOCKED", "reason": message, "reports": []})
    delta_path = RUN_DIR / "delta_n_report.json"
    write_json(delta_path, {"run_id": RUN_ID, "status": "N-BLOCKED", "delta_n": None, "reason": message})
    decision_path = RUN_DIR / "claim_n_decision.md"
    decision_path.write_text(
        f"# Claim N Decision\n\n**N-BLOCKED**\n\nReason: {message}\n\nNo rerun is permitted under this authorization.\n",
        encoding="utf-8",
    )
    rec = {
        "schema_version": "t2t-s3-execution-record-v1", "run_id": RUN_ID,
        "package_version": PACKAGE_VERSION, "run_status": "N-BLOCKED",
        "phase_at_stop": phase, "failure": message,
        "source_labels_generated": source_labels_generated,
        "source_labels_generated_count": source_labels_generated_count,
        "heldout_outcomes_attached": heldout_outcomes_attached,
        "predictions_committed": predictions_committed,
        "no_retry": True, "s3_execution_count": 1,
        "runner_sha256": file_sha(Path(__file__)),
        "recorded_at": now(),
    }
    write_json(RUN_DIR / "s3_execution_record.json", rec)


try:
    if not RUN_DIR.is_dir():
        raise RuntimeError("authorized execution directory missing")
    existing = [name for name in OUTPUT_NAMES if (RUN_DIR / name).exists()]
    if existing:
        raise RuntimeError(f"execution outputs already exist; refusing a second attempt: {existing}")

    # Integrity preflight; no world transition, fit, prediction, or score here.
    freeze = load_json(S3 / "freeze_manifest.json")
    for item in freeze["frozen_files"]:
        if file_sha(ROOT / item["path"]) != item["sha256"]:
            raise RuntimeError(f"frozen package hash mismatch: {item['path']}")
    manifests_hashes = load_json(S3 / "manifest_hashes.json")
    for name, expected in manifests_hashes["generated_artifacts"].items():
        if file_sha(S3 / name) != expected:
            raise RuntimeError(f"manifest hash mismatch: {name}")
    for name, expected in manifests_hashes["frozen_inputs"].items():
        if file_sha(S3 / name) != expected:
            raise RuntimeError(f"manifest input hash mismatch: {name}")

    source = load_json(S3 / "source_manifest.json")
    held = load_json(S3 / "heldout_manifest.json")
    diagnostic = load_json(S3 / "diagnostic_manifest.json")
    role_map = load_json(S3 / "context_role_map.json")
    for schema_name, doc in (
        ("source_manifest_schema.json", source),
        ("heldout_manifest_schema.json", held),
        ("context_role_map_schema.json", role_map),
    ):
        schema = load_json(S3 / schema_name)
        Draft202012Validator.check_schema(schema)
        Draft202012Validator(schema).validate(doc)
    for doc in (source, held, diagnostic):
        validate_no_outcome_fields(doc)

    if len(source["contexts"]) != 7 or len(held["contexts"]) != 105 or len(diagnostic["contexts"]) != 10:
        raise RuntimeError("frozen context counts do not match 7/105/10")
    expected_cells = [x["cell_id"] for x in held["cell_declarations"]]
    if len(expected_cells) != 35 or len(set(expected_cells)) != 35:
        raise RuntimeError("primary cell declaration set is not exactly 35 unique cells")
    if any(x["eligibility_status"] != "ELIGIBLE" or x["planned_count"] != 3 for x in held["cell_declarations"]):
        raise RuntimeError("a held-out cell is ineligible or count differs from frozen policy")
    context_ids = [c["context_id"] for doc in (source, held, diagnostic) for c in doc["contexts"]]
    if len(context_ids) != 122 or len(set(context_ids)) != 122:
        raise RuntimeError("context IDs duplicate or context count differs from 122")
    if {x["context_id"] for x in role_map["assignments"]} != set(context_ids) or len(role_map["assignments"]) != 122:
        raise RuntimeError("role map is incomplete, duplicated, or contains an unknown ID")
    if {x["context_id"] for x in source["contexts"]}.intersection(
        {x["context_id"] for x in held["contexts"] + diagnostic["contexts"]}
    ):
        raise RuntimeError("source/held-out role overlap")

    source_records = [(c, state_from(c), action_from(c)) for c in source["contexts"]]
    held_records = [(c, state_from(c), action_from(c)) for c in held["contexts"]]
    diag_records = [(c, state_from(c), action_from(c)) for c in diagnostic["contexts"]]
    if any(not state.is_complete() or state.has_dangling_relations() for _, state, _ in source_records + held_records):
        raise RuntimeError("incomplete or dangling state in source/primary held-out manifest")
    if any(state.is_complete() for _, state, _ in diag_records):
        raise RuntimeError("diagnostic context unexpectedly became complete")

    phase = "SOURCE_LABELS_AND_FIT"
    # Source labels are training evidence, generated once under the explicit run authorization.
    source_traces = []
    for context, state, action in source_records:
        effect = RelationalUnlockWorld.step(state, action)
        if effect is None:
            raise RuntimeError(f"source context has unknown effect: {context['context_id']}")
        source_traces.append(UnlockTrace(context["trace_id"], state, action, effect, "SYNTHETIC_SOURCE"))
        source_labels_generated_count += 1
    source_labels_generated = True

    arms = {
        "R0": R0RawReplay.fit(source_traces),
        "R1": R1ParameterizedReplay.fit(source_traces),
        "R2": R2CompressedReplay.fit(source_traces),
        "R3": R3GrammarReplay.fit(source_traces),
        "R4": R4ReplayMax.fit(source_traces),
        "I0": I0Invariant.fit(source_traces),
    }
    if tuple(arms) != ARM_IDS:
        raise RuntimeError("arm order/identity mismatch")

    phase = "HELDOUT_PREDICTIONS"
    # Predictor receives only state/action. Cell/role/semantic/context metadata stays in evaluator.
    prediction_by_arm_context = {}
    prediction_events = []
    eval_records = [(c,s,a,"PRIMARY") for c,s,a in held_records] + [(c,s,a,"DIAGNOSTIC_ONLY") for c,s,a in diag_records]
    for arm_id, arm in arms.items():
        for context, state, action, scope in eval_records:
            prediction = arm.predict(state, action)
            key = (arm_id, context["context_id"])
            if key in prediction_by_arm_context:
                raise RuntimeError(f"duplicate prediction: {key}")
            prediction_by_arm_context[key] = prediction
            cell_id = context["cell_id"]
            ev = prediction_event(
                event_id=f"PRED-{arm_id}-{context['context_id']}", package_version=PACKAGE_VERSION,
                arm_id=arm_id, cell_id=cell_id, state=state, action=action, prediction=prediction,
                resource_cost={"prediction_opportunities": 1},
            )
            prediction_events.append(ev.to_json_line())
    if len(prediction_events) != len(ARM_IDS) * (len(held_records) + len(diag_records)):
        raise RuntimeError("prediction event count mismatch")
    pred_path = RUN_DIR / "prediction_events.jsonl"
    tmp_path = RUN_DIR / "prediction_events.jsonl.tmp"
    data = ("\n".join(prediction_events) + "\n").encode("utf-8")
    with tmp_path.open("wb") as f:
        f.write(data); f.flush(); os.fsync(f.fileno())
    os.replace(tmp_path, pred_path)
    pred_hash = file_sha(pred_path)
    commit = {
        "schema_version":"t2t-s3-prediction-commit-v1", "run_id":RUN_ID,
        "prediction_event_count":len(prediction_events), "prediction_events_sha256":pred_hash,
        "heldout_context_count":len(held_records), "diagnostic_context_count":len(diag_records),
        "recorded_at":now(), "outcomes_attached":False,
    }
    write_json(RUN_DIR / "prediction_commit.json", commit)
    predictions_committed = True

    phase = "HELDOUT_OUTCOME_ATTACHMENT_AND_SCORING"
    # Only now, after the complete prediction artifact is committed, obtain each primary outcome.
    eligible = []
    score_events = []
    for context, state, action in held_records:
        observed = RelationalUnlockWorld.step(state, action)
        if observed is None:
            raise RuntimeError(f"primary context has unknown outcome: {context['context_id']}")
        eligible.append(EligibleContext(context["context_id"], context["cell_id"], observed))
        for arm_id in ARM_IDS:
            prediction = prediction_by_arm_context[(arm_id, context["context_id"])]
            ev = score_event(
                event_id=f"SCORE-{arm_id}-{context['context_id']}", package_version=PACKAGE_VERSION,
                arm_id=arm_id, cell_id=context["cell_id"], state=state, action=action,
                prediction=prediction, observed_effect=observed,
            )
            score_events.append(ev.to_json_line())
        heldout_outcomes_attached = True
    # Diagnostics have no exact effect. Verify the simulator's unknown contract only after predictions;
    # record no label and do not score them.
    diagnostic_unknown_count = 0
    for context, state, action in diag_records:
        if RelationalUnlockWorld.step(state, action) is not None:
            raise RuntimeError(f"diagnostic context unexpectedly received an exact effect: {context['context_id']}")
        diagnostic_unknown_count += 1

    score_path = RUN_DIR / "score_events.jsonl"
    with score_path.open("wb") as f:
        f.write(("\n".join(score_events) + "\n").encode("utf-8"))
        f.flush()
        os.fsync(f.fileno())

    primary_predictions = [
        PredictionRecord(context_id=context["context_id"], arm_id=arm_id,
                         prediction=prediction_by_arm_context[(arm_id, context["context_id"])])
        for arm_id in ARM_IDS for context, _, _ in held_records
    ]
    score_report = aggregate_all_context_scores(
        eligible_contexts=eligible,
        predictions=primary_predictions,
        arm_ids=ARM_IDS,
        expected_cell_ids=expected_cells,
    )
    all_report = {
        "schema_version":"t2t-s3-all-context-report-v1", "run_id":RUN_ID,
        "primary_context_count":len(eligible), "cell_count":len(expected_cells),
        "arms":{arm:summary_payload(score_report.all_context[arm]) for arm in ARM_IDS},
        "diagnostics":{
            "context_count":len(diag_records), "unknown_world_returns":diagnostic_unknown_count,
            "primary_denominator_includes_diagnostics":False,
            "prediction_status_counts":{
                arm:{status:sum(1 for c,_,_ in diag_records if prediction_by_arm_context[(arm,c['context_id'])].status==status)
                     for status in sorted({prediction_by_arm_context[(arm,c['context_id'])].status for c,_,_ in diag_records})}
                for arm in ARM_IDS
            },
        },
        "scoring_rule":"all primary contexts remain in denominator; correct=1, wrong/abstain/invalid/missing=0",
    }
    per_cell = []
    for cell in expected_cells:
        per_cell.append({
            "cell_id":cell,
            "declared_count":next(d["planned_count"] for d in held["cell_declarations"] if d["cell_id"]==cell),
            "eligibility_status":"ELIGIBLE",
            "arms":{arm:summary_payload(score_report.by_cell[(arm,cell)]) for arm in ARM_IDS},
        })
    per_report = {"schema_version":"t2t-s3-per-cell-report-v1","run_id":RUN_ID,"cells":per_cell}
    all_hash=write_json(RUN_DIR/"all_context_report.json",all_report)
    per_hash=write_json(RUN_DIR/"per_cell_report.json",per_report)

    i0 = score_report.all_context["I0"]
    r4 = score_report.all_context["R4"]
    delta = Fraction(i0.correct, i0.denominator) - Fraction(r4.correct, r4.denominator)
    if delta > 0:
        decision = "N-PASS"
    else:
        decision = "N-FAIL"
    delta_report = {
        "schema_version":"t2t-s3-delta-n-report-v1", "run_id":RUN_ID,
        "formula":"Accuracy(I0) - Accuracy(R4)",
        "I0":{"correct":i0.correct,"denominator":i0.denominator,"accuracy":i0.accuracy},
        "R4":{"correct":r4.correct,"denominator":r4.denominator,"accuracy":r4.accuracy},
        "delta_n_exact":{"numerator":delta.numerator,"denominator":delta.denominator},
        "delta_n_decimal":float(delta), "classification":decision,
        "decision_rule":"Delta_N > 0 => N-PASS; Delta_N <= 0 => N-FAIL; integrity/protocol failure => N-BLOCKED",
        "scope":"frozen finite synthetic suite only",
    }
    delta_hash=write_json(RUN_DIR/"delta_n_report.json",delta_report)
    decision_text=(
        "# Claim N Decision\n\n"
        f"**Decision: {decision}**\n\n"
        f"- `Accuracy(I0)`: {i0.correct}/{i0.denominator} = {i0.accuracy:.12f}\n"
        f"- `Accuracy(R4)`: {r4.correct}/{r4.denominator} = {r4.accuracy:.12f}\n"
        f"- `Delta_N = Accuracy(I0) - Accuracy(R4)`: {delta.numerator}/{delta.denominator} = {float(delta):.12f}\n\n"
        "This decision applies only to the frozen finite synthetic suite and the preregistered scoring rule. "
        "It does not establish ARC transfer, population-level effects, or general intelligence.\n"
    )
    (RUN_DIR/"claim_n_decision.md").write_text(decision_text,encoding="utf-8")

    phase = "COMPLETE"
    run_record = {
        "schema_version":"t2t-s3-execution-record-v1", "run_id":RUN_ID,
        "run_status":"COMPLETED", "claim_n_classification":decision,
        "authorization":"one frozen S3 execution explicitly authorized by owner in this session",
        "authorization_scope":"one execution only; no regeneration, refit, or rerun",
        "s3_execution_count":1, "reruns":0,
        "started_at":execution_started_at, "completed_at":now(),
        "package_version":PACKAGE_VERSION,
        "freeze_manifest_sha256":file_sha(S3/"freeze_manifest.json"),
        "manifest_hashes_sha256":file_sha(S3/"manifest_hashes.json"),
        "manifests":{
            name:file_sha(S3/name) for name in ["source_manifest.json","heldout_manifest.json","diagnostic_manifest.json","context_role_map.json"]
        },
        "counts":{"source":len(source_records),"heldout_primary":len(held_records),"diagnostic_only":len(diag_records),"primary_cells":len(expected_cells)},
        "arms":list(ARM_IDS), "source_trace_ids":[x.trace_id for x in source_traces],
        "fit_inputs":"same seven source traces for every arm; source labels generated once from frozen world under this authorization",
        "prediction_events":{"path":"prediction_events.jsonl","sha256":pred_hash,"committed_before_heldout_outcome_access":True,"event_count":len(prediction_events)},
        "prediction_commit_sha256":file_sha(RUN_DIR/"prediction_commit.json"),
        "world_accesses":{"source_label_generation":len(source_records),"heldout_primary_after_prediction_commit":len(held_records),"diagnostic_unknown_checks_after_prediction_commit":diagnostic_unknown_count,"total":len(source_records)+len(held_records)+diagnostic_unknown_count},
        "source_labels_generated":True,"source_labels_generated_count":len(source_traces),"heldout_outcomes_attached_after_prediction_commit":True,
        "diagnostic_policy":"unknown-required-state, diagnostic-only; no effect labels; excluded from primary denominator",
        "resource_vector":"RESOURCE_VECTOR_V1; one prediction per arm/context; no retries/adaptive refit/post-holdout updates",
        "environment":{"python":sys.version.split()[0],"timezone":"Asia/Calcutta"},
        "runner_sha256":file_sha(Path(__file__)),
        "reports":{
            "all_context_report.json":all_hash,"per_cell_report.json":per_hash,
            "delta_n_report.json":delta_hash,"claim_n_decision.md":file_sha(RUN_DIR/"claim_n_decision.md"),
            "score_events.jsonl":file_sha(score_path),
        },
        "protocol_deviations":[], "reruns":0,
    }
    write_json(RUN_DIR/"s3_execution_record.json",run_record)

except Exception as exc:
    traceback.print_exc()
    record_n_blocked(exc)
    raise
