# Contributing

This repository accepts bounded, evidence-backed contributions that preserve
the portable core, synthetic/public-data boundary, and accountable-authority
gates.

## Before changing code or content

1. Read `AGENTS.md`, `conductor/index.md`, `conductor/product-guidelines.md`,
   and `conductor/workflow.md`.
2. Select the owning Conductor track or issue. Do not create a parallel schema,
   workflow, client behaviour, or system of record.
3. Use synthetic placeholders and public or explicitly authorised sources.
   Never commit patient, consumer, employee, credential, confidential, or
   organisation-sensitive information.
4. Record exact source revisions, rights, limitations, and rollback where the
   change depends on external material.

## Validation

After installing the development dependencies, run the complete deterministic
local gate with one command:

```bash
uv run python -m tools.full_validation
```

The command performs lint, type, governance, deterministic benchmark, and test
checks. It does not download model weights or establish hosted, clinical,
legal, policy, regulatory, employment, cultural-safety, organisational, or
deployment approval.

## Pull requests

- Keep one coherent acceptance boundary per pull request.
- Explain the evidence, negative findings, tests, privacy mode, rights, and
  rollback.
- Do not request or imply human approval as a repository completion condition;
  stable automated checks are the merge gate for this solo-maintainer project.
- Treat releases, submissions, credentials, hosted settings, private data, and
  accountable-authority decisions as separate actions.

See `SECURITY.md` for vulnerability reporting and `SUPPORT.md` for the support
boundary.
