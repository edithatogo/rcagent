# Queensland HEAPS source map

Checked **16 November 2026, Australia/Brisbane**. This is an original planning
crosswalk for Human Error and Patient Safety (HEAPS) review support. It records
what was inspected, what each source supports and what remains unknown. It does
not certify an official HEAPS template or a Cairns and Hinterland Hospital and
Health Service (CHHHS) procedure.

[sources.json](./sources.json) is the machine-readable planning inventory.
The existing [jurisdiction registry](../../jurisdictions/registry.json) remains
the canonical authority record. The source IDs `qld-qh-hsd-032` and
`qld-qh-hsdgdl-032-2` are references to that registry; this track creates no
second authority registry or enabled policy rules. Source bytes and official
templates are not included, and no source-byte hashes were invented.

## Source and applicability matrix

| Source | Material inspected | Permitted planning use | Limitation |
|---|---|---|---|
| `qld-qh-hsd-032` | Current public directive HTML; version 6.0 dated 9 October 2024 | Existing SAC1 reporting baseline, report content and statewide risk escalation | Correct classification, trigger dates and authorised process remain necessary |
| `qld-qh-hsdgdl-032-2` | Current public guideline HTML; version history 4.0 dated 13 March 2026 | Method selection, participation, report accessibility and action follow-through | Effective-date conflict remains; guidance is not silently made mandatory |
| `heaps-qld-sqep-template-index` | Public HEAPS resource landing page | Establishes the existence and QHEPS location of the tools | Current tools, fields and redistribution rights were not inspected |
| `heaps-qld-best-practice-guide-2023` | Partial indexed introductory text and indexed page 42 excerpt | HEAPS as a comprehensive-analysis tool; wider incident-management context | Subsequent live retrieval failed; no full guide or current template verification |
| `heaps-qld-learning-action-2010` | Relevant official report text, printed page 14 | Historical contributing-factor domains and system-learning orientation | Describes older practice; supplies no current routing or template rule |
| `heaps-metro-north-governance-2021` | Official review recommendations, printed pages 4-5 | Evidence-to-factor-to-action links, timelines and duplicate-action checks | Local review recommendations, not statewide mandates |
| `heaps-oho-incident-management-2024` | Full two-page regulator snapshot text | Action ownership, dates, status, recurring themes and implementation evidence | One entity's evaluation, not an official HEAPS schema or CHHHS assessment |

## Existing statewide authority

### Patient safety directive

[Patient safety, QH-HSD-032](https://www.health.qld.gov.au/system-governance/policies-standards/health-service-directives/patient-safety)
is recorded as `qld-qh-hsd-032`. Its mandatory clinical-incident requirements
cover reporting applicable Severity Assessment Code 1 (SAC1) incidents through
RiskMan within one business day of awareness and submitting an analysis report
within 90 calendar days of reporting as SAC1. Reports must cover event facts,
contributing factors and recurrence-prevention recommendations. The directive
also addresses escalation of risks with potential statewide impact.

Planning consequence: preserve incident occurrence, awareness, SAC1 reporting
and submission as separate events. A generated packet is not proof of a
submission. Reuse qualified jurisdiction components and their applicability
checks; this inventory does not activate a deadline, notification or connector.

### Clinical incident management guideline

[Clinical incident management guideline, QH-HSDGDL-032-2](https://www.health.qld.gov.au/system-governance/policies-standards/health-service-directives/patient-safety/clinical-incident-management)
is recorded as `qld-qh-hsdgdl-032-2`. Sections 3.2.2-3.2.4 support explicit
method selection and distinguish it from the conditions for statutory RCA
protection. Queensland Health does not prescribe one analysis method for SAC1.
Sections 3.2.6-3.3 support participation, accessible reporting and accountable
recommendation follow-through.

Keep method, analysis depth, incident classification, legal basis and authority
as separate attributes. A method name or report label cannot grant privilege.
The stated reportable-event condition is not a complete legal admission test.
Guideline recommendations expressed as *should* remain guidance unless another
applicable source establishes a mandatory requirement.

The page's version history lists **4.0, 13 March 2026**, with a last-updated
date of **18 June 2026**. Its header says effective **1 July 2024**, review
**1 July 2027**; the approval block instead says effective **1 July 2027**.
Preserve this conflict. Do not infer withdrawal, invent a corrected date or
overwrite the canonical registry from this planning record.

## Official HEAPS tools: current field-level gap

The [Queensland Health Safety and Quality Education Program's incident review
templates page](https://sqep.csds.qld.edu.au/resources/incident-review-templates/)
advertises a HEAPS set of tools and morbidity and mortality report templates.
It identifies a Queensland Health audience and links to QHEPS. The public page
was inspected; the linked tools were not accessed and no intranet authentication
was attempted. Its 6 June 2024 update date is not a verified template revision.

Unknowns remain: exact current sections and fields, required and conditional
content, factor taxonomy, team and approval rules, CHHHS adaptations and rights
to reproduce or adapt the actual tools. Do not reconstruct an official form from
memory or describe a proposed workflow as the authenticated HEAPS process.
An initial original profile may be described as a **HEAPS-aligned draft** while
those dependent claims remain held.

## 2023 best-practice guide: partial observation

The [legacy public guide URL](https://clinicalexcellence.qld.gov.au/sites/default/files/2018-01/clinicalincidentguide.pdf)
initially returned indexed text identifying the **second edition, January 2023**.
The URL's `2018-01` path is not the edition date. The tool reported 126 pages and
7,041 lines but displayed only lines 0-544, including title, licence, contents
and introductory material. A separate indexed search excerpt exposed printed
page 42, which identifies HEAPS alongside RCA and London Protocol as available
tools for comprehensive analysis.

Subsequent open, find and screenshot attempts returned 404 or inaccessible
responses, including attempts at the newer `docs/resources` and
`docs/resourses` paths. No complete source PDF was obtained. The source is
therefore recorded as **partial indexed inspection with failed live retrieval**,
not as a successful current full-text review.

The contents describe six general incident-management stages. They do not prove
six specific HEAPS steps or an exact template structure. The observed page 2
states Creative Commons Attribution 3.0 Australia for the guide; that statement
does not establish rights for a separate current QHEPS template, branding or
third-party content. This track links and paraphrases only.

## Historical domains and observed quality failures

### Historical HEAPS description

[Patient Safety: From Learning to Action III](https://www.health.qld.gov.au/__data/assets/pdf_file/0024/423537/lta3.pdf),
Queensland Health, May 2010, printed page 14, describes patient, task,
practitioner, team, workplace and organisational factors. These are useful
historical domains for a provisional mapping. They are neither six process
steps nor a verified current taxonomy.

The report concerns 2007-08 practice and superseded arrangements. Its older
descriptions of method eligibility, severity routing or team participation
must not override the current guideline. It supports maintaining a system
learning purpose alongside separate accountability processes.

### Metro North review: explicit links and quality review

The [October 2021 Independent Governance Review of Caboolture Hospital
Surgery](https://metronorth.health.qld.gov.au/wp-content/uploads/2021/11/independent-governance-review-2021.pdf),
version 1.0, printed pages 4-5, recommendations 8-10, calls for independent
re-review, timeline sections, links from contributing factors to recommendations,
checking duplicated previous recommendations and governance review before
finalisation.

These findings inform proposed checks for missing timelines, unsupported
findings, orphan recommendations and repeated actions. They are local review
recommendations from 2021, not a current statewide HEAPS specification.
Repository agent review may examine implementation and synthetic evidence;
it does not supply the independent clinical or organisational authority described
in a health-service review.

### Health Ombudsman snapshot: follow-through needs evidence

The [Office of the Health Ombudsman's incident-management snapshot](https://www.oho.qld.gov.au/assets/reports/snapshot-report-202409-clinical-incidents.pdf)
reports an August 2024 evaluation. Page 1 recommends reviewing common themes and
implementation progress and identifying action dates, responsible people and
ongoing or completed status. Page 2 identifies gaps in evidence linking audit
findings to corrective actions in the evaluated entity.

Planning consequence: record approval, implementation and effectiveness
separately, each with its own evidence. A completed report or implemented action
does not establish effectiveness. This evaluation is not a finding about CHHHS
and does not supply a HEAPS field-level contract.

## Intake contract for current local material

The next source-specific dependency is an **authorised blank current CHHHS
procedure and HEAPS template**, together with the applicable statewide tool
revision and any documented local adaptation. It is not a request for a
completed review or a clinical record. Blank material can still be restricted.

1. Record issuer, local custodian, document identifier, title, version,
   approval/effective/review dates, current-status evidence and applicability.
2. Record source location, access date, classification and the authorised
   environment. Record permission to inspect, adapt and redistribute separately;
   possession of a document does not establish all three.
3. Check that the material contains no patient, staff, case or incident
   identifiers, credentials, completed examples or internal comments. Keep
   restricted source bytes in the authorised environment.
4. If an authorised copy is acquired, calculate a checksum from the actual
   bytes. Until then, retain a null hash with its reason.
5. Produce an original field crosswalk: source locator, required/optional/
   conditional status with evidence, canonical rcagent object, provenance,
   local role or approval dependency, ambiguity and disposition.
6. Review conflicts against the canonical jurisdiction registry and preserve
   unresolved questions. Any canonical registry change belongs to its existing
   owner; this track does not establish competing policy rules.

Only rights-cleared original mappings and synthetic examples may enter the
public repository. Official text, branded templates and restricted material
are not copied by default. Exact template fidelity, current CHHHS policy
conformance and local operational approval remain separate held claims until
their evidence and accountable authority are available.

These gaps do not block original public-source contracts, synthetic fixtures or
non-operational quality checks. They block only the claims and operational
behaviour that depend on the missing local sources or authority.

## H1 refresh

On 16 November 2026 the directive, guideline and SQEP HEAPS index were rechecked. Their applicability classification and the guideline metadata conflict are retained. Source-specific current observations, failed guide retrievals and two supporting discovery references are recorded in sources.json h1_refresh and [h1.md](./h1.md). Historical and local improvement sources retain their earlier observations; they are not relabelled as freshly retrieved. The inventory remains inactive and does not admit the unavailable official template.
