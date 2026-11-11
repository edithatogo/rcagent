# Sax Institute patient complaints evidence (2022–2024)

Source-first reference register for the RCA / Cognitive Autopsy research workbench. Verified 12 November 2026. These links are **external original sources**, not local copies of the publications. Do not conflate the 2022 commissioned Evidence Check with the updated 2024 peer-reviewed review.

## Source inventory

| ID | Publication | Authoritative source | Files / appendices | Rights and disposition |
|---|---|---|---|---|
| SAX-2022 | Schultz TJ, Zhou M, Gray J, Roseleur J, Clark R, Mordaunt DA, Hibbert P. *Patient characteristics and interventions associated with complaints and medico-legal claims*. Sax Institute Evidence Check for Avant Insurance Limited (report dated November 2022; website publication 2023). DOI [10.57022/lioq6047](https://doi.org/10.57022/lioq6047). | [Sax landing page](https://www.saxinstitute.org.au/evidence-check/patient-characteristics-and-interventions-associated-with-complaints-and-medico-legal-claims/); [publisher PDF](https://www.saxinstitute.org.au/wp-content/uploads/Patient-characteristics-and-interventions-associated-with-complaints-and-medico-legal-claims.pdf) | Appendix 1: search strategy; Appendix 2: PRISMA flowchart; Appendix 3: evidence grading; Appendix 4: data extraction tables. All are within publisher PDF. | © Avant 2022. Acknowledged non-commercial reproduction is permitted by the report notice; wider redistribution or commercial use needs permission. Prefer canonical link over committing a copy until reuse implications are reviewed. |
| SR-2024 | Schultz TJ, Zhou M, Gray J, Roseleur J, Clark R, Mordaunt DA, Hibbert PD, Haysom G, Wright M. *Patient characteristics of, and remedial interventions for, complaints and medico-legal claims against doctors: a rapid review of the literature*. *Systematic Reviews* 2024;13:104. DOI [10.1186/s13643-024-02501-8](https://doi.org/10.1186/s13643-024-02501-8). | [Journal article](https://link.springer.com/article/10.1186/s13643-024-02501-8); [publisher PDF](https://link.springer.com/content/pdf/10.1186/s13643-024-02501-8.pdf); [PMC record](https://pmc.ncbi.nlm.nih.gov/articles/PMC11003134/) | [Publisher supplementary DOCX, Additional file 1](https://static-content.springer.com/esm/art%3A10.1186%2Fs13643-024-02501-8/MediaObjects/13643_2024_2501_MOESM1_ESM.docx), tables S1–S7 | Published open access under [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), subject to any third-party credits and specific exceptions. |

## Supplementary file map (SR-2024)

- **S1–S3:** Search strategies for PubMed, Scopus, and Web of Science (8 September 2022).
- **S4:** Design and NHMRC levels of evidence for included studies.
- **S5:** Quality appraisals of eight comparative studies with concurrent controls.
- **S6:** Quality appraisals of three systematic reviews.
- **S7:** Quality appraisals of fourteen uncontrolled pre/post studies.

## Evidence interpretation guardrails

- Both works are **secondary evidence**, not original complaints datasets. No patient-level data, confidential commissioned material, or raw complaints should be inferred or imported.
- The 2024 review included 25 studies (7 addressing patient characteristics and 18 addressing interventions). Evidence of intervention effectiveness is generally **very weak**, with major risks of confounding and bias; do not encode causal effectiveness or patient-level propensity scores from this review.
- Keep the Sax report and journal article separately versioned; search updates, eligibility, evidence tables and findings are not necessarily identical.
- Avoid using patient characteristics as a proxy for complaint credibility or as a reason to dismiss a complaint.
- Treat bibliographic metadata, methodological extraction tables, normative interpretation and operational evaluation as separate provenance layers.
- If PDFs/DOCX are subsequently vendored, preserve exact original bytes, calculate SHA-256 checksums, document retrieval date and source URL, and check redistribution permissions. **No source binaries were vendored in this change.**

## Suggested integration points

1. Map the two review questions and study-level evidence-quality fields into research/evaluation contracts; do not directly modify triage decisions.
2. Compare complaint taxonomies and study designs against synthetic cases; require human review before any clinical or regulatory inference.
3. Add tests that prevent the workbench from treating correlation, low-quality before–after evidence, or lack of evidence as proof of a patient characteristic or intervention effect.

Provenance: Sax Institute official publication and Springer Nature article/supplement, verified 2026-11-12. Bibliographic citations and external links only.
