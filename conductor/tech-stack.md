# Technical Strategy and Candidate Stack

## Status

This document defines architecture constraints and candidate frameworks, not final selections. A candidate becomes supported only after its exact revision passes the applicable benchmark, privacy, safety, licence, device, compatibility, maintenance, and rollback gates.

The project will reuse maintained upstream frameworks through thin adapters and versioned contracts. It will not maintain a bespoke copy of an entire model, retrieval, document, imaging, or workflow stack.

All choices follow [integration-strategy.md](./integration-strategy.md) and the
machine-readable [integration-map.json](./integration-map.json). The order is:
existing organisational system, configuration or profile, open standard,
maintained dependency, thin adapter, upstream contribution, small
project-specific extension, then a new subsystem only by approved exception.

Dependencies are introduced through locked profiles: standard-only, core,
optional adapter, enterprise connector, evaluation/development, or
experimental. The portable skill core must not inherit enterprise, model,
workflow-engine, vector, imaging, training, or client-specific dependencies.

## Architecture Layers

| Layer | Responsibility | Core rule |
|---|---|---|
| Portable skills | Client-neutral instructions, references, assets, and scripts | Self-contained Agent Skills conformance |
| Safety domain core | Evidence, claims, workflow, actions, effectiveness, audit | Interoperability contract; not a competing source-of-record platform |
| Jurisdiction packs | Policy sources, authority, rules, templates, drift | No jurisdiction assumptions in the generic core |
| Capability fabric | OCR, encoders, speech, images, signals, models | `CapabilityProfile` and `ExecutionDisclosure` |
| Knowledge system | Ingest, full-text search, vectors, hybrid retrieval, citations | Lexical baseline; public/private separation |
| Interfaces | CLI, API, optional local UI, imports, exports | Replaceable; human-review gates remain visible |
| Evaluation and assurance | Fixtures, benchmarks, safety/privacy tests, receipts | Evidence before support claims |
| Client and distribution adapters | Codex, Claude, other clients and marketplaces | Thin adapters outside the portable core |

## Portable Content and Data Contracts

- Markdown and GitHub-flavoured Markdown for human-readable content
- YAML frontmatter only where the relevant standard or client contract permits it
- JSON Schema for canonical records, manifests, capability profiles, execution disclosures, and receipts
- JSON or JSON Lines for event streams and machine-readable evidence
- CSV or Parquet for bounded analytical exports, with data dictionaries and provenance
- Mermaid source for version-controlled diagrams
- UTF-8, stable identifiers, explicit schema versions, and deterministic serialisation where signatures or hashes matter

The Agent Skills official validator and the project conformance profile govern portable skills. Client-specific metadata lives in adapter directories.

## Harness and Automation

Python is the initial portable harness language because the relevant document, model, evaluation, and scientific ecosystems are mature. The project commands compose maintained tools rather than reimplement them. Use a pinned environment and lock file, with small commands for:

- `doctor`: environment, device, dependency, policy, model, and source preflight
- `context`: bounded context-pack assembly with provenance and freshness
- `queue`: next-ready-task selection from dependency and decision state
- `validate`: schemas, links, skills, fixtures, policies, privacy, and adapters
- `eval`: compose Inspect AI as the primary evaluation runner plus specialised adapters where justified
- `receipts`: durable environment, command, revision, result, limitation, and decision evidence
- `reconcile`: Conductor, Git, GitHub, CI, source, benchmark, and release-state comparison

Exact command names and packaging are Track 01 decisions. Scripts must work locally and in CI, return non-zero on applicable failures, and distinguish offline, unavailable-upstream, unsupported, advisory, and failed states.

The harness implements [autonomy.md](./autonomy.md) and
[autonomy.json](./autonomy.json): deterministic next-ready dispatch,
cross-phase and cross-track continuation, idempotent run IDs, leases and stale
lock recovery, bounded retry and autonomous plan repair, circuit breakers,
decision and external-wait queues, resumable context packs, automatic review
and rework, and evidence-based terminal detection.

Upstream Conductor `main` remains the protocol reference. Experimental Ralph,
ASDD, and isolation-worktree branches are assessed as design inputs for
iteration-bounded replanning, persistent state, DAG analysis, locks, resumable
worktrees, and review rework. They remain disabled research adapters until
their exact revisions pass compatibility, Windows, dirty-worktree,
concurrency, state-integrity, security, rollback, and replacement tests.

## Storage and Retrieval

Use an approved content, records, or knowledge system first when it already
meets the requirement. For a local workbench gap, start with the smallest
portable components:

1. canonical files plus SQLite for metadata and audit views;
2. SQLite FTS or an equivalent deterministic lexical baseline;
3. an optional local embedding adapter and replaceable vector index;
4. hybrid fusion; and
5. a local reranker only when benchmark evidence justifies it.

Candidate vector implementations may include Qdrant, LanceDB, FAISS, or another maintained local-capable framework. Candidate orchestration frameworks may include Haystack or LlamaIndex, but orchestration must remain behind project contracts, telemetry must be off or local by default, and the project must retain a simple path that does not depend on them.

Public and private corpora use separate stores, indexes, caches, queues, keys, and receipts. Cross-compartment retrieval fails closed.

## Local Model Runtimes

| Device context | Primary runtime candidates | Notes |
|---|---|---|
| Windows, Intel CPU/iGPU, 32 GB RAM | llama.cpp, ONNX Runtime, OpenVINO; DirectML only if measured | Optimise for quantised small/medium models, predictable memory, and graceful fallback |
| Apple silicon | MLX, llama.cpp, ONNX Runtime where useful | Measure unified-memory pressure and exact MLX model support |
| Larger CPU/GPU workstation | llama.cpp, Transformers, ONNX Runtime, vendor accelerators | Same contracts and benchmarks; no automatic promotion |
| Experimental | Modular MAX or Mojo spikes | Isolated adapter only; never a portable-core dependency until support evidence passes |

Generic model families are evaluated before domain adaptation. Current hypotheses include Gemma 4 12B, Apriel 15B Thinker, Nemotron variants, G9-class small models, Phi-4 reasoning variants, Qwen 27B-class models, DiffusionGemma experiments, and relevant medical models. Names, availability, licences, revisions, formats, and suitability must be verified at evaluation time.

Every model entry records exact repository and revision, licence, architecture, intended and out-of-scope use, knowledge limits, context or input envelope, runtime, quantisation, device, RAM, storage, latency, calibration, benchmark evidence, privacy behaviour, remote-code requirement, failure modes, governance status, and evidence date.

## Multimodal Framework Candidates

### Documents and OCR

- Docling-compatible ingestion for layout, OCR, tables, reading order, and coordinates
- Local OCR backends selected through device and document-quality benchmarks
- Source page, region, confidence, transformation, and checksum provenance

### Encoders and Rerankers

- Hugging Face Transformers for research and reference adapters
- ONNX Runtime and Optimum/OpenVINO for portable or Intel-optimised inference
- Local embedding and cross-encoder models selected by retrieval and device benchmarks

### Speech

- whisper.cpp for portable local transcription
- faster-whisper for supported accelerated environments
- pyannote or NVIDIA NeMo as optional diarisation candidates subject to licence, compute, privacy, and accuracy review

### Images and DICOM

- pydicom for DICOM records and de-identification checks
- Orthanc-compatible local DICOM workflows where a server is justified
- MONAI-compatible research adapters for medical imaging
- Clinical interpretation disabled by default pending separate governance and validation

### ECG and Time Series

- WFDB-compatible records, leads, sampling, annotations, and deterministic signal processing
- Model inference isolated from ingestion and feature extraction
- Diagnostic interpretation disabled by default

## Workflow and Interface Candidates

- Canonical workflow state machines in project schemas
- CMMN 1.1 for adaptive, evidence-led investigation and review cases
- BPMN 2.0 for predictable policy and integration processes
- DMN for transparent, versioned decision tables
- An approved organisational workflow platform before a new runtime
- Flowable or another maintained standards-based engine only when a local executable CMMN/BPMN/DMN runtime is justified
- Common Workflow Language for reproducible data/model pipeline experiments where it adds value
- A small CLI and API before a richer interface
- Approved ims+, Microsoft 365, SharePoint, Teams, Power Automate, Dataverse, or comparable surfaces where they can safely host the workflow
- A maintained local application framework, such as Gradio or another evaluated option, only for a demonstrated privacy or analysis gap
- Office and PDF generation through maintained document tooling, with Markdown and canonical data as sources

Framework adoption requires an adapter, contract tests, a compatibility window, upstream-drift checks, telemetry review, and a removal path.

## Evaluation, Testing, and Assurance

- Inspect AI is the primary candidate for model, agent, tool, multimodal, sandbox, scorer, and evaluation-log orchestration
- EleutherAI's Language Model Evaluation Harness is an adapter for applicable standard language-model benchmarks
- MLflow local tracking is a candidate for experiment and artefact lineage when it meets privacy and maintenance gates
- Ragas or established information-retrieval measures may provide retrieval diagnostics, but cannot replace project evidence and safety gates
- pytest and focused testing libraries remain the deterministic contract and fixture layer
- Official Agent Skills validator plus project stable and experimental conformance rules
- Schema and link validation
- Positive and negative fixtures before implementation
- Unit, property, contract, integration, round-trip, migration, adversarial, privacy, safety, recovery, and device tests
- Retrieval, citation, calibration, robustness, latency, memory, storage, and energy-proxy benchmarks
- Repeated model runs with raw observations and visible nondeterminism
- Synthetic and de-identified data by default
- Durable result manifests and receipts; no pass claim from CI colour alone

The legacy H0-H8 evaluation estate remains historical evidence and will be reconciled into the canonical benchmark harness without rewriting its original results.

## Supply Chain and Model Governance

- Pin exact source, dependency, model, dataset, and validator revisions
- Record the existing system, standard, configuration, adapter, and upstream contribution options considered before admission
- Verify checksums, signatures, attestations, licences, and remote-code requirements
- Prefer reproducible builds and local cached artefacts for governed modes
- Evaluate SPDX 3 AI Profile, OpenSSF model-signing approaches, and MLCommons Croissant where applicable
- Generate software/model/data bills of materials and provenance receipts appropriate to the artefact
- Define update, vulnerability, revocation, rollback, deletion, and air-gapped refresh procedures
- Define a data-exit and dependency-replacement path; no accepted dependency may become an undocumented permanent fork

## Distribution

- Canonical portable skills: versioned GitHub source and release artefacts
- Claude Code: thin plugin and self-hosted marketplace, then an optional official marketplace submission
- Codex/OpenAI: current plugin manifest, `agents/openai.yaml`, optional app or MCP metadata, personal testing, then an optional universal plugin-directory submission
- Other clients: the same adapter contract and compatibility profile

Every public release or registry submission is an owner decision. No credentials, publisher verification, legal policies, production services, or public claims are created merely because packaging tests pass.
