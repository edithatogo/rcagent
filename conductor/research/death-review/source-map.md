# NSW and Queensland death-review sources

Checked 12 November 2026 UTC / 13 November 2026 Australia/Brisbane. This is an original planning crosswalk, not legal advice or a replacement for an authorised service's procedures. [sources.json](./sources.json) records version, authority, access, rights, retrieval and uncertainty for each source. References are links; official forms, logos and copyrighted templates are not redistributed.

## Material currency findings

- NSW CEC's current [incident-policy page](https://cec.health.nsw.gov.au/incident-management/policy) points to **PD2026_036**. Its [implementation update](https://cec.health.nsw.gov.au/incident-management/policy/key-changes) says the revision was published **9 November 2026** and changes reporting definitions, SAER processes and timeframes. Older CEC report pages still cite PD2020_047. The new directive's full text was not retrievable during this review; changed obligations remain unresolved rather than inherited from 2020.
- **PD2026_019**, published **9 April 2026**, is Active and expressly replaces **PD2021_006**. NSW's legal compendium, last current at April 2025, still lists the old maternal directive. A current-looking index is not sufficient evidence of currency. [Current maternal directive](https://www1.health.nsw.gov.au/pds/ActivePDSDocuments/PD2026_019.pdf).
- The CEC-linked M&M guideline is dated **September 2020**. It remains publicly linked; that does not make it a 2026 edition or validate every old policy/legal reference inside it. [CEC M&M page](https://cec.health.nsw.gov.au/improving-practice-and-culture/evaluate/morbidity-mortality-meetings).
- The current CHASM page says its previous mortality-review method ended in **2025** and redesign commenced in **2026**. An old notification destination or process must not be hardcoded as current. [CHASM](https://cec.health.nsw.gov.au/incident-management/committees/chasm).
- QLD's clinical-incident guideline identifies **QH-HSDGDL-032-2**, an effective date of **1 July 2024** and review date **1 July 2027**; its approval block instead says effective **1 July 2027**, while version history lists **4.0, 13 March 2026**. Preserve this conflict and seek current applicability confirmation before automating a rule. [QLD guideline](https://www.health.qld.gov.au/system-governance/policies-standards/health-service-directives/patient-safety/clinical-incident-management).
- A current freely accessible statewide QLD general mortality-screening instrument was not established by this search. An official resource index points to QLD Health M&M/HEAPS resources. The applicable HHS instrument and its version remain an explicit local dependency; NSW tools must not be substituted silently.

## NSW-DS

**NSW CEC — Death Screening and Database Project.** Public overview, no formal policy number or publication date displayed. It describes a standardised admitted-patient death-screening approach and review of deaths to examine care. The actual current screening instrument and completion-guideline version were not available from the retrieved public page. Engineering implication: support screening as a distinct stage, keep scope and tool revision explicit, and do not assume all screened deaths require a full RCA.

Source: [CEC death screening](https://cec.health.nsw.gov.au/improving-practice-and-culture/end-of-life/death-screening-and-database-project).

## NSW-MM

**Guidelines for Conducting and Reporting Morbidity and Mortality/Clinical Review Meetings**, CEC, September 2020; SHPN (CEC) 200272. Currently linked guidance, not a policy directive. It supports structured, multidisciplinary, psychologically safe discussion, documented learning and governance follow-through. Appendix D covers cognitive autopsy. Engineering implication: prepare an evidence-grounded meeting packet and action trace; do not treat an M&M discussion as a statutory finding or reuse outdated linked policies as current authority.

Sources: [CEC landing page](https://cec.health.nsw.gov.au/improving-practice-and-culture/evaluate/morbidity-mortality-meetings); [September 2020 guideline](https://cec.health.nsw.gov.au/__data/assets/pdf_file/0003/602697/Guidelines-for-Conducting-and-Reporting-Morbidity-and-Mortality.pdf).

## NSW-IM

**Incident Management, PD2026_036**, NSW Health. CEC identifies the current revision and publication on 9 November 2026. The retrieved implementation guidance highlights person-centred, trauma-informed and culturally responsive incident review. The full directive's effective arrangements, replacement statement and detailed changed rules were not verified. **PD2020_047** is retained as historical/transition evidence, not the default current authority. No incident deadline is enabled by this plan.

Sources: [current policy guidance](https://cec.health.nsw.gov.au/incident-management/policy); [implementation changes](https://cec.health.nsw.gov.au/incident-management/policy/key-changes); [PDS record](https://www1.health.nsw.gov.au/pds/Pages/doc.aspx?dn=PD2026_036); [clinical incident resources](https://cec.health.nsw.gov.au/incident-management/policy/responding-to-a-clinical-incident).

## NSW-VD

**Verification of death and medical certificate of cause of death, PD2023_014**, NSW Health; published 6 July 2023; review 6 July 2028; **Active** on retrieved PDF. It covers practitioner roles and separate verification/certification processes. rcagent may identify existing documentation and gaps, but neither examine a person nor complete the practitioner's determination.

Source: [PD2023_014](https://www1.health.nsw.gov.au/pds/ActivePDSDocuments/PD2023_014.pdf).

## NSW-COR

**Coroners Cases and Coroners Act 2009, PD2024_036**, NSW Health; published 19 December 2024; review 19 December 2029; **Active**. Replaces PD2010_054 and IB2010_058. It addresses reportable deaths, reporting and family support, including specific child and voluntary-assisted-dying issues. rcagent should preserve a coronial question for the responsible person; a mortality or M&M review does not resolve statutory reporting.

Source: [PD2024_036](https://www1.health.nsw.gov.au/pds/ActivePDSDocuments/PD2024_036.pdf). Exact legal applicability still requires the current Act, regulations and local authorised process at use time.

## NSW-MAT

**Identifying and Reporting of Maternal Deaths in New South Wales, PD2026_019**, NSW Health/CEC; published 9 April 2026; review 9 April 2031; **Active**; replaces PD2021_006. The directive covers identification, notification and review, including deaths during pregnancy and up to 365 days after pregnancy ends. It also recognises additional incident, coronial and specialty pathways. Record a maternal-route question with evidence and applicable version; do not infer cause or generate the statutory submission.

Source: [PD2026_019](https://www1.health.nsw.gov.au/pds/ActivePDSDocuments/PD2026_019.pdf). The old policy is explicitly superseded; the April 2025 [legal-compendium listing](https://www.health.nsw.gov.au/legislation/Pages/end-of-life-issues.aspx) is discovery evidence only.

## NSW-PERI

**Investigation, Review and Reporting of Perinatal Deaths, PD2022_046**, NSW Health/CEC; published 26 September 2022; review 26 September 2027; **Active** on PDF; replaces PD2022_026. It defines a separate perinatal review/classification/reporting process. Its references to PD2020_047 and MPMRC require reconciliation with the newer incident directive and the maternal policy's committee changes. Do not mechanically copy an old committee address or incident deadline. Preserve a specialty-route question until the current service destination is verified.

Source: [PD2022_046](https://www1.health.nsw.gov.au/pds/ActivePDSDocuments/PD2022_046.pdf); compare [PD2026_019](https://www1.health.nsw.gov.au/pds/ActivePDSDocuments/PD2026_019.pdf).

## NSW-CHASM

**Collaborating Hospitals' Audit of Surgical Mortality**, CEC current programme page. It records the discontinuation of the previous mortality-review method in 2025 and a redesign beginning in 2026. This is a programme-transition source, not proof of a currently executable referral workflow. Confirm surgical/anaesthetic specialty destinations and the service process before use.

Source: [CEC CHASM](https://cec.health.nsw.gov.au/incident-management/committees/chasm).

## QLD-PS

**Patient Safety, QH-HSD-032**, Queensland Health service directive; effective 9 October 2024; review 9 October 2027; supersedes version 5.0. It applies to HHSs and includes clinical-incident, mortality-indicator and coronial-response requirements. Its SAC1 reporting/analysis obligations apply to that defined class, not automatically to every death. A future deadline feature must preserve the classification, triggering date, applicability and source, with human authority.

Source: [QH-HSD-032](https://www.health.qld.gov.au/system-governance/policies-standards/health-service-directives/patient-safety).

## QLD-CIM

**Clinical Incident Management Guideline, QH-HSDGDL-032-2**, Queensland Health; public version history 4.0 dated 13 March 2026, with conflicting effective-date metadata described above. It permits different incident-analysis methods and addresses patient/family engagement, reporting and learning. Statutory RCA protections have specific conditions; an ordinary review does not automatically acquire them. Engineering implication: represent method selection and protection status explicitly, and preserve uncertain applicability.

Source: [QH-HSDGDL-032-2](https://www.health.qld.gov.au/system-governance/policies-standards/health-service-directives/patient-safety/clinical-incident-management). The official [SQEP resource index](https://sqep.csds.qld.edu.au/category/guides/) points to HEAPS/M&M resources; it does not establish a fully retrieved current statewide general screening instrument.

## QLD-MP

**Queensland Maternal and Perinatal Quality Council**, Clinical Excellence Queensland; public page last updated August 2026. It describes maternal/late maternal and perinatal review, local perinatal audit and reporting resources. It distinguishes an opportunity to reduce risk or improve care from proof that a death could have been prevented. This supports separate fields for care quality, causal hypotheses and preventability uncertainty. The approved committee's status does not confer its protection on rcagent outputs.

Source: [QMPQC](https://www.clinicalexcellence.qld.gov.au/committees-and-networks/quality-assurance-committees/queensland-maternal-and-perinatal-quality-council).

## QLD-ANA

**Queensland Perioperative and Periprocedural Anaesthetic Mortality Review Committee**, Clinical Excellence Queensland. The current page describes notification/review for deaths within 30 days of an anaesthetic/sedation procedure and its approved-committee status. This is a specialty review scope; proximity alone does not establish anaesthetic causation, clinical incident status or coronial reportability. Preserve the specialty question and authorised notification pathway.

Source: [QPPAMRC](https://www.clinicalexcellence.qld.gov.au/committees-and-networks/quality-assurance-committees/queensland-perioperative-and-periprocedural-anaesthetic-mortality-review-committee).

## QLD-COR

**Coroners Court Queensland — For health professionals** links the current reporting guidance and advice pathway for uncertainty. **Coroners Act 2003**, current consolidated legislation, is the legal anchor. **Form 1A, version 11, 1 July 2024** has specific eligibility; it is not a generic all-deaths reporting route. rcagent can assemble questions and index evidence, while qualified humans determine the applicable pathway and submit required documents.

Sources: [health-professional guidance](https://www.coronerscourt.qld.gov.au/for-health-professionals); [current Act](https://www.legislation.qld.gov.au/view/whole/html/current/act-2003-013); [Form 1A](https://www.coronerscourt.qld.gov.au/__data/assets/pdf_file/0005/806513/form-1a-medical-practitioner-report-of-a-death-to-a-coroner.pdf).

## Source admission and refresh rules

Current authority, event-time clinical standards and retrospective learning guidance are different roles. Retain all three where needed; a 2026 rule must not become the standard a clinician was presumed to know in 2024. Retrieval date is not publication date, search-engine freshness is not a new edition, and a past review date alone is not proof of withdrawal. Conflict resolution uses the issuer's current authoritative text and scope, not majority vote among pages.

Before operational use, verify the exact jurisdiction and service, current source revision and relevant local instrument. Record downloaded bytes/hash only if actually obtained; this planning register has no fabricated hashes. Use source snapshots within their rights and keep restricted documents in the authorised environment. A missing source disables its dependent rule, not independent synthetic research or already qualified source extraction.
