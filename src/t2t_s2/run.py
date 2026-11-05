"""Run the one frozen, deterministic S2 key/door mechanism check."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from .evaluation import evaluate_boundary, evaluate_prediction_accuracy
from .invariant import BoundaryLearner, CounterexampleRecord, InvariantI0
from .replay import R1MaxReplay
from .world import ACTION, NO_EFFECT, SUCCESS, KeyDoorState, KeyDoorWorld, Trace


def _state(
    context_id: str,
    key_color: str,
    door_color: str,
    *,
    adjacent: bool = True,
    door_closed: bool = True,
    has_key: bool = True,
    corridor_clear: bool = True,
) -> KeyDoorState:
    return KeyDoorState(
        context_id=context_id,
        adjacent=adjacent,
        door_closed=door_closed,
        has_key=has_key,
        corridor_clear=corridor_clear,
        key_color=key_color,
        door_color=door_color,
    )


def frozen_source_traces() -> tuple[Trace, ...]:
    states = (
        _state("SRC-POS-blue", "blue", "blue"),
        _state("SRC-POS-green", "green", "green"),
        _state("SRC-CE-red-blue", "red", "blue"),
        _state("SRC-NEG-purple-yellow", "purple", "yellow"),
        _state("SRC-NEG-no-key", "black", "black", has_key=False),
        _state("SRC-NEG-blocked", "tan", "tan", corridor_clear=False),
        _state("SRC-NEG-not-adjacent", "white", "white", adjacent=False),
        _state("SRC-NEG-door-open", "gray", "gray", door_closed=False),
    )
    return tuple(KeyDoorWorld.trace(f"trace:{state.context_id}", state) for state in states)


def frozen_n_holdout() -> tuple[KeyDoorState, ...]:
    return (
        _state("N-H1-yellow", "yellow", "yellow"),
        _state("N-H2-orange", "orange", "orange"),
        _state("N-H3-cyan", "cyan", "cyan"),
        _state("N-H4-magenta", "magenta", "magenta"),
        _state("N-H5-amber-violet", "amber", "violet"),
        _state("N-H6-teal-brown", "teal", "brown"),
        _state("N-H7-no-key", "white", "white", has_key=False),
        _state("N-H8-blocked", "gray", "gray", corridor_clear=False),
    )


def frozen_b_holdout() -> tuple[KeyDoorState, ...]:
    return (
        _state("B-H1-gold", "gold", "gold"),
        _state("B-H2-silver", "silver", "silver"),
        _state("B-H3-violet-orange", "violet", "orange"),
        _state("B-H4-pink-teal", "pink", "teal"),
        _state("B-H5-no-key", "white", "white", has_key=False),
        _state("B-H6-blocked", "gray", "gray", corridor_clear=False),
    )


def run_s2() -> dict:
    source = frozen_source_traces()
    source_by_id = {trace.state.context_id: trace for trace in source}
    n_holdout = frozen_n_holdout()
    b_holdout = frozen_b_holdout()

    # S2.2: fit the trace-derived macro first, only on the frozen source corpus.
    replay = R1MaxReplay.fit(source)

    # S2.3: instantiate the one predeclared explicit relation; no target tuning.
    invariant = InvariantI0.fit(source)
    n_cases = tuple((state, KeyDoorWorld.step(state, ACTION)) for state in n_holdout)
    n_result = evaluate_prediction_accuracy(
        n_cases,
        {
            "I0": invariant.predict_effect,
            "R1-Max": replay.predict,
        },
    )
    n_i0 = n_result["arms"]["I0"]["accuracy"]
    n_r1 = n_result["arms"]["R1-Max"]["accuracy"]
    n_result["delta_accuracy_I0_minus_R1"] = n_i0 - n_r1
    n_result["decision"] = "N-PASS" if n_i0 > n_r1 else "N-FAIL"

    # S2.5: the red/blue source event was frozen before its observed effect and
    # is used for refinement only; it is excluded from the fresh B holdout.
    ce_trace = source_by_id["SRC-CE-red-blue"]
    parent = invariant.initial_boundary()
    ce_prediction = invariant.predict_skill_effect(ce_trace.state, parent)
    if ce_prediction is None:
        raise AssertionError("frozen G0 should admit the predeclared CE context")
    counterexample = CounterexampleRecord(
        record_id="synthetic:ce:red-blue:v1",
        state=ce_trace.state,
        predicted_skill_effect=ce_prediction,
        observed_effect=ce_trace.observed_effect,
    )
    positive_supports = tuple(
        trace for trace in source if trace.observed_effect == SUCCESS
    )
    refiner = BoundaryLearner()
    successor = refiner.refine(parent, counterexample, positive_supports)
    b_result = evaluate_boundary(
        b_holdout,
        {"I0-G0-no-boundary-update": parent, "I1-G1-CE-updated": successor},
    )
    g0 = b_result["boundaries"]["I0-G0-no-boundary-update"]
    g1 = b_result["boundaries"]["I1-G1-CE-updated"]
    b_pass = (
        g1["false_activation"] < g0["false_activation"]
        and g1["true_admitted"] >= g0["true_admitted"]
    )
    b_result["decision"] = "B-PASS" if b_pass else "B-FAIL"
    b_result["refinement"] = {
        "counterexample_id": counterexample.record_id,
        "counterexample_context_id": ce_trace.state.context_id,
        "prediction_frozen_before_observation": True,
        "predicted_skill_effect": asdict(counterexample.predicted_skill_effect),
        "observed_effect": asdict(counterexample.observed_effect),
        "parent_boundary_id": parent.version_id,
        "successor_boundary_id": successor.version_id,
        "successor_predicate": "key_color == door_color",
        "counterexample_not_in_holdout": all(
            state.context_id != ce_trace.state.context_id for state in b_holdout
        ),
        "append_only_counterexample_count": len(refiner.counterexample_ledger),
    }

    result = {
        "run_id": "T2T-S2-KeyDoor-Run-v1-revised",
        "run_date": "2026-11-04",
        "plan_id": "T2T-S2-SyntheticMechanism-v1.0.0-draft",
        "scope": "one deterministic synthetic key/door world; Claims N and B only",
        "not_arc_or_benchmark": True,
        "n_decision_grade_status": "N-BLOCKED",
        "n_validity_reason": (
            "This revised run follows an earlier pilot that exposed the same N holdout; "
            "R1-Max and I0 were changed after the pilot output, so these raw revised scores are exploratory."
        ),
        "b_scope_status": "FINITE_SYNTHETIC_FIXTURE_ONLY",
        "world_rule": "base_conditions AND key_color == door_color -> open and advance; otherwise no effect",
        "source_contexts": [
            {"trace_id": trace.trace_id, "state": asdict(trace.state), "effect": asdict(trace.observed_effect)}
            for trace in source
        ],
        "n_holdout_contexts": [asdict(state) for state in n_holdout],
        "b_holdout_contexts": [asdict(state) for state in b_holdout],
        "n_result": n_result,
        "b_result": b_result,
        "interpretation_limit": (
            "Deterministic finite-fixture result only. No statistical, population, ARC,"
            " harm-reduction, cost-effectiveness, or novelty claim follows."
        ),
    }
    return result


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("docs/05_trace_to_transfer/s2/results/keydoor_run_v1.json"),
    )
    args = parser.parse_args()
    result = run_s2()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"{result['run_id']}: {result['n_result']['decision']}; {result['b_result']['decision']}")
    for arm, metrics in result["n_result"]["arms"].items():
        print(f"N {arm}: {metrics['correct']}/{metrics['denominator_all_contexts']} accuracy; abstain={metrics['abstain']}")
    for boundary, metrics in result["b_result"]["boundaries"].items():
        print(
            f"B {boundary}: false_activation={metrics['false_activation']}/{metrics['non_applicable']}; "
            f"applicable_coverage={metrics['true_admitted']}/{metrics['true_applicable']}"
        )
    print(f"Wrote {args.output}")


if __name__ == "__main__":
    main()
