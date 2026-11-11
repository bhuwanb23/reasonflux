"""Tests for Phase 11C-2 Stage 2 — trace normalization."""

from core import ReasoningStep, ReasoningTrace, TraceOutcome
from traces import (
    DEFAULT_SYNONYM_MAP,
    canonicalize_operation,
    normalize_lookup_key,
    normalize_trace,
)


def _trace(operations, *, outcome_success=True, family=None, task_id="t1"):
    steps = [
        ReasoningStep(step_id=f"s{i}", operation=op)
        for i, op in enumerate(operations, start=1)
    ]
    metadata = {"task_family": family} if family else {}
    return ReasoningTrace(
        trace_id="tr1",
        task_id=task_id,
        timestamp=1.0,
        steps=steps,
        outcome=TraceOutcome(success=outcome_success),
        metadata=metadata,
    )


def test_synonym_map_canonicalizes_doc_example():
    assert canonicalize_operation("LocateObject") == "detect_object"
    assert canonicalize_operation("FindMirrorAxis") == "find_symmetry"
    assert canonicalize_operation("Reflect") == "apply_reflection"
    assert canonicalize_operation("Verify") == "verify_output"


def test_case_and_punctuation_handling():
    assert normalize_lookup_key("Find-Symmetry!") == "findsymmetry"
    assert canonicalize_operation("Find_Symmetry") == "find_symmetry"
    assert canonicalize_operation("detect-object") == "detect_object"


def test_unmapped_names_pass_through_normalized():
    assert canonicalize_operation("my_custom_step") == "my_custom_step"
    assert canonicalize_operation("CustomOp") == "customop"


def test_normalize_trace_aligns_synonym_variants():
    a = _trace(["LocateObject", "FindMirrorAxis", "Reflect", "Verify"], family="reflection")
    b = _trace(
        ["DetectObject", "FindSymmetry", "ApplyReflection", "VerifyOutput"],
        family="reflection",
        task_id="t2",
    )
    na = normalize_trace(a)
    nb = normalize_trace(b)
    assert na.operations == nb.operations == [
        "detect_object",
        "find_symmetry",
        "apply_reflection",
        "verify_output",
    ]


def test_task_family_from_metadata_else_task_id():
    with_family = normalize_trace(_trace(["DetectObject"], family="rotation"))
    assert with_family.task_family == "rotation"
    without = normalize_trace(_trace(["DetectObject"], task_id="solo-task"))
    assert without.task_family == "solo-task"


def test_missing_outcome_defaults_to_success():
    steps = [ReasoningStep(step_id="s1", operation="DetectObject")]
    trace = ReasoningTrace(trace_id="tr", task_id="t", timestamp=1.0, steps=steps)
    assert normalize_trace(trace).success is True


def test_failure_outcome_preserved():
    assert normalize_trace(_trace(["DetectObject"], outcome_success=False)).success is False


def test_default_synonym_map_covers_core_ops():
    for key in ("detectobject", "findsymmetry", "applyreflection", "findrotation"):
        assert key in DEFAULT_SYNONYM_MAP
