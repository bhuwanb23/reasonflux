"""Skill Creation Trigger — decide create vs observe using SCV (SCT).

SCV = Reuse × AG × TS − CreationCost
Create if SCV > skill_creation_threshold.
"""


class SkillCreationTrigger:
    """Decide whether a skill candidate should be promoted."""

    def should_create(self, *args, **kwargs):
        raise NotImplementedError("SkillCreationTrigger.should_create is not implemented yet")

    def compute_scv(self, *args, **kwargs):
        raise NotImplementedError("SkillCreationTrigger.compute_scv is not implemented yet")
