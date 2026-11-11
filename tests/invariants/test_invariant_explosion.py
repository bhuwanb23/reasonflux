"""F2 invariant explosion IER."""

from invariants.robustness import ier_level, monitor_ier, should_restrict_promotion


def test_ier_warn_and_restrict():
    assert ier_level(1.5) == "warn"
    assert ier_level(4.0) == "restrict"
    assert not should_restrict_promotion(1.5)
    assert should_restrict_promotion(4.0)


def test_monitor_ier_payload():
    out = monitor_ier(300, 100)
    assert out["ier"] == 3.0
    assert out["level"] == "restrict"
