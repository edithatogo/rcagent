# Track 11 Foundation and Packaging Receipt

## Scope

This receipt covers Phase 0, the registry-funnel assessment, and the local
review-only portion of portable-skill packaging. It does not cover a public
release, hosted installation, client marketplace submission, directory
acceptance, publisher verification, or support commitment.

## Revisions

- Track activation: `5a0d062`
- Deterministic package builder and tests: `66831ec`
- Fit-gap and registry assessment: `f310539`
- Hard dependency: Track 00 completion receipt dated 2026-08-29
- Licence: Apache-2.0

## Verification

The focused distribution suite passed with three tests. It proves deterministic
archive bytes, per-file and archive SHA-256 checksums, the bundled licence,
CycloneDX metadata, absence of network and telemetry requirements, refusal to
overwrite a non-empty destination, and explicit `public_release: false` state.

Fresh-context review added six negative release-identifier cases and one
negative source-tree-output case in `a4a2c77`. The focused distribution suite
now contains ten passing tests.

Owner conditions added on 2026-08-29 require public artefacts to contain no
third-party-controlled material and no private clinical or employee data, and
to carry clinical, policy, legal, and organisational-approval disclaimers.
Commit `b8b2b7a` bundles `DISCLAIMER.md` and adds machine-readable public-only,
rights, and approval-boundary declarations to each local package.

Repository governance validation passed after the fit-gap and registry records
were added. Existing adapter contract tests cover isolated copies of the
unmodified portable core for Codex, Claude Code, OpenCode, Cline, and Cursor.

The closeout checkpoint reported:

- Ruff over `tools` and `tests`: passed;
- ty over `tools` and `tests`: passed;
- basedpyright: passed with no diagnostics;
- repository governance validation: passed;
- portable-skill validation: passed; and
- pytest: 202 passed.

A bare unscoped `ty check` also inspected the vendored SourceRight submodule and
reported seven diagnostics in its optional Colab and Streamlit surfaces. Those
files are outside the Track 11 revision and configured project type boundary;
the repository-owned scoped gate passed after the Track 11 manifest typing was
fixed in `7655578`.

## Limitations and negative findings

- Current hosted marketplace and directory guidance was not established by the local package tests.
- The registry assessment is provisional rather than a current-source matrix; exact hosted versions, terms, telemetry, maintenance, and deprecation evidence remain pending.
- The archive does not yet satisfy the plan's complete changelog, source-revision provenance, and client-compatibility metadata claim.
- The package controls express and test policy, but do not prove file-by-file third-party rights clearance or the absence of private data; an exact-candidate rights and public-data review remains pending.
- No tag, GitHub release, attestation, signing event, upload, submission, or acceptance was performed.
- Tracks 01, 03, 05, and 09 remain phase dependencies for later Track 11 validation.
- Community catalogue ownership and removal guarantees remain unverified and unsuitable for submission.
- A pinned GitHub release is part of Track 11 acceptance, so repository-only work cannot complete the track.

## Safe continuation

Continue local compatibility, negative-test, drift, and submission-packet work.
The owner authorised public releases and registry or marketplace submissions on
2026-08-29. Decision `20260829-004-track11-first-public-release` is therefore
approved with conditions. Continue to fail closed until all affected dependency
receipts and exact-candidate release or submission checks pass; the instruction
does not turn an incomplete or unreviewed artefact into a releasable one.
