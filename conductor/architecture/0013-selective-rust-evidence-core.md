# ADR 0013: Assess selective Rust adoption for evidence integrity and local execution

- Status: recommended bounded spike; no Rust migration implemented or runtime qualified
- Date: 2026-11-13
- Owners: Track 13 assurance and Track 12 component contracts
- Scope: memory/resource control, typed deterministic boundaries, local worker and reuse

## Context

The user asked whether Rust's memory management justifies migration. The current implementation is predominantly Python orchestration, JSON/domain validation and agent-skill content. The observed defects concern semantic reference types, export policy and template admission. They can be repaired in Python and are not evidence of a memory-corruption failure. Existing Python NLP/model/document tooling remains useful.

Rust's ownership and borrowing model offers compile-time guarantees for safe-code memory use without a garbage collector [S1]. Unsafe code and foreign/native dependencies require separate scrutiny [S2]. Those properties do not establish source truth, semantic correctness, absence of hallucinations, data confidentiality or bounded allocation by themselves. Python/Rust boundary copies, native parsers, model runtimes, OS permissions and resource limits remain part of the threat model.

## Recommendation

Repair and profile the current system first. Reuse qualified existing Rust libraries from the user's ecosystem where their contracts fit. Then run one bounded side-by-side spike for a deterministic evidence boundary, rather than migrate the entire workbench before its research contract is stable.

Good candidates are streaming source hashing/size limits, typed ID/reference validation, exact span validation, interval/partial-order checks, bounded export manifests, or a narrowly scoped local worker/broker. Keep clinical inference, experiment composition and maintained Python NLP/model adapters at their existing boundary until a measured need exists.

## Alternatives

| Option | Benefits | Costs and risks | Proposed disposition |
| --- | --- | --- | --- |
| Harden typed Python and reuse current native libraries | Fastest defect repair; mature research tooling; few packaging surfaces | Dynamic data boundaries and memory overhead require tests/profiling | Immediate baseline |
| Rust deterministic core with Python API via PyO3/maturin | Explicit domain types, predictable ownership, reusable compiled core | FFI/copy semantics, build/wheel support, dual-language maintenance | Bounded candidate spike [S3] |
| Rust isolated worker with versioned JSON/IPC | Explicit process boundary and resource controls; language-independent contract | Protocol/version/cancellation/OS sandbox work; no automatic no-egress guarantee | Candidate if isolation/resource evidence identifies the need |
| Full Rust rewrite | Single implementation language for core services | Rebuilds mature adapters, delays component evidence, introduces migration risk | Defer until comparative evidence supports this scope |

## Fixed benchmark and decision rule

Use the same admitted synthetic small/large/adversarial workloads for Python and Rust: streamed documents, malformed Unicode, deeply nested/oversized JSON, forged digests, wrong-kind IDs, cyclic temporal relations, duplicate events and bounded exports. Freeze input hashes and output-contract versions before measuring.

Require output parity on supported cases, explicit matching failure semantics, all critical invariants, bounded allocation/cancellation, reproducible builds and install/uninstall success on target platforms. Measure peak RSS and memory growth, p50/p95 latency, cold start, binary/wheel size, FFI copies, security surface and maintenance effort. Freeze an adoption margin after profiling and before running the candidate; choose Rust only when it materially improves a declared constraint without losing correctness, portability or privacy. No manufactured numeric speedup target is claimed before baseline data exists.

If adopted, require rustfmt, clippy with warnings denied, cargo test, proptest, cargo-fuzz for parser boundaries, cargo-mutants for invariants, dependency/advisory/licence checks, minimal features, and an explicit unsafe-code policy. Record MSRV/toolchain/lockfile and cross-language schema compatibility. Use Miri where applicable to project unsafe/FFI-facing logic; its pass is not proof of every native dependency. Candidate tools need current-version admission before installation.

## Compatibility and rollback

Version the contract independently of language. Keep Python as the parity oracle during the spike; do not silently fall back across a privacy boundary. Feature-disable or remove the Rust adapter if parity/resource/security gates fail. A full rewrite or new distribution surface is a later evidence-backed decision, not implied by this ADR.

## Sources

- S1: Rust Book, What is Ownership?, checked 13 November 2026: https://doc.rust-lang.org/book/ch04-01-what-is-ownership.html
- S2: Rust Book, Unsafe Rust: https://doc.rust-lang.org/book/ch20-01-unsafe-rust.html
- S3: PyO3 user guide, Getting started, checked 13 November 2026: https://pyo3.rs/main/getting-started.html. Maintainers recommend maturin for the binding/build route; exact versions remain a spike input.
- Existing [Track 12 process-mining plan](../research/cognitive-autopsy/process-mining.md) identifies the Rust4PM reuse boundary; SourceRight already has a thin adapter in this repository.
