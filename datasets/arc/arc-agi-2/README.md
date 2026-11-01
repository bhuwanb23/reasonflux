# ARC-AGI-2 Phase 13G data snapshot

Source: ARC Prize Foundation, https://github.com/arcprize/ARC-AGI-2, pinned commit `f3283f727488ad98fe575ea6a5ac981e4a188e49`. This directory contains only the upstream public `data/training` task JSONs, plus upstream license/readme/training ID list and hash manifests. Dataset terms: Apache License 2.0; see `LICENSE`.

The 1,000 task IDs are partitioned into discovery (600), transfer (200), and final holdout (200) by the fixed SHA-256 ranking in `split_manifest.json`. Do not use any other split. A pre-run schema audit decoded these 1,000 training JSONs, including eventual holdout, only for grid rectangularity/color-domain checks; it did not compare input/output transformations or score outcomes. In the analytic runner, holdout JSONs are loaded after the pre-holdout model lock. No official evaluation JSON was extracted, parsed, scored, or used as feedback. A temporary upstream archive that included evaluation blobs was downloaded during source discovery; only its filename listing was queried, and it was deleted without extracting or reading those JSON files. This transport deviation is disclosed in the preregistration and run report.

Attribution: ARC-AGI-2 task data © ARC Prize Foundation. Preserve the upstream `LICENSE`, `UPSTREAM_README.md`, pinned source commit, and per-file hashes when copying or redistributing.
