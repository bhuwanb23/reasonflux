"""Modular implementation of the Phase 13C-SCT-V1 experiment."""
from __future__ import annotations

from pathlib import Path
import sys
_ROOT = Path(__file__).resolve().parents[2]
for _path in (_ROOT, _ROOT / "src"):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))
