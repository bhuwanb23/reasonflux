"""Phase 11F spec: claim → module → metric → experiment → verifier must resolve.

Also enforces the v0.1 non-goals so scope creep fails the build.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "configs" / "modules.yaml"
METRICS = ROOT / "configs" / "metrics.yaml"
EXPERIMENTS = ROOT / "configs" / "experiments.yaml"
TRACEABILITY = ROOT / "docs" / "04_paper" / "claim_traceability.md"
READINESS = ROOT / "docs" / "00_project" / "v0_1_readiness.md"
SRC = ROOT / "src"

FORBIDDEN_MODULE_PATTERNS = (
    "planner",
    "agent",
    "meta_reasoner",
    "world_model",
    "self_improve",
    "concept_graph",
)
FORBIDDEN_IMPORTS = ("torch", "transformers", "tensorflow", "jax")


@pytest.fixture(scope="module")
def registry() -> dict[str, Any]:
    return yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))


@pytest.fixture(scope="module")
def modules(registry: dict[str, Any]) -> list[dict[str, Any]]:
    return registry["modules"]


@pytest.fixture(scope="module")
def metric_names() -> set[str]:
    data = yaml.safe_load(METRICS.read_text(encoding="utf-8"))
    return set((data.get("metrics") or {}).keys())


@pytest.fixture(scope="module")
def experiment_ids() -> set[str]:
    data = yaml.safe_load(EXPERIMENTS.read_text(encoding="utf-8"))
    return set((data.get("experiments") or {}).keys())


def test_module_metrics_are_registered(modules: list[dict[str, Any]], metric_names: set[str]):
    unknown: list[str] = []
    for m in modules:
        for metric in m.get("metrics") or []:
            if metric not in metric_names:
                unknown.append(f"{m['id']}:{metric}")
    assert not unknown, f"modules cite unregistered metrics: {unknown}"


def test_module_experiments_are_registered(
    modules: list[dict[str, Any]], experiment_ids: set[str]
):
    unknown: list[str] = []
    for m in modules:
        for exp in m.get("experiments") or []:
            if exp not in experiment_ids:
                unknown.append(f"{m['id']}:{exp}")
    assert not unknown, f"modules cite unregistered experiments: {unknown}"


def test_every_contribution_has_full_chain(
    registry: dict[str, Any],
    modules: list[dict[str, Any]],
    metric_names: set[str],
    experiment_ids: set[str],
):
    by_id = {m["id"]: m for m in modules}
    problems: list[str] = []
    for c in registry["contributions"]:
        cid = c["id"]
        if not c.get("modules"):
            problems.append(f"{cid}: no modules")
            continue
        for mid in c["modules"]:
            if mid not in by_id:
                problems.append(f"{cid}: unknown module {mid}")
        if not c.get("metrics"):
            problems.append(f"{cid}: no metrics")
        for metric in c.get("metrics") or []:
            if metric not in metric_names:
                problems.append(f"{cid}: unregistered metric {metric}")
        if not c.get("experiments"):
            problems.append(f"{cid}: no experiments")
        for exp in c.get("experiments") or []:
            if exp not in experiment_ids:
                problems.append(f"{cid}: unregistered experiment {exp}")
        if not c.get("claim"):
            problems.append(f"{cid}: no claim statement")
        if not c.get("paper_artifact"):
            problems.append(f"{cid}: no paper artifact")
    assert not problems, problems


def test_contributions_cover_all_modules(registry: dict[str, Any], modules: list[dict[str, Any]]):
    covered = {mid for c in registry["contributions"] for mid in c["modules"]}
    uncovered = {m["id"] for m in modules} - covered
    assert not uncovered, f"modules not tied to any claim: {sorted(uncovered)}"


def test_gate_verifiers_exist(registry: dict[str, Any]):
    problems: list[str] = []
    for gate in registry["gates"]:
        assert gate["status"] in {"demonstrated", "blocked"}, gate["id"]
        verifier = gate["verifier"]
        path_part, _, test_name = verifier.partition("::")
        path = ROOT / path_part
        if not path.exists():
            problems.append(f"{gate['id']}: missing {path_part}")
            continue
        if not test_name:
            problems.append(f"{gate['id']}: verifier has no test name")
            continue
        if test_name not in path.read_text(encoding="utf-8"):
            problems.append(f"{gate['id']}: {path_part} lacks {test_name}")
    assert not problems, problems


def test_blocked_gates_name_a_live_stub(registry: dict[str, Any]):
    """Any gate still marked blocked must name a live stub.

    As of Phase 11 completion there are zero blocked gates, so this validates the
    invariant conditionally rather than requiring a blocker to exist. The
    companion guard (``test_no_stubs_remain`` in the registry spec) is what stops
    the gate list from silently drifting back to ``blocked``.
    """
    stub_paths = {s["path"] for s in registry["stubs"]}
    for gate in registry["gates"]:
        if gate["status"] != "blocked":
            continue
        blocker = gate.get("blocker")
        assert blocker, f"{gate['id']} is blocked but names no blocker"
        assert blocker in stub_paths, (
            f"{gate['id']} blocker {blocker} is not a registered stub"
        )
        text = (ROOT / blocker).read_text(encoding="utf-8")
        assert "NotImplementedError" in text, (
            f"{blocker} no longer a stub; update the gate"
        )


def test_demonstrated_gates_are_not_blocked(registry: dict[str, Any]):
    for gate in registry["gates"]:
        if gate["status"] == "demonstrated":
            assert not gate.get("blocker"), f"{gate['id']} demonstrated yet names a blocker"


def test_non_goals_documented(registry: dict[str, Any]):
    non_goals = registry.get("non_goals") or []
    assert len(non_goals) >= 10, "v0.1 exclusion list is incomplete"
    text = (ROOT / "docs" / "02_design" / "implementation_blueprint.md").read_text(
        encoding="utf-8"
    )
    for item in non_goals:
        keyword = item.split()[0].lower()
        assert keyword in text.lower(), f"non-goal not documented: {item}"


def test_no_forbidden_capabilities_in_src():
    offenders: list[str] = []
    for path in SRC.rglob("*.py"):
        stem = path.stem.lower()
        if any(pat in stem for pat in FORBIDDEN_MODULE_PATTERNS):
            offenders.append(str(path.relative_to(ROOT)))
    assert not offenders, f"v0.1 non-goal modules present: {offenders}"


def test_no_neural_framework_imports():
    pattern = re.compile(
        r"^\s*(?:import|from)\s+(" + "|".join(FORBIDDEN_IMPORTS) + r")\b", re.MULTILINE
    )
    offenders: list[str] = []
    for path in SRC.rglob("*.py"):
        if pattern.search(path.read_text(encoding="utf-8")):
            offenders.append(str(path.relative_to(ROOT)))
    assert not offenders, f"neural framework imports violate v0.1 scope: {offenders}"


def test_traceability_doc_covers_every_contribution(registry: dict[str, Any]):
    text = TRACEABILITY.read_text(encoding="utf-8")
    missing = [c["id"] for c in registry["contributions"] if c["id"] not in text]
    assert not missing, f"claim_traceability.md omits: {missing}"


def test_readiness_doc_matches_gate_status(registry: dict[str, Any]):
    text = READINESS.read_text(encoding="utf-8")
    for gate in registry["gates"]:
        assert gate["id"] in text, f"readiness doc omits gate {gate['id']}"
    blocked = [g for g in registry["gates"] if g["status"] == "blocked"]
    assert "BLOCKED" in text if blocked else True
