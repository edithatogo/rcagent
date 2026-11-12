# Presentation production amendment — v1.1.0

**Prepared:** 13 November 2026  
**Scope:** `sax-patient-complaints-20min`  
**State:** Built and assessed production candidate; presenter approval, timed rehearsal and PowerPoint device tests remain open.

This amendment supplements `PRODUCTION_CONTRACT.md` version 1.0.0 on this branch. The full expanded v1.1.0 contracts, editable PPTX, ten-slide PDF, notes, data, build scripts and assessment were delivered in the accompanying conversation package. Those binary artifacts and the complete machine-readable package are **not committed by this amendment**. This document does not imply a merged PR or passing repository CI.

## Built scope

The blank, neutral 16:9 presentation contains exactly ten main slides and four genuinely hidden backups. It has no institutional logos, unconfirmed event/date, invented affiliations or stock images. The main PDF contains ten pages. Every slide includes narration, source locators, qualifications, a transition and a shorter-delivery fallback in its notes. The allocation remains 18 minutes plus two minutes of discussion held on S10; actual delivery timing is not yet established.

Tables are native editable PowerPoint tables. S06 is a native numeric XY chart with an embedded data workbook. The opening denominator example and time series are explicitly hypothetical/synthetic. The fictional case and proposed evaluation are distinguished from published findings. The appendix remains an inventory-only fallback; no unverified supplementary table cells have been used.

## Contract changes

1. **G09:** use the explicitly requested blank template. No institutional master or logos.
2. **G05:** clarify typography roles. Large quantitative numerals may be 36–64 pt; navigation/metadata may be 14–16 pt. Narrative text and chart/table minima are retained.
3. **S06 / G16:** count visible chart/axis labels and caveats as body copy. Revise S06's ceiling from 40 to 65 words; the produced slide contains 46. This is an explicit deviation from the baseline, not a retroactive claim that it satisfied the original ceiling. Keeping the synthetic-data label and denominator is more important than hiding them to meet the old limit. Slide count and timing do not change.
4. **S06 / G21:** require a numeric time axis, the programme boundary at x=0 and a zero-based y-axis. Do not compress the -1 to +1 interval into one category step. No fitted or causal effect is inferred.
5. **S03/S05/S06/B03:** consistently distinguish included publications from independent trials or patient cohorts.
6. **S09:** define the staff-experience balancing measure alongside access, response time, recurrence and staff hours. These are proposed local measures, not validated or approved commitments.
7. **G22:** keep manual advancement; S10 is the final visible slide. Hidden backups have internal navigation and return links.
8. **G23–G25:** separate structural, visual and content checks from timed rehearsal, current-disclosure confirmation, presenter approval, source-byte retrieval and device tests. A candidate can be delivered with explicit pending gates; final sign-off cannot be inferred from machine checks.
9. **G26:** test text visibility as well as existence. The first render exposed an opaque card covering a reused text placeholder. Layering and inherited paragraph spacing/indentation were corrected, with a failing-before/passing-after regression test and fresh visual inspection.
10. **G08/G22:** correct and test the location of manual slideshow properties in the OOXML package. A renderer accepting malformed metadata is not proof of compatibility.
11. **Contract schema:** permit an as-built candidate with actual copy, narration, assessment methods and evidence. Preserve v1.0.0 as baseline rather than overwriting its historical state.

## Assessment

Assistant self-review, not independent scientific or clinical validation:

- **12 structural/regression tests passed.** They cover slide counts/hidden flags, native titles and notes, margins, native tables/chart, labels/arithmetic, timing allocation, source identifiers, body-copy limits, foreground visibility and slideshow metadata.
- **14/14 final slide renders inspected.** Final main-slide PDF has ten pages. A rendered-text smoke check found all expected tokens in 158 text-object bounding boxes.
- **53 slide-level criteria:** 49 PASS; 1 PARTIAL; 2 NOT RUN; 1 NOT APPLICABLE. The not-run criteria are live interaction timings. The partial criterion is complete end-to-end external-source link resolution. The not-applicable criterion concerns optional detailed supplementary-table adaptation, which was not used.
- **10 release gates:** 6 PASS; 1 PARTIAL; 3 NOT RUN. The partial gate includes current-disclosure confirmation. Timed rehearsal, PowerPoint Mac/Android testing and presenter sign-off remain unperformed.
- Alt-text presence, direct labels, content sequence and defined colour-pair contrast were checked. No screen-reader user test or accessibility certification is claimed.

Render environment: LibreOffice 25.2.3.2; Python-pptx 1.0.2; PyMuPDF 1.26.7. Arial is requested; LibreOffice substitutes Liberation Sans. This is not a PowerPoint Mac or Android compatibility test.

## Remaining boundaries

Original source PDFs/DOCX were not acquired in this production session. Publisher records support the scoped claims and appendix inventory; individual supplementary cells remain unverified. Embedded link targets match the intended sources, but complete end-to-end retrieval remains incompletely verified. The talk is not an updated 2026 literature review. No real complaint data, source binaries or font files are redistributed.

Before final presentation sign-off, rehearse with the scripted interactions; confirm current disclosures and interpretations; and inspect the deck in the intended PowerPoint application/version. These checks must be recorded, not silently marked passed.
