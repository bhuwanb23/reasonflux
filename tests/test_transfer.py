"""Smoke / package export tests for transfer (Phase 11C-4)."""

from pathlib import Path

from transfer import (
    TransferConfig,
    TransferGraph,
    TransferMemory,
    TransferTracker,
    TransferType,
    classify_transfer,
    map_related_tasks,
)
from utils.config import load_transfer_config


def test_transfer_package_exports():
    assert TransferType.NEAR.value == "near"
    assert callable(classify_transfer)
    assert callable(map_related_tasks)
    assert TransferMemory is not None
    assert TransferGraph is not None
    assert TransferTracker is not None


def test_load_transfer_config_from_repo():
    cfg = load_transfer_config(Path("configs"))
    assert isinstance(cfg, TransferConfig)
    assert cfg.min_transfer_attempts == 2
    assert cfg.min_its == 0.5
    assert cfg.ntr_limit == 0.3
