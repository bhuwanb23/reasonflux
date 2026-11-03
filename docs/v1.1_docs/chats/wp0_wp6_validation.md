This will give you a copy-paste-ready operational package for WP3 execution. The goal is to make it easy for your human annotators while preserving the independence requirements already frozen in Phase 2I-A.
WP3 Human Annotation Execution Checklist
Package
 
ASFT-V1.1-WP3-INDEPENDENT-FAMILY-ANNOTATION
 
Purpose
Produce a frozen, independently adjudicated:
 
Task → Primary Family
 
mapping for the 600 discovery tasks.
1. Personnel Assignment
Required Roles
Annotator A
Responsibilities:
 
Label all 600 tasks
 
Provide rationale
 
Provide confidence
 
Provide evidence pair indices
 
Must not see:
 
Annotator B labels
 
Adjudicator decisions
 
Solver outputs
 
R1 outputs
 
R3 outputs
 
Candidate yield
 
Annotator B
Responsibilities:
 
Same as Annotator A
 
Must remain fully independent.
Adjudicator
Responsibilities:
 
Review disagreements
 
Review ambiguous cases
 
Issue final label
 
Must not participate as:
 
Annotator A
 
or
 
Annotator B
 
2. Materials Preparation
Packet A
Contains:
 
task_id
 
training demonstrations
 
blank annotation fields
 
Packet B
Contains:
 
task_id
 
training demonstrations
 
blank annotation fields
 
Verify Exclusions
Confirm packets contain:
 
NO test inputs
 
NO test outputs
 
NO solver traces
 
NO candidate outputs
 
NO family labels
 
NO prior annotations
 
Checklist:
 
☐ Verified
 
3. Annotator Instructions
Provide the frozen ontology only.
Allowed primary labels:
 
OBJ_RELATION
 
SPATIAL_CHANGE
 
COLOR_ATTRIBUTE
 
COUNT_REPLICATION
 
PATTERN_COMPLETION
 
REGION_TOPOLOGY
 
FRAME_BOUNDS
 
SYMBOLIC_SEQUENCE
 
COMPOSITE_RULE
 
UNKNOWN_AMBIGUOUS
 
Annotators answer:
Q1
 
Primary family
 
Required.
Q2
 
Confidence
 
Choose:
 
HIGH
 
MEDIUM
 
LOW
 
 
Q3
 
Supporting pair indices
 
Example:
 
1,2,3
 
Q4
 
Brief rationale
 
1-3 sentences.
Q5
 
Secondary tags (optional)
 
Not used for eligibility.
4. Independence Verification
Before annotation begins:
Independence Checklist
Annotator A confirms:
 
☐ No access to Annotator B labels
 
☐ No solver outputs viewed
 
☐ No candidate outputs viewed
 
Annotator B confirms:
 
☐ No access to Annotator A labels
 
☐ No solver outputs viewed
 
☐ No candidate outputs viewed
 
Adjudicator confirms:
 
☐ Not involved in coding
 
☐ No solver outputs viewed
 
5. Annotation Execution
For every task:
Annotator completes:
 
Primary family
 
Confidence
 
Evidence indices
 
Rationale
 
Rules:
 
Never infer test behavior
 
Never inspect test data
 
Never use solver reasoning
 
Never use representation assumptions
 
If uncertain:
 
Use UNKNOWN_AMBIGUOUS
 
6. Agreement Analysis
After both coders finish.
Generate:
 
Agreement table
 
Confusion matrix
 
κ statistic
 
Missing count
 
Ambiguous count
 
Checklist:
 
☐ Exact agreement computed
 
☐ κ computed
 
☐ Confusion matrix generated
 
7. Agreement Decision Rule
If
 
κ ≥ 0.70
 
Proceed to adjudication.
If
 
κ < 0.70
 
Stop.
Create:
 
Rubric clarification report
 
without viewing:
 
Candidate yield
 
R1 outputs
 
R3 outputs
 
Then:
 
Version rubric
 
Re-run coding
 
8. Adjudication
Only disagreement cases proceed.
For each disagreement:
Adjudicator records:
 
Annotator A label
 
Annotator B label
 
Final label
 
Reason
 
Must use:
 
Training demonstrations only
 
Must not use:
 
Solver outputs
 
Trace outputs
 
Candidate outputs
 
Test outputs
 
9. Final Freeze
Produce:
 
task_family_map.csv
 
Fields:
 
task_id
 
final_primary_family
 
annotation_version
 
adjudication_status
 
Produce:
 
agreement_report.md
 
Produce:
 
adjudication_log.csv
 
Generate hashes for:
 
Family map
 
Agreement report
 
Adjudication log
 
Rubric version
 
Checklist:
 
☐ Family map frozen
 
☐ Hash generated
 
☐ Version recorded
 
10. WP3 Completion Gate
WP3 is complete only if:
 
☐ Annotator A completed
 
☐ Annotator B completed
 
☐ Adjudicator completed
 
☐ κ ≥ 0.70
 
☐ Disagreements adjudicated
 
☐ Family map frozen
 
☐ Hashes recorded
 
☐ No prohibited data accessed
 
Deliverables
 
packet_A.csv
 
packet_B.csv
 
annotator_A_labels.csv
 
annotator_B_labels.csv
 
agreement_report.md
 
confusion_matrix.csv
 
adjudication_log.csv
 
task_family_map.csv
 
family_map_hash.txt
 
wp3_completion_review.md
 
Final Success Condition
WP3 succeeds when you can truthfully state:
Two independent annotators labeled all 600 discovery tasks using only training demonstrations, disagreements were resolved by an independent adjudicator, agreement statistics were recorded, and a frozen, hash-pinned family map was produced without access to solver outputs, candidate yields, test data, or future outcomes.
Only then should the family map become eligible for use in the later Phase 2I candidate-production run.