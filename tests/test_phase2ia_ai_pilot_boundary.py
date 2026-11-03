from __future__ import annotations
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
PKG=ROOT/"reports/experiments/ASFT-V1.1-PHASE-2I-A-CANDIDATE-PRODUCTION-ENABLEMENT-V1"
PILOT=PKG/"wp3_ai_pilot_v1"
HEADER="# WP3-AI-PILOT — Exploratory Only"


def _sha(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def test_ai_pilot_is_separate_hash_pinned_and_never_eligible():
    pilot=json.loads((PILOT/"pilot_manifest.json").read_text())
    assert pilot["status"]=="EXPLORATORY_ONLY_NOT_WP3"
    assert pilot["wp3_status"].startswith("INCOMPLETE")
    assert pilot["modeling_boundary"].startswith("Pass A, Pass B, and adjudication were produced by the same AI assistant")
    assert all(value is False for value in pilot["use_restrictions"].values())
    source=PKG/"annotation_packets/annotator_A_train_only.jsonl"
    assert _sha(source)==pilot["sample"]["source_packet_sha256"]
    packet_manifest=json.loads((PKG/"annotation_packets/packet_manifest.json").read_text())
    assert pilot["sample"]["source_packet_rows"]==600
    ids=pilot["sample"]["task_ids"]
    rows=[json.loads(line) for line in source.read_text().splitlines()]
    byid={row["task_id"]:row for row in rows}
    assert len(ids)==12 and len(set(ids))==12
    assert set(ids)<=set(byid)
    for task_id in ids:
        row=byid[task_id]
        assert set(row)=={"task_id","train_pairs","annotation"}
        assert not row["annotation"]["primary_family"]
        assert all(set(pair)=={"input","output"} for pair in row["train_pairs"])
        assert pilot["sample"]["train_pair_sha256"][task_id]==packet_manifest["train_pair_hashes_sha256"][task_id]
    for name,expected in pilot["outputs_sha256"].items():
        path=PILOT/name
        assert _sha(path)==expected
        text=path.read_text()
        assert text.startswith(HEADER) or name=="README.md"
        assert "Not Independent Annotation" in text
    assert pilot["results"]["pass_a_pass_b_exact_agreement"]==4
    assert pilot["results"]["cohen_kappa_descriptive"]==0.232
    assert pilot["results"]["ai_adjudication_unknown_ambiguous"]==4
