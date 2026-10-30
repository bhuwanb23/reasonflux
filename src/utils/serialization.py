"""Serialize and deserialize ASFT objects (JSON)."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Callable, TypeVar

T = TypeVar("T")


def save_object(obj: Any, path: str | Path) -> Path:
    """Serialize an object with ``to_dict()`` to a JSON file."""
    if not hasattr(obj, "to_dict") or not callable(obj.to_dict):
        raise TypeError(f"Object of type {type(obj)!r} has no to_dict()")
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    payload = obj.to_dict()
    target.write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return target


def load_object(path: str | Path, from_dict: Callable[[dict[str, Any]], T]) -> T:
    """Deserialize JSON via a type's ``from_dict`` constructor."""
    target = Path(path)
    data = json.loads(target.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise ValueError(f"Expected JSON object in {target}, got {type(data).__name__}")
    return from_dict(data)
