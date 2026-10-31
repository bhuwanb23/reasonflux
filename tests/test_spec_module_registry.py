"""Phase 11F spec: the module registry must match disk reality.

Guards against the failure mode where a checklist marks everything complete
while entry points are still stubs.
"""

from __future__ import annotations

import importlib
import re
from pathlib import Path
from typing import Any

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "configs" / "modules.yaml"
BLUEPRINT = ROOT / "docs" / "02_design" / "implementation_blueprint.md"

VALID_STATUS = {"implemented", "partial", "stub", "missing"}
VALID_LAYERS = {1, 2, 3, 4, 5}


@pytest.fixture(scope="module")
def registry() -> dict[str, Any]:
    assert REGISTRY.exists(), f"missing registry: {REGISTRY}"
    data = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    assert isinstance(data, dict)
    return data


@pytest.fixture(scope="module")
def modules(registry: dict[str, Any]) -> list[dict[str, Any]]:
    mods = registry.get("modules") or []
    assert mods, "registry defines no modules"
    return mods


def test_module_ids_contiguous(modules: list[dict[str, Any]]):
    ids = [m["id"] for m in modules]
    m_ids = sorted(i for i in ids if i.startswith("M"))
    assert m_ids == [f"M{n:02d}" for n in range(1, 24)], m_ids
    assert "T1" in ids, "transfer engine must be registered"
    assert len(ids) == len(set(ids)), "duplicate module ids"


def test_layers_in_range(modules: list[dict[str, Any]]):
    for m in modules:
        assert m["layer"] in VALID_LAYERS, f"{m['id']} has layer {m['layer']}"


def test_status_vocabulary(modules: list[dict[str, Any]]):
    for m in modules:
        assert m["status"] in VALID_STATUS, f"{m['id']} status {m['status']!r}"


def test_every_declared_path_exists(modules: list[dict[str, Any]]):
    missing: list[str] = []
    for m in modules:
        assert m.get("paths"), f"{m['id']} declares no paths"
        for rel in m["paths"]:
            if not (ROOT / rel).exists():
                missing.append(f"{m['id']} -> {rel}")
    assert not missing, f"registry points at non-existent paths: {missing}"


def test_implemented_modules_expose_their_symbols(modules: list[dict[str, Any]]):
    """An `implemented` module must actually import its public entry point."""
    # Import order matters: `invariants` first avoids the transfer<->invariants
    # circular-import bootstrapping path when `transfer` is imported cold.
    importlib.import_module("invariants")
    broken: list[str] = []
    for m in modules:
        if m["status"] != "implemented":
            continue
        assert m.get("symbols"), f"{m['id']} is implemented but exposes no symbol"
        for spec in m["symbols"]:
            mod = importlib.import_module(spec["module"])
            if not hasattr(mod, spec["name"]):
                broken.append(f"{m['id']}: {spec['module']}.{spec['name']}")
    assert not broken, f"implemented modules missing symbols: {broken}"


def test_partial_modules_own_a_stub(registry: dict[str, Any], modules: list[dict[str, Any]]):
    """A `partial` status must be justified by a real NotImplementedError stub."""
    stubs = registry.get("stubs") or []
    owners = {s["module"] for s in stubs}
    unjustified = [
        m["id"] for m in modules if m["status"] == "partial" and m["id"] not in owners
    ]
    assert not unjustified, (
        "modules marked partial without a registered stub: " f"{unjustified}"
    )


def test_implemented_modules_own_no_stub(
    registry: dict[str, Any], modules: list[dict[str, Any]]
):
    """The inverse guard: an `implemented` module may not still own a stub.

    Without this, a module whose *libraries* exist can be relabelled
    `implemented` while its entry point is still unimplemented — exactly the
    checklist drift this spec exists to prevent.
    """
    owners = {s["module"] for s in registry.get("stubs") or []}
    overclaimed = [
        m["id"] for m in modules if m["status"] == "implemented" and m["id"] in owners
    ]
    assert not overclaimed, (
        "modules marked implemented but still own stubs: " f"{overclaimed}"
    )


def test_stub_files_really_raise(registry: dict[str, Any]):
    """Each stub entry must still be unimplemented at its declared location.

    ``kind: declaration`` entries are packages that only carry a docstring, so
    they are checked for the absence of real definitions instead.
    """
    offenders: list[str] = []
    for stub in registry.get("stubs") or []:
        path = ROOT / stub["path"]
        if not path.exists():
            offenders.append(f"{stub['path']} (missing)")
            continue
        text = path.read_text(encoding="utf-8")
        if stub.get("kind") == "declaration":
            if re.search(r"^(def |class )", text, re.MULTILINE):
                offenders.append(f"{stub['path']} (declaration now has code)")
            continue
        if "NotImplementedError" not in text:
            offenders.append(f"{stub['path']} (no NotImplementedError)")
            continue
        if stub["symbol"].split(".")[-1] not in text:
            offenders.append(f"{stub['path']} (no symbol {stub['symbol']})")
    assert not offenders, f"stale stub inventory: {offenders}"


def test_stub_owners_are_registered_modules(registry: dict[str, Any], modules: list[dict[str, Any]]):
    ids = {m["id"] for m in modules}
    for stub in registry.get("stubs") or []:
        assert stub["module"] in ids, f"stub {stub['path']} owned by unknown {stub['module']}"


def test_blueprint_documents_every_module(modules: list[dict[str, Any]]):
    text = BLUEPRINT.read_text(encoding="utf-8")
    undocumented = [m["name"] for m in modules if m["name"] not in text]
    assert not undocumented, f"blueprint omits modules: {undocumented}"


def test_blueprint_documents_every_stub(registry: dict[str, Any]):
    text = BLUEPRINT.read_text(encoding="utf-8")
    undocumented = [
        s["path"] for s in registry.get("stubs") or [] if s["path"] not in text
    ]
    assert not undocumented, f"blueprint omits stubs: {undocumented}"


def test_no_stubs_remain():
    """Completion guard: no entry point under src/ may raise NotImplementedError.

    This is the assertion that makes flipping every module to `implemented`
    legitimate rather than aspirational.
    """
    offenders = [
        str(p.relative_to(ROOT))
        for p in (ROOT / "src").rglob("*.py")
        if "NotImplementedError" in p.read_text(encoding="utf-8")
    ]
    assert not offenders, f"unimplemented entry points remain: {offenders}"


def test_registry_declares_no_stubs(registry: dict[str, Any]):
    assert registry.get("stubs") == [], "stub list must stay empty once complete"


def test_all_gates_demonstrated(registry: dict[str, Any]):
    blocked = [g["id"] for g in registry["gates"] if g["status"] != "demonstrated"]
    assert not blocked, f"gates not demonstrated: {blocked}"
