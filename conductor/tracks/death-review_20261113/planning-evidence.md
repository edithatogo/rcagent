# Death-review planning verification

## Delivered scope

Track 14 specification, staged plan, metadata and evidence ledger; official NSW/QLD source register and original crosswalk; proposed workflow/evaluation contract; a portable skill reference; and eight wholly synthetic acceptance-design cases. This delivery includes planning/guidance and a bounded jurisdiction-registry safety fix. No patient records, real death cases, model experiments, statutory submissions or clinical validation were performed.

## Scoped checks

A Python validation command run in the integration worktree parsed all three JSON files and every evidence-ledger line, checked the ledger's required fields, verified required source metadata and unique identifiers, checked source references in the synthetic catalogue, and resolved local Markdown links in the owned paths.

Observed result before this receipt was added: **10 files checked, 3 JSON files, 19 sources, 8 synthetic design cases, 0 local-link errors; exit code 0**. Public source URLs were researched separately; a syntactically valid URL is not claimed to have passed an automated live-link test.

The source review preserved unresolved currentness/access issues: complete PD2026_036 text and effective arrangements; conflicting QLD guideline effective-date metadata; unavailable current local mortality/screening instruments; and NSW specialty programme/committee transitions. These gaps block the dependent current-rule automation, not the bounded planning delivery.

## Completed planning and source integration

Track 14 is registered as [issue 126](https://github.com/edithatogo/rcagent/issues/126), with shared Conductor roadmap/index/skill routing and the source-transition registry integrated. The root completed the integration review after the shared-context agent panel and its bounded corrections. The [integrated review receipt](../frontier-assurance_20261113/review.md) records three substantive cross-review scopes plus root integration review, including review of assigned repairs; these are agent engineering reviews, not independent human or clinical observations.

Planning and source integration are complete. The overall scientific track remains open. The eight synthetic cases remain an acceptance design, not an implemented or passed clinical test suite; model studies, component qualification and operational clinical decisions remain pending. The current NSW directive's full text and other source uncertainties below are still unresolved.

The delivery is in [PR 127](https://github.com/edithatogo/rcagent/pull/127). At this documentation handoff, the integration owner records head `d0771fc4670552a4785d2ac56666561379f44eff` as queued for hosted CI. No hosted pass or merge is claimed here; later observed results belong in the delivery receipt.

## Integrated engineering verification

The [root delivery evidence](../frontier-assurance_20261113/delivery-evidence.md) records locked dependency resolution, Ruff and formatting, ty, strict basedpyright 1.40.2 with a non-growth baseline, Bandit, Vulture, Unicode, repository and benchmark contracts as passed on the integrated code. Seven deterministic benchmark cases passed. The strict typing baseline is explicit remaining debt, not a claim that the entire repository has zero type diagnostics.

The complete local validation run recorded **1,890 passed, 11 skipped and 53 failed**. Of the failures, 52 were attributed to the environment's existing AF_UNIX restriction; the remaining Hypothesis timing flake was addressed with a finite 1,000 ms correctness budget and retained regression example. The focused coverage rerun passed all four properties without disabling health checks or reducing generated ranges. These results are not a full local suite pass and do not replace hosted platform evidence.

The integrated receipt also records 80 packaging/admission and 50 evidence-core tests for the privacy review, 67 report-gate/validation-command tests after the platform adapter, 23 of 23 real mutation kills, a completed 300-iteration synthetic Scalene workload and live Agent Skills conformance. Those are engineering observations within their recorded scopes; they do not implement or qualify the death-review design cases. Historical scoped checks below are preserved.

## Jurisdiction source-transition implementation

At the integration owner's request, the lane also changed `conductor/jurisdictions/registry.json`, `conductor/schemas/jurisdiction-pack.schema.json`, `tools/jurisdiction_pack.py` and `tests/test_jurisdiction_pack.py`.

Registry version 1.1.0 adds separate current CEC transition evidence and the unavailable complete PD2026_036 source. The two formerly active 2020 incident mappings now use `pending_source_verification`, have null deadlines and explicit uncertainty, and block the NSW pack. Source retrieval requires no new owner decision. Historical PD2020_047 bytes/checksum, retrieval timestamp and decision remain recorded. Unavailable authority cannot be activated by an owner approval. Under-review behaviour remains covered using a synthetic source/rule rather than a manufactured real-policy status. Required people/culture/system safeguards were retained.

QLD SAC1 report/analysis deadlines remain active with direct QH-HSD-032 authority; the guideline's conflicting date metadata is recorded without asserting issuer withdrawal.

Observed verification:

- `.venv/bin/ruff format tools/jurisdiction_pack.py tests/test_jurisdiction_pack.py`: applied formatting to both files.
- `.venv/bin/python -m pytest -q tests/test_jurisdiction_pack.py`: **28 passed**.
- `.venv/bin/python -m tools.jurisdiction_pack validate`: **passed**.
- `.venv/bin/ruff check tools/jurisdiction_pack.py tests/test_jurisdiction_pack.py`: **passed**.
- `.venv/bin/python -m mypy tools/jurisdiction_pack.py tests/test_jurisdiction_pack.py`: **not run successfully; that scoped worktree environment had no mypy module**. This historical attempt is preserved; the integrated typing gates used ty and strict basedpyright, with results linked above.

The new source-verification state does not retrieve or interpret the missing directive, enable clinical capabilities, or resolve operational policy applicability. Full PD2026_036 verification and the other source questions remain open in Phase 1.
