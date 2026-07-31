# Capability Profiles and Optional Installation

## Principle

The portable investigation core must remain useful without heavyweight model,
retrieval, document, speech, imaging, signal, cloud, or client dependencies.
Every advanced capability is an optional, replaceable profile whose activation
cannot weaken privacy, evidence, clinical-safety, or human-review controls.

The machine-readable registry is
[`capability-profiles.json`](./capability-profiles.json).

## Installation and Operation Contract

Each profile declares:

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
- Track 09 owns interface-level discovery and runtime setup assistance.
- Track 10 owns domain-adaptation profiles.
- Track 11 owns packaging, update, rollback, registry, and plugin distribution.

No track may add a mandatory heavyweight dependency to `core` merely because
an optional profile uses it.
