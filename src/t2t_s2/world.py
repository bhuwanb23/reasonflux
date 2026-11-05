"""One deterministic key/door world for the S2 mechanism check."""

from __future__ import annotations

from dataclasses import dataclass

ACTION = "USE_KEY_AND_ENTER"


@dataclass(frozen=True, slots=True)
class KeyDoorState:
    context_id: str
    adjacent: bool
    door_closed: bool
    has_key: bool
    corridor_clear: bool
    key_color: str | None
    door_color: str | None

    def is_complete(self) -> bool:
        return (
            isinstance(self.adjacent, bool)
            and isinstance(self.door_closed, bool)
            and isinstance(self.has_key, bool)
            and isinstance(self.corridor_clear, bool)
            and isinstance(self.key_color, str)
            and isinstance(self.door_color, str)
            and bool(self.key_color)
            and bool(self.door_color)
        )

    def base_conditions_hold(self) -> bool:
        return (
            self.adjacent
            and self.door_closed
            and self.has_key
            and self.corridor_clear
        )

    def colors_match(self) -> bool:
        return self.key_color is not None and self.key_color == self.door_color


@dataclass(frozen=True, slots=True)
class Effect:
    door_open: bool
    agent_advanced: bool

    @property
    def succeeded(self) -> bool:
        return self.door_open and self.agent_advanced


SUCCESS = Effect(door_open=True, agent_advanced=True)
NO_EFFECT = Effect(door_open=False, agent_advanced=False)


@dataclass(frozen=True, slots=True)
class Trace:
    trace_id: str
    state: KeyDoorState
    action: str
    observed_effect: Effect


class KeyDoorWorld:
    """Deterministic transition rule; all labels are synthetic and observable."""

    @staticmethod
    def applicable(state: KeyDoorState) -> bool:
        return state.is_complete() and state.base_conditions_hold() and state.colors_match()

    @classmethod
    def step(cls, state: KeyDoorState, action: str = ACTION) -> Effect:
        if action != ACTION:
            raise ValueError(f"unsupported synthetic action: {action!r}")
        return SUCCESS if cls.applicable(state) else NO_EFFECT

    @classmethod
    def trace(cls, trace_id: str, state: KeyDoorState) -> Trace:
        return Trace(trace_id, state, ACTION, cls.step(state))
