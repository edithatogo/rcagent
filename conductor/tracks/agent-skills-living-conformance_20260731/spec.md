# Specification: Agent Skills Living Conformance and Portable Architecture

**GitHub coordination:** [#5](https://github.com/edithatogo/rcagent/issues/5)

## Overview

Refactor `skills/rca-investigation/` into a self-contained, portable Agent Skill
that continuously conforms to the latest official Agent Skills specification
and applicable creator guidance.

The canonical skill will remain client-neutral. Claude Code, Codex, and future
client-specific behaviour will be implemented through separate adapters that
consume the portable core without duplicating its authoritative domain content.

“100% conformance” means that every applicable item in a versioned compliance
matrix has objective passing evidence. Requirements judged inapplicable must
have an explicit, reviewed rationale.

## Autonomous Execution Requirement

Execution follows [autonomy.md](../../autonomy.md) and
[autonomy.json](../../autonomy.json). Once implementation is authorised, work
continues across tasks, phases, automatic review and rework, documentation
synchronization, and the next ready track without routine confirmation.

Only the affected scope pauses at an owner decision gate. Its request must
present a recommended option first, rationale and evidence, viable
alternatives, trade-offs, reversibility, safe default, paused scope,
continuing work, and dependency impact. Safe independent work continues.

## Integration-First Requirement

This track follows the portfolio
[integration-first strategy](../../integration-strategy.md) and its entry in
[integration-map.json](../../integration-map.json). Before it adds project
code or metadata, it must assess the current standard, official validator,
client contracts, packaging systems, maintained dependencies, and upstream
extension points.

The preferred response to a generic gap is configuration, a standards profile,
a thin adapter, or an authorised upstream contribution. A local compatibility
shim must be isolated, contract-tested, time-limited, and linked to its
removal condition. A new subsystem or permanent fork requires a fit-gap record
and an approved Architecture Decision Record.

## Objectives

1. Achieve complete deterministic compliance with the current Agent Skills specification.
2. Apply all relevant official best-practice guidance.
3. Implement every applicable stable and experimental option through a governed extension model.
4. Make the canonical skill independently portable and installable.
5. Preserve RCA/SAE domain capability, privacy protections, and AU/NZ terminology.
6. Detect and respond to future upstream specification changes.
7. Produce durable validation receipts supporting every conformance claim.

## Authoritative Sources

The implementation must resolve and record the current versions of:

- `https://agentskills.io/specification`
- `https://agentskills.io/skill-creation/best-practices`
- `https://agentskills.io/skill-creation/optimizing-descriptions`
- `https://agentskills.io/skill-creation/evaluating-skills`
- `https://github.com/agentskills/agentskills`
- The official `skills-ref` validator revision used for each validation run

A validation receipt must record retrieval time, source URL, validator commit
SHA, and result. Network failure must be reported as unverified, never treated
as a pass.

## Functional Requirements

### 1. Compliance Matrix

Create a machine-readable and human-readable compliance matrix covering:

- Required directory structure
- `SKILL.md` frontmatter and body constraints
- Name and directory-name equivalence
- Description length and trigger quality
- Stable optional fields
- Experimental fields
- Resource-directory conventions
- Progressive-disclosure guidance
- File-reference integrity
- Portability requirements
- Creator best practices
- Client-adapter compatibility
- Trigger and output-quality evaluations
- Upstream-drift status

Every item must have:

- Requirement identifier
- Source and source revision
- Requirement text or concise paraphrase
- Applicability
- Implementation location
- Validation method
- Current result
- Evidence or receipt path
- Omission rationale where inapplicable

Completion requires 100% of applicable matrix items to pass.

### 2. Canonical Portable Core

The canonical package must:

- Be fully contained within `skills/rca-investigation/`
- Operate without repository-root files
- Resolve every referenced path from the skill root
- Contain all required procedures, references, scripts, and assets
- Avoid assumptions about a particular agent client
- Avoid hard-coded absolute paths
- Remain functional when copied or extracted into an isolated temporary directory
- Preserve a single authoritative copy of each domain workflow

The existing triage, investigation, reporting, and tracking agent instructions
must be migrated into portable workflow resources inside the skill.

### 3. `SKILL.md` Redesign

Refactor `SKILL.md` to provide:

- Valid, concise frontmatter
- An imperative, intent-focused description
- Clear activation and non-activation boundaries
- A deterministic operating-mode selection procedure
- Intake and evidence sufficiency checks
- Privacy, safety, uncertainty, and human-review gates
- Explicit instructions identifying when each reference must be loaded
- A stepwise investigation workflow
- Output selection and validation procedures
- Common gotchas and failure handling
- A final quality-control loop

The main file must remain below the current recommended line and token limits.

### 4. Governed Options and Extensions

Assess and implement every applicable stable and experimental option, including:

- `license`
- `compatibility`
- Namespaced `metadata`
- Experimental `allowed-tools`
- Bundled scripts
- References
- Assets
- Client adapters

Requirements:

- The project owner must approve the licence before it is declared.
- Metadata values must comply with the current schema.
- Compatibility must describe genuine runtime requirements only.
- Experimental fields must have documented client-support evidence.
- Unsupported experimental behaviour must fail safely or be omitted with an explicit applicability rationale.
- `allowed-tools` must not be placed in the portable core unless cross-client tests demonstrate acceptable behaviour.
- Adapter-specific variants may declare supported experimental fields without changing the canonical source.

### 5. Client-Adapter Architecture

Create an adapter layer for at least:

- Claude Code
- Codex

Also provide a documented adapter contract for other clients.

Each adapter must:

- Reference or generate from canonical workflows
- Declare supported and unsupported extensions
- Contain no divergent copy of authoritative RCA content
- Pass path, activation, and representative execution tests
- Degrade safely when a client lacks an experimental feature

### 6. Description and Activation Evaluation

Create realistic trigger evaluation datasets containing:

- Positive prompts
- Near-miss negative prompts
- Explicit and implicit RCA/SAE requests
- Casual and formal phrasing
- Multi-step requests
- Adjacent but out-of-scope clinical, legal, risk, and document-generation requests

Use separate training and held-out validation sets. Run repeated activation
trials and record trigger rates.

Acceptance requires every held-out query to meet its declared positive or
negative threshold. The deterministic evaluation harness and thresholds must
pass completely; raw model nondeterminism must remain visible in the results.

### 7. Output-Quality Evaluation

Add representative evaluation cases for:

- Triage
- Investigation
- Reporting
- CAPA tracking
- Privacy/de-identification
- Evidence insufficiency
- Conflicting evidence
- Jurisdictional uncertainty
- Unsupported client extensions

Validate outputs against explicit assertions covering:

- Correct workflow selection
- Evidence-grounded reasoning
- Systems-focused language
- No invented facts
- Required de-identification
- Appropriate uncertainty
- Correct AU/NZ terminology
- Safe escalation and human-review gates
- Required output structure
- Reference and template integrity

Existing evaluation results must be preserved. The refactor must not claim
improvement without comparable evidence.

### 8. Automated Validation

Provide a deterministic validation command that checks:

- Official `skills-ref` validation
- YAML and metadata constraints
- Directory/name agreement
- Description, line, and token limits
- Internal links and file references
- Missing and orphaned resources
- Isolated-package portability
- Licence and compatibility declarations
- Extension applicability
- Adapter integrity
- Trigger-evaluation schema
- Output-evaluation schema
- Privacy sentinel rules
- Compliance-matrix completeness
- Upstream-drift status

Validation must return non-zero on any applicable failure and provide actionable
diagnostics.

### 9. Living-Conformance Monitoring

Implement an upstream-drift check that:

- Resolves the current official specification and validator revision
- Detects changed fields, constraints, recommendations, or validator behaviour
- Records the checked revisions
- Fails the conformance gate when a normative requirement changes
- Produces an advisory result for non-normative guidance changes
- Never silently substitutes cached evidence for a current check
- Supports a clearly labelled offline mode that cannot produce a current-conformance claim

Document the review and upgrade process for responding to drift.

### 10. Documentation and Evidence

Create and maintain:

- Compliance matrix
- Extension registry
- Portability architecture
- Client-adapter guide
- Migration guide
- Validation guide
- Evaluation methodology
- Upstream-drift policy
- Generated validation receipts
- Changelog entry

All “compliant”, “portable”, and “current” claims must link to supporting evidence.

## Non-Functional Requirements

- Preserve AU/NZ English and clinical-governance terminology.
- Preserve mandatory de-identification safeguards.
- Do not imply legal privilege automatically applies.
- Keep canonical content client-neutral.
- Avoid duplicated sources of truth.
- Make deterministic validation runnable on Windows and a portable CI environment.
- Pin dependencies used for reproducible local execution while resolving current upstream revisions for living-conformance checks.
- Distinguish specification failures, quality failures, network failures, and unsupported-client results.

## Acceptance Criteria

The track is complete only when:

1. The current official `skills-ref` validator passes with zero findings.
2. Every applicable compliance-matrix item passes.
3. Every omission has a documented and reviewed inapplicability rationale.
4. All skill-root references resolve in an isolated copy of the skill.
5. No canonical workflow depends on repository-root `agents/`.
6. Stable optional fields are implemented wherever applicable.
7. Applicable experimental options pass documented compatibility tests.
8. Unsupported experimental options have safe fallbacks and explicit evidence.
9. Claude Code and Codex adapters pass their compatibility suites.
10. Trigger training and held-out validation suites meet all declared thresholds.
11. Output-quality assertions pass without privacy or evidence-integrity failures.
12. Existing evaluation artefacts remain preserved and traceable.
13. Living upstream validation passes against the then-current standard.
14. Offline validation cannot be misrepresented as current upstream conformance.
15. Documentation, migration instructions, and receipts are complete.
16. A clean reviewer can reproduce the validation results from documented commands.
17. No acceptance claim relies solely on checklist state; each claim has durable evidence.

## Out of Scope

- Completing the wider H0–H8 experimental study
- Rewriting all clinical-method references unless validation identifies a relevant defect
- Selecting or changing the project licence without owner approval
- Publishing the skill externally
- Creating credentials or enabling external services
- Claiming universal compatibility with untested clients
- Treating subjective best-practice guidance as a normative specification requirement without an explicit project policy

## Autonomous Execution

Reversible work inside this approved specification proceeds without per-phase
approval when objective verification passes. The track stops for an owner
decision only when required for licensing, public release or submission,
publisher verification, an unevidenced experimental compatibility claim, or
another gate declared in `metadata.json`.

Every decision request must include a recommendation, viable alternatives,
evidence, rationale, trade-offs, reversibility, safe default, and dependency
impact. No external publication or submission is authorised by this plan.
