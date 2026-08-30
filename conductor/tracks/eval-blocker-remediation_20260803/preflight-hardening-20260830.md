# Evaluation preflight hardening

## Scope and result

This is a fail-closed security repair, not completed study admission. The three
legacy PowerShell entry points no longer accept prose or a nonempty CSV as
evidence. Admission, scoring and analysis transitions return exit 1 with
`semantic_admission_not_implemented` and `study_unlocked: false`.
Existing named input aliases are retained; Track 5's `BlindingMap` argument
is accepted but cannot enable scoring. Python 3.11+ is required; select it
with `-PythonExecutable` when `python` is not the configured interpreter.

## Fixture contract

The Python CLI offers `--check-fixture` only for synthetic contract testing:

```sh
uv run python -m tools.evaluation_preflight --stage admission --check-fixture --receipt /absolute/synthetic/receipt.json --expected-sha256 <receipt-digest>
```

The JSON object has exactly `schema_version` (`1.0`), `purpose`
(`contract-fixture`), `study_id` (lowercase slug), `revision` (40 lowercase
hex characters), `stage`, and `files`. Each file entry has exactly `role`,
`path` (relative to the receipt), and `sha256` (64 lowercase hex characters).
Files must be nonempty, at most 4 MiB each, with unique paths and roles;
symlinks, path traversal and duplicate JSON keys are rejected.

| Stage | Required roles |
|---|---|
| admission | protocol, manifest, raw, normalized, metadata, attestation |
| scoring | protocol, manifest, admission, blinding |
| analysis | protocol, manifest, admission, blinding, scores, panel-review |

Fixture success is exit 0, `fixture_pass`, **always** `study_unlocked: false`.
Study callers must not consume fixture exit status as admission. The wrappers
do not expose fixture mode. Role names do not validate artefact semantics.
The revision is format-checked, not authenticated; hashes prove byte identity,
not authorship or correctness. No historical cohort inventory was performed.

## Verification and limitations

Tests generate synthetic temporary files only. They exercise all stages,
legacy wrappers, pins, malformed JSON, invalid fields, duplicate identities,
path escapes, missing/empty/modified files and resource limits.
Local evidence on macOS/Python 3.14.5: the focused suite passed 43 tests,
including actual PowerShell execution. The 40-test fixture suite measured
100% statement/branch coverage of the new Python validator. Ruff, ty,
basedpyright and repository governance checks passed. The initial full gate
passed 513 tests; the final full rerun passed 516 tests (92.49% overall
coverage), including the three added interpreter regression cases.
Hosted CI is not claimed here.
Agent-panel review covers acceptance, evidence and security; agreement is
agent agreement, not independent human validation. No clinical, legal, policy,
regulatory, employment, cultural-safety, organisational or deployment approval
is implied. No provider execution, private data, acquisition or release occurs.

Panel disposition: acceptance and evidence reviewers accepted the bounded
scope; the evidence reviewer requested the migration documentation above.
The security reviewer reproduced a success-returning interpreter bypass in
the wrappers. All three now return exit 1 unconditionally, with success-stub
and missing-interpreter regressions. The security reviewer rechecked the fix
and reported no remaining blocker. Reviewer identities: portfolio_acceptance,
portfolio_evidence and portfolio_security, agent class; exact model revisions
not exposed. Review inputs were the branch diff against `7ba8b1c`, this plan,
and synthetic tests. Correlated agent errors remain possible; review is not
independent human agreement or empirical validation of the study.

The next step is the approved versioned synthetic protocol and semantic
admission adapter, then scoring and analysis validators. Until those exist,
all live transitions remain blocked. Root #1 and historical evaluation remain
open/incomplete. Do not revert to the permissive scripts as an operational
fallback; retain the lock while repairing any defect.
