# Repository review incorporation and implementation order

Date: 16 November 2026 (Australia/Brisbane). Reviewed baseline:
`c6892497aa0b03555d5145242c04965471eccc1d` on `master`.

The owner requested incorporation of the repository review into Conductor and
an ordered implementation report. This refinement makes the recommendations
actionable within existing tracks. It does not implement the pending fixes,
accept D0, qualify a model, or establish an operational capability.

The canonical queues remain the [Track 13 plan](./plan.md), the
[25 Track 12 work packages](../cognitive-autopsy_20261107/work-packages.md), and
the [Track 14 plan](../death-review_20261113/plan.md). Recommendation keys below
are traceability labels, not new work packages. Preserve the 24 FAW packages,
25 CAW packages and D0–D8 identifiers. The
[machine-readable order](./execution-order-20261116.json) is a planning view of
those queues, not a second scheduler. The
[incorporation receipt](./recommendations-evidence-20261116.md) records evidence
and delivery limits.

## Ownership and concurrent work

Coordinator conversation `6af6164f-cf84-8321-9f96-8b7d685aabe5` remains the sole
shared integrator and merge owner. This branch supplies a concrete Conductor
integration proposal. Shared contracts, canonical schemas, CI, locks, runtime
dispatch and release decisions retain their existing ownership.

| Existing scope | State observed on 16 November | Incorporation boundary |
|---|---|---|
| Track 13 FAW07 / D0 | Draft implementation [#132](https://github.com/edithatogo/rcagent/pull/132), head `4746027c7de6cd4e0ed1518241f847146d79faef`; draft verification [#133](https://github.com/edithatogo/rcagent/pull/133), head `4057512f23a2301d6ffe4649e42fb055eeb83937`; acceptance pending | Preserve the [exclusive file contract](./faw07-d0-contract.md). This refinement neither takes over the two workers nor widens their increment. Reconcile fresh heads before integration. |
| Track 12 | Scientific components CA01–CA12 / CAW01–CAW25 | Add requirements to existing leaves; preserve corpus, split, model and research ownership. |
| Track 14 | Death-review planning and source register; runtime and practice claims unqualified | Consume accepted shared components. Source gaps block only the affected jurisdiction/profile claims. |
| AcciMap, [#139](https://github.com/edithatogo/rcagent/issues/139) | Separately authorised guided workflow and synthetic companion graph; track ID `accimap-workflow_20261116`; track number not allocated here | Existing owner retains `tools/accimap.py`, `evaluation/accimap/**`, `tests/test_accimap.py`, `tests/fixtures/accimap/**`, the AcciMap guide and its track namespace. Link its handoff; do not duplicate implementation or claim acceptance. |
| HEAPS, [#140](https://github.com/edithatogo/rcagent/issues/140) | Separately authorised Queensland Human Error and Patient Safety review planning; track ID `qld-heaps-review_20261116`; track number not allocated here | Existing owner retains its track namespace and H1–H6 plan. Shared registration follows coordinator reconciliation. AcciMap is an optional accepted analytical view, not a prerequisite for every HEAPS packet. |

Existing authority for reversible work carries forward. A pending leaf becomes
available for bounded owner/file-scope assignment when its prerequisites pass;
this document does not claim it for a new worker. Maintain one integration lane
and at most two active implementation lanes. The parallel scopes above are an
ownership inventory, not an instruction to run them all simultaneously.

## Recommendation-to-work-package map

All implementation acceptance below is **pending**. Historical accepted work
and negative study evidence remain unchanged.

| Key | Recommendation and owning scope | Concrete acceptance |
|---|---|---|
| R01 | Repair renderer admission: follow-up to accepted FAW01; required by FAW14/16 when using this view | `interface_actions.render_view` consumes the canonical domain validator. Unknown source references, duplicate source IDs and illegal workflow transitions reject at both boundaries. Valid records, hash binding, audience/privacy policy and rejection behaviour remain compatible. Add composition/property/mutation regressions. |
| R02 | Consolidate small code paths and measure before optimising: FAW06 maintenance / CAW02/08; optional FAW20 | Reuse `jsonschema`; cache schema/validator instances by immutable version or digest with the same format/reference policy. Use `collections.Counter` for duplicate-ID detection. Preserve error semantics. Version hash/serialisation adapters without changing historical receipts. Split retrieval/rendering responsibilities only when a bounded change improves contract ownership. No full rewrite or new validation framework. |
| R03 | Deliver the useful deterministic path: FAW07–10 / D0–D3; CAW02/04/08/10/20 | A reproducible command and inspected outputs cover source binding, explicit extraction, uncertain chronology and actor/cutoff-specific evidence plus patient/family concerns. Unknowns, contradictions and missing voice survive. Each stage has positive and discriminating negative fixtures and exact-version receipts. |
| R04 | Admit dependencies through replaceable adapters: CAW01/04/05/07/21/22; FAW11–13/18 | Reuse conventional NLP/ML, document parsing and evaluation infrastructure where the fit-gap receipt demonstrates benefit. Keep heavy dependencies optional. Record exact versions, licences, installation/resource impact, privacy/egress, independent tests and disable/replace paths; a candidate name alone does not become supported. |
| R05 | Enforce permitted evidence everywhere: CAW10/20/21; FAW09/10/14/15 | Test event, recording and recipient-availability clocks across retrieval, snippets, metadata, caches, verifiers and final rendering. Unknown availability stays unknown. A late result cannot leak through a second path. Actual traffic/log/cache canaries substantiate isolation claims before sensitive execution. |
| R06 | Source-qualify method views: CA08; FAW16; existing AcciMap owner | Record method, adaptation/version and source basis. Typed nodes/edges distinguish observations, accounts, hypotheses, support, conflict and gaps. Preserve unsupported/unassigned items and legitimate feedback; no universal DAG assumption or automatic causal validity. AcciMap is delivered by #139. CAST/STPA/FRAM extensions remain source-qualified CA08 work, not claimed implemented. |
| R07 | Make capability status inspectable: FA12/FA13 requirements under FAW18 and coordinator-owned delivery metadata | Generate a status view from existing manifests and receipts with distinct release, source implementation, synthetic test, benchmark, workflow and operational states. Bind task/configuration/date/exclusions. Missing evidence yields unknown. Update stale documentation from observed evidence, not a hand-maintained second registry. |
| R08 | Compose packets and propagate evidence changes: FAW14/16; CA08–CA12; DR-04–12 | Compose only qualified included components. A corrected, withdrawn or newly unavailable source invalidates or queues re-review of dependent claims, views, exports and action justifications; retain immutable history and independent unaffected outputs. Final prose/omissions are checked after rendering. Test complete, incomplete and contradictory cases and record correction burden. |
| R09 | Strengthen evaluation and report-quality scoring: CAW03/05/07/21/22/25; FAW11/13/17/18; DR-13–19 | Freeze family splits and material-error/useful-coverage criteria before holdout access. Compare rules/classical NLP, the same model with a competent prompt, portable skill and verified pipeline. Report severe errors, omissions, concern fidelity, false blocking, abstention, cost and failures. Reuse source-qualified LRRT/IGZ rubric items where applicable, with rights and agreement assessed; report quality is distinct from clinical benefit. |
| R10 | Test workflow benefit only when claimed: FAW19; DR-20/21; HEAPS H6 through its owner | A bounded study can compare ordinary review, deterministic evidence viewer, and viewer plus generated assistance, using randomised/counterbalanced allocation where feasible. Observe omissions, detection of seeded unsupported claims, correction time, reviewer reliance and burden; label agent and human observations. This is a research design, not an added human engineering-approval step. |
| R11 | Prioritise availability-sensitive investigation research: CAW11/12/21/22; FAW17/18 | Use the existing independent-session 2×3 outcome/availability design. Test invariance to irrelevant outcome exposure and sensitivity to genuinely available decision-relevant cues separately. Use family-clustered analysis, blinded references and held-out source/style variants. A model that ignores every new fact cannot pass as hindsight-resistant. |
| R12 | Make further research conditional: CAW16–19/23/24; FAW20–24; DR-22/23 | Process adapters preserve interval/partial-order uncertainty; deviations are not clinical errors. Formal value of information needs explicit states, priors, likelihoods, utilities and acquisition cost. Compare questions at fixed evidence/reviewer budget. Measure action implementation separately from effects. Rust needs a measured bottleneck; adaptation needs persistent learnable residual errors; broader claims need replication. Preserve negative results and simpler fallbacks. |

### R01: confirmed boundary defect, not a speculative refactor

At the reviewed baseline,
[`render_view`](https://github.com/edithatogo/rcagent/blob/c6892497aa0b03555d5145242c04965471eccc1d/tools/interface_actions.py)
uses a JSON Schema validator and a source hash but does not call
[`evidence_core.validate_record`](https://github.com/edithatogo/rcagent/blob/c6892497aa0b03555d5145242c04965471eccc1d/tools/evidence_core.py).
On the existing generated-synthetic fixture, three separately mutated records
were rejected by the canonical validator and accepted by the renderer: an
unknown evidence source, a duplicate source ID, and an invalid state transition.
The valid control passed both. The renderer already admits only
`generated_synthetic` data; this observation does not establish an operational
data leak. The [receipt](./recommendations-evidence-20261116.md) supplies the
bounded reproducer and its limits.

R01 is a new follow-up to previously accepted FAW01, not a retrospective change
to its acceptance. It can run alongside D0 only after the coordinator confirms
non-overlapping files. It is required before accepting composed outputs that
use the renderer, not a fabricated prerequisite for unrelated D0 work.
The fix must retain canonical format checking and rejection of unreferenced
duplicate IDs and invalid relationship endpoint types, rather than copying
only the three demonstrated checks into another validator.

## Dependency reuse decisions

Keep the [integration map](../../integration-map.json) authoritative. The rows
below select assessments or preserve current components; they do not promote
an untested candidate to `adopt` or install it in the portable core.

| Use | Preferred reuse and small rcagent-owned gap | Admission/stop condition |
|---|---|---|
| Record validation | Existing [`jsonschema`](https://python-jsonschema.readthedocs.io/en/stable/validate/) plus the canonical domain validator | Cache only with equivalent formats/local-reference handling; do not introduce competing Pydantic or handwritten schema engines. |
| Retrieval | Existing [SQLite FTS5](https://www.sqlite.org/fts5.html) / BM25 | Add version, rights, case and availability filters; add vector/reranker complexity only after measured lexical failures. |
| Explicit extraction and classical baseline | Optional [spaCy rules](https://spacy.io/usage/rule-based-matching), [medspaCy](https://github.com/medspacy/medspacy), [scikit-learn grouped validation](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GroupKFold.html) | Preserve original offsets, polarity, attribution, train-only fitting and family splits. Do not make model availability a prerequisite for the deterministic packet. |
| Document/layout ingestion | Assess [Docling document representation](https://docling-project.github.io/docling/concepts/docling_document/) | Map page/table/span coordinates to immutable originals; pin parser and any model artifacts separately. Enable only for a demonstrated ingestion need, with rights/egress and resource evidence. |
| Model-study orchestration | Assess a thin [Inspect AI](https://inspect.aisi.org.uk/) adapter | Reuse generic runs/scorers/log structure where compatible; preserve rcagent receipts, all-attempt denominators and permitted views. Local logs/scorers must meet the privacy contract. Deterministic tests remain usable independently. |
| Method/provenance graph mechanics | Existing structures first; optional [NetworkX MultiDiGraph](https://networkx.org/documentation/stable/reference/classes/multidigraph.html) only when needed | rcagent owns typed edge semantics, source binding and review state. Graph algorithms do not supply causal authority. |
| Interoperable evidence export | [W3C PROV-O](https://www.w3.org/TR/prov-o/) and optional [RO-Crate](https://www.researchobject.org/ro-crate/) tooling | Consumer-driven mapping with provenance round-trip, local-only defaults and explicit export losses. No automatic remote retrieval. |
| Hash interoperability | Preserve existing versioned formats; assess [RFC 8785](https://www.rfc-editor.org/rfc/rfc8785) only for a future cross-language contract | Existing serializers differ in Unicode escaping and hash-prefix conventions. Do not silently rehash prior receipts; require version negotiation and golden Unicode/numeric fixtures. |
| Process analysis | Qualified [Rust4PM](https://rust4pm.aarkue.eu/) consumer adapter; optional comparators separately admitted | Use upstream algorithms; document interval/order losses and distinct licensing. Do not build another discovery/alignment engine. |

Every optional adapter receipt must state the demonstrated gap, custom code
avoided, exact source/dependency/runtime tuple, independent positive and negative
cases, installation size, latency/memory, licence and data/egress behaviour,
maintenance owner, and disable/replace path. Measure representative workloads
before expanding a profile. Reuse does not justify replacing specialised
process/socket or privacy controls without parity evidence.

## Implementation order

This table is the preferred delivery path. Hard prerequisites attach to
individual outputs, not whole tracks. Existing source/rights and owner gates
apply throughout; preparation does not claim its dependency is complete.

| Order | Existing track/work packages | Exit and sequencing |
|---|---|---|
| 0 — finish the active increment | Track 13 FAW07 / D0; existing #132/#133 owners | Reconcile current heads and pass A0–A5 in the D0 contract. In a separately assigned scope, repair R01 before affected renderer composition; prepare corpus/source/dependency admissions and the capability-status design. Do not change D0 ownership. |
| 1 — explicit extraction | Track 13 FAW08 / D1; Track 12 CAW01–04/08 | Consume accepted D0 and source/span contracts. Demonstrate dates, units, negation, identity and ambiguity with preserved original offsets. Grouped source-family splits precede scored comparisons. |
| 2 — uncertain chronology | Track 13 FAW09 / D2; Track 12 CAW10 | Consume D1. Preserve event/recording/availability intervals, conflicting accounts and partial order; test cutoff boundaries. |
| 3 — useful evidence packet | Track 13 FAW10 / D3; Track 12 CAW20 | Consume D2. Produce an inspectable decision-time packet, patient/family concern trace and unresolved questions, with the permitted view enforced across every path. |
| 4 — qualify components and final output | Track 13 FAW11/13/14/15; Track 12 CAW05/07/09/11/12/21/22 | D4 compares conventional and selected model arms; optional critics must earn their cost. FAW14 qualifies claims, omissions and final rendering. Actual isolation evidence precedes sensitive execution. The availability experiment can be designed/piloted here under its own prerequisites. |
| 5 — compose selected profiles | Track 13 FAW16 / D6; Track 14 DR-04–12; existing AcciMap/HEAPS owners | Packet/fixture preparation may start after D3. Accept D6 only after R01, final-rendering/omission admission and qualification of every included component. A text-only deterministic packet need not wait for all D4 model arms, D5 OCR, CAW14/15 synthetic-world work, or CAW17–19 process studies. |
| 6 — establish frontier evidence | Track 13 FAW17–19 / D7; Track 12 CAW03/21/22/25; Track 14 DR-13–21 where applicable | Consume relevant D4 comparisons, accepted D6 and a frozen eligible external/temporal holdout. Report material errors at useful coverage, severe failures, concern fidelity, false blocking, reviewer effort and resource costs with case-clustered uncertainty. Human observations are needed only for the claims that require them. |
| 7 — selected research extensions | Track 13 FAW20–24 / D8; Track 12 CAW16–19/23/24; Track 14 DR-22/23 | Prefer one justified empirical hypothesis after promising comparative evidence. This is an investment priority, not a blanket D7 gate: independently useful source-to-trace/process adapters and a measured Rust spike may be implemented and accepted as soon as their canonical prerequisites pass. Add uncertain conformance, active evidence questions, action effectiveness or transportability selectively; adaptation requires its own residual-error evidence. |

### Parallel application profiles

AcciMap source/guide/graph work proceeds through #139's existing owner. Its
synthetic companion graph can qualify its own structural contract without
waiting for automatic extraction. It consumes accepted D1–D3 components only
when claiming extraction, chronology or decision-time behaviour.

HEAPS proceeds through #140: **H1 source applicability/scope → H2 guidance and
H3 profile/fixtures in parallel → H4 deterministic synthetic packet → H5
independent engineering qualification → H6 conditional local-template/practice
alignment**. Authorised inspection of the current blank local instrument may
run in parallel. Unknown local-template conformity must remain explicit but
does not block public-source planning or synthetic engineering.

Track 14 source reconciliation DR-01–03 and minimal packet/fixture design DR-04
can proceed alongside the main path. Only the affected policy-dependent output
waits for a source gap; generic extraction is not blocked by unresolved NSW/QLD
policy text. None of these profiles may claim more than the accepted shared
components they actually consume.

## What counts as frontier or beyond-frontier evidence

**Frontier** is a result for an exact task, evidence view and configuration:
useful improvement against the strongest relevant current baseline under a
frozen contrast, with omissions, severe errors, coverage, workload and cost
included. A new dependency, many agents, a polished report or a green software
suite does not establish that result. Refresh the primary literature and
available comparators at study freeze; publish rejection cards as well as
positive qualification cards.

**First research priority beyond that comparison:** test whether a system can
preserve contemporaneous decision context while changing its assessment when
genuinely relevant evidence becomes available. Use CAW12's existing 2×3 design,
not another parallel protocol. Separate behavioural invariance, cue sensitivity,
source validity and review quality; allow multiple defensible method maps when
the evidence does not identify a unique causal explanation.

As specified in the [controlled experiments](../../research/cognitive-autopsy/controlled-experiments.md),
outcome invariance concerns prospective decision justifiability and unsupported
blame. Harm/consequence fields and justified retrospective causal assessments
may change when relevant outcome evidence changes; do not impose blanket
invariance on every output field.

Reuse the [HSSIB learning-response review tool](https://www.hssib.org.uk/knowledge-exchange/learning-response-review-and-improvement-tool/)
as a candidate source for report-quality rubric items, and examine LRRT/IGZ
measurement in the [2026 Australian report study](https://academic.oup.com/intqhc/article/38/3/mzag077/8694671).
The instrument's applicability, exact version, rights, item definitions and
rating reliability must be admitted before use. Do not infer patient benefit
from report quality or reproduce restricted instruments in the portable core.

Other primary studies inform comparator and failure-mode selection rather than
serving as directly comparable rcagent benchmarks: the
[contributing-factor NLP comparison](https://pubmed.ncbi.nlm.nih.gov/42160079/),
[severity-classification study](https://pubmed.ncbi.nlm.nih.gov/42888060/), and
[radiation-oncology incident analysis study](https://journals.plos.org/digitalhealth/article?id=10.1371/journal.pdig.0001740).
Verify populations, models, tasks and scoring at freeze. Preserve natural model
errors separately from injected-error challenge sets; split all derivatives of
a case together and keep development decisions outside the holdout.

Later hypotheses concern information acquisition under uncertainty, uncertain
process reconstruction, and whether linked actions change observed outcomes.
They require explicit assumptions and appropriate follow-up evidence. No
architecture alone warrants a beyond-frontier, causal, economic or clinical
benefit claim.

## Acceptance, maintenance and rollback

The current incorporation is complete only when its links, JSON, canonical
package mappings, acyclic planning order, scope preservation and agent review
are verified and the exact publication state is reported. Runtime acceptance
remains with each original work package and its observed evidence.

At implementation handoff, assign a bounded file scope, record prerequisites,
test rejection paths, inspect the actual output and bind the receipt to the
tested revision. Keep early failure/resource limits, zero typing allowances and
historical negative evidence intact. Dependency fit-gap findings may reject an
adapter without blocking the independent deterministic path.

Rollback this planning refinement through a normal commit if its priorities
change. Revert or disable failed optional implementations independently;
preserve source snapshots, prior receipts, correction history and failed runs.
Never weaken disclosure or evidence gates merely to restore a desired output.
