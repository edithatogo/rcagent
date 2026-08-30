# Context Pack: Bounded Darwin runtime profile

Base: `370d0689aebc0d440da723a21e9a044d20b3f860`; branch/PR:
`codex/prospective-continuation`, #83. Owning track:
eval-blocker-remediation_20260803. The preceding documentation head passed
seven hosted checks; this does not validate the new adapter or authorise merge.

## Scope and fit

Implement the finite [dependency repair route](../tracks/eval-blocker-remediation_20260803/runtime-dependency-route-20260830.md).
Reuse Python standard-library subprocess/hash capture and existing comparator
admission. Add a Darwin-only pinned invocation profile outside the portable
skill core, not a general dependency manager. Exact cached binaries remain
local; no acquisition, registry rewrite, global link change or new dependency.

Own `tools/darwin_runtime_profile.py`, its focused tests, the optional profile
integration in `tools/local_execution_probe.py`, and bounded prospective
profile receipts plus this track's plan/cursor/evidence. The test agent owns
only its named new test file. Read-only protocol review can run independently;
no study execution or score is authorised by this profile checkpoint alone.

## Acceptance and limits

Pin executable, direct libraries and observed optional CPU backends. Select
only exact cached directories in a cleared process environment, check actual
loader diagnostics and bytes before/after, reject missing/changed/unknown
non-system images, malformed traces, launch/timeout/output failures and
unsupported hosts. Preserve full bounded local raw diagnostics, publicise only
an inspected projection, and never claim OS attestation or study admission.

Fixture-first tests precede the live fixed version diagnostic. Require full
validation and agent-panel review; then one bounded non-study model probe may
verify the new profile on inference if its prior admitted model pins pass.
No clinical/employee data, credentials, remote inference or weight publication.
No claim that a successful process proves model suitability or no network egress.

## Commands and handoff

Use focused pytest, Ruff/types and `uv run python -m tools.full_validation`.
Review exact current diff, preserve existing PR work, and record evidence and
failures before advancing. Freshness expires on any pinned byte/loader/profile
change. Rollback only the new helper, optional integration and records; retain
historical evidence and old study locks. Next phase: frozen prospective protocol
and semantic transitions, under existing decision 20260830-002.
