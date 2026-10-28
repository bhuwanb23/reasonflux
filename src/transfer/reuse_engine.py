"""Reuse engine — apply stored skills/invariants on new tasks."""


class ReuseEngine:
    """Apply prior skills to a new task and measure cost/accuracy change."""

    def apply(self, *args, **kwargs):
        raise NotImplementedError("ReuseEngine.apply is not implemented yet")
