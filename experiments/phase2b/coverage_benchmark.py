"""Phase 2B coverage-only benchmark. Never parses or uses ARC test-output fields."""
from __future__ import annotations
import csv, hashlib, json, math, sys, time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "experiments"))
from phase13g.common import PROGRAMS, PROGRAM_FAMILY, infer_context, apply_program, trace_for
from phase13g.runner import mine_invariants

MANIFEST = ROOT / "datasets/arc/arc-agi-2/split_manifest.json"
OUT = ROOT / "reports/experiments/ASFT-V1.1-PHASE-2B-ARC-COVERAGE-BENCHMARK-V1"
BUDGET = 3
FULLSCAN_BUDGET = len(PROGRAMS)


def _read_char(f):
    return f.read(1)


def _skip_ws(f):
    c = _read_char(f)
    while c and c.isspace(): c = _read_char(f)
    return c


def _read_quoted(f, first='"'):
    if first != '"': raise ValueError('Expected JSON string key')
    chars = [first]; escaped = False
    while True:
        c = _read_char(f)
        if not c: raise ValueError('Truncated JSON string')
        chars.append(c)
        if escaped: escaped = False
        elif c == '\\': escaped = True
        elif c == '"': break
    return json.loads(''.join(chars))


def read_train_only(path: Path):
    """Read and parse only the first top-level `train` array; stop before `test`."""
    with path.open(encoding='utf-8') as f:
        if _skip_ws(f) != '{': raise ValueError(f'Unexpected root schema: {path}')
        if _skip_ws(f) != '"': raise ValueError(f'Expected first key train: {path}')
        key = _read_quoted(f)
        if key != 'train': raise ValueError(f'Fail-closed: first key is not train: {path}')
        if _skip_ws(f) != ':': raise ValueError(f'Expected colon after train: {path}')
        if _skip_ws(f) != '[': raise ValueError(f'Expected train array: {path}')
        chars = ['[']; depth = 1; in_string = False; escaped = False
        while depth:
            c = _read_char(f)
            if not c: raise ValueError(f'Truncated train array: {path}')
            chars.append(c)
            if in_string:
                if escaped: escaped = False
                elif c == '\\': escaped = True
                elif c == '"': in_string = False
            else:
                if c == '"': in_string = True
                elif c == '[': depth += 1
                elif c == ']': depth -= 1
        train = json.loads(''.join(chars))
    if not isinstance(train, list) or not train: raise ValueError(f'Empty/invalid train array: {path}')
    return train


def grid_ok(grid):
    return (isinstance(grid, list) and len(grid) > 0 and
            all(isinstance(row, list) and len(row) > 0 for row in grid) and
            len({len(row) for row in grid}) == 1 and
            all(type(v) is int and 0 <= v <= 9 for row in grid for v in row))


def task_schema_ok(demos):
    return bool(demos) and all(isinstance(p, dict) and grid_ok(p.get('input')) and
        grid_ok(p.get('output')) for p in demos)


def search(demos, budget):
    tried = 0
    for program in PROGRAMS[:budget]:
        tried += 1
        context = infer_context(program, demos)
        if context is not None:
            return {'program': program, 'family': PROGRAM_FAMILY[program], 'demo_fit': True,
                    'candidate_trials': tried, 'context': context}
    return {'program': '', 'family': 'unsupported_v1', 'demo_fit': False,
            'candidate_trials': tried, 'context': {}}


def independently_replay(demos, result):
    if not result['demo_fit']: return False
    ctx = result['context']; prog = result['program']
    for pair in demos:
        source = tuple(tuple(int(c) for c in row) for row in pair['input'])
        expected = tuple(tuple(int(c) for c in row) for row in pair['output'])
        if apply_program(prog, source, ctx) != expected: return False
    return True


def validate_trace(trace, task_id, split, result, schema_valid):
    ops = trace.operations
    if trace.task_id != task_id or trace.metadata.get('split') != split: return False
    if trace.metadata.get('test_outputs_used_for_trace') is not False: return False
    if trace.outcome is None or trace.outcome.success != bool(result['demo_fit']): return False
    if result['demo_fit']:
        expected = ['validate_grid_schema', 'enumerate_candidate_programs',
                    f"apply_{result['program']}", 'verify_demonstrations']
    else:
        expected = ['validate_grid_schema', 'enumerate_candidate_programs',
                    'candidate_budget_exhausted']
    return bool(schema_valid and ops == expected and len(trace.steps) == len(expected))


def signature(result):
    if not result['demo_fit']: return ''
    return result['program'] + '|' + json.dumps(result['context'], sort_keys=True, separators=(',', ':'))


def entropy(labels):
    n = len(labels)
    if not n: return 'NOT_ESTIMABLE'
    counts = Counter(labels)
    return round(max(0.0, -sum((v/n) * math.log2(v/n) for v in counts.values())), 6)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = json.loads(MANIFEST.read_text())
    rows = manifest['tasks']
    if len(rows) != 1000 or Counter(r['split'] for r in rows) != {'discovery':600,'transfer':200,'holdout':200}:
        raise SystemExit('Split manifest counts mismatch; fail closed')
    if len({r['task_id'] for r in rows}) != len(rows): raise SystemExit('Duplicate task IDs')
    records = []
    fit_traces = {'budgeted': [], 'fullscan': []}
    start = time.monotonic()
    for i, row in enumerate(rows, 1):
        path = ROOT / 'datasets/arc' / row['path']
        demos = read_train_only(path)
        if len(demos) != row['train_pairs']: raise SystemExit(f'Train-pair count mismatch: {row["task_id"]}')
        schema_valid = task_schema_ok(demos)
        if not schema_valid: raise SystemExit(f'Invalid demonstration schema: {row["task_id"]}')
        task = {'task_id': row['task_id'], 'split': row['split'], 'train': demos}
        results = {}
        traces = {}
        trace_valid = {}
        for mode, budget in [('budgeted', BUDGET), ('fullscan', FULLSCAN_BUDGET)]:
            result = search(demos, budget)
            results[mode] = result
            trace = trace_for(task, result)
            traces[mode] = trace
            trace_valid[mode] = validate_trace(trace, row['task_id'], row['split'], result, schema_valid)
            if not trace_valid[mode]: raise SystemExit(f'Independent trace validation failed: {row["task_id"]}/{mode}')
            if result['demo_fit']:
                if not independently_replay(demos, result): raise SystemExit(f'Independent exact-fit replay failed: {row["task_id"]}/{mode}')
                fit_traces[mode].append(trace)
        records.append({'task_id':row['task_id'],'split':row['split'],'train_pairs':len(demos),
            'schema_valid':schema_valid,
            'budgeted_C1_representable_within_budget':results['budgeted']['demo_fit'],
            'budgeted_program':results['budgeted']['program'],'budgeted_candidate_trials':results['budgeted']['candidate_trials'],
            'budgeted_C2_trace_generated':True,'budgeted_trace_valid':trace_valid['budgeted'],
            'budgeted_C3_successful_trace':bool(results['budgeted']['demo_fit'] and traces['budgeted'].outcome.success),
            'budgeted_signature':signature(results['budgeted']),
            'fullscan_C1_representable_within_budget':results['fullscan']['demo_fit'],
            'fullscan_program':results['fullscan']['program'],'fullscan_candidate_trials':results['fullscan']['candidate_trials'],
            'fullscan_C2_trace_generated':True,'fullscan_trace_valid':trace_valid['fullscan'],
            'fullscan_C3_successful_trace':bool(results['fullscan']['demo_fit'] and traces['fullscan'].outcome.success),
            'fullscan_signature':signature(results['fullscan']),
            'accuracy_measured':False,'test_outputs_parsed_or_used':False})
        if i % 100 == 0: print(f'processed {i}/1000 tasks', flush=True)

    # Apply the frozen discovery support threshold to actual successful budgeted and full-scan traces.
    inv_result = {}
    invariant_candidates = {}
    for mode in ('budgeted','fullscan'):
        # Filter by discovery task IDs without consulting any task test fields.
        discovery_ids = {x['task_id'] for x in records if x['split']=='discovery'}
        dtraces = [t for t in fit_traces[mode] if t.task_id in discovery_ids]
        mined, by_program, candidate_rows = mine_invariants(dtraces)
        support_counts = dict(Counter(t.outcome.result['program'] for t in dtraces if t.outcome and t.outcome.result))
        inv_result[mode] = {'candidate_count':len(by_program),'trace_miner_candidate_count':len(candidate_rows),
                            'accepted_programs':sorted(by_program),'source_successful_traces':len(dtraces),
                            'discovery_success_support_by_program':support_counts}
        invariant_candidates[mode] = set(by_program)
    for r in records:
        for mode in ('budgeted','fullscan'):
            c4 = bool(r[f'{mode}_program'] and r[f'{mode}_program'] in invariant_candidates[mode])
            r[f'{mode}_C4_invariant_candidate_available'] = c4
            # Later chain stages are not executed: they require a nonempty C4 pool and
            # Phase 13G transfer qualification includes test-label use, prohibited here.
            r[f'{mode}_C5_skill_candidate_available'] = False
            r[f'{mode}_C6_transfer_eligible'] = False
            r[f'{mode}_C7_capability_eligible'] = False
            r[f'{mode}_C5_C7_status'] = 'blocked_upstream_no_C4_candidate' if not invariant_candidates[mode] else 'not_run_requires_separate_authorized_transfer_protocol'

    cols = list(records[0])
    with (OUT/'task_stage_outcomes.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=cols);w.writeheader();w.writerows(records)
    with (OUT/'invariant_mining_summary.json').open('w') as f:
        json.dump({'support_threshold':5,'min_consistency':1.0,'results':inv_result,
                   'interpretation':'Actual Phase 13G TraceMiner invoked on successful discovery traces only; later stages not run.'},f,indent=2);f.write('\n')
    by_split=[]
    for split in ('discovery','transfer','holdout','all'):
        rr=[r for r in records if split=='all' or r['split']==split]
        n=len(rr); out={'split':split,'tasks':n}
        for mode in ('budgeted','fullscan'):
            def count(col): return sum(bool(r[col]) for r in rr)
            c1=count(f'{mode}_C1_representable_within_budget')
            c2=count(f'{mode}_C2_trace_generated');valid=count(f'{mode}_trace_valid')
            c3=count(f'{mode}_C3_successful_trace');c4=count(f'{mode}_C4_invariant_candidate_available')
            out.update({f'{mode}_C1_representable_count':c1,f'{mode}_C1_representable_pct':round(100*c1/n,4),
                f'{mode}_C2_trace_generated_count':c2,f'{mode}_C2_trace_generated_pct':round(100*c2/n,4),
                f'{mode}_trace_valid_count':valid,f'{mode}_trace_valid_pct':round(100*valid/n,4),
                f'{mode}_C3_successful_trace_count':c3,f'{mode}_C3_successful_trace_pct':round(100*c3/n,4),
                f'{mode}_C4_invariant_task_count':c4,f'{mode}_C4_invariant_task_pct':round(100*c4/n,4),
                f'{mode}_C5_skill_candidate_count':0,f'{mode}_C6_transfer_eligible_count':0,f'{mode}_C7_capability_eligible_count':0,
                f'{mode}_trace_steps_per_task':0})
            # trace records are generated by construction; successful traces carry 4 steps, no-fit traces 3.
            out[f'{mode}_trace_steps_per_task']=round((4*c3+3*(n-c3))/n,4)
            out[f'{mode}_successful_signature_diversity_n']=len({r[f'{mode}_signature'] for r in rr if r[f'{mode}_signature']})
            out[f'{mode}_successful_program_entropy_bits']=entropy([r[f'{mode}_program'] for r in rr if r[f'{mode}_program']])
            out[f'{mode}_mean_candidate_trials']=round(sum(r[f'{mode}_candidate_trials'] for r in rr)/n,4)
        out['accuracy']='NOT_MEASURED_BY_DESIGN'
        by_split.append(out)
    with (OUT/'coverage_summary_by_split.csv').open('w',newline='') as f:
        w=csv.DictWriter(f,fieldnames=list(by_split[0]));w.writeheader();w.writerows(by_split)
    run={'phase':'ASFT-V1.1-PHASE-2B','package':'ASFT-V1.1-PHASE-2B-ARC-COVERAGE-BENCHMARK-V1',
        'protocol':'experiments/phase2b/preregistration.md','config':'experiments/phase2b/config.json',
        'protocol_sha256':hashlib.sha256((ROOT/'experiments/phase2b/preregistration.md').read_bytes()).hexdigest(),
        'config_sha256':hashlib.sha256((ROOT/'experiments/phase2b/config.json').read_bytes()).hexdigest(),
        'runner_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        'dataset_manifest_sha256':hashlib.sha256(MANIFEST.read_bytes()).hexdigest(),
        'dataset_source_manifest_sha256':hashlib.sha256((ROOT/'datasets/arc/arc-agi-2/source_manifest.json').read_bytes()).hexdigest(),
        'task_count':len(records),'split_counts':dict(Counter(r['split'] for r in records)),
        'budgeted_candidate_limit':BUDGET,'fullscan_candidate_limit':FULLSCAN_BUDGET,
        'program_order':list(PROGRAMS),'test_output_fields_parsed_or_used':False,'accuracy_measured':False,
        'runtime_seconds':round(time.monotonic()-start,3),'historical_phase13g_outcomes_modified':False,
        'invariant_mining':inv_result,'run_status':'completed_coverage_only'}
    (OUT/'run_manifest.json').write_text(json.dumps(run,indent=2)+'\n')
    print(json.dumps({'summary':by_split,'invariants':inv_result,'runtime_s':run['runtime_seconds']},indent=2))

if __name__ == '__main__': main()
