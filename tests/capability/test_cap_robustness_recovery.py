"""plan/apply reduces fragmentation or restores declining."""

from capability.library import CapabilityLibrary
from capability.models import Capability
from capability.robustness.recovery import apply_recovery, plan_recovery
from capability.robustness.taxonomy import CapabilityFailureKind, FailureDiagnosis
from capability.states import CapabilityLifecycle
from invariants.robustness.escalation import FailureLevel


def test_plan_cf2_archives():
    action = plan_recovery(
        FailureDiagnosis(
            CapabilityFailureKind.CF2,
            FailureLevel.RESTRICTED,
            ["high_fragmentation_ratio"],
            {},
            ["tiny1"],
        )
    )
    assert action.action == "archive"


def test_apply_archive_reduces_active_caps():
    caps = CapabilityLibrary()
    for i in range(3):
        caps.add(
            Capability(
                capability_id=f"c{i}",
                skill_ids=[f"s{i}"],
                state=CapabilityLifecycle.DECLINING,
            )
        )
    action = plan_recovery(
        FailureDiagnosis(
            CapabilityFailureKind.CF2,
            FailureLevel.RESTRICTED,
            ["frag"],
            {},
            ["c0", "c1"],
        )
    )
    affected = apply_recovery(action, caps)
    assert "c0" in affected
    assert caps.get("c0").state is CapabilityLifecycle.ARCHIVED


def test_apply_restore_declining():
    caps = CapabilityLibrary()
    caps.add(
        Capability(
            capability_id="down",
            skill_ids=["s0"],
            state=CapabilityLifecycle.DECLINING,
            metadata={"dormant": True},
        )
    )
    action = plan_recovery(
        FailureDiagnosis(
            CapabilityFailureKind.CF6,
            FailureLevel.RESTRICTED,
            ["sustained_negative_cgr"],
            {},
            ["down"],
        )
    )
    affected = apply_recovery(action, caps)
    assert "down" in affected
    assert caps.get("down").state is CapabilityLifecycle.DEVELOPING
