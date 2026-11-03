"""Common R1/R3 semantic-event projection for Phase 2I-A WP2.

The adapter preserves candidate action families in the operation strings that
TraceMiner consumes. Representation-specific provenance lives in a separate
sidecar and is never copied into the mining projection.
"""
from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Mapping
import re
import uuid

from core.trace import ReasoningStep, ReasoningTrace, TraceOutcome
from representations.r3 import Action

TRACE_SCHEMA_VERSION = "ASFT-2I-SEMANTIC-TRACE-V1"
MAX_TRACE_STEPS = 4
_ACTION_FAMILIES = frozenset({
    "identity", "flip_left_right", "flip_top_bottom", "rotate_90", "rotate_180", "rotate_270",
    "transpose", "anti_transpose", "translate", "recolor", "copy", "delete", "crop",
})


class Representation(StrEnum):
    R1 = "R1"
    R3 = "R3"


class EventStage(StrEnum):
    INPUT_VALIDATION = "input_validation"
    REPRESENTATION_CONSTRUCTION = "representation_construction"
    CANDIDATE_APPLICATION = "candidate_application"
    DEMONSTRATION_VERIFICATION = "demonstration_verification"


class TargetScope(StrEnum):
    GRID = "grid"
    OBJECT = "object"
    NONE = "none"


class EventOutcome(StrEnum):
    PASS = "pass"
    FAIL = "fail"


@dataclass(frozen=True, slots=True)
class SemanticEvent:
    schema_version: str
    stage: EventStage
    operation_family: str
    target_scope: TargetScope
    outcome: EventOutcome

    def __post_init__(self) -> None:
        if self.schema_version != TRACE_SCHEMA_VERSION:
            raise ValueError("unsupported semantic trace schema version")
        if not self.operation_family or self.operation_family.strip() != self.operation_family:
            raise ValueError("operation_family must be a nonempty canonical token")
        expected = {
            EventStage.INPUT_VALIDATION: "grid_input",
            EventStage.REPRESENTATION_CONSTRUCTION: "scene",
            EventStage.DEMONSTRATION_VERIFICATION: "exact_training_fit",
        }
        if self.stage in expected and self.operation_family != expected[self.stage]:
            raise ValueError("control event uses an unregistered operation family")
        if self.stage is EventStage.CANDIDATE_APPLICATION and self.operation_family not in _ACTION_FAMILIES:
            raise ValueError("candidate action family is not registered")
        if self.stage is not EventStage.CANDIDATE_APPLICATION and self.target_scope is not TargetScope.NONE:
            raise ValueError("control events must use target_scope=none")
        if self.outcome is not EventOutcome.PASS:
            raise ValueError("only complete successful candidate traces are emitted")

    @property
    def operation_token(self) -> str:
        """Token consumed by the current miner; no arm/scope/parameter labels."""
        if self.stage is EventStage.CANDIDATE_APPLICATION:
            return f"apply_{self.operation_family}"
        return {
            EventStage.INPUT_VALIDATION: "validate_input",
            EventStage.REPRESENTATION_CONSTRUCTION: "construct_representation",
            EventStage.DEMONSTRATION_VERIFICATION: "verify_demonstrations",
        }[self.stage]

    def to_dict(self) -> dict[str, str]:
        return {
            "schema_version": self.schema_version,
            "stage": self.stage.value,
            "operation_family": self.operation_family,
            "target_scope": self.target_scope.value,
            "outcome": self.outcome.value,
            "operation_token": self.operation_token,
        }


@dataclass(frozen=True, slots=True)
class TraceProvenance:
    """Arm/candidate lineage kept outside the object handed to TraceMiner."""
    task_id: str
    representation: Representation
    candidate_id: str
    grammar_hash: str
    implementation_hash: str
    trial_index: int

    def __post_init__(self) -> None:
        if not self.task_id or not self.candidate_id:
            raise ValueError("trace provenance identifiers are required")
        if not re.fullmatch(r"[0-9a-f]{64}", self.grammar_hash) or not re.fullmatch(r"[0-9a-f]{64}", self.implementation_hash):
            raise ValueError("grammar_hash and implementation_hash must be lowercase SHA-256 hex")
        if self.trial_index < 1 or self.trial_index > 10:
            raise ValueError("trial_index must be in [1,10]")


@dataclass(frozen=True, slots=True)
class AdaptedTrace:
    trace: ReasoningTrace
    events: tuple[SemanticEvent, ...]
    provenance: TraceProvenance

    def mining_projection(self, *, independent_task_family: str) -> ReasoningTrace:
        """Return a sanitized trace with only independently assigned family.

        Callers must supply a family label from the frozen external annotation
        map. Arm, grammar, candidate, target scope, raw parameters and outputs
        are deliberately absent from this projection.
        """
        family = independent_task_family.strip()
        if not family:
            raise ValueError("an independent task-family label is required")
        return ReasoningTrace(
            trace_id=self.trace.trace_id,
            task_id=self.trace.task_id,
            timestamp=self.trace.timestamp,
            steps=list(self.trace.steps),
            outcome=TraceOutcome(success=True, result=None, cost=0.0),
            metadata={"task_family": family, "semantic_trace_schema": TRACE_SCHEMA_VERSION},
        )


# Exact aliases from the Phase 2F registered R1 and R3 grammars.
_R1: Mapping[str, str] = {
    "identity": "identity",
    "reflect_horizontal": "flip_left_right",
    "reflect_vertical": "flip_top_bottom",
    "rotate_90": "rotate_90",
    "rotate_180": "rotate_180",
    "rotate_270": "rotate_270",
    "transpose": "transpose",
    "anti_transpose": "anti_transpose",
    "translate_constant": "translate",
    "recolor_bijection": "recolor",
}
_R3: Mapping[str, str] = {
    "identity": "identity",  # canonical effect alias for the zero-offset move
    "move": "translate",
    "copy": "copy",
    "delete": "delete",
    "recolor": "recolor",
    "rotate_90": "rotate_90",
    "rotate_180": "rotate_180",
    "rotate_270": "rotate_270",
    "reflect_horizontal_axis": "flip_top_bottom",
    "reflect_vertical_axis": "flip_left_right",
    "crop_bbox": "crop",
}


def _family(rep: Representation, operation: str) -> str:
    mapping = _R1 if rep is Representation.R1 else _R3
    try:
        return mapping[operation]
    except KeyError as exc:
        raise ValueError(f"operation is not in frozen {rep.value} grammar: {operation!r}") from exc


def r3_operation_name(action: Action) -> str:
    """Map a frozen R3 AST action to its semantic operation alias."""
    params = dict(action.params)
    if action.kind == "move" and set(params)=={"dx","dy"} and all(type(params[k]) is int and -2<=params[k]<=2 for k in ("dx","dy")):
        return "identity" if params["dx"]==0 and params["dy"]==0 else "move"
    if action.kind == "rotate" and params.get("k") in {1, 2, 3}:
        return f"rotate_{int(params['k']) * 90}"
    if action.kind == "reflect_horizontal_axis" and not params:
        return "reflect_horizontal_axis"
    if action.kind == "reflect_vertical_axis" and not params:
        return "reflect_vertical_axis"
    if action.kind in {"move", "copy", "delete", "recolor", "crop_bbox"}:
        return action.kind
    raise ValueError(f"invalid R3 action for semantic trace: {action.to_dict()!r}")


def adapt_successful_candidate(
    *,
    representation: Representation | str,
    operation: str | Action,
    task_id: str,
    candidate_id: str,
    grammar_hash: str,
    implementation_hash: str,
    trial_index: int,
    trace_id: str | None = None,
    timestamp: float = 0.0,
) -> AdaptedTrace:
    """Adapt a first exact training-demo-fit candidate into the common trace.

    Only a successful complete candidate is traceable. Failed parse/search or
    an invalid candidate returns no partial trace and must be logged separately.
    """
    rep = Representation(representation)
    semantic_operation = r3_operation_name(operation) if rep is Representation.R3 and isinstance(operation, Action) else operation
    if not isinstance(semantic_operation, str):
        raise TypeError("R1 operation must be a registered operation string; R3 must use an Action or registered alias")
    scope = TargetScope.GRID if rep is Representation.R1 else TargetScope.OBJECT
    family = _family(rep, semantic_operation)
    events = (
        SemanticEvent(TRACE_SCHEMA_VERSION, EventStage.INPUT_VALIDATION, "grid_input", TargetScope.NONE, EventOutcome.PASS),
        SemanticEvent(TRACE_SCHEMA_VERSION, EventStage.REPRESENTATION_CONSTRUCTION, "scene", TargetScope.NONE, EventOutcome.PASS),
        SemanticEvent(TRACE_SCHEMA_VERSION, EventStage.CANDIDATE_APPLICATION, family, scope, EventOutcome.PASS),
        SemanticEvent(TRACE_SCHEMA_VERSION, EventStage.DEMONSTRATION_VERIFICATION, "exact_training_fit", TargetScope.NONE, EventOutcome.PASS),
    )
    if len(events) > MAX_TRACE_STEPS:
        raise AssertionError("semantic trace exceeded frozen step cap")
    provenance = TraceProvenance(task_id, rep, candidate_id, grammar_hash, implementation_hash, trial_index)
    tid = trace_id or f"TR-{uuid.uuid4().hex}"
    steps = []
    for i, event in enumerate(events, start=1):
        # Scope remains in the common raw trace for interpretation, but the
        # frozen normalizer mines only operation strings. No arm/candidate IDs
        # or raw action parameters are copied into step inputs.
        inputs = ([{"target_scope": event.target_scope.value}]
                  if event.stage is EventStage.CANDIDATE_APPLICATION else [])
        steps.append(ReasoningStep(step_id=f"{tid}-S{i}", operation=event.operation_token, inputs=inputs))
    trace = ReasoningTrace(
        trace_id=tid,
        task_id=task_id,
        timestamp=float(timestamp),
        steps=steps,
        outcome=TraceOutcome(success=True, result=None, cost=0.0),
        metadata={"semantic_trace_schema": TRACE_SCHEMA_VERSION},
    )
    return AdaptedTrace(trace, events, provenance)


def validate_semantic_trace(adapted:AdaptedTrace) -> None:
    """Independent fail-closed validation of an adapted success trace.

    This checks the trace contract without calling the miner normalizer, so a
    normalization pass cannot silently stand in for schema validation.
    """
    trace=adapted.trace
    if trace.task_id!=adapted.provenance.task_id or len(trace.steps)!=4 or len(adapted.events)!=4:
        raise ValueError("semantic trace task lineage or four-step contract failed")
    if trace.outcome is None or not trace.outcome.success or trace.outcome.result is not None:
        raise ValueError("semantic trace must be successful with a null result")
    if trace.metadata!={"semantic_trace_schema":TRACE_SCHEMA_VERSION}:
        raise ValueError("raw trace metadata contains unregistered fields")
    expected=[event.operation_token for event in adapted.events]
    if trace.operations!=expected: raise ValueError("semantic trace tokens do not match typed events")
    if len({step.step_id for step in trace.steps})!=4: raise ValueError("semantic step IDs must be unique")
    for index,step in enumerate(trace.steps):
        if step.outputs: raise ValueError("semantic trace outputs are forbidden")
        allowed_inputs=([{"target_scope":adapted.events[index].target_scope.value}]
                        if adapted.events[index].stage is EventStage.CANDIDATE_APPLICATION else [])
        if step.inputs!=allowed_inputs: raise ValueError("semantic trace inputs contain unregistered fields")
    if any(event.outcome is not EventOutcome.PASS for event in adapted.events):
        raise ValueError("only complete successful semantic events are permitted")


def operation_mapping_table() -> dict[str, dict[str, str]]:
    """Return a copy for validation/reporting; callers cannot mutate maps."""
    return {"R1": dict(_R1), "R3": dict(_R3)}
