# Implementation Plan: Retrieval and Knowledge System

**GitHub:** [#12](https://github.com/edithatogo/rcagent/issues/12)

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

- [x] Task: Establish the system and dependency context
  - [x] Read `integration-strategy.md` and this track's entry in `integration-map.json`
  - [x] Identify the current organisational system, standard, framework, runtime, or platform that already owns each capability
  - [x] Record exact versions, extension points, licences, maintenance, privacy, telemetry, offline, device, and security constraints
  - [x] Test existing configuration, profiles, APIs, exports, imports, plugins, and adapters against representative fixtures

- [x] Task: Select the smallest adequate intervention
  - [x] Prefer existing-system configuration or a standards profile
  - [x] Prefer a thin replaceable adapter when translation is the remaining gap
  - [x] Identify generic gaps suitable for an authorised upstream issue or contribution
  - [x] Limit project code to the smallest safety-, privacy-, jurisdiction-, or domain-specific extension
  - [x] Require a fit-gap record and approved ADR before any new subsystem or permanent fork

- [x] Task: Define the dependency lifecycle
  - [x] Assign each dependency to a locked core, optional adapter, enterprise connector, evaluation, or experimental profile
  - [x] Define contract tests, compatibility windows, drift checks, failure isolation, and safe fallback
  - [x] Give every local shim an upstream reference, owner, expiry or removal condition, and replacement path
  - [x] Update `integration-map.json` with the selected status and evidence links

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify that no planned work duplicates an adequate existing capability
  - [x] Verify the system-of-record and data-authority boundary
  - [x] Verify the smallest remaining gap and ownership rationale
  - [x] Record the fit-gap receipt and bounded handoff context
  - [x] Continue automatically through the next ready phase, review, bounded rework, documentation synchronization, and next ready track
  - [x] If an owner gate is reached, create a complete decision packet, pause only the affected scope, release the lane, and continue independent work

## Phase 1: Define source and corpus contracts

- [x] Task: Implement the phase scope
  - [x] Define ingestion manifests for authority, jurisdiction, rights, version, freshness, checksum, and compartment
  - [x] Define chunk, page, section, table, transcript, image-region, and signal-window provenance
  - [x] Define public, governed private, ephemeral, and excluded corpus states
  - [x] Create deletion, supersession, correction, and re-index requirements
  - [x] Define federated source contracts for incident history, prior reviews, findings, recommendations, effectiveness, comparative benchmarking, operational data, and quality-and-safety measures
  - [x] Define literature query, screening, study-quality, citation, claim-link, and recommendation-rationale records
  - [x] Specify a thin pinned SourceRight adapter for CSL validation, citation reconciliation, metadata conflicts, and claim/source provenance without reimplementing those functions

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #12 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 2: Implement the lexical baseline

- [x] Task: Implement the phase scope
  - [x] Package lexical retrieval as an optional local profile with a deterministic scripted installer and health check
  - [x] Implement SQLite FTS or an equivalently portable full-text baseline behind a retrieval port
  - [x] Support field, authority, jurisdiction, date, source, and status filters
  - [x] Return stable citations, locations, scores, and query receipts
  - [x] Benchmark exact, phrase, acronym, typo, and policy-version queries
  - [x] Assess existing enterprise search and content APIs before creating a parallel local corpus
  - [x] Define a replaceable literature-search provider port and fail-closed receipt contract; no provider execution was admitted
  - [x] Reuse the selected retrieval framework's indexing, query, filtering, and persistence capabilities rather than creating a general-purpose engine

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #12 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 3: Evaluate optional local vector admission

- [x] Task: Close the phase at the per-artefact admission gate with explicit negative results
  - [x] Define separately selectable disabled profiles for embeddings, vector storage, and reranking rather than core dependencies
  - [x] Record that no measured profile qualified for recommendation or installation
  - [x] Record that no encoder candidate passed the CapabilityProfile and benchmark admission prerequisites
  - [x] Preserve required version, chunking, normalisation, quantisation, index, and device fields as unresolved until an artefact is admitted
  - [x] Keep any future vector storage replaceable and local by default
  - [x] Record semantic gain, false-neighbour, drift, memory, and rebuild-cost measurements as not performed because no candidate was admitted
  - [x] Assess Haystack, LlamaIndex, Qdrant, LanceDB, and FAISS at the admission boundary; record exact versions, licences and extension tests as unavailable because none was installed
  - [x] Build no vector database, embedding runtime, or generic retriever inside the project

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #12 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 4: Evaluate hybrid search and reranking admission

- [x] Task: Implement the phase scope
  - [x] Define deterministic fusion and candidate-set contracts
  - [x] Stop local cross-encoder and model-reranking evaluation at the missing-model admission gate
  - [x] Record quality, calibration, latency, memory, privacy, and failure-regression measurements as not performed for unadmitted candidates
  - [x] Retain the lexical baseline without declaring an operational threshold or unmeasured comparative gain

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #12 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 5: Ground answers and defend retrieval

- [x] Task: Implement the phase scope
  - [x] Require claim-evidence links, citation verification, conflict representation, and abstention
  - [x] Validate the SourceRight fail-closed adapter contract; record that no Track 07 invocation or successful validation result was admitted
  - [x] Separate bibliographic integrity, study quality, applicability, clinical interpretation, and authorised recommendation decisions
  - [x] Detect instruction-like or poisoned content without erasing legitimate evidence
  - [x] Separate source content from system and workflow instructions
  - [x] Test malicious documents, misleading metadata, stale policies, and unsupported synthesis

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #12 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 6: Implement lifecycle operations

- [x] Task: Implement the phase scope
  - [x] Implement incremental ingest, correction, supersession, delete, rebuild, backup, and restore
  - [x] Verify public and private index separation through negative tests
  - [x] Verify purpose, access, minimisation, aggregation, lineage, retention, freshness, and cross-case inference controls for organisational memory
  - [x] Propagate source and policy drift to affected answers and receipts
  - [x] Provide deterministic export and audit views

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #12 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 7: Produce retrieval assurance receipts

- [x] Task: Implement the phase scope
  - [x] Run quality, citation, privacy, robustness, freshness, latency, memory, and recovery suites
  - [x] Compare lexical, vector, hybrid, and reranked configurations transparently
  - [x] Declare known blind spots, unsupported sources, and device limits
  - [x] Approve no retrieval claim without exact source and benchmark evidence

- [x] Task: Validate the phase deliverables
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #12 and dependency evidence

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Final Track Verification

- [x] Task: Complete the track evidence pack
  - [x] Verify every acceptance criterion has direct evidence
  - [x] Re-run the complete applicable validation and regression suite
  - [x] Reconcile local files, Git history, GitHub hierarchy, native dependencies, and receipts
  - [x] Record unresolved limitations and owner decisions without downgrading them
  - [x] Close the GitHub issue only after the completion receipt passes

## Review Fixes

- [x] Task: Harden compartment, evidence and receipt boundaries — `7d2a3e3`, `f09b5fc`, `cdfa3db`
  - [x] Bind persistent indexes to one compartment and scope lifecycle operations
  - [x] Fail closed on fabricated rights, grounding, SourceRight success and Unicode instruction content
  - [x] Bind deterministic assurance and volatile research observations with separate integrity hashes
- [x] Task: Close the hosted patch-coverage gap — merged follow-up `a7f2787`
  - [x] Add negative-path coverage for lifecycle, literature and assurance bindings
  - [x] Verify the follow-up Codecov patch check and all six repository checks passed
- [x] Task: Correct false-completion and atomic-rebuild findings — `12c3698`
  - [x] Validate replacement manifests before mutation and rebuild in one transaction
  - [x] Preserve index bytes and audit state after an invalid rebuild attempt
  - [x] Return structured errors for malformed literature receipts
  - [x] Hash raw backup bytes in restore provenance
  - [x] Reconcile unexecuted vector, reranker, provider and SourceRight work as explicit negative results
- [x] Task: Complete malformed-identifier and restore-provenance review fixes — `2ec967a`
  - [x] Reject non-string result and screening identifiers without raising
  - [x] Assert restore audit provenance against the raw backup-byte SHA-256
  - [x] Clarify specification-level negative admission semantics for optional capabilities
