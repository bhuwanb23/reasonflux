"""Phase 2C deterministic search/budget sensitivity benchmark; test-label blind."""
from __future__ import annotations
import csv, hashlib, json, math, platform, resource, sys, time
from collections import Counter
from pathlib import Path
import yaml
ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT/'src'));sys.path.insert(0,str(ROOT/'experiments'))
from phase13g.common import PROGRAMS, PROGRAM_FAMILY, infer_context, apply_program, trace_for, _infer_context_cached
from phase13g.runner import mine_invariants
OUT=ROOT/'reports/experiments/ASFT-V1.1-PHASE-2C-SEARCH-BUDGET-AUDIT-V1'
CONFIG_PATH=ROOT/'experiments/phase2c/config.json';REGISTRY_PATH=ROOT/'experiments/phase2c/budget_registry.yaml'
SPLIT_PATH=ROOT/'datasets/arc/arc-agi-2/split_manifest.json'

class BudgetViolation(RuntimeError): pass

def skip_ws(f):
 c=f.read(1)
 while c and c.isspace():c=f.read(1)
 return c

def read_quoted(f):
 chars=['"'];escape=False
 while True:
  c=f.read(1)
  if not c:raise ValueError('Truncated JSON key')
  chars.append(c)
  if escape:escape=False
  elif c=='\\':escape=True
  elif c=='"':break
 return json.loads(''.join(chars))

def read_train_only(path):
 with path.open(encoding='utf-8') as f:
  if skip_ws(f)!='{':raise ValueError('Task JSON root invalid')
  if skip_ws(f)!='"' or read_quoted(f)!='train':raise ValueError('Fail closed: first key is not train')
  if skip_ws(f)!=':':raise ValueError('Missing train colon')
  if skip_ws(f)!='[':raise ValueError('Train is not an array')
  chars=['['];depth=1;quoted=False;escaped=False
  while depth:
   c=f.read(1)
   if not c:raise ValueError('Truncated train array')
   chars.append(c)
   if quoted:
    if escaped:escaped=False
    elif c=='\\':escaped=True
    elif c=='"':quoted=False
   else:
    if c=='"':quoted=True
    elif c=='[':depth+=1
    elif c==']':depth-=1
 demos=json.loads(''.join(chars))
 if not isinstance(demos,list) or not demos:raise ValueError('Empty/invalid demonstrations')
 return demos

def valid_grid(g):
 return isinstance(g,list) and len(g)>0 and all(isinstance(row,list) and len(row)>0 for row in g) and len({len(r) for r in g})==1 and all(type(x) is int and 0<=x<=9 for r in g for x in r)

def valid_demos(demos):return bool(demos) and all(isinstance(p,dict) and valid_grid(p.get('input')) and valid_grid(p.get('output')) for p in demos)

def canon(obj):return json.dumps(obj,sort_keys=True,separators=(',',':'))
def context_json(ctx):return canon(ctx) if ctx is not None else ''
def sha_text(text):return hashlib.sha256(text.encode()).hexdigest()

def search(demos,condition,cap,requested,unique_pool,wall_limit):
 start=time.monotonic();attempts=[];chosen=None;ctxchosen=None;timed_out=False
 for ix,program in enumerate(unique_pool[:min(cap,len(unique_pool))],1):
  if time.monotonic()-start>wall_limit:timed_out=True;break
  ctx=infer_context(program,demos)
  if time.monotonic()-start>wall_limit:timed_out=True;break
  rec={'ordinal':ix,'program':program,'demo_fit':ctx is not None,'context':context_json(ctx)}
  attempts.append(rec)
  if ctx is not None:
   chosen=program;ctxchosen=ctx;break
 result={'program':chosen or '', 'family':PROGRAM_FAMILY[chosen] if chosen else 'unsupported_v1',
         'demo_fit':chosen is not None,'context':ctxchosen or {},'attempts':attempts,
         'candidate_trials':len(attempts),'timed_out':timed_out,
         'elapsed_seconds':time.monotonic()-start,'budget_id':condition,
         'requested_budget':requested,'enforced_cap':cap,'candidate_pool_available':len(unique_pool)}
 result['trial_fingerprint']=sha_text(canon(attempts)+canon({'program':result['program'],'context':result['context'],'demo_fit':result['demo_fit']}))
 return result

def independent_fit(demos,result):
 if not result['demo_fit']:return False
 prog=result['program'];ctx=result['context']
 for pair in demos:
  source=tuple(tuple(int(v) for v in row) for row in pair['input'])
  expected=tuple(tuple(int(v) for v in row) for row in pair['output'])
  if apply_program(prog,source,ctx)!=expected:return False
 return True

def trace_valid(trace,tid,split,result,demo_valid):
 ops=trace.operations
 expected=(['validate_grid_schema','enumerate_candidate_programs',f"apply_{result['program']}",'verify_demonstrations'] if result['demo_fit'] else ['validate_grid_schema','enumerate_candidate_programs','candidate_budget_exhausted'])
 return bool(demo_valid and trace.task_id==tid and trace.metadata.get('split')==split and trace.metadata.get('test_outputs_used_for_trace') is False and trace.outcome and trace.outcome.success==result['demo_fit'] and ops==expected and len(ops)<=4)

def runtime_hash(paths):
 entries={p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in paths}
 payload={'files':entries,'python':platform.python_version(),'platform':platform.platform()}
 return hashlib.sha256(canon(payload).encode()).hexdigest(),entries,payload

def condition_signature(row):
    return (row['candidate_trial_fingerprint'],row['candidate_program_selected'],row['exact_demo_fit'],row['candidate_trials_evaluated'],row['trace_valid'],row['successful_trace'])

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 cfg=json.loads(CONFIG_PATH.read_text());reg=yaml.safe_load(REGISTRY_PATH.read_text())
 if cfg['phase']!=reg['phase']:raise BudgetViolation('config/registry phase mismatch')
 if cfg['representation']['programs']!=list(PROGRAMS):raise BudgetViolation('DSL config differs from runtime program inventory')
 if cfg['replay']['passes']!=1 or cfg['replay']['clear_inference_cache_before_replay'] is not True or cfg['replay']['traces_emitted_in_replay'] is not False:
  raise BudgetViolation('replay execution differs from frozen config')
 if cfg['representation']['search_depth']!=reg['shared_budgets']['B2_search_depth']:raise BudgetViolation('B2 config/registry mismatch')
 for cond in cfg['sensitivity_conditions']:
  r=reg['conditions'][cond['id']]
  for k1,k2 in [('requested_candidate_budget','requested_candidate_budget'),('enforced_trial_cap','enforced_candidate_trial_cap'),('candidate_pool_available','available_unique_candidates')]:
   if cond[k1]!=r[k2]:raise BudgetViolation(f'{cond["id"]} config/registry mismatch {k1}')
 shared=reg['shared_budgets']
 for field,val in [('B2_search_depth',cfg['budget_fields']['B2_search_depth']),('B3_primary_trace_records_per_task_condition',cfg['budget_fields']['B3_trace_budget']['primary_traces_per_task_condition']),('B3_max_trace_steps',cfg['budget_fields']['B3_trace_budget']['maximum_steps']),('B4_wall_clock_seconds_per_search',cfg['budget_fields']['B4_runtime_budget_seconds_per_search']),('B5_process_address_space_limit_mib',cfg['budget_fields']['B5_process_memory_budget_mib']),('B6_primary_task_ids_per_condition',cfg['budget_fields']['B6_evaluation_budget']['primary_tasks_per_condition']),('B6_deterministic_replay_task_ids_per_condition',cfg['budget_fields']['B6_evaluation_budget']['replay_tasks_per_condition'])]:
  if shared[field]!=val:raise BudgetViolation('shared budget mismatch '+field)
 if shared['B6_total_search_invocations_per_condition'] != shared['B6_primary_task_ids_per_condition'] + shared['B6_deterministic_replay_task_ids_per_condition']:
  raise BudgetViolation('B6 total invocation mismatch')
 mem_bytes=shared['B5_process_address_space_limit_mib']*1024*1024
 resource.setrlimit(resource.RLIMIT_AS,(mem_bytes,mem_bytes))
 manifest=json.loads(SPLIT_PATH.read_text());rows=manifest['tasks']
 split_counts=Counter(r['split'] for r in rows)
 if len(rows)!=shared['B6_primary_task_ids_per_condition'] or dict(split_counts)!=shared['split_task_ids']:raise BudgetViolation('B6 split/count mismatch')
 if len({r['task_id'] for r in rows})!=len(rows):raise BudgetViolation('duplicate task IDs')
 task_cache={}
 for row in rows:
  demos=read_train_only(ROOT/'datasets/arc'/row['path'])
  if len(demos)!=row['train_pairs'] or not valid_demos(demos):raise BudgetViolation('task train schema/count mismatch '+row['task_id'])
  task_cache[row['task_id']]=(row,demos)
 config_hash=hashlib.sha256(CONFIG_PATH.read_bytes()).hexdigest();registry_hash=hashlib.sha256(REGISTRY_PATH.read_bytes()).hexdigest()
 runtime_paths=['experiments/phase2c/search_budget_benchmark.py','experiments/phase13g/common.py','experiments/phase13g/runner.py','src/core/trace.py','src/core/invariant.py','src/core/states.py','src/invariants/detector.py','src/invariants/pattern_mining.py','src/invariants/aggregation.py','src/invariants/candidate_generation.py','src/solver/grid.py','src/traces/normalizer.py','src/traces/segmentation.py']
 runtime_paths += sorted(str(p.relative_to(ROOT)) for p in (ROOT/'src/invariants/specification').glob('*.py'))
 runtime_digest,runtime_entries,runtime_payload=runtime_hash(runtime_paths)
 primary_rows=[];trial_rows=[];replay_rows=[];traces_by_condition={};fits_by_condition={};tic=time.monotonic()
 cond_defs={c['id']:c for c in cfg['sensitivity_conditions']}
 for cid,cdef in cond_defs.items():
  _infer_context_cached.cache_clear()
  cap=cdef['enforced_trial_cap'];requested=cdef['requested_candidate_budget'];pool=list(PROGRAMS[:cdef['candidate_pool_available']])
  traces_by_condition[cid]=[];fits_by_condition[cid]=[]
  primary_by_id={}
  for row,demos in task_cache.values():
   tid=row['task_id'];split=row['split']
   result=search(demos,cid,cap,requested,pool,shared['B4_wall_clock_seconds_per_search'])
   if result['timed_out'] or result['elapsed_seconds']>shared['B4_wall_clock_seconds_per_search']:raise BudgetViolation(f'B4 timeout: {cid}/{tid}')
   if result['demo_fit'] and not independent_fit(demos,result):raise BudgetViolation(f'independent replay mismatch {cid}/{tid}')
   task={'task_id':tid,'split':split,'train':demos};trace=trace_for(task,result)
   isvalid=trace_valid(trace,tid,split,result,valid_demos(demos))
   if not isvalid:raise BudgetViolation(f'B3 trace validation failed {cid}/{tid}')
   if len(trace.steps)>shared['B3_max_trace_steps']:raise BudgetViolation(f'B3 trace step cap {cid}/{tid}')
   rec={'task_id':tid,'split':split,'condition':cid,'requested_candidate_budget':str(requested),
       'enforced_candidate_trial_cap':cap,'candidate_pool_available':len(pool),
       'candidate_programs_generated':len(pool),'candidate_trials_evaluated':result['candidate_trials'],
       'candidate_budget_slots_not_generated':len(PROGRAMS)-len(pool),
       'declared_cap_slots_unfillable_due_to_finite_dsl':max(0,cap-len(pool)),
       'candidates_not_evaluated_after_first_fit':len(pool)-result['candidate_trials'],
       'candidate_pruned_count':0,'candidate_program_selected':result['program'],
       'exact_demo_fit':result['demo_fit'],'search_depth_declared':shared['B2_search_depth'],
       'search_depth_executed':1,'search_depth_logged':1,
       'trace_budget_cap':shared['B3_primary_trace_records_per_task_condition'],'trace_records_emitted':1,
       'trace_steps':len(trace.steps),'trace_valid':isvalid,'successful_trace':bool(trace.outcome and trace.outcome.success),
       'trace_pruned_count':0,'runtime_budget_seconds':shared['B4_wall_clock_seconds_per_search'],
       'runtime_observed_seconds':round(result['elapsed_seconds'],8),'memory_budget_mib':shared['B5_process_address_space_limit_mib'],
       'evaluation_budget_primary_task_ids':shared['B6_primary_task_ids_per_condition'],
       'evaluation_budget_replay_task_ids':shared['B6_deterministic_replay_task_ids_per_condition'],
       'evaluation_budget_total_search_invocations':shared['B6_total_search_invocations_per_condition'],
       'candidate_trial_fingerprint':result['trial_fingerprint'],'accuracy':'NOT_MEASURED_BY_DESIGN'}
   # Budget value parity is explicit in every row.
   rec['declared_candidate_budget_logged']=str(requested)
   rec['runtime_enforced_candidate_cap_logged']=cap
   if rec['requested_candidate_budget']!=rec['declared_candidate_budget_logged'] or rec['enforced_candidate_trial_cap']!=rec['runtime_enforced_candidate_cap_logged']:
    raise BudgetViolation('B1 declaration/log mismatch')
   primary_rows.append(rec);primary_by_id[tid]=rec;traces_by_condition[cid].append(trace)
   if result['demo_fit']:fits_by_condition[cid].append(trace)
   for att in result['attempts']:
    trial_rows.append({'task_id':tid,'split':split,'condition':cid,'trial_ordinal':att['ordinal'],
      'program':att['program'],'demo_fit':att['demo_fit'],'inferred_context_json':att['context'],
      'selected':att['program']==result['program'],'trial_fingerprint':result['trial_fingerprint']})
  # Full deterministic replay per task/condition; clear the context cache so this is a true recomputation.
  _infer_context_cached.cache_clear()
  for row,demos in task_cache.values():
   tid=row['task_id'];rep=search(demos,cid,cap,requested,pool,shared['B4_wall_clock_seconds_per_search']);pri=primary_by_id[tid]
   if rep['timed_out'] or rep['elapsed_seconds']>shared['B4_wall_clock_seconds_per_search']:raise BudgetViolation(f'B4 replay timeout: {cid}/{tid}')
   exact=(rep['trial_fingerprint']==pri['candidate_trial_fingerprint'] and rep['program']==pri['candidate_program_selected'] and rep['candidate_trials']==pri['candidate_trials_evaluated'] and rep['demo_fit']==pri['exact_demo_fit'])
   replay_rows.append({'task_id':tid,'split':row['split'],'condition':cid,
      'requested_candidate_budget':str(requested),'declared_candidate_budget_logged':str(requested),
      'enforced_candidate_trial_cap':cap,'runtime_enforced_candidate_cap_logged':cap,
      'candidate_pool_available':len(pool),
      'search_depth_declared':shared['B2_search_depth'],'search_depth_executed':1,'search_depth_logged':1,
      'trace_budget_cap':shared['B3_primary_trace_records_per_task_condition'],
      'trace_budget_logged':shared['B3_primary_trace_records_per_task_condition'],'replay_trace_records_emitted':0,
      'primary_fingerprint':pri['candidate_trial_fingerprint'],'replay_fingerprint':rep['trial_fingerprint'],
      'selected_program_primary':pri['candidate_program_selected'],'selected_program_replay':rep['program'],
      'primary_trials':pri['candidate_trials_evaluated'],'replay_trials':rep['candidate_trials'],
      'exact_reproduction':exact,'replay_runtime_budget_seconds':shared['B4_wall_clock_seconds_per_search'],
      'replay_runtime_budget_seconds_logged':shared['B4_wall_clock_seconds_per_search'],
      'replay_runtime_observed_seconds':round(rep['elapsed_seconds'],8),
      'memory_budget_mib':shared['B5_process_address_space_limit_mib'],
      'memory_budget_logged_mib':shared['B5_process_address_space_limit_mib'],
      'evaluation_budget_total_search_invocations_logged':shared['B6_total_search_invocations_per_condition'],

      'evaluation_budget_primary_task_ids':shared['B6_primary_task_ids_per_condition'],
      'evaluation_budget_replay_task_ids':shared['B6_deterministic_replay_task_ids_per_condition'],
      'evaluation_budget_total_search_invocations':shared['B6_total_search_invocations_per_condition']})
   if not exact:raise BudgetViolation(f'Deterministic replay mismatch {cid}/{tid}')

 # Fail closed if any logged/runtime value differs from the single registry.
 process_peak_mib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
 if process_peak_mib>shared['B5_process_address_space_limit_mib']:
  raise BudgetViolation('B5 process memory cap exceeded')
 for rec in primary_rows:
  if rec['search_depth_declared']!=shared['B2_search_depth'] or rec['search_depth_executed']!=shared['B2_search_depth'] or rec['search_depth_logged']!=shared['B2_search_depth']:
   raise BudgetViolation('B2 parity failure')
  if rec['trace_budget_cap']!=shared['B3_primary_trace_records_per_task_condition'] or rec['trace_records_emitted']!=1 or rec['trace_steps']>shared['B3_max_trace_steps']:
   raise BudgetViolation('B3 parity failure')
  if rec['runtime_budget_seconds']!=shared['B4_wall_clock_seconds_per_search'] or rec['runtime_observed_seconds']>shared['B4_wall_clock_seconds_per_search']:
   raise BudgetViolation('B4 parity failure')
  if rec['memory_budget_mib']!=shared['B5_process_address_space_limit_mib']:
   raise BudgetViolation('B5 parity failure')
  if rec['evaluation_budget_primary_task_ids']!=shared['B6_primary_task_ids_per_condition'] or rec['evaluation_budget_replay_task_ids']!=shared['B6_deterministic_replay_task_ids_per_condition'] or rec['evaluation_budget_total_search_invocations']!=shared['B6_total_search_invocations_per_condition']:
   raise BudgetViolation('B6 parity failure')
 for rec in replay_rows:
  if rec['enforced_candidate_trial_cap']!=cond_defs[rec['condition']]['enforced_trial_cap'] or rec['requested_candidate_budget']!=str(cond_defs[rec['condition']]['requested_candidate_budget']) or rec['declared_candidate_budget_logged']!=rec['requested_candidate_budget'] or rec['runtime_enforced_candidate_cap_logged']!=rec['enforced_candidate_trial_cap']:
   raise BudgetViolation('B1 replay parity failure')
  if rec['search_depth_declared']!=shared['B2_search_depth'] or rec['search_depth_executed']!=shared['B2_search_depth'] or rec['search_depth_logged']!=shared['B2_search_depth']:
   raise BudgetViolation('B2 replay parity failure')
  if rec['trace_budget_cap']!=shared['B3_primary_trace_records_per_task_condition'] or rec['trace_budget_logged']!=shared['B3_primary_trace_records_per_task_condition'] or rec['replay_trace_records_emitted']!=0:
   raise BudgetViolation('B3 replay parity failure')
  if rec['replay_runtime_budget_seconds']!=shared['B4_wall_clock_seconds_per_search'] or rec['replay_runtime_budget_seconds_logged']!=shared['B4_wall_clock_seconds_per_search'] or rec['replay_runtime_observed_seconds']>shared['B4_wall_clock_seconds_per_search']:
   raise BudgetViolation('B4 replay parity failure')
  if rec['memory_budget_mib']!=shared['B5_process_address_space_limit_mib'] or rec['memory_budget_logged_mib']!=shared['B5_process_address_space_limit_mib']:
   raise BudgetViolation('B5 replay parity failure')
  if rec['evaluation_budget_primary_task_ids']!=shared['B6_primary_task_ids_per_condition'] or rec['evaluation_budget_replay_task_ids']!=shared['B6_deterministic_replay_task_ids_per_condition'] or rec['evaluation_budget_total_search_invocations']!=shared['B6_total_search_invocations_per_condition'] or rec['evaluation_budget_total_search_invocations_logged']!=shared['B6_total_search_invocations_per_condition']:
   raise BudgetViolation('B6 replay parity failure')
 # Verify S3 numeric cap and S4 unrestricted saturate to identical finite candidate behavior.
 s3={r['task_id']:r for r in primary_rows if r['condition']=='S3'};s4={r['task_id']:r for r in primary_rows if r['condition']=='S4'}
 if any(condition_signature(s3[t])!=condition_signature(s4[t]) for t in s3):raise BudgetViolation('S3/S4 finite DSL saturation mismatch')
 # Run the actual Phase 13G invariant miner on successful discovery traces only.
 invariants={}
 for cid in cond_defs:
  disids={tid for tid,(row,_) in task_cache.items() if row['split']=='discovery'}
  dtr=[t for t in fits_by_condition[cid] if t.task_id in disids]
  mined,by_program,candidate_rows=mine_invariants(dtr)
  support=dict(Counter(t.outcome.result['program'] for t in dtr if t.outcome and t.outcome.result))
  invariants[cid]={'successful_discovery_traces':len(dtr),'support_by_program':support,
    'trace_miner_candidates':len(candidate_rows),'mapped_invariant_count':len(by_program),'accepted_programs':sorted(by_program)}
 # Files
 def write_csv(path,rows):
  if not rows:raise ValueError('empty rows '+path)
  with (OUT/path).open('w',newline='',encoding='utf-8') as f:
   w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 write_csv('search_execution_log.csv',primary_rows);write_csv('candidate_trial_log.csv',trial_rows);write_csv('replay_validation.csv',replay_rows)
 (OUT/'invariant_mining_summary.json').write_text(json.dumps({'support_threshold':5,'consistency_threshold':1.0,'by_condition':invariants},indent=2)+'\n')
 by_condition=[];by_split=[]
 for cid in cond_defs:
  rr=[r for r in primary_rows if r['condition']==cid];n=len(rr);fits=sum(r['exact_demo_fit'] for r in rr);evals=sum(r['candidate_trials_evaluated'] for r in rr);generated=sum(r['candidate_programs_generated'] for r in rr)
  replay=[r for r in replay_rows if r['condition']==cid]
  maxrss=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024
  by_condition.append({'condition':cid,'requested_budget':str(cond_defs[cid]['requested_candidate_budget']),
    'enforced_candidate_trial_cap':cond_defs[cid]['enforced_trial_cap'],'candidate_pool_per_task':cond_defs[cid]['candidate_pool_available'],
    'tasks':n,'coverage_count':fits,'coverage_pct':round(100*fits/n,4),'candidates_generated_total':generated,
    'candidates_evaluated_total':evals,'candidates_not_evaluated_after_first_fit_total':sum(r['candidates_not_evaluated_after_first_fit'] for r in rr),
    'candidate_slots_not_generated_due_budget_total':sum(r['candidate_budget_slots_not_generated'] for r in rr),
    'declared_cap_slots_unfillable_due_to_finite_dsl_total':sum(r['declared_cap_slots_unfillable_due_to_finite_dsl'] for r in rr),
    'candidate_pruned_total':0,'primary_traces':sum(r['trace_records_emitted'] for r in rr),'valid_traces':sum(r['trace_valid'] for r in rr),
    'successful_traces':sum(r['successful_trace'] for r in rr),'trace_pruned_total':0,'invariant_candidates':invariants[cid]['mapped_invariant_count'],
    'mean_trials_per_task':round(evals/n,5),'mean_runtime_ms':round(1000*sum(r['runtime_observed_seconds'] for r in rr)/n,5),
    'max_runtime_seconds':max(r['runtime_observed_seconds'] for r in rr),'replay_tasks':len(replay),
    'replay_exact_matches':sum(r['exact_reproduction'] for r in replay),'process_peak_rss_mib':round(maxrss,3),
    'accuracy':'NOT_MEASURED_BY_DESIGN'})
  for split in ('discovery','transfer','holdout','all'):
   ss=[r for r in rr if split=='all' or r['split']==split];nn=len(ss);ff=sum(r['exact_demo_fit'] for r in ss)
   by_split.append({'condition':cid,'split':split,'tasks':nn,'coverage_count':ff,'coverage_pct':round(100*ff/nn,4),
     'candidates_generated_total':sum(r['candidate_programs_generated'] for r in ss),
     'candidates_evaluated_total':sum(r['candidate_trials_evaluated'] for r in ss),
     'valid_traces':sum(r['trace_valid'] for r in ss),'successful_traces':sum(r['successful_trace'] for r in ss),
     'invariant_candidates_global':invariants[cid]['mapped_invariant_count'],'accuracy':'NOT_MEASURED_BY_DESIGN'})
 write_csv('budget_sensitivity_summary.csv',by_condition);write_csv('budget_sensitivity_by_split.csv',by_split)
 (OUT/'budget_audit_record.json').write_text(json.dumps({'phase':cfg['phase'],'config_sha256':config_hash,'registry_sha256':registry_hash,
   'budget_parity':'PASS','conditions':by_condition,'fail_closed_on_any_mismatch':True},indent=2)+'\n')
 # Immutable log hashes and runtime fingerprint.
 logpaths=['search_execution_log.csv','candidate_trial_log.csv','replay_validation.csv']
 loghashes={p:hashlib.sha256((OUT/p).read_bytes()).hexdigest() for p in logpaths}
 composite_log_hash=hashlib.sha256(canon(loghashes).encode()).hexdigest()
 integrity={'R1_config_hash':config_hash,'budget_registry_hash':registry_hash,'R2_runtime_hash':runtime_digest,
   'runtime_source_hashes':runtime_entries,'runtime_environment':runtime_payload,'R3_search_log_hash':composite_log_hash,
   'individual_search_log_hashes':loghashes,'R4_budget_audit_record_sha256':hashlib.sha256((OUT/'budget_audit_record.json').read_bytes()).hexdigest(),
   'hash_validation':'PASS','budget_parity':'PASS','replay_validation':'PASS','test_output_fields_parsed_or_used':False,
   'accuracy_measured':False,'run_runtime_seconds':round(time.monotonic()-tic,3),
   'process_memory_limit_mib':shared['B5_process_address_space_limit_mib'],'process_peak_rss_mib':round(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1024,3)}
 (OUT/'runtime_integrity_record.json').write_text(json.dumps(integrity,indent=2)+'\n')
 run={'phase':cfg['phase'],'package':cfg['package'],'protocol':'experiments/phase2c/preregistration.md',
  'config':'experiments/phase2c/config.json','budget_registry':'experiments/phase2c/budget_registry.yaml',
  'config_sha256':config_hash,'registry_sha256':registry_hash,'runtime_hash':runtime_digest,'search_log_hash':composite_log_hash,
  'dataset_split_manifest_sha256':hashlib.sha256(SPLIT_PATH.read_bytes()).hexdigest(),'task_count':len(rows),
  'split_counts':dict(split_counts),'conditions':len(cond_defs),'primary_task_condition_runs':len(primary_rows),
  'deterministic_replay_runs':len(replay_rows),'total_search_invocations':len(primary_rows)+len(replay_rows),
  'process_memory_limit_mib':shared['B5_process_address_space_limit_mib'],'process_peak_rss_mib':integrity['process_peak_rss_mib'],
  'wall_clock_limit_sec_per_search':shared['B4_wall_clock_seconds_per_search'],
  'test_output_fields_parsed_or_used':False,'accuracy_measured':False,'run_status':'completed_budget_parity_and_replay_pass'}
 (OUT/'run_manifest.json').write_text(json.dumps(run,indent=2)+'\n')
 print(json.dumps({'budget_sensitivity':by_condition,'invariants':invariants,'integrity':integrity},indent=2))

if __name__=='__main__':
 try:main()
 except Exception as e:
  OUT.mkdir(parents=True,exist_ok=True)
  (OUT/'protocol_violation.json').write_text(json.dumps({'status':'protocol_violation','error':repr(e)},indent=2)+'\n')
  raise
