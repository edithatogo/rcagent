# Implementation Plan: Multimodal Capability Fabric

**GitHub:** [#11](https://github.com/edithatogo/rcagent/issues/11)

Execution follows [workflow.md](../../workflow.md) and the
[continuous autonomy contract](../../autonomy.md).

## Continuous Execution Contract

- Continue automatically through tasks, phase checkpoints, fresh-context
  review, bounded rework, documentation synchronization, and the next ready
  track.
- Do not ask for routine approval at task, phase, review, or track boundaries.
- If a decision gate is reached, pause only the affected scope, release its
  lane, continue safe independent work, and present options with a
  recommendation, rationale, evidence, trade-offs, reversibility, safe
  default, and dependency impact.
- Use bounded retry, autonomous plan repair, durable resume state, stale-lock
  recovery, and safety circuit breakers from `autonomy.md`.

## Phase 0: Existing-System Fit and Gap Closure

- [x] Task: Establish the system and dependency context — `2c87747`
  - [x] Read `integration-strategy.md` and this track's entry in `integration-map.json`
  - [x] Identify the current organisational system, standard, framework, runtime, or platform that already owns each capability
  - [x] Record exact versions, extension points, licences, maintenance, privacy, telemetry, offline, device, and security constraints
  - [x] Test existing configuration, profiles, APIs, exports, imports, plugins, and adapters against representative fixtures

- [x] Task: Select the smallest adequate intervention — `2c87747`
  - [x] Prefer existing-system configuration or a standards profile
  - [x] Prefer a thin replaceable adapter when translation is the remaining gap
  - [x] Identify generic gaps suitable for an authorised upstream issue or contribution
  - [x] Limit project code to the smallest safety-, privacy-, jurisdiction-, or domain-specific extension
  - [x] Require a fit-gap record and approved ADR before any new subsystem or permanent fork

- [x] Task: Define the dependency lifecycle — `2c87747`
  - [x] Assign each dependency to a locked core, optional adapter, enterprise connector, evaluation, or experimental profile
  - [x] Define contract tests, compatibility windows, drift checks, failure isolation, and safe fallback
  - [x] Give every local shim an upstream reference, owner, expiry or removal condition, and replacement path
  - [x] Update `integration-map.json` with the selected status and evidence links

- [x] Task: Phase Verification & Checkpoint — `2c87747`
  - [x] Verify that no planned work duplicates an adequate existing capability
  - [x] Verify the system-of-record and data-authority boundary
  - [x] Verify the smallest remaining gap and ownership rationale
  - [x] Record the fit-gap receipt and bounded handoff context
  - [x] Continue automatically through the next ready phase, review, bounded rework, documentation synchronization, and next ready track
  - [x] If an owner gate is reached, create a complete decision packet, pause only the affected scope, release the lane, and continue independent work

## Phase 1: Define capability and disclosure contracts

- [x] Task: Implement the phase scope — `2c87747`
  - [x] Register OCR, encoder, speech, imaging, and ECG capabilities as independent optional profiles
  - [x] Define script and agent-assisted installation, discovery, health-check, rollback, and uninstall contracts for each profile
  - [x] Ensure missing optional profiles degrade to explicit unsupported states rather than weakening the core workflow
  - [x] Define revision, licence, task, modality, intended use, exclusion, knowledge, context, and input-envelope fields
  - [x] Define upstream and local evaluation, device, runtime, quantisation, RAM, latency, and failure fields
  - [x] Define privacy, telemetry, cache, remote-code, governance, and regulatory fields
  - [x] Require an ExecutionDisclosure before every non-deterministic or external capability run
  - [x] Map every capability to an existing document, encoder, speech, DICOM, imaging, or signal framework and prohibit a new engine or storage format
  - [x] Define adapter contribution points so generic framework gaps can be fixed upstream

- [x] Task: Validate the phase deliverables — `2c87747`
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #11 and dependency evidence

- [x] Task: Phase Verification & Checkpoint — `2c87747`
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 2: Evaluate document and OCR adapters

- [!] Task: Implement the phase scope
  - [ ] Prototype Docling-compatible layout, OCR, table, reading-order, and coordinate extraction
  - [ ] Test born-digital, scanned, rotated, low-quality, multilingual, handwritten, and hostile documents
  - [ ] Preserve page, region, confidence, transformation, and source provenance
  - [ ] Compare CPU and accelerated local backends without making Docling a core dependency

- [!] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #11 and dependency evidence

- [!] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 3: Evaluate encoder and reranker adapters

- [!] Task: Implement the phase scope
  - [ ] Prototype Transformers, ONNX Runtime, and OpenVINO encoder contracts
  - [ ] Evaluate dense embeddings, cross-encoders, classification, similarity, and extraction tasks
  - [ ] Measure truncation, input length, language, domain, calibration, drift, and quantisation effects
  - [ ] Prevent untrusted remote code and undeclared telemetry

- [!] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #11 and dependency evidence

- [!] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 4: Evaluate speech and diarisation adapters

- [!] Task: Implement the phase scope
  - [ ] Prototype whisper.cpp and faster-whisper compatible transcription interfaces
  - [ ] Prototype optional pyannote or NeMo diarisation behind separate licence and compute checks
  - [ ] Measure accents, terminology, overlap, noise, timestamps, speaker uncertainty, and hallucination
  - [ ] Keep audio, intermediate features, and transcripts within the selected privacy mode

- [!] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #11 and dependency evidence

- [!] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 5: Prototype medical image and DICOM ingestion

- [!] Task: Implement the phase scope
  - [ ] Use pydicom and Orthanc-compatible contracts for safe metadata and pixel ingestion
  - [ ] Evaluate MONAI-compatible preprocessing and research inference adapters
  - [ ] Test de-identification, burned-in identifiers, series integrity, provenance, and adversarial files
  - [ ] Disable clinical interpretation by default and expose the research-only status

- [!] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #11 and dependency evidence

- [!] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 6: Prototype ECG and time-series ingestion

- [!] Task: Implement the phase scope
  - [ ] Use WFDB-compatible records, leads, sampling, annotations, and provenance
  - [ ] Separate deterministic signal processing from model inference
  - [ ] Measure missing leads, noise, duration, resampling, device variation, and context limits
  - [ ] Disable diagnostic interpretation unless a separate governed pathway exists

- [!] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #11 and dependency evidence

- [!] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 7: Benchmark and certify adapter claims

- [!] Task: Implement the phase scope
  - [ ] Run contract, fixture, privacy, safety, quality, latency, memory, and failure tests
  - [ ] Compare framework versions through thin adapters and defined compatibility windows
  - [ ] Publish evidence-backed support matrices and explicit unsupported combinations
  - [ ] Create upstream-drift, rollback, and capability-disable procedures

- [!] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #11 and dependency evidence

- [!] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Final Track Verification

- [!] Task: Complete the track evidence pack
  - [ ] Verify every acceptance criterion has direct evidence
  - [ ] Re-run the complete applicable validation and regression suite
  - [ ] Reconcile local files, Git history, GitHub hierarchy, native dependencies, and receipts
  - [ ] Record unresolved limitations and owner decisions without downgrading them
  - [ ] Close the GitHub issue only after the completion receipt passes

## Review Fixes

- [x] Task: Add fail-closed capability validation and disclosure probes — `2c87747`
  - [x] Reject duplicate and unknown profile identifiers
  - [x] Keep network, telemetry, remote code and clinical interpretation disabled
  - [x] Emit hashed synthetic disclosures with coordinate or timestamp provenance

- [x] Task: Complete required profile and lifecycle fields — `a4c3322`
  - [x] Record task, intended use, exclusions, knowledge and context limits
  - [x] Record evaluation, runtime, quantisation, RAM, latency and regulatory states
  - [x] Register the independent encoder profile without claiming installation
