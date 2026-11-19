# OpenGrep SAST pilot for portable core

Status: **pilot, source only, not a required check**. Started 20 November 2026.

Scope: tracked Python files under `tools/` (not research evidence,
conductor records or tests); `repo-standards` reusable SAST workflow pinned
at `59a82e66216601bd07409aaeb0871a46753d6996`. No clinical data or
external models are processed. Do not infer full-repository coverage.

The shared job checks OpenGrep v1.33.1 binary provenance, synthetic
positive/negative fixtures, nonempty scan inventory, scanner errors, and
WARNING findings with `--strict --error`. No raw result is uploaded.
The live `p/python` rule pack is not yet immutable or proven equivalent
to Semgrep. Existing quality, privacy, dependency and rights gates
remain unchanged.

Acceptance:
- [x] Add separate source-security pilot in an unowned workflow and retain all existing workflows.
- [ ] Verify workflow_call resolves this exact shared commit and runs on the exact PR SHA.
- [ ] Record scanned and skipped files, new findings, parser errors, and runtime.
- [ ] Resolve qualified findings or source parser gaps without blanket exceptions.
- [ ] Freeze rule bytes with compliant rights and establish baseline/parity.
- [ ] Promote to required protection only after proven, accepted scanner behaviour.

This does not reopen completed Track 03 or compete with Track 13
scientific/visual owners. It is a narrow portfolio security control.
