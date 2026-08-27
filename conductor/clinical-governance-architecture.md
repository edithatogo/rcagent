# Clinical Governance System-of-Systems Architecture

This map extends the Safety Systems Workbench from an investigation toolkit
into a composable clinical-governance and quality-and-safety workbench. It
does not replace the incident, clinical, records, identity, workforce,
enterprise-risk, quality-measure, or document systems that remain
authoritative.

The machine-readable source of truth is
[`clinical-governance-architecture.json`](./clinical-governance-architecture.json).

## Architecture layers

### 1. Governed incident lifecycle

The lifecycle is a stateful case-management spine, not one monolithic agent:

1. initial incident submission and immediate safety response;
2. incident huddle, preservation instructions, support, and escalation;
3. provisional risk assessment, checklist completion, and provisional harm
   scoring under the current jurisdiction pack;
4. review-path selection, terms of reference, conflicts, and review-team
   formation;
5. evidence acquisition and review, including records, notes, audit trails,
   operational data, interviews, chronology, patient problem list, and
   incident problem list;
6. systems analysis using the smallest suitable methods, diagrams, strengths,
   weaknesses, controls, barriers, data analysis, and consultations;
7. governed invocation of related pathways such as lookback, cluster review,
   indicator review, open disclosure, cultural review, enterprise or clinical
   risk assessment, and individual-worker review;
8. evidence-tested findings, dissent, uncertainty, and authorised acceptance;
9. recommendations supported where appropriate by searched and verified
   literature;
10. action ownership, implementation evidence, effectiveness, balancing
    measures, residual risk, organisational learning, and closure.

Each transition preserves authority, evidence, decision, timestamp, policy
version, privacy compartment, and human approval. A provisional harm or risk
score is never silently promoted into a final classification.

### 2. Shared evidence and knowledge services

These services are reused across every lifecycle stage and specialist domain:

- case, evidence, claim, provenance, interview, consultation, chronology,
  problem-list, finding, recommendation, action, and effectiveness contracts;
- policy and jurisdiction authority mapping;
- privacy, records, access, cultural-safety, legal, and clinical-safety gates;
- deterministic search, retrieval, data-analysis, document, diagram, and
  multimodal adapters;
- literature discovery, screening, citation verification, claim-to-source
  provenance, and bibliography quality; and
- benchmark, calibration, robustness, and drift evaluation.

Literature discovery remains separable from citation integrity. Search
providers may change, but candidate references and claims pass through a
thin, pinned `edithatogo/sourceright` adapter for CSL validation, citation
reconciliation, DOI/metadata conflict reporting, claim/source provenance,
and review-required diagnostics. SourceRight does not establish study
quality, clinical truth, or recommendation appropriateness.

### 3. Specialist governance domains

Specialist domains share the evidence and workflow core but retain their own
authority, methods, roles, records, safeguards, and evaluation:

- enterprise risk assessment;
- clinical risk management;
- lookback and cohort ascertainment;
- cluster and thematic incident review;
- quality-measure, safety-indicator, operational, and comparative-data
  analysis;
- individual clinician or worker concerns, complaints, conduct, capability,
  health, and employment pathways;
- Just Culture decision support;
- Aboriginal cultural safety and broader cultural assessment;
- quality improvement, implementation, service redesign, and human factors;
- medicolegal, claims, disclosure, coronial, regulatory, and privilege review;
  and
- proactive safety analysis and resilience learning.

The workbench may route and prepare evidence, but does not combine these
pathways into an automated personnel, legal, regulatory, cultural, or clinical
decision.

### 4. Organisational memory and learning

Governed connectors may make prior incidents, serious-adverse-event reviews,
findings, recommendations, actions, effectiveness results, Health Roundtable
or comparable benchmarking, operational data, and quality-and-safety measures
discoverable within their source permissions.

The initial pattern is federated retrieval with source-linked snapshots. A
central copy is justified only by an approved fit-gap record covering legal
authority, purpose, minimisation, lineage, retention, access, deletion,
freshness, re-identification, Indigenous data governance, and system-of-record
reconciliation. Cross-case learning defaults to de-identified or aggregate
views and prevents a retrieval result from becoming a causal finding.

## Integration and separation rule

Begin each capability as a bounded module behind shared contracts. Extract it
into a separate track, skill, agent, workflow, domain pack, or plugin only
when at least one condition is evidenced:

- it has a distinct authority, safety case, privacy compartment, or
  system-of-record boundary;
- it has an independently useful lifecycle or release cadence;
- it needs specialist evaluation, credentials, dependencies, or deployment;
- its context would materially degrade another capability's trigger quality;
  or
- independent maintenance measurably reduces coupling or risk.

Extraction must preserve one canonical schema, provenance chain, terminology
mapping, decision ledger, and orchestration contract. Shared services are not
copied into specialist modules.

## Portfolio ownership

| Architecture area | Initial owning tracks |
|---|---|
| Lifecycle states and evidence semantics | 02 Evidence Workflow Core |
| National baseline plus NSW and Queensland risk, harm, huddle, review, lookback, cluster, workforce and consultation policy mappings | 04 Jurisdiction Packs (national baseline, NSW, QLD) |
| Literature discovery, organisational memory and retrieval | 07 Retrieval and Knowledge System |
| SourceRight citation and provenance adapter | 07 Retrieval, validated by 05 Benchmark |
| Forms, huddles, interviews, methods, consultation and action surfaces | 09 Interfaces, Templates and Closed-Loop Actions |
| Data and model evaluation | 05 Benchmark and Evaluation Harness |
| Specialist-domain routing and privacy compartments | 01 Foundation, 03 Privacy and Security, then the relevant domain track |
| Optional local, multimodal and client capabilities | 06, 08, 10 and 11 |

Track 01 must refine this map into stable contracts and extraction decisions.
Tracks 02, 04, 07, and 09 implement the first lifecycle vertical slice. New
formal tracks are created only after their definition of ready and split
criteria are satisfied.
