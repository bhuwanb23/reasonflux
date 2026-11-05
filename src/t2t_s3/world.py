"""Deterministic Relational Unlock World for S3 implementation-only work."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ObjectKind(str, Enum):
    KEY = "KEY"
    TARGET = "TARGET"
    DISTRACTOR = "DISTRACTOR"


@dataclass(frozen=True, slots=True)
class UnlockObject:
    object_id: str
    kind: ObjectKind
    x: int
    y: int
    color: str
    shape: str
    opens_target_id: str | None = None
    closed: bool | None = None


@dataclass(frozen=True, slots=True)
class UnlockAction:
    key_id: str
    target_id: str


@dataclass(frozen=True, slots=True)
class UnlockState:
    context_id: str
    objects: tuple[UnlockObject, ...]
    agent_x: int
    agent_y: int
    path_clear: bool | None

    def is_complete(self) -> bool:
        if not isinstance(self.path_clear, bool):
            return False
        ids = [obj.object_id for obj in self.objects]
        if len(ids) != len(set(ids)) or any(not object_id for object_id in ids):
            return False
        for obj in self.objects:
            if obj.kind is ObjectKind.KEY and not obj.opens_target_id:
                return False
            if obj.kind is ObjectKind.TARGET and not isinstance(obj.closed, bool):
                return False
        return True

    def object_by_id(self, object_id: str) -> UnlockObject | None:
        return next((obj for obj in self.objects if obj.object_id == object_id), None)

    def targets(self) -> tuple[UnlockObject, ...]:
        return tuple(obj for obj in self.objects if obj.kind is ObjectKind.TARGET)

    def keys(self) -> tuple[UnlockObject, ...]:
        return tuple(obj for obj in self.objects if obj.kind is ObjectKind.KEY)

    def has_dangling_relations(self) -> bool:
        ids = {obj.object_id for obj in self.objects}
        return any(
            obj.kind is ObjectKind.KEY and obj.opens_target_id not in ids
            for obj in self.objects
        )


@dataclass(frozen=True, slots=True)
class Effect:
    target_opened: bool
    agent_advanced: bool

    @property
    def success(self) -> bool:
        return self.target_opened and self.agent_advanced


SUCCESS = Effect(target_opened=True, agent_advanced=True)
NO_EFFECT = Effect(target_opened=False, agent_advanced=False)


@dataclass(frozen=True, slots=True)
class UnlockTrace:
    trace_id: str
    state: UnlockState
    action: UnlockAction
    observed_effect: Effect
    provenance: str = "SYNTHETIC_SOURCE"


class RelationalUnlockWorld:
    """World rule uses explicit typed object references and visible state only."""

    @staticmethod
    def adjacent(state: UnlockState, target: UnlockObject) -> bool:
        return abs(state.agent_x - target.x) + abs(state.agent_y - target.y) == 1

    @classmethod
    def applicable(cls, state: UnlockState, action: UnlockAction) -> bool | None:
        if not state.is_complete():
            return None
        if state.has_dangling_relations():
            return False
        key = state.object_by_id(action.key_id)
        target = state.object_by_id(action.target_id)
        if key is None or target is None:
            return False
        if key.kind is not ObjectKind.KEY or target.kind is not ObjectKind.TARGET:
            return False
        return bool(
            key.opens_target_id == target.object_id
            and target.closed is True
            and cls.adjacent(state, target)
            and state.path_clear is True
        )

    @classmethod
    def step(cls, state: UnlockState, action: UnlockAction) -> Effect | None:
        applicability = cls.applicable(state, action)
        if applicability is None:
            return None
        return SUCCESS if applicability else NO_EFFECT

    @staticmethod
    def trace(trace_id: str, state: UnlockState, action: UnlockAction) -> UnlockTrace:
        effect = RelationalUnlockWorld.step(state, action)
        if effect is None:
            raise ValueError("cannot record a source effect from an unknown required state")
        return UnlockTrace(trace_id, state, action, effect)

    @staticmethod
    def exact_state_signature(state: UnlockState) -> tuple:
        return (
            state.agent_x,
            state.agent_y,
            state.path_clear,
            tuple(
                (
                    obj.object_id,
                    obj.kind.value,
                    obj.x,
                    obj.y,
                    obj.color,
                    obj.shape,
                    obj.opens_target_id,
                    obj.closed,
                )
                for obj in state.objects
            ),
        )

    @staticmethod
    def source_only_features(state: UnlockState, action: UnlockAction) -> dict[str, bool] | None:
        """Return the frozen feature grammar, or None for incomplete bindings."""
        if not state.is_complete():
            return None
        key = state.object_by_id(action.key_id)
        target = state.object_by_id(action.target_id)
        return {
            "key_is_key": key is not None and key.kind is ObjectKind.KEY,
            "target_is_target": target is not None and target.kind is ObjectKind.TARGET,
            "target_closed": target is not None and target.closed is True,
            "agent_adjacent": target is not None and RelationalUnlockWorld.adjacent(state, target),
            "path_clear": state.path_clear is True,
            "key_unlocks_selected_target": (
                key is not None and target is not None and key.opens_target_id == target.object_id
            ),
        }


def validate_trace(trace: UnlockTrace) -> None:
    if trace.provenance not in {"SYNTHETIC_SOURCE", "SYNTHETIC_DEVELOPMENT"}:
        raise ValueError("S3 implementation accepts synthetic source/development traces only")
    if not trace.state.is_complete():
        raise ValueError("source trace must contain a complete observable state")
    if trace.state.has_dangling_relations():
        raise ValueError("source trace has a dangling object relation")
    if trace.observed_effect not in {SUCCESS, NO_EFFECT}:
        raise ValueError("partial effects are invalid; the world has success or exact no-effect outcomes only")
