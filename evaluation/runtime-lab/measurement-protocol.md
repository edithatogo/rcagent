# Track 08 measurement protocol

## Scope

This protocol distinguishes discovery, interface conformance, measured
research evidence and support. Discovery or a passing fake-runtime test is not
a benchmark and cannot produce a recommendation.

## Device contexts

| Context | Required observation | Current state |
|---|---|---|
| 32 GiB Intel CPU/iGPU | exact local probe, runtime/build/driver and repeated execution receipt | unavailable; unsupported |
| Apple silicon with MLX | exact local probe, MLX/runtime/model receipt and repeated execution | runtime command observed but unmeasured; unsupported |
| Larger CPU/GPU host | exact local probe, accelerator/driver/runtime/model and repeated execution receipt | unavailable; unsupported |

Device receipts contain only coarse operating-system family, architecture,
logical processor count, four-GiB memory floor, accelerator class and explicit
redaction state. They exclude hostnames, user names, serials, network
addresses, mount paths, process lists and environment values.

## Required measures

An execution receipt must bind cold load, warm latency, throughput, peak
resident memory, storage bytes, context length, repeated-run variance and a
clearly labelled CPU-time or energy-counter power proxy. It must also bind the
exact runtime executable hash, build flags, model repository and immutable
revision, every admitted file hash, quantisation, fixture hash, arguments,
sanitised environment-key policy and device receipt.

Missing measures produce `unsupported`, never an estimated value. Swap,
thrash, crash, timeout, cancellation, non-zero exit, checksum drift, ambiguous
network isolation or unsupported modality fail closed.

## Safety and privacy benchmark

Only the Track 05 generated synthetic cases may be used without a new data
decision. Tests cover incomplete and conflicting evidence, injection, leakage,
hallucination, refusal, uncertainty, citation and authority boundaries. Raw
outputs remain local and are represented in durable receipts by hashes. No
clinical, legal, policy, employment, regulatory or organisational conclusion
is scored as valid.

## Recommendation rule

A row may become `conditional` or `supported` only when the exact
runtime-model-quantisation-device tuple has a current passing resource,
quality, privacy and lifecycle receipt. Contract-only, installed-unmeasured,
unavailable and experimental profiles remain unsupported. Public comparative
claims require a separate authority action and publication receipt.
