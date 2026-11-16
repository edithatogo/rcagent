# HEAPS review preparation

Use this original Human Error and Patient Safety (HEAPS) preparation profile
across **triage, investigate, report and track**. It helps a reviewer organise
evidence, questions and proposed improvements. The initial implementation scope
is generated-synthetic, non-operational work. It is not a Queensland Health
issued form, a qualified clinical review or a submission to an incident system.

Apply the verified jurisdictional requirements and authorised local process
before repository method heuristics. Record the person's method-selection
decision and its source; a Severity Assessment Code (SAC), an adverse outcome
or the word HEAPS does not select the review process automatically. Record
analytical tools separately from that process. A local target cannot relax an
applicable statewide obligation.

Use the [original draft outline](../../assets/templates/markdown/15-heaps-review-draft.md)
and [template use contract](../../assets/template-use-contract.md). Their
headings are working aids, not verified official HEAPS fields. General
[investigation quality checks](../investigation-quality-checklist.md) still
apply.

## Contents

- [Source and authority boundary](#source-and-authority-boundary)
- [Triage](#triage-establish-the-review-and-its-unanswered-questions)
- [Investigate](#investigate-preserve-evidence-perspectives-and-alternatives)
- [Report](#report-produce-an-original-draft-for-a-defined-audience)
- [Track](#track-connect-proposed-improvements-to-evidence-of-effect)
- [Canonical mapping](#canonical-mapping-for-report-authors)
- [Content check](#content-check-before-handoff)

## Source and authority boundary

The public sources were checked on **16 November 2026, Australia/Brisbane**.
The [source applicability crosswalk](https://github.com/edithatogo/rcagent/blob/58fb0b15171322f70ee070cea6756f32fe792f50/conductor/tracks/qld-heaps-review_20261116/source-map.md)
records inspected material, authority, pinpoints and limits. Refresh applicable
sources at use; this dated crosswalk does not override a later verified rule.

- Queensland Health's [Patient safety directive, QH-HSD-032](https://www.health.qld.gov.au/system-governance/policies-standards/health-service-directives/patient-safety),
  version 6.0 dated 9 October 2024, provides the relevant statewide reporting
  baseline. Preserve the actual triggering events and source applicability;
  this guide supplies no calculated deadline.
- The [Clinical incident management guideline, QH-HSDGDL-032-2](https://www.health.qld.gov.au/system-governance/policies-standards/health-service-directives/patient-safety/clinical-incident-management),
  sections 3.2-3.3, addresses method selection, participation, reporting and
  improvement. Its version history lists 4.0 dated 13 March 2026; the header's
  effective date of 1 July 2024 conflicts with 1 July 2027 in the approval block.
  Keep that conflict visible. Guidance and statutory RCA conditions do not
  become an automated legal decision.
- The [official template index](https://sqep.csds.qld.edu.au/resources/incident-review-templates/)
  links HEAPS tools through QHEPS. The current tools and local CHHHS procedure
  have not been inspected. Their fields, team rules, adaptations and rights
  remain unverified. The 2023 best-practice guide was only partly inspected
  through indexed text; failed PDF retrieval did not establish withdrawal.

Use the canonical jurisdiction source identifiers `qld-qh-hsd-032` and
`qld-qh-hsdgdl-032-2` through the existing registry. Keep current reporting rules
separate from the clinical standards applicable when the care occurred.
Confidentiality, privilege, severity, disclosure and notification remain
decisions for the applicable authorised process. No default protection label
belongs on this draft.

## Triage: establish the review and its unanswered questions

1. Record the purpose, scope, exclusions, care setting, jurisdiction, permitted
   data boundary and accountable role. Preserve immediate safety and evidence
   preservation work in the existing authorised system; packet preparation
   must not delay it.
2. Identify the current local procedure and template, or record that they are
   unavailable. Record the human decision to use HEAPS, its rationale and
   source separately from provisional severity, analysis depth and selected
   tools. An analyst's suggestion is not the commissioning decision.
3. Record concurrent questions, including mortality, coronial, specialty,
   clinical-risk or other review routes where relevant. Progress on HEAPS does
   not resolve a different route's authority or obligations.
4. Distinguish event occurrence, awareness, SAC1 reporting and submission
   timestamps. Missing trigger or calendar information stays unresolved.
   Changing review method does not reset an applicable reporting clock.
5. Record who was involved in the incident and who will facilitate, provide
   expertise, challenge the analysis, review findings or approve a defined
   output. Document conflicts and their disposition. Local policy determines
   the team; this guide does not exclude or require a person merely because
   they participated in care.
   Profile `incident_involvement: unknown` preserves missing knowledge;
   an absent record does not establish `not_involved`.
6. Identify the questions that the available evidence can answer. Select a
   supporting tool only for a recorded unanswered question and explain its
   limits. A partly known chronology is useful if its gaps remain explicit.

**Triage output:** a scoped preparation brief, a sourced selection decision or
unresolved selection question, an evidence inventory, a participation plan and
assigned questions. Do not invent a completed review to fill an empty packet.

## Investigate: preserve evidence, perspectives and alternatives

### Build an inspectable evidence trail

Keep source, artefact, evidence and statement identities distinct. Preserve the
original account and any correction history; describe extraction, redaction,
transcription and model involvement where applicable. Retain withheld or
withdrawn evidence status without exposing restricted content.

Record common source families: a document, its transcription, its OCR text and
several summaries may all originate from one account. Their agreement is not
independent corroboration. Keep supporting and contrary evidence together,
including family concerns that differ from a clinical record. Absence of a
record does not prove that an action did not occur.

Construct the clinical chronology from sourced statements. Show event time,
document time and when information became available only to their supported
precision. The canonical `events` collection records workflow transitions;
do not insert a clinical occurrence as a fabricated transition. Late evidence
must not become information a clinician was presumed to have earlier.

### Preserve participation without implying agreement

Separate the person providing an account, the role recording it, participation
in a meeting, confirmation of an account, review of an analysis and approval
of an output. None entails the next. Record whether an opportunity was offered,
whether a contribution is available, declined, withdrawn, pending or unknown,
and the evidence for that description. These are process descriptions; use
the profile's exact fields and values when serialising them.

Profile `participation[].state` distinguishes `provided`, `declined`,
`unavailable`, `not_requested`, `withdrawn`, `pending` and `unknown`. Record the
basis in `state_note` and `state_basis_refs`. Missing knowledge is `unknown`,
not evidence that participation was never requested. Keep `confirmation`
separate from this contribution state and from agreement with the analysis.

Keep each concern, response, correction and remaining disagreement attributable.
Do not blend conflicting voices into a consensus. Silence, no reply or declined
participation is not agreement. Record only expressed language, accessibility,
cultural and support needs; do not infer a person's identity or wishes.
Requests for contact or support go to the accountable human through an approved
route. Drafting this packet contacts nobody.

### Examine system conditions and protective factors

Describe work as done and the information available at the time: tasks, tools,
interfaces, workload, team coordination, environment, resources, policies,
adaptations and governance. Ask what helped as well as what made safe work
difficult. An unexplained label such as human error is not a sufficient account
of how the system behaved.

The [2010 Queensland learning report](https://www.health.qld.gov.au/__data/assets/pdf_file/0024/423537/lta3.pdf),
printed page 14, describes patient, task, practitioner, team, workplace and
organisational domains. If used, label the mapping as historical or provisional,
with its source and revision. It is not the authenticated current HEAPS taxonomy.
A factor may have multiple mappings or remain unmapped with a rationale; do not
force an unsupported category.

For each candidate factor or finding, retain its source statement, supporting
evidence, contrary evidence, alternative explanations and uncertainty. A factor's
function (`contributory`, `protective`, `barrier` or `system_condition`) is
different from its taxonomy category. Preserve its actual recorded status;
diagram placement or category assignment cannot accept it as a finding.

Use a [timeline](./timeline-analysis.md), [barrier analysis](./barrier-analysis.md)
or other admitted tool when it answers the review question. An optional
[AcciMap](./accimap.md) can expose relationships across system levels after its
applicable interface is accepted. Keep node and edge references, uncertainty
and contrary evidence; an edge does not itself establish causation. Leave out
an unqualified optional view while retaining the supported preparation work.

**Investigation output:** evidence-linked statements, a chronology with visible
gaps, separate participant accounts, candidate factors and proposed findings
with alternatives. An authorised person must inspect the evidence and record
the decision before a proposed finding is presented as accepted.

## Report: produce an original draft for a defined audience

Start with a short plain-language account of what is supported, what remains
uncertain and what decisions are requested. Expand acronyms. Keep the technical
references available without making a consumer interpret them to understand
the concern. A plain-language paraphrase must preserve attribution, uncertainty
and the original concern's meaning.

Use the draft outline to keep accounts, analysis, findings, recommendations
and decisions separate. Carry contrary evidence and limitations into the
summary; do not hide them only in an appendix. If no finding is supported,
say so and provide the evidence questions. If participation is missing or
declined, describe it rather than claiming consultation was completed.

Optional diagrams are additional views of the same referenced records. Give
each a draft caption, a source-linked explanation and an accessible text
equivalent. Do not introduce unsupported edges or turn a visual sequence into
a causal chain.

Bind the draft to the exact case and profile revisions and the source/mapping
inputs it used. The report body must not embed its own digest, the later packet
manifest digest or a later approval. Store the manifest and review decision
separately under the agreed profile contract. Material changes need new
revision bindings and renewed review of affected decisions; retain earlier
revisions.

Keep preparation, structural validation, source verification, local-template
mapping, authorised review and submission distinct. A source identifier or
record hash alone does not prove a source passage was checked. An existing
communication approval cannot approve every substantive finding or action.
A file described as a draft is not an official HEAPS form or an external
submission, even after engineering content checks pass.

## Track: connect proposed improvements to evidence of effect

For each recommendation, identify the finding or documented condition it
addresses, intended mechanism, accountable role, resources, dependencies,
unintended effects and due-date basis. Prefer a proportionate system change;
justify reliance on education or reminders if selected. Record implementation
evidence separately from planned and measured effectiveness.

Specify process, outcome and balancing measures, their baseline, denominator
or exposure, data source, review timing and interpretation limits. No fixed
follow-up interval is supplied here. An action marked implemented does not
show that the measure improved, and an improved measure alone does not prove
that the action caused the change.

Use actual canonical action and outcome states without substituting a single
complete flag. A review record marked complete describes that record's process
state; it does not confer clinical acceptance or close the case. Preserve
ineffective changes, harm, residual risks, overdue actions and unsuccessful
attempts. Escalation and closure decisions belong to the authorised system.

Where permitted, examine repeated recommendations and themes with explicit
denominators and source lineage. Several reports derived from one incident
must not be counted as independent events or as evidence of benefit.

## Canonical mapping for report authors

The canonical contract is `conductor/schemas/safety-work.schema.json`, version
1.1. The HEAPS sidecar is defined separately in
`evaluation/heaps/heaps-profile.schema.json`; the normative packet contract is
`conductor/tracks/qld-heaps-review_20261116/h3-contract.md`. These repository
contracts are not embedded or executed by reading this portable guide.

| Report information | Actual canonical identity or field | Boundary |
|---|---|---|
| Case and record revision | `case_id`, `schema_version`, integer `version` | Bind the admitted payload; do not confuse case version with profile version |
| People and responsibilities | `roles[].role_id`, `role_type`, `authority` | A role label records a claim of authority; it does not grant it |
| Source and captured material | `sources[].source_id`, `artefacts[].artefact_id`, `evidence[].evidence_id` | Keep their fingerprints, links and custody states distinct |
| Accounts, analysis and findings | `statements[].statement_id` plus `kind` and `provenance` | Accounts use `reported_account`; findings use `finding`; there is no core `account_id` or `finding_id` |
| Selection and other decisions | `statement_id` with `kind: decision` | A stored decision needs its source, role, scope and review evidence |
| Factors | `factors[].factor_id`, `statement_id`, `kind`, `status` | Taxonomy mappings belong outside the closed core factor |
| Supporting and contrary links | `relationships[].from_id`, `relation`, `to_id`, `rationale` | Preserve `supports`, `contradicts` and `derived_from`; validate target kinds in the consuming profile |
| Recommendations and actions | Recommendation `statement_id`; `actions[].action_id`, `recommendation_id`, `owner_role_id` | `recommendation_id` refers to the recommendation statement; dates and measures are not new core action fields |
| Review evidence | `reviews[].review_id`, `reviewer_role_ids`, `statement_ids`, `status` | Meeting attendance or process completion is not substantive approval |
| Outcomes and concurrent routes | `outcomes[].outcome_id`, `referrals[].referral_id` | Preserve evidence and status; an output does not perform the external route |

Profile references use the contract's typed `{kind, id}` form. Resolve both
identity and expected type at the bound case revision. Core provenance
`recorded_at` is the statement-recording time, not automatically the event or
original document time. Unknowns use explicit uncertainty and the profile's
question records; never fabricate a canonical entity or timestamp.

The core's objects are closed. Source-family membership, clinical chronology
annotations, participation dispositions, richer action plans and packet status
belong in their specified profile or companion records. Follow the exact
contract rather than adding convenient properties or unsupported enum values.

### HEAPS sidecar and companion records

The following are rcagent fields, not an official HEAPS form crosswalk.

| Preparation information | Profile fields | Mapping rule |
|---|---|---|
| Scope and selection | `applicability`; `selection.selected_by`, `decision_ref`, `analytical_tools` | Resolve role and decision references separately; each tool records its question |
| Inputs and source families | `source_snapshots`; `source_families[].source_ref`, `family_id`, `derived_from`, `independence` | Record snapshot version, locator, purpose, applicability and rights; common origin does not establish independent corroboration |
| Roles and participation | `roles[].role_ref`, `incident_involvement`, `responsibilities`; `participation` | Keep involvement, review tasks, contribution state, confirmation and expressed needs separate |
| Clinical and obligation times | `chronology[].statement_ref`, `event_time`, `document_time`, `available_time`, `ordering_note`; `clocks`; `deadlines` | Preserve precision and gaps; a deadline needs its trigger, rule, calendar snapshot, time zone and counting convention |
| Taxonomy and findings | `factor_assignments`; `finding_context[].finding_ref`, `supporting_refs`, `contrary_refs`, `alternative_refs`, `uncertainty` | Classification does not accept a factor; alternatives remain separate statements |
| Action plans | `action_context[].action_ref`, `recommendation_ref`, `finding_refs`, `condition_refs` and plan/measure fields | `condition_refs` targets statements; resolve a factor through its `statement_id`. Implementation state remains in the core action |
| Mapping gaps and parallel routes | `template_mapping`; `open_route_questions`; `optional_components` | Preserve unavailable or stale instruments, unanswered questions and unqualified optional views |

Packet components and later decisions use the separate
`packet-manifest.schema.json`, `review-decision.schema.json` and
`status-receipt.schema.json` contracts in `evaluation/heaps/`. A source check's
scope matters: `record_reference_integrity` does not establish
`accepted_d0_byte_spans`. Neither alone establishes source truth, causal support
or independent corroboration. This increment keeps actual authority unverified,
clinical review not established and external submission `not_submitted`.
Even `synthetic_draft_reviewed` is a bounded synthetic preparation status.
Do not promote these values through narrative wording or a filled template.

## Content check before handoff

- The authorised local process and the person's method-selection decision are
  identifiable, or their absence is explicit.
- Every substantive statement has its kind, source, reviewer state and limits;
  alternative explanations and contrary evidence remain visible.
- Source-family lineage prevents derived copies being treated as corroboration.
- Participation, confirmation, review and approval are separate, including
  absent, declined and withdrawn contributions.
- Recommendations trace to supported conditions and have an owner and an
  implementation/effectiveness plan; unknown inputs remain unknown.
- Current-template fidelity, legal protection and operational authority are
  not inferred from public sources, identifiers, software checks or a diagram.
- Input identities and later manifest/approval records remain separately
  bound; no self-referential report hash is introduced.

Record content review and unresolved gaps separately from executable test
results. This guidance and a completed outline do not qualify an assembler,
establish source-byte verification or demonstrate patient benefit.
