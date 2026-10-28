"""Track transfer effects over sequences of tasks."""


class TransferTracker:
    """Record before/after performance for transfer scoring."""

    def record(self, *args, **kwargs):
        raise NotImplementedError("TransferTracker.record is not implemented yet")

    def summary(self, *args, **kwargs):
        raise NotImplementedError("TransferTracker.summary is not implemented yet")
