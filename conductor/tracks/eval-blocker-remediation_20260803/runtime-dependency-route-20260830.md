# Bounded runtime dependency repair route

Base: `dec4728b12d408939d1e695d626252d789a0eea9`; observed 2026-08-30.
This diagnoses the next local execution blocker. It is not a runtime-profile
implementation, complete loader receipt, model run or study admission.

## Observed drift

The original llama-cli 0.2.0 executable still hashes to
`456af2d481095b6a953b6ad21e9caa0411e5508955eb841f37574235da10a44e`.
Read-only `otool -L` and resolved paths show that its mutable Homebrew links
now select ggml 0.22.0 and libomp 23.1.0; the existing registry describes
0.21.0 and 22.1.8. Exact old files remain cached. The
[earlier probe](./local-execution-provenance-20260830.md) correctly excluded
shared-library attestation; its limited process-observation claim is unchanged.

The old llama installation receipt describes OpenSSL package 3.6.3, revision
0, bottle rebuild 1. The registry's label `3.6.3_1` must not be represented as
verified package revision 1. Record that discrepancy in the new profile;
do not rewrite the historical registry or publish installation-cache paths.

## Tested route and limits

A single `llama-cli --version` diagnostic used a cleared environment with
`PATH=/usr/bin:/bin`, `LANG=C`, `DYLD_PRINT_LIBRARIES=1`, and a process-local
`DYLD_LIBRARY_PATH` containing only these exact directories, in this order:

1. `/opt/homebrew/Cellar/llama.cpp/0.2.0/lib`
2. `/opt/homebrew/Cellar/ggml/0.21.0/lib`
3. `/opt/homebrew/Cellar/libomp/22.1.8/lib`
4. `/opt/homebrew/Cellar/openssl@3/3.6.3/lib`

The command exited 0 and reported version 0.2.0, build 10566, commit
`bb4caa754`, AppleClang 21.0.0.21000101 for Darwin arm64. Displayed loader
lines selected those old llama/ggml/libomp libraries and OpenSSL 3.6.3.
Later lines showed ggml 0.21.0 CPU backends under `libexec/`, which must also
be considered by the profile. No model argument, prompt or study case was
supplied; no model download, credential or global symlink change occurred.

The diagnostic output exceeded the tool's display limit. It is therefore
partial observed evidence, not an exhaustively retained or hashed loader
trace. A new adapter must capture complete bounded diagnostics locally and
verify every reported non-system image before it can pass. The successful
version invocation does not prove model-inference compatibility or network
isolation, and it does not admit a study condition.

Read-only SHA-256 checks also confirmed these currently available old bytes:

| File under its exact Cellar directory | SHA-256 |
| --- | --- |
| ggml/0.21.0/lib/libggml.0.21.0.dylib | `c3d660fbd37d5bae33e68371d27aab78b9875ccb5676532d3f1cfe1cea6f8734` |
| ggml/0.21.0/lib/libggml-base.0.21.0.dylib | `5d193ff57adff4912c686903b38a2802a716639d2240cebd4275faeee4d94574` |
| libomp/22.1.8/lib/libomp.dylib | `b6d9b621ca10f9e097de32b77b1bd50ca0b6e606168a0d7368e82fd279dbfb4f` |

These are a snapshot, not a complete allowlist or authenticity proof.

## Agent recommendation and implementation acceptance

The `dependency_scope` agent recommended a bounded Darwin invocation profile
over copying or rewriting binaries, silently accepting newer dependencies,
or building a general macOS dependency-attestation subsystem. The main agent's
version diagnostic supports feasibility, not completed implementation.

Use exact allowlisted Cellar directories and file hashes; verify pins before
and after execution, record the actual loader selections including backends,
and reject changed/missing/unrecognised non-system images. Add fixture tests
for malformed or absent diagnostics, injected loader paths, changed pins,
timeout, nonzero exit and output truncation. Bound time and retained output;
inspect paths before any public receipt projection. Reuse existing admission
and execution adapters without weakening their gates.

System shared-cache libraries, OS/driver identity, dynamic-load coverage,
TOCTOU and unenforced network isolation remain explicit limitations. A finite
userland profile can support bounded synthetic research without claiming a
fully attested OS. No new dependency acquisition or owner approval is required
for this exact local repair. If it cannot pass after bounded evidence-led
recovery, retain the failure and use the approved contingency only when its
conditions actually apply.
