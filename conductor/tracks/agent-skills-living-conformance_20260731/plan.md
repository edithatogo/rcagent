# Implementation Plan: Agent Skills Living Conformance and Portable Architecture

**GitHub:** [#5](https://github.com/edithatogo/rcagent/issues/5)

Execution follows [workflow.md](../../workflow.md) and the
[continuous autonomy contract](../../autonomy.md).

## Continuous Execution Contract

> Reconciled 2026-08-11 against merged implementation, deterministic tests,
> current upstream baseline `69ef37e9424c0a7ea9dd2293b559e43ec8176379`,
> and hosted PR #21. `[!]` denotes a real owner or clinical-governance gate;
> unchecked leaf items remain unverified and are not implied complete by nearby
> implementation.

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

- [x] Task: Establish the system and dependency context
  - [x] Read `integration-strategy.md` and this track's entry in `integration-map.json`
  - [x] Identify the current organisational system, standard, validator, framework, runtime, or client contract that already owns each capability
  - [x] Record exact versions, extension points, licences, maintenance, privacy, telemetry, offline, device, and security constraints
  - [x] Test existing configuration, profiles, APIs, exports, imports, plugins, and adapters against representative fixtures

- [x] Task: Select the smallest adequate intervention
  - [x] Prefer existing-system configuration or a standards profile
  - [x] Prefer a thin replaceable adapter when translation is the remaining gap
  - [x] Identify generic gaps suitable for an authorised upstream issue or contribution
  - [x] Limit project code to the smallest safety-, privacy-, jurisdiction-, or domain-specific extension
  - [x] Require a fit-gap record and approved ADR before any new subsystem or permanent fork

- [x] Task: Define the dependency lifecycle
  - [x] Assign each dependency to a locked core, optional adapter, enterprise connector, evaluation, or experimental profile
  - [x] Define contract tests, compatibility windows, drift checks, failure isolation, and safe fallback
  - [x] Give every local shim an upstream reference, owner, expiry or removal condition, and replacement path
  - [x] Update `integration-map.json` with the selected status and evidence links

- [x] Task: Phase Verification & Checkpoint
  - [x] Verify that no planned work duplicates an adequate existing capability
  - [x] Verify the system-of-record and data-authority boundary
  - [x] Verify the smallest remaining gap and ownership rationale
  - [x] Record the fit-gap receipt and bounded handoff context
  - [x] Continue automatically through the next ready phase, review, bounded rework, documentation synchronization, and next ready track
  - [x] If an owner gate is reached, create a complete decision packet, pause only the affected scope, release the lane, and continue independent work

## Phase 1: Establish the Authoritative Baseline

- [x] Task: Capture the current Agent Skills standards baseline
  - [x] Record the current specification URL and retrieval timestamp
  - [x] Record the official creator-guidance URLs and retrieval timestamps
  - [x] Resolve and record the current `agentskills/agentskills` revision
  - [x] Resolve and record the official `skills-ref` validator commit SHA
  - [x] Store source provenance without copying excessive upstream content

- [x] Task: Inventory the existing skill package
  - [x] Enumerate all files under `skills/rca-investigation/`
  - [x] Enumerate repository-root files currently required by the skill
  - [x] Map every `SKILL.md` reference to its resolved target
  - [x] Identify missing, broken, external, duplicated, and orphaned resources
  - [x] Record current frontmatter fields, limits, and validator result
  - [x] Record current skill size and progressive-disclosure structure

- [x] Task: Establish the initial compliance matrix
  - [x] Add every normative specification requirement
  - [x] Add applicable official best-practice recommendations
  - [x] Add stable optional fields
  - [x] Add experimental fields and extensions
  - [x] Add portability and client-adapter requirements
  - [x] Add trigger and output-evaluation requirements
  - [x] Give every item a stable requirement identifier
  - [x] Mark applicability without claiming premature compliance

- [x] Task: Reconcile project documentation with the new technical scope
  - [x] Identify statements claiming there are no tests, scripts, or CI gates
  - [x] Draft necessary updates to `conductor/tech-stack.md`
  - [x] Draft necessary updates to `conductor/workflow.md`
  - [x] Preserve the content-first quality model
  - [x] Add deterministic validation expectations for executable tooling

- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md)
  - [x] Verify every baseline source is authoritative and current
  - [x] Verify no compliance item lacks provenance
  - [x] Verify no user content or historical evaluation artefact changed
  - [x] Record the baseline receipt
  - [x] Continue automatically to Phase 2 unless a declared owner decision gate is reached

## Phase 2: Define Architecture, Contracts, and Failing Fixtures

- [x] Task: Define the portable-core architecture
  - [x] Specify the canonical skill-root boundary
  - [x] Define permitted `SKILL.md`, `references/`, `scripts/`, and `assets/` dependencies
  - [x] Define the canonical location for triage, investigation, reporting, and tracking workflows
  - [x] Prohibit repository-root dependencies from the portable core
  - [x] Define how authoritative domain content avoids duplication
  - [x] Define isolated-copy and archive-extraction portability tests

- [x] Task: Define the governed extension model
  - [x] Create the extension registry schema
  - [x] Define stable, experimental, supported, unsupported, and inapplicable states
  - [x] Define required evidence for each state
  - [x] Define safe fallback behaviour
  - [x] Define namespacing rules for custom metadata
  - [x] Define approval requirements for licensing
  - [x] Define compatibility-test requirements for `allowed-tools`

- [x] Task: Define client-adapter contracts
  - [x] Define the common adapter interface
  - [x] Define the Claude Code adapter contract
  - [x] Define the Codex adapter contract
  - [x] Define a template contract for additional clients
  - [x] Define capability discovery and unsupported-feature handling
  - [x] Define how adapters consume canonical workflows without copying them
  - [x] Define adapter conformance receipts

- [x] Task: Create validation fixtures before validator implementation
  - [x] Create a known-valid minimal skill fixture
  - [x] Create invalid-name and directory-mismatch fixtures
  - [x] Create invalid-description-length fixtures
  - [x] Create broken and escaping-reference fixtures
  - [x] Create missing-resource and orphan-resource fixtures
  - [x] Create malformed metadata fixtures
  - [x] Create unsupported experimental-field fixtures
  - [x] Create non-portable absolute-path fixtures
  - [x] Create offline/current-conformance misrepresentation fixtures
  - [x] Define the expected result and diagnostic for every fixture

- [x] Task: Define evaluation schemas and thresholds
  - [x] Define trigger-query schema
  - [x] Define training and held-out validation partitions
  - [x] Define positive and negative trigger thresholds
  - [x] Define output-quality assertion schema
  - [x] Define deterministic pass/fail aggregation
  - [x] Define how model nondeterminism remains visible
  - [x] Define regression and evidence-retention rules

- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md)
  - [x] Review architecture against the approved specification
  - [x] Verify every extension has a governed lifecycle
  - [x] Verify fixtures cover every deterministic failure class
  - [x] Verify thresholds do not convert unverified results into passes
  - [x] Continue automatically to Phase 3 unless a declared owner decision gate is reached

## Phase 3: Build the Self-Contained Portable Core

- [x] Task: Migrate operating-mode workflows into the skill
  - [x] Move or adapt triage instructions into the portable skill
  - [x] Move or adapt investigation instructions into the portable skill
  - [x] Move or adapt reporting instructions into the portable skill
  - [x] Move or adapt CAPA tracking instructions into the portable skill
  - [x] Preserve clinically material instructions and safeguards
  - [x] Replace repository-root path assumptions with skill-root-relative references

- [x] Task: Normalise resource organisation
  - [x] Ensure references contain agent-readable documentation
  - [x] Ensure assets contain static templates and resources
  - [x] Ensure executable logic is confined to scripts
  - [x] Reduce unnecessarily deep reference chains
  - [x] Add explicit routing for conditionally loaded resources
  - [x] Remove or document orphaned files
  - [x] Preserve all historically material resources

- [x] Task: Implement evidence, safety, and privacy gates
  - [x] Add evidence-sufficiency checks
  - [x] Add missing and conflicting evidence handling
  - [x] Add explicit uncertainty requirements
  - [x] Add de-identification checks
  - [x] Add human-review and escalation boundaries
  - [x] Correct any implication that legal privilege applies automatically
  - [x] Preserve systems-focused and Just Culture language

- [x] Task: Prove isolated portability
  - [x] Copy the skill into a clean temporary directory
  - [x] Validate all references from the copied skill root
  - [x] Validate packaged archive extraction
  - [x] Confirm the core does not read repository-root `agents/`
  - [x] Confirm the core contains no absolute local paths
  - [x] Record a portability receipt

- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md)
  - [x] Validate content accuracy and AU/NZ terminology
  - [x] Validate patient and staff placeholders
  - [x] Validate every cross-reference
  - [x] Compare migrated workflows against their sources
  - [x] Confirm no authoritative content was silently lost
  - [x] Continue automatically to Phase 4 unless a declared owner decision gate is reached

## Phase 4: Refactor `SKILL.md` and Frontmatter

- [x] Task: Optimise the skill description
  - [x] Rewrite using imperative, user-intent-focused phrasing
  - [x] State when the skill should activate
  - [x] State important near-miss boundaries
  - [x] Retain relevant AU/NZ RCA and SAE terminology
  - [x] Keep the description within the current maximum length
  - [x] Avoid overfitting to individual evaluation prompts

- [x] Task: Implement applicable stable frontmatter options
  - [x] Retain a valid name matching the parent directory
  - [x] Add the approved licence declaration or block completion pending approval (`784245f`)
  - [x] Add an accurate compatibility declaration
  - [x] Add namespaced metadata with schema-valid string values
  - [x] Record implementation evidence in the extension registry

- [x] Task: Implement applicable experimental options
  - [x] Assess `allowed-tools` against each supported client
  - [x] Add it only where compatibility evidence passes
  - [x] Document unsupported-client behaviour
  - [x] Add safe fallback behaviour
  - [x] Record omissions as reviewed inapplicability decisions
  - [x] Prevent experimental options from weakening privacy or review gates

- [x] Task: Rewrite the body as an executable procedure
  - [x] Add scope and activation boundaries
  - [x] Add deterministic operating-mode selection
  - [x] Add intake and evidence-sufficiency workflow
  - [x] Add method-selection routing
  - [x] Add explicit resource-loading triggers
  - [x] Add output-selection routing
  - [x] Add validation and correction loop
  - [x] Add common gotchas and failure handling
  - [x] Add final privacy, evidence, and quality checklist

- [x] Task: Enforce progressive-disclosure limits
  - [x] Measure lines and tokens
  - [x] Keep only always-needed instructions in `SKILL.md`
  - [x] Move conditional detail into focused references
  - [x] Verify every moved resource has a clear load trigger
  - [x] Verify reference chains remain shallow and navigable

- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md)
  - [x] Run official frontmatter validation
  - [x] Verify description and naming constraints
  - [x] Verify all options against the extension registry
  - [x] Verify the main file remains within current guidance
  - [x] Complete editorial and clinical-safety review — see `evidence/phase4-editorial-review-20260827.md`
  - [x] Continue automatically to Phase 5 unless a declared owner decision gate is reached

## Phase 5: Implement Portable Client Adapters

- [x] Task: Implement the Claude Code adapter
  - [x] Map Claude Code activation and agent behaviour to the canonical core
  - [x] Replace divergent root-level agent content with adapter shims or generated references
  - [x] Declare supported stable and experimental capabilities
  - [x] Implement unsupported-feature fallbacks
  - [x] Add representative activation and execution tests

- [x] Task: Implement the Codex adapter
  - [x] Map Codex skill discovery and execution to the canonical core
  - [x] Declare supported stable and experimental capabilities
  - [x] Implement unsupported-feature fallbacks
  - [x] Add representative activation and execution tests
  - [x] Verify no Codex-only rule leaks into the portable core

- [x] Task: Provide an additional-client adapter template
  - [x] Document required adapter metadata
  - [x] Document workflow linkage
  - [x] Document capability negotiation
  - [x] Document compatibility-test expectations
  - [x] Provide a safe unsupported-client default

- [x] Task: Verify single-source authority
  - [x] Detect duplicated canonical workflow text
  - [x] Confirm adapters reference or derive from canonical resources
  - [x] Confirm adapter removal does not damage the portable core
  - [x] Confirm adapter failure does not bypass safety gates

- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md)
  - [x] Run both adapter compatibility suites
  - [x] Validate client-specific extension declarations
  - [x] Validate fallbacks
  - [x] Record adapter receipts
  - [x] Continue automatically to Phase 6 unless a declared owner decision gate is reached

## Phase 6: Implement Deterministic Conformance Validation

- [x] Task: Implement the validation command
  - [x] Run the official `skills-ref` validator
  - [x] Validate YAML and frontmatter constraints
  - [x] Validate directory/name agreement
  - [x] Validate description, line, and token limits
  - [x] Validate internal links and file references
  - [x] Validate resource roles and orphan status
  - [x] Validate portable-core isolation
  - [x] Validate extension applicability and evidence
  - [x] Validate adapter integrity
  - [x] Validate evaluation-data schemas
  - [x] Validate compliance-matrix completeness
  - [x] Return non-zero on every applicable failure

- [x] Task: Implement actionable diagnostics
  - [x] Identify the failed requirement ID
  - [x] Identify the affected file and field
  - [x] Explain the expected constraint
  - [x] Distinguish errors, unsupported features, advisories, and unavailable upstream evidence
  - [x] Avoid leaking sensitive content in diagnostic output

- [x] Task: Run the complete fixture suite
  - [x] Confirm every valid fixture passes
  - [x] Confirm every invalid fixture fails
  - [x] Confirm every failure produces its expected diagnostic
  - [x] Add regression fixtures for defects found during implementation
  - [x] Record fixture-suite results

- [x] Task: Generate durable validation receipts
  - [x] Record tool and dependency versions
  - [x] Record source and validator revisions
  - [x] Record deterministic results
  - [x] Record network and offline status
  - [x] Record adapter results
  - [x] Make receipts reviewable without exposing credentials or sensitive data

- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md)
  - [x] Reproduce validation from documented commands
  - [x] Confirm all negative fixtures remain negative
  - [x] Confirm no warnings are represented as passes
  - [x] Review validation receipts
  - [x] Continue automatically to Phase 7 unless a declared owner decision gate is reached

## Phase 7: Validate Triggering and Output Quality

- [x] Task: Build the trigger-evaluation corpus
  - [x] Add realistic positive prompts
  - [x] Add near-miss negative prompts
  - [x] Add explicit and implicit RCA requests
  - [x] Add casual, formal, terse, and multi-step prompts
  - [x] Add adjacent clinical, legal, document, risk, and QI requests
  - [x] De-identify every example
  - [x] Freeze training and held-out validation partitions

- [x] Task: Establish the description baseline
  - [x] Run repeated activation trials on the original description
  - [x] Record per-query trigger rates
  - [x] Preserve raw observations
  - [x] Identify false positives and false negatives

- [x] Task: Optimise without validation-set leakage
  - [x] Use only training-set failures for revisions
  - [x] Run repeated training evaluations
  - [x] Preserve every tested description
  - [x] Select candidates based on declared criteria
  - [x] Evaluate the selected candidate once against the held-out set
  - [x] Require every held-out query to meet its declared threshold

- [x] Task: Build and run output-quality evaluations
  - [x] Test triage
  - [x] Test investigation
  - [x] Test reporting
  - [x] Test CAPA tracking
  - [x] Test evidence insufficiency
  - [x] Test conflicting evidence
  - [x] Test privacy and de-identification
  - [x] Test jurisdictional uncertainty
  - [x] Test unsupported extensions and adapters
  - [x] Record assertion-level results

- [x] Task: Compare against preserved baselines
  - [x] Preserve existing study artefacts
  - [x] Use comparable cases where a comparison is claimed
  - [x] Report regressions and uncertainty
  - [x] Do not claim improvement without evidence
  - [x] Block completion on privacy or evidence-integrity regression

- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md)
  - [x] Verify trigger thresholds
  - [x] Verify output assertions
  - [x] Verify train/validation separation
  - [x] Verify raw nondeterministic results remain visible
  - [x] Complete clinical-governance review — see `evidence/phase7-clinical-governance-review-20260829.md`
  - [x] Continue automatically to Phase 8 unless a declared owner decision gate is reached

## Phase 8: Implement Living-Conformance Monitoring

- [x] Task: Implement the upstream-drift checker
  - [x] Resolve current official documentation
  - [x] Resolve the current official validator revision
  - [x] Compare fields, constraints, and validator behaviour
  - [x] Detect normative requirement changes
  - [x] Detect non-normative guidance changes
  - [x] Record checked revisions and timestamps

- [x] Task: Implement honest online and offline modes
  - [x] Make current-conformance checks require successful upstream resolution
  - [x] Provide a clearly labelled offline validation mode
  - [x] Prevent cached evidence from producing a current-conformance claim
  - [x] Distinguish network failure from specification failure
  - [x] Preserve the last verified receipt without presenting it as current

- [x] Task: Integrate validation into project workflows
  - [x] Add a local validation entry point
  - [x] Add a portable CI validation entry point
  - [x] Add a scheduled upstream-drift check
  - [x] Define failure ownership and remediation workflow
  - [x] Ensure external service or credential requirements remain gated

- [x] Task: Validate drift behaviour
  - [x] Simulate a normative field change
  - [x] Simulate a guidance-only change
  - [x] Simulate upstream unavailability
  - [x] Simulate validator-behaviour change
  - [x] Verify each condition produces the correct status

- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md)
  - [x] Run a live upstream check
  - [x] Review the current-conformance receipt
  - [x] Verify scheduled and local modes agree
  - [x] Verify offline mode remains honestly labelled
  - [x] Continue automatically to Phase 9 unless a declared owner decision gate is reached

## Phase 9: Documentation, Migration, and Final Evidence

- [x] Task: Complete user and maintainer documentation
  - [x] Document portable-core architecture
  - [x] Document resource routing and progressive disclosure
  - [x] Document extension governance
  - [x] Document client-adapter development
  - [x] Document validation and evaluation commands
  - [x] Document upstream-drift response
  - [x] Document known limitations

- [x] Task: Complete migration documentation
  - [x] Map every former repository-root dependency to its new location
  - [x] Document adapter migration
  - [x] Document compatibility changes
  - [x] Document rollback procedure
  - [x] Confirm historical artefacts remain recoverable

- [x] Task: Finalise licensing and compatibility
  - [x] Obtain explicit owner approval for the licence
  - [x] Add or update the bundled licence file (`784245f`)
  - [x] Verify the frontmatter licence reference
  - [x] Verify compatibility statements against test evidence
  - [x] Block release claims if licence approval remains unresolved

- [x] Task: Execute the final conformance audit
  - [x] Run the official validator against the current upstream revision
  - [x] Run deterministic validation
  - [x] Run isolated portability validation
  - [x] Run client-adapter suites
  - [x] Run trigger validation
  - [x] Run output-quality validation
  - [x] Run privacy and evidence-integrity checks
  - [x] Run the upstream-drift check
  - [x] Require every applicable compliance item to pass

- [x] Task: Produce the final evidence pack
  - [x] Generate the final compliance matrix
  - [x] Generate validation receipts
  - [x] Generate extension and adapter support matrices
  - [x] Record unresolved limitations without downgrading them
  - [x] Link every conformance claim to evidence
  - [x] Update the changelog

- [x] Task: Phase Verification & Checkpoint (Refer to workflow.md)
  - [x] Verify all approved specification acceptance criteria
  - [x] Confirm no checklist-only claim lacks evidence
  - [x] Confirm no external publication occurred
  - [x] Confirm the working tree contains only intended changes
  - [x] Obtain owner approval for the licence; retain external release as a separate gate
  - [x] Otherwise declare the track complete from the reconciled evidence without an additional approval pause
