# Implementation Plan: Distribution, Registries, and Client Plugins

**GitHub:** [#16](https://github.com/edithatogo/rcagent/issues/16)

Execution follows [workflow.md](../../workflow.md) and the
[continuous autonomy contract](../../autonomy.md).

## Continuous Execution Contract

- Continue automatically through tasks, phase checkpoints, fresh-context
  review, bounded rework, documentation synchronization, and the next ready
  track.
- Do not ask for routine approval at task, phase, review, or track boundaries.
- If a decision gate is reached, pause only the affected scope, release its
  lane, continue safe independent work, and present options with a
  recommendation, rationale, evidence, trade-offs, reversibility, safe
  default, and dependency impact.
- Use bounded retry, autonomous plan repair, durable resume state, stale-lock
  recovery, and safety circuit breakers from `autonomy.md`.

## Phase 0: Existing-System Fit and Gap Closure

- [x] Task: Establish the system and dependency context (`464e972`; 15 first-party source receipts)
  - [x] Read `integration-strategy.md` and this track's entry in `integration-map.json`
  - [x] Identify the current organisational system, standard, framework, runtime, or platform that already owns each capability
  - [x] Record exact current hosted versions, extension points, licences, maintenance, privacy, telemetry, offline, device, and security constraints
  - [x] Test existing configuration, profiles, APIs, exports, imports, plugins, and adapters against representative fixtures

- [x] Task: Select the smallest adequate intervention (`f310539`)
  - [x] Prefer existing-system configuration or a standards profile
  - [x] Prefer a thin replaceable adapter when translation is the remaining gap
  - [x] Identify generic gaps suitable for an authorised upstream issue or contribution
  - [x] Limit project code to the smallest safety-, privacy-, jurisdiction-, or domain-specific extension
  - [x] Require a fit-gap record and approved ADR before any new subsystem or permanent fork

- [x] Task: Define the dependency lifecycle (`f310539`)
  - [x] Assign each dependency to a locked core, optional adapter, enterprise connector, evaluation, or experimental profile
  - [x] Define contract tests, compatibility windows, drift checks, failure isolation, and safe fallback
  - [x] Give every local shim an upstream reference, owner, expiry or removal condition, and replacement path
  - [x] Confirm `integration-map.json` already records the selected project-owned gap; preserve evidence in the fit-gap record

- [x] Task: Phase Verification & Checkpoint (`464e972`)
  - [x] Verify that no planned work duplicates an adequate existing capability
  - [x] Verify the system-of-record and data-authority boundary
  - [x] Verify the smallest remaining gap and ownership rationale
  - [x] Record the fit-gap receipt and bounded handoff context
  - [x] Continue automatically through the next ready phase, review, bounded rework, and documentation synchronization
  - [x] If an owner gate is reached, create a complete decision packet, pause only the affected scope, release the lane, and continue independent work

## Phase 1: Govern the registry and marketplace funnel

- [x] Task: Implement the phase scope (`464e972`)
  - [x] Create an assessment matrix for specification projects, registries, directories, marketplaces, installers, and community catalogues
  - [x] Record current operator, ownership, verification, security review, licence, terms, telemetry, maintenance, discoverability, versioning, deprecation, and rollback from first-party sources
  - [x] Classify official, first-party, community, experimental, and unsuitable routes
  - [x] Require an owner decision before any public submission

- [x] Task: Validate the phase deliverables (`464e972`; point-in-time and fail-closed)
  - [x] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [x] Verify exact current sources, revisions, licences, assumptions, and unsupported states
  - [x] Record commands, environment, results, limitations, risks, and negative findings
  - [x] Reconcile Conductor state with GitHub issue #16 and dependency evidence

- [x] Task: Phase Verification & Checkpoint (`464e972`)
  - [x] Verify every current hosted-route deliverable against the specification and product safeguards
  - [x] Store a durable phase receipt and bounded handoff context
  - [x] Update dependencies, risks, decisions, and freshness dates
  - [x] Continue automatically when the phase passes and no owner gate is reached
  - [x] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 2: Release the canonical portable skills

- [~] Task: Implement the phase scope (`464e972`; approved GitHub release not yet created)
  - [ ] Publish the portable core and thin client bundles through the approved pinned GitHub release
  - [x] Generate reviewable local manifests for scripted, agent-assisted, offline, update, rollback, and uninstall paths
  - [x] Package self-contained skills from the portable core with complete provenance, compatibility, changelog, and core-only SBOM metadata
  - [x] Test deterministic archive extraction and offline package integrity; hosted GitHub installation remains pending release execution
  - [~] Reuse GitHub releases, checksums, CycloneDX metadata, and hosted integrity tooling; hosted evidence pending release
  - [x] Record no upstream contribution: no generic gap with established fit remained after using current validators and declarative packages
  - [x] Keep public release as an explicit owner-approved action (`20260829-004`)

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #16 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 3: Assess Agent Skills discovery routes

- [x] Task: Implement the phase scope (`464e972`)
  - [x] Track the official Agent Skills specification and examples without assuming a universal official registry
  - [x] Assess GitHub-based installation; do not claim an official universal registry
  - [x] Assess contribution opportunities and retain no upstream contribution where fit is not established
  - [x] Assess community catalogues and fail them closed where ownership and trust are unverified

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #16 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 4: Package for Claude Code

- [x] Task: Implement the phase scope (`464e972`)
  - [x] Create a thin Claude Code plugin and validated self-hosted marketplace candidate
  - [x] Test manifest discovery, isolated installation, update, removal, unsupported-surface exclusion, and portable-core integrity
  - [x] Prepare current official marketplace submission metadata and evidence as not submitted
  - [x] Record owner approval before self-hosted publication or official submission

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #16 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 5: Package for Codex and OpenAI

- [~] Task: Implement the phase scope (`464e972`; hosted listing inputs remain external)
  - [x] Create the current OpenAI skills-only plugin manifest around the portable skill
  - [x] Exclude optional app, MCP, hook, credential, network, telemetry and storage declarations
  - [x] Create positive, negative, trigger, privacy, compatibility, and review contracts under the approved No-LLM evaluation boundary
  - [~] Prepare privacy, terms and support candidates; hosted URLs, logo, publisher and Apps Management access remain absent

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #16 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 6: Prepare the OpenAI universal directory submission

- [~] Task: Implement the phase scope (`464e972`; draft incomplete and not submitted)
  - [x] Validate the package against current OpenAI build and submission guidance
  - [x] Run local structural, lifecycle, trigger and output-contract testing without claiming directory acceptance
  - [x] Assemble reviewer instructions, safety boundaries, data flows, test definitions, limitations, and rollback
  - [x] Record owner approval for publisher verification and submission; credentials/access remain external

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #16 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 7: Assess additional client ecosystems

- [x] Task: Implement the phase scope (`464e972`)
  - [x] Use the existing adapter template and compatibility profile to assess other agent clients
  - [x] Prefer maintained declarative manifests over bespoke client behavior
  - [x] Test safe fallback, no telemetry, privacy boundaries, updates, and removal
  - [x] Add no additional public client claim without evidence and maintenance capacity

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #16 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Phase 8: Operate compatibility and release governance

- [x] Task: Implement the phase scope (`464e972`)
  - [x] Automate fail-closed upstream source and marker drift checks
  - [x] Maintain version authority, provenance, security response, support, update, removal, and rollback procedures
  - [x] Track installation, compatibility, and safety evidence without collecting private content
  - [x] Treat future public releases or submissions as separate external mutations

- [ ] Task: Validate the phase deliverables
  - [ ] Run applicable schema, link, fixture, contract, privacy, safety, and regression checks
  - [ ] Verify exact sources, revisions, licences, assumptions, and unsupported states
  - [ ] Record commands, environment, results, limitations, risks, and negative findings
  - [ ] Reconcile Conductor state with GitHub issue #16 and dependency evidence

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify every deliverable against the specification and product safeguards
  - [ ] Store a durable phase receipt and bounded handoff context
  - [ ] Update dependencies, risks, decisions, and freshness dates
  - [ ] Continue automatically when the phase passes and no owner gate is reached
  - [ ] If an owner gate is reached, apply `decision-needed` and present options, recommendation, rationale, safe default, and impact

## Final Track Verification

- [ ] Task: Complete the track evidence pack
  - [ ] Verify every acceptance criterion has direct evidence
  - [ ] Re-run the complete applicable validation and regression suite
  - [ ] Reconcile local files, Git history, GitHub hierarchy, native dependencies, and receipts
  - [ ] Record unresolved limitations and owner decisions without downgrading them
  - [ ] Close the GitHub issue only after the completion receipt passes

## Review Fixes

- [x] Task: Correct distribution-manifest typing (`7655578`)
  - [x] Make nested manifest metadata explicit to both configured type checkers
  - [x] Re-run Ruff, scoped ty, basedpyright, repository governance, skill validation, and the full test suite
  - [x] Preserve unrelated vendored SourceRight diagnostics outside the Track 11 change scope

- [x] Task: Contain distribution output paths and reconcile overclaimed completion (`a4a2c77`)
  - [x] Reject traversal-capable release identifiers
  - [x] Refuse package output inside the portable source tree
  - [x] Add positive and negative regression tests
  - [x] Return unverified hosted-route, provenance, compatibility, and changelog claims to pending state

- [x] Task: Enforce release disclaimers and public-data boundaries (`b8b2b7a`)
  - [x] Bundle clinical, policy, legal, organisational-approval, privacy, rights, and release-status disclaimers
  - [x] Declare public-only packaging and prohibit private clinical or employee data
  - [x] Declare third-party-controlled content prohibited unless release-specific rights review passes
  - [x] Add package-content and manifest regression tests
