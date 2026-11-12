# Process mining for cognitive autopsy

Status: planning only; sources checked 2026-11-07. No engine, dataset or model is qualified by this document, and no dependency installation or case processing has been performed.

Read with [component studies](./component-studies.md), [controlled experiments](./controlled-experiments.md), [verification and reuse](./verification-and-reuse.md), and the [component matrix](./component-matrix.md).

## Purpose and evidence boundary

Process mining can deconstruct the documented flow of events and test whether a trace is compatible with a specified process. A single case supports trace reconstruction and bounded conformance questions; discovery of a general process requires comparable cases. Conformance means agreement with the chosen process model, not good care. A deviation may be a sensible adaptation, a recording gap or a system problem. Frequency, order, alignment cost and a directly-follows graph do not establish causation, clinician cognition or culpability.

The first question is whether faithful event reconstruction improves subsequent safety analysis. Keep process algorithms upstream; rcagent owns the clinical evidence contract, uncertainty and interpretation boundaries, and the evaluation adapter. Source ingestion remains with the existing corpus pipeline.

## Source-to-assessment pipeline

| Stage | Required output and failure behaviour |
| --- | --- |
| Immutable source | Source revision, content hash and page/paragraph/span coordinates; preserve the original text and any extraction uncertainty. |
| Candidate events | Activity, actor/role, related objects and assertion status with exact support; rules and LLMs produce candidates, not findings. Unsupported events remain rejected or explicitly hypothetical. |
| Uncertain trace | Event-time intervals, documentation time and information-availability time, recipient and evidence of receipt where supported; retain unknowns, conflicts and partial order. |
| Optional exchange view | XES for case-centric traces or OCEL 2.0 for linked objects; record the mapping and any information lost by conversion. |
| Process engine | Discovery or conformance against an explicitly versioned model; attach the engine, options, input and output receipts. Do not silently treat uncertain input as a certain total order. |
| Clinical interpretation | Source-linked description of deviations, possible explanations and missing evidence; test this component separately. A result cannot become an RCA finding solely because an engine produced it. |

Use [XES IEEE 1849-2023](https://standards.ieee.org/ieee/1849/10907/) for ordinary case-centric exchange. [OCEL 2.0](https://www.ocel-standard.org/2.0/ocel20_specification.pdf) adds objects, changing attributes and qualified relationships; it is useful when an event involves an encounter, order, result, message and team. Its expressiveness does not by itself supply clinical semantics or uncertainty-aware analysis.

## Trace semantics and verification

- Keep occurrence, documentation and availability as three distinct clocks. Record precision, interval bounds, source timezone when present, and unknown values. Never invent a calendar date, time of day or event order to satisfy an importer.
- Availability is actor-specific. An information item existing is not proof that a particular clinician could access it; access is not proof of receipt or consideration. Preserve the distinction between a contemporaneous record, retrospective account, later appraisal and model hypothesis.
- Separate observed order, logically constrained order and unresolved order. Preserve ties and concurrency. Check impossible precedence cycles deterministically and return the conflicting evidence instead of deleting an inconvenient relation.
- Missing text is not an omitted clinical action. Mark a genuinely documented non-occurrence separately from an event hidden by the experimental packet builder, an extraction failure and an unknown history.
- Preserve the canonical uncertain trace outside any lossy exchange view. If an algorithm requires a total order, run a declared sensitivity analysis over admissible orderings or mark that input unsupported; do not report one arbitrary ordering as the observed pathway.
- Keep later outcomes and appraisals outside decision-time views, including object attributes, filenames, graph labels and cached engine inputs. Apply the existing A/B/C compartment contract to every derived representation.
- A normative model needs source, version, date, jurisdiction and applicability. Learning a model from complaint-selected cases estimates those documented pathways, not a population standard of good care.

Each run receipt records case-family and packet IDs, source and trace revisions, extractor/rules/model revisions, schema and exchange mappings, engine version/options, uncertainty treatment, normative-model provenance, failures and output hashes. Sensitive trace content stays in the admitted local environment; repository receipts contain only permitted metadata.

## Closest prior work and remaining contribution

[Buss et al. (2026), *Process mining between the lines: Extracting object-centric event logs from textual data*, Information Systems 140:102713](https://doi.org/10.1016/j.is.2026.102713) already combines heuristic NLP and generative extraction and evaluates synthetic and naturalistic text, including a legal judgment. Text-to-log extraction and an NLP/LLM comparison are not new by themselves. A plausible contribution is clinically grounded availability reconstruction and measured effects of extraction errors on safety judgments.

[Pegoraro, Uysal and van der Aalst (2021), *Conformance checking over uncertain event data*, Information Systems 102:101810](https://doi.org/10.1016/j.is.2021.101810) represents uncertain time, activity and case attributes and derives upper/lower conformance bounds. Its [author manuscript](https://vdaalst.com/publications/p1244.pdf) also describes controlled corruption experiments. Reproduce relevant baselines rather than claim uncertainty or perturbation testing as a new method.

## Three bounded experiments

| Experiment | Comparison and measurements | Claim supported and limitation |
| --- | --- | --- |
| Narrative-to-trace fidelity | Rules/medspaCy, a classical statistical baseline where annotations permit, an untuned local LLM and a hybrid; event/actor/object extraction, supported temporal relations, uncertainty retention, fabricated events and critical omissions. | Measures reconstruction on held-out case families. It does not qualify RCA, diagnosis or actual knowledge of a clinician's mental state. |
| Uncertainty and conformance | Forced sorting versus preservation of intervals/partial order; controlled hidden events, ambiguous labels and widened time intervals with a retained mutation manifest. Measure false deviation alerts, recovery of known changes and stability across admissible histories. | Tests robustness to representation and missingness. A documented event removed from view is not a real omission; controlled log corruption alone is established practice. |
| Downstream error propagation | Give the same frozen assessment component an audited reference trace, a rules-derived trace and an LLM-derived trace. Measure changes in material errors, unsupported attribution and recommendations; attribute changes to trace differences. | Tests whether verified reconstruction improves investigation output and identifies useful automation boundaries. It does not establish that an intervention prevents patient harm. |

Begin with the downstream experiment's trace-fidelity prerequisites. Use independent case-family splits, include failures and abstentions, and cluster intervals by source case. Do not count generated variants as independent patients. Keep synthetic, real-event-log and HDC results separate. Model-judge agreement is not independent clinical validation; retain the reviewer classes and reference uncertainty specified in the evaluation design.

## Existing engines and dependency ownership

| Candidate | Verified capability and licence | Planned use and constraint |
| --- | --- | --- |
| [Rust4PM / `process_mining`](https://github.com/aarkue/rust4pm) | Dual MIT/Apache-2.0. Official [v0.6.2 documentation](https://rust4pm.aarkue.eu/docs/rust/) covers XES/OCEL 2.0, discovery and conformance; [alignments](https://rust4pm.aarkue.eu/docs/how-to/check-conformance/) and [Python/Polars entry points](https://rust4pm.aarkue.eu/) are documented. | Preferred candidate through a thin, pinned adapter when acceptance fixtures pass. Upstream warns of API changes. General uncertain-input conformance was not verified in the reviewed API; ordinary alignment support is not that capability. |
| [PM4Py](https://github.com/process-intelligence-solutions/pm4py/blob/release/README.md) | AGPL-3.0 in the README; [PyPI metadata](https://pypi.org/project/pm4py/2.7.23.12/) specifies AGPL-3.0-or-later. Separate commercial closed-source licensing is offered. | Optional comparator or missing-algorithm adapter after compatibility and licence checks. Rust4PM documents [interoperability](https://rust4pm.aarkue.eu/docs/how-to/use-with-pm4py/). A subprocess does not create a licence exemption. |
| [PROVED](https://github.com/proved-py/proved-core) | Author-owned GPL-3.0 implementation of uncertainty graphs and conformance bounds. The [PyPI release observed](https://pypi.org/project/proved/) dates to January 2021; documentation is sparse. | Pinned research replication candidate after inspecting the paper's experiment branch and dependencies. Do not assume current production maintenance or copy its algorithms into the portable core. |

Portfolio inventory identifies [edithatogo/rust4pm](https://github.com/edithatogo/rust4pm) and [edithatogo/propel](https://github.com/edithatogo/propel) as forks. Check their exact upstream relationship, divergence and release state before reuse. Prefer maintained upstream packages; Propel is a candidate inspection interface, not evidence that the new clinical trace contract is supported. Do not revive archived careops-process as a duplicate engine or assume process-mappings is canonical; its boundary is recorded in [verification and reuse](./verification-and-reuse.md).

Use maintained assertion/section components rather than a new generic clinical NLP engine: [medspaCy](https://github.com/medspacy/medspacy) includes ConText. Preserve canonical evidence before any normalisation and retain offset maps. Reuse schema validators and graph primitives for structural checks; domain-specific availability rules remain small, explicit and tested. Generic algorithm gaps should have an upstream path; local shims need a removal condition.

## Event-log datasets and citations

| Dataset | Verified content and suitable use | Evidence ceiling |
| --- | --- | --- |
| **Mannhardt, F. (2016). Sepsis Cases — event log. 4TU.Centre for Research Data. [DOI 10.4121/uuid:915d2bfb-7e84-49ad-a286-dc35f063a460](https://doi.org/10.4121/uuid:915d2bfb-7e84-49ad-a286-dc35f063a460).** | The [creator's university record](https://research.tue.nl/en/datasets/sepsis-cases-event-log/) describes approximately 1,000 hospital ERP traces, 15,000 events, 16 activities and 39 attributes. Useful for trace/replay and controlled missingness experiments. | No gold RCA, cognition or information-receipt labels. Absolute timestamps were randomised; within-trace elapsed times were preserved. Do not infer original calendar context or cross-patient concurrency. |
| **Mannhardt, F. (2017). Hospital Billing — Event Log. 4TU.Centre for Research Data. [DOI 10.4121/uuid:76c46b83-c930-4798-a1c9-4be94dfeb741](https://doi.org/10.4121/uuid:76c46b83-c930-4798-a1c9-4be94dfeb741).** | The [creator's university record](https://research.tue.nl/en/datasets/hospital-billing-event-log/) describes 100,000 sampled billing traces. Useful for scale, conversion, conformance and known corruption tests. | It explicitly lacks information on actual medical services. This is an administrative engineering control. Dates were randomised while within-trace elapsed times were retained. |

These are established process-mining datasets, not previously unused clinical RCA benchmarks. Creator metadata and DOIs were verified; the original 4TU rights pages were unavailable during this review. Exact snapshot redistribution and training terms remain unresolved. Do not infer CC-BY from a mirror, upload original bytes to Hugging Face, or broaden HDC ethics to these datasets. Prepare citation/loader manifests; use admitted local copies only after their actual terms are recorded. Synthetic fixtures with known origins can proceed independently.

## Implementation acceptance

- Freeze the event/availability contract and a small source-linked fixture set before evaluating engines; do not build a second ingestion or provenance subsystem.
- Prove export round-trips on supported fields and explicitly report interval/relationship losses. An unsupported export fails visibly and retains the canonical trace.
- Compare upstream engine outputs on known fixtures before replacing custom code. Record exact dependencies and compatibility results; no new runtime support claim comes from this plan.
- Demonstrate that a missing source event, uncertain ordering, contradictory receipt evidence and a genuine documented non-occurrence produce distinct outputs.
- Test downstream sensitivity before expanding to whole-RCA interpretation. Disable a component that increases material errors; retain deterministic trace inspection and the negative finding.
