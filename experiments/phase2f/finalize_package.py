from __future__ import annotations
import csv,hashlib,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PKG=ROOT/'reports/experiments/ASFT-V1.1-PHASE-2F-REPRESENTATION-ALTERNATIVES-V1'
REQ=['representation_hypothesis_audit.md','representation_registry.csv','representation_taxonomy.md',
'coverage_comparison_framework.md','trace_comparison_framework.md','invariant_comparison_framework.md',
'activation_comparison_framework.md','bottleneck_attribution_framework.md','representation_reporting_standard.md','phase2F_readiness_review.md']
EXCLUDE={'source_manifest.json','source_hashes.csv','provenance_validation.md'}
INPUTS=[
('experiments/phase2f/build_framework.py','framework_builder_code','Generates the machine-readable registry, comparison matrix and config.'),
('experiments/phase2f/finalize_package.py','package_qa_code','Final package count, link, scope, and provenance verification.'),
('reports/experiments/ASFT-V1.1-PHASE-2A-REPRESENTATION-AUDIT-V1/README.md','prior_phase_protocol','Phase 2A audit context and prior alternative requirements.'),
('reports/experiments/ASFT-V1.1-PHASE-2A-REPRESENTATION-AUDIT-V1/historical_representation_audit.md','prior_phase_evidence','Source-based historical representation and coverage audit.'),
('reports/experiments/ASFT-V1.1-PHASE-2A-REPRESENTATION-AUDIT-V1/missing_concepts_audit.md','prior_phase_evidence','Missing/partial representation concepts and limits.'),
('reports/experiments/ASFT-V1.1-PHASE-2A-REPRESENTATION-AUDIT-V1/representation_bottleneck_assessment.md','prior_phase_evidence','Prior B2 representation hypothesis assessment.'),
('reports/experiments/ASFT-V1.1-PHASE-2A-REPRESENTATION-AUDIT-V1/representation_requirements_v2.md','prior_phase_design','R0/R1/HCC and matched design requirements.'),
('reports/experiments/ASFT-V1.1-PHASE-2A-REPRESENTATION-AUDIT-V1/primitive_inventory.csv','prior_phase_evidence','Ten-program DSL and auxiliary/helper inventory.'),
('reports/experiments/ASFT-V1.1-PHASE-2B-ARC-COVERAGE-BENCHMARK-V1/phase2B_readiness_review.md','prior_phase_evidence','Budgeted/fullscan coverage results and boundaries.'),
('reports/experiments/ASFT-V1.1-PHASE-2B-ARC-COVERAGE-BENCHMARK-V1/coverage_summary_by_split.csv','prior_phase_data','Saved Phase 2B coverage results.'),
('experiments/phase2c/config.json','frozen_budget_reference','Frozen B1-B6 conditions and test-blind scope.'),
('experiments/phase2c/budget_registry.yaml','frozen_budget_reference','Budget registry and historical mismatch.'),
('experiments/phase2c/preregistration.md','frozen_budget_reference','Phase 2C search, task, and data-isolation protocol.'),
('experiments/phase2c/search_budget_benchmark.py','reference_runner','Corrected search/coverage runner and deterministic conditions.'),
('reports/experiments/ASFT-V1.1-PHASE-2C-SEARCH-BUDGET-AUDIT-V1/budget_sensitivity_summary.csv','prior_phase_data','S1-S4 coverage sensitivity by fixed DSL.'),
('reports/experiments/ASFT-V1.1-PHASE-2C-SEARCH-BUDGET-AUDIT-V1/search_execution_log.csv','prior_phase_data','Saved test-output-blind task-condition logs.'),
('reports/experiments/ASFT-V1.1-PHASE-2D-TRACE-GENERATION-AUDIT-V1/phase2D_readiness_review.md','prior_phase_evidence','Trace generation yield and validation results.'),
('reports/experiments/ASFT-V1.1-PHASE-2E-INVARIANT-DISCOVERY-AUDIT-V1/phase2E_readiness_review.md','prior_phase_evidence','Recurrence, support, candidate, and validator findings.'),
('experiments/phase13g/common.py','historical_representation_source','Frozen ten-program source and trace construction.'),
('experiments/phase13g/runner.py','historical_pipeline_source','Historical miner, skill, transfer, and capability orchestration.'),
('experiments/phase13g/config.json','historical_protocol_source','Original historical representation/budget configuration.'),
('src/invariants/detector.py','downstream_runtime_source','Frozen TraceMiner and candidate validation orchestration.'),
('src/invariants/pattern_mining.py','downstream_runtime_source','Pattern extraction thresholds.'),
('src/invariants/candidate_generation.py','downstream_runtime_source','Candidate generation interface.'),
('src/invariants/validator.py','downstream_runtime_source','Invariant validator state transitions.'),
('src/skills/qualification.py','downstream_runtime_source','Existing skill qualification rules.'),
('src/skills/config.py','downstream_runtime_source','Existing SkillConfig.'),
('src/capability/config.py','downstream_runtime_source','Existing CapabilityConfig.'),
]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1<<20),b''):h.update(b)
 return h.hexdigest()
def csvrows(name):
 with (PKG/name).open(newline='',encoding='utf-8') as f:return list(csv.DictReader(f))
def main():
 errors=[]
 for n in REQ:
  if not (PKG/n).is_file():errors.append('Missing required deliverable: '+n)
 registry=csvrows('representation_registry.csv');matrix=csvrows('comparison_matrix.csv')
 if len(registry)!=9:errors.append(f'Expected 9 registry rows (R0-R7+HCC), got {len(registry)}')
 ids={r['representation_id'] for r in registry}
 if ids!={'R0','R1','R2','R3','R4','R5','R6','R7','HCC'}:errors.append('Registry IDs incomplete')
 if len(matrix)!=6:errors.append(f'Expected 6 comparison rows, got {len(matrix)}')
 for r in registry:
  for fld in ['primitive_inventory_json','object_model','relation_model','composition_model','search_interface','parameterization_semantics']:
   if not r.get(fld):errors.append(f'{r["representation_id"]} missing registry field {fld}')
  if r['representation_id'] in {'R2','R3','R4','R5','R6','R7'} and r['implementation_state']!='NOT_IMPLEMENTED_OR_RUN':errors.append('Alternative falsely marked implemented')
 try:
  cfg=json.loads((PKG/'phase2F_framework_config.json').read_text())
  if cfg.get('status')!='FRAMEWORK_ONLY_NO_REPRESENTATION_COMPARISON_RUN':errors.append('Framework status not explicit')
  if cfg.get('common_task_data',{}).get('test_outputs_parsed_or_used') is not False:errors.append('Test-output scope guard failed')
  if cfg.get('common_search_budget',{}).get('candidate_trials_per_task')!=10:errors.append('Common B1 reference budget mismatch')
  if cfg.get('downstream_frozen',{}).get('min_frequency')!=5:errors.append('Downstream support threshold not frozen')
 except Exception as e:errors.append(f'Framework JSON invalid: {e}')
 for p in PKG.glob('*.csv'):
  try:csvrows(p.name)
  except Exception as e:errors.append(f'CSV parse failure {p.name}: {e}')
 # Local markdown links
 links=0;link_re=re.compile(r'\[[^\]]*\]\(([^)]+)\)')
 for md in PKG.glob('*.md'):
  for target in link_re.findall(md.read_text(encoding='utf-8')):
   target=target.strip().split('#',1)[0]
   if not target or re.match(r'^[a-z]+://',target):continue
   links+=1
   if not (md.parent/target).resolve().exists():errors.append(f'Broken link in {md.name}: {target}')
 # Source/artifact manifest
 entries=[]
 for p in sorted(PKG.iterdir()):
  if p.is_file() and p.name not in EXCLUDE:
   entries.append({'path':p.relative_to(ROOT).as_posix(),'kind':'phase2f_package_artifact','note':'Final Phase 2F report, registry, matrix, or config.'})
 for path,kind,note in INPUTS:
  p=ROOT/path
  if not p.is_file():errors.append('Missing provenance input: '+path);continue
  entries.append({'path':path,'kind':kind,'note':note})
 for e in entries:
  p=ROOT/e['path'];e['sha256']=sha(p);e['bytes']=p.stat().st_size
 manifest={'phase':'ASFT-V1.1-PHASE-2F','package':'ASFT-V1.1-PHASE-2F-REPRESENTATION-ALTERNATIVES-V1',
  'scope':'Framework specification only; no alternative representation implementation or ARC comparison run.',
  'record_count':len(entries),'records':entries}
 (PKG/'source_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 with (PKG/'source_hashes.csv').open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=['path','kind','sha256','bytes','note']);w.writeheader();w.writerows(entries)
 verified=sum(sha(ROOT/e['path'])==e['sha256'] for e in entries)
 if verified!=len(entries):errors.append('Provenance verification mismatch')
 status='PASS' if not errors else 'FAIL'
 report=(f'# Phase 2F provenance and package QA\n\n**Status: {status}.**\n\n'
  f'- Required Markdown deliverables: {sum((PKG/n).is_file() for n in REQ if n.endswith(".md"))}/9 present.\n'
  f'- Representation registry rows: {len(registry)}; alternatives specified: 6; implementation/run status: not implemented.\n'
  f'- Comparison matrix contrasts: {len(matrix)}; HCC control specified, not built/run.\n'
  f'- Local Markdown links checked: {links}.\n'
  f'- Provenance records hashed and verified: {verified}/{len(entries)}.\n'
  f'- ARC comparison/search/test scoring: **Not run**; test-output use: **No**; accuracy: **Not measured**.\n'
  f'- Confirmatory execution readiness: **Not ready**; source/reporting scope remains specification only.\n'
  f'- Interpretation: no representation effect, ASFT mechanism, transfer, capability, or accuracy claim.\n')
 if errors:report+='\n## Errors\n\n'+'\n'.join('- '+e for e in errors)+'\n'
 (PKG/'provenance_validation.md').write_text(report)
 print(report)
 if errors:raise SystemExit(1)
if __name__=='__main__':main()
