"""Read-only submission-readiness checks for the Research Cycle 1 archive.

These tests answer the questions a reviewer or competition organizer is
likely to ask before accepting the package:

* Are the promised manuscript, figures, and writeup artifacts present and valid?
* Does the README/docs index link only to files that exist?
* Does every frozen claim still map to an evidence file and its recorded verdict?
* Are the headline numbers and the prior negative results still intact?
* Is the T2T/S3 provenance exclusion visible and internally consistent?

They deliberately do not run experiments or write into ``reports/``. A failing
test here means the submission package or its audit trail is inconsistent --
not that a scientific claim was re-evaluated.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PKG = ROOT / "submission_package"
ASSETS = PKG / "assets"
REPORTS = ROOT / "reports" / "experiments"
DOCS = ROOT / "docs"

LINK_RE = re.compile(r"\]\(([^)]+)\)")
BACKTICK_PATH_RE = re.compile(r"`([^`]+\.(?:pdf|docx|md|txt|png|jpg|jpeg|svg|json|csv))`")


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as stream:
        return list(csv.DictReader(stream))


def local_links(path: Path) -> list[str]:
    text = read_text(path)
    links = []
    for target in LINK_RE.findall(text):
        if target.startswith(("http://", "https://", "mailto:", "#")):
            continue
        links.append(target.split("#", 1)[0])
    return links


def unresolved_links(path: Path) -> list[str]:
    base = path.parent
    return [link for link in local_links(path) if not (base / link).exists()]


def exact_case_exists(base: Path, link: str) -> bool:
    """Case-sensitive existence check, so a Windows-only pass cannot hide a Linux break."""
    current = base
    for part in Path(link).parts:
        if part == "..":
            current = current.parent
            continue
        if part in (".", ""):
            continue
        try:
            entries = os.listdir(current)
        except OSError:
            return False
        if part not in entries:
            return False
        current = current / part
    return True


def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def matches_with_line_ending_provenance(path: Path, expected: str) -> bool:
    raw = path.read_bytes()
    if sha256_bytes(raw) == expected:
        return True
    return sha256_bytes(raw.replace(b"\n", b"\r\n")) == expected


# ---------------------------------------------------------------------------
# 1. Submission package integrity
# ---------------------------------------------------------------------------

REQUIRED_PACKAGE_FILES = [
    "paper.pdf",
    "visual_overview.pdf",
    "paper_editable.docx",
    "paper_source_v4.md",
    "UPLOAD_MANIFEST.md",
    "KAGGLE_WRITEUP_READY_TO_PASTE.md",
    "PROJECT_DESCRIPTION_PLAIN_TEXT.txt",
]

REQUIRED_ASSETS = [
    "kaggle_card_560x280.png",
    "hero_banner_1680x840.jpg",
    "claim_ladder.png",
    "disposition_map.png",
    "research_cycle_claim_audit_timeline.png",
    "research_cycle_claim_audit_timeline.svg",
    "scope_and_provenance.png",
]


def test_required_submission_files_exist_and_are_non_empty():
    for name in REQUIRED_PACKAGE_FILES:
        path = PKG / name
        assert path.is_file(), f"missing submission artifact: {name}"
        assert path.stat().st_size > 1_000, f"suspiciously small artifact: {name}"


def test_required_assets_exist_and_are_non_empty():
    for name in REQUIRED_ASSETS:
        path = ASSETS / name
        assert path.is_file(), f"missing asset: {name}"
        assert path.stat().st_size > 1_000, f"suspiciously small asset: {name}"


def test_binary_artifact_magic_bytes():
    assert (PKG / "paper.pdf").read_bytes()[:5] == b"%PDF-"
    assert (PKG / "visual_overview.pdf").read_bytes()[:5] == b"%PDF-"
    assert (PKG / "paper_editable.docx").read_bytes()[:2] == b"PK"
    assert (ASSETS / "kaggle_card_560x280.png").read_bytes()[:8] == b"\x89PNG\r\n\x1a\n"
    assert (ASSETS / "hero_banner_1680x840.jpg").read_bytes()[:2] == b"\xff\xd8"


def test_card_and_banner_have_exact_requested_dimensions():
    Image = pytest.importorskip("PIL.Image")
    with Image.open(ASSETS / "kaggle_card_560x280.png") as card:
        assert card.size == (560, 280)
    with Image.open(ASSETS / "hero_banner_1680x840.jpg") as banner:
        assert banner.size == (1680, 840)


def test_upload_manifest_paths_exist():
    manifest = read_text(PKG / "UPLOAD_MANIFEST.md")
    referenced = BACKTICK_PATH_RE.findall(manifest)
    assert referenced, "manifest does not reference any concrete artifacts"
    for name in referenced:
        assert (PKG / name).exists(), f"manifest references a missing file: {name}"


def test_writeup_asset_references_exist():
    writeup = read_text(PKG / "KAGGLE_WRITEUP_READY_TO_PASTE.md")
    referenced = sorted(set(re.findall(r"assets/[A-Za-z0-9_.-]+", writeup)))
    assert referenced, "writeup does not reference any assets"
    for name in referenced:
        assert (ASSETS / Path(name).name).is_file(), f"writeup references a missing asset: {name}"


def test_submission_package_is_under_upload_limit():
    total = sum(path.stat().st_size for path in PKG.rglob("*") if path.is_file())
    assert total < 100 * 1024 * 1024, f"package is {total / 1024 / 1024:.1f} MB"


def test_project_description_word_count_is_in_declared_range():
    text = read_text(PKG / "PROJECT_DESCRIPTION_PLAIN_TEXT.txt")
    description = text.split("PROJECT DESCRIPTION", 1)[1].split("\n\n", 1)[1]
    words = re.findall(r"\b[\w’'-]+\b", description)
    assert 250 <= len(words) <= 350, f"project description word count: {len(words)}"


# ---------------------------------------------------------------------------
# 2. Manuscript and paper-facing claims
# ---------------------------------------------------------------------------

def test_packaged_manuscript_matches_the_archived_source():
    archived = DOCS / "research_notes" / "arc_claim_evaluation_case_study_draft_v4.md"
    packaged = PKG / "paper_source_v4.md"
    assert archived.read_bytes() == packaged.read_bytes(), (
        "submission_package/paper_source_v4.md is out of sync with the archived v4 source"
    )


def test_manuscript_has_required_sections():
    paper = read_text(PKG / "paper_source_v4.md")
    for heading in (
        "### Abstract",
        "## 1. Introduction",
        "## 2. Scope and audit method",
        "## 3. Case findings through the claim ladder",
        "## 4. Lessons from the claim audit",
        "## 5. Conclusion",
        "## References",
    ):
        assert heading in paper, f"manuscript is missing section: {heading}"


def test_manuscript_does_not_print_excluded_s3_results():
    paper = read_text(PKG / "paper_source_v4.md")
    for forbidden in ("105/105", "N-FAIL", "Delta_N"):
        assert forbidden not in paper, (
            f"excluded S3 result leaked into the submission-facing paper: {forbidden}"
        )
    assert "T2T/S3 is excluded" in paper or "T2T/S3 is omitted" in paper
    assert "provenance" in paper.lower()


def test_manuscript_keeps_the_five_dispositions_distinct():
    paper = read_text(PKG / "paper_source_v4.md")
    for disposition in (
        "**PARTIAL SUPPORT**",
        "**MIXED**",
        "**UNVALIDATED CONSTRUCT**",
        "**NOT DEMONSTRATED**",
        "**TERMINATED AT P0**",
    ):
        assert disposition in paper, f"Table 1 disposition missing: {disposition}"


# ---------------------------------------------------------------------------
# 3. Claim-to-evidence index and documentation links
# ---------------------------------------------------------------------------

INDEX = DOCS / "04_paper" / "claim_evidence_index.md"


def test_claim_index_exists():
    assert INDEX.is_file()


def test_claim_index_links_resolve():
    missing = [link for link in local_links(INDEX) if not exact_case_exists(INDEX.parent, link)]
    assert not missing, f"claim index has broken links: {missing}"


@pytest.mark.parametrize(
    "path",
    [
        ROOT / "README.md",
        DOCS / "README.md",
        DOCS / "04_paper" / "claim_traceability.md",
    ],
)
def test_documentation_links_resolve(path):
    missing = [link for link in local_links(path) if not exact_case_exists(path.parent, link)]
    assert not missing, f"{path.relative_to(ROOT)} has broken links: {missing}"


def test_readme_links_the_claim_index_and_final_status():
    readme = read_text(ROOT / "README.md")
    assert "docs/04_paper/claim_evidence_index.md" in readme
    assert "All failed hypotheses" in readme
    assert "Research Cycle 1: CLOSED" in readme


def test_claim_index_covers_every_frozen_claim_id():
    index_text = read_text(INDEX)
    ids = set()
    ids.update(row["claim_id"] for row in csv_rows(REPORTS / "PHASE-13H-EVIDENCE-CONSOLIDATION-V1" / "claim_evidence_matrix.csv"))
    ids.update(
        row["claim_id"]
        for row in csv_rows(
            REPORTS / "PHASE-14J-FINAL-SCIENTIFIC-CONCLUSIONS-V1" / "final_claim_classification.csv"
        )
    )
    assert ids, "no claim IDs found in the frozen records"
    missing = [claim_id for claim_id in sorted(ids) if f"**{claim_id}**" not in index_text]
    assert not missing, f"claim index is missing frozen claim IDs: {missing}"


@pytest.mark.parametrize(
    "claim_id",
    ["IDT-2", "IDT-3", "SCT-3", "CGM-3", "CHAIN-2", "CHAIN-3", "CHAIN-4", "BASE-1", "ARC-1"],
)
def test_failed_claims_are_not_upgraded_in_the_index(claim_id):
    index_text = read_text(INDEX)
    rows = [line for line in index_text.splitlines() if f"| **{claim_id}** |" in line]
    assert len(rows) == 1, f"expected exactly one index row for {claim_id}"
    assert "❌" in rows[0], f"{claim_id} must remain a failed/not-established disposition"


# ---------------------------------------------------------------------------
# 4. Frozen numbers and negative evidence
# ---------------------------------------------------------------------------

@pytest.mark.parametrize(
    ("relative_path", "needles"),
    [
        ("idt_evidence/summary.md", ["0.095809", "0.063113"]),
        ("PHASE-13C-SCT-V1/evidence_package.md", ["44/44", "0.345", "1.325", "0.700"]),
        ("PHASE-13H-EVIDENCE-CONSOLIDATION-V1/package_F_ARC.md", ["3/600", "5/200", "2/200", "1/200"]),
        ("PHASE-13E-CAP-GROWTH-V1/evidence_package.md", ["0.2946", "-0.0039"]),
        ("PHASE-13H-EVIDENCE-CONSOLIDATION-V1/package_A_IDT.md", ["-0.0424"]),
        ("PHASE-13H-EVIDENCE-CONSOLIDATION-V1/package_C_CGM.md", ["-0.503", "-0.1429", "-0.0361"]),
    ],
)
def test_headline_numbers_remain_in_the_evidence(relative_path, needles):
    path = REPORTS / relative_path
    assert path.is_file(), f"missing evidence file: {path}"
    text = read_text(path)
    for needle in needles:
        assert needle in text, f"{needle!r} missing from {path.relative_to(ROOT)}"


def test_negative_evidence_register_is_complete():
    rows = csv_rows(
        REPORTS / "PHASE-13H-EVIDENCE-CONSOLIDATION-V1" / "negative_evidence_register.csv"
    )
    assert len(rows) == 20
    assert [row["id"] for row in rows] == [f"NEG-{i:02d}" for i in range(1, 21)]
    assert all(row["status"] for row in rows)
    by_id = {row["id"]: row for row in rows}
    assert by_id["NEG-01"]["status"] == "failed_primary_gate"
    assert by_id["NEG-03"]["status"] == "failed_superiority"
    assert by_id["NEG-17"]["status"] == "low_adapter_coverage"


def test_final_scorecard_keeps_failed_areas_failed():
    rows = {
        row["area"]: row
        for row in csv_rows(
            REPORTS / "PHASE-14J-FINAL-SCIENTIFIC-CONCLUSIONS-V1" / "final_scientific_scorecard.csv"
        )
    }
    assert len(rows) == 15
    expected = {
        "Transfer-aware ranking superiority": "Primary gate failed",
        "SCT / SCV policy superiority": "Not demonstrated",
        "ARC mechanism validation": "Not demonstrated",
        "Full ASFT causal chain": "Not validated end to end",
        "Intelligence-growth interpretation": "Not established",
    }
    for area, verdict in expected.items():
        assert area in rows, f"scorecard lost area: {area}"
        assert rows[area]["verdict"] == verdict, (
            f"scorecard verdict changed for {area}: {rows[area]['verdict']!r}"
        )


# ---------------------------------------------------------------------------
# 5. Provenance, exclusions, and cycle closure
# ---------------------------------------------------------------------------

def test_s3_provenance_discrepancy_is_documented_and_excluded():
    execution = json.loads(
        read_text(REPORTS / "T2T-S3-EXEC-2026-11-05-001" / "s3_execution_record.json")
    )
    assert execution["completed_at"].startswith("2026-11-05")
    assert execution["run_status"] == "COMPLETED"

    paper = read_text(PKG / "paper_source_v4.md")
    assert "105/105" not in paper
    assert "2026-10-28" in paper
    assert "2026-11-05" in paper or "completion timestamp" in paper

    reconciliation = DOCS / "research_notes" / "s3_provenance_date_reconciliation.md"
    text = read_text(reconciliation)
    assert "unresolved" in text.lower()
    assert "excluded" in text.lower()
    assert "Do not edit its timestamp" in text


def test_claim_n_archive_records_the_frozen_failure():
    decision = read_text(REPORTS / "T2T-S3-EXEC-2026-11-05-001" / "claim_n_decision.md")
    assert "N-FAIL" in decision
    assert "105/105" in decision
    archive = read_text(DOCS / "05_trace_to_transfer" / "claim_n_archive.md")
    assert "CLOSED" in archive and "FAILED (decision-grade predictive endpoint)" in archive
    assert "Delta_N = 0.0" in archive
    assert "No S3 rerun" in archive


def test_bl1_was_terminated_before_implementation():
    review = read_text(
        DOCS / "05_trace_to_transfer" / "bl1" / "boundary_prior_art_review.md"
    )
    assert "terminate BL1 at P0" in review
    assert "No implementation, context generation, model fitting, or experiment has occurred" in review
    assert not list(REPORTS.glob("BL1*")), "BL1 must not have an experiment package"


def test_research_cycle_closure_is_explicit():
    closure = read_text(DOCS / "research_notes" / "research_cycle_1_closure.md")
    assert "ASFT v1 | **CLOSED**" in closure
    assert "T2T Claim N | **CLOSED**" in closure
    assert "decision-grade N-FAIL" in closure
    assert "BL1 | **TERMINATED AT P0**" in closure
    assert "no active research program" in closure.lower()
    assert "observation mode only" in closure.lower()


# ---------------------------------------------------------------------------
# 6. Byte-level evidence integrity
# ---------------------------------------------------------------------------

ANNOTATION_PACKETS = (
    REPORTS
    / "ASFT-V1.1-PHASE-2I-A-CANDIDATE-PRODUCTION-ENABLEMENT-V1"
    / "annotation_packets"
)


def test_annotation_packets_verify_byte_exactly():
    manifest = json.loads(read_text(ANNOTATION_PACKETS / "packet_manifest.json"))
    assert manifest["packet_sha256"], "packet manifest has no hashes"
    for name, expected in manifest["packet_sha256"].items():
        path = ANNOTATION_PACKETS / name
        assert path.is_file(), f"missing annotation packet: {name}"
        assert sha256_bytes(path.read_bytes()) == expected, (
            f"annotation packet hash mismatch (must be LF-exact): {name}"
        )


def test_phase13h_source_manifest_matches_with_documented_encoding():
    manifest = json.loads(
        read_text(REPORTS / "PHASE-13H-EVIDENCE-CONSOLIDATION-V1" / "source_manifest.json")
    )
    assert manifest["hash_algorithm"] == "SHA-256"
    assert len(manifest["sources"]) == manifest["source_count"]
    unexplained = []
    crlf_derived = []
    for source in manifest["sources"]:
        path = ROOT / source["path"]
        if not path.is_file():
            unexplained.append(f"missing: {source['path']}")
        elif not matches_with_line_ending_provenance(path, source["sha256"]):
            unexplained.append(f"content mismatch: {source['path']}")
        elif sha256_bytes(path.read_bytes()) != source["sha256"]:
            crlf_derived.append(source["path"])
    assert not unexplained, f"unexplained Phase 13H integrity failures: {unexplained}"
    assert len(crlf_derived) == 3, (
        f"expected 3 CRLF-derived Phase 13H digests, found {len(crlf_derived)}; "
        "update docs/research_notes/encoding_provenance.md if this changed"
    )


def test_phase14j_source_hashes_match_with_documented_encoding():
    rows = csv_rows(
        REPORTS / "PHASE-14J-FINAL-SCIENTIFIC-CONCLUSIONS-V1" / "source_hashes.csv"
    )
    assert len(rows) == 95
    unexplained = []
    crlf_derived = []
    for row in rows:
        path = ROOT / row["path"]
        if not path.is_file():
            unexplained.append(f"missing: {row['path']}")
        elif not matches_with_line_ending_provenance(path, row["sha256"]):
            unexplained.append(f"content mismatch: {row['path']}")
        elif sha256_bytes(path.read_bytes()) != row["sha256"]:
            crlf_derived.append(row["path"])
    assert not unexplained, f"unexplained Phase 14J integrity failures: {unexplained}"
    assert len(crlf_derived) == 16, (
        f"expected 16 CRLF-derived Phase 14J digests, found {len(crlf_derived)}; "
        "update docs/research_notes/encoding_provenance.md if this changed"
    )


def test_encoding_provenance_note_is_linked_and_complete():
    note = DOCS / "research_notes" / "encoding_provenance.md"
    assert note.is_file()
    text = read_text(note)
    assert ".gitattributes" in text
    assert "CRLF" in text and "SHA-256" in text
    assert "Phase 13H" in text and "Phase 14J" in text
    assert not [link for link in local_links(note) if not exact_case_exists(note.parent, link)]


def test_writeup_and_project_description_do_not_leak_s3_results():
    for name in (
        "KAGGLE_WRITEUP_READY_TO_PASTE.md",
        "PROJECT_DESCRIPTION_PLAIN_TEXT.txt",
    ):
        text = read_text(PKG / name)
        for forbidden in ("105/105", "N-FAIL", "Delta_N"):
            assert forbidden not in text, f"excluded S3 detail leaked into {name}: {forbidden}"
        assert "T2T/S3" in text or "T2T" in text
