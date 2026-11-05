"""T2T-S3 implementation package; importing it never executes a run."""

from .arms import (
    I0Invariant,
    Prediction,
    R0RawReplay,
    R1ParameterizedReplay,
    R2CompressedReplay,
    R3GrammarReplay,
    R4ReplayMax,
)
from .generator import (
    TransformationRecipe,
    apply_recipe,
    appearance_shift_recipe,
    composed_surface_recipe,
    identity_shift_recipe,
    layout_shift_recipe,
    role_layout_recipe,
)
from .scoring import EligibleContext, PredictionRecord, ScoreReport, ScoreSummary, aggregate_all_context_scores
from .transforms import SurfaceTransform, transform_state
from .world import (
    Effect,
    ObjectKind,
    RelationalUnlockWorld,
    UnlockAction,
    UnlockObject,
    UnlockState,
    UnlockTrace,
)

__all__ = [
    "Effect",
    "EligibleContext",
    "I0Invariant",
    "ObjectKind",
    "Prediction",
    "PredictionRecord",
    "R0RawReplay",
    "R1ParameterizedReplay",
    "R2CompressedReplay",
    "R3GrammarReplay",
    "R4ReplayMax",
    "RelationalUnlockWorld",
    "ScoreReport",
    "ScoreSummary",
    "SurfaceTransform",
    "TransformationRecipe",
    "UnlockAction",
    "UnlockObject",
    "UnlockState",
    "UnlockTrace",
    "aggregate_all_context_scores",
    "appearance_shift_recipe",
    "apply_recipe",
    "composed_surface_recipe",
    "identity_shift_recipe",
    "layout_shift_recipe",
    "role_layout_recipe",
    "transform_state",
]
