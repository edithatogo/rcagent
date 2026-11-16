# Proposed HEAPS profile contract

Status: design input for H3; no implemented schema or official HEAPS template is claimed.

## Core and profile ownership

Keep the canonical case in safety-work v1.1. The HEAPS profile owns process-specific metadata and references. It must not copy chronology, participant accounts, findings or actions into a competing case record.

Proposed profile information:

| Information | Required semantics |
| --- | --- |
| Profile identity | Stable profile ID, explicit version and its own canonical content hash |
| Case binding | Canonical schema version, case ID, record version and exact record hash |
| Applicability | Jurisdiction, HHS/local procedure, review purpose/scope, source references and source status |
| Selection | Human-recorded selection of HEAPS and scope; analytical tools recorded independently |
| People and participation | References to canonical roles/accounts/reviews; incident involvement distinguished from facilitation, independent challenge and approval |
| Factor classification | Versioned taxonomy assignments referencing factor IDs; preserve unmapped/multiply mapped factors and uncertainty |
| Template mapping | Source/version/rights status, field-to-canonical-ID mapping, original/adapted/official distinctions and unresolved gaps |
| Review decisions | Exact reviewer authority and decision references, disputed/unresolved matters, approval status |
| Packet identity | Detached manifest of already computed core, profile, source, mapping and output hashes; final approval references the manifest and is stored separately |
| Delivery | Intended audience, data boundary, output identity and separate external-submission evidence |

A canonical factor's contributory/protective/barrier/system-condition kind is not its HEAPS taxonomy category. Historical domain names do not activate the current official taxonomy. Profile references must resolve to the right entity type and case/revision. A withdrawal or material change invalidates dependent acceptance; never silently repair a stale binding.

## State dimensions and transition evidence

Keep preparation, structural validation, source-support verification, template mapping, authorised review and external submission separate. H3 freezes exact enum values and permitted transitions. The initial state must not imply approval or conformity.

- Prepared evidence may contain explicit unknowns and conflicting accounts.
- Structural validity does not establish factual or causal truth.
- A proposed finding becomes accepted only through a recorded authorised decision at the relevant revision.
- A missing/declined/unavailable participant contribution is not agreement.
- A generated report is not external submission, notification or closure.
- Implementation and effectiveness reuse the canonical action/outcome states; outcome and balancing evidence remain distinct from implementation evidence.

Approvals bind the complete detached packet manifest. Use an acyclic construction order: hash the canonical case and source/mapping artefacts; hash the profile; render and hash the report using the already fixed input identities; then construct and hash the detached manifest. Finally, store the approval separately, bound to that manifest. The profile digest domain excludes manifest and final approval/receipt references. The rendered report must not embed its own hash, the later manifest hash or a later approval. H3 freezes exact encoding, exclusions and any separately generated approval appendix. Each object's own digest field is excluded according to that contract.

Change to a case, material account, finding, procedure snapshot, mapping or report requires a new manifest and fresh review as applicable. Preserve earlier revisions and decisions. Existing canonicalisation sorts object keys but preserves array order: changed canonical array bytes produce a new hash and stale dependent bindings, even when a permitted collection permutation leaves a semantic comparison unchanged.

## Time and source applicability

Separate event time, record/document time and information-availability time where available. Preserve partial ordering and ambiguous precision. Also retain awareness, SAC1 reporting and submission trigger dates independently. Store the applicable obligation ID/revision, calendar basis and local target separately. Missing trigger/calendar evidence yields an unresolved deadline, not an assumed date. Method changes do not reset clocks.

Current incident-management obligations and historical standards applicable at the event time have different roles. A newer policy cannot silently become a standard a clinician was presumed to know earlier. Shared jurisdiction registry remains authoritative for active rules; this track's source inventory is a planning crosswalk.

## Optional AcciMap and death-review composition

Consume the graph contract owned by #139 only after acceptance. A mapping references the canonical case/revision and accepted graph/profile identity; it preserves evidence links, edge type, candidate/accepted status, alternatives and uncertainty. A graph edge is not automatically a causal finding. No duplicate renderer, graph schema or AcciMap fixture estate is created here.

For deaths, share relevant Track 14 records/questions without making review routes mutually exclusive. HEAPS findings do not settle certification, coronial, specialty or statutory questions.

## Initial deterministic interface

H4 will accept bounded, prestructured generated-synthetic inputs using a frozen H3 schema. It will validate, assemble original draft views and emit a receipt with input/component/rule/source/output identities, actual accepted/rejected counts, explicit errors and limitations. It must reject malformed, wrong-case, stale and non-synthetic input through documented outcomes. Empty/all-abstain input must not be presented as a successful completed review.

Two runs with identical admitted inputs and revisions must produce identical deterministic payload bytes. Runtime/timing observations belong in a separate execution receipt. No network, model, RiskMan write or hidden fallback belongs in this initial interface. The coordinator owns any workbench dispatch hook. Exact byte-span validation is added only through accepted D0; existing record hashing must not be relabelled as that capability.

## H1 observed interface constraints

The [H1 receipt](./h1.md) and executable diagnostic pin current shared behaviour. Core fingerprints and interface hashes use different Unicode encodings and notation; calculate and label each from the same admitted payload. The renderer alone does not apply canonical semantic validation, and the locked environment lacks the date-time format checker. Require qualified guards or shared repairs before consuming those guarantees. Existing approval scopes do not include heaps_packet; its mapping remains for receiving agreement, and communication approval must not imply approval of every substantive finding/action. Recommendation records require an explicit canonical mapping and evaluation time. H3 must resolve these boundaries without silently changing shared APIs.
