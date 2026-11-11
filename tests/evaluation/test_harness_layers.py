"""Layer evaluators on synthetic libraries."""

from evaluation.harness.layers import (
    evaluate_capability_layer,
    evaluate_intelligence_layer,
    evaluate_invariant_layer,
    evaluate_skill_layer,
    evaluate_transfer_layer,
)
from evaluation.harness.scenarios import scenario_skill_formation


def test_layers_return_expected_keys():
    steps = scenario_skill_formation()
    final = steps[-1]
    inv = evaluate_invariant_layer(final.skills)
    skill = evaluate_skill_layer(final.skills)
    xfer = evaluate_transfer_layer(final.skills)
    assert inv.layer == "invariant" and "is_proxy" in inv.metrics
    assert skill.layer == "skill" and "mean_su" in skill.metrics
    assert xfer.layer == "transfer" and "ntr" in xfer.metrics
    assert inv.passed and skill.passed and xfer.passed

    prev = None
    for i, step in enumerate(steps):
        cap = evaluate_capability_layer(
            step.capabilities,
            step.skills,
            previous_score=prev,
        )
        prev = cap.metrics["capability_score"]
    assert cap.passed
    assert "cgr" in cap.metrics

    intel = evaluate_intelligence_layer(
        final.capabilities,
        final.skills,
        previous_ig=0.0,
        previous_score=0.0,
        experiences=10,
    )
    assert intel.layer == "intelligence"
    assert "ig" in intel.metrics
