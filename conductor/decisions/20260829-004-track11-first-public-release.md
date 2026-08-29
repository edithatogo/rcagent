# Decision: Create the First Public Portable-Skill Release

- **Decision ID:** `20260829-004-track11-first-public-release`
- **Status:** Proposed
- **Date raised:** 2026-08-29
- **Owner:** Repository owner
- **Track:** `distribution-registries-plugins_20260731`
- **GitHub issue:** [#16](https://github.com/edithatogo/rcagent/issues/16)
- **Decision needed by:** Before creating any public GitHub release or claiming clean installation from one

## Decision Needed

Decide whether Track 11 may prepare and create the repository's first public
Apache-2.0 portable-skill release after the remaining phase dependencies and
release-specific validation pass. This decision does not authorize a client
marketplace or universal-directory submission.

## Recommendation

**Recommend: Approve a bounded GitHub release after dependency closure.**

Authorize one versioned release only after Tracks 01, 03, 05, and 09 provide
the phase evidence required by Track 11, the exact release commit passes the
complete local and hosted gates, and the dry-run archive, manifest, checksums,
CycloneDX metadata, changelog, rollback plan, and licence are reviewed. Keep
all marketplace and directory submissions as separate decisions.

## Options

| Option | Benefits | Risks and trade-offs | Reversibility | Cost and effort | Dependency impact |
|---|---|---|---|---|---|
| Approve a bounded GitHub release after dependency closure | Enables pinned installation evidence without conflating release and marketplace approval | Creates a durable public artefact and maintenance obligation | Supersession is possible; public history may remain observable | Moderate final validation and hosted release work | Allows the release acceptance lane after Tracks 01, 03, 05, and 09 pass |
| Keep distribution private | Avoids public mutation and support expectations | Track 11 cannot satisfy its pinned-public-release acceptance criterion | Fully reversible local packages remain available | Low | Track 11 remains blocked |
| Approve release and all submissions | Reduces future prompts | Overbroad; current directory, publisher, privacy, support, and compatibility evidence is incomplete | Some public actions are not fully reversible | High | Not acceptable under the current governance contract |

## Evidence and Assumptions

- Track 00 has a passing completion receipt and Apache-2.0 licence decision.
- Commit `66831ec` adds deterministic, offline, review-only packaging with SHA-256 and CycloneDX metadata.
- The package declares `public_release: false` and performs no network or hosting mutation.
- Current client and marketplace requirements must be reverified immediately before any release-adjacent submission.
- Tracks 01, 03, 05, and 09 are phase dependencies for release and client compatibility evidence.

## Privacy, Security, Legal, and Maintenance Impact

The proposed release contains the public portable core and licence only. It
must exclude credentials, private data, internal paths, generated evidence,
and optional runtime dependencies. Approval creates an expectation to address
security issues, provenance drift, deprecation, and supersession for that
release; it does not make clinical, legal, or client-universal claims.

## Safe Default if Deferred

Retain deterministic packages as local review artefacts, do not create a tag
or release, do not upload assets, and make no public installation claim.

## Execution Impact

- **Paused scope:** Public tag/release creation, hosted installation evidence, and Track 11 completion.
- **Work continuing autonomously:** Local packaging, compatibility contracts, negative tests, governance records, and dependency-ready submission materials.
- **Dependency effect:** Track 11 remains in progress until its phase dependencies and this decision pass.
- **Wake condition:** The owner selects an option and all named phase dependencies have passing receipts.

## Response Requested

Respond exactly: `Approve bounded GitHub release after dependency closure`.

## Owner Decision

- **Decision:** Pending
- **Conditions:** Pending
- **Date:** Pending
- **Recorded by:** Pending

## Follow-up

- [ ] Record the decision and conditions in Track 11 metadata and evidence
- [ ] Reverify release and client requirements against first-party sources
- [ ] Build and validate the exact release candidate from its final commit
- [ ] Keep every marketplace or directory submission behind its own decision
