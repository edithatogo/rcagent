# Implementation Plan: Multimodal Capability Fabric

**GitHub:** [#11](https://github.com/edithatogo/rcagent/issues/11)

Execution follows [workflow.md](../../workflow.md). Phases continue automatically when objective verification passes and no owner decision gate is reached.

## Phase 1: Define capability and disclosure contracts

- [ ] Task: Implement the phase scope
  - [ ] Define revision, licence, task, modality, intended use, exclusion, knowledge, context, and input-envelope fields
  - [ ] Define upstream and local evaluation, device, runtime, quantisation, RAM, latency, and failure fields
  - [ ] Define privacy, telemetry, cache, remote-code, governance, and regulatory fields
  - [ ] Require an ExecutionDisclosure before every non-deterministic or external capability run

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #11 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 2: Evaluate document and OCR adapters

- [ ] Task: Implement the phase scope
  - [ ] Prototype Docling-compatible layout, OCR, table, reading-order, and coordinate extraction
  - [ ] Test born-digital, scanned, rotated, low-quality, multilingual, handwritten, and hostile documents
  - [ ] Preserve page, region, confidence, transformation, and source provenance
  - [ ] Compare CPU and accelerated local backends without making Docling a core dependency

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #11 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 3: Evaluate encoder and reranker adapters

- [ ] Task: Implement the phase scope
  - [ ] Prototype Transformers, ONNX Runtime, and OpenVINO encoder contracts
  - [ ] Evaluate dense embeddings, cross-encoders, classification, similarity, and extraction tasks
  - [ ] Measure truncation, input length, language, domain, calibration, drift, and quantisation effects
  - [ ] Prevent untrusted remote code and undeclared telemetry

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #11 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 4: Evaluate speech and diarisation adapters

- [ ] Task: Implement the phase scope
  - [ ] Prototype whisper.cpp and faster-whisper compatible transcription interfaces
  - [ ] Prototype optional pyannote or NeMo diarisation behind separate licence and compute checks
  - [ ] Measure accents, terminology, overlap, noise, timestamps, speaker uncertainty, and hallucination
  - [ ] Keep audio, intermediate features, and transcripts within the selected privacy mode

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #11 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 5: Prototype medical image and DICOM ingestion

- [ ] Task: Implement the phase scope
  - [ ] Use pydicom and Orthanc-compatible contracts for safe metadata and pixel ingestion
  - [ ] Evaluate MONAI-compatible preprocessing and research inference adapters
  - [ ] Test de-identification, burned-in identifiers, series integrity, provenance, and adversarial files
  - [ ] Disable clinical interpretation by default and expose the research-only status

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #11 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 6: Prototype ECG and time-series ingestion

- [ ] Task: Implement the phase scope
  - [ ] Use WFDB-compatible records, leads, sampling, annotations, and provenance
  - [ ] Separate deterministic signal processing from model inference
  - [ ] Measure missing leads, noise, duration, resampling, device variation, and context limits
  - [ ] Disable diagnostic interpretation unless a separate governed pathway exists

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #11 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 7: Benchmark and certify adapter claims

- [ ] Task: Implement the phase scope
  - [ ] Run contract, fixture, privacy, safety, quality, latency, memory, and failure tests
  - [ ] Compare framework versions through thin adapters and defined compatibility windows
  - [ ] Publish evidence-backed support matrices and explicit unsupported combinations
  - [ ] Create upstream-drift, rollback, and capability-disable procedures

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #11 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Final Track Verification

- [ ] Task: Complete the track evidence pack
  - [ ] Verify every acceptance criterion has direct evidence
  - [ ] Re-run the complete applicable validation and regression suite
  - [ ] Reconcile local files, Git history, GitHub hierarchy, native dependencies, and receipts
  - [ ] Record unresolved limitations and owner decisions without downgrading them
  - [ ] Close the GitHub issue only after the completion receipt passes
