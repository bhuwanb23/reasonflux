from __future__ import annotations
import csv, hashlib, json, re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PKG=ROOT/'reports/experiments/ASFT-V1.1-PHASE-2E-INVARIANT-DISCOVERY-AUDIT-V1'
REQUIRED_MD=['historical_invariant_audit.md','invariant_taxonomy.md','recurrence_benchmark.md','candidate_generation_audit.md','support_threshold_audit.md','invariant_validation_audit.md','discovery_yield_report.md','invariant_failure_localization.md','invariant_reporting_standard.md','phase2E_readiness_review.md']
EXCLUDE={'source_manifest.json','source_hashes.csv','provenance_validation.md'}
INPUTS=[
('experiments/phase2e/preregistration.md','frozen_phase2e_protocol','Support levels and analysis boundaries frozen before audit execution.'),
('experiments/phase2e/invariant_audit.py','executed_audit_code','Retrospective recurrence, threshold, candidate, and validation-stage audit; no search/test scoring.'),
('experiments/phase2e/finalize_package.py','package_qa_code','Package hash, count, structure, scope, and link checks.'),
('experiments/phase13g/runner.py','historical_runtime_source','Phase 13G thresholds, candidate/trace mining orchestration.'),
('experiments/phase13g/common.py','historical_trace_runtime_source','Historical trace construction and program-family labels.'),
('src/invariants/detector.py','miner_runtime_source','TraceMiner stages and validation orchestration.'),
('src/invariants/pattern_mining.py','pattern_runtime_source','Pattern extraction and support gates.'),
('src/invariants/aggregation.py','aggregation_runtime_source','Pattern-to-structure aggregation.'),
('src/invariants/candidate_generation.py','candidate_runtime_source','Structure-to-candidate mapping and generation rejection.'),
('src/invariants/specification/policy.py','policy_runtime_source','Frozen invariant policy fields.'),
('src/invariants/specification/rejection.py','rejection_runtime_source','Candidate rejection criteria.'),
('src/invariants/validator.py','validation_runtime_source','Candidate validation states and stage counts.'),
('src/invariants/ranking.py','validation_runtime_source','Validation score calculation.'),
('src/invariants/validation/scores.py','validation_runtime_source','Validation score fields and thresholds.'),
('src/traces/normalizer.py','trace_normalizer_source','Frozen operation normalization.'),
('src/traces/segmentation.py','trace_segmentation_source','Frozen operation n-gram segmentation.'),
('src/core/trace.py','trace_data_model','ReasoningTrace/ReasoningStep serialization.'),
('reports/experiments/ASFT-V1.1-PHASE-2D-TRACE-GENERATION-AUDIT-V1/trace_audit_records.csv','audited_saved_phase2c_records','4,000 Phase 2C trace records; Phase 2E uses discovery successes only.'),
('reports/experiments/ASFT-V1.1-PHASE-2D-TRACE-GENERATION-AUDIT-V1/historical_trace_validation.csv','audited_historical_validation','Independent retrospective validation of saved Phase 13G serialized traces.'),
('reports/experiments/ASFT-V1.1-PHASE-2C-SEARCH-BUDGET-AUDIT-V1/search_execution_log.csv','upstream_saved_search_log','Saved Phase 2C test-output-blind search outcomes.'),
('reports/experiments/ASFT-V1.1-PHASE-2C-SEARCH-BUDGET-AUDIT-V1/source_hashes.csv','upstream_provenance','Phase 2C task and source hashes.'),
('reports/experiments/PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/discovery_traces.jsonl','historical_saved_traces','Serialized Phase 13G discovery traces.'),
('reports/experiments/PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/summary.json','historical_saved_summary','Historical saved mining statistics used for parity checks.'),
('reports/experiments/PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/invariants.csv','historical_saved_final_invariants','Historical final invariant table; zero data rows.'),
]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def read_csv(name):
 with (PKG/name).open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
def main():
 errors=[]
 for n in REQUIRED_MD:
  if not (PKG/n).is_file():errors.append('Missing required Markdown: '+n)
 rec=read_csv('recurrence_by_signature.csv');rs=read_csv('recurrence_summary.csv')
 sw=read_csv('candidate_generation_audit.csv');details=read_csv('candidate_and_validation_details.csv')
 vs=read_csv('validation_diagnostic_summary.csv')
 if len(rs)!=5:errors.append(f'Expected 5 recurrence sources, found {len(rs)}')
 if len(sw)!=15:errors.append(f'Expected 15 source-threshold rows, found {len(sw)}')
 if {r['threshold_id'] for r in sw}!={'RELAXED_S2','CURRENT_S1','STRICT_S3'}:errors.append('Threshold IDs mismatch')
 by={(r['source'],r['threshold_id']):r for r in sw}
 for source in ['PHASE13G_HISTORICAL','S2','S3','S4']:
  if by[(source,'CURRENT_S1')]['patterns_after_frequency_and_cross_trace_gates']!='0':errors.append(f'Current support unexpectedly passed patterns for {source}')
  if by[(source,'RELAXED_S2')]['patterns_after_frequency_and_cross_trace_gates']!='4':errors.append(f'Relaxed pattern count mismatch for {source}')
  if by[(source,'RELAXED_S2')]['candidate_proposals_before_generation_rejections']!='2':errors.append(f'Relaxed proposal count mismatch for {source}')
  if by[(source,'RELAXED_S2')]['accepted_generation_candidates']!='0':errors.append(f'Accepted candidate count mismatch for {source}')
 hist=next(r for r in rs if r['source']=='PHASE13G_HISTORICAL')
 if hist['max_distinct_trace_support']!='3' or hist['signatures_support_ge_5']!='0':errors.append('Historical recurrence summary mismatch')
 # Machine-readable manifest scope guards.
 try:
  manifest=json.loads((PKG/'phase2E_audit_manifest.json').read_text())
  if manifest.get('test_outputs_parsed_or_used') is not False or manifest.get('new_arc_search_or_scoring_run') is not False:errors.append('Scope guard failed')
  if manifest.get('transfer_holdout_traces_used_for_discovery_mining') is not False:errors.append('Transfer/holdout exclusion failed')
  saved=manifest.get('phase13g_saved_summary_mining_statistics',{})
  if saved.get('traces_in')!=3 or saved.get('fragments')!=30 or saved.get('raw_patterns')!=0 or saved.get('candidates')!=0:errors.append('Historical mining summary mismatch')
 except Exception as e:errors.append(f'Manifest JSON invalid: {e}')
 # Validate all CSVs and local Markdown links.
 for p in PKG.glob('*.csv'):
  try:read_csv(p.name)
  except Exception as e:errors.append(f'CSV parse error {p.name}: {e}')
 link_re=re.compile(r'\[[^\]]*\]\(([^)]+)\)');links=0
 for md in PKG.glob('*.md'):
  for target in link_re.findall(md.read_text(encoding='utf-8')):
   target=target.strip().split('#',1)[0]
   if not target or re.match(r'^[a-z]+://',target):continue
   links+=1
   if not (md.parent/target).resolve().exists():errors.append(f'Broken link in {md.name}: {target}')
 # Hash all package files other than mutually-referential provenance outputs, plus declared inputs.
 entries=[]
 for p in sorted(PKG.iterdir()):
  if p.is_file() and p.name not in EXCLUDE:
   entries.append({'path':p.relative_to(ROOT).as_posix(),'kind':'phase2e_package_artifact','note':'Final Phase 2E report, data, or manifest.'})
 for path,kind,note in INPUTS:
  p=ROOT/path
  if not p.is_file():errors.append('Missing provenance input: '+path);continue
  entries.append({'path':path,'kind':kind,'note':note})
 for e in entries:
  p=ROOT/e['path'];e['sha256']=sha(p);e['bytes']=p.stat().st_size
 sm={'phase':'ASFT-V1.1-PHASE-2E','package':'ASFT-V1.1-PHASE-2E-INVARIANT-DISCOVERY-AUDIT-V1',
  'scope':'Retrospective invariant-discovery audit on saved Phase 13G and Phase 2C discovery traces only; no ARC search/test-output use.',
  'record_count':len(entries),'records':entries}
 (PKG/'source_manifest.json').write_text(json.dumps(sm,indent=2)+'\n')
 with (PKG/'source_hashes.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=['path','kind','sha256','bytes','note']);w.writeheader();w.writerows(entries)
 verified=sum(sha(ROOT/e['path'])==e['sha256'] for e in entries)
 if verified!=len(entries):errors.append('Provenance verification count mismatch')
 status='PASS' if not errors else 'FAIL'
 report=(f'# Phase 2E provenance and package QA\n\n**Status: {status}.**\n\n'
  f'- Required Markdown deliverables: {sum((PKG/n).is_file() for n in REQUIRED_MD)}/{len(REQUIRED_MD)} present.\n'
  f'- Recurrence signature rows: {len(rec)}; source summaries: {len(rs)}; support-sweep rows: {len(sw)}.\n'
  f'- Candidate/validation detail rows: {len(details)}; validator diagnostic source summaries: {len(vs)}.\n'
  f'- Local Markdown links checked: {links}.\n'
  f'- Provenance records hashed and verified: {verified}/{len(entries)}.\n'
  f'- Test outputs parsed/used: **No**; new ARC search/scoring: **No**; historical outcomes modified: **No**.\n'
  f'- FDR/independent semantic generality: **Not measured/estimable**.\n'
  f'- Interpretation: audit-only; no invariant correctness, transfer, accuracy, capability, or causal-mechanism claim.\n')
 if errors:report+='\n## Errors\n\n'+'\n'.join('- '+e for e in errors)+'\n'
 (PKG/'provenance_validation.md').write_text(report)
 print(report)
 if errors:raise SystemExit(1)
if __name__=='__main__':main()
