# Death-review planning verification

## Delivered scope

Track 14 specification, staged plan, metadata and evidence ledger; official NSW/QLD source register and original crosswalk; proposed workflow/evaluation contract; a portable skill reference; and eight wholly synthetic acceptance-design cases. This delivery includes planning/guidance and a bounded jurisdiction-registry safety fix. No patient records, real death cases, model experiments, statutory submissions or clinical validation were performed.

## Scoped checks

A Python validation command run in the integration worktree parsed all three JSON files and every evidence-ledger line, checked the ledger's required fields, verified required source metadata and unique identifiers, checked source references in the synthetic catalogue, and resolved local Markdown links in the owned paths.

Observed result before this receipt was added: **10 files checked, 3 JSON files, 19 sources, 8 synthetic design cases, 0 local-link errors; exit code 0**. Public source URLs were researched separately; a syntactically valid URL is not claimed to have passed an automated live-link test.

The source review preserved unresolved currentness/access issues: complete PD2026_036 text and effective arrangements; conflicting QLD guideline effective-date metadata; unavailable current local mortality/screening instruments; and NSW specialty programme/committee transitions. These gaps block the dependent current-rule automation, not the bounded planning delivery.

## Remaining integration and capability work

The integration owner handles the Track 14 GitHub issue, shared roadmap/index/skill routing, current-policy registry changes, agent review and whole-repository checks. No commit or external write was made by this lane. The synthetic catalogue is an acceptance design, not an implemented or passed clinical test suite. Every executable study, component qualification and operational decision remains pending in the plan.

## Jurisdiction source-transition implementation

At the integration owner's request, the lane also changed `conductor/jurisdictions/registry.json`, `conductor/schemas/jurisdiction-pack.schema.json`, `tools/jurisdiction_pack.py` and `tests/test_jurisdiction_pack.py`.

Registry version 1.1.0 adds separate current CEC transition evidence and the unavailable complete PD2026_036 source. The two formerly active 2020 incident mappings now use `pending_source_verification`, have null deadlines and explicit uncertainty, and block the NSW pack. Source retrieval requires no new owner decision. Historical PD2020_047 bytes/checksum, retrieval timestamp and decision remain recorded. Unavailable authority cannot be activated by an owner approval. Under-review behaviour remains covered using a synthetic source/rule rather than a manufactured real-policy status. Required people/culture/system safeguards were retained.

QLD SAC1 report/analysis deadlines remain active with direct QH-HSD-032 authority; the guideline's conflicting date metadata is recorded without asserting issuer withdrawal.

Observed verification:

- `.venv/bin/ruff format tools/jurisdiction_pack.py tests/test_jurisdiction_pack.py`: applied formatting to both files.
- `.venv/bin/python -m pytest -q tests/test_jurisdiction_pack.py`: **28 passed**.
- `.venv/bin/python -m tools.jurisdiction_pack validate`: **passed**.
- `.venv/bin/ruff check tools/jurisdiction_pack.py tests/test_jurisdiction_pack.py`: **passed**.
- `.venv/bin/python -m mypy tools/jurisdiction_pack.py tests/test_jurisdiction_pack.py`: **not run successfully; the main worktree environment has no mypy module**. Full strict-environment validation remains with integration.

The new source-verification state does not retrieve or interpret the missing directive, enable clinical capabilities, or resolve operational policy applicability. Full PD2026_036 verification and the other source questions remain open in Phase 1.
