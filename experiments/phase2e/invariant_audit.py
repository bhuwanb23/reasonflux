"""Phase 2E retrospective invariant-discovery audit; no ARC search/test scoring."""
from __future__ import annotations
import csv, json, sys
from collections import Counter, defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
sys.path[:0]=[str(ROOT/'src'),str(ROOT/'experiments')]
from core.trace import ReasoningTrace
from invariants.candidate_generation import generate_candidates
from invariants.detector import InvariantDetector, TraceMiner
from invariants.pattern_mining import (MiningConfig, aggregate_patterns, extract_patterns)
from invariants.specification import InvariantPolicy
from traces.normalizer import normalize_traces
from traces.segmentation import segment_traces
from phase13g.common import PROGRAM_FAMILY, trace_for

OUT=ROOT/'reports/experiments/ASFT-V1.1-PHASE-2E-INVARIANT-DISCOVERY-AUDIT-V1'
P13=ROOT/'reports/experiments/PHASE-13G-ARC-AGI-2-TRACE-TRANSFER-V1'
P2D=ROOT/'reports/experiments/ASFT-V1.1-PHASE-2D-TRACE-GENERATION-AUDIT-V1'
THRESHOLDS=[('RELAXED_S2',2),('CURRENT_S1',5),('STRICT_S3',6)]

def boolv(x): return x is True or str(x).lower()=='true'
def j(x): return json.dumps(x,sort_keys=True,separators=(',',':'))
def make_config(k):
 return MiningConfig(min_frequency=k,min_cross_trace=k,max_fragment_length=4,min_core_length=1,successful_trace_bias=True)
def make_policy(k):
 return InvariantPolicy(min_frequency=k,min_consistency=1.0,min_task_families=2,min_generality=0.0,
    require_transfer_evidence=False,min_transfer_events=0)
def write_csv(name,rows):
 if not rows:
  rows=[{'status':'NO_ROWS'}]
 keys=[]
 for row in rows:
  for key in row:
   if key not in keys: keys.append(key)
 with (OUT/name).open('w',newline='',encoding='utf-8') as f:
  w=csv.DictWriter(f,fieldnames=keys);w.writeheader();w.writerows(rows)
def traces_by_source():
 out={}
 hist=[]
 for line in (P13/'discovery_traces.jsonl').read_text().splitlines():
  raw=json.loads(line)
  if raw.get('outcome') and raw['outcome'].get('success'):
   hist.append(ReasoningTrace.from_dict(raw))
 out['PHASE13G_HISTORICAL']=hist
 records=list(csv.DictReader((P2D/'trace_audit_records.csv').open(newline='',encoding='utf-8')))
 for condition in ('S1','S2','S3','S4'):
  chosen=[]
  for r in records:
   if r['condition']!=condition or r['split']!='discovery' or not boolv(r['T4_successful']): continue
   program=r['program']
   tr=trace_for({'task_id':r['task_id'],'split':'discovery'},
       {'program':program,'family':PROGRAM_FAMILY.get(program,'unsupported_v1'),'demo_fit':True,
        'candidate_trials':int(r['candidate_trials_evaluated'])})
   if tr.operations!=json.loads(r['operations_json']) or tr.trace_id!=r['trace_id']:
    raise SystemExit(f'Phase 2D trace reconstruction mismatch {condition}/{r["task_id"]}')
   chosen.append(tr)
  out[condition]=chosen
 return out

def recurrence(traces,source):
 norm=normalize_traces(traces)
 frags=segment_traces(norm,max_length=4)
 by=defaultdict(list)
 for f in frags: by[f.signature].append(f)
 rows=[]
 for sig,items in sorted(by.items(),key=lambda z:(-len({f.trace_id for f in z[1]}),z[0])):
  tids=sorted({f.trace_id for f in items if f.trace_id})
  taskids=sorted({f.task_id for f in items if f.task_id})
  families=sorted({f.task_family for f in items if f.task_family})
  rows.append({'source':source,'pattern_signature_json':j(sig),'pattern_length':len(sig),
   'distinct_trace_support':len(tids),'distinct_task_support':len(taskids),
   'occurrence_count_after_per_trace_dedupe':len(items),
   'successful_trace_coverage_pct':round(100*len(tids)/len(traces),6) if traces else 'NOT_ESTIMABLE',
   'all_discovery_task_coverage_pct':round(100*len(taskids)/600,6),
   'observed_trace_family_labels_json':j(families),
   'cross_task_recurrence_ge_2':len(tids)>=2,
   'cross_task_family_labels_independent':False,
   'semantic_arc_invariant_established':False})
 return norm,frags,rows

def audit_source(source,traces):
 norm,frags,recrows=recurrence(traces,source)
 support=Counter(len({f.trace_id for f in [z for z in frags if z.signature==sig]}) for sig in {z.signature for z in frags})
 # Robust exact signature support distribution.
 signature_support=Counter()
 trace_ids_by_sig=defaultdict(set); task_ids_by_sig=defaultdict(set)
 for f in frags:
  trace_ids_by_sig[f.signature].add(f.trace_id);task_ids_by_sig[f.signature].add(f.task_id)
 supp_hist=Counter(len(v) for v in trace_ids_by_sig.values())
 summary={'source':source,'successful_discovery_traces':len(traces),'discovery_tasks_processed':600,
  'distinct_operation_ngram_signatures':len(trace_ids_by_sig),'fragment_occurrences_after_per_trace_dedupe':len(frags),
  'signatures_support_ge_2':sum(n>=2 for n in supp_hist.elements()),
  'signatures_support_ge_3':sum(n>=3 for n in supp_hist.elements()),
  'signatures_support_ge_5':sum(n>=5 for n in supp_hist.elements()),
  'max_distinct_trace_support':max(supp_hist,default=0),
  'signature_support_histogram_json':j(dict(sorted(supp_hist.items()))),
  'trace_family_labels_used_as_independent_evidence':False,
  'recurrence_semantics':'exact operation n-grams only; not semantic ARC-family labels'}
 rows=[];detail=[]
 for name,k in THRESHOLDS:
  cfg=make_config(k);policy=make_policy(k)
  mined=TraceMiner(cfg,policy).mine(traces)
  normal_success=[t for t in normalize_traces(traces) if t.success]
  fragments=segment_traces(normal_success,max_length=cfg.max_fragment_length)
  patterns=extract_patterns(fragments,total_traces=len(normal_success),min_frequency=k,min_cross_trace=k)
  structures=aggregate_patterns(patterns,min_core_length=cfg.min_core_length)
  raw_proposals=generate_candidates(structures,total_families=max(len({t.task_family for t in normal_success if t.task_family}),1),policy=policy,apply_rejections=False)
  ordinary=generate_candidates(structures,total_families=max(len({t.task_family for t in normal_success if t.task_family}),1),policy=policy,apply_rejections=True)
  if len(patterns)!=mined.statistics.raw_patterns or len(structures)!=mined.statistics.structures:
   raise SystemExit(f'Miner stage parity mismatch {source} {name}')
  reason_counts=Counter(reason for _,reasons in ordinary.rejected for reason in reasons)
  proposals=len(raw_proposals.candidates)
  survivors=len(ordinary.candidates);rejected=len(ordinary.rejected)
  rows.append({'source':source,'threshold_id':name,'support_floor':k,'successful_discovery_trace_inputs':len(traces),
    'max_prethreshold_exact_signature_support':max(supp_hist,default=0),
    'fragments':len(fragments),'prethreshold_unique_signatures':len(trace_ids_by_sig),
    'prethreshold_signatures_support_ge_floor':sum(v>=k for v in supp_hist.values()),
    'patterns_after_frequency_and_cross_trace_gates':len(patterns),
    'aggregated_structures':len(structures),'candidate_proposals_before_generation_rejections':proposals,
    'accepted_generation_candidates':survivors,'generation_rejected_candidates':rejected,
    'generation_rejection_reason_counts_json':j(dict(reason_counts)),
    'candidate_proposals_per_successful_trace':round(proposals/len(traces),6) if traces else 'NOT_ESTIMABLE',
    'accepted_candidate_yield_per_successful_trace':round(survivors/len(traces),6) if traces else 'NOT_ESTIMABLE',
    'production_validator_input_count':survivors,
    'validator_status':'BLOCKED_UPSTREAM_NO_GENERATION_ACCEPTED_CANDIDATE' if survivors==0 else 'NOT_RUN_IN_PRODUCTION_SWEEP',
    'mining_stats_json':j(mined.statistics.to_dict())})
  for i,p in enumerate(patterns,1):
   detail.append({'source':source,'threshold_id':name,'stage':'MINED_PATTERN','item_id':p.pattern_id,
    'signature_json':j(p.signature),'distinct_trace_support':p.frequency,'occurrences':p.occurrences,
    'families_json':j(p.task_families),'candidate_status':'NOT_CANDIDATE'})
  for st in structures:
   detail.append({'source':source,'threshold_id':name,'stage':'AGGREGATED_STRUCTURE','item_id':st.structure_id,
    'signature_json':j(st.representative.signature),'distinct_trace_support':st.frequency,'occurrences':st.occurrences,
    'families_json':j(st.task_families),'candidate_status':'PROPOSAL_BEFORE_FILTERS'})
  # Record proposals and reasons, preserving candidates rejected by the ordinary generation policy.
  for inv in raw_proposals.candidates:
   matching=[(x,rs) for x,rs in ordinary.rejected if x.invariant_id==inv.invariant_id]
   reason=matching[0][1] if matching else []
   detail.append({'source':source,'threshold_id':name,'stage':'CANDIDATE_PROPOSAL','item_id':inv.invariant_id,
    'signature_json':j(inv.pattern_signature),'distinct_trace_support':inv.frequency,'occurrences':inv.evidence.observations,
    'families_json':j(inv.task_families),'candidate_status':'REJECTED' if reason else 'ACCEPTED',
    'generation_rejection_reasons_json':j(reason)})
 # Separate diagnostic: at S2, bypass only the candidate-generator rejection criteria, then run validator in memory.
 diag_k=2;diag_policy=make_policy(diag_k);diag_cfg=make_config(diag_k)
 diag_norm=[t for t in normalize_traces(traces) if t.success]
 diag_frags=segment_traces(diag_norm,max_length=diag_cfg.max_fragment_length)
 diag_patterns=extract_patterns(diag_frags,total_traces=len(diag_norm),min_frequency=2,min_cross_trace=2)
 diag_structures=aggregate_patterns(diag_patterns,min_core_length=diag_cfg.min_core_length)
 diag_proposals=generate_candidates(diag_structures,total_families=max(len({t.task_family for t in diag_norm if t.task_family}),1),policy=diag_policy,apply_rejections=False)
 validation=InvariantDetector(config=diag_cfg,policy=diag_policy).validate(diag_proposals.candidates)
 valmap={x.invariant.invariant_id:x for x in validation.ranked}
 val_reasons={inv.invariant_id:reasons for inv,reasons in validation.rejected}
 validated_ids={x.invariant_id for x in validation.validated};tv_ids={x.invariant_id for x in validation.transfer_verified};prom_ids={x.invariant_id for x in validation.promotable}
 for inv in diag_proposals.candidates:
  ranked=valmap[inv.invariant_id];scores=ranked.scores
  detail.append({'source':source,'threshold_id':'RELAXED_S2_DIAGNOSTIC_BYPASS','stage':'VALIDATOR_DIAGNOSTIC',
   'item_id':inv.invariant_id,'signature_json':j(inv.pattern_signature),'distinct_trace_support':inv.frequency,
   'occurrences':inv.evidence.observations,'families_json':j(inv.task_families),
   'candidate_status':'BYPASSED_GENERATION_FILTERS_NOT_PRODUCTION_CANDIDATE',
   'validator_state':'VALIDATED_STRUCTURAL_FCG' if inv.invariant_id in validated_ids else 'NOT_VALIDATED',
   'V1_consistency':scores.consistency,'V2_generality':'NOT_INDEPENDENTLY_VALIDATED_FAMILY_LABELS_OUTCOME_DERIVED',
   'V2_code_generalization_score':scores.generality,'V3_transfer_verified':inv.invariant_id in tv_ids,
   'V3_promotable':inv.invariant_id in prom_ids,'V4_false_discovery_rate':'NOT_ESTIMABLE_NO_INDEPENDENT_TRUTH_LABELS',
   'validator_transfer_score':scores.transfer,'validator_reasoning_value_score':scores.reasoning_value,
   'validator_score':scores.score,'validator_reasons_json':j(scores.reasons),
   'validator_stage_rejection_reasons_json':j(val_reasons.get(inv.invariant_id,[])),
   'same_trace_data_used_for_proposal_and_validation':True})
 return summary,rows,recrows,detail,validation

def main():
 OUT.mkdir(parents=True,exist_ok=True)
 sources=traces_by_source()
 all_summary=[];sweep=[];recrows=[];details=[];validation_summary=[]
 for source,traces in sources.items():
  sm,sw,rr,dd,vr=audit_source(source,traces)
  all_summary.append(sm);sweep.extend(sw);recrows.extend(rr);details.extend(dd)
  validation_summary.append({'source':source,'diagnostic_candidates_bypassing_generation_filters':len(vr.ranked),
   'validator_ranked':vr.statistics.ranked,'structurally_validated_FCG':vr.statistics.validated,
   'transfer_verified':vr.statistics.transfer_verified,'promotable':vr.statistics.promotable,
   'validator_rejection_records':vr.statistics.rejected,
   'FDR':'NOT_ESTIMABLE_NO_INDEPENDENT_TRUTH_LABELS',
   'status':'DIAGNOSTIC_ONLY_NOT_PRODUCTION_CANDIDATE_FLOW'})
 write_csv('recurrence_by_signature.csv',recrows)
 write_csv('recurrence_summary.csv',all_summary)
 write_csv('candidate_generation_audit.csv',sweep)
 write_csv('candidate_and_validation_details.csv',details)
 write_csv('validation_diagnostic_summary.csv',validation_summary)
 # Historical saved final invariant and mining checks.
 historical_saved=json.loads((P13/'summary.json').read_text())
 if historical_saved.get('mining_statistics',{}).get('candidates')!=0: raise SystemExit('Historical candidate count not zero')
 final={'phase':'ASFT-V1.1-PHASE-2E','package':'ASFT-V1.1-PHASE-2E-INVARIANT-DISCOVERY-AUDIT-V1',
   'sources':{k:{'successful_discovery_traces':len(v)} for k,v in sources.items()},
   'phase13g_saved_summary_mining_statistics':historical_saved['mining_statistics'],
   'support_thresholds':{'RELAXED_S2':2,'CURRENT_S1':5,'STRICT_S3':6},
   'test_outputs_parsed_or_used':False,'new_arc_search_or_scoring_run':False,
   'historical_outcomes_modified':False,'accuracy_measured':False,
   'transfer_holdout_traces_used_for_discovery_mining':False,
   'false_discovery_rate_measured':False,
   'status':'INVARIANT_AUDIT_COMPLETE'}
 (OUT/'phase2E_audit_manifest.json').write_text(json.dumps(final,indent=2)+'\n')
 print(json.dumps({'manifest':final,'recurrence_summary':all_summary,'threshold_sweep':sweep,'validation_summary':validation_summary},indent=2))
if __name__=='__main__':main()
