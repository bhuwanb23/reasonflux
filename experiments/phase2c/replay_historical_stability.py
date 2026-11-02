"""Training-demo-only replay of Phase 13G's 10-permutation search-stability diagnostic."""
from __future__ import annotations
import csv,hashlib,json,random,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT/'experiments'))
from phase13g.common import PROGRAMS,infer_context
OUT=ROOT/'reports/experiments/ASFT-V1.1-PHASE-2C-SEARCH-BUDGET-AUDIT-V1'
SPLIT=ROOT/'datasets/arc/arc-agi-2/split_manifest.json'
QUALITY=ROOT/'reports/experiments/PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/discovery_trace_quality.csv'
TRACES=ROOT/'reports/experiments/PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1/discovery_traces.jsonl'

def read_train(path):
 with path.open(encoding='utf-8') as f:
  def ws():
   c=f.read(1)
   while c and c.isspace():c=f.read(1)
   return c
  if ws()!='{':raise ValueError('bad task root')
  if ws()!='"':raise ValueError('first key not train')
  q=['"'];esc=False
  while True:
   c=f.read(1)
   if not c:raise ValueError('truncated key')
   q.append(c)
   if esc:esc=False
   elif c=='\\':esc=True
   elif c=='"':break
  if json.loads(''.join(q))!='train' or ws()!=':':raise ValueError('unexpected task key')
  if ws()!='[':raise ValueError('train not array')
  out=['['];d=1;quoted=False;esc=False
  while d:
   c=f.read(1)
   if not c:raise ValueError('truncated train')
   out.append(c)
   if quoted:
    if esc:esc=False
    elif c=='\\':esc=True
    elif c=='"':quoted=False
   else:
    if c=='"':quoted=True
    elif c=='[':d+=1
    elif c==']':d-=1
 return json.loads(''.join(out))

def search(demos):
 tried=0
 for p in PROGRAMS:
  tried+=1
  ctx=infer_context(p,demos)
  if ctx is not None:return p,tried
 return '',tried

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 split=json.loads(SPLIT.read_text());refs=[r for r in split['tasks'] if r['split']=='discovery']
 quality={r['task_id']:r for r in csv.DictReader(QUALITY.open(newline='',encoding='utf-8'))}
 saved={json.loads(line)['task_id']:json.loads(line) for line in TRACES.read_text().splitlines() if line.strip()}
 if len(refs)!=600 or len(quality)!=600 or len(saved)!=600:raise SystemExit('historical discovery count mismatch')
 primary_mismatch=stability_mismatch=0;main_trials=permutation_trials=0;perm_rows=[];task_rows=[]
 for row in refs:
  tid=row['task_id'];demos=read_train(ROOT/'datasets/arc'/row['path']);primary,pt=search(demos);main_trials+=pt
  q=quality[tid];trace=saved[tid];stored_result=(trace.get('outcome') or {}).get('result') or {};stored_cost=(trace.get('outcome') or {}).get('cost')
  if primary!=q['program'] or (primary!='' and not bool(q['demo_fit'])) or (primary=='' and q['demo_fit']=='True') or stored_result.get('program','')!=primary or int(stored_cost or 0)!=pt:primary_mismatch+=1
  key=int(hashlib.sha256(('phase13g-stability:'+tid).encode()).hexdigest()[:16],16);rng=random.Random(key+1307)
  stable=0;total_trials=0
  for j in range(10):
   perm=list(demos);rng.shuffle(perm);selected,trials=search(perm);total_trials+=trials;permutation_trials+=trials
   same=bool(primary and selected==primary);stable+=int(same)
   perm_rows.append({'task_id':tid,'permutation':j+1,'candidate_trials':trials,'selected_program':selected,
     'primary_program':primary,'matches_primary':same})
  calculated=(stable/10) if primary else None
  saved_stability=float(q['stability']) if q['stability'] not in ('','None','null') else None
  equal=(calculated==saved_stability)
  if not equal:stability_mismatch+=1
  task_rows.append({'task_id':tid,'primary_program_reproduced':primary==q['program'],'primary_candidate_trials_reproduced':int(stored_cost or 0)==pt,
    'primary_candidate_trials':pt,'stability_permutations':10,'permutation_candidate_trials_total':total_trials,
    'reproduced_stability':calculated if calculated is not None else 'NOT_APPLICABLE_NO_PRIMARY_FIT',
    'saved_stability':saved_stability if saved_stability is not None else 'NOT_APPLICABLE_NO_PRIMARY_FIT','stability_exact_match':equal})
 with (OUT/'historical_stability_search_log.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(perm_rows[0]));w.writeheader();w.writerows(perm_rows)
 with (OUT/'historical_stability_task_audit.csv').open('w',newline='') as f:
  w=csv.DictWriter(f,fieldnames=list(task_rows[0]));w.writeheader();w.writerows(task_rows)
 summary={'task_count':600,'permutation_searches':len(perm_rows),'primary_search_candidate_trials':main_trials,
  'stability_replay_candidate_trials':permutation_trials,'primary_result_or_trial_count_mismatches':primary_mismatch,
  'saved_stability_value_mismatches':stability_mismatch,'saved_trace_permutation_count':10,
  'test_outputs_parsed_or_used':False,'accuracy_measured':False,
  'status':'EXACT_REPRODUCTION' if primary_mismatch==0 and stability_mismatch==0 else 'MISMATCH'}
 (OUT/'historical_stability_replay_summary.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps(summary,indent=2))
 if summary['status']!='EXACT_REPRODUCTION':raise SystemExit(1)
if __name__=='__main__':main()
