# Component-study planning refinement evidence

Date: 2026-11-07. Scope: documentation, bibliographies, dataset metadata, experiment catalogue and Conductor plans only.

## Reviewed bases and scope

- rcagent draft head before refinement: 1ad436ff50d9f269efa5078130d84028f87e1b91.
- learningfromharm draft head: d71764ddb292751f5df97a9fac0e9799ae20f496.
- corpus-cases-medilegal-nz draft head: 39d9f4c02338d4bf61ca831f979f07abae8fb051.

The owner requested small literature gaps, conventional NLP comparisons, supplemental datasets, behavioural economics, controlled cases, process mining, dependency reuse and verification. The updated plan contains eight prospective questions and 25 bounded coding-agent packages. The candidate register contains eight NLP families and two process-log datasets; all are unadmitted. The component bibliography adds 31 entries to the existing 12.

No inference, weight adaptation, patient/clinician study, source-payload acquisition, data release, new dependency installation or clinical qualification was performed. Existing code and historical negative results remain intact. The qualified-profile and run-receipt lists are empty.

## Verification performed

- python tools/validate_repository.py: passed the repository governance checks.
- Initial unstaged whitespace checks passed. The first staged check additionally detected surplus blank EOF lines in three new files; these were removed and the staged check rerun. Whitespace-only normalisation after hashed reviews does not change their semantic findings.
- Changed JSON/JSONL syntax and relative Markdown links were checked, using authenticated remote trees for files not materialised in the two companion repositories.
- Candidate dataset IDs and citation keys were reconciled; selected revisions/checksums/admission remain empty.
- Both bibliography files have unique keys and balanced structural braces. No full BibTeX parser was available; no parser-level pass is claimed.
- The 25 work-package dependency graph has no cycles or unknown IDs. Study task IDs, dataset aliases and repository-root source-register paths resolve.
- Materialised companion-file baselines were compared with authenticated remote blob hashes before replacement.
- The three remaining draft-track links identified during review were changed to the coordinated branch and checked by the coordinator.

These checks establish planning consistency, not runtime performance or empirical reference quality.

## Agent repository review

Three new fresh-context reviewer tasks were attempted and each failed at the platform level with an incomplete-response/max-output-tokens error before providing a review. They are not counted as completed reviews.

Three existing agents then performed bounded cross-reviews of documents they had not authored, with the approved repository roles:

- [Evidence integrity](./reviews/evidence-integrity.md): scientific claims, outcomes and reference/metric consistency.
- [Acceptance and reproducibility](./reviews/acceptance.md): dependency semantics, paths, architecture and implementation boundaries.
- [Safety and privacy](./reviews/safety-privacy.md): packet leakage, reference circularity, unsupported claims and cross-stage controls.

The review files contain instructions/scope, findings, exact file hashes where recorded, closure checks and limitations. Exact serving-model revisions were not exposed. These are context-aware agent reviews, not fresh/blinded review, independent-model agreement, human clinical validation or numerical study scoring. Shared context and correlated errors remain limitations.

## Findings and disposition

All identified planning findings were corrected: CS04 now tests fixed-risk framing only; CS08 measures directional quality/error improvement at a fixed evidence budget with burden separate; optional framing/encoder branches no longer block initial analysis/adaptation; calibration requires frozen case-family splits; simple availability/risk fixtures do not require later mechanistic worlds; catalogue paths resolve from the repository root; every generation/verification/retrieval/render stage is bound to the same immutable permitted view; and the reference inventory is frozen, source-linked, attributed and cannot consist solely of the candidate's own output.

Reviewers confirmed closure of their substantive findings. The coordinator corrected adjacent draft-index links. No remaining hard-gate finding was identified within the documentation review scope. Future model, data, privacy-boundary and clinical claims still require their own evidence.

## Delivery and rollback

Update the three existing planning branches without rewriting history, with expected-head checks and remote blob readback. This receipt does not claim a merge or deployment. Reverting the bounded planning commits restores the preceding plans; original sources and previous receipts are preserved.
