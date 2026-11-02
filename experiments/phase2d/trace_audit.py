"""Phase 2D audit of Phase 13G and saved Phase 2C traces; does not search or score tests."""
from __future__ import annotations
import csv,hashlib,json,math,sys
from collections import Counter,defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'experiments')]
from phase13g.common import PROGRAMS,PROGRAM_FAMILY,infer_context,trace_for,structural_bucket
from phase13g.runner import mine_invariants
from core.trace import ReasoningTrace
from phase2c.search_budget_benchmark import read_train_only
OUT=ROOT/'reports/experiments/ASFT-V1.1-PHASE-2D-TRACE-GENERATION-AUDIT-V1'
C2=ROOT/'reports/experiments/ASFT-V1.1-PHASE-2C-SEARCH-BUDGET-AUDIT-V1'
P13=ROOT/'reports/experiments/PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1'
MANIFEST=ROOT/'datasets/arc/arc-agi-2/split_manifest.json'

def canon(x):return json.dumps(x,sort_keys=True,separators=(',',':'))
def entropy(vals):
 if not vals:return 'NOT_ESTIMABLE'
 c=Counter(vals);n=sum(c.values())
 return round(max(0.0,-sum((x/n)*math.log2(x/n) for x in c.values())),6)
def boolv(x):return x is True or str(x).lower()=='true'

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 manifest=json.loads(MANIFEST.read_text());tasks={}
 for r in manifest['tasks']:
  train=read_train_only(ROOT/'datasets/arc'/r['path'])
  task={'task_id':r['task_id'],'split':r['split'],'train':train}
  tasks[r['task_id']]=task
 search_rows=list(csv.DictReader((C2/'search_execution_log.csv').open(newline='',encoding='utf-8')))
 candidate_rows=list(csv.DictReader((C2/'candidate_trial_log.csv').open(newline='',encoding='utf-8')))
 selected_ctx={}
 for r in candidate_rows:
  if boolv(r['selected']):selected_ctx[(r['task_id'],r['condition'])]=json.loads(r['inferred_context_json']) if r['inferred_context_json'] else {}
 records=[];traces_by_condition=defaultdict(list);fit_traces_by_condition=defaultdict(list)
 for r in search_rows:
  tid=r['task_id'];cid=r['condition'];task=tasks[tid];program=r['candidate_program_selected'];success=boolv(r['exact_demo_fit'])
  context=selected_ctx.get((tid,cid),{}) if success else {}
  result={'program':program,'family':PROGRAM_FAMILY[program] if program else 'unsupported_v1',
          'demo_fit':success,'candidate_trials':int(r['candidate_trials_evaluated']),'context':context}
  trace=trace_for({'task_id':tid,'split':task['split']},result)
  expected=(['validate_grid_schema','enumerate_candidate_programs',f'apply_{program}','verify_demonstrations'] if success else ['validate_grid_schema','enumerate_candidate_programs','candidate_budget_exhausted'])
  structurally_valid=(trace.task_id==tid and trace.metadata.get('split')==task['split'] and trace.operations==expected and trace.outcome is not None and trace.outcome.success==success and len(trace.steps)<=4)
  fit_exact=False
  if success:
   inferred=infer_context(program,task['train'])
   fit_exact=inferred is not None and canon(inferred)==canon(context)
  if not structurally_valid or (success and not fit_exact):raise SystemExit(f'trace audit validation failure {cid}/{tid}')
  sig=(program,canon(context)) if success else ('','')
  bucket=structural_bucket(task)
  rec={'condition':cid,'task_id':tid,'split':task['split'],'trace_id':trace.trace_id,
       'primary_class':'T4_SUCCESSFUL_TRACE' if success else 'T2_VALID_TRACE',
       'T1_invalid':False,'T2_valid':True,'T3_partial':False,'T4_successful':success,
       'program':program,'context_json':canon(context) if success else '',
       'solution_signature':canon(sig) if success else '',
       'candidate_programs_generated':int(r['candidate_programs_generated']),
       'candidate_trials_evaluated':int(r['candidate_trials_evaluated']),
       'operations_json':canon(trace.operations),'trace_step_count':len(trace.steps),
       'trace_structurally_valid':structurally_valid,'train_demo_fit_independently_replayed':fit_exact if success else 'NOT_APPLICABLE_NO_SELECTED_CANDIDATE',
       'structural_bucket_diagnostic':bucket,'accuracy':'NOT_MEASURED_BY_DESIGN'}
  records.append(rec);traces_by_condition[cid].append((rec,trace))
  if success:fit_traces_by_condition[cid].append((rec,trace))

 # Support and cross-split overlap diagnostics, derived only from found demo fits.
 support_stats={};support_by_condition={}
 for cid,items in fit_traces_by_condition.items():
  disc=[r for r,t in items if r['split']=='discovery']
  by_sig=Counter(r['solution_signature'] for r in disc)
  by_op=Counter(r['program'] for r in disc)
  disc_ops={r['program'] for r in disc};transfer_ops={r['program'] for r,t in items if r['split']=='transfer'}
  exact_disc={r['solution_signature'] for r in disc};exact_transfer={r['solution_signature'] for r,t in items if r['split']=='transfer'}
  support_stats[cid]={'discovery_successful_traces':len(disc),'exact_signature_support':dict(by_sig),
    'program_operation_support':dict(by_op),'max_discovery_signature_support':max(by_sig.values(),default=0),
    'high_support_signature_count_ge_5':sum(v>=5 for v in by_sig.values()),
    'programs_observed_in_both_discovery_and_transfer':sorted(disc_ops & transfer_ops),
    'exact_signatures_observed_in_both_discovery_and_transfer':len(exact_disc & exact_transfer)}
  support_by_condition[cid]=(by_sig,by_op,disc_ops & transfer_ops)
 for rec in records:
  by_sig,by_op,shared_ops=support_by_condition[rec['condition']]
  rec['discovery_exact_signature_support']=by_sig.get(rec['solution_signature'],0) if rec['solution_signature'] else 0
  rec['discovery_operation_support']=by_op.get(rec['program'],0) if rec['program'] else 0
  rec['T5_high_support']=bool(rec['program'] and rec['split']=='discovery' and by_op.get(rec['program'],0)>=5)
  rec['T6_transfer_relevant_program_level']=bool(rec['program'] and rec['program'] in shared_ops)

 # Re-run the actual frozen Phase 13G TraceMiner on the reconstructed successful discovery traces.
 miner_rows=[];miner_json={}
 for cid,items in traces_by_condition.items():
  dtr=[t for rec,t in items if rec['split']=='discovery' and rec['T4_successful']]
  mined,by_program,candidates=mine_invariants(dtr)
  stat=mined.statistics.to_dict()
  existing=json.loads((C2/'invariant_mining_summary.json').read_text())['by_condition'][cid]
  if len(by_program)!=existing['mapped_invariant_count'] or len(candidates)!=existing['trace_miner_candidates']:
   raise SystemExit('TraceMiner output differs from Phase 2C record '+cid)
  support_stats[cid].update({'miner_statistics':stat,'trace_miner_candidate_count':len(candidates),'mapped_invariant_count':len(by_program)})
  miner_rows.append({'condition':cid,'successful_discovery_trace_inputs':len(dtr),**stat,
     'trace_miner_candidates':len(candidates),'mapped_invariant_candidates':len(by_program),
     'support_threshold':5,'consistency_threshold':1.0,
     'readiness':'I3_NOT_READY' if not by_program else 'REQUIRES_POLICY_REVIEW'})
  miner_json[cid]=support_stats[cid]
 # Historical Phase 13G saved traces: validate structure retrospectively, not the hard-coded generation flag.
 quality={r['task_id']:r for r in csv.DictReader((P13/'discovery_trace_quality.csv').open(newline='',encoding='utf-8'))}
 hist_records=[];hist_fit=[];hist_success_traces=[]
 for line in (P13/'discovery_traces.jsonl').read_text().splitlines():
  if not line.strip():continue
  raw=json.loads(line);trace=ReasoningTrace.from_dict(raw);tid=trace.task_id;task=tasks[tid];q=quality[tid]
  prog=str((trace.outcome.result or {}).get('program','')) if trace.outcome else ''
  success=bool(trace.outcome and trace.outcome.success)
  ops=trace.operations
  expected=(['validate_grid_schema','enumerate_candidate_programs',f'apply_{prog}','verify_demonstrations'] if prog else ['validate_grid_schema','enumerate_candidate_programs','candidate_budget_exhausted'])
  valid=(trace.task_id==tid and trace.trace_id==f'arc2-{tid}' and ops==expected and trace.outcome is not None and trace.outcome.success==boolv(q['demo_fit']))
  exact=False
  if success:
   ctx=infer_context(prog,task['train']);exact=ctx is not None
   if not exact:raise SystemExit('Historical successful trace fails train-demo replay '+tid)
   hist_fit.append({'task_id':tid,'program':prog,'context':canon(ctx),'signature':canon((prog,canon(ctx))),'split':'discovery'})
   hist_success_traces.append(trace)
  if not valid:raise SystemExit('Historical structural trace audit failed '+tid)
  hist_records.append({'task_id':tid,'historical_trace_schema_valid_flag':q['trace_schema_valid'],
    'independent_serialized_trace_validation':True,'program':prog,'demo_fit':success,
    'exact_train_demo_replay':exact if success else 'NOT_APPLICABLE_NO_SELECTED_CANDIDATE',
    'saved_stability_permutations':q['permutations'],'trace_operations_json':canon(ops)})
 hist_support=Counter(x['program'] for x in hist_fit)
 hist_mining,hist_by_program,hist_candidates=mine_invariants(hist_success_traces)
 hist_miner_stats=hist_mining.statistics.to_dict()
 saved_mining=json.loads((P13/'summary.json').read_text())['mining_statistics']
 if hist_miner_stats!=saved_mining:raise SystemExit('Historical TraceMiner replay differs from saved mining summary')
 hist_summary={'tasks':600,'serialized_traces':len(hist_records),'retrospective_structural_valid':sum(r['independent_serialized_trace_validation'] for r in hist_records),
   'successful_traces':len(hist_fit),'no_fit_valid_traces':len(hist_records)-len(hist_fit),
   'discovery_success_program_support':dict(hist_support),'high_support_programs_ge_5':sum(v>=5 for v in hist_support.values()),
   'trace_miner_statistics':hist_miner_stats,'trace_miner_candidates':len(hist_candidates),
   'mapped_invariant_candidates':len(hist_by_program),
   'phase13g_schema_flag_was_hardcoded':True,'generation_time_validator_established':False,
   'successful_train_demo_replay_count':sum(r['exact_train_demo_replay'] is True for r in hist_records),
   'test_output_fields_parsed_or_used':False,'accuracy_measured':False}
 # Write evidence tables.
 def write(path,rows):
  if not rows:raise ValueError('empty '+path)
  with (OUT/path).open('w',newline='',encoding='utf-8') as f:
   w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
 write('trace_audit_records.csv',records)
 write('historical_trace_validation.csv',hist_records)
 write('invariant_readiness_summary.csv',miner_rows)
 (OUT/'trace_mining_details.json').write_text(json.dumps({'phase2c_by_condition':miner_json,'phase13g_historical':hist_summary},indent=2)+'\n')
 (OUT/'historical_trace_validation_summary.json').write_text(json.dumps(hist_summary,indent=2)+'\n')
 # Taxonomy counts: T1/T2 primary validity; T3 is not represented by this trace builder; T5/T6 are non-exclusive overlays.
 taxonomy=[]
 for cid in list(traces_by_condition)+['PHASE13G_HISTORICAL']:
  rr=[r for r in records if r['condition']==cid] if cid!='PHASE13G_HISTORICAL' else hist_records
  n=len(rr);succ=sum(boolv(r['T4_successful']) if cid!='PHASE13G_HISTORICAL' else boolv(r['demo_fit']) for r in rr)
  valid=sum(boolv(r['T2_valid']) if cid!='PHASE13G_HISTORICAL' else boolv(r['independent_serialized_trace_validation']) for r in rr)
  high=sum(boolv(r['T5_high_support']) for r in rr) if cid!='PHASE13G_HISTORICAL' else 0
  trrel=sum(boolv(r['T6_transfer_relevant_program_level']) for r in rr) if cid!='PHASE13G_HISTORICAL' else 0
  taxonomy.extend([
   {'condition':cid,'taxonomy_id':'T1','trace_class':'Invalid Trace','count':n-valid,'status':'measured_retrospectively' if cid=='PHASE13G_HISTORICAL' else 'independently_validated'},
   {'condition':cid,'taxonomy_id':'T2','trace_class':'Valid Trace','count':valid,'status':'historical_structural_validation_not_generation_time' if cid=='PHASE13G_HISTORICAL' else 'independently_validated'},
   {'condition':cid,'taxonomy_id':'T3','trace_class':'Partial Trace','count':0,'status':'not_emitted_by_builder; candidate failures are not partial trace records'},
   {'condition':cid,'taxonomy_id':'T4','trace_class':'Successful Trace','count':succ,'status':'exact demonstration fit'},
   {'condition':cid,'taxonomy_id':'T5','trace_class':'High-Support Trace','count':high,'status':'nonexclusive; discovery program support >=5'},
   {'condition':cid,'taxonomy_id':'T6','trace_class':'Transfer-Relevant Trace','count':trrel,'status':'nonexclusive program-level discovery/transfer overlap; not transfer success'}])
 write('trace_taxonomy_counts.csv',taxonomy)
 # Diversity and quality summaries by split/mode.
 diversity=[];quality_rows=[];lifecycle=[]
 for cid in traces_by_condition:
  allrr=[r for r in records if r['condition']==cid]
  for split in ('discovery','transfer','holdout','all'):
   rr=[r for r in allrr if split=='all' or r['split']==split];n=len(rr);successful=[r for r in rr if r['T4_successful']]
   sigs=[r['solution_signature'] for r in successful];buckets=[r['structural_bucket_diagnostic'] for r in successful]
   op_lists=[tuple(json.loads(r['operations_json'])) for r in rr]
   ops=[op for seq in op_lists for op in seq]
   selected_ops=[r['program'] for r in successful]
   diversity.append({'condition':cid,'split':split,'tasks':n,'trace_records':n,
      'unique_trace_ids':len({r['trace_id'] for r in rr}),
      'successful_traces':len(successful),'unique_solution_signatures':len(set(sigs)),
      'solution_signature_entropy_bits':entropy(sigs),'distinct_structural_buckets_among_successes':len(set(buckets)) if buckets else 'NOT_ESTIMABLE',
      'structural_bucket_entropy_bits':entropy(buckets),'unique_operation_names':len(set(ops)),
      'operation_name_entropy_bits':entropy(ops),'unique_successful_program_labels':len(set(selected_ops)),
      'successful_program_entropy_bits':entropy(selected_ops),'unique_operation_sequence_templates':len(set(op_lists)),
      'trace_emission_density_per_task':round(len(rr)/n,6) if n else 'NOT_ESTIMABLE',
      'boundary':'structural buckets are coarse first-demo diagnostics, not semantic ARC families'})
   if split=='all':
    q2=(sum(boolv(r['train_demo_fit_independently_replayed']) for r in successful)/len(successful)) if successful else 'NOT_ESTIMABLE'
    q4=max((Counter(r['discovery_operation_support'] for r in successful if r['split']=='discovery')).values(),default=0)
    qsig=max((Counter(r['discovery_exact_signature_support'] for r in successful if r['split']=='discovery')).values(),default=0)
    shared=support_stats[cid]['programs_observed_in_both_discovery_and_transfer']
    quality_rows.append({'condition':cid,'tasks':n,'valid_traces':sum(r['T2_valid'] for r in rr),
      'successful_traces':len(successful),'Q1_demo_fit_rate_pct':round(100*len(successful)/n,4),
      'Q2_consistency_among_successful_exact_replays':q2,'Q3_generalization_beyond_demos':'NOT_MEASURED_TEST_OUTPUT_BLIND',
      'Q4_max_discovery_program_support':max(Counter(r['program'] for r in successful if r['split']=='discovery').values(),default=0),
      'Q4_max_exact_signature_support':max((Counter(r['solution_signature'] for r in successful if r['split']=='discovery')).values(),default=0),
      'Q5_program_level_discovery_transfer_overlap':len(shared),'Q5_exact_signature_overlap':support_stats[cid]['exact_signatures_observed_in_both_discovery_and_transfer'],
      'invariant_score_or_skill_score_used':False})
  # Task-level lifecycle per condition, with rates conditional on prior-stage denominator.
  n=len(allrr);valid=sum(r['T2_valid'] for r in allrr);succ=sum(r['T4_successful'] for r in allrr)
  dsuccess=[r for r in allrr if r['split']=='discovery' and r['T4_successful']]
  invc=support_stats[cid]['mapped_invariant_count']
  lifecycle.append({'condition':cid,'task_condition_denominator':n,'candidate_pool_nonempty_tasks':n,
   'search_attempted_tasks':n,'trace_generated':n,'valid_traces':valid,'successful_traces':succ,
   'invariant_candidate_count':invc,'skill_candidate_count':0,
   'candidate_to_search_survival_pct':100.0,'search_to_trace_survival_pct':100.0,
   'trace_generated_to_valid_survival_pct':round(100*valid/n,4),
   'valid_to_successful_survival_pct':round(100*succ/valid,4) if valid else 'NOT_ESTIMABLE',
   'successful_discovery_to_invariant_survival_pct':round(100*invc/len(dsuccess),4) if dsuccess else 'NOT_ESTIMABLE',
   'invariant_to_skill_survival_pct':'NOT_ESTIMABLE_ZERO_INVARIANTS' if invc==0 else 'NOT_RUN',
   'trace_successes_on_all_splits_not_equal_discovery_miner_input':succ,'miner_input_successful_discovery_traces':len(dsuccess),
   'skill_stage_status':'BLOCKED_UPSTREAM_NO_INVARIANT_CANDIDATE'})
 write('trace_diversity_summary.csv',diversity);write('trace_quality_summary.csv',quality_rows);write('trace_lifecycle_summary.csv',lifecycle)
 summary={'phase':'ASFT-V1.1-PHASE-2D','phase2c_conditions_audited':list(traces_by_condition),
  'trace_records_reconstructed':len(records),'historical_serialized_traces_validated':len(hist_records),
  'trace_miner_replays':len(miner_rows),'test_output_fields_parsed_or_used':False,'accuracy_measured':False,
  'new_arc_search_or_scoring_run':False,'historical_outcomes_modified':False,
  'status':'TRACE_AUDIT_COMPLETE'}
 (OUT/'trace_audit_manifest.json').write_text(json.dumps(summary,indent=2)+'\n')
 print(json.dumps({'summary':summary,'invariant_readiness':miner_rows,'historical':hist_summary,'quality':quality_rows},indent=2))
if __name__=='__main__':main()
