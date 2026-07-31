# Implementation Plan: Local Runtime and Model Lab

**GitHub:** [#13](https://github.com/edithatogo/rcagent/issues/13)

Execution follows [workflow.md](../../workflow.md). Phases continue automatically when objective verification passes and no owner decision gate is reached.

## Phase 1: Define devices and measurement protocol

- [ ] Task: Implement the phase scope
  - [ ] Define current Intel CPU/iGPU 32 GB, Apple silicon/MLX, and larger CPU/GPU device contexts
  - [ ] Implement reproducible probes for CPU, accelerators, RAM, storage, OS, drivers, and supported instructions
  - [ ] Define warm/cold latency, throughput, memory, storage, load time, context, and power-proxy measurements
  - [ ] Define privacy-preserving environment manifests and repeatability rules

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #13 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 2: Implement thin runtime adapters

- [ ] Task: Implement the phase scope
  - [ ] Prototype llama.cpp, ONNX Runtime, OpenVINO, and MLX adapters behind common generation and embedding contracts
  - [ ] Evaluate Windows DirectML or other backends only through measured compatibility spikes
  - [ ] Isolate experimental Modular MAX or Mojo work from the portable and supported core
  - [ ] Define version, build flag, driver, quantisation, cache, error, timeout, and cancellation receipts

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #13 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 3: Create the governed model registry

- [ ] Task: Implement the phase scope
  - [ ] Register generic, reasoning, small, medical/domain, diffusion, encoder, OCR, ASR, vision, and signal candidates by exact repository and revision
  - [ ] Record licence, architecture, parameters, context/input envelope, knowledge limits, intended use, exclusions, and remote-code needs
  - [ ] Track Gemma 4 12B, Apriel 15B Thinker, Nemotron, G9, Phi-4 reasoning, Qwen 27B-class, DiffusionGemma, and medical candidates as hypotheses pending verification
  - [ ] Record availability and naming uncertainty rather than inventing specifications

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #13 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 4: Characterise quantisation and resource fit

- [ ] Task: Implement the phase scope
  - [ ] Benchmark supported precision and quantisation variants on each feasible device context
  - [ ] Measure quality, calibration, context degradation, latency, memory, load, and storage trade-offs
  - [ ] Test long-context, structured output, tool-use, retrieval, and failure scenarios
  - [ ] Reject configurations that swap, thrash, crash, or breach privacy/safety gates

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #13 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 5: Run task and privacy benchmarks

- [ ] Task: Implement the phase scope
  - [ ] Run representative incident, policy, retrieval, summarisation, reasoning, and multimodal tasks
  - [ ] Run prompt injection, data leakage, hallucination, refusal, uncertainty, and citation checks
  - [ ] Compare generic models before domain-specific models
  - [ ] Preserve raw outputs, repeated-run variance, exact manifests, and negative results

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #13 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 6: Implement routing and offline packaging

- [ ] Task: Implement the phase scope
  - [ ] Route by task, modality, governance status, privacy mode, device capability, context, and resource budget
  - [ ] Provide deterministic and smaller-model fallbacks plus explicit no-capability outcomes
  - [ ] Define verified download, checksum, provenance, cache, update, rollback, and air-gapped bundles
  - [ ] Emit pre-run execution disclosures and post-run resource receipts

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #13 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 7: Publish device recommendation matrices

- [ ] Task: Implement the phase scope
  - [ ] Recommend supported, conditional, experimental, and unsuitable profiles by measured evidence
  - [ ] Explain accuracy, knowledge, context, latency, RAM, storage, privacy, licence, and maintenance trade-offs
  - [ ] Date every recommendation and connect it to drift checks
  - [ ] Require owner approval before public comparative claims

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #13 and dependency evidence

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
