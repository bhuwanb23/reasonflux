"""Trace Store — persist and retrieve reasoning traces."""


class TraceStore:
    """Storage and retrieval for ReasoningTrace records."""

    def save(self, *args, **kwargs):
        raise NotImplementedError("TraceStore.save is not implemented yet")

    def load(self, *args, **kwargs):
        raise NotImplementedError("TraceStore.load is not implemented yet")
