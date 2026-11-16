# HEAPS review — synthetic preparation draft

> Original rcagent working outline. Apply the [template use contract](../../template-use-contract.md)
> and [HEAPS preparation guide](../../../references/methods/heaps.md). This is
> not a Queensland Health issued HEAPS form. Use generated-synthetic placeholders
> for this preparation increment. A filled field establishes no finding,
> agreement, approval, legal protection, notification, submission or benefit.

## Preparation identity and audience

| Item | Record |
|---|---|
| Case | `[Case ID]`; canonical `case_id: [case_id]` |
| Canonical record | `schema_version: [1.1]`; `version: [integer]`; `[core hash and declared domain]` |
| HEAPS profile | `[Profile identity, version and precomputed input hash]` |
| Source and mapping inputs | `[Exact input identities/revisions; unavailable inputs stated]` |
| Preparation date | `[Date and Time, including timezone]` |
| Intended audience and use | `[Synthetic review/meeting preparation; audience and limits]` |
| Permitted data boundary | `[Generated-synthetic input declaration; canonical privacy_mode; storage and audience]` |
| Model/tool involvement | `[Not used, or exact tool/revision, task and limitations]` |

The core and profile identities identify inputs. Do not place this report's own
hash, a later packet-manifest hash or a later review decision in its body.
The detached manifest and review/delivery receipts are separate artefacts.
Replacing placeholders does not itself validate the underlying records.

## 1. Scope, applicable process and authority

| Question | Source-grounded record or unresolved question |
|---|---|
| What is this review intended to understand? | `[Purpose, date range, care setting, scope and exclusions]` |
| Which requirements and local process apply? | `[Jurisdiction; issuer, document identifier/version, pinpoint, applicability and reference]` |
| Why was HEAPS selected? | `[Human-recorded selection decision statement_id; responsible role_id; rationale and evidence]` |
| What analysis depth and tools were selected? | `[Scope and each tool's unanswered question; keep distinct from review process]` |
| Who commissioned the review? | `[Role, recorded authority and decision reference, or unresolved]` |
| What is the recorded incident classification? | `[Authorised determination and source, provisional description, or unresolved; do not infer from outcome]` |
| What current template/local mapping is available? | `[Profile template_mapping.state: original/unavailable/mapped_unverified/stale; actual instrument, revision, rights and field gaps]` |
| What concurrent routes remain? | `[Mortality, specialty, reporting or other questions with owners; existing referral_id where applicable]` |
| What confidentiality/disclosure/protection decision exists? | `[Unverified unless an authorised applicable determination and exact scope are evidenced]` |

Use the source/authority crosswalk in the HEAPS guide. Preserve the Queensland
guideline's conflicting effective-date metadata. The public HEAPS index and
partially inspected guide do not establish current CHHHS template conformity.
Do not add a blanket protection heading.

### Timing and immediate safeguards

| Matter | Known time/precision and evidence | Responsible role and unresolved input |
|---|---|---|
| Incident occurrence | `[Supported time or unresolved; statement_id/evidence_id]` | `[role_id; gap]` |
| Awareness of applicable event | `[Supported trigger or unresolved; statement_id/evidence_id]` | `[role_id; gap]` |
| SAC1 reporting, if applicable | `[Actual recorded trigger or unresolved; reference]` | `[role_id; classification/trigger gap]` |
| External submission, if evidenced | `[Receipt reference or not evidenced]` | `[role_id; separate authorised process]` |
| Applicable timing rule/local target | `[Existing rule ID/revision, applicability and calendar basis, or unresolved]` | `[role_id; missing inputs]` |
| Immediate safety/evidence preservation | `[Recorded action and evidence; proposed action labelled]` | `[role_id; outstanding safeguard]` |

No duration or deadline is supplied by this outline. Keep local targets and
statewide obligations separate; changing method does not reset a reporting
clock. Packet preparation is not the reporting or immediate-response process.

## 2. Plain-language account and questions

**What the available evidence describes:**
`[Brief neutral account, using [Patient A], [Clinician A], [Ward X] and cited statement IDs.]`

**What remains uncertain or disputed:**
`[Contrary accounts, missing material and alternatives, with their IDs where available.]`

**What the reviewers are being asked to decide:**
`[Specific review questions; no assumed consensus or mandatory finding.]`

If no finding is supported, say **“No supported finding has been recorded in
this draft”** and retain the evidence questions. Expand specialist terms and
preserve the meaning and uncertainty of each concern in any plain-language
paraphrase.

## 3. Roles, participation and concerns

### Roles and review responsibilities

| Canonical role | Involvement in the incident | Review responsibility | Authority/conflict evidence and disposition |
|---|---|---|---|
| `[role_id; synthetic role label]` | `[involved/not_involved/unknown; recorded basis]` | `[Facilitation, expertise, challenge, review or scoped approval; do not infer]` | `[Source/decision statement_id and unresolved conflict]` |

Local policy determines composition and conflict management. Involvement in
care does not itself confer or remove facilitation, review or approval
authority. `role_type` describes a role; it does not prove that authority.
Absence of an involvement record means involvement is unknown; it does not
establish `incident_involvement: not_involved`.

### Participation and account handling

| Voice or role | Opportunity and participation evidence | Account and correction references | Concern, response and remaining disagreement |
|---|---|---|---|
| `[Patient A / family / carer / staff / other relevant role]` | `[Offered/not evidenced; contribution available, pending, declined, withdrawn or unknown, with source]` | `[reported_account statement_id; source_id; correction/supersession references, or absent]` | `[Concern in its own meaning; attributable response; unresolved disagreement]` |

Record expressed contact, language, accessibility, cultural and support needs
in the designated participation record and permitted environment. Do not infer
needs or consent. Record a requested human follow-up without sending contact.
No reply, declined participation, meeting attendance and confirmation of an
account are distinct from agreement with findings or recommendations.
For profile serialisation use `participation[].state` exactly: `provided`,
`declined`, `unavailable`, `not_requested`, `withdrawn`, `pending` or `unknown`.
Record `state_note` and `state_basis_refs`; do not turn an unknown or pending
response into `not_requested`. Keep account `confirmation` separate.

## 4. Evidence and source-family register

| Source | Artefact/evidence references | Location, transformation and custody | Common source family | Limits or contrary material |
|---|---|---|---|---|
| `[source_id; source type and title]` | `[artefact_id; evidence_id]` | `[Inspectable locator if verified; extraction/redaction/custody detail]` | `[Profile family reference and common origin; unknown if not established]` | `[Missing, late, withdrawn, restricted, conflicting or unverified material]` |

Keep the source's actual fingerprint and evidence identity in the bound
records. A source reference or hash alone does not verify a quoted passage.
One record, its transcription and several summaries may share one origin;
do not count them as independent corroboration. Cite an actual source-byte
verification receipt only when that check was performed for these exact inputs.

## 5. Clinical chronology with uncertainty

| Sourced statement and kind | Occurrence time/precision | Document/information-availability evidence | Account or observed content | Gap or conflict |
|---|---|---|---|---|
| `[statement_id; observed_fact/reported_account/inference as actually recorded]` | `[Supported time/range or unresolved]` | `[Original document time and when known, if supported; source/evidence reference]` | `[Neutral content preserving attribution]` | `[Uncertain ordering, later knowledge or contrary statement_id]` |

The core `events` array contains workflow transitions. Clinical chronology is
a view of referenced statements and profile annotations; do not fabricate a
workflow event for a clinical occurrence. A statement's `provenance.recorded_at`
is not automatically the occurrence or original document time. Do not invent
an exact time or total ordering where the evidence supports only a partial one.
If only a range is supported and the profile cannot express it as a known
`time_value`, retain the range in uncertainty/`ordering_note` with the time
unknown; do not invent a precision value or a point estimate.

## 6. System conditions and factor analysis

| Factor and source statement | Function and recorded status | Taxonomy mapping | Support and contrary evidence | Alternative explanation or gap |
|---|---|---|---|---|
| `[factor_id; statement_id]` | `[Actual factor.kind and status]` | `[Profile taxonomy/version; one, several or unmapped with rationale]` | `[Typed references; relationship rationale; source-family limits]` | `[Competing mechanism, protective factor or evidence needed]` |

Distinguish factor function from classification. The core factor functions are
`contributory`, `protective`, `barrier` and `system_condition`; current status
is recorded independently. Historical HEAPS domains are provisional mapping
prompts unless the actual current taxonomy has been verified. Consider work
as done, constraints, information available at the time and what helped.

**Optional diagram:** `[Omit unless it answers a recorded question. Include
referenced nodes/edges, draft caption, uncertainty and accessible text.]`

A diagram edge, classification or repeated account is not proof of causation
or a finding. Preserve contrary evidence in both the analysis and its summary.

## 7. Proposed findings and recorded decisions

| Statement ID and kind | Content | Support, contrary evidence and alternatives | Provenance review state | Recorded review/decision evidence |
|---|---|---|---|---|
| `[statement_id; hypothesis/inference/finding/decision as actually recorded]` | `[Separate proposed interpretation from accepted determination]` | `[Typed IDs and unresolved uncertainty]` | `[Actual provenance.review_state]` | `[review_id; reviewer role_id; decision/source reference or absent]` |

An authorised reviewer must inspect the evidence before accepting a proposed
finding. Keep hypothesis, inference, finding and decision kinds distinct.
An `accepted` label, a completed review or a model's confidence does not alone
prove the source support or the reviewer's authority. Preserve rejected and
withdrawn material with its reasons and correction history.

## 8. Recommendations, actions and evaluation

### Recommendation-to-action trace

| Recommendation statement | Linked finding/condition and mechanism | Canonical action and owner | Implementation evidence/state | Effectiveness evidence/state |
|---|---|---|---|---|
| `[statement_id with kind recommendation]` | `[finding or condition statement_id; optional factor_id trace; intended mechanism and support]` | `[action_id; owner_role_id]` | `[Actual action.status; implementation_evidence_ids or absent]` | `[Actual action.effectiveness_state; outcome_id/evidence or unresolved]` |

`actions[].recommendation_id` references the recommendation statement.
The canonical action's implementation and effectiveness states are separate.
Do not mark an action effective because it was implemented.
For profile `action_context[].condition_refs`, reference the condition's actual
statement kind and `statement_id`. When starting from a factor, resolve its
`factors[].statement_id`; a `factor_id` is not a statement ID.

### Plan detail and measurement questions

| Linked action | Plan or missing input | Evidence needed for evaluation | Review responsibility |
|---|---|---|---|
| `[action_id]` | `[Resources, dependencies, due-date source, proposed system change and foreseeable unintended effects]` | `[Process/outcome/balancing measure; baseline, denominator/exposure, target, data source and timing, or explicit gaps]` | `[role_id; authority and escalation route]` |

Store richer plan details in the designated profile or companion records;
do not add due-date, measure or resource properties to the closed core action.
An absent baseline or denominator remains a gap. Keep implementation evidence,
observed outcome changes, balancing effects and causal interpretation separate.
The reviewer determines follow-up and residual-risk disposition through the
applicable process; this outline supplies no automatic closure.

## 9. Unresolved questions and next evidence

| Question | Related canonical references, if present | Evidence needed | Responsible role and follow-up basis |
|---|---|---|---|
| `[Missing source, conflict, participation, policy, timing or authority question]` | `[{kind, id}; do not invent an entity to fill a blank]` | `[Specific source or authorised determination needed]` | `[role_id or explicitly unassigned; source for timing]` |

An empty or all-abstaining analysis is not a completed review. Report the
supported preparation work and outstanding questions with an honest denominator
if a completeness count is shown. Do not substitute a generic success statement.

## 10. Meeting preparation and record

**Meeting reference:** `[review_id, if a canonical review record exists; actual
review_type and status; do not create a new HEAPS core enum.]`

**Participants and accessibility arrangements:** `[role_ids; evidenced
arrangements and absent/declined voices, with no assumed agreement.]`

Suggested agenda, adapted through the authorised local process:

1. Confirm purpose, authority, scope, conflicts, support and data boundary.
2. Hear the recorded patient/family/carer and staff concerns separately; identify
   corrections and questions that remain unanswered.
3. Review the chronology, source families, contrary evidence and missing items.
4. Examine candidate conditions and alternative explanations; record which
   findings need more evidence or a scoped authorised decision.
5. Discuss linked recommendations, feasibility, owners and possible unintended
   effects; distinguish proposals from authorised actions.
6. Record implementation/effectiveness measures, unresolved questions, follow-up
   responsibilities and the separate communication/approval process.

**Meeting record:** `[Decision statement_ids; dissent; corrections; evidence
requests; named synthetic role owners and actions. Preserve who said what.]`

Completing an agenda or meeting record does not approve a finding, imply
participation by an absent person or prove that an external communication occurred.

## 11. Preparation limits and separate decisions

| Dimension | Evidence or current limitation |
|---|---|
| Preparation | `[What was assembled and what is absent]` |
| Structural validation | `[Exact executed receipt or not performed; no inferred pass]` |
| Source-support verification | `[Checks actually performed and remaining gaps; no hash-only verification claim]` |
| Current local-template mapping | `[original/unavailable/mapped_unverified/stale; evidence and gaps without official-conformity inference]` |
| Authorised substantive review | `[Input decision/review references for each scope, or absent/unresolved]` |
| Packet communication/release | `[Separate later decision receipt required; not supplied by this draft]` |
| External submission | `[Separate system-of-record evidence, or not evidenced]` |
| Implementation and effectiveness | `[Separate records and limitations; no patient-benefit inference]` |

Use the exact status values of each applicable contract when serialising these
dimensions; these table descriptions do not add enum values to the core.
For this increment, actual authority remains `unverified`, clinical review
`not_established` and submission `not_submitted`. A source check that covers
`record_reference_integrity` does not establish `accepted_d0_byte_spans`.
A `synthetic_draft_reviewed` receipt is not clinical or organisational approval.
A later manifest or approval belongs in a separate receipt, not as a
self-referential addition to the report that it approves. Changes to the case,
profile, source/mapping inputs or report invalidate the affected prior bindings
and require the appropriate renewed review.

## Canonical reference notes

- Accounts, findings, recommendations and decisions use `statement_id` plus
  their respective `kind`; there is no core `finding_id` or `account_id`.
- Source material uses `source_id`, `artefact_id` and `evidence_id`. Source-family
  membership is separate profile metadata, not a new property of a core source.
- People, factors, actions, reviews, outcomes and referrals use `role_id`,
  `factor_id`, `action_id`, `review_id`, `outcome_id` and `referral_id` respectively.
- Typed profile references use `{kind, id}` and must resolve to the expected
  entity type and bound case revision. A generic relationship endpoint existing
  somewhere is not enough to establish the intended type.
- Uncertainty and questions stay explicit. Every placeholder in this outline
  is a prompt, not evidence that a canonical record or decision exists.
