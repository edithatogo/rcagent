# Client, mode and distribution evidence reconciliation

Scope: dated repository-evidence reconciliation at clean checkpoint `4cd3790`,
activated after PR #103 post-merge Quality `33337488195` and conformance
`33337488240` passed. This adds no model/client execution, portal inspection,
publication, installation or current-upstream compatibility claim. Historical
receipts remain unchanged; their exact versions and limitations still apply.

## Client evidence matrix

Contract validation, installation/discovery, observed model behaviour and
deployment enforcement are separate evidence classes. A manifest is not proof
that a client executed the skill; a local package validator is not a hosted
directory approval.

| Client or profile | Repository/package evidence | Actual behaviour evidence | Supported claim and remaining boundary |
| --- | --- | --- | --- |
| Codex | [Adapter contract](../agent-skills-living-conformance_20260731/evidence/adapters.md); isolated hosted v0.1.1 archive install/discovery/remove in [release receipt](../../archive/distribution-registries-plugins_20260731/evidence/hosted-release-v0.1.1-20260829.md) | [Codex 0.145.0 v4 held-out receipt](../../../evaluations/skills/rca-investigation/runs/codex-0.145.0-20260731-v4-heldout/result.md): revision `5f2f0ca`, 18/18 completed trials, three per case, recorded pass | Evidence supports the tested description, client revision and cases, not current/future Codex or deployed-mode assurance. The earlier one-case [smoke](../agent-skills-living-conformance_20260731/evidence/codex-activation-smoke.md) has missing retained raw-stream/global-discovery limits; it is not the only trial evidence. |
| Claude Code | Same adapter contract; hosted v0.1.1 isolated archive lifecycle; Claude Code 2.1.126 local plugin and marketplace validation in release receipt | Release acceptance records No-LLM trigger/output contracts, not equivalent model trials | Package/lifecycle evidence is bounded to recorded bytes; repeated actual trigger/output trials, `--strict`, hosted screening and catalogue installability are not established by these receipts. |
| Cursor | [Manifest](../../../adapters/cursor/adapter.json) plus isolated unmodified-core installer contract tests | No actual runtime trial established by this bounded review | Static/isolated installer-contract evidence, not actual client execution; do not inherit Codex/Claude hosted archive lifecycle or model evidence. |
| Cline | [Manifest](../../../adapters/cline/adapter.json), optional discovery through `.clinerules`, plus isolated installer contract tests | No actual runtime trial established by this bounded review | Same static/installer boundary; declaration and core validation do not prove client execution. |
| OpenCode | [Manifest](../../../adapters/opencode/adapter.json) plus isolated installer contract tests | No actual runtime trial established by this bounded review | Same static/installer boundary; no arbitrary-client compatibility claim. |
| Gemini | Remediation plan retains client trial/conformance gaps | No passing actual trial established here | Keep unobserved rather than relabelling another client's result. No installation/authentication is authorised by this matrix. |
| Adapter template | [Template](../../../adapters/template/adapter.json) | Not an executable client result | Extension scaffold, not an additional supported runtime. |

The [compliance matrix](../agent-skills-living-conformance_20260731/evidence/compliance-matrix.json)
is a project conformance record, not a current cross-client certification.
Its [output-quality composite](../../../evaluations/skills/rca-investigation/output-quality-result.md)
retains failed v1–v3 evidence and combines later passing cases; it is not an
independent replication across every adapter. This reconciliation does not
re-score those outputs or alter historical assertions.

[Foundation packaging evidence](../../archive/distribution-registries-plugins_20260731/evidence/foundation-and-packaging-20260829.md)
and [current adapter tests](../../../tests/test_skill_adapters.py) establish
isolated installer contracts for all five named adapters. These extra clients
must not be reduced to manifest-only evidence. The Codex 18-trial result file
has SHA-256 `913404262b5fa5737a633c6c9339efdc18ac3113582e092d1289dbd885b16814`;
its full evaluated revision is `5f2f0cabe7faef3114008acd2e42a3f679daa101`.

## Mode evidence matrix

[Track 03 completion](../../archive/privacy-security-assurance_20260731/evidence/completion-receipt-20260829.md)
records deterministic assurance/routing contracts and negative tests, with
review-fix `aa597fe` and merged remediation `ca07cfb`. Its four
[mode runbooks](../../archive/privacy-security-assurance_20260731/evidence/mode-assurance-and-runbooks-20260829.md)
explicitly inherit organisational controls. None is a receipt for every
client-by-mode deployment combination.

| Mode | Evidence available | Not established by that evidence |
| --- | --- | --- |
| Public remote | Public-only routing, explicit disclosure and unknown-state rejection contracts | Current endpoint/telemetry/storage enforcement, permission to disclose private data, or safety of any arbitrary remote client |
| Governed hybrid | Declared de-identification check for sensitive content and compartment keys; authority/transfer requirements in runbooks | Real de-identification effectiveness, organisational transfer authority, deployed keys/stores/logs; no executable authority/transfer field is claimed |
| Fully local | Destination/egress and disclosure contracts; separate frozen study has retained local Unix-socket/process evidence | OS-level network isolation, universal local-runtime enforcement, or successful study admission |
| Air-gapped | No-network/dependency/time/rollback policy and fail-closed rules | Observed physical/OS isolation or a validated air-gapped deployment |

The [failed prospective capture](./prospective-capture-20260831.md) remains
0/2 admitted. Its first-slot token-limit failure and skipped second slot cannot
validate these modes or provide performance/agent-agreement results. The
[scoped readiness fallback](./readiness-addendum-20260831.md) does not close
historical H0–H8/H8P, root #1 or the owning remediation criteria.

## Distribution readiness, not submission

The [dated Track 11 acceptance map](../../archive/distribution-registries-plugins_20260731/evidence/acceptance-map-20260829.md)
and its linked packets are the sources below. No portal or current terms were
checked during this local reconciliation. Release v0.1.1 is recorded at
`af5777bdefa2cb0052ee80c1c5fac9ed972568a4`; its annotated tag is not a
cryptographic signature. Current repository HEAD is not that release.

| Route | Recorded evidence/state | Concrete remaining prerequisite |
| --- | --- | --- |
| GitHub v0.1.1 | Published release, exact asset checksums and downloaded-archive lifecycle verified on 2026-08-29 | Future release is a distinct exact-artifact action; no new release claimed here |
| OpenAI packet | `draft_incomplete_not_submitted`; five synthetic positive and three negative test prompts prepared | Publisher/write access unobserved; logo not prepared; availability not selected; website/support/privacy/terms not hosted in the dated packet; route/terms must be freshly verified before submission |
| Claude packet | `prepared_not_submitted`; local package validation | Team/console access, hosted safety screening and catalogue installation unobserved; `--strict` not established; fresh route verification before submission |
| Agent Skills specification | Interoperability specification in the recorded route assessment | Not a universal submission registry; do not invent a submission requirement |

Local material preparation and externally hosted/access prerequisites must
not be conflated. A repository document is not a deployed website or an
accepted directory listing. Existing approval of public releases/submissions
does not attest publisher verification, legal terms, asset eligibility or
successful submission.

## Existing listing materials and local gaps

The old packet's `not_hosted` values must not be read as absent repository
content. The following files are present in this reviewed checkout:

| Material | Existing source | Remaining boundary |
| --- | --- | --- |
| Privacy notice | [PRIVACY.md](../../../PRIVACY.md) | Applies to skills-only package, not all workbench tools or the host platform; no directory-ready URL or acceptance verified here |
| Support | [SUPPORT.md](../../../SUPPORT.md) | Best-effort public issues with no sensitive content; no response-time or availability promise |
| Security reporting | [SECURITY.md](../../../SECURITY.md) | Private reporting only when available; channel availability was not tested |
| Approval/rights limitations | [DISCLAIMER.md](../../../DISCLAIMER.md) | Retain clinical, policy, legal, organisational and private-data boundaries in any listing |
| Licence/release notes | [LICENSE](../../../LICENSE), [CHANGELOG.md](../../../CHANGELOG.md) | Apache-2.0 is not a substitute for platform terms or third-party rights admission |
| Product introduction | [Conductor product](../../product.md) and canonical skill | Wider workbench aspirations must not become claims about the smaller released package; no root README was found |
| Standalone terms/logo | No project-owned standalone terms page or logo identified in bounded root/material search | Do not borrow vendored branding or invent legal service commitments; a draft is not adopted terms or hosted material |

Candidate file URLs can be prepared from exact source commits later, but this
review does not assert that a directory accepts repository file URLs as its
website/privacy/support/terms fields. No hosted settings, accounts or publisher
identity were inspected or changed.

## Review, validation and next action

Agent acceptance (`root_acceptance_map`) and safety/distribution
(`runtime_security_review`) reviewed this matrix against its bounded sources.
Acceptance passed; safety review clarified declared hybrid checks versus
runbook-only authority/transfer requirements, now corrected above. Review also
preserved extra-adapter installer evidence and existing privacy/support text.
Governance and diff checks pass. `uv run python -m tools.full_validation`
passed with 1,536 tests in 483.27 seconds and 94.56% coverage, plus lint,
types, governance and benchmark checks. Hosted delivery remains separate.
Historical source receipts are not rewritten to fit a pass.

Next useful local route: prepare a bounded public-information landing draft
using the existing product definition, disclaimers, licence and support
mechanisms, and a packet-delta record reusing the material inventory above.
Check what is already present before creating anything;
do not promise support service, adopt legal terms, invent publisher identity,
host pages or submit a packet. Fresh first-party route verification belongs
before selecting a real external submission. Batch genuinely new destination,
authority or access decisions once, after exhausting local preparation.

Repository engineering/review uses agents under standing decisions 001/002.
Historical human-comparator data is not replaced. Clinical, legal, policy,
regulatory, employment, cultural-safety, organisational and deployment
authority remains external. Apache-2.0 and per-artefact rights remain explicit;
no private clinical/employee data or raw model streams enter this document.
