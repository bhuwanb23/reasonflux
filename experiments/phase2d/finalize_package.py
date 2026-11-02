from __future__ import annotations
import csv, hashlib, json, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PKG = ROOT / 'reports/experiments/ASFT-V1.1-PHASE-2D-TRACE-GENERATION-AUDIT-V1'
PKG_REL = PKG.relative_to(ROOT).as_posix()
REQUIRED_MD = [
'historical_trace_audit.md','trace_taxonomy.md','trace_lifecycle_report.md','trace_yield_report.md',
'trace_diversity_report.md','trace_quality_report.md','invariant_readiness_audit.md',
'trace_failure_localization.md','trace_reporting_standard.md','phase2D_readiness_review.md']
EXCLUDE = {'source_manifest.json','source_hashes.csv','provenance_validation.md'}
INPUTS = [
('experiments/phase2d/trace_audit.py','executed_audit_code','Phase 2D reconstruction, retrospective validation, and TraceMiner replay; test-output blind.'),
('experiments/phase2d/finalize_package.py','package_qa_code','Package provenance, hash, structure, count, scope, and link validation.'),
('experiments/phase2c/config.json','frozen_protocol','Phase 2C conditions and budget definitions.'),
('experiments/phase2c/preregistration.md','frozen_protocol','Frozen Phase 2C search and interpretation limits.'),
('experiments/phase2c/search_budget_benchmark.py','executed_search_code','Runner that generated the saved Phase 2C logs audited here.'),
('experiments/phase13g/runner.py','historical_runtime_source','Historical trace generation and miner path.'),
('experiments/phase13g/common.py','historical_runtime_source','Historical search and trace helpers.'),
('src/core/trace.py','trace_runtime_source','Trace structure and serialization semantics.'),
('src/core/invariant.py','miner_runtime_source','Invariant mining runtime.'),
('src/invariants/pattern_mining.py','miner_runtime_source','Pattern extraction runtime.'),
('src/invariants/aggregation.py','miner_runtime_source','Pattern aggregation runtime.'),
('src/invariants/candidate_generation.py','miner_runtime_source','Invariant candidate generation runtime.'),
('reports/experiments/ASFT-V1.1-PHASE-2C-SEARCH-BUDGET-AUDIT-V1/search_execution_log.csv','audited_saved_log','Primary 4,000 Phase 2C task-condition search records.'),
('reports/experiments/ASFT-V1.1-PHASE-2C-SEARCH-BUDGET-AUDIT-V1/candidate_trial_log.csv','audited_saved_log','Candidate-level Phase 2C attempt and outcome log.'),
('reports/experiments/ASFT-V1.1-PHASE-2C-SEARCH-BUDGET-AUDIT-V1/budget_sensitivity_summary.csv','audited_saved_summary','Frozen condition-level search yield summary.'),
('reports/experiments/ASFT-V1.1-PHASE-2C-SEARCH-BUDGET-AUDIT-V1/source_hashes.csv','upstream_provenance','Phase 2C source/artifact hashes, including training task inputs.'),
('reports/experiments/PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/discovery_traces.jsonl','historical_saved_trace','600 Phase 13G serialized discovery trace records.'),
('reports/experiments/PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/summary.json','historical_saved_summary','Historical trace, mining, and outcome summary used for replay parity.'),
]

def sha(path: Path) -> str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for b in iter(lambda:f.read(1<<20),b''): h.update(b)
    return h.hexdigest()

def main():
    errors=[]
    for name in REQUIRED_MD:
        if not (PKG/name).is_file(): errors.append(f'Missing required Markdown: {name}')
    # Validate artifact structure and key denominators.
    def rows(name):
        with (PKG/name).open(newline='',encoding='utf-8') as f: return list(csv.DictReader(f))
    records=rows('trace_audit_records.csv'); historical=rows('historical_trace_validation.csv')
    if len(records)!=4000: errors.append(f'Expected 4000 Phase 2C records, found {len(records)}')
    if len(historical)!=600: errors.append(f'Expected 600 historical serialized records, found {len(historical)}')
    for fn in [p.name for p in PKG.glob('*.csv')]:
        try: rows(fn)
        except Exception as e: errors.append(f'CSV parse failure {fn}: {e}')
    if any(str(r.get('accuracy','')).upper() not in ('NOT_MEASURED_BY_DESIGN','NOT_MEASURED','') for r in records):
        errors.append('Unexpected accuracy value in trace records')
    if sum(r.get('T2_valid')=='True' for r in records)!=4000: errors.append('Phase 2C valid trace count mismatch')
    if sum(r.get('T4_successful')=='True' for r in records)!=27: errors.append('Phase 2C successful trace total mismatch')
    try:
        hsum=json.loads((PKG/'historical_trace_validation_summary.json').read_text())
        mining=json.loads((PKG/'trace_mining_details.json').read_text())
        manifest=json.loads((PKG/'trace_audit_manifest.json').read_text())
        if hsum.get('retrospective_structural_valid')!=600: errors.append('Historical retrospective validation count mismatch')
        if hsum.get('successful_traces')!=3: errors.append('Historical successful trace count mismatch')
        if hsum.get('generation_time_validator_established') is not False: errors.append('Historical validator limitation missing')
        if manifest.get('test_output_fields_parsed_or_used') is not False or manifest.get('accuracy_measured') is not False: errors.append('Scope guard failed')
        histminer=mining.get('phase13g_historical',{}).get('trace_miner_statistics',{})
        if histminer.get('traces_in')!=3 or histminer.get('fragments')!=30 or histminer.get('raw_patterns')!=0 or histminer.get('candidates')!=0:
            errors.append('Historical miner replay metrics mismatch')
    except Exception as e: errors.append(f'JSON QA error: {e}')
    # Check all local Markdown links (ignore external URLs and anchors).
    link_re=re.compile(r'\[[^\]]*\]\(([^)]+)\)')
    link_count=0
    for md in PKG.glob('*.md'):
        text=md.read_text(encoding='utf-8')
        for target in link_re.findall(text):
            target=target.strip().split('#',1)[0]
            if not target or re.match(r'^[a-z]+://',target): continue
            link_count+=1
            if not (md.parent/target).resolve().exists(): errors.append(f'Broken Markdown link {md.name}: {target}')
    # Hash all package artifacts (excluding the three self-referential final provenance files) and explicit inputs.
    records_out=[]
    for p in sorted(PKG.iterdir()):
        if p.is_file() and p.name not in EXCLUDE:
            rel=p.relative_to(ROOT).as_posix()
            records_out.append({'path':rel,'kind':'phase2d_package_artifact','note':'Final Phase 2D report, data, or audit manifest.'})
    for rel,kind,note in INPUTS:
        p=ROOT/rel
        if not p.is_file(): errors.append(f'Missing provenance input: {rel}'); continue
        records_out.append({'path':rel,'kind':kind,'note':note})
    for r in records_out:
        p=ROOT/r['path']; r['sha256']=sha(p); r['bytes']=p.stat().st_size
    sm={'phase':'ASFT-V1.1-PHASE-2D','package':'ASFT-V1.1-PHASE-2D-TRACE-GENERATION-AUDIT-V1',
        'scope':'Retrospective audit of saved Phase 2C test-output-blind traces and Phase 13G serialized historical traces; no new search, test-label parsing, or accuracy measurement.',
        'record_count':len(records_out),'records':records_out}
    (PKG/'source_manifest.json').write_text(json.dumps(sm,indent=2)+'\n')
    with (PKG/'source_hashes.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=['path','kind','sha256','bytes','note']);w.writeheader()
        for r in records_out:w.writerow(r)
    # Re-read and verify every recorded digest.
    verified=0
    for r in records_out:
        if sha(ROOT/r['path'])!=r['sha256']:errors.append(f"Hash mismatch: {r['path']}")
        else:verified+=1
    status='PASS' if not errors else 'FAIL'
    report=(f'# Phase 2D provenance and package QA\n\n**Status: {status}.**\n\n'
      f'- Required Markdown deliverables: {len(REQUIRED_MD)}/{len(REQUIRED_MD)} present.\n'
      f'- Phase 2C trace records: {len(records)} (expected 4,000); valid: {sum(r.get("T2_valid")=="True" for r in records)}; successful: {sum(r.get("T4_successful")=="True" for r in records)}.\n'
      f'- Historical serialized records: {len(historical)} (expected 600); retrospective structural validation: {sum(r.get("independent_serialized_trace_validation")=="True" for r in historical)}.\n'
      f'- JSON/CSV structure and key lifecycle assertions: checked.\n'
      f'- Local Markdown links checked: {link_count}.\n'
      f'- Provenance records hashed and verified: {verified}/{len(records_out)}.\n'
      f'- Test-output fields parsed/used: **No**; accuracy measured: **No**; new ARC search/scoring: **No**.\n'
      f'- Phase 13G generation-time validator: **not established**; retrospective validation is not retroactively attributed to the historical runtime.\n'
      f'- Scope decision: Phase 2D audit only; Phase 2 remains blocked; no confirmatory, transfer, capability, accuracy, or causal-mechanism claim.\n')
    if errors: report+='\n## Errors\n\n'+'\n'.join(f'- {e}' for e in errors)+'\n'
    (PKG/'provenance_validation.md').write_text(report)
    print(report)
    if errors: raise SystemExit(1)
if __name__=='__main__': main()
