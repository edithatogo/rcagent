# Exact-commit prospective freeze verification

Base: `b10abeb68df1258b3d82beec73aacc790ebce6b2`, merged PR #83.
This checkpoint implements the missing Git byte-consistency check, not an
approved or executable study protocol.

## Contract

`tools.prospective_freeze.verify_freeze(protocol_path, expected_sha256,
commit, root)` first checks the existing strict protocol-candidate contract.
It requires a full commit object identity and the repository's exact root.
The protocol, its five referenced text artefacts and the explicit seven-file
component list must be regular committed blobs whose working bytes match.
Results enumerate paths and SHA-256 digests. Branch names, tree IDs, missing
objects, untracked files, altered/staged bytes, path escapes and symlinks fail.

Git reads use a cleared environment and disable replacement-object lookup and
lazy fetching. No commit, tag, branch, file or remote is written by the checker.
Temporary captured output is bounded on read; this is not a disk quota or
protection against an untrusted Git binary/configuration. Concurrent filesystem
mutation cannot be made atomic by these checks; consuming execution must
recheck the declared inputs and pins immediately before and after its run.

The result `freeze_verified` means exact-commit consistency only. It always
retains `admitted: false` and `study_unlocked: false`. It does not establish
agent review, approval, privacy, loaded interpreter/code identity, runtime
availability, complete transitive dependencies, runner identity or ancestry.
The currently fixed component list must be extended to bind the actual runner,
normaliser and their dependencies before a study can execute. Neither a caller
chosen commit nor internally consistent synthetic fixtures are primary evidence.

## Validation and review

Tests create temporary synthetic Git repositories and preserve the distinction
between matching committed bytes and study admission. They cover changed and
missing files, symlink modes, wrong roots, malformed commits, environment
redirection, replacement objects and changes between protocol reads. No model
is executed by the test suite. Initial fixture import failed before the module
existed; subsequent checks and exact-head hosted results belong to this PR's
validation evidence.

The first full local gate passed 702 tests at 92.95% coverage, and all three
hosted operating-system suites passed. Hosted patch coverage nevertheless
rejected the new module's 88% coverage: several explicit rejection/error paths
had no direct tests. The follow-up adds focused failure-path tests without
changing production behaviour or lowering any coverage threshold.
The expanded 30-test focused suite passed with 100% statement and branch
coverage (73 statements, 26 branches), using an isolated coverage data file.

`protocol_contract_review` implements only the two named source/test files;
the main agent reviews integration, and `root_acceptance_map` performs a
separate read-only review. Exact agent revisions are unavailable, and correlated
errors remain possible. This is agent engineering review, not human agreement
or clinical, legal, policy, regulatory, employment, cultural-safety,
organisational or deployment validation.

## Remaining work and rollback

The [runtime drift record](./runtime-drift-20260830.md) remains an execution
blocker, not an approval request. Prepare a separate explicitly admitted runtime
profile, implement deterministic runner/output extraction, then bind and review
the actual protocol plus all execution components. Add affirmative admission,
blinding, scoring and analysis transitions against actual observations.
Historical H0-H8/H8P and root #1 remain incomplete. Rollback this helper/tests
without altering raw evidence, historic profiles or existing live preflight locks.
