# Planning evidence

Historical P0 receipt at published commit 3bd2061cc8508fed374f98e4281ea53c190385ec. Hashes and completed checks below refer to that planning snapshot, not subsequent H1 edits. Current H1 evidence is recorded in [h1.md](./h1.md) and [h1-review.md](./h1-review.md).

## Scope and identity

User-authorised deliverable: incorporate the HEAPS recommendations into Conductor and report tracks/order. Base master: c6892497aa0b03555d5145242c04965471eccc1d. Issue: [#140](https://github.com/edithatogo/rcagent/issues/140). Branch: docs/qld-heaps-conductor-20261116. This increment changes only conductor/tracks/qld-heaps-review_20261116/**.

Planning checks and two agent reviews passed with the documented findings corrected. The repository remains unmerged from this lane; shared registration and portfolio numbering are pending coordinator integration. The PR supplies the published commit and hosted status; this local receipt does not claim a hosted pass.

## Executed validation

| Check | Result and boundary |
| --- | --- |
| python -m tools.validate_repository | Passed repository governance validation. This does not independently validate every semantic contract in an unregistered proposed track. |
| Inline standard-library planning validation | Passed UTF-8/JSON/JSONL parsing, local Markdown path resolution, unique work-package/case IDs, acyclic dependency graph, H2/H3 parallel entry and H4 join, H6.1 preparation entry, absence of new hard dependencies, unassigned number and unexecuted acceptance states. |
| Source inventory validation | Two canonical source references resolve; five supplementary IDs are unique. No active second authority registry, copied official template or fabricated source hash. |
| git diff --cached --check | Passed whitespace/error check for the dedicated track. |
| Scope inspection | Only the dedicated HEAPS track is changed; no runtime, shared registry/schema/method, CI, dependency, AcciMap or D0 source edits. |
| Independent agent review | Two scoped reviewers; P2/P3/low findings corrected and narrowly re-reviewed. See review.md for exact reviewed bytes and limits. |

Final design contains six work packages and 25 acceptance cases. These cases are specifications, not executed tests. H1-H6 implementation remains pending. Full runtime suite, model runs, real-case processing, official-template conformity, clinical validation and operational deployment are not claimed.

## Reproduction

From the checkout root run python -m tools.validate_repository and git diff --check. Parse every JSON document in this track and every line of evidence.jsonl. Check relative Markdown links from their containing file. For delivery-plan.json, require unique H1-H6 IDs, resolve every depends_on edge and reject cycles; require H2/H3 depend on H1 and H4 on both, with H6.1 preparation after H1. Require empty hard_dependencies and an unassigned proposal number. For acceptance-catalogue.json require unique HP01-HP25 IDs and all execution_status values not_run. Resolve sources.json authority_source_references against the existing canonical jurisdiction registry. Review content and live ownership separately; structural checks do not establish authority or truth.

## Final planning-content identities

The following are SHA-256 hashes of the final substantive and administrative planning inputs. Evidence/review receipts are excluded from this manifest to avoid self-reference. The publication commit binds the entire directory.

| File | SHA-256 |
| --- | --- |
| index.md | f82ce192904ec37dc6f439ca9abe10df99103ecbf6fa358b2761e2581c2b5c49 |
| spec.md | 1dfc54050297f37694ba984be243779ab6e49ee3322046ae6fd7aff017e12e23 |
| plan.md | 5d7a104f8c5b591a3816dd8788888eac7c25cda04cf7e6155538bf44af333944 |
| metadata.json | b3e64da29c01011dfebaf5af90b6e95d25cbc160de0fbed9e9bf4f248b20a006 |
| implementation-order.md | 3919afe64a3e34c53693e325d55ba5e83c2452559c7efba0351043c416a7b65e |
| delivery-plan.json | 613cf03621c42d44016fd0bfbba64bf5e3cbf1f4c91ae49e2a3f6b286a4b57ff |
| contract.md | 90907174f5a2d4df8dcc9b49a017faaa0f94160ab4a15b7efc5e59b527dbab63 |
| fit-gap.md | cb86c1788f4d0611e0d436842e7177f9451db09281f6eda09f49a1808bd77cca |
| acceptance-catalogue.json | c6881b817a94a3017306ab5bdc2d042b3d366d6236e090c59c762b7a5b8773a5 |
| context-pack.md | 0e6b4edd3a41d41db67599e06d823fc5003aa90086993696aca937bdc084c4e1 |
| integration-handoff.md | baf270ea6398d7be2215a13ea08b12762d196bb67bcf3f1822872eb45d45005e |
| registration-proposal.json | dac951039cf8fa5b023a1a0a57875ca5821ea044d8716a5b61066663cb8044fe |
| source-map.md | cec8454b8925a22278b7fdb893dfe70fb314ee493057b2727a4797abcb37c5fb |
| sources.json | 5cb5411dd121a80359491b21c632a7c8204ebd06509bb924d53bf23543aa43fa |

Generated evidence timestamp: 2026-11-16T07:37:57+00:00.

## Hosted privacy-check remediation

The first published draft, commit 1b2a19efa1cbe5260381ca25d1dc624500f6cd5b, triggered one Gitleaks generic-api-key finding at sources.json line 6 in [privacy job 133157697057](https://github.com/edithatogo/rcagent/actions/runs/43825326396/job/133157697057). The flagged value was the public timezone identifier Australia/Brisbane. Renamed its metadata field from access_timezone to timezone; the value, source interpretation and access restrictions are unchanged. No scanner configuration, allowlist, workflow or detection rule was changed. The isolated single-commit draft will be replaced against its unchanged base so the commit-range scanner receives the corrected planning addition. This does not rewrite master or another owner's branch.

The current input-manifest digest is c67ac7efb364c3bb0b2d078eb3ad847ae34807e8c6f905a3bf09043a8d814d5f. Reproduce it by sorting the 14 filenames in the table, emitting each SHA-256 followed by two spaces, the filename and LF, then hashing the UTF-8 concatenation. Earlier evidence events retain their historical identities; the latest metadata-remediation event identifies these current inputs. Hosted checks on the replacement commit remain separate and are reported in the PR.
