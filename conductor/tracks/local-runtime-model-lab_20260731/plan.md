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
  - [x] Implement reproducible probes for CPU, accelerators, RAM, storage, OS, drivers, and supported instructions
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
  - [x] Package llama.cpp, OpenVINO, MLX, and MAX/Mojo as independent optional or experimental profiles
  - [x] Implement device-aware agent-assisted selection that explains resource, privacy, licence, download, and quality trade-offs before invoking scripts
  - [x] Provide idempotent scripted preflight, installation, verification, rollback, uninstall, and offline-bundle paths
  - [x] Prototype llama.cpp, ONNX Runtime, OpenVINO, and MLX adapters behind common generation and embedding contracts
  - [x] Assess Ollama or another maintained local facade, MLX-LM, Transformers, and vLLM for profiles where they remove project-owned model-management work
  - [x] Evaluate Windows DirectML or other backends only through measured compatibility spikes
  - [x] Isolate experimental Modular MAX or Mojo work from the portable and supported core
  - [x] Define version, build flag, driver, quantisation, cache, error, timeout, and cancellation receipts
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
  - [x] Register generic, reasoning, small, medical/domain, diffusion, encoder, OCR, ASR, vision, and signal candidates by exact repository and revision
  - [x] Record licence, architecture, parameters, context/input envelope, knowledge limits, intended use, exclusions, and remote-code needs
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
  - [x] Benchmark supported precision and quantisation variants on each feasible device context
  - [x] Measure quality, calibration, context degradation, latency, memory, load, and storage trade-offs
  - [x] Test long-context, structured output, tool-use, retrieval, and failure scenarios
  - [x] Reject configurations that swap, thrash, crash, or breach privacy/safety gates

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
  - [x] Run representative incident, policy, retrieval, summarisation, reasoning, and multimodal tasks
  - [x] Run prompt injection, data leakage, hallucination, refusal, uncertainty, and citation checks
  - [x] Compare generic models before domain-specific models
  - [x] Preserve raw outputs, repeated-run variance, exact manifests, and negative results

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
  - [x] Route by task, modality, governance status, privacy mode, device capability, context, and resource budget
  - [x] Provide deterministic and smaller-model fallbacks plus explicit no-capability outcomes
  - [x] Define verified download, checksum, provenance, cache, update, rollback, and air-gapped bundles
  - [x] Emit pre-run execution disclosures and post-run resource receipts

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
  - [x] Recommend supported, conditional, experimental, and unsuitable profiles by measured evidence
  - [x] Explain accuracy, knowledge, context, latency, RAM, storage, privacy, licence, and maintenance trade-offs
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

- [~] Task: Complete the track evidence pack
  - [x] Verify every acceptance criterion has direct evidence
  - [x] Re-run the complete applicable validation and regression suite
  - [x] Reconcile local files, Git history, GitHub hierarchy, native dependencies, and receipts
  - [x] Record unresolved limitations and owner decisions without downgrading them
  - [x] Close the GitHub issue only after the completion receipt passes
