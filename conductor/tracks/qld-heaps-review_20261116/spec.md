# HEAPS profile specification

## Problem and intended outcome

Queensland Health identifies Human Error and Patient Safety (HEAPS) as an incident-analysis approach. rcagent currently mentions its resource index in death-review planning, but has no dedicated executable HEAPS profile. Existing evidence, jurisdiction, participation, reporting and action contracts can support a thin application layer.

The intended initial outcome is one reproducible synthetic review packet with an applicable-source manifest, evidence-linked chronology, separate accounts and analysis, reviewed factors/findings, traceable recommendations, action/effectiveness records and a provenance receipt. Exact source-span and automated reasoning claims depend on the particular qualified upstream components used.

## Users and authority

Review facilitators, patient-safety staff, participating clinicians, consumers and accountable governance reviewers are the intended users of a future authorised deployment. Public engineering uses generated synthetic records. Software supports preparation and review; authorised people retain severity, method-selection, clinical, legal, disclosure, reporting, acceptance and closure decisions.

## Functional requirements

- HEAPS-01: keep jurisdiction, local procedure, review process, analysis scope, analytical tools, commissioning authority and protection status distinct.
- HEAPS-02: bind a versioned HEAPS profile to the existing canonical case ID, schema version, record version and hash. Reference canonical objects; do not duplicate the case.
- HEAPS-03: represent current source status, applicability, rights and exact local-instrument mapping. A public index does not establish access to its linked internal template.
- HEAPS-04: preserve observed facts, accounts, inferences, hypotheses, findings, recommendations and decisions with support, contrary evidence, unknowns and review status.
- HEAPS-05: map factor categories separately from canonical factor function; allow multiple mappings and unmapped factors with rationale.
- HEAPS-06: preserve participant concerns, responses, disagreements and participation status. Never infer consultation or agreement from silence.
- HEAPS-07: connect recommendations to accepted findings or explicitly documented conditions and evidence; require mechanism, accountable owner, resources, dependencies, due-date basis and process/outcome/balancing measures.
- HEAPS-08: bind approval to the whole packet, including core, profile, source snapshots, mapping and rendered output. Material change creates a new revision and stale approval.
- HEAPS-09: retain distinct event, awareness, SAC1 reporting and submission times. Missing trigger dates remain unresolved; changing method does not reset a clock. A local target does not replace a statewide obligation.
- HEAPS-10: distinguish preparation, structural validation, source-support verification, template conformity, human acceptance, external submission and effectiveness. Do not compress them into one complete flag.
- HEAPS-11: consume the accepted AcciMap contract only when an explicit review question warrants it. Preserve graph edge type, uncertainty, evidence and profile identity.
- HEAPS-12: support concurrent death-review and other route questions without treating HEAPS completion as resolution of a separate pathway.
- HEAPS-13: produce a deterministic synthetic packet and inspectable receipt before optional models, extraction or new runtime infrastructure are considered.

## Engineering and content requirements

Follow [product safeguards](../../product-guidelines.md), [workflow](../../workflow.md) and [quality constraints](../../../CONSTRAINTS.md). Use Australian English and original neutral templates. Preserve zero typing debt, privacy and evidence gates. Reuse existing JSON Schema, Python standard-library primitives, pytest and Hypothesis. No new dependency is required by this plan.

The current canonical schema rejects unknown properties. Do not add HEAPS fields to it without coordinated versioning/migration. Current participation and report-view functions are synthetic-only; their admission condition is not changed by a new profile name.

## Interfaces and dependencies

The [contract](./contract.md) defines the proposed profile, packet manifest, bindings and state semantics. [Delivery plan](./delivery-plan.json) records work-package dependencies and capability-specific gates. [Fit-gap](./fit-gap.md) records existing-system reuse and the small project-owned gap.

No hard dependency blocks source/planning work. Track 13 gates only the source-span, extraction, chronology, decision-time or composed capability actually consumed. Track 12 owns scientific suggestions and studies. Track 14 is a partner for overlapping death-review questions, not a prerequisite for nonfatal incidents. AcciMap #139 is optional.

## Acceptance

The initial implementation must execute the positive, negative and revision cases in the [acceptance catalogue](./acceptance-catalogue.json) through the actual public interface, preserve rejection reasons and denominators, and publish an exact-revision receipt. Independent expected results must not be generated by the implementation under test. Repository agent review establishes engineering review only.

Conformity with the current CHHHS instrument requires an authorised blank template/procedure and field-by-field comparison. Operational claims additionally require the applicable data boundary, local authority and a bounded practice evaluation. None is established by synthetic passes.

## Non-goals and open questions

The current H4 increment implements the deterministic synthetic consumer and integrates its H2/H3 prerequisites through an explicitly authorised PR and merge after passing hosted checks. It does not copy official forms, import clinical cases, activate RiskMan, choose a legal protection, alter shared schemas/CI, deploy or release. Optional model studies and automated extraction remain outside this deterministic implementation. H1 source/diagnostic and H3 fixture-design receipts retain their historical scope.

Open questions: current local instrument and rights; exact local roles and approval route; unresolved Queensland guideline date metadata; accepted upstream capability revisions; optional AcciMap interface; coordinator assignment of shared edits and portfolio number. Resolve only the affected scope. Preserve failed evidence and enable safe independent work.
