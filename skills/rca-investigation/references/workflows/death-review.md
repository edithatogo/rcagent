# Death review and mortality learning workflow

Use this workflow to prepare a source-grounded review packet and questions for authorised reviewers. It is portable guidance, not a qualified automated clinical review, death certificate, coronial determination or reporting service. Keep evidence, accounts, inference, proposed findings and accepted decisions distinct.

## 1. Establish scope and concurrent routes

Record the jurisdiction, organisation, care setting, review purpose, date range, available records, applicable policy revision and responsible human. Distinguish routine mortality screening, structured case review/M&M, clinical incident management, verification/certification of death, coronial reporting and specialty review. Several routes may apply concurrently. A death being expected does not rule out a care-quality question; an unexpected death does not establish error or preventability.

In NSW, CEC describes a [standardised death-screening approach](https://cec.health.nsw.gov.au/improving-practice-and-culture/end-of-life/death-screening-and-database-project). Its current tool and local completion process must be obtained where required. For M&M, use the principles in the [currently linked September 2020 guideline](https://cec.health.nsw.gov.au/improving-practice-and-culture/evaluate/morbidity-mortality-meetings), checking any older policy references against current sources.

For Queensland, establish the applicable HHS mortality/M&M process. The [Patient Safety directive QH-HSD-032](https://www.health.qld.gov.au/system-governance/policies-standards/health-service-directives/patient-safety) and [Clinical Incident Management Guideline QH-HSDGDL-032-2](https://www.health.qld.gov.au/system-governance/policies-standards/health-service-directives/patient-safety/clinical-incident-management) govern relevant incident questions; they do not make every death a SAC1 incident or prescribe RCA for every review.

Do not delay existing urgent escalation, evidence preservation or reporting processes while preparing an AI-assisted packet. Give unresolved questions an owner, not an invented answer.

## 2. Check source currency and authority

Record issuer, exact identifier, jurisdiction, publication/effective/review dates, retrieved version, authority, local applicability and uncertainty. Distinguish rules applying now from standards applying when the care occurred.

As checked on 13 November 2026 Australia/Brisbane:

- NSW CEC identifies [Incident Management PD2026_036](https://cec.health.nsw.gov.au/incident-management/policy), published 9 November 2026, with changed [definitions, review processes and timeframes](https://cec.health.nsw.gov.au/incident-management/policy/key-changes). Older pages still cite PD2020_047. The complete new directive was not retrieved for this workflow; verify its exact requirements before using a deadline or reporting rule.
- QLD QH-HSDGDL-032-2 has conflicting effective-date metadata: the page header says 1 July 2024; the approval block says 1 July 2027; version history lists 4.0 dated 13 March 2026. Preserve the conflict and verify current applicability rather than silently correcting it.

The workflow does not confer privilege or confidentiality. A protected statutory process, a service review and an ordinary M&M discussion have different requirements. Record confirmed protection only when the relevant authorised process and current legal basis are verified.

## 3. Build the evidence-backed trajectory

Use minimum necessary identifiers and the approved records environment. Do not place patient records in public issues, repository fixtures, CI, ordinary logs or an unapproved external model.

For each material event or assertion, retain the source identifier, inspectable page/span, who recorded or reported it, and extraction uncertainty. Keep event time, document time and information-availability time separate. Show uncertain dates, conflicting accounts and missing documents. Do not turn absent documentation into proof that care was omitted.

Prepare a concise trajectory of admission, transfers, recognition of deterioration, escalation, treatments and symptom care, documented goals/resuscitation decisions, and the recorded circumstances of death. Later autopsy, molecular/genetic, laboratory or coronial results belong to later knowledge states; they must not be attributed to an earlier clinical decision.

Regex, date parsers and NLP can flag dates, units, negation, uncertain expressions, medications and escalation/goals terms. Preserve raw text and ambiguity. A keyword match can raise a question but cannot establish diagnosis, causality or reportability.

## 4. Preserve patient, family and staff perspectives

Record actual concerns, goals, questions and responses with attribution. Show where family voice is absent, rather than manufacturing engagement. Include documented language, disability, cultural and access needs and relevant system constraints. Use respectful, trauma-informed language and avoid assumptions about identity or cultural wishes.

Ask what remains unanswered about deterioration, communication, transitions, end-of-life goals and care. Preserve reasonable alternatives and disagreement. The current NSW [incident implementation guidance](https://cec.health.nsw.gov.au/incident-management/policy/key-changes) and Queensland [clinical-incident guideline](https://www.health.qld.gov.au/system-governance/policies-standards/health-service-directives/patient-safety/clinical-incident-management) support person/family-focused learning; consultation itself remains a human process.

## 5. Separate quality, causality and preventability

Use separate headings for documented care, possible quality concerns, causal hypotheses, competing explanations, information gaps and questions for authorised assessment. Make assumptions in a counterfactual explicit. Model confidence and agreement do not establish the probability that a death was preventable.

The [Queensland Maternal and Perinatal Quality Council](https://www.clinicalexcellence.qld.gov.au/committees-and-networks/quality-assurance-committees/queensland-maternal-and-perinatal-quality-council) expressly distinguishes possible care improvement from proof that a death could have been prevented. Apply that distinction throughout the packet. Do not generate a final preventability, negligence, blame or cause-of-death verdict.

## 6. Surface jurisdiction and specialty questions

Use current official sources and the service's authorised reviewer to decide applicability. The following sources identify distinct routes; they are not interchangeable checklists:

| Question | Official source / limit |
|---|---|
| NSW verification/certification | [PD2023_014](https://www1.health.nsw.gov.au/pds/ActivePDSDocuments/PD2023_014.pdf); record existing practitioner documentation, never make the determination |
| NSW coronial obligations | [PD2024_036](https://www1.health.nsw.gov.au/pds/ActivePDSDocuments/PD2024_036.pdf); keep coronial reporting separate from mortality review |
| QLD coronial obligations | [Coroners Court health-professional guidance](https://www.coronerscourt.qld.gov.au/for-health-professionals) and [current Coroners Act 2003](https://www.legislation.qld.gov.au/view/whole/html/current/act-2003-013); seek authorised advice when uncertain |
| NSW maternal deaths | [PD2026_019](https://www1.health.nsw.gov.au/pds/ActivePDSDocuments/PD2026_019.pdf), replacing PD2021_006; preserve the current maternal and concurrent-route questions |
| NSW perinatal deaths | [PD2022_046](https://www1.health.nsw.gov.au/pds/ActivePDSDocuments/PD2022_046.pdf); verify current committee/destination and new incident-policy references |
| QLD maternal/perinatal deaths | [QMPQC](https://www.clinicalexcellence.qld.gov.au/committees-and-networks/quality-assurance-committees/queensland-maternal-and-perinatal-quality-council); use current specialty audit/reporting process |
| QLD anaesthetic/sedation deaths | [QPPAMRC](https://www.clinicalexcellence.qld.gov.au/committees-and-networks/quality-assurance-committees/queensland-perioperative-and-periprocedural-anaesthetic-mortality-review-committee); a specialty review scope is not proof of causation |
| NSW surgical review | [CHASM](https://cec.health.nsw.gov.au/incident-management/committees/chasm); previous method ended in 2025 and redesign began in 2026, so verify the current destination |

Also identify paediatric/sudden unexpected infant death, mental-health/suicide, custody/care, disability, violence/neglect and other specialty questions when supported by the case. Retrieve the current applicable pathway rather than extrapolating from the sources above. Do not automatically submit records, contact families or decide reportability.

## 7. Verify and hand off learning

Check material claims against original evidence, including negation, dose/unit, actor and time. If another modality or model is used, preserve which source and method produced each assertion. OCR and text from one document are not independent corroboration. Different models can share errors; agreement is insufficient verification. Expose disagreements and unresolved issues to the human reviewer.

Produce a compact packet: scope/authority; evidence index; supported chronology; documented perspectives; separate quality/causality/preventability questions; concurrent-route questions; and proposed actions. Each action needs an evidence link, responsible role, mechanism, authorising human, due-date basis, intended outcome and balancing measure. Distinguish action completion from demonstrated benefit.

Label the output as draft or evidence-checked questions until accepted by the relevant authorised person. Preserve the qualified scope, sources, omissions, corrections and model/rule versions. If evidence is inadequate, provide the supported chronology and unanswered questions with explicit limits.
