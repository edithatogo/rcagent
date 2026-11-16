# H1 checkpoint review and verification

## Disposition

The bounded H1 public-source refresh, interface appraisal and engineering checkpoint are complete. H1.3 receiving agreement and H1.4 shared registration/allocation remain pending. The two unresolved component findings, four unsafe-admission observations and failed full local gate are retained; no H1 phase acceptance, H2/H3 readiness, HEAPS runtime qualification or merge is claimed.

This increment is relative to HEAPS planning commit 3bd2061cc8508fed374f98e4281ea53c190385ec and shared-source master c6892497aa0b03555d5145242c04965471eccc1d. The publication commit binds the final files. H1 owns only this dedicated track.

## Review panel

| Reviewer | Scope and execution | Disposition |
| --- | --- | --- |
| /root/proposal_review | Independent checkpoint review of current changes, source applicability, scope/rights/ownership and actual locked diagnostic execution; separately retrieved primary policy and discovery pages. | No new blocking increment finding. Reproduced all 13 controls and byte-identical diagnostic output after remediation. Existing renderer and timestamp defects remain P2 component findings. |
| /root/repo_heaps_mapping | Earlier interface appraisal, followed by a separate review of the root-authored consumer proposal and diagnostic; actual locked subprocess and comparison with stored observation. | No blocking increment finding. Low wording finding about literal approval digests corrected and narrowly re-reviewed; same 13/9/4 result. Not independent of its own earlier interface appraisal and not a fresh source-policy review. |
| /root/heaps_guidance | Public-source research and subsequent source-specialist consistency check of H1, inventory and crosswalk. | No source-accuracy correction. Author checking is not counted as independent source corroboration or engineering acceptance. |

These are agent reviews with shared conversation context and possible correlated errors. They are not clinical, cultural, legal or organisational authority, coordinator receiving agreement, current-template conformity or a human-comparator study.

## Executed checks

The unchanged lock was installed with `uv sync --locked --extra validate --extra test --extra lint --extra assurance`; uv 0.13.6 selected CPython 3.15.2. A cache hardlink warning caused ordinary file-copy fallback; dependency resolution succeeded without a manifest or lock change.

| Command or check | Actual result |
| --- | --- |
| `uv run --no-sync python conductor/tracks/qld-heaps-review_20261116/h1_interface_probe.py` | Exit 2: 13 controls, 9 expectations met, 4 unmet. Both reviewers independently reproduced the output. This is negative interface evidence, not a passing HEAPS suite. |
| Explicit Ruff check and format check on the H1 diagnostic | Passed. |
| Explicit `basedpyright` on the H1 diagnostic | Final result: 0 errors, 0 warnings, 0 notes. Initial empty-list inference error corrected with precise tuple/object annotations; no ignore, baseline or allowance added. |
| Explicit `ty check` and Bandit on the H1 diagnostic | Passed. |
| `uv run --no-sync pytest -q tests/test_evidence_core.py tests/test_interface_actions.py tests/test_jurisdiction_pack.py tests/test_template_admission.py` | 215 passed. These existing regressions do not include the new unmet expectations. |
| `uv run --no-sync python -m tools.validate_repository` | Passed repository governance checks; unregistered-track semantic checks are recorded separately. |
| `uv run --no-sync python -m tools.full_validation` | **Failed, exit 1:** 2,182 passed, 53 failed, 11 skipped; measured branch coverage 93.27%. Earlier lint, format, ty, strict basedpyright/zero baseline, security, dead-code, invisible-character, governance and seven-case benchmark stages passed. |
| Historical source test after retrieving its missing commit | 1 passed; see explanation below. The original full-run failure remains recorded. |
| Track structural checks | Six JSON documents and JSONL parse; 45 relative links resolved at the initial check; six-node dependency graph acyclic; source references valid; 13 diagnostic outcomes/counts and ten component hashes reconcile; no new hard dependency. |
| Historical receipt check | All 14 P0 input hashes match their actual bytes at 3bd2061; they are not relabelled as H1 hashes. |
| Diff/ownership | Only the dedicated HEAPS track changed. No shared code/schema/registry, dependency, CI, other owner or historical study mutation. Whitespace checks passed. |

No full-suite result is upgraded from a focused rerun. Hosted checks must be assessed on the exact newly published head; the successful P0 head does not qualify H1 by inheritance. The diagnostic is separate from all 25 HP01–HP25 designs, which remain unexecuted. No model or real case was run.

## Full local gate limitations

The failed run contained 52 failures in existing Unix-socket/session/controller groups and one historical-source lookup failure in `test_actual_protocol_references_and_declared_condition_remain_consistent`. Direct construction of `socket(AF_UNIX, SOCK_STREAM)` independently raised `PermissionError: [Errno 1] Operation not permitted`. This is evidence of the local socket restriction; it is not a substitute for executing the groups successfully on a suitable runner.

The history lookup failed because the earlier shallow checkout lacked e6c1453d68b562829b99f40b925de6d287496601. Fetching that exact public commit restored the required Git object. Re-running only that test with the unchanged sources passed (1 passed). No historical declaration or expected result changed. The whole suite was not rerun after that repair, so the recorded 2,182/53/11 result remains the complete-run observation.

The raw full-run log is an execution-local intermediate; its SHA-256 is 13ec020c4ecd8b85012ae9d2b1320b31d2d804a27c152b6a1b3e916bfd30ca63. The command, group counts, diagnostics and limitations above are the durable summary. No test was disabled and no gate was weakened. The unrelated local execution restriction does not resolve the H1 renderer/date-time findings.

## Review remediation

The approval controls compare literal synthetic digests, not a computed detached manifest. H1 now says a declaration matches the supplied digest and expressly withholds end-to-end packet approval. A strict typing finding on the empty expected-error list was fixed with a typed tuple and `JsonObject`; two independent reruns showed unchanged output. These are the final diagnostic bytes below.

A development-only transition control initially used an invalid enum value and was rejected at schema level. It was corrected to a legal pair of states with an invalid transition. The duplicate control was also isolated by appending a source while preserving all referenced IDs. The final diagnostic correctly exposes the distinct semantic boundary without weakening its expected rejection.

## Exact checkpoint-reviewed identities

The following identities were returned by the independent checkpoint reviewer after substantive remediation. Later administrative changes recorded completed review/blocked-state dispositions, appended the shared-interface intake already described in H1 and wrote this receipt. They do not relabel the earlier review bytes as later bytes.

| File | SHA-256 at checkpoint review |
| --- | --- |
| h1.md | 381972833eea8122f9b3f5293aed8f5f38f3b7fee61f56ff97b1df5e915cd170 |
| h1_interface_probe.py | 55d3e00cf42024a05d66f62ecab524620406238de8cdeab857a27c20641e1404 |
| h1-interface-observation.json | 104aa9b89bf1c1271720027c6c104dca7dca3d886342fbcbd290cf7be38c8e07 |
| contract.md | e50a1a92c161df096a96213b4f528861b0a8644d2f09e2f75b8aa8aa660cad9e |
| plan.md | e9623dfcf2fe8f91b89f698375fc92c26d99617921d32d327ca1b42bdf8b0226 |
| delivery-plan.json | 7a575b4dc2637caa14e3f05e3997ea01c3c37ba8f88830b9114df4545a94fba1 |
| metadata.json | d3c2f648a1b7841a6416b9b5656bcf46e6528f7be1c59559aafca0dcce684bf5 |
| sources.json | 4aa67a1e1adea513538162dacf8d7042f693ec1966c069378de24e54a0c4eb87 |
| source-map.md | a8eeb3a151f81e527cf71471e552eaf8078e6751e90db3f3c03131782d46e913 |
| context-pack.md | 207447f2be07ac3664d14258b9be838a05e1aa1ba37205b1741fcb28585544d6 |
| integration-handoff.md | 97aacb4ef8a14ee4382c18637505c045ac1f2eb096f0877cb78e2cdbfb16cc13 |

## Final H1 input identities

This manifest includes the final inputs and administrative state. It excludes this receipt and evidence.jsonl to avoid self-reference. Reproduce the digest by sorting the filenames, writing each SHA-256, two spaces, filename and LF, then SHA-256 hashing the UTF-8 concatenation.

Manifest SHA-256: c7a3296f5ea6f4e23132032fe965fcaeda3996fd0118a4156ca97a32d774a9a8

| File | Final SHA-256 |
| --- | --- |
| acceptance-catalogue.json | c6881b817a94a3017306ab5bdc2d042b3d366d6236e090c59c762b7a5b8773a5 |
| context-pack.md | 14173f5ad508cbc3df796e666d780121e40a2fd226e0a5fc6805b23209caf8d6 |
| contract.md | e50a1a92c161df096a96213b4f528861b0a8644d2f09e2f75b8aa8aa660cad9e |
| delivery-plan.json | 3e317643e52909012405a4325a8d161b83257a311a14bbcf74c7f25ca05c1cd1 |
| fit-gap.md | f846b68e480ba9df68072c1465c5b4f2ab9428d5caecacc85b247b1ccde9a37e |
| h1-interface-observation.json | 104aa9b89bf1c1271720027c6c104dca7dca3d886342fbcbd290cf7be38c8e07 |
| h1.md | 035cf6d0b80806900b595609813e71205d60e6bfc25d8942bbbad165ee440716 |
| h1_interface_probe.py | 55d3e00cf42024a05d66f62ecab524620406238de8cdeab857a27c20641e1404 |
| implementation-order.md | 3919afe64a3e34c53693e325d55ba5e83c2452559c7efba0351043c416a7b65e |
| index.md | db790498b088ed67c03a4a21b008ce1cb3ff7a5400f258e3d427e0a9ae91edca |
| integration-handoff.md | 97aacb4ef8a14ee4382c18637505c045ac1f2eb096f0877cb78e2cdbfb16cc13 |
| metadata.json | 524dc863767bd1b779b7a1172509677b8d57060bffcf93fcde28b0cc557a39d7 |
| plan.md | 710e501891cad7dbce668ac828ce66ec09fa3dc525e0b99bb761a9d3ec09fcff |
| planning-evidence.md | b55ad8ffc787d5bff4c032ddbc6b4fcfd51a4a66b4b5dc7b27af4b6c80fcd379 |
| registration-proposal.json | 2259b07f1a2ec93a173c3462084ee5d5b0e7c7dda2dcd9070f65652849997070 |
| review.md | d3b834f3c4643d7fb2dfa138299a9c12eab3c1c5132f066f5efd3c4531b1b00f |
| source-map.md | a8eeb3a151f81e527cf71471e552eaf8078e6751e90db3f3c03131782d46e913 |
| sources.json | 4aa67a1e1adea513538162dacf8d7042f693ec1966c069378de24e54a0c4eb87 |
| spec.md | bcfe8e514d9d42e48fc19d63af3dad860b102f75949d8adee45e5f0f62c8307a |

## Resume and rollback

The [H1 receiving request](./h1.md) and [coordinator handoff](./integration-handoff.md) identify the exact unresolved agreements and shared repairs. No new routine user approval is requested. The existing coordinator must record receiving scope and allocate paths before H2/H3 can claim readiness. Revert only this H1 increment to withdraw it; preserve P0 and historical negative evidence.
