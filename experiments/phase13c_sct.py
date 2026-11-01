"""Backward-compatible launcher for the modular Phase 13C-SCT-V1 package.

Run explicitly with ``python -m experiments.phase13c_sct calibrate`` or
``python -m experiments.phase13c_sct confirm``. The pre-run implementation is
archived in the experiment report's source_snapshot directory.
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for _path in (ROOT, ROOT / "src"):
    if str(_path) not in sys.path:
        sys.path.insert(0, str(_path))

# Keep the previous import surface for tests and existing scripts while the
# implementation itself lives in small, responsibility-scoped modules.
from experiments.phase13c.common import (  # noqa: E402
    CONFIG_PATH,
    MC_SENSITIVITY,
    OUT_DIR,
    ROOT as PROJECT_ROOT,
    _config_digest,
    _quantile,
    clip01,
    load_config,
)
from experiments.phase13c.scoring import (  # noqa: E402
    _candidate_score,
    _eligible_pool,
    _gate_config,
)
from experiments.phase13c.tasking import (  # noqa: E402
    _enforce_opportunity_horizon,
    _is_eligible_opportunity,
    _macro_ops_for_signature,
    _opportunities,
    _task_batches,
)
from experiments.phase13c.evaluation import (  # noqa: E402
    _evaluate_memory_only,
    _evaluate_skill,
    _summarize_reuse,
)
from experiments.phase13c.calibration import (  # noqa: E402
    run_calibration,
    run_calibration_seed,
)
from experiments.phase13c.arms import (  # noqa: E402
    _candidate_arm_result,
    _clone_skill,
    _operation_for_skill,
)
from experiments.phase13c.lifecycle import _run_lifecycle  # noqa: E402
from experiments.phase13c.composition import _composition_eval  # noqa: E402
from experiments.phase13c.statistics import (  # noqa: E402
    _bootstrap_mean_ci,
    _correlation_report,
    _rank,
    _spearman,
)
from experiments.phase13c.confirmation_seed import run_confirmation_seed  # noqa: E402
from experiments.phase13c.reporting import (  # noqa: E402
    _render_summary,
    _write_csvs,
    run_confirmation,
)
from experiments.phase13c.cli import main  # noqa: E402

if __name__ == "__main__":
    main()
