"""Build machine-readable Phase 2F representation registry/framework artifacts."""
from __future__ import annotations
import csv,hashlib,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
PKG=ROOT/'reports/experiments/ASFT-V1.1-PHASE-2F-REPRESENTATION-ALTERNATIVES-V1'

def hash_file(rel):
 h=hashlib.sha256((ROOT/rel).read_bytes()).hexdigest();return h
LEGACY=['identity','reflect_horizontal','reflect_vertical','rotate_90','rotate_180','rotate_270','transpose','anti_transpose','translate_constant','recolor_bijection']
BUDGET={'candidate_trials_per_task':10,'search_depth':1,'primary_trace_records_per_task_condition':1,
 'max_trace_steps':4,'runtime_seconds_per_search':30,'memory_mib':2048,
 'primary_task_ids_per_condition':1000,'deterministic_replay_task_ids_per_condition':1000,
 'total_search_invocations_per_condition':2000,'composition_search_note':'One complete program is one flat candidate; a bounded composed AST is one candidate, not iterative deepening.'}
COMMON=('Inputs are rectangular integer-color grids. Coverage runner consumes training demonstrations only; exact equality on every demonstration is the fit rule; one deterministic enumerator and first-fit selection; no test-output access; candidate trials, candidate IDs, parse state, and stopping reason logged. Every condition emits at most one four-step high-level ReasoningTrace/task: validate input; construct representation; enumerate/apply candidates; verify demonstrations. Independent trace validator is mandatory.')
ROWS=[]
def add(rid,name,role,tax,status,legacy,primitives,objects,relations,composition,search,limits,priority='SECONDARY_SPECIFIED_NOT_IMPLEMENTED'):
 ROWS.append({'representation_id':rid,'name':name,'role':role,'taxonomy_id':tax,'specification_status':status,
  'legacy_aliases':legacy,'primitive_inventory_json':json.dumps(primitives,separators=(',',':')),
  'object_model':objects,'relation_model':relations,'composition_model':composition,
  'parameterization_semantics':'Defined per registered primitive; inferred from training demonstrations only; unsupported/ambiguous parameter fits are explicit no-fit states.',
  'search_interface':search,'shared_evaluation_contract':COMMON,
  'matched_budget_json':json.dumps(BUDGET,separators=(',',':')),
  'downstream_contract':'Same frozen Phase 2E TraceMiner/support/consistency policy; same Invariant, SkillConfig/qualify_candidate, transfer eligibility, and CapabilityConfig/state machine. Representation adapter serializes identical schema; unsupported adapters are UNAVAILABLE_INTERFACE, never zero. Independent task-family labels required; program-derived labels prohibited for comparison.',
  'known_limit_and_interpretation':limits,'implementation_state':'NOT_IMPLEMENTED_OR_RUN' if rid not in ('R0','R1','HCC') else ('HISTORICAL_ONLY' if rid=='R0' else ('EXISTING_RUNNER_REFERENCE' if rid=='R1' else 'SPECIFIED_POSITIVE_CONTROL_NOT_BUILT')),
  'source_or_code_hash':(json.dumps({'experiments/phase13g/common.py':hash_file('experiments/phase13g/common.py'),'experiments/phase13g/runner.py':hash_file('experiments/phase13g/runner.py'),'experiments/phase13g/config.json':hash_file('experiments/phase13g/config.json')},sort_keys=True) if rid=='R0' else (json.dumps({'experiments/phase13g/common.py':hash_file('experiments/phase13g/common.py'),'experiments/phase2c/search_budget_benchmark.py':hash_file('experiments/phase2c/search_budget_benchmark.py'),'experiments/phase2c/config.json':hash_file('experiments/phase2c/config.json'),'experiments/phase2c/budget_registry.yaml':hash_file('experiments/phase2c/budget_registry.yaml')},sort_keys=True) if rid=='R1' else 'SPECIFICATION_ONLY_NO_IMPLEMENTATION_HASH')),
  'comparison_priority':priority})

add('R0','Historical ARC Representation','AUDIT_REFERENCE_ONLY','REFERENCE',
 'Exact saved Phase 13G representation; historical search/budget defects retained as recorded.','R0-H / Phase 2A historical DSL',LEGACY,
 'Whole-grid integer matrix only; no object records.','No explicit relation graph or predicates.',
 'No general composition; one atomic candidate at a time. rotate_180/270 are fixed atomic programs.',
 'Historical ordered 10-program DSL; discovery default 10 vs config 3; scored arms cap3; first-fit. Not eligible as matched causal baseline.',
 'Not corrected or rerun. Historical outcomes are descriptive only; low coverage does not prove semantic impossibility.')
add('R1','Current Production Bounded Representation','PRIMARY_REFERENCE','REFERENCE',
 'Same ten-program inventory and semantics as R0, run under the Phase 2C frozen test-output-blind budget/log protocol.','R0 corrected reference (Phase 2A R0); Phase 2C S4',LEGACY,
 'Whole-grid integer matrix; no object records.','No explicit relation graph or predicates.',
 'No general composition; one atomic candidate at a time.','Phase 2C frozen S4: ten candidate trials maximum, flat one-level fixed-order enumeration, first exact demo-fit; separate test-sealed evaluator. This is a corrected execution reference, not a new representation.',
 'S4 covers only the finite existing DSL; no-fit means not found within this bounded search. This is the causal comparison baseline, not proof of full ARC coverage.',
 'PRIMARY_CONTROLLED_COMPARATOR')
add('R2','Primitive-Expanded Whole-Grid DSL','ALTERNATIVE','T1_PRIMITIVE_EXPANSION',
 'Fully specified finite operator additions; implementation and grammar hashes pending.','None',
 LEGACY+['crop_nonbackground_bbox','pad_to_demo_shape','recolor_many_to_one','translate_selected_color','tile_grid_2x2_or_3x3','erase_one_color'],
 'No object IDs or per-object record; only whole-grid raster and global color/palette summaries.',
 'No explicit relation graph. Pixel adjacency remains implicit in grid operations.',
 'Atomic whole-grid candidates only; composition disabled.' ,
 'Same flat candidate-enumeration interface/cap; immutable candidate IDs; deterministic canonical order is frozen before use. Parameter expansions count as individual candidate hypotheses; cap10 applies to evaluated hypotheses.',
 'Added primitives may increase candidate-space size. Ten-trial coverage measures representation-plus-fixed-budget performance, not exhaustive language ceiling. No arbitrary fill, hidden parser, or test-label parameter inference.')
add('R3','Object-Centric Representation','ALTERNATIVE','T2_OBJECT_CENTRIC',
 'Deterministic object parser and one-action object-rule grammar specified; not implemented.','Decomposes Phase 2A proposed R1 object-centric relational candidate into R3 object base + R4 relation extension',
 ['parse_same_color_4_connected_components','select_by_color','select_by_area_rank','select_by_bbox_shape','select_by_border_contact','move_selected_object','copy_selected_object','delete_selected_object','recolor_selected_object','rotate_or_reflect_selected_object','crop_selected_bbox'],
 'Background color fixed to 0; foreground objects are same-color 4-connected components. IDs sorted by (top,left,color,mask lexicographic). Store color, occupied-cell mask, bbox, h/w, area, rational centroid, shape signature, border/contact flags. Eight-connectivity and alternate background are separate future variants.',
 'No relation edges used by the R3 selector grammar; position, color, shape, size, and border are object-local selectors only.',
 'One selected object action per candidate; composition and conditional relation rules disabled.',
 'Parser emits representation records; candidate is one selector+action+parameter hypothesis; deterministic grammar order, cap10; exact demonstration fit; no test access.',
 'Same-color touching objects merge; background=0 assumption; objects are inferred from grids, not ground truth. Segmentation failures/ambiguity are explicit parser states, not no-fit.')
add('R4','Relation-Centric Scene Graph','ALTERNATIVE','T3_RELATION_CENTRIC',
 'Finite relation graph and one-relation conditional action grammar specified; not implemented.','Phase 2A proposed R1 relational layer',
 ['R3_object_parser','rel_above','rel_below','rel_left_of','rel_right_of','rel_edge_adjacent','rel_overlap','rel_bbox_contains','rel_same_color','rel_same_shape','rel_aligned_center','rel_aligned_edge','rel_area_order','conditional_grid_action'],
 'Reuse exact R3 object parser and object fields; nodes are object records with stable IDs.',
 'Directed above/below/left/right use strict bbox separation; adjacency means any orthogonal neighboring occupied-cell pair; overlap means masks intersect; containment means bbox contains; same-color/shape exact equality; alignment exact equal center/edge coordinate; area-order compares cell counts. Predicates and parameter ranges are finite and unit-tested before use.',
 'One relation predicate (or its negation) plus one R3 object action; conjunctions/recursion disabled.',
 'One full conditional-rule program is one flat trial under cap10; canonical lexicographic relation/selector/action order; first exact demo fit.',
 'This adds both object parsing and relation use relative to R1; not a single-factor relation contrast against raster R1. R3-vs-R4 is the cleaner incremental relational contrast.')
add('R5','Hierarchical Object/Group Representation','ALTERNATIVE','T4_HIERARCHICAL',
 'Bounded object-to-group hierarchy and group-action grammar specified; not implemented.','None',
 ['R3_object_parser','group_by_same_color','group_by_shape_signature','group_by_edge_adjacency','group_member_count','group_bbox','group_color_histogram','move_group','copy_group','delete_group','recolor_group','apply_same_action_to_members'],
 'R3 object nodes plus group nodes at maximum 3 hierarchy levels: cell-component → object → group. Group IDs sorted by canonical member object IDs; overlapping groups prohibited within one candidate.',
 'Membership edges and R4 relations on object/group bounding boxes; predicate vocabulary finite and inherited definitions frozen.',
 'One group selector+one group action; no nested plans, loops, or general program composition.',
 'Flat enumeration over complete group-rule candidates, cap10; same first-fit, exact demo, compute/resource budget.',
 'Hierarchy can change segmentation and search-space size; parse/ambiguity failures must be logged separately. No semantic group truth labels assumed.')
add('R6','Bounded Compositional Whole-Grid DSL','ALTERNATIVE','T5_COMPOSITIONAL',
 "Finite AST over R1's exact ten atomic programs; bounded compositions specified; not implemented.",'None',
 LEGACY+['compose_2_atoms','compose_3_atoms'],
 'Same whole-grid raster as R1; no objects.', 'No explicit relation graph.',
 'Program ::= atom | atom∘atom | atom∘atom∘atom. No loops, branches, recursion, learned macros, or arbitrary code. Intermediate grids are explicit; invalid intermediate outputs fail the candidate.',
 'Each complete AST is one flat candidate trial (search depth remains one); deterministic order by AST length then canonical atom IDs; cap10. Fit rule/budgets identical.',
 'The language expands through composition while the candidate-trial cap remains fixed; no-fit is budgeted search failure, not proof the finite composed language lacks a fit.')
add('R7','Hybrid Object-Relation-Hierarchy-Composition','ALTERNATIVE','T6_HYBRID',
 'Finite union of R3–R6 with max one relation condition, one selected object/group target, and at most two actions; not implemented.','None',
 ['R3_object_primitives','R4_relation_predicates','R5_group_primitives','compose_at_most_2_actions'],
 'R3 parser plus R5 groups, with same deterministic object IDs.',
 'R4 finite predicate vocabulary; one relation antecedent only.',
 'Rule ::= optional_relation_guard + selector + action | optional_relation_guard + selector + action∘action. No branching beyond one guard; no recursion.',
 'Flat complete-rule enumeration and cap10, canonical cost then ID order; all standard resource caps unchanged.',
 'Bundles several representational changes; any gain cannot identify which component caused it. Secondary/future condition only, after component contrasts.')
add('HCC','High-Coverage Known-Rule Control','POSITIVE_CONTROL_NOT_ARC','REFERENCE_CONTROL',
 'Specified positive-control task generator/reference; not built or run.','Phase 2A HCC',
 ['six known shared transformations: identity, horizontal/vertical reflection, rotation_90, global bijective recolor, constant translation'],
 'Generated task families chosen so equivalent rules are explicitly expressible in each compared representation; task instances share paired IDs.',
 'Known rule and independent generated semantic-family label stored outside solver input.',
 'Each control task has one known generating rule; exact target generated by versioned deterministic code.',
 'Same coverage runner/candidate cap where applicable; separate oracle condition maps known generator to exact output to verify evaluator plumbing.',
 'Synthetic/procedural control only. It tests plumbing and threshold activation, never ARC generality or ASFT efficacy.',
 'PLUMBING_CONTROL_ONLY')

# Explicit parameter/semantics freeze for each representation row.
PARAMS={
 'R0':'Exact historical Phase 13G semantics: translate_constant uses up to 16 deterministic rare-color anchors; recolor_bijection is global one-to-one; other eight programs are parameter-free fixed transforms. Historical discovery/runtime cap mismatch remains attached to R0.',
 'R1':'Same exact ten primitive semantics as R0. Translation/recolor parameter inference is unchanged; Phase 2C S4 common cap is ten evaluated candidate programs.',
 'R2':'crop_nonbackground_bbox crops to tight bbox of all nonzero cells (all-zero input invalid); pad_to_demo_shape only pads bottom/right with 0 to one target H/W uniquely inferred from train pairs and rejects if source exceeds target; recolor_many_to_one is one global input-color→output-color map over colors in training demos, non-injective allowed, exact replay required; translate_selected_color selects one nonzero color present in every demo and applies one constant integer (dy,dx) inferred from demos, no wrap, vacated cells=0, collisions invalid; tile_grid repeats both axes by the same factor k∈{2,3}; erase_one_color chooses one nonzero training-demo color and sets it to 0. Each parameter assignment is a separate candidate ID; lexicographic parameter serialization within fixed primitive ID.',
 'R3':'Object selectors are one of: exact color; area rank among current objects; exact normalized bbox aspect/shape signature; border-contact boolean. Candidate action is move with integer dy,dx∈[-2,2], copy, delete, recolor to any color 0..9, rotate by k×90° (k∈{1,2,3}) around object bbox center, reflect about bbox horizontal/vertical axis, or crop object bbox. Invalid collision/out-of-grid candidates are rejected; all params are fit/verified using training demos only.',
 'R4':'One ordered object-selector pair plus one relation from the frozen vocabulary, optionally negated (no conjunction); consequent is one R3 action with same finite parameter domains. Relation predicates are computed from parsed training objects only; any ambiguous parse is parser-ambiguous, not a rule no-fit.',
 'R5':'Groups are canonical sets generated by exactly one grouping rule (same color, same shape signature, or connected by edge-adjacency); max hierarchy depth 3; one group selector and one action from move/copy/delete/recolor/transform-members. Candidate params are finite and demo-inferred as in R3; overlapping memberships invalidate a candidate.',
 'R6':'Atomic programs are exactly the ten R1 operators. Complete programs of length 1, 2, or 3 are generated; composition is left-to-right with each intermediate grid validated. Candidate order is length then canonical ordered atom IDs and inferred parameter serialization; no branching, loops, recursion, or learned macro.',
 'R7':'One optional R4 relation guard; one R3/R5 selector; one or two actions from object/group move, copy, delete, recolor, rotate/reflect; intermediate grids validated. No other predicates, conjunctions, loops, branches, or recursion; parameters follow R3/R5 finite domains.',
 'HCC':'Six deterministic, known rule families shared across conditions: identity, horizontal/vertical reflection, 90-degree rotation, global bijective recoloring, and constant translation. Generate 20 task IDs per family (120 total), at least 2 train demonstrations/task; rule/task-family label is retained outside solver input. Each registered representation must have an explicitly verified equivalent program for every HCC task; oracle answers are used only by the control evaluator.'}
for row in ROWS: row['parameterization_semantics']=PARAMS[row['representation_id']]

# Registry CSV
PKG.mkdir(parents=True,exist_ok=True)
with (PKG/'representation_registry.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(ROWS[0]));w.writeheader();w.writerows(ROWS)

# Comparison plan rows
matrix=[]
for alt,contrast,question,priority in [
 ('R2','R1 vs R2','Does finite whole-grid primitive expansion improve coverage/trace yield under equal candidate/resource cap?','SECONDARY_EXPLORATORY'),
 ('R3','R1 vs R3','Does object parsing/action representation improve coverage and activation?','PRIMARY_ALTERNATIVE'),
 ('R4','R3 vs R4','Does adding explicit relation predicates improve the object-centric representation?','SECONDARY_COMPONENT_CONTRAST'),
 ('R5','R3 vs R5','Does adding an object/group hierarchy improve coverage and activation?','SECONDARY_COMPONENT_CONTRAST'),
 ('R6','R1 vs R6','Does bounded program composition improve coverage and activation?','SECONDARY_COMPONENT_CONTRAST'),
 ('R7','R3/R4/R5/R6 vs R7','Does the hybrid add benefit beyond the specified components?','LATER_ONLY_MULTIFACTOR'),
]:
 matrix.append({'contrast_id':contrast,'alternative_id':alt,'primary_endpoint':'paired training-demo-fit coverage under fixed B1-B6; accuracy excluded',
  'secondary_endpoints':'valid trace rate; successful trace yield; recurrence/support; candidate and validated invariant yield; skill eligibility; transfer eligibility; capability eligibility',
  'same_task_ids':'yes, prospectively frozen common task set; prior Phase13G holdout is not pristine confirmation',
  'held_fixed':'input demonstrations; search algorithm/flat trial policy; candidate cap10; depth1; B3 trace cap; B4/B5; support/miner/validator/skill/transfer/capability code and thresholds; evaluator',
  'intended_representation_change':question,'analysis_unit':'task_id; paired risk difference and discordant win/loss/tie counts; 95% paired bootstrap CI; exact numerators/denominators',
  'interpretation_rule':'No fit means not found within declared language and budget; attribution to representation requires parity, measured implementation, and no protocol violation.',
  'priority':priority,'status':'FRAMEWORK_ONLY_NOT_RUN'})
with (PKG/'comparison_matrix.csv').open('w',newline='',encoding='utf-8') as f:
 w=csv.DictWriter(f,fieldnames=list(matrix[0]));w.writeheader();w.writerows(matrix)

config={'phase':'ASFT-V1.1-PHASE-2F','package':'ASFT-V1.1-PHASE-2F-REPRESENTATION-ALTERNATIVES-V1',
 'status':'FRAMEWORK_ONLY_NO_REPRESENTATION_COMPARISON_RUN',
 'legacy_namespace_note':'Phase2F registry follows user labels R0 historical, R1 current production. Phase2A called its object-centric relational proposal R1; Phase2F decomposes it into R3 object base plus R4 relation extension. Phase2A R0 corrected reference maps to Phase2F R1.',
 'representation_reference':{'R0':'historical 13G exact language and mismatched historical path; audit-only','R1':'same ten programs under current Phase2C frozen test-blind execution; matched comparison baseline'},
 'primary_comparison':'R1 vs R3 object-centric; R2 primitive-expanded and R4-R7 are specified secondary/component/hybrid alternatives.',
 'common_task_data':{'training_demo_only':True,'same_task_ids_per_representation':True,'prospective_common_evaluation_set_required':True,'all_1000_phase2c_task_ids_previously_audited':True,'existing_phase2c_set_confirmatory_use':'diagnostic_only; all IDs have prior coverage/trace/invariant inspection','confirmatory_data_requirement':'new authorized untouched common split; do not use historical Phase13G holdout as pristine','historical_13g_holdout_pristine':False,'test_outputs_parsed_or_used':False},
 'common_search_budget':BUDGET,
 'common_fit_rule':'All available training demonstration pairs must be reproduced exactly; first exact fit under deterministic order; no fit is NOT_FOUND_WITHIN_LANGUAGE_AND_BUDGET, never semantic impossibility.',
 'trace_contract':{'records_per_task_condition':1,'max_high_level_steps':4,'schema_validator_required':True,'no_partial_trace_from_failed_candidate':True,'full_candidate_trial_ledger_separate':True},
 'downstream_frozen':{'miner':'unchanged Phase 2E TraceMiner','min_frequency':5,'min_cross_trace':5,'min_consistency':1.0,'min_task_families':2,'skill_pipeline':'existing SkillConfig and qualify_candidate','transfer_applicability_minimum':3,'capability_pipeline':'existing CapabilityConfig and lifecycle'},
 'statistics':{'independent_unit':'task_id','primary':'paired coverage risk difference','report':'win/loss/tie counts plus 95% paired bootstrap CI; predeclare seed, multiplicity handling, and practical delta before outputs','material_effect_threshold':'must be preregistered before execution; not selected in this framework'},
 'required_before_run':['implement each alternative and freeze code/grammar hashes','freeze shared independent task-family annotations or mark family-breadth endpoints unavailable','predeclare δ_coverage and δ_activation','freeze a prospective paired task set disjoint from representation development','test coverage-only runner cannot access test outputs','verify identical budget, trace, downstream and evaluator contracts','positive-control HCC generator and oracle run','authorize any sealed accuracy evaluation separately'],
 'prohibited':['claiming ARC accuracy from demo-fit coverage','claiming transfer/capability from coverage alone','calling no-fit semantic unrepresentability','automatic representation-root-cause attribution','promoting exploratory results to confirmatory','using outcome-derived program labels as independent task-family labels']}
(PKG/'phase2F_framework_config.json').write_text(json.dumps(config,indent=2)+'\n')
