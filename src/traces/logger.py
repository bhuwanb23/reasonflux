"""Trace Logger — capture reasoning traces during task solving.

Contribution support: IDT.
"""


class TraceLogger:
    """Capture solver steps into a ReasoningTrace."""

    def log(self, *args, **kwargs):
        raise NotImplementedError("TraceLogger.log is implemented in a later Phase 11 module")
