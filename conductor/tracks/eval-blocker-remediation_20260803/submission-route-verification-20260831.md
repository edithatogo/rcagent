# Submission-route verification — 2026-08-31

Current documentation check from base `35d1fdfb3d103e418317e97db57fb951dd08779d`.
This is preparation, not a submitted draft, vendor approval or publication.
Archived Track 11 packets remain point-in-time records; the
[listing delta](./listing-packet-delta-20260831.md) supplies existing material.

## OpenAI route

The [submission documentation](https://developers.openai.com/plugins/deploy/submission)
was retrieved on 2026-08-31. It explicitly accepts skills-only submissions.
Required preparation includes verified publisher identity, Apps Management
write access, descriptions, logo/category, public website/support/privacy/terms
URLs, final tested skill bundle, starter prompts, five positive and three
negative cases, availability and release notes. Country selection must match
publisher/support/legal readiness. Policy attestations follow verification.
Submission, vendor review, approval and publisher-triggered publication are
distinct states. MCP-specific prerequisites do not apply to this skills-only
candidate. Reuse the exact tested tree; uploading an arbitrary current checkout
would not preserve the release evidence.

The [packaging documentation](https://developers.openai.com/plugins/build/plugins)
identifies `.codex-plugin/plugin.json` and relative component paths; optional
manifest metadata is not equivalent to satisfying public-listing requirements.
No new runtime, MCP server or account is needed merely to prepare the packet.

The public [portal retrieval](https://platform.openai.com/apps-manage) returned
no readable content. No authenticated publisher status was observed. This is
not evidence of denied access, verification failure or an existing submission.
The documentation Markdown endpoints were unavailable to the browsing tool;
the HTML pages above were read instead.

Scoped authenticated-page follow-up by `claude_routes` found no applicable
publisher connector. After the required browser setup/recovery checks,
URL-based selection returned `No browser is available` before navigation.
Neither publisher account was inspected. This is a browser-runtime limitation,
not an account-access denial; no login, session-store read or draft mutation
occurred. The wake condition is an available authenticated browser/connector,
not renewed blanket submission approval.

## Current fit and remaining prerequisites

| Item | Evidence and next action |
|---|---|
| Existing release | Retain v0.1.1 and its exact archive hashes in the [hosted receipt](../../archive/distribution-registries-plugins_20260731/evidence/hosted-release-v0.1.1-20260829.md); do not replace assets. |
| Public information | README, privacy, support, security, disclaimer, licence and changelog exist. Their candidate URLs are recorded in the listing delta; portal acceptance remains unverified. |
| OpenAI draft | The [new reviewer packet](./reviewer-fixtures-20260831.json) supplies five positive and three negative synthetic inputs. Logo, availability, publisher identity/access and a suitable terms URL remain unverified or incomplete. Apache-2.0 is not automatically a vendor-accepted service-terms page. |
| Claude route | See the [current Claude delta](./claude-route-verification-20260831.md). Community review is not curated official endorsement; source-update behaviour requires exact-candidate handling. |
| Local strict validation | Installed Claude 2.1.126 help does not expose `--strict`. Record the version limitation; do not upgrade or mislabel ordinary validation as strict validation. |

## Recommendation and boundary

Continue local packet completeness and historical-guidance repairs under
existing authority. Use generated-synthetic reviewer fixtures only. Keep
submission false until scoped portal access, exact candidate/source handling,
required fields and applicable attestations are established. Do not request
blanket submission or agent-review approval again. No platform terms, legal
facts, country readiness or professional approval can be supplied by an agent
vote. Existing release authority remains intact.

No source case bodies, private evidence, credentials or new third-party assets
were copied. The frozen study remains consumed with 0/2 admitted; no retry,
blinding or scoring occurred. Rollback only these new guidance records, not
historical evidence or release assets.

At `2026-08-31T09:50:51Z`, `claude --version` and
`claude plugin validate --help` confirmed the local version/help limitation.
SHA-256 checks of the existing cached Claude plugin and marketplace ZIPs
matched the hosted receipt (`dcb6113e…1a30e`, `782def8d…54055`). This is cache
identity verification, not a fresh download or strict validation. No client
upgrade or plugin installation occurred.

## Validation and review

Baseline full validation completed: 1,536 tests in 399.56 seconds, 94.56%
coverage. The integrating full run is recorded separately below.

Agent panel roles: `plan_audit` acceptance/evidence reconciliation,
`historical_readiness` privacy/authority, and `claude_routes` route/material
verification. Main integrated and checked OpenAI sources and the complete diff.
Exact model revisions are unavailable; shared context and author overlap limit
independence. All three reviewed their bounded artefacts; the two non-author
agents additionally passed the complete reviewer packet at SHA-256
`10c02970941550d11bc2eba12b83f9e591c88d13c03fb6129a40e660eeb44b15`.
Safety review required explicit selection-versus-admission wording and an
illustrative-directory qualification; both fixes were applied. No unresolved
hard-gate review finding remains in this documentation slice. This is agent
review, not human agreement or professional validation.

JSON parsing and assertions checked all eight IDs, exact preservation of every
archived case field, nonempty input objects, workflow path existence and false
execution/submission state. `git diff v0.1.1 -- skills/rca-investigation` was
empty. These checks do not execute the skill or establish trigger success.
Governance and diff checks passed. Historical case bytes and frozen execution
sources remain unchanged; only historical guidance changed under `evaluation/`.

Validation environment incident: during session 49956, a separate `uv run`
structural check reported interpreter-cache warnings and recreated `.venv`
using CPython 3.14.6. Its fixture assertions passed, but the concurrent full
run is not final clean-environment evidence. It finished with 1,535 passes and
one failed subprocess collection test: the recreated `.venv` lacked pytest
(`test_transport_node_ids_are_bounded`), 414.08 seconds, 94.56% coverage.
No product fix or threshold change is warranted for that environment failure.
An offline locked all-extras environment was created separately at
`/tmp/rcagent-route-validation.PZEpQN/venv` using CPython 3.14.6; its direct
Python invocation of `-m tools.full_validation` is session 64613, log
`/tmp/rcagent-route-isolated-validation.log`. It stopped at basedpyright with
62 errors and 15 warnings while workspace dependency resolution still saw the
incomplete `.venv`; it never reached tests. A separate environment alone does
not isolate the type checker's workspace discovery.

The second bounded recovery restored the original CPython 3.14.5 workspace
environment with `uv sync --offline --locked --all-extras --python 3.14.5`.
The final gate used `.venv/bin/python -m tools.full_validation` directly,
session 88263, log `/tmp/rcagent-route-restored-validation.log`, without
concurrent environment mutation. It passed: 1,536 tests in 697.27 seconds,
94.56% coverage, with lint, types, governance and benchmark checks successful.
Earlier failures remain visible. PR #107 exact-head hosted delivery is pending;
local acceptance completion is not a merged or submitted claim.
