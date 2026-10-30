"""Claim mapping and audit gate."""

from evaluation.harness.evidence import gate_run, map_claims
from evaluation.harness.runner import run_benchmark


def test_map_claims_and_gate():
    run = run_benchmark("capability")
    claims = map_claims(run)
    assert len(claims) >= 4
    assert any(c.metric == "cgr" for c in claims)
    ok, kinds = gate_run(run)
    assert isinstance(ok, bool)
    assert isinstance(kinds, list)
