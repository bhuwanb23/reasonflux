"""Tests for Phase 11B-3 interface contracts (structural Protocol typing)."""

from core import (
    Invariant,
    InvariantState,
    PromotedSkillProvider,
    Skill,
    SkillState,
    SkillUsageStats,
    SkillUsageStatsProvider,
    TraceBatchProvider,
    ValidatedInvariantProvider,
    ReasoningTrace,
)


class FakeTraceProvider:
    def get_traces(self) -> list[ReasoningTrace]:
        return [
            ReasoningTrace(trace_id="tr1", task_id="t1", timestamp=1.0),
        ]


class FakeInvariantProvider:
    def get_validated_invariants(self) -> list[Invariant]:
        return [
            Invariant(
                invariant_id="INV-1",
                pattern_signature=["reflect"],
                state=InvariantState.VALIDATED,
            )
        ]


class FakeSkillProvider:
    def get_promoted_skills(self) -> list[Skill]:
        return [Skill(skill_id="SK-1", state=SkillState.PROMOTED)]


class FakeStatsProvider:
    def get_usage_stats(self) -> list[SkillUsageStats]:
        return [SkillUsageStats(skill_id="SK-1", reuse_count=3, transfer_score=0.5)]


def test_trace_batch_provider_protocol():
    provider: TraceBatchProvider = FakeTraceProvider()
    traces = provider.get_traces()
    assert isinstance(provider, TraceBatchProvider)
    assert len(traces) == 1
    assert traces[0].trace_id == "tr1"


def test_validated_invariant_provider_protocol():
    provider: ValidatedInvariantProvider = FakeInvariantProvider()
    invs = provider.get_validated_invariants()
    assert isinstance(provider, ValidatedInvariantProvider)
    assert invs[0].state == InvariantState.VALIDATED


def test_promoted_skill_and_stats_protocols():
    skills: PromotedSkillProvider = FakeSkillProvider()
    stats: SkillUsageStatsProvider = FakeStatsProvider()
    assert isinstance(skills, PromotedSkillProvider)
    assert isinstance(stats, SkillUsageStatsProvider)
    assert skills.get_promoted_skills()[0].skill_id == "SK-1"
    assert stats.get_usage_stats()[0].reuse_count == 3


def test_skill_usage_stats_round_trip():
    stats = SkillUsageStats(skill_id="SK-1", reuse_count=2, utility=0.8)
    restored = SkillUsageStats.from_dict(stats.to_dict())
    assert restored.skill_id == "SK-1"
    assert restored.utility == 0.8
