"""Trace logging, normalization, and segmentation — supports IDT."""

from traces.normalizer import (
    DEFAULT_SYNONYM_MAP,
    NormalizedTrace,
    canonicalize_operation,
    normalize_lookup_key,
    normalize_trace,
    normalize_traces,
)
from traces.segmentation import TraceFragment, segment_trace, segment_traces

__all__ = [
    "DEFAULT_SYNONYM_MAP",
    "NormalizedTrace",
    "TraceFragment",
    "canonicalize_operation",
    "normalize_lookup_key",
    "normalize_trace",
    "normalize_traces",
    "segment_trace",
    "segment_traces",
]
