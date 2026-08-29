# Decision: Use agent panels for repository research review

- **Decision ID:** 20260829-004-agent-panel-research-governance
- **Status:** Approved with conditions
- **Date:** 2026-08-29
- **Owner:** Repository owner
- **Tracks:** benchmark-evaluation-harness_20260731; multimodal-capability-fabric_20260731

## Decision

Approve agent-panel research scoring and conservative non-operational thresholds. Record agent agreement, not human agreement. Do not require independent human reviewers for repository engineering review, synthetic-case scoring, evidence reconciliation, adversarial testing, or research-only recommendations.

## Operating Contract

- Use at least three blind scoring agents and a separate post-submission adjudicator.
- Record reviewer class, role, exact agent revision where exposed, instructions, input and rubric hashes, individual scores, evidence references, uncertainty, abstentions, disagreements, aggregation, correlated-error limitations, and owner disposition.
- Never represent agent-panel output as human agreement, a clinical gold standard, external validation, operational suitability, or organisational approval.
- Privacy, security, clinical-safety, cultural-safety, and harmful-output flags are zero-tolerance and cannot be averaged away.
- A panel recommends `conditional`, `experimental`, `unsupported`, or a bounded research threshold. It does not authorise reserved actions.
- Reuse this standing protocol at subsequent repository checkpoints. Do not request repetitive approvals when the action remains inside this envelope.

## Reserved Authority Boundaries

Agent panels may analyse and recommend but do not establish clinical, legal, policy, regulatory, employment, cultural-safety, organisational, or deployment validation. Those claims remain outside repository completion unless separately authorised by the applicable authority.

The repository owner retains material scope, licence and terms acceptance, paid commitment, credential, rights exception, redistribution, public release or submission, support commitment, and material residual-risk decisions. Real private clinical or employee data remains unauthorised.

## Approved Research Threshold Envelope

- Thresholds are for synthetic, internal regression evidence only.
- All receipts and evidence references must validate.
- Privacy, security, clinical-safety, cultural-safety, and harmful-output hard-gate violations must be zero.
- Panel raw agreement target is at least `0.80`; ordinal agreement target is at least `0.67` where statistically supportable.
- Failure narrows the claim, revises the rubric prospectively, or records the candidate as unsupported. It never weakens a hard gate or retroactively edits scores.
- No comparator is promoted merely because a research threshold passes.

## Owner Authorisation

The owner explicitly approved this decision and directed execution with minimal approval slop or spam on 2026-08-29.
