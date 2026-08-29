# SourceRight adapter fit-gap

## Observed source

- Repository: `https://github.com/edithatogo/sourceright`
- Historical discovery HEAD: `aa57f115d0d6914d29dd7787a6382cb1432109cd`
- Current vendored pin observed for Track 07: `c5fa583`
- Reconciliation date: 2026-08-29
- Current vendored checkout state: clean. Track 02 recorded inherited offline
  13/13 evidence, but Track 07 did not invoke SourceRight and does not promote
  that inherited evidence into a Track 07 success claim.

The observed CLI documentation describes deterministic surfaces for CSL
validation, reference-integrity reports, citation reconciliation, review
queues, claim/source provenance, policy checks, exports, benchmarks,
citation-manager preview/sync, plugin inspection, and MCP inspection. It also
states important boundaries: claim provenance does not assert truth; policy
checks do not perform semantic relevance; conflicts remain review-required;
and live Zotero transport is opt-in.

## Selected responsibility boundary

SourceRight owns bibliographic integrity and claim-to-source provenance:

- canonical CSL validation and diagnostics;
- manuscript citation/reference reconciliation;
- DOI and metadata conflict reporting;
- reference review queues;
- claim/source graph generation;
- deterministic reference-policy checks; and
- citation-workflow receipts exposed through CLI or an evaluated MCP adapter.

The Safety Systems Workbench owns:

- problem and question formulation;
- literature-provider search orchestration;
- screening, deduplication and eligibility decisions;
- critical appraisal, study quality and evidence certainty;
- applicability to a finding, control, intervention or local context;
- recommendation rationale and implementation/effectiveness linkage; and
- clinical-governance review and acceptance.

Neither component may represent citation correctness as evidence that a claim
is true or a recommendation is safe.

## Adapter sequence

1. Track 01 records SourceRight as an optional shared dependency, not portable
   core.
2. Track 02 defines literature query, candidate, screened-study, citation,
   claim-link and recommendation-rationale contracts.
3. Track 05 creates synthetic contract fixtures and benchmark assertions.
4. Track 07 validates the fail-closed adapter contract against the clean pin;
   bounded CLI execution remains unavailable in this track unless an exact
   invocation and output receipt is admitted. MCP remains unevaluated.
5. The adapter uses structured JSON, exact executable and source revisions,
   bounded inputs, timeouts, no implicit network, and review-required conflict
   states.
6. A missing or incompatible SourceRight installation falls back to preserved
   CSL and screening artefacts with citation verification explicitly
   unavailable; it never silently marks citations verified.

## Gaps and upstream path

- Literature-provider discovery is not assigned to SourceRight by the
  currently observed command contract; use replaceable search adapters rather
  than adding provider-specific search to the workbench core.
- A stable machine-readable contract for every required command must be
  verified against a clean pinned revision before adoption.
- Generic healthcare-neutral improvements to structured outputs, provenance,
  or adapter ergonomics should be proposed upstream in SourceRight.
- The local adapter expires when SourceRight publishes an equivalent supported
  integration contract or when benchmark evidence rejects it.
