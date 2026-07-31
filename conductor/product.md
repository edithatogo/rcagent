# Product: Safety Systems Workbench

## What This Is

The Safety Systems Workbench is a privacy-first, evidence-grounded repository of portable agent skills, investigation and learning workflows, templates, schemas, evaluation harnesses, knowledge packs, and optional local AI capabilities.

Its initial domain is healthcare incident investigation and serious adverse event review. Its wider purpose is to support the complete safety-learning loop:

1. detect and triage hazards, incidents, near misses, and weak signals;
2. collect, preserve, and assess evidence;
3. analyse interacting system conditions without defaulting to individual blame;
4. communicate with consumers, families, staff, and governance bodies;
5. design and govern recommendations and actions; and
6. verify implementation, effectiveness, unintended consequences, and residual risk.

The canonical core is client-neutral. Codex, Claude Code, and other client integrations are optional adapters outside that core.

## Target Users

- Clinical governance, patient safety, quality, and risk teams
- Clinicians and trained investigators
- Consumers, families, advocates, and liaison staff participating in review
- Managers and executives responsible for actions and assurance
- Human factors, systems safety, data, privacy, security, and policy specialists
- Researchers evaluating safety-analysis methods and assistive AI
- Small teams or individual developers who need a reproducible, auditable toolkit

## Operating Modes

The same workflow contracts support four explicit modes:

| Mode | Data boundary | Typical use |
|---|---|---|
| Public remote | Public or explicitly approved data may use remote services | Policy research, public-case evaluation, non-sensitive authoring |
| Governed hybrid | Private content and private indexes stay local; approved bounded artefacts may use remote services | Local evidence processing with approved remote assistance |
| Fully local | Models, indexes, storage, logs, and interfaces run on the device or local network | Sensitive investigation work |
| Air-gapped | Dependencies, models, sources, time, updates, and receipts operate without network access | High-assurance or isolated environments |

Every run declares its actual mode, capabilities, model and framework revisions, data boundary, limitations, and required human review.

## Core Capabilities

- Portable Agent Skills for triage, investigation, reporting, action tracking, and effectiveness review
- Evidence and claim provenance, conflicting-evidence handling, audit events, and bounded exports
- Retrospective and proactive systems methods, including RCA, SEIPS, AcciMap, FRAM, STPA, bow-tie, barrier analysis, FMEA, and Safety-II approaches where appropriate
- Versioned jurisdiction packs, beginning with NSW Health and Clinical Excellence Commission sources
- Workflows and original or rights-cleared templates for serious adverse events, open disclosure, consumer and family participation, staff support, cultural safety, and governance review
- Citation-first retrieval that starts with full-text search and adds local embeddings, hybrid search, or reranking only when evaluation supports them
- Replaceable multimodal adapters for document layout and OCR, encoders, speech transcription and diarisation, images and DICOM, and ECG or time-series inputs
- Device-aware local model and runtime profiles for CPU/iGPU Windows systems, Apple silicon/MLX, and larger hosts
- Benchmark, privacy, safety, calibration, robustness, resource, and upstream-drift harnesses
- Client adapters and governed distribution packages for GitHub, Claude, OpenAI/Codex, and other ecosystems

## Product Principles

1. **Evidence before inference.** Preserve sources, provenance, conflicts, uncertainty, and reviewer decisions.
2. **Systems before blame.** Examine work, context, design, resources, interactions, and governance before individual accountability.
3. **Privacy by mode.** Data never crosses a compartment merely because a model or tool is convenient.
4. **Human authority.** The workbench assists; accountable humans make clinical, legal, policy, employment, disclosure, and release decisions.
5. **Benchmark before selection.** Models, runtimes, retrieval methods, and frameworks earn support through measured evidence.
6. **Simple before complex.** Deterministic tools and lexical retrieval remain valid baselines; fine-tuning is a late option, not a default.
7. **Portable core, thin adapters.** Reuse maintained frameworks and client capabilities without forking the whole stack.
8. **Living conformance.** Standards, policy, model, framework, and marketplace claims carry exact versions and drift checks.
9. **Closed-loop learning.** Completion of a report or action does not prove safety improvement.
10. **Honest boundaries.** Research, experimental, operational, and unsupported capabilities are visibly distinct.

## Initial Jurisdiction Strategy

The generic core contains no silent jurisdictional assumptions. A versioned NSW Health pack will map current authoritative sources from NSW Health, the Clinical Excellence Commission, the Agency for Clinical Innovation, relevant legislation, and national standards. Source authority, status, supersession, rights, retrieval date, and unresolved interpretation will remain visible.

Additional jurisdictions can implement the same contracts without copying NSW-specific rules into the core.

## What This Is Not

- An autonomous investigator, clinician, legal adviser, regulator, or decision-maker
- A replacement for incident management, records, imaging, or clinical systems
- Proof that a document is legally privileged or protected
- A licence to place identifiable information in a remote model or service
- A claim that medical-image, ECG, or domain-model output is clinically validated
- A guarantee that a named model or framework is suitable until its exact revision is measured

## Success Measures

- A fresh-context maintainer can reproduce every material claim from durable evidence.
- Private data remains inside its declared compartment under adversarial testing.
- Investigations distinguish evidence, accounts, analysis, findings, decisions, and uncertainty.
- Recommendations become owned actions with measurable effectiveness and residual-risk review.
- Supported device profiles meet declared quality, safety, privacy, latency, memory, and maintenance gates.
- Portable skills and client adapters pass current conformance and compatibility tests.
- Public releases and registry submissions occur only after an explicit owner decision.
