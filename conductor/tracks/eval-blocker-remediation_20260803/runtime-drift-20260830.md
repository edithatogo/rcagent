# Runtime availability drift after PR 83

On 2026-08-30, after merging PR #83 as `b10abeb`, a fresh
`darwin_runtime_profile.verify_files()` failed with
`profile_backend_directory_unavailable`. The requested help diagnostic never
launched. Direct existence checks also found the pinned llama 0.2.0 executable,
libomp 22.1.8 library and all five ggml 0.21.0 backend files absent. Some other
old libraries remain. Earlier successful version and READY receipts are
unchanged time-bounded observations, not proof of current availability.

## Bounded recovery inspection

Read-only inspection found cached old llama 0.2.0 and ggml 0.21.0 bottles, but
no old libomp 22.1.8 archive in the inspected Homebrew cache. No files were
restored, downloaded or installed; no global links were changed.

Installed candidates now include llama 0.3.0, ggml 0.22.0 and libomp 23.1.0.
An agent review (`root_acceptance_map`) inspected package receipts and local
licence files without executing a runtime. llama identifies source
`c1d0e7a004015f23bc0233470b747b596f29b264`. The new OpenSSL dependency receipt
names bottle rebuild 2, distinct from the old rebuild 1, so unchanged version
text is not sufficient to reuse its pin.

The installed llama/ggml licence files declare MIT. libomp's formula label says
MIT, whereas installed `LICENSE.TXT` says Apache-2.0 with LLVM Exceptions.
This is a declaration conflict to reconcile against exact component/source
evidence before positive admission, not a new legal conclusion or an assumed
rights exception. No third-party bytes are redistributed by this record.

## Recommendation and continuation

Prepare a separately versioned candidate profile for the installed runtime
under bounded local comparator acquisition decision 20260829-002. Preserve the old registry,
old profile and all raw receipts. Require exact executable/library/licence
pins, cleared environment, loader evidence, cross-profile rejection and a
fresh non-study diagnostic before any study condition is admitted. Do not
silently change old pins or promote the new profile from version labels.

Exact-commit freeze verification can proceed independently now. Runner/output
extraction must target the explicitly admitted runtime grammar, and the actual
protocol must bind that runtime and all execution components before execution.
No frozen study, admitted condition, primary result or readiness-only fallback
is claimed: unfinished engineering is not evidence that no condition is feasible.

This is agent review, not human agreement or clinical, legal, regulatory,
cultural-safety, employment, organisational or deployment validation. Exact
agent model revisions were not exposed. Rollback only this record if needed;
do not rewrite or delete historical observations.
