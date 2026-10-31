"""Trace Store — persist and retrieve reasoning traces (Phase 11).

One JSON document per trace, keyed by trace id, laid out by task family so
``list_by_family`` is a directory read rather than a full scan.
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterable

from core.states import TraceLifecyclePhase
from core.trace import ReasoningTrace

__all__ = ["TraceStore"]


class TraceStore:
    """Filesystem storage and retrieval for ReasoningTrace records."""

    def __init__(self, root: str | Path = "reports/traces") -> None:
        self.root = Path(root)
        self.root.mkdir(parents=True, exist_ok=True)

    def _path(self, family: str, trace_id: str) -> Path:
        return self._assert_within(self.root / _safe(family) / f"{_safe(trace_id)}.json")

    def _assert_within(self, path: Path) -> Path:
        """Guarantee the path stays inside the store root."""
        root = self.root.resolve()
        resolved = path.resolve()
        if root != resolved and root not in resolved.parents:
            raise ValueError(f"refusing path outside trace store: {path}")
        return path

    def save(self, trace: ReasoningTrace) -> Path:
        """Write one trace, marking it stored."""
        family = str((trace.metadata or {}).get("task_family") or "unknown")
        path = self._path(family, trace.trace_id)
        path.parent.mkdir(parents=True, exist_ok=True)
        if trace.phase is TraceLifecyclePhase.CREATED:
            trace.transition_to(TraceLifecyclePhase.STORED)
        path.write_text(_dumps(trace.to_dict()), encoding="utf-8")
        return path

    def save_many(self, traces: Iterable[ReasoningTrace]) -> list[Path]:
        return [self.save(t) for t in traces]

    def load(self, trace_id: str, *, family: str | None = None) -> ReasoningTrace:
        """Load a trace by id. ``family`` avoids a directory scan."""
        if family is not None:
            path = self._path(family, trace_id)
            if not path.exists():
                raise FileNotFoundError(path)
            return ReasoningTrace.from_dict(_loads(path))
        matches = list(self.root.glob(f"*/{_safe(trace_id)}.json"))
        if not matches:
            raise FileNotFoundError(f"trace not found: {trace_id!r}")
        return ReasoningTrace.from_dict(_loads(matches[0]))

    def list_by_family(self, family: str) -> list[ReasoningTrace]:
        """All traces for one task family, ordered by trace id."""
        directory = self._assert_within(self.root / (_safe(family) or "unknown"))
        if not directory.exists():
            return []
        return [
            ReasoningTrace.from_dict(_loads(p))
            for p in sorted(directory.glob("*.json"))
        ]

    def load_all(self) -> list[ReasoningTrace]:
        """Every stored trace."""
        out: list[ReasoningTrace] = []
        for directory in sorted(p for p in self.root.iterdir() if p.is_dir()):
            out.extend(self.list_by_family(directory.name))
        return out

    def families(self) -> list[str]:
        return sorted(p.name for p in self.root.iterdir() if p.is_dir())

    def count(self) -> int:
        return sum(1 for _ in self.root.glob("*/*.json"))

    def clear(self) -> None:
        for path in self.root.glob("*/*.json"):
            path.unlink()


def _safe(name: str) -> str:
    """Sanitize a path segment, rejecting traversal.

    ``.`` survives the allow-list, so ``..`` would escape the store root; it is
    collapsed explicitly and verified afterwards by ``_assert_within``.
    """
    cleaned = "".join(c if (c.isalnum() or c in "-_.") else "_" for c in str(name))
    cleaned = cleaned.replace("..", "_").strip("._")
    return cleaned


def _dumps(payload: dict) -> str:
    import json

    return json.dumps(payload, indent=2, sort_keys=True)


def _loads(path: Path) -> dict:
    import json

    return json.loads(path.read_text(encoding="utf-8"))
