# Context Pack: Server-specific model eligibility

Track `eval-blocker-remediation_20260803`, issue #1; original base `5a782e5`.
PR #88 subsequently passed all seven checks at `eeba35e`, merged as `8918936`,
and its exact tree was verified. Branch `codex/server-model-eligibility` now
integrates that parent while preserving its unique eligibility helper and tests.
No worktree lease is enabled.

## Scope and ownership

Add `tools/prospective_server_model.py` and synthetic tests. Reuse the existing
registry and `local_model_comparator` rights/file validator, but bind only the
separate `darwin_server_v030` profile. Preserve the CLI helper and all historical
receipts. Avoid refactoring pinned imports or accepting arbitrary runtime
profiles. Agent `runtime_profile_tests` owns implementation/tests; main owns
integration and evidence; `root_acceptance_map` reviews acceptance and integrity.

This is the smallest prerequisite for the approved lifecycle adapter: a CLI
eligibility receipt must never identify a server invocation. Retain original
registry identity, selected model identity, all model-class checks, exact server
executable/profile identity, deterministic digest and explicit false study flags.
Reject unsafe roots, registry/runtime/licence/model drift and changes during
checks. No subprocess, socket, download, real model probe or admission transition.

## Inputs, validation and boundaries

Load track spec/plan/metadata, workflow/guidelines, continuation cursor and
decisions 20260829-002 and 20260830-001/002. Bound code context to the server
profile, existing prospective model helper, original comparator validator and
their tests. Parent checks passed; this combined branch requires its own validation.

Use synthetic fixture-first tests, Ruff, both type checkers (including Windows
target), full repository validation and agent-panel review. The project remains
Apache-2.0; component/model rights remain separately checked, with no redistribution.
No client-specific platform guide applies. Scope is read-only eligibility,
not operational validation, process isolation, OS/egress attestation or a freeze.

## Handoff and rollback

Record exact code/test evidence and parent delivery status. Next: bounded server
process lifecycle, fixed structured non-study probe, primary runner, full-component
freeze and affirmative study admission. Remove only these new helper/tests and
their plan entries to roll back; never alter prior evidence or unlock live gates.
