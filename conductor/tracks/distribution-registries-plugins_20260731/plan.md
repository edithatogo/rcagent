# Implementation Plan: Distribution, Registries, and Client Plugins

**GitHub:** [#16](https://github.com/edithatogo/rcagent/issues/16)

Execution follows [workflow.md](../../workflow.md). Phases continue automatically when objective verification passes and no owner decision gate is reached.

## Phase 1: Govern the registry and marketplace funnel

- [ ] Task: Implement the phase scope
  - [ ] Create a current assessment matrix for specification projects, registries, directories, marketplaces, installers, and community catalogues
  - [ ] Record operator, ownership, verification, security review, licence, terms, telemetry, maintenance, discoverability, versioning, deprecation, and rollback
  - [ ] Classify official, first-party, community, experimental, and unsuitable routes
  - [ ] Require an owner decision before any public submission

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

## Phase 2: Release the canonical portable skills

- [ ] Task: Implement the phase scope
  - [ ] Package self-contained skills from the portable core with licences, checksums, provenance, compatibility, changelog, and SBOM-style metadata
  - [ ] Test clean GitHub installation, archive extraction, offline use, updates, rollback, and uninstallation
  - [ ] Create signed or attestable release evidence where supported
  - [ ] Keep public release as an explicit owner-approved action

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

- [ ] Task: Implement the phase scope
  - [ ] Track the official Agent Skills specification and examples without assuming a universal official registry
  - [ ] Assess GitHub-based installation and current skills.sh or equivalent discovery mechanisms
  - [ ] Assess contribution opportunities to official examples only when contribution policy and fit are clear
  - [ ] Assess community catalogues through supply-chain, ownership, licence, privacy, and maintenance gates

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

- [ ] Task: Implement the phase scope
  - [ ] Create a thin Claude Code plugin with a self-hosted GitHub marketplace manifest
  - [ ] Test plugin discovery, installation, update, removal, activation, unsupported features, and portable-core integrity
  - [ ] Prepare current official marketplace submission metadata and evidence
  - [ ] Require owner approval before self-hosted publication or official submission

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

- [ ] Task: Implement the phase scope
  - [ ] Create the current OpenAI plugin manifest and agents/openai metadata around the portable skill
  - [ ] Add optional app or MCP declarations only when product scope and security evidence require them
  - [ ] Create required positive, negative, trigger, privacy, compatibility, and review tests
  - [ ] Prepare public privacy, terms, support, publisher, website, and production-service evidence only when applicable

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

- [ ] Task: Implement the phase scope
  - [ ] Validate the package against current OpenAI build and submission guidance
  - [ ] Run personal or private testing without claiming directory acceptance
  - [ ] Assemble reviewer instructions, safety boundaries, data flows, test evidence, and rollback
  - [ ] Require owner approval for publisher verification and submission

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

- [ ] Task: Implement the phase scope
  - [ ] Use the adapter template and compatibility profile to assess other agent clients and plugin systems
  - [ ] Prefer maintained frameworks and declarative manifests over bespoke installers
  - [ ] Test capability negotiation, safe fallback, telemetry, privacy, updates, and removal
  - [ ] Add support only when evidence and maintenance capacity exist

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

- [ ] Task: Implement the phase scope
  - [ ] Automate upstream specification, validator, client, marketplace, dependency, and policy drift checks
  - [ ] Maintain version support windows, provenance, security response, deprecation, and rollback procedures
  - [ ] Track installation, compatibility, and safety evidence without collecting private content
  - [ ] Treat every future public release or submission as a new owner decision

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
