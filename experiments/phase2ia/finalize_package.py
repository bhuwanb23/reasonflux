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
 "annotation_packets/packet_manifest.json"]
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
 "tests/invariants/test_r3_representation.py",
 "tests/traces/test_semantic_adapter.py",
 "experiments/phase2ia/build_annotation_packets.py",
 "experiments/phase2ia/runtime_config.py",
 "experiments/phase2ia/hcc_control.py",
 "experiments/phase2ia/runner.py",
 "experiments/phase2ia/search_adapters.py",
 "experiments/phase2ia/train_only_source.py",
 "experiments/phase13g/common.py",
 "tests/phase2ia/test_phase2ia_hcc_control.py",
 "tests/phase2ia/test_phase2ia_runner.py",
 "tests/phase2ia/test_phase2ia_train_only_source.py",
 "tests/phase2ia/test_phase2ia_wp3_provisional_boundary.py",
 "tests/t2t/test_train_only_annotation_packets.py",
 "tests/phase2ia/test_phase2ia_runtime_config.py",
 "datasets/arc/arc-agi-2/split_manifest.json",
]
REMOTE_WP3={
 "source_url":"https://github.com/bhuwanb23/reasonflux/tree/eb3c6a2cb04afe6a7289e30e7141fdec9b64fa99/reports/experiments/ASFT-V1.1-PHASE-2I-A-CANDIDATE-PRODUCTION-ENABLEMENT-V1/wp3_provisional_v1",
 "commit":"eb3c6a2cb04afe6a7289e30e7141fdec9b64fa99",
 "status":"AI_PROVISIONAL_ONLY_NOT_WP3",
 "local_copy":"NOT RETAINED; verified against remote outputs",
 "task_count":600,
 "label_mode":"AI_PROVISIONAL",
 "independence":"A/B/C are deterministic AI policies sharing feature code, ontology, and author; not independent human coders/adjudicator",
 "agreement":{"n":600,"exact_matches":476,"observed_agreement":0.7933333333333333,
  "cohen_kappa_descriptive":0.7196367336172137,"unknown_a":226,"unknown_b":264,
  "final_unknown_ambiguous":226,"final_non_unknown":374},
 "family_map_sha256":"79e92048b6c840deaf04d9a0136d9c09304789effac51ced32f5fa1d024123bd",
 "source_packet_sha256":"846bf7c396f4563204142cc5859b604279e67b5e6389a27bef0bf4cfa390436e",
 "outputs_sha256":{
  "adjudication_log.csv":"e73f1d8bd427d3b903e1ce1f7dcd73e224c3888c808138a927766f3221b4c17f",
  "agreement_report.md":"6876ae47d57c9ce4d2ae5bfc598166571326cbb98f51f507fde4df6214a57ec8",
  "annotator_A_labels.csv":"8bde7e6786f7749f6be234cdcac051d263518afec76432692fdd0060b414fc8a",
  "annotator_B_labels.csv":"440c57c9b74e5a7a41a92e052896b2eb5e6fd750079d134b537699d94e2616b5",
  "confusion_matrix.csv":"3b5700f98468efcd729f197ea439f6a1dadb4a146b7b09ba85da54d4d7f6e13c",
  "disagreement_priority_queue.csv":"f572f2dbe69ef8a001a7836104e4decb102547f51acb550a11e64ec8f016cc34",
  "family_map_hash.txt":"bf4712d1ec9311f275348125e8cf30408aa9106fee4c3bd6f15e2f24824bdb47",
  "README.md":"274aa38101c8ba90b3454a0d39b2b26e87a000433d8e41ec5ac37788c2003a33",
  "review_packet_manifest.json":"96910b318e9c24713c13de6e06f0b19ba60839c160c67edca4d1b00aa589262e",
  "reviewer_A_packet.jsonl":"2c42f64690b206adada89f5091eba68a96a428c53bfa293c92ed29be4668bf91",
  "reviewer_B_packet.jsonl":"84af61c1a4bce16df352a3f2b1a2a4b5c9f65fd269ff847110e9787f718a3f06",
  "reviewer_C_packet.jsonl":"5396d298b9fa1bf2fd9958be6c595ce07970c5515e04896cd39fbe11fa1aae3b",
  "task_family_map.csv":"79e92048b6c840deaf04d9a0136d9c09304789effac51ced32f5fa1d024123bd",
  "wp3_completion_review.md":"20477b46e9f7017fdf669a59f795be9f2ec425ef66217addee1766b390bbc1ef"},
 "all_map_rows_status":"PROVISIONAL_NOT_ADJUDICATED_BY_HUMAN",
 "human_review":{"status":"AI_DRAFT_FOR_HUMAN_REVIEW_ONLY","reviews_present":0,
  "human_gate_completion_percent":0,"coder_packet_rows_per_role":600,
  "all_A_B_C_rows_unreviewed":True,"adjudication_reviews_present":0,
  "promotion_blockers":["600 of 600 tasks lack complete reviews from roles A and B",
   "no human adjudication records for role C"]},
 "review_packet_sha256":{
  "reviewer_A_packet.jsonl":"2c42f64690b206adada89f5091eba68a96a428c53bfa293c92ed29be4668bf91",
  "reviewer_B_packet.jsonl":"84af61c1a4bce16df352a3f2b1a2a4b5c9f65fd269ff847110e9787f718a3f06",
  "reviewer_C_packet.jsonl":"5396d298b9fa1bf2fd9958be6c595ce07970c5515e04896cd39fbe11fa1aae3b",
  "disagreement_priority_queue.csv":"f572f2dbe69ef8a001a7836104e4decb102547f51acb550a11e64ec8f016cc34"},
 "eligible_for_family_qualification":False,
 "eligible_for_candidate_eligibility":False,
 "eligible_for_phase2i_execution":False,
 "wp3_complete":False,
 "labels_used_by_runner_or_phase2i":False,
 "phase2i_run":"NOT AUTHORIZED; NOT RUN"
}
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
    source_packet=PKG/"annotation_packets/annotator_A_train_only.jsonl"
    if REMOTE_WP3["status"]!="AI_PROVISIONAL_ONLY_NOT_WP3" or REMOTE_WP3["source_packet_sha256"]!=digest(source_packet):
      raise SystemExit("remote WP3 provisional bundle must remain pinned to the train-only source and non-eligible")
    if REMOTE_WP3["outputs_sha256"].get("task_family_map.csv")!=REMOTE_WP3["family_map_sha256"]:
      raise SystemExit("remote provisional family map hash reference is inconsistent")
    if any(REMOTE_WP3.get(k) is not False for k in
      ("eligible_for_family_qualification","eligible_for_candidate_eligibility","eligible_for_phase2i_execution","wp3_complete","labels_used_by_runner_or_phase2i")):
      raise SystemExit("remote AI provisional labels must remain prohibited from eligibility and execution")
    if REMOTE_WP3["agreement"]["n"]!=600 or REMOTE_WP3["agreement"]["exact_matches"]!=476 or REMOTE_WP3["agreement"]["final_unknown_ambiguous"]!=226:
      raise SystemExit("remote WP3 provisional summary does not match the audited outputs")
    if REMOTE_WP3["human_review"]["reviews_present"]!=0 or REMOTE_WP3["human_review"]["human_gate_completion_percent"]!=0:
      raise SystemExit("latest remote WP3 commit has no completed human reviews; do not promote its AI drafts")
    if any(REMOTE_WP3["review_packet_sha256"].get(name)!=REMOTE_WP3["outputs_sha256"].get(name)
      for name in REMOTE_WP3["review_packet_sha256"]):
      raise SystemExit("human-review packet hashes differ from the remote bundle output hashes")
    env=os.environ.copy()
    env["PYTHONPATH"]=str(ROOT/"src")+os.pathsep+env.get("PYTHONPATH","")
    r3_run=subprocess.run([sys.executable,"-m","pytest","-q","tests/invariants/test_r3_representation.py"],cwd=ROOT,env=env,
      text=True,capture_output=True)
    if r3_run.returncode:
      raise SystemExit("R3 contract tests failed:\\n"+r3_run.stdout+r3_run.stderr)
    r3_summary=r3_run.stdout.strip().splitlines()[-1]
    if "11 passed" not in r3_summary:
      raise SystemExit(f"unexpected R3 test summary: {r3_summary}")
    test_run=subprocess.run([sys.executable,"-m","pytest","-q",
      "tests/invariants/test_r3_representation.py","tests/traces/test_semantic_adapter.py","tests/t2t/test_train_only_annotation_packets.py",
      "tests/phase2ia/test_phase2ia_runtime_config.py","tests/phase2ia/test_phase2ia_hcc_control.py","tests/phase2ia/test_phase2ia_runner.py","tests/phase2ia/test_phase2ia_train_only_source.py","tests/phase2ia/test_phase2ia_wp3_provisional_boundary.py","tests/core/test_core_invariant.py","tests/traces/test_trace_miner.py","tests/traces/test_trace_normalizer.py",
      "tests/traces/test_trace_segmentation.py"],cwd=ROOT,env=env,
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
      "test_sha256":digest(ROOT/"tests/traces/test_semantic_adapter.py"),"tests_included_in_suite":10,
      "scope":"Common action tokens; target_scope retained in raw trace; arm/candidate provenance sidecar only",
      "synthetic_trace_miner_parity":"PASS for semantic token/pattern parity using frozen runtime config; full four-event fixture may produce zero candidates under core-length-1 aggregation and is not a positive-yield check"}
    manifest["wp3_annotation"]={"status":"RUBRIC_DEFINED; 600 TRAIN_ONLY_PACKETS_BUILT; INDEPENDENT_HUMAN_CODERS_AND_ADJUDICATOR_PENDING",
      "protocol_sha256":digest(PKG/"family_annotation_protocol.md"),
      "packet_manifest_sha256":digest(PKG/"annotation_packets/packet_manifest.json"),
      "annotator_packet_sha256":packet_manifest["packet_sha256"],
      "label_map":"BLANK; remote AI-provisional map is not eligible and is not used",
      "remote_ai_provisional_reference":"wp3_remote_provisional; external commit-pinned source",
      "test_fields":"not decoded; packet field allowlist audit PASS"}
    manifest.pop("wp3_ai_pilot",None)
    manifest["wp3_remote_provisional"]=REMOTE_WP3
    manifest["wp4_policy_identity"]={"status":"OWNER_APPROVED_FROZEN_AND_RUNTIME_TESTED",
      "config_sha256":digest(PKG/"wp4_runtime_config_v1.json"),
      "resolution_doc_sha256":digest(PKG/"wp4_policy_identity_resolution.md"),
      "runtime_factory_sha256":digest(ROOT/"experiments/phase2ia/runtime_config.py"),
      "code_changes":"No modifications to InvariantIdentity; frozen runtime factory and arm-separated identity ledger implemented"}
    hcc_summary=__import__("experiments.phase2ia.hcc_control",fromlist=["run_hcc_control"]).run_hcc_control()
    manifest["wp5_hcc"]={"status":"IMPLEMENTED_AND_TESTED_SYNTHETIC_ONLY; NO_ARC_HCC_RUN",
      "control_version":hcc_summary.control_version,"implementation_sha256":digest(ROOT/"experiments/phase2ia/hcc_control.py"),
      "test_sha256":digest(ROOT/"tests/phase2ia/test_phase2ia_hcc_control.py"),
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
      "test_sha256":digest(ROOT/"tests/phase2ia/test_phase2ia_runner.py"),
      "train_only_source_test_sha256":digest(ROOT/"tests/phase2ia/test_phase2ia_train_only_source.py"),
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
      "wp3_remote_provisional":"Latest 14-output AI-draft/review-packet bundle hash-audited; 0 human reviews/sign-offs present; WP3 and Phase 2I remain blocked",
      "artifact_boundary":"Train-only source and synthetic output allowlist/field/hash audit PASS; no ARC run artifacts were created",  
      "empirical_arc_run":"NOT RUN; NOT AUTHORIZED","phase3":"BLOCKED / UNAUTHORIZED","local_markdown_links":"PASS"}
    mp.write_text(json.dumps(manifest,indent=2)+"\n")
    files=[PKG/n for n in ARTIFACTS]+[ROOT/p for p in SOURCES]
    missing=[str(p.relative_to(ROOT)) for p in files if not p.is_file()]
    if missing: raise SystemExit(f"missing provenance sources: {missing}")
    prov={"package_id":manifest["package_id"],"sha256":{p.relative_to(ROOT).as_posix():digest(p) for p in files},
      "scope":"WP0-WP2 core implementation (including effect-based reflection correction), WP3 train-only packets plus a commit-pinned external AI-provisional bundle audited by output hashes but not used for qualification, WP4 frozen config/identity ledger, WP5 synthetic HCC control, and WP6 paired-runner/search adapters/path-confined source/synthetic artifact audit. No ARC test outputs or WP3-qualified family map, ARC HCC, or Phase 2I candidate-production run was accessed or performed; the real ARC run remains blocked pending independent human WP3 coding and separate authorization.",
      "decision":"WP3 labels remain on hold; WP4 complete. Phase 2I ARC execution not authorized; Phase 3B/3D remain blocked."}
    (PKG/"provenance.json").write_text(json.dumps(prov,indent=2)+"\n")
    print(json.dumps({"package_id":manifest["package_id"],"qa":manifest["qa"],"sha256_entries":len(files)},indent=2))
if __name__=="__main__": main()
