# RCA Investigation — Safety Systems Workbench

`rca-investigation` is a portable, Markdown-based Agent Skill for
evidence-grounded healthcare safety investigation support. It helps organise
scope, chronology, system contributors, reports, actions and effectiveness
checks. It assists an accountable investigation team; it is not an autonomous
investigator, clinician, legal adviser or system of record.

## Package and repository scope

The recorded supported public package is
[v0.1.1](https://github.com/edithatogo/rcagent/releases/tag/v0.1.1), built from
commit `af5777bdefa2cb0052ee80c1c5fac9ed972568a4`. Its portable core and
skills-only Codex and Claude Code archives have exact checksums and isolated
installation evidence in the
[release receipt](conductor/archive/distribution-registries-plugins_20260731/evidence/hosted-release-v0.1.1-20260829.md).
Use the receipt and release checksum manifest to identify the exact artefact;
this source checkout is not itself a new release.

The skills-only packages contain instructions and supporting files, not a
model endpoint, MCP server, account integration or telemetry service. The
host client controls execution, permissions, logging, model processing and
data handling. Package installation does not establish client compatibility,
privacy enforcement or organisational approval beyond the exact evidence.

The wider repository contains validation tools, schemas, research and
governed capability work. Its [product plan](conductor/product.md) describes
a broader workbench; those plans are not claims that every capability is
included in the released skill or validated for operational use.

## Explore the workflow

Start with the [portable skill](skills/rca-investigation/SKILL.md). It selects
four workflow stages:

- **Triage:** scope the review, identify evidence gaps and select methods.
- **Investigate:** organise chronology, conflicts, system conditions and barriers.
- **Report:** communicate reviewed evidence, analysis and uncertainty.
- **Track:** turn accepted recommendations into actions and evaluate effectiveness.

Use generated-synthetic placeholders by default. Keep evidence, accounts,
analysis, findings and decisions distinct. Missing or conflicting evidence
must remain visible; completing a report or action does not prove safety
improvement.

## Evidence and compatibility limits

The [client/mode evidence matrix](conductor/tracks/eval-blocker-remediation_20260803/client-mode-evidence-20260831.md)
separates installer tests, package lifecycle, version-specific client trials
and deployment enforcement. Codex's historical 18-trial result is not proof
for another client or version. Cursor, Cline and OpenCode installer contracts
are not actual runtime trials. Four mode contracts do not establish four
validated deployments.

The separate frozen prospective study retained a first-slot token-limit
failure and did not attempt its second slot: zero of two expected observations
were admitted. No scoring or performance result is claimed from that run;
see the [negative evidence receipt](conductor/tracks/eval-blocker-remediation_20260803/prospective-capture-20260831.md).
Historical evaluation and broader repository acceptance remain incomplete.
Recorded OpenAI and Claude directory packets are not submitted or approved
listings; a GitHub release is a separate publication route.

## Privacy, support and authority

Read the [privacy notice](PRIVACY.md), [support boundary](SUPPORT.md),
[security reporting guidance](SECURITY.md) and [full disclaimer](DISCLAIMER.md).
The privacy notice applies to the distributed skills-only packages, not to
every repository tool or the host platform. Do not include private clinical,
patient, consumer, employee, credential or confidential material in public
issues, examples or uploads. Real-data use requires a separately authorised
governed pathway; de-identification is not guaranteed anonymity.

Outputs are not clinical advice, legal advice, policy determinations or
evidence of regulatory, employment, cultural-safety, organisational or
deployment approval. Installation, tests, release and agent review confer no
endorsement or validation by a health service, regulator or client vendor.
Repository engineering uses agent-panel review; historical human-comparator
observations and accountable professional decisions are not replaced by it.
Support is best-effort, with no response-time or availability commitment.

## Repository validation and contribution

For a development checkout with its declared dependencies provisioned, run:

```sh
uv run python -m tools.validate_repository
uv run python -m tools.full_validation
```

These validate repository contracts and fixtures, not clinical effectiveness,
real-world deployment or directory acceptance. See
[CONTRIBUTING.md](CONTRIBUTING.md), the [Conductor index](conductor/index.md)
and [delivery workflow](conductor/workflow.md) for project conventions.
No live model run is required to read this package introduction.

## Licence and release records

Project-authored material is licensed under [Apache-2.0](LICENSE). Third-party
materials retain their own rights; references do not grant redistribution
rights or imply endorsement. Consult [CHANGELOG.md](CHANGELOG.md) and the
exact release receipt. This page adds no terms of service, publisher
verification, new release, hosted website or marketplace submission.
