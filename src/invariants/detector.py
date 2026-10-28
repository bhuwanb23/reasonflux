"""Invariant Detector — end-to-end IDT entry point.

Input: collection of ReasoningTrace
Output: ranked Invariant list
"""


class InvariantDetector:
    """Discover invariants from reasoning traces."""

    def detect(self, *args, **kwargs):
        raise NotImplementedError("InvariantDetector.detect is not implemented yet")
