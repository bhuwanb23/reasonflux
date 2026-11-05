"""Tiny synthetic T2T-S2 mechanism prototype; no ARC integrations."""

from .evaluation import evaluate_boundary, evaluate_prediction_accuracy
from .invariant import BoundaryLearner, BoundaryVersion, InvariantI0
from .replay import R1MaxReplay
from .world import Effect, KeyDoorState, KeyDoorWorld, Trace

__all__ = [
    "BoundaryLearner",
    "BoundaryVersion",
    "Effect",
    "InvariantI0",
    "KeyDoorState",
    "KeyDoorWorld",
    "R1MaxReplay",
    "Trace",
    "evaluate_boundary",
    "evaluate_prediction_accuracy",
]
