# Failure Cascade Analysis

| Stage | Intended transition | Observed record | Failure/status |
|---|---|---|---|
| ARC task IDs → loaded grids | Load disjoint discovery/transfer/holdout tasks | 600/200/200 public training tasks; task files loaded | Completed; not the primary bottleneck |
| Grid → bounded program fit | At least one DSL candidate exactly fits all demonstrations | Full 10-program scan: 3/600, 5/200, 2/200 | First major bottleneck; near-total miss |
| Fit → trace | Record operation and demonstration verification | 600 schema-valid discovery trace rows; only 3 successful exact-fit traces | Serializer works; successful trace population is tiny |
| Trace population → invariant | Mine recurring signatures from successful traces | 3 traces in miner; programs are 1 each; min frequency/cross-trace support 5; raw patterns/candidates 0 | No qualifying invariant population; IDT not meaningfully tested on diverse ARC traces |
| Invariant/support → ASFT skill | Require support and transfer qualification | Support per program 1; minimum 5; eligible programs []; skills 0 | Mechanically blocked |
| Skill → learned transfer | Apply validated learned skills on transfer tasks | Learned-skill applicability denominator 0; precision null; ASFT exact task accuracy 0/200 | Skill-based transfer claim unavailable; bounded solver performance remains poor |
| Discovery memory → episodic baseline | Nearest-episode retrieval | B2 solves 1/200 transfer tasks | Narrow memory event, not ASFT skill transfer |
| Skills → capability group | Propose validated multi-skill group | 0 skills/capability groups | Downstream stage cannot activate |
| Capability → CGM / IG | Compute C_t/CGR/IG if required capability exists | Unavailable in every discovery prefix | No positive or negative ARC growth estimate |

## The cascade is not “no data”

The run processes the task IDs and produces trace/task records. It does not provide a useful *successful task-derived program population* to IDT. The correct mechanism inference is that the learned chain is untestable under the observed coverage and gates—not that no ARC information at all entered the system.

## Arm-level distinction

The full-DSL coverage scan tests all ten operations; main transfer/holdout arms test at most three candidates. A source audit adds a material discrepancy: frozen config declares three candidates per task, but `discover()` defaults to ten. Thus discovery fit and coverage counts are full-inventory counts, not discovery rates under the declared limit. Among the three saved successful fits, only `reflect_vertical` is within the first three fixed programs; this is a code/results implication, not a rerun. ASFT has no learned ordering, B3/B4 have no support-qualified operator pool, and B1 uses fixed order. B2 can insert the nearest stored discovery program before fixed search. This explains why full-inventory fit counts and arm-level accuracy differ and why one memory-baseline transfer success can occur despite zero ASFT skills.
