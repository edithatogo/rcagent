# Implementation Plan: Agent Skills Living Conformance and Portable Architecture

**GitHub:** [#5](https://github.com/edithatogo/rcagent/issues/5)

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

- [~] Task: Establish the system and dependency context
  - [ ] Read `integration-strategy.md` and this track's entry in `integration-map.json`
  - [ ] Identify the current organisational system, standard, validator, framework, runtime, or client contract that already owns each capability
  - [ ] Record exact versions, extension points, licences, maintenance, privacy, telemetry, offline, device, and security constraints
  - [ ] Test existing configuration, profiles, APIs, exports, imports, plugins, and adapters against representative fixtures

- [ ] Task: Select the smallest adequate intervention
  - [ ] Prefer existing-system configuration or a standards profile
  - [ ] Prefer a thin replaceable adapter when translation is the remaining gap
  - [ ] Identify generic gaps suitable for an authorised upstream issue or contribution
  - [ ] Limit project code to the smallest safety-, privacy-, jurisdiction-, or domain-specific extension
  - [ ] Require a fit-gap record and approved ADR before any new subsystem or permanent fork

- [ ] Task: Define the dependency lifecycle
  - [ ] Assign each dependency to a locked core, optional adapter, enterprise connector, evaluation, or experimental profile
  - [ ] Define contract tests, compatibility windows, drift checks, failure isolation, and safe fallback
  - [ ] Give every local shim an upstream reference, owner, expiry or removal condition, and replacement path
  - [ ] Update `integration-map.json` with the selected status and evidence links

- [ ] Task: Phase Verification & Checkpoint
  - [ ] Verify that no planned work duplicates an adequate existing capability
  - [ ] Verify the system-of-record and data-authority boundary
  - [ ] Verify the smallest remaining gap and ownership rationale
  - [ ] Record the fit-gap receipt and bounded handoff context
  - [ ] Continue automatically through the next ready phase, review, bounded rework, documentation synchronization, and next ready track
  - [ ] If an owner gate is reached, create a complete decision packet, pause only the affected scope, release the lane, and continue independent work

## Phase 1: Establish the Authoritative Baseline

- [ ] Task: Capture the current Agent Skills standards baseline
  - [ ] Record the current specification URL and retrieval timestamp
  - [ ] Record the official creator-guidance URLs and retrieval timestamps
  - [ ] Resolve and record the current `agentskills/agentskills` revision
  - [ ] Resolve and record the official `skills-ref` validator commit SHA
  - [ ] Store source provenance without copying excessive upstream content

- [ ] Task: Inventory the existing skill package
  - [ ] Enumerate all files under `skills/rca-investigation/`
  - [ ] Enumerate repository-root files currently required by the skill
  - [ ] Map every `SKILL.md` reference to its resolved target
  - [ ] Identify missing, broken, external, duplicated, and orphaned resources
  - [ ] Record current frontmatter fields, limits, and validator result
  - [ ] Record current skill size and progressive-disclosure structure

- [ ] Task: Establish the initial compliance matrix
  - [ ] Add every normative specification requirement
  - [ ] Add applicable official best-practice recommendations
  - [ ] Add stable optional fields
  - [ ] Add experimental fields and extensions
  - [ ] Add portability and client-adapter requirements
  - [ ] Add trigger and output-evaluation requirements
  - [ ] Give every item a stable requirement identifier
  - [ ] Mark applicability without claiming premature compliance

- [ ] Task: Reconcile project documentation with the new technical scope
  - [ ] Identify statements claiming there are no tests, scripts, or CI gates
  - [ ] Draft necessary updates to `conductor/tech-stack.md`
  - [ ] Draft necessary updates to `conductor/workflow.md`
  - [ ] Preserve the content-first quality model
  - [ ] Add deterministic validation expectations for executable tooling

- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)
  - [ ] Verify every baseline source is authoritative and current
  - [ ] Verify no compliance item lacks provenance
  - [ ] Verify no user content or historical evaluation artefact changed
  - [ ] Record the baseline receipt
  - [ ] Continue automatically to Phase 2 unless a declared owner decision gate is reached

## Phase 2: Define Architecture, Contracts, and Failing Fixtures

- [ ] Task: Define the portable-core architecture
  - [ ] Specify the canonical skill-root boundary
  - [ ] Define permitted `SKILL.md`, `references/`, `scripts/`, and `assets/` dependencies
  - [ ] Define the canonical location for triage, investigation, reporting, and tracking workflows
  - [ ] Prohibit repository-root dependencies from the portable core
  - [ ] Define how authoritative domain content avoids duplication
  - [ ] Define isolated-copy and archive-extraction portability tests

- [ ] Task: Define the governed extension model
  - [ ] Create the extension registry schema
  - [ ] Define stable, experimental, supported, unsupported, and inapplicable states
  - [ ] Define required evidence for each state
  - [ ] Define safe fallback behaviour
  - [ ] Define namespacing rules for custom metadata
  - [ ] Define approval requirements for licensing
  - [ ] Define compatibility-test requirements for `allowed-tools`

- [ ] Task: Define client-adapter contracts
  - [ ] Define the common adapter interface
  - [ ] Define the Claude Code adapter contract
  - [ ] Define the Codex adapter contract
  - [ ] Define a template contract for additional clients
  - [ ] Define capability discovery and unsupported-feature handling
  - [ ] Define how adapters consume canonical workflows without copying them
  - [ ] Define adapter conformance receipts

- [ ] Task: Create validation fixtures before validator implementation
  - [ ] Create a known-valid minimal skill fixture
  - [ ] Create invalid-name and directory-mismatch fixtures
  - [ ] Create invalid-description-length fixtures
  - [ ] Create broken and escaping-reference fixtures
  - [ ] Create missing-resource and orphan-resource fixtures
  - [ ] Create malformed metadata fixtures
  - [ ] Create unsupported experimental-field fixtures
  - [ ] Create non-portable absolute-path fixtures
  - [ ] Create offline/current-conformance misrepresentation fixtures
  - [ ] Define the expected result and diagnostic for every fixture

- [ ] Task: Define evaluation schemas and thresholds
  - [ ] Define trigger-query schema
  - [ ] Define training and held-out validation partitions
  - [ ] Define positive and negative trigger thresholds
  - [ ] Define output-quality assertion schema
  - [ ] Define deterministic pass/fail aggregation
  - [ ] Define how model nondeterminism remains visible
  - [ ] Define regression and evidence-retention rules

- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)
  - [ ] Review architecture against the approved specification
  - [ ] Verify every extension has a governed lifecycle
  - [ ] Verify fixtures cover every deterministic failure class
  - [ ] Verify thresholds do not convert unverified results into passes
  - [ ] Continue automatically to Phase 3 unless a declared owner decision gate is reached

## Phase 3: Build the Self-Contained Portable Core

- [ ] Task: Migrate operating-mode workflows into the skill
  - [ ] Move or adapt triage instructions into the portable skill
  - [ ] Move or adapt investigation instructions into the portable skill
  - [ ] Move or adapt reporting instructions into the portable skill
  - [ ] Move or adapt CAPA tracking instructions into the portable skill
  - [ ] Preserve clinically material instructions and safeguards
  - [ ] Replace repository-root path assumptions with skill-root-relative references

- [ ] Task: Normalise resource organisation
  - [ ] Ensure references contain agent-readable documentation
  - [ ] Ensure assets contain static templates and resources
  - [ ] Ensure executable logic is confined to scripts
  - [ ] Reduce unnecessarily deep reference chains
  - [ ] Add explicit routing for conditionally loaded resources
  - [ ] Remove or document orphaned files
  - [ ] Preserve all historically material resources

- [ ] Task: Implement evidence, safety, and privacy gates
  - [ ] Add evidence-sufficiency checks
  - [ ] Add missing and conflicting evidence handling
  - [ ] Add explicit uncertainty requirements
  - [ ] Add de-identification checks
  - [ ] Add human-review and escalation boundaries
  - [ ] Correct any implication that legal privilege applies automatically
  - [ ] Preserve systems-focused and Just Culture language

- [ ] Task: Prove isolated portability
  - [ ] Copy the skill into a clean temporary directory
  - [ ] Validate all references from the copied skill root
  - [ ] Validate packaged archive extraction
  - [ ] Confirm the core does not read repository-root `agents/`
  - [ ] Confirm the core contains no absolute local paths
  - [ ] Record a portability receipt

- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)
  - [ ] Validate content accuracy and AU/NZ terminology
  - [ ] Validate patient and staff placeholders
  - [ ] Validate every cross-reference
  - [ ] Compare migrated workflows against their sources
  - [ ] Confirm no authoritative content was silently lost
  - [ ] Continue automatically to Phase 4 unless a declared owner decision gate is reached

## Phase 4: Refactor `SKILL.md` and Frontmatter

- [ ] Task: Optimise the skill description
  - [ ] Rewrite using imperative, user-intent-focused phrasing
  - [ ] State when the skill should activate
  - [ ] State important near-miss boundaries
  - [ ] Retain relevant AU/NZ RCA and SAE terminology
  - [ ] Keep the description within the current maximum length
  - [ ] Avoid overfitting to individual evaluation prompts

- [ ] Task: Implement applicable stable frontmatter options
  - [ ] Retain a valid name matching the parent directory
  - [ ] Add the approved licence declaration or block completion pending approval
  - [ ] Add an accurate compatibility declaration
  - [ ] Add namespaced metadata with schema-valid string values
  - [ ] Record implementation evidence in the extension registry

- [ ] Task: Implement applicable experimental options
  - [ ] Assess `allowed-tools` against each supported client
  - [ ] Add it only where compatibility evidence passes
  - [ ] Document unsupported-client behaviour
  - [ ] Add safe fallback behaviour
  - [ ] Record omissions as reviewed inapplicability decisions
  - [ ] Prevent experimental options from weakening privacy or review gates

- [ ] Task: Rewrite the body as an executable procedure
  - [ ] Add scope and activation boundaries
  - [ ] Add deterministic operating-mode selection
  - [ ] Add intake and evidence-sufficiency workflow
  - [ ] Add method-selection routing
  - [ ] Add explicit resource-loading triggers
  - [ ] Add output-selection routing
  - [ ] Add validation and correction loop
  - [ ] Add common gotchas and failure handling
  - [ ] Add final privacy, evidence, and quality checklist

- [ ] Task: Enforce progressive-disclosure limits
  - [ ] Measure lines and tokens
  - [ ] Keep only always-needed instructions in `SKILL.md`
  - [ ] Move conditional detail into focused references
  - [ ] Verify every moved resource has a clear load trigger
  - [ ] Verify reference chains remain shallow and navigable

- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)
  - [ ] Run official frontmatter validation
  - [ ] Verify description and naming constraints
  - [ ] Verify all options against the extension registry
  - [ ] Verify the main file remains within current guidance
  - [ ] Complete editorial and clinical-safety review
  - [ ] Continue automatically to Phase 5 unless a declared owner decision gate is reached

## Phase 5: Implement Portable Client Adapters

- [ ] Task: Implement the Claude Code adapter
  - [ ] Map Claude Code activation and agent behaviour to the canonical core
  - [ ] Replace divergent root-level agent content with adapter shims or generated references
  - [ ] Declare supported stable and experimental capabilities
  - [ ] Implement unsupported-feature fallbacks
  - [ ] Add representative activation and execution tests

- [ ] Task: Implement the Codex adapter
  - [ ] Map Codex skill discovery and execution to the canonical core
  - [ ] Declare supported stable and experimental capabilities
  - [ ] Implement unsupported-feature fallbacks
  - [ ] Add representative activation and execution tests
  - [ ] Verify no Codex-only rule leaks into the portable core

- [ ] Task: Provide an additional-client adapter template
  - [ ] Document required adapter metadata
  - [ ] Document workflow linkage
  - [ ] Document capability negotiation
  - [ ] Document compatibility-test expectations
  - [ ] Provide a safe unsupported-client default

- [ ] Task: Verify single-source authority
  - [ ] Detect duplicated canonical workflow text
  - [ ] Confirm adapters reference or derive from canonical resources
  - [ ] Confirm adapter removal does not damage the portable core
  - [ ] Confirm adapter failure does not bypass safety gates

- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)
  - [ ] Run both adapter compatibility suites
  - [ ] Validate client-specific extension declarations
  - [ ] Validate fallbacks
  - [ ] Record adapter receipts
  - [ ] Continue automatically to Phase 6 unless a declared owner decision gate is reached

## Phase 6: Implement Deterministic Conformance Validation

- [ ] Task: Implement the validation command
  - [ ] Run the official `skills-ref` validator
  - [ ] Validate YAML and frontmatter constraints
  - [ ] Validate directory/name agreement
  - [ ] Validate description, line, and token limits
  - [ ] Validate internal links and file references
  - [ ] Validate resource roles and orphan status
  - [ ] Validate portable-core isolation
  - [ ] Validate extension applicability and evidence
  - [ ] Validate adapter integrity
  - [ ] Validate evaluation-data schemas
  - [ ] Validate compliance-matrix completeness
  - [ ] Return non-zero on every applicable failure

- [ ] Task: Implement actionable diagnostics
  - [ ] Identify the failed requirement ID
  - [ ] Identify the affected file and field
  - [ ] Explain the expected constraint
  - [ ] Distinguish errors, unsupported features, advisories, and unavailable upstream evidence
  - [ ] Avoid leaking sensitive content in diagnostic output

- [ ] Task: Run the complete fixture suite
  - [ ] Confirm every valid fixture passes
  - [ ] Confirm every invalid fixture fails
  - [ ] Confirm every failure produces its expected diagnostic
  - [ ] Add regression fixtures for defects found during implementation
  - [ ] Record fixture-suite results

- [ ] Task: Generate durable validation receipts
  - [ ] Record tool and dependency versions
  - [ ] Record source and validator revisions
  - [ ] Record deterministic results
  - [ ] Record network and offline status
  - [ ] Record adapter results
  - [ ] Make receipts reviewable without exposing credentials or sensitive data

- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)
  - [ ] Reproduce validation from documented commands
  - [ ] Confirm all negative fixtures remain negative
  - [ ] Confirm no warnings are represented as passes
  - [ ] Review validation receipts
  - [ ] Continue automatically to Phase 7 unless a declared owner decision gate is reached

## Phase 7: Validate Triggering and Output Quality

- [ ] Task: Build the trigger-evaluation corpus
  - [ ] Add realistic positive prompts
  - [ ] Add near-miss negative prompts
  - [ ] Add explicit and implicit RCA requests
  - [ ] Add casual, formal, terse, and multi-step prompts
  - [ ] Add adjacent clinical, legal, document, risk, and QI requests
  - [ ] De-identify every example
  - [ ] Freeze training and held-out validation partitions

- [ ] Task: Establish the description baseline
  - [ ] Run repeated activation trials on the original description
  - [ ] Record per-query trigger rates
  - [ ] Preserve raw observations
  - [ ] Identify false positives and false negatives

- [ ] Task: Optimise without validation-set leakage
  - [ ] Use only training-set failures for revisions
  - [ ] Run repeated training evaluations
  - [ ] Preserve every tested description
  - [ ] Select candidates based on declared criteria
  - [ ] Evaluate the selected candidate once against the held-out set
  - [ ] Require every held-out query to meet its declared threshold

- [ ] Task: Build and run output-quality evaluations
  - [ ] Test triage
  - [ ] Test investigation
  - [ ] Test reporting
  - [ ] Test CAPA tracking
  - [ ] Test evidence insufficiency
  - [ ] Test conflicting evidence
  - [ ] Test privacy and de-identification
  - [ ] Test jurisdictional uncertainty
  - [ ] Test unsupported extensions and adapters
  - [ ] Record assertion-level results

- [ ] Task: Compare against preserved baselines
  - [ ] Preserve existing study artefacts
  - [ ] Use comparable cases where a comparison is claimed
  - [ ] Report regressions and uncertainty
  - [ ] Do not claim improvement without evidence
  - [ ] Block completion on privacy or evidence-integrity regression

- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)
  - [ ] Verify trigger thresholds
  - [ ] Verify output assertions
  - [ ] Verify train/validation separation
  - [ ] Verify raw nondeterministic results remain visible
  - [ ] Complete clinical-governance review
  - [ ] Continue automatically to Phase 8 unless a declared owner decision gate is reached

## Phase 8: Implement Living-Conformance Monitoring

- [ ] Task: Implement the upstream-drift checker
  - [ ] Resolve current official documentation
  - [ ] Resolve the current official validator revision
  - [ ] Compare fields, constraints, and validator behaviour
  - [ ] Detect normative requirement changes
  - [ ] Detect non-normative guidance changes
  - [ ] Record checked revisions and timestamps

- [ ] Task: Implement honest online and offline modes
  - [ ] Make current-conformance checks require successful upstream resolution
  - [ ] Provide a clearly labelled offline validation mode
  - [ ] Prevent cached evidence from producing a current-conformance claim
  - [ ] Distinguish network failure from specification failure
  - [ ] Preserve the last verified receipt without presenting it as current

- [ ] Task: Integrate validation into project workflows
  - [ ] Add a local validation entry point
  - [ ] Add a portable CI validation entry point
  - [ ] Add a scheduled upstream-drift check
  - [ ] Define failure ownership and remediation workflow
  - [ ] Ensure external service or credential requirements remain gated

- [ ] Task: Validate drift behaviour
  - [ ] Simulate a normative field change
  - [ ] Simulate a guidance-only change
  - [ ] Simulate upstream unavailability
  - [ ] Simulate validator-behaviour change
  - [ ] Verify each condition produces the correct status

- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)
  - [ ] Run a live upstream check
  - [ ] Review the current-conformance receipt
  - [ ] Verify scheduled and local modes agree
  - [ ] Verify offline mode remains honestly labelled
  - [ ] Continue automatically to Phase 9 unless a declared owner decision gate is reached

## Phase 9: Documentation, Migration, and Final Evidence

- [ ] Task: Complete user and maintainer documentation
  - [ ] Document portable-core architecture
  - [ ] Document resource routing and progressive disclosure
  - [ ] Document extension governance
  - [ ] Document client-adapter development
  - [ ] Document validation and evaluation commands
  - [ ] Document upstream-drift response
  - [ ] Document known limitations

- [ ] Task: Complete migration documentation
  - [ ] Map every former repository-root dependency to its new location
  - [ ] Document adapter migration
  - [ ] Document compatibility changes
  - [ ] Document rollback procedure
  - [ ] Confirm historical artefacts remain recoverable

- [ ] Task: Finalise licensing and compatibility
  - [ ] Obtain explicit owner approval for the licence
  - [ ] Add or update the bundled licence file
  - [ ] Verify the frontmatter licence reference
  - [ ] Verify compatibility statements against test evidence
  - [ ] Block release claims if licence approval remains unresolved

- [ ] Task: Execute the final conformance audit
  - [ ] Run the official validator against the current upstream revision
  - [ ] Run deterministic validation
  - [ ] Run isolated portability validation
  - [ ] Run client-adapter suites
  - [ ] Run trigger validation
  - [ ] Run output-quality validation
  - [ ] Run privacy and evidence-integrity checks
  - [ ] Run the upstream-drift check
  - [ ] Require every applicable compliance item to pass

- [ ] Task: Produce the final evidence pack
  - [ ] Generate the final compliance matrix
  - [ ] Generate validation receipts
  - [ ] Generate extension and adapter support matrices
  - [ ] Record unresolved limitations without downgrading them
  - [ ] Link every conformance claim to evidence
  - [ ] Update the changelog

- [ ] Task: Phase Verification & Checkpoint (Refer to workflow.md)
  - [ ] Verify all approved specification acceptance criteria
  - [ ] Confirm no checklist-only claim lacks evidence
  - [ ] Confirm no external publication occurred
  - [ ] Confirm the working tree contains only intended changes
  - [ ] Obtain owner approval for any unresolved licence or external-release decision
  - [ ] Otherwise declare the track complete from the reconciled evidence without an additional approval pause
