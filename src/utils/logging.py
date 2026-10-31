"""Project logging helpers.

Idempotent by design: calling ``get_logger`` twice for the same name must not
stack handlers (a classic cause of duplicated log lines in pipelines).
"""

from __future__ import annotations

import logging
import os

_HANDLER_TAG = "_asft_handler"
_DEFAULT_FORMAT = "%(asctime)s %(levelname)-7s %(name)s | %(message)s"


def get_logger(name: str = "asft") -> logging.Logger:
    """Return a configured logger for ``name``."""
    logger = logging.getLogger(name)
    level_name = os.environ.get("ASFT_LOG_LEVEL", "INFO").upper()
    logger.setLevel(getattr(logging, level_name, logging.INFO))
    if not any(getattr(h, _HANDLER_TAG, False) for h in logger.handlers):
        handler = logging.StreamHandler()
        handler.setFormatter(logging.Formatter(_DEFAULT_FORMAT))
        setattr(handler, _HANDLER_TAG, True)
        logger.addHandler(handler)
    # Pipelines own their handlers; don't double-log through the root logger.
    logger.propagate = False
    return logger
