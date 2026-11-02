from __future__ import annotations
import csv,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PKG=ROOT/'reports/experiments/ASFT-V1.1-PHASE-2G-ARC-FOUNDATION-READINESS-V1'
REQ=['foundation_evidence_review.md','arc_readiness_matrix.csv','arc_risk_assessment.md','protocol_integrity_review.md','mechanism_test_readiness.md','representation_hypothesis_status.md','phase2_exit_decision.md','phase2_readiness_report.md']
EXCLUDE={'source_manifest.json','source_hashes.csv','provenance_validation.md'}
INPUTS=[
('experiments/phase2g/finalize_package.py','package_qa_code','Integrated package structure, claims, link, and provenance checks.'),
('reports/experiments/ASFT-V1.1-PHASE-2A-REPRESENTATION-AUDIT-V1/phase2A_readiness_review.md','phase2a_evidence','Representation audit and original phase gate status.'),
('reports/experiments/ASFT-V1.1-PHASE-2A-REPRESENTATION-AUDIT-V1/historical_representation_audit.md','phase2a_evidence','Historical Phase 13G language, budget, and coverage audit.'),
('reports/experiments/ASFT-V1.1-PHASE-2A-REPRESENTATION-AUDIT-V1/primitive_inventory.csv','phase2a_evidence','Phase 13G primitive inventory.'),
('reports/experiments/ASFT-V1.1-PHASE-2A-REPRESENTATION-AUDIT-V1/missing_concepts_audit.md','phase2a_evidence','Missing/partial solution concepts.'),
('reports/experiments/ASFT-V1.1-PHASE-2A-REPRESENTATION-AUDIT-V1/representation_bottleneck_assessment.md','phase2a_evidence','Prior representation hypothesis grade.'),
('reports/experiments/ASFT-V1.1-PHASE-2B-ARC-COVERAGE-BENCHMARK-V1/phase2B_readiness_review.md','phase2b_evidence','Coverage benchmark and isolation status.'),
('reports/experiments/ASFT-V1.1-PHASE-2B-ARC-COVERAGE-BENCHMARK-V1/coverage_summary_by_split.csv','phase2b_data','Saved Phase 2B split/condition coverage.'),
('reports/experiments/ASFT-V1.1-PHASE-2B-ARC-COVERAGE-BENCHMARK-V1/run_manifest.json','phase2b_manifest','Phase 2B run scope, task, and integrity record.'),
('experiments/phase2c/config.json','phase2c_protocol','Frozen B1-B6 search budget configuration.'),
('experiments/phase2c/budget_registry.yaml','phase2c_protocol','Budget source of truth and historical mismatch.'),
('reports/experiments/ASFT-V1.1-PHASE-2C-SEARCH-BUDGET-AUDIT-V1/phase2C_readiness_review.md','phase2c_evidence','Search-budget audit results and parity decision.'),
('reports/experiments/ASFT-V1.1-PHASE-2C-SEARCH-BUDGET-AUDIT-V1/budget_sensitivity_summary.csv','phase2c_data','S1-S4 coverage sensitivity results.'),
('reports/experiments/ASFT-V1.1-PHASE-2C-SEARCH-BUDGET-AUDIT-V1/replay_validation.csv','phase2c_data','Deterministic replay validation.'),
('reports/experiments/ASFT-V1.1-PHASE-2C-SEARCH-BUDGET-AUDIT-V1/runtime_integrity_record.json','phase2c_data','B1-B6 parity and runtime integrity.'),
('reports/experiments/ASFT-V1.1-PHASE-2D-TRACE-GENERATION-AUDIT-V1/phase2D_readiness_review.md','phase2d_evidence','Trace validity/yield/diversity and readiness.'),
('reports/experiments/ASFT-V1.1-PHASE-2D-TRACE-GENERATION-AUDIT-V1/trace_lifecycle_summary.csv','phase2d_data','Trace lifecycle stage counts.'),
('reports/experiments/ASFT-V1.1-PHASE-2D-TRACE-GENERATION-AUDIT-V1/invariant_readiness_summary.csv','phase2d_data','TraceMiner inputs and invariant-readiness counts.'),
('reports/experiments/ASFT-V1.1-PHASE-2E-INVARIANT-DISCOVERY-AUDIT-V1/phase2E_readiness_review.md','phase2e_evidence','Recurrence, support, candidate, validation, and status.'),
('reports/experiments/ASFT-V1.1-PHASE-2E-INVARIANT-DISCOVERY-AUDIT-V1/recurrence_summary.csv','phase2e_data','Prethreshold operation-signature support.'),
('reports/experiments/ASFT-V1.1-PHASE-2E-INVARIANT-DISCOVERY-AUDIT-V1/candidate_generation_audit.csv','phase2e_data','Current/relaxed/strict candidate stage results.'),
('reports/experiments/ASFT-V1.1-PHASE-2E-INVARIANT-DISCOVERY-AUDIT-V1/validation_diagnostic_summary.csv','phase2e_data','Diagnostic validator counts and limits.'),
('reports/experiments/ASFT-V1.1-PHASE-2F-REPRESENTATION-ALTERNATIVES-V1/phase2F_readiness_review.md','phase2f_evidence','Representation framework readiness and outstanding gates.'),
('reports/experiments/ASFT-V1.1-PHASE-2F-REPRESENTATION-ALTERNATIVES-V1/representation_registry.csv','phase2f_data','R0/R1, alternatives, HCC, and implementation status.'),
('reports/experiments/ASFT-V1.1-PHASE-2F-REPRESENTATION-ALTERNATIVES-V1/phase2F_framework_config.json','phase2f_data','Common budgets, task-set caveats, and preregistration gates.'),
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
 for n in REQ:
  if not (PKG/n).is_file():errors.append('Missing deliverable '+n)
 matrix=read_csv('arc_readiness_matrix.csv')
 if len(matrix)<10:errors.append(f'Expected integrated readiness matrix of >=10 rows, got {len(matrix)}')
 if not any(r['area']=='ARC mechanism-level readiness' and r['status']=='BLOCKED' for r in matrix):errors.append('Mechanism readiness must be BLOCKED')
 if not any(r['area']=='Alternative representation framework' and r['status']=='PARTIAL' for r in matrix):errors.append('Alternative framework implementation status not captured')
 for p in PKG.glob('*.csv'):
  try:read_csv(p.name)
  except Exception as e:errors.append(f'CSV parse failure {p.name}: {e}')
 # Scope and exit decision manifest.
 integrated={'phase':'ASFT-V1.1-PHASE-2G','package':'ASFT-V1.1-PHASE-2G-ARC-FOUNDATION-READINESS-V1',
  'review_only_no_new_arc_science_or_search':True,'test_outputs_parsed_or_used':False,
  'phase2_exit_decision':'PARTIAL','arc_mechanism_testing':'BLOCKED',
  'representation_hypothesis':'H4_UNRESOLVED','confirmatory_authorization':False,
  'historical_holdout_pristine':False,'all_phase2c_1000_task_ids_previously_audited':True,
  'accuracy_measured_in_phase2g':False,'status':'FOUNDATION_READINESS_REVIEW_COMPLETE'}
 (PKG/'phase2G_integrated_manifest.json').write_text(json.dumps(integrated,indent=2)+'\n')
 try:
  data=json.loads((PKG/'phase2G_integrated_manifest.json').read_text())
  if data.get('phase2_exit_decision')!='PARTIAL' or data.get('arc_mechanism_testing')!='BLOCKED':errors.append('Exit/authorization decision inconsistent')
  if data.get('test_outputs_parsed_or_used') is not False:errors.append('Test-output scope violation')
 except Exception as e:errors.append(f'Integrated manifest invalid: {e}')
 # Links
 link_re=re.compile(r'\[[^\]]*\]\(([^)]+)\)');links=0
 for md in PKG.glob('*.md'):
  for target in link_re.findall(md.read_text(encoding='utf-8')):
   target=target.strip().split('#',1)[0]
   if not target or re.match(r'^[a-z]+://',target):continue
   links+=1
   if not (md.parent/target).resolve().exists():errors.append(f'Broken local link {md.name}: {target}')
 # Provenance inventory
 entries=[]
 for p in sorted(PKG.iterdir()):
  if p.is_file() and p.name not in EXCLUDE:
   entries.append({'path':p.relative_to(ROOT).as_posix(),'kind':'phase2g_integrated_artifact','note':'Integrated readiness report, matrix, or manifest.'})
 for path,kind,note in INPUTS:
  p=ROOT/path
  if not p.is_file():errors.append('Missing provenance input '+path);continue
  entries.append({'path':path,'kind':kind,'note':note})
 for e in entries:
  p=ROOT/e['path'];e['sha256']=sha(p);e['bytes']=p.stat().st_size
 sm={'phase':'ASFT-V1.1-PHASE-2G','package':'ASFT-V1.1-PHASE-2G-ARC-FOUNDATION-READINESS-V1',
  'scope':'Read-only integration of Phases 2A-2F. No new ARC search, test scoring, or representation comparison.',
  'record_count':len(entries),'records':entries}
 (PKG/'source_manifest.json').write_text(json.dumps(sm,indent=2)+'\n')
 with (PKG/'source_hashes.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=['path','kind','sha256','bytes','note']);w.writeheader();w.writerows(entries)
 verified=sum(sha(ROOT/e['path'])==e['sha256'] for e in entries)
 if verified!=len(entries):errors.append('Provenance digest mismatch')
 status='PASS' if not errors else 'FAIL'
 report=(f'# Phase 2G provenance and package QA\n\n**Status: {status}.**\n\n'
  f'- Required deliverables: {sum((PKG/n).is_file() for n in REQ)}/{len(REQ)} present.\n'
  f'- Readiness matrix rows: {len(matrix)}; mechanism readiness correctly BLOCKED.\n'
  f'- Local Markdown links checked: {links}.\n'
  f'- Provenance records hashed and verified: {verified}/{len(entries)}.\n'
  f'- Phase 2G new ARC searches/scoring: **None**; test-output use: **No**; accuracy measured: **No**.\n'
  f'- Integrated decision recorded: Phase 2 exit **PARTIAL**; confirmatory mechanism testing **BLOCKED**.\n')
 if errors:report+='\n## Errors\n\n'+'\n'.join('- '+e for e in errors)+'\n'
 (PKG/'provenance_validation.md').write_text(report)
 print(report)
 if errors:raise SystemExit(1)
if __name__=='__main__':main()
