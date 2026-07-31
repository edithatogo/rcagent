# Integration-First and Dependency Strategy

## Policy

The Safety Systems Workbench must integrate, configure, profile, extend, or
contribute to an existing system before it builds a parallel capability.

A new project-owned capability is justified only when a recorded fit-gap
assessment shows that existing organisational systems, open standards,
maintained dependencies, adapters, and upstream contribution cannot meet a
material requirement within the privacy, safety, interoperability, device,
licence, maintenance, and offline constraints.

This policy applies to every Conductor track and every supported execution
mode.

Delivery also follows [autonomy.md](./autonomy.md). When a dependency or
organisational system has a gap, the agent continues through assessment,
configuration, adapter spikes, validation, and other safe ready work without
routine approval. It asks only when the next action reaches an owner decision
gate, and then presents options, a recommendation, rationale, evidence,
trade-offs, reversibility, and a safe default.

## Capability Acquisition Ladder

Use the first adequate step:

1. **Use the existing organisational system.** Keep the approved system of
   record, identity provider, content store, workflow, reporting surface, or
   clinical platform authoritative.
2. **Configure or profile it.** Use existing fields, workflows, rules,
   templates, exports, APIs, permissions, and local configuration.
3. **Map an open standard.** Prefer an established interchange, workflow,
   provenance, clinical, imaging, signal, packaging, or assurance standard.
4. **Adopt a maintained dependency.** Use a current upstream library,
   framework, runtime, engine, or service behind a project contract.
5. **Add a thin adapter.** Translate between the project contract and the
   existing system without reproducing its internals.
6. **Contribute the generic gap upstream.** Open an upstream issue or propose a
   bounded patch when the missing capability benefits the dependency's wider
   users.
7. **Implement a small project extension.** Own only the domain-specific,
   privacy-specific, or jurisdiction-specific gap that upstream should not
   own.
8. **Build a new subsystem only by exception.** Require an Architecture
   Decision Record, owner approval where material, an exit strategy, and
   evidence that steps 1-7 are inadequate.

Convenience, novelty, or dissatisfaction with an interface is not sufficient
evidence for a new subsystem.

## Authoritative Candidate Sources

These are discovery and compatibility anchors, not permanent endorsements.
Each track must resolve the current version, status, licence, guidance, and
organisational availability during its fit-gap assessment.

| Area | Primary source |
|---|---|
| NSW Health incident management and ims+ | [Clinical Excellence Commission incident management](https://cec.health.nsw.gov.au/Review-incidents/incident-management) |
| NSW Health incident policy | [PD2020_047 Incident Management](https://www1.health.nsw.gov.au/pds/ActivePDSDocuments/PD2020_047.pdf) |
| Adaptive case work | [OMG Case Management Model and Notation](https://www.omg.org/cmmn/) |
| Workflow and decision standards | [OMG specification catalogue](https://www.omg.org/spec) |
| Standards-based workflow engine candidate | [Flowable Open Source](https://www.flowable.com/open-source) |
| Healthcare adverse-event exchange | [HL7 FHIR R5 AdverseEvent](https://hl7.org/fhir/R5/adverseevent.html) |
| Healthcare provenance exchange | [HL7 FHIR R5 Provenance](https://hl7.org/fhir/R5/provenance.html) |
| Healthcare work-item exchange | [HL7 FHIR R5 Task](https://hl7.org/fhir/R5/task.html) |
| Generic provenance | [W3C PROV-O](https://www.w3.org/TR/prov-o/) |
| Primary evaluation orchestrator candidate | [Inspect AI](https://inspect.aisi.org.uk/) |
| Standard language-model evaluation adapter | [EleutherAI LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness) |
| Local experiment tracking candidate | [MLflow Tracking](https://mlflow.org/docs/latest/tracking/) |
| Retrieval diagnostics candidate | [Ragas](https://docs.ragas.io/en/stable/) |
| Parameter-efficient adaptation | [Hugging Face PEFT](https://huggingface.co/docs/peft/index) |
| Training workflow candidate | [LlamaFactory](https://github.com/hiyouga/LlamaFactory) |

## System Roles and Boundaries

### Incident and Safety System of Record

For NSW Health work, ims+ or another approved incident management system such
as a locally authorised alternative remains the source of record for incident
notification and required incident-management data.

The workbench may:

- ingest approved bounded exports or user-supplied artefacts;
- map fields to canonical and open-standard representations;
- support local evidence review and systems analysis;
- prepare rights-cleared content for authorised re-entry or import;
- reconcile identifiers, versions, status, and provenance; and
- report gaps that require an approved system change.

The workbench must not create a shadow incident registry or imply that a local
case is lodged, updated, approved, or closed in the system of record unless
that external action is verified.

### Evidence and Enterprise Content

Approved enterprise content, records, imaging, and collaboration systems
remain authoritative where they are in use. Examples may include governed
SharePoint or Microsoft 365 locations, approved network stores, electronic
medical record systems, PACS/DICOM systems, and records platforms.

The repository stores only public, synthetic, de-identified, or explicitly
authorised artefacts. A local private workspace references or processes
authorised evidence under its selected mode; it does not become an
uncontrolled enterprise records repository.

### Identity, Access, and Collaboration

Use the organisation's approved identity, access, device, collaboration, and
audit controls when deployed in an enterprise environment. Do not build
custom authentication, staff directories, messaging, or approval systems when
approved platform capabilities can be adapted.

### Workflow and Case Management

- Use Case Management Model and Notation (CMMN) to assess adaptive,
  evidence-led investigation work.
- Use Business Process Model and Notation (BPMN) for predictable policy and
  integration processes.
- Use Decision Model and Notation (DMN) for transparent, versioned decision
  tables where rules are appropriate.
- Assess an existing organisational workflow platform first.
- Assess a maintained standards-based engine, such as Flowable, only when an
  executable local or portable engine is required.

The canonical project state model is an interoperability and validation
contract. It must not quietly grow into a competing workflow platform.

### Clinical and Healthcare Interoperability

Assess HL7 FHIR mappings where a clinical system exposes or consumes them:

- `AdverseEvent` for actual and potential patient adverse events;
- `Provenance` and `AuditEvent` for exchange and audit context;
- `Task` for bounded work items;
- `DocumentReference` for governed evidence references;
- `Questionnaire` and `QuestionnaireResponse` for structured forms; and
- other resources only when their defined boundaries fit the use case.

FHIR is an interchange option, not the internal investigation ontology and
not evidence that a source system supports an integration. R5 resources with
low maturity or trial-use status require explicit compatibility and version
profiles.

### Provenance and Research Packaging

Assess W3C PROV for interoperable entity, activity, agent, derivation, and
attribution concepts. Assess RO-Crate, BagIt, or another maintained packaging
standard for portable evidence or benchmark bundles where its licence,
security, and metadata model fit.

The project owns healthcare investigation semantics and safety-specific
constraints; it should not invent a generic provenance vocabulary or archival
container.

### Evaluation and Experiment Tracking

Use one primary evaluation orchestrator and bridge specialised tools:

- Assess Inspect AI as the primary model, agent, tool, multimodal, sandbox,
  scorer, and evaluation-log framework.
- Use EleutherAI's Language Model Evaluation Harness through an adapter for
  applicable standard language-model benchmarks.
- Use MLflow in a local-only configuration when experiment tracking,
  artefact lineage, comparison, and review fit the privacy mode.
- Assess Ragas or established information-retrieval measures for retrieval
  diagnostics, while retaining domain-specific evidence and safety gates.
- Use pytest and focused testing libraries for deterministic contracts and
  fixtures.

The project owns its clinical-safety cases, rubrics, hard gates, and adapters.
It must not recreate a generic evaluation runner, model-provider abstraction,
trace store, or results viewer unless the fit-gap record proves it necessary.

### Models, Multimodal Processing, and Training

Use maintained runtimes and frameworks:

- llama.cpp, Ollama or another evaluated local facade, ONNX Runtime,
  OpenVINO, MLX/MLX-LM, Transformers, Optimum, and vLLM where the device and
  mode support them;
- Docling and existing OCR backends for documents;
- whisper.cpp or faster-whisper, with optional maintained diarisation
  frameworks, for speech;
- pydicom, Orthanc, and MONAI for DICOM and research imaging workflows;
- WFDB for ECG and time-series interchange;
- Transformers, PEFT, TRL, LlamaFactory, Axolotl, MLX-LM, or another current
  maintained training framework for any approved adaptation.

The project owns capability profiles, safety gates, benchmark cases, routing,
and domain adapters. It must not implement a new inference engine, tensor
library, OCR engine, DICOM store, signal format, or fine-tuning framework.

### Retrieval and Knowledge

Use SQLite FTS or an equivalent existing lexical engine for the baseline.
Assess maintained orchestration and indexing frameworks such as Haystack,
LlamaIndex, Qdrant, LanceDB, or FAISS through replaceable adapters.

The project owns source authority, rights, jurisdiction, compartment,
freshness, citation, abstention, and policy-drift semantics. It must not build
a vector database or general-purpose retrieval framework.

### Interfaces and Reporting

Prefer existing enterprise surfaces and maintained document/reporting tools:

- approved Microsoft 365, SharePoint, Teams, Power Automate, Dataverse, or
  comparable organisational capabilities where available;
- ims+ or approved incident-system workflows for authoritative incident data;
- existing workflow or case-management engines;
- maintained CLI, API, local-application, Markdown, Mermaid, Pandoc, Quarto,
  office-document, and PDF tooling.

A project UI is justified only for privacy-preserving analysis, evidence
review, capability disclosure, or workflow gaps that existing surfaces cannot
safely meet. It must exchange bounded artefacts with systems of record rather
than duplicate them.

## Dependency Classes

Every dependency or external system is assigned one class:

| Class | Meaning |
|---|---|
| Standard | Interchange or conformance target; no runtime dependency |
| Core | Small, essential, portable, and required in every supported profile |
| Optional adapter | Installed only for a capability or integration profile |
| Enterprise connector | Available only in an approved organisational environment |
| Evaluation/development | Required for authoring, testing, benchmarking, or assurance |
| Experimental | Disabled by default; no support claim without evidence |

Keep the portable skill core free of enterprise, model, imaging, workflow
engine, vector database, and client-specific dependencies.

Use locked optional dependency groups or profiles so a local CPU installation
does not inherit GPU, cloud, DICOM, training, or enterprise packages it does
not need.

## Fit-Gap Record

Before implementation, record:

1. required capability and user outcome;
2. current organisational system and source-of-record role;
3. applicable standards;
4. candidate dependencies and upstream health;
5. existing configuration, extension, API, export, import, or plugin options;
6. privacy mode, data flows, telemetry, credentials, and offline behaviour;
7. licence, terms, maintenance, security, device, and accessibility fit;
8. measured fit against acceptance fixtures;
9. the smallest remaining gap;
10. whether the gap belongs in configuration, mapping, an adapter, upstream,
    or the project;
11. replacement, upgrade, disable, rollback, and data-exit paths; and
12. the decision and evidence.

Record this in the track evidence and update
[`integration-map.json`](./integration-map.json).

## Upstream Gap Protocol

When a maintained dependency has a generic gap:

1. reproduce it with a minimal non-sensitive fixture;
2. verify that it is not configuration or version misuse;
3. search current upstream issues and release notes;
4. open or link an upstream issue when external communication is authorised;
5. propose an upstream patch when it is bounded and maintainable;
6. keep any local shim small, isolated, tested, and time-limited;
7. record the upstream reference and removal condition; and
8. reassess the shim on every supported upstream release.

Do not create a permanent fork merely to avoid coordination.

## Dependency Admission Gate

A dependency cannot become supported until evidence covers:

- project fit and the alternative systems considered;
- active maintenance, release cadence, API stability, and bus factor;
- licence, redistribution, model/data terms, and transitive obligations;
- vulnerabilities, supply-chain posture, provenance, signatures, and SBOM;
- privacy, telemetry, network, cache, log, credential, and remote-code
  behaviour;
- Windows CPU/iGPU, macOS/MLX, GPU, local, and air-gapped compatibility as
  applicable;
- performance, resource use, failure behaviour, and accessibility;
- version pin, compatibility window, upgrade and drift tests;
- rollback, replacement, export, and removal; and
- the smallest project-owned gap.

Popularity or benchmark leadership alone is insufficient.

## Autonomous Decision Rule

An agent may autonomously choose configuration, standards mapping, a reversible
adapter spike, or a non-production development dependency when the track
scope and admission gate permit it.

Owner approval is required for a new enterprise connection, credential,
external message or upstream contribution, public dependency commitment,
licence exception, paid service, production workflow change, system-of-record
write, or a new project-owned subsystem.
