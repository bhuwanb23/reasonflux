"""QA/provenance finalizer for the Phase 2I-A engineering work package only.

It runs R3 unit/contract tests on synthetic fixtures, checks package artifacts,
and records source hashes. It never runs an ARC task or empirical Phase 2I/HCC
experiment.
"""
from __future__ import annotations
import csv, hashlib, json, re, os, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
PKG=ROOT/"reports/experiments/ASFT-V1.1-PHASE-2I-A-CANDIDATE-PRODUCTION-ENABLEMENT-V1"
ARTIFACTS=["README.md","implementation_work_package.md","wp0_wp6_end_to_end_summary.md","r3_grammar_addendum_v1.md",
 "r3_implementation_contract.md","semantic_trace_adapter_contract.md","family_annotation_protocol.md",
 "task_breakdown.csv","ambiguity_register.csv","wp4_policy_identity_resolution.md",
 "wp4_runtime_config_v1.json","package_manifest.json",
 "annotation_packets/annotator_A_train_only.jsonl","annotation_packets/annotator_B_train_only.jsonl",
 "annotation_packets/packet_manifest.json",
 "wp3_ai_pilot_v1/README.md","wp3_ai_pilot_v1/prompt_specification.md","wp3_ai_pilot_v1/pass_A.md",
 "wp3_ai_pilot_v1/pass_B.md","wp3_ai_pilot_v1/ai_adjudication.md","wp3_ai_pilot_v1/agreement_report.md",
 "wp3_ai_pilot_v1/pilot_manifest.json",
 "wp3_provisional_v1/README.md","wp3_provisional_v1/annotator_A_labels.csv","wp3_provisional_v1/annotator_B_labels.csv",
 "wp3_provisional_v1/adjudication_log.csv","wp3_provisional_v1/agreement_report.md",
 "wp3_provisional_v1/confusion_matrix.csv","wp3_provisional_v1/task_family_map.csv",
 "wp3_provisional_v1/family_map_hash.txt","wp3_provisional_v1/wp3_completion_review.md",
 "wp3_provisional_v1/provisional_manifest.json",
 "wp3_provisional_v1/reviewer_A_packet.jsonl","wp3_provisional_v1/reviewer_B_packet.jsonl",
 "wp3_provisional_v1/reviewer_C_packet.jsonl","wp3_provisional_v1/disagreement_priority_queue.csv",
 "wp3_provisional_v1/review_packet_manifest.json"]
SOURCES=[
 "experiments/phase2ia/finalize_package.py",
 "reports/experiments/ASFT-V1.1-PHASE-2I-INVARIANT-CANDIDATE-PRODUCTION-V1/candidate_production_protocol.md",
 "reports/experiments/ASFT-V1.1-PHASE-2I-INVARIANT-CANDIDATE-PRODUCTION-V1/candidate_eligibility_contract.md",
 "reports/experiments/ASFT-V1.1-PHASE-2I-INVARIANT-CANDIDATE-PRODUCTION-V1/representation_and_trace_plan.md",
 "reports/experiments/ASFT-V1.1-PHASE-2F-REPRESENTATION-ALTERNATIVES-V1/representation_registry.csv",
 "reports/experiments/ASFT-V1.1-PHASE-2F-REPRESENTATION-ALTERNATIVES-V1/phase2F_framework_config.json",
 "src/invariants/specification/policy.py",
 "src/invariants/specification/rejection.py",
 "src/invariants/specification/identity.py",
 "src/invariants/specification/qualification.py",
 "src/invariants/specification/taxonomy.py",
 "src/invariants/candidate_generation.py",
 "src/invariants/detector.py",
 "src/invariants/pattern_mining.py",
 "experiments/phase2e/invariant_audit.py",
 "experiments/phase2e/preregistration.md",
 "src/traces/normalizer.py",
 "src/traces/segmentation.py",
 "src/representations/__init__.py",
 "src/representations/r3.py",
 "src/traces/semantic_adapter.py",
 "tests/test_r3_representation.py",
 "tests/test_semantic_adapter.py",
 "experiments/phase2ia/build_annotation_packets.py",
 "experiments/phase2ia/runtime_config.py",
 "experiments/phase2ia/hcc_control.py",
 "experiments/phase2ia/runner.py",
 "experiments/phase2ia/search_adapters.py",
 "experiments/phase2ia/train_only_source.py",
 "experiments/phase13g/common.py",
 "tests/test_phase2ia_hcc_control.py",
 "tests/test_phase2ia_runner.py",
 "tests/test_phase2ia_train_only_source.py",
 "tests/test_phase2ia_ai_pilot_boundary.py",
 "tests/test_train_only_annotation_packets.py",
 "tests/test_phase2ia_runtime_config.py",
 "datasets/arc/arc-agi-2/split_manifest.json",
]
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    missing=[n for n in ARTIFACTS if not (PKG/n).is_file() or not (PKG/n).stat().st_size]
    if missing: raise SystemExit(f"missing package artifacts: {missing}")
    tasks=list(csv.DictReader((PKG/"task_breakdown.csv").open(newline="")))
    issues=list(csv.DictReader((PKG/"ambiguity_register.csv").open(newline="")))
    assert [r["work_id"] for r in tasks]==[f"WP{i}" for i in range(8)]
    assert len(issues)==12
    assert all(r["empirical_arc_run"] in {"NO","NOT PART OF THIS WORK PACKAGE"} for r in tasks)
    assert all(next(r for r in issues if r["issue_id"]==i)["gate_status"]=="RESOLVED_WP0_V1" for i in ("A01","A02","A03","A04"))
    assert next(r for r in issues if r["issue_id"]=="A06")["gate_status"]=="RESOLVED_WP2_WP4_V1"
    assert all(next(r for r in issues if r["issue_id"]==i)["gate_status"]=="RESOLVED_WP4_V1" for i in ("A07","A08","A09"))
    assert next(r for r in issues if r["issue_id"]=="A10")["gate_status"]=="DECIDED_BUILD"
    addendum=(PKG/"r3_grammar_addendum_v1.md").read_text().lower()
    assert "owner approved" in addendum and "frozen for wp1 implementation" in addendum
    assert all(r["gate_status"]=="RESOLVED_WP0_V1" for r in issues if r["issue_id"] in {"A01","A02","A03","A04"})
    text=(PKG/"implementation_work_package.md").read_text().lower()
    for token in ("not authorized", "phase 1c", "phase 3a-r", "hcc", "no generated arc artifact", "derived/predicted test outputs", "forbidden-sentinel rejection test"):  
        if token not in text: raise SystemExit(f"work package missing scope token: {token}")
    link_re=re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    broken=[]
    for md in PKG.glob("*.md"):
      for target in link_re.findall(md.read_text()):
        if target.startswith(("http://","https://","mailto:","#")): continue
        if not (md.parent/target.split("#",1)[0]).exists(): broken.append(f"{md.name}: {target}")
    if broken: raise SystemExit(f"broken local links: {broken}")
    packet_manifest=json.loads((PKG/"annotation_packets/packet_manifest.json").read_text())
    if packet_manifest.get("task_count")!=600 or packet_manifest.get("included_split")!="discovery only":
      raise SystemExit("annotation packet must contain exactly the 600 discovery tasks")
    if "NOT DECODED" not in packet_manifest.get("test_data_access",""):
      raise SystemExit("packet manifest does not attest train-only extraction")
    wp4_config=json.loads((PKG/"wp4_runtime_config_v1.json").read_text())
    if wp4_config.get("status")!="OWNER_APPROVED_FROZEN":
      raise SystemExit("WP4 config must remain owner-approved and frozen")
    if wp4_config["trace_mining"]!={"min_frequency":5,"min_cross_trace":5,"max_fragment_length":4,"min_core_length":1,"successful_trace_bias":True}:
      raise SystemExit("WP4 config deviates from audited Phase 2E/2F mining settings")
    if wp4_config["candidate_policy"]["min_consistency"]!=1.0 or wp4_config["candidate_policy"]["min_task_families"]!=2:
      raise SystemExit("WP4 candidate floors mismatch")
    for packet_name,expected_hash in packet_manifest["packet_sha256"].items():
      packet_path=PKG/"annotation_packets"/packet_name
      if hashlib.sha256(packet_path.read_bytes()).hexdigest()!=expected_hash:
        raise SystemExit(f"annotation packet hash mismatch: {packet_name}")
      rows=[json.loads(line) for line in packet_path.read_text().splitlines()]
      if len(rows)!=600: raise SystemExit(f"annotation packet row count mismatch: {packet_name}")
      for row in rows:
        if set(row)!={"task_id","train_pairs","annotation"}: raise SystemExit("forbidden annotation packet fields")
        if any(set(pair)!={"input","output"} for pair in row["train_pairs"]): raise SystemExit("non-train pair in annotation packet")
        if row["annotation"].get("primary_family") or row["annotation"].get("rationale"):
          raise SystemExit("family labels must remain blank until independent coding")
    pilot_manifest=json.loads((PKG/"wp3_ai_pilot_v1/pilot_manifest.json").read_text())
    if pilot_manifest.get("status")!="EXPLORATORY_ONLY_NOT_WP3" or pilot_manifest.get("wp3_status","").startswith("COMPLETE"):
      raise SystemExit("AI annotation pilot must remain non-qualifying; WP3 labels stay pending")
    if any(pilot_manifest.get("use_restrictions",{}).get(k) is not False for k in
      ("independent_annotation","family_qualification","candidate_eligibility","phase2i_execution","phase3_claims_or_inputs","wp3_completion","freeze_as_label_map")):
      raise SystemExit("AI pilot use restrictions must all remain false")
    source_packet=PKG/"annotation_packets/annotator_A_train_only.jsonl"
    if pilot_manifest["sample"]["source_packet_sha256"]!=digest(source_packet) or pilot_manifest["sample"]["source_packet_rows"]!=600:
      raise SystemExit("AI pilot source must be the 600-row train-only packet")
    pilot_header="WP3-AI-PILOT — Exploratory Only"
    for name,expected in pilot_manifest["outputs_sha256"].items():
      pilot_path=PKG/"wp3_ai_pilot_v1"/name
      if digest(pilot_path)!=expected or pilot_header not in pilot_path.read_text():
        raise SystemExit(f"AI pilot artifact hash/header mismatch: {name}")
    if pilot_manifest["results"]["n"]!=12 or pilot_manifest["results"]["pass_a_pass_b_exact_agreement"]!=4:
      raise SystemExit("unexpected AI pilot sample/report state")
    provisional_manifest=json.loads((PKG/"wp3_provisional_v1/provisional_manifest.json").read_text())
    if provisional_manifest.get("status")!="AI_PROVISIONAL_ONLY_NOT_WP3" or not provisional_manifest.get("wp3_status","").startswith("INCOMPLETE"):
      raise SystemExit("provisional WP3 bundle must remain non-qualifying; WP3 labels stay pending")
    if any(value is not False for value in provisional_manifest.get("use_restrictions",{}).values()):
      raise SystemExit("provisional WP3 use restrictions must all remain false")
    if provisional_manifest["source_packet_sha256"]!=digest(source_packet) or provisional_manifest["task_count"]!=600:
      raise SystemExit("provisional WP3 bundle must derive from the 600-row train-only packet")
    provisional_header="AI_PROVISIONAL — NOT HUMAN ANNOTATION — NOT WP3-ELIGIBLE"
    labelled_csvs={"annotator_A_labels.csv","annotator_B_labels.csv","adjudication_log.csv","task_family_map.csv"}
    for name,expected in provisional_manifest["outputs_sha256"].items():
      provisional_path=PKG/"wp3_provisional_v1"/name
      if digest(provisional_path)!=expected:
        raise SystemExit(f"provisional WP3 artifact hash mismatch: {name}")
      if name.endswith(".md") and provisional_header not in provisional_path.read_text():
        raise SystemExit(f"provisional WP3 report missing non-eligibility header: {name}")
      if name in labelled_csvs:
        header=provisional_path.read_text().splitlines()[0]
        if "label_mode" not in header:
          raise SystemExit(f"provisional WP3 label CSV must carry a label_mode column: {name}")
        if not all("AI_PROVISIONAL" in line for line in provisional_path.read_text().splitlines()[1:]):
          raise SystemExit(f"provisional WP3 label CSV has a row without AI_PROVISIONAL mode: {name}")
    if provisional_manifest["data_access"]["test_fields_or_outputs_accessed"] is not False:
      raise SystemExit("provisional WP3 bundle must not access test fields")
    schema=provisional_manifest.get("human_review_schema",{})
    if schema.get("reviews_present")!=0: raise SystemExit("provisional WP3 bundle must ship with zero human reviews")
    if not schema.get("promotion_blockers"): raise SystemExit("provisional WP3 bundle must record promotion blockers")
    packets=provisional_manifest.get("review_packets",{})
    if packets.get("review_fields_prefilled") is not False:
      raise SystemExit("provisional WP3 review packets must ship unlabelled")
    if sum(packets.get("queue_counts",{}).values())!=600:
      raise SystemExit("provisional WP3 priority queue must cover all 600 tasks")
    for name in ("reviewer_A_packet.jsonl","reviewer_B_packet.jsonl","reviewer_C_packet.jsonl"):
      packet_path=PKG/"wp3_provisional_v1"/name
      if digest(packet_path)!=packets["packet_sha256"][name]:
        raise SystemExit(f"review packet hash mismatch: {name}")
      for line in packet_path.read_text().splitlines():
        row=json.loads(line)
        if any(value for value in row.values() if isinstance(value,str) and "HIDDEN_TEST" in value):
          raise SystemExit(f"review packet leaked test sentinel: {name}")
        if set(row)&{"test","test_output","solver_program","trace","candidate_yield"}:
          raise SystemExit(f"review packet leaked prohibited field: {name}")
        for field in ("review_decision","reviewer_id","reviewed_at_utc","sign_off_sha256"):
          if row.get(field): raise SystemExit(f"review packet must not prefill {field}: {name}")
    coder_packet=(PKG/"wp3_provisional_v1/reviewer_A_packet.jsonl").read_text().splitlines()[0]
    if "coder_b_family" in coder_packet or "ai_draft_family" not in coder_packet:
      raise SystemExit("coder A packet must expose only coder A's draft")
    env=os.environ.copy()
    env["PYTHONPATH"]=str(ROOT/"src")+os.pathsep+env.get("PYTHONPATH","")
    r3_run=subprocess.run([sys.executable,"-m","pytest","-q","tests/test_r3_representation.py"],cwd=ROOT,env=env,
      text=True,capture_output=True)
    if r3_run.returncode:
      raise SystemExit("R3 contract tests failed:\\n"+r3_run.stdout+r3_run.stderr)
    r3_summary=r3_run.stdout.strip().splitlines()[-1]
    if "11 passed" not in r3_summary:
      raise SystemExit(f"unexpected R3 test summary: {r3_summary}")
    test_run=subprocess.run([sys.executable,"-m","pytest","-q",
      "tests/test_r3_representation.py","tests/test_semantic_adapter.py","tests/test_train_only_annotation_packets.py",
      "tests/test_phase2ia_runtime_config.py","tests/test_phase2ia_hcc_control.py","tests/test_phase2ia_runner.py","tests/test_phase2ia_train_only_source.py","tests/test_phase2ia_ai_pilot_boundary.py","tests/test_core_invariant.py","tests/test_trace_miner.py","tests/test_trace_normalizer.py",
      "tests/test_trace_segmentation.py"],cwd=ROOT,env=env,
      text=True,capture_output=True)
    if test_run.returncode:
      raise SystemExit("R3 synthetic/integration tests failed:\\n"+test_run.stdout+test_run.stderr)
    test_summary=test_run.stdout.strip().splitlines()[-1]
    if "68 passed" not in test_summary:
      raise SystemExit(f"unexpected regression test summary: {test_summary}")
    mp=PKG/"package_manifest.json"
    manifest=json.loads(mp.read_text())
    manifest["package_integrity"]="PASS"
    manifest["status"]="WP0-WP2_CORE_COMPLETE; WP3_ON_HOLD_FOR_INDEPENDENT_ANNOTATORS; WP4_COMPLETE; WP5_SYNTHETIC_CONTROL_TESTED; WP6_IMPLEMENTATION_AND_SYNTHETIC_AUDITS_COMPLETE; ARC_RUN_BLOCKED"
    manifest["active_workstream"]="WP3 labels remain held pending independent coders/adjudicator; all eligible WP6 plumbing complete; no ARC run authorization"
    manifest["wp1_r3"]={"status":"IMPLEMENTED_AND_TESTED","grammar_version":"R3-GRAMMAR-ADDENDUM-V1",
      "grammar_sha256":digest(PKG/"r3_grammar_addendum_v1.md"),
      "implementation_sha256":digest(ROOT/"src/representations/r3.py"),
      "focused_contract_tests":r3_summary,"combined_synthetic_regressions":test_summary,
      "test_data":"synthetic fixtures only; no ARC task/test data accessed"}
    manifest["wp2_semantic_trace"]={"status":"IMPLEMENTED; SYNTHETIC_MINER_PARITY_PASS_USING_FROZEN_WP4_CONFIG",
      "schema_version":"ASFT-2I-SEMANTIC-TRACE-V1","implementation_sha256":digest(ROOT/"src/traces/semantic_adapter.py"),
      "test_sha256":digest(ROOT/"tests/test_semantic_adapter.py"),"tests_included_in_suite":10,
      "scope":"Common action tokens; target_scope retained in raw trace; arm/candidate provenance sidecar only",
      "synthetic_trace_miner_parity":"PASS for semantic token/pattern parity using frozen runtime config; full four-event fixture may produce zero candidates under core-length-1 aggregation and is not a positive-yield check"}
    manifest["wp3_annotation"]={"status":"RUBRIC_DEFINED; 600 TRAIN_ONLY_PACKETS_BUILT; INDEPENDENT_CODERS_AND_LABELS_PENDING",
      "protocol_sha256":digest(PKG/"family_annotation_protocol.md"),
      "packet_manifest_sha256":digest(PKG/"annotation_packets/packet_manifest.json"),
      "annotator_packet_sha256":packet_manifest["packet_sha256"],
      "label_map":"BLANK; not yet assigned/frozen","test_fields":"not decoded; packet field allowlist audit PASS"}
    manifest["wp3_ai_pilot"]={"status":"EXPLORATORY_ONLY; NOT_INDEPENDENT; NOT_WP3_COMPLETION",
      "pilot_manifest_sha256":digest(PKG/"wp3_ai_pilot_v1/pilot_manifest.json"),
      "source_train_packet_sha256":pilot_manifest["sample"]["source_packet_sha256"],
      "sample_size":pilot_manifest["sample"]["count"],
      "pass_agreement":"4/12; descriptive only","cohen_kappa_descriptive":pilot_manifest["results"]["cohen_kappa_descriptive"],
      "ai_adjudication_unknown":pilot_manifest["results"]["ai_adjudication_unknown_ambiguous"],
      "eligible_for_family_or_candidate_gates":False,"wp3_complete":False,
      "labels_used_by_runner_or_phase2i":False}
    manifest["wp3_provisional"]={"status":"AI_PROVISIONAL_ONLY; NOT_HUMAN; NOT_WP3_COMPLETION",
      "provisional_manifest_sha256":digest(PKG/"wp3_provisional_v1/provisional_manifest.json"),
      "source_train_packet_sha256":provisional_manifest["source_packet_sha256"],
      "task_count":provisional_manifest["task_count"],
      "exact_matches":provisional_manifest["agreement"]["exact_matches"],
      "cohen_kappa_descriptive":provisional_manifest["agreement"]["cohen_kappa_descriptive"],
      "unknown_a":provisional_manifest["agreement"]["unknown_a"],
      "unknown_b":provisional_manifest["agreement"]["unknown_b"],
      "disagreement_count":len(provisional_manifest["disagreement_task_ids"]),
      "family_map_sha256":provisional_manifest["family_map_sha256"],
      "eligible_for_family_or_candidate_gates":False,"wp3_complete":False,
      "labels_used_by_runner_or_phase2i":False,
      "note":"complete first pass for human review only; agreement is between two rule policies, not readers"}
    manifest["wp4_policy_identity"]={"status":"OWNER_APPROVED_FROZEN_AND_RUNTIME_TESTED",
      "config_sha256":digest(PKG/"wp4_runtime_config_v1.json"),
      "resolution_doc_sha256":digest(PKG/"wp4_policy_identity_resolution.md"),
      "runtime_factory_sha256":digest(ROOT/"experiments/phase2ia/runtime_config.py"),
      "code_changes":"No modifications to InvariantIdentity; frozen runtime factory and arm-separated identity ledger implemented"}
    hcc_summary=__import__("experiments.phase2ia.hcc_control",fromlist=["run_hcc_control"]).run_hcc_control()
    manifest["wp5_hcc"]={"status":"IMPLEMENTED_AND_TESTED_SYNTHETIC_ONLY; NO_ARC_HCC_RUN",
      "control_version":hcc_summary.control_version,"implementation_sha256":digest(ROOT/"experiments/phase2ia/hcc_control.py"),
      "test_sha256":digest(ROOT/"tests/test_phase2ia_hcc_control.py"),
      "result":{"synthetic_tasks":hcc_summary.task_count,"training_pairs":hcc_summary.training_pair_count,
        "r1_exact_demo_checks":hcc_summary.r1_equivalent_demo_checks,"r3_exact_demo_checks":hcc_summary.r3_equivalent_demo_checks,
        "r1_generator_accepted":hcc_summary.r1_candidates,"r3_generator_accepted":hcc_summary.r3_candidates,
        "r1_structurally_eligible":hcc_summary.r1_structurally_eligible,"r3_structurally_eligible":hcc_summary.r3_structurally_eligible,
        "candidate_signatures_equal":hcc_summary.identical_candidate_signatures},
      "miner_fixture_boundary":"oracle-selected one-action synthetic fixtures; not search coverage or full four-event production integration",
      "arc_namespace_guard":"negative HCC-to-ARC task-ID test passes","scientific_evidence":False}
    manifest["wp6_runner"]={"status":"IMPLEMENTED_AND_SYNTHETIC_END_TO_END_TESTED; ARC_EXECUTION_BLOCKED_BY_WP3_AND_AUTHORIZATION",
      "implementation_sha256":digest(ROOT/"experiments/phase2ia/runner.py"),
      "search_adapters_sha256":digest(ROOT/"experiments/phase2ia/search_adapters.py"),
      "train_only_source_sha256":digest(ROOT/"experiments/phase2ia/train_only_source.py"),
      "test_sha256":digest(ROOT/"tests/test_phase2ia_runner.py"),
      "train_only_source_test_sha256":digest(ROOT/"tests/test_phase2ia_train_only_source.py"),
      "paired_synthetic_replay":"PASS; six synthetic IDs; identical ordered IDs and resource limits",
      "synthetic_file_to_search_to_trace_to_mining_to_artifact_audit":"PASS; registered R1/R3 callbacks; train-only stream stops before trailing test-output sentinel",
      "authorization":"ARC mode requires separate run-specific authorization bound to protocol/task/source-allowlist/family-map/config/resource-limit/arm/grammar/runner/adapter/search-code hashes; none provided",
      "controls":["path-confined explicit task-file allowlist","train-first streaming parser and prefix byte cap","10-trial/task/search-time ceiling","900-cell grid and 2048-MiB worker address-space caps","hashed train-demo/family-map/code provenance","opaque candidate/trial IDs","HCC namespace rejection","forbidden-field and raw-grid rejection","exact output-file allowlist plus SHA-256","stage ledger","paired-order/budget checks","arm-separated identity"],
      "remaining":["independent WP3 family labels/adjudication are held and unavailable","owner run-specific authorization is not provided","no actual ARC artifacts exist to audit because ARC execution is not authorized"],
      "arc_run":"NOT RUN; NOT AUTHORIZED"}
    manifest["qa"]={"artifacts":f"{len(ARTIFACTS)}/{len(ARTIFACTS)} present","workstreams":"8 sequenced","active_workstream":"WP3 labels held pending independent coders/adjudicator; WP5 and WP6 synthetic engineering tests pass; ARC execution remains blocked",   
      "open_specification_decisions":sum(r["gate_status"].startswith("OPEN") for r in issues),
      "wp1_r3_contract_tests":r3_summary,"combined_synthetic_regressions":test_summary,
      "wp4":"frozen config, transfer/taxonomy separation, identity ledger; runtime tests pass", 
      "hcc":"ASFT-2I-HCC-SYNTH-V1 synthetic plumbing passes; no ARC HCC run or evidence",
      "wp3_ai_pilot":"12-task exploratory AI pilot only; 4/12 agreement, descriptive kappa 0.232; not independent and not eligible",

      "artifact_boundary":"Train-only source and synthetic output allowlist/field/hash audit PASS; no ARC run artifacts were created",  
      "empirical_arc_run":"NOT RUN; NOT AUTHORIZED","phase3":"BLOCKED / UNAUTHORIZED","local_markdown_links":"PASS"}
    mp.write_text(json.dumps(manifest,indent=2)+"\n")
    files=[PKG/n for n in ARTIFACTS]+[ROOT/p for p in SOURCES]
    missing=[str(p.relative_to(ROOT)) for p in files if not p.is_file()]
    if missing: raise SystemExit(f"missing provenance sources: {missing}")
    prov={"package_id":manifest["package_id"],"sha256":{p.relative_to(ROOT).as_posix():digest(p) for p in files},
      "scope":"WP0-WP2 core implementation (including effect-based reflection correction), WP3 train-only packets plus a separate 12-task non-qualifying AI rubric pilot, WP4 frozen config/identity ledger, WP5 synthetic HCC control, and WP6 paired-runner/search adapters/path-confined source/synthetic artifact audit. No ARC test outputs or WP3-qualified family map, ARC HCC, or Phase 2I candidate-production run was accessed or performed; the real ARC run remains blocked pending independent WP3 coding and separate authorization.",
      "decision":"WP3 labels remain on hold; WP4 complete. Phase 2I ARC execution not authorized; Phase 3B/3D remain blocked."}
    (PKG/"provenance.json").write_text(json.dumps(prov,indent=2)+"\n")
    print(json.dumps({"package_id":manifest["package_id"],"qa":manifest["qa"],"sha256_entries":len(files)},indent=2))
if __name__=="__main__": main()
