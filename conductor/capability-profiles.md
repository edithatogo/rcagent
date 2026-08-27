# Capability Profiles and Optional Installation

## Principle

The portable investigation core must remain useful without heavyweight model,
retrieval, document, speech, imaging, signal, cloud, or client dependencies.
Every advanced capability is an optional, replaceable profile whose activation
cannot weaken privacy, evidence, clinical-safety, or human-review controls.

The machine-readable registry is
[`capability-profiles.json`](./capability-profiles.json).
Its structural contract is
[`schemas/capability-profiles.schema.json`](./schemas/capability-profiles.schema.json),
with cross-record invariants enforced by `tools/validate_repository.py`.

## Installation and Operation Contract

An implemented profile declares the applicable details below. Planned profiles
are intentionally limited declarations until their owning track supplies and
tests those details:

- whether it is `core`, `optional`, `experimental`, `enterprise`, or
  `research-only`;
- whether it is implemented, planned, blocked, or unavailable;
- supported operating systems, architectures, execution modes, and device
  classes;
- exact dependencies, licences, telemetry, network, storage, and model/data
  download implications;
- minimum and recommended resources plus known context and quality limits;
- script, agent-assisted, manual, container, and offline installation paths;
- preflight, install, verify, health-check, update, rollback, and uninstall
  commands;
- capability discovery, safe fallback, and failure-isolation behaviour; and
- evidence receipts recording versions, checks, limitations, and residual
  risk.

The agent-assisted installer must inspect the device and approved execution
mode, explain material downloads or egress, recommend the smallest adequate
profile, and call the same idempotent scripts available to a human operator.
It must not improvise an undocumented installation command or silently enable
telemetry, remote processing, paid services, or research-only clinical use.

## Baseline Profiles

| Profile | Default | Intended role |
|---|---:|---|
| `core` | Yes | Portable skills, workflows, templates, and deterministic contracts |
| `validate` | CI and maintainer | Repository, schema, link, policy, fixture, and conformance checks |
| `retrieval-lexical` | No | Local deterministic full-text retrieval |
| `retrieval-vector` | No | Local embeddings, vector index, hybrid fusion, and reranking |
| `documents-ocr` | No | Document parsing, layout analysis, and OCR adapters |
| `speech-local` | No | Local transcription and optional diarisation |
| `medical-imaging-research` | No | DICOM and image ingestion under a research-only gate |
| `ecg-research` | No | ECG/time-series ingestion and evidence extraction under a research-only gate |
| `runtime-openvino` | No | Intel CPU/iGPU inference where benchmark evidence supports it |
| `runtime-mlx` | No | Apple Silicon inference through MLX |
| `runtime-llamacpp` | No | Portable quantised local inference |
| `runtime-mojo-experimental` | No | Time-bounded MAX/Mojo adapter experiments |
| `enterprise-connectors` | No | Approved systems of record, identity, content, workflow, and reporting adapters |
| `client-adapters` | No | Claude, Codex, and other thin client packages |
| `domain-adaptation` | No | Governed prompting, adapters, LoRA, or fine-tuning after readiness gates |
| `jurisdiction-national` | No | Shared national-baseline standards mapping (NSQHS, ACSQHC) consumed by every state pack |
| `jurisdiction-nsw` | No | NSW Health / CEC / ACI source mappings over the national baseline |
| `jurisdiction-qld` | No | Queensland Health / CEQ / QLD coronial source mappings over the national baseline |
| `health-analytics-process-mining` | No | Process mining and aggregate quality/safety analytics on de-identified event data (research-only gate) |

Planned profiles are declarations, not claims that their dependencies or
installers already exist. A profile becomes installable only after its owning
track supplies tested scripts, a compatibility matrix, rollback, and a signed
or otherwise reviewable receipt.

## Track Ownership

- Track 00 owns portable-core and client capability declarations.
- Track 01 owns profile schemas, installer contracts, discovery, receipts, and
  operator experience.
- Track 03 owns privacy, egress, telemetry, secrets, retention, and assurance
  gates.
- Tracks 06–08 own multimodal, retrieval, runtime, and model profiles.
- Track 04 owns jurisdiction capability declarations; state packs inherit
  `jurisdiction-national` and may not widen core safeguards.
- Track 07 owns aggregate health-analytics declarations; nothing there touches
  identifiable data outside the research-only gate.

## Contributing a Jurisdiction Pack

Any new state or territory follows the same generic contract — no core code
changes required:

1. Pick the identifier from `jurisdiction_framework.id_pattern`
   (`jurisdiction-<state>`, e.g. `jurisdiction-vic`, `jurisdiction-wa`).
2. Add one entry to `profiles` in `capability-profiles.json` with
   `"class": "optional"`, `"status": "planned"`, `"default": false`, and
   `"owner_track": 4` (Track 04 owns the framework; per-jurisdiction source
   mapping work lands there until it earns its own track).
3. Register authoritative sources in the jurisdiction source registry with
   issuer, version, status, retrieval date, rights, and review cadence —
   national-baseline requirements are inherited from
   `jurisdiction-national` and must not be re-declared.
4. Model only genuinely state-specific workflows on top of the baseline;
   record any conflicting interpretation as an owner decision per Track 04's
   specification.
5. Pass the same preflight/install/receipt/rollback contract as every other
   profile; `planned` profiles are declarations, never installables.

- Track 09 owns interface-level discovery and runtime setup assistance.
- Track 10 owns domain-adaptation profiles.
- Track 11 owns packaging, update, rollback, registry, and plugin distribution.

No track may add a mandatory heavyweight dependency to `core` merely because
an optional profile uses it.
