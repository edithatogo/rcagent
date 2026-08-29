# Implementation Plan: Local Runtime and Model Lab

**GitHub:** [#13](https://github.com/edithatogo/rcagent/issues/13)

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

## Evidence Interpretation

An unavailable or unmeasured runtime/device/model is a valid negative result
when the contract, probe, admission rules, safe fallback and limitation receipt
pass. It does not count as executed adapter coverage, measured suitability or
support. Installation and offline lifecycle tasks complete for the supported
profile set, which is empty; their verifier contracts do not claim that any
third-party runtime or model was downloaded, installed, redistributed or
removed.

## Phase 0: Existing-System Fit and Gap Closure

- [x] Task: Establish the system and dependency context (`62be300`)
  - [x] Read `integration-strategy.md` and this track's entry in `integration-map.json`
  - [x] Identify the current organisational system, standard, framework, runtime, or platform that already owns each capability
  - [x] Record exact versions, extension points, licences, maintenance, privacy, telemetry, offline, device, and security constraints
  - [x] Test existing configuration, profiles, APIs, exports, imports, plugins, and adapters against representative fixtures

- [x] Task: Select the smallest adequate intervention (`62be300`)
  - [x] Prefer existing-system configuration or a standards profile
  - [x] Prefer a thin replaceable adapter when translation is the remaining gap
  - [x] Identify generic gaps suitable for an authorised upstream issue or contribution
  - [x] Limit project code to the smallest safety-, privacy-, jurisdiction-, or domain-specific extension
  - [x] Require a fit-gap record and approved ADR before any new subsystem or permanent fork

- [x] Task: Define the dependency lifecycle (`62be300`)
  - [x] Assign each dependency to a locked core, optional adapter, enterprise connector, evaluation, or experimental profile
  - [x] Define contract tests, compatibility windows, drift checks, failure isolation, and safe fallback
  - [x] Give every local shim an upstream reference, owner, expiry or removal condition, and replacement path
  - [x] Update `integration-map.json` with the selected status and evidence links

- [x] Task: Phase Verification & Checkpoint (`62be300`)
  - [x] Verify that no planned work duplicates an adequate existing capability
  - [x] Verify the system-of-record and data-authority boundary
  - [x] Verify the smallest remaining gap and ownership rationale
  - [x] Record the fit-gap receipt and bounded handoff context
  - [x] Continue automatically through the next ready phase, review, bounded rework, documentation synchronization, and next ready track
  - [x] If an owner gate is reached, create a complete decision packet, pause only the affected scope, release the lane, and continue independent work

## Phase 1: Define devices and measurement protocol

- [x] Task: Implement the phase scope (`62be300`)
  - [x] Define current Intel CPU/iGPU 32 GB, Apple silicon/MLX, and larger CPU/GPU device contexts
  - [x] Implement a reproducible privacy-safe coarse CPU/accelerator probe and record RAM, storage, drivers, instructions and power as explicitly unobserved where not safely measured
  - [x] Define warm/cold latency, throughput, memory, storage, load time, context, and power-proxy measurements
  - [x] Define privacy-preserving environment manifests and repeatability rules

- [x] Task: Validate the phase deliverables (`62be300`)
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #13 and dependency evidence

- [x] Task: Phase Verification & Checkpoint (`62be300`)
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 2: Implement thin runtime adapters

- [x] Task: Implement the phase scope (`62be300`; negative-result closure)
  - [x] Classify llama.cpp, ONNX Runtime, OpenVINO and MLX as independent optional profiles and MAX/Mojo as isolated experimental; none is supported
  - [x] Implement model-free discovery and fail-closed selection disclosures without invoking installation or inference scripts
  - [x] Provide an idempotent operator-owned offline inventory verifier; record install, update, rollback and uninstall as unavailable for the empty supported set
  - [x] Reuse the Track 05 llama.cpp comparator and Track 06 ONNX encoder contracts; record OpenVINO and MLX as unavailable or installed-unmeasured, not executed adapters
  - [x] Assess maintained facades and frameworks at fit-gap level only; admit none without an exact artefact and execution receipt
  - [x] Record DirectML and other unobserved backends as unsupported; no measured compatibility spike occurred
  - [x] Isolate experimental Modular MAX or Mojo work from the portable and supported core
  - [x] Define required future receipt fields and preserve version, build, driver, quantisation, cache, timeout and cancellation evidence as missing
  - [x] Implement no inference engine, tensor library, model format, or downloader that an admitted upstream runtime already provides

- [x] Task: Validate the phase deliverables (`62be300`)
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #13 and dependency evidence

- [x] Task: Phase Verification & Checkpoint (`62be300`)
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 3: Create the governed model registry

- [x] Task: Implement the phase scope (`62be300`; no models admitted)
  - [x] Admit no model because no candidate had a complete exact repository, immutable revision and device receipt
  - [x] Require licence, provenance, context/input, task, quantisation, device, failure and remote-code fields for any future admitted entry
  - [x] Track Gemma 4 12B, Apriel 15B Thinker, Nemotron, G9, Phi-4 reasoning, Qwen 27B-class, DiffusionGemma, and medical candidates as hypotheses pending verification
  - [x] Record availability and naming uncertainty rather than inventing specifications

- [x] Task: Validate the phase deliverables (`62be300`)
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #13 and dependency evidence

- [x] Task: Phase Verification & Checkpoint (`62be300`)
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 4: Characterise quantisation and resource fit

- [x] Task: Implement the phase scope (`62be300`; no eligible tuple)
  - [x] Find no supported runtime-model-quantisation-device tuple eligible for benchmarking
  - [x] Preserve quality, calibration, context, latency, memory, load and storage measures as unavailable rather than estimating them
  - [x] Define long-context, structured-output, tool-use, retrieval and failure measures for future admitted tuples; execute none
  - [x] Reject every unmeasured configuration before swap, thrash, crash or privacy/safety exposure

- [x] Task: Validate the phase deliverables (`62be300`)
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #13 and dependency evidence

- [x] Task: Phase Verification & Checkpoint (`62be300`)
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 5: Run task and privacy benchmarks

- [x] Task: Implement the phase scope (`62be300`; Track 05 evidence reused, no execution)
  - [x] Reuse Track 05 synthetic task and privacy evidence as dependency context; run no Track 08 model task
  - [x] Verify routing and admission controls against injection/leakage boundary fixtures without generating model output
  - [x] Admit neither generic nor domain-specific models, so no comparative ranking occurred
  - [x] Preserve exact manifests and negative admission results; no Track 08 raw model output or repeated-run variance exists

- [x] Task: Validate the phase deliverables (`62be300`)
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #13 and dependency evidence

- [x] Task: Phase Verification & Checkpoint (`62be300`)
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 6: Implement routing and offline packaging

- [x] Task: Implement the phase scope (`62be300`)
  - [x] Keep absence or failure of a local runtime non-fatal to the portable core and expose an explicit capability-limited mode
  - [x] Validate task, modality, data class, local isolation, runtime/model admission and context; reject governed-private and all unmeasured routes
  - [x] Preserve existing deterministic workflows as the only fallback and emit explicit no-capability for models
  - [x] Verify checksums, paths and exact inventory for operator-owned offline directories without download, cache mutation or redistribution
  - [x] Emit discovery and no-capability receipts; no post-run resource receipt exists because no execution occurred

- [x] Task: Validate the phase deliverables (`62be300`)
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #13 and dependency evidence

- [x] Task: Phase Verification & Checkpoint (`62be300`)
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 7: Publish device recommendation matrices

- [x] Task: Implement the phase scope (`62be300`; internal unsupported matrix)
  - [x] Publish an internal matrix classifying every declared runtime as unsupported from observed negative evidence
  - [x] State that accuracy, knowledge, context, latency, RAM, storage and quality trade-offs are unmeasured; preserve privacy, licence and maintenance boundaries
  - [x] Date every recommendation and connect it to drift checks
  - [x] Require owner approval before public comparative claims

- [x] Task: Validate the phase deliverables (`62be300`)
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #13 and dependency evidence

- [x] Task: Phase Verification & Checkpoint (`62be300`)
  - [x] Verify every deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Final Track Verification

- [x] Task: Complete the track evidence pack (`fb38ea3`)
  - [x] Verify every acceptance criterion has direct evidence
  - [x] Re-run the complete applicable validation and regression suite
  - [x] Reconcile local files, Git history, GitHub hierarchy, native dependencies, and receipts
  - [x] Record unresolved limitations and owner decisions without downgrading them
  - [ ] Close the GitHub issue only after the completion receipt and hosted integration checks pass

## Review Fixes

- [x] Task: Close forged routing, malformed-input, modality, private-data, registry and bundle-integrity findings (`eaf9ea3`)
- [x] Task: Close receipt privacy, undeclared-symlink and negative-state contract findings (`8000b2c`)
- [x] Task: Record phase, completion and unanimous agent-panel evidence while preserving external gates
- [x] Task: Reject POSIX and Windows absolute bundle paths consistently after hosted Windows replay
