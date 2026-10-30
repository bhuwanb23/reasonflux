"""CF enum / diagnosis round-trip."""

from capability.robustness.taxonomy import (
    CapabilityFailureKind,
    FailureDiagnosis,
    kind_from_legacy,
)
from invariants.robustness.escalation import FailureLevel


def test_cf_enum_values():
    assert CapabilityFailureKind.CF1.value.startswith("cf1_")
    assert len(CapabilityFailureKind) == 10


def test_diagnosis_to_dict_round_trip():
    d = FailureDiagnosis(
        CapabilityFailureKind.CF2,
        FailureLevel.RESTRICTED,
        ["high_fragmentation_ratio"],
        {"fr": 0.9},
        ["c1"],
    )
    payload = d.to_dict()
    assert payload["kind"] == "cf2_fragmentation"
    assert payload["level"] == "restricted"
    assert payload["capability_ids"] == ["c1"]
    assert payload["metrics"]["fr"] == 0.9


def test_kind_from_legacy_mapping():
    assert kind_from_legacy("skill_count_illusion") is CapabilityFailureKind.CF1
    assert kind_from_legacy("fragmentation") is CapabilityFailureKind.CF2
    assert kind_from_legacy("metric_gaming") is CapabilityFailureKind.CF7
    assert kind_from_legacy("unknown_xyz") is None
