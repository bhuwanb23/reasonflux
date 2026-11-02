"""Reconstruct Phase 13G transfer program-probe call/trial counts from train demos only."""
from __future__ import annotations
import csv,json,sys
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'experiments')]
from phase13g.common import PROGRAMS,infer_context
from phase2c.search_budget_benchmark import read_train_only
OUT=ROOT/'reports/experiments/ASFT-V1.1-PHASE-2C-SEARCH-BUDGET-AUDIT-V1'
MANIFEST=ROOT/'datasets/arc/arc-agi-2/split_manifest.json'

def baseline_search(demos):
 tried=0
 for p in PROGRAMS[:3]:
  tried+=1
  if infer_context(p,demos) is not None:return p,tried,True
 return '',tried,False

def main():
 rows=json.loads(MANIFEST.read_text())['tasks'];transfer=[r for r in rows if r['split']=='transfer']
 if len(transfer)!=200:raise SystemExit('Expected 200 transfer tasks')
 stats={p:{'program':p,'probe_calls':0,'probe_candidate_trials':0,'demo_fit_applications':0,'conditional_baseline_calls':0,'baseline_candidate_trials':0,'baseline_demo_fits':0} for p in PROGRAMS}
 for row in transfer:
  demos=read_train_only(ROOT/'datasets/arc'/row['path'])
  for p in PROGRAMS:
   s=stats[p];s['probe_calls']+=1;s['probe_candidate_trials']+=1
   applicable=infer_context(p,demos) is not None
   if applicable:
    s['demo_fit_applications']+=1;s['conditional_baseline_calls']+=1
    _,trials,fit=baseline_search(demos);s['baseline_candidate_trials']+=trials;s['baseline_demo_fits']+=int(fit)
 out=list(stats.values())
 with (OUT/'historical_transfer_probe_reconstruction.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(out[0]));w.writeheader();w.writerows(out)
 summary={'transfer_task_ids':200,'programs':len(PROGRAMS),'program_specific_probe_calls':sum(x['probe_calls'] for x in out),
  'program_specific_candidate_trials':sum(x['probe_candidate_trials'] for x in out),
  'conditional_baseline_calls':sum(x['conditional_baseline_calls'] for x in out),
  'conditional_baseline_candidate_trials':sum(x['baseline_candidate_trials'] for x in out),
  'conditional_baseline_demo_fits':sum(x['baseline_demo_fits'] for x in out),
  'test_output_fields_parsed_or_used':False,'accuracy_measured':False,
  'status':'TRAIN_DEMO_ONLY_CODE_PATH_RECONSTRUCTION_NOT_ORIGINAL_PER_TASK_LOG'}
 (OUT/'historical_transfer_probe_reconstruction.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
if __name__=='__main__':main()
