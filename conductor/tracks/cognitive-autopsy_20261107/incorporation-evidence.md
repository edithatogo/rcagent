# Owner incorporation evidence — 8 November 2026

## Scope and baselines

The owner requested incorporation of the preceding recommendations into relevant repositories. The existing eight-study/25-package programme is retained. This increment reconciles ownership and four planning ambiguities, adds bounded generic owner plans, and repairs a type-only hosted delivery failure. It does not execute a cognitive-autopsy study, admit data or qualify a model.

| Repository | Reviewed base | Delivery |
| --- | --- | --- |
| rcagent | `0c8607661e64a34b351b87ca1c6148d0e291fbed` | Existing PR 117 |
| learningfromharm | `a9c5bdba7018ca5c71e460bbc2f6db9a43dfe71b` | Existing PR 8 |
| corpus-cases-medilegal-nz | `06fcf44987a783a0883e1867da0c4231d2ad7f0d` | Existing PR 30 |
| sourceright | `3a603ec8344e9865c68998d48eca573499d3fb5d` | PR 133; Track 110 |
| searchright | `4bfffc43e25641962fca394d43446888376156b4` | PR 759; existing Track 13 |
| nlp-policy-nz | `e2940f045ad2e065ef2b406843db10c7e850f0f6` | PR 358; source-fidelity track |

Voiage's existing optional outcome boundary was inspected at `862d510f1cd0420d32c7b84734066ee6d6f291bb`. No new numerical implementation or mandatory upstream track was needed. Process engines, simulation and other optional candidates remain consumer-side investigations until a generic gap is demonstrated.

## Findings addressed

- Correct the stale description of the corpus GitHub repository as archived without moving capture from archive-govt-nz or neutral extraction from nlp-policy-nz. Preserve the existing Hugging Face public dataset identity and source/research separation.
- Use the fixed-evidence-budget CS08 question, with burden separate; do not restore a cost-ratio endpoint.
- Allow source-linked HDC/synthetic support labels in CAW09, keeping external NLI/error datasets optional.
- Separate training vocabulary/parameter fitting, development tuning and calibration; name all partitions in CAW03.
- Include PLOS Digital Health in the coordinating publication strategy.
- Correct SourceRight/SearchRight CAW10 mapping to temporal entitlement; contradictory-evidence retrieval remains a separate consumer requirement.
- Repair inherited cross-repository reference links and pin the inspected NLP source reference.
- Add an explicit existing-contracts selected-system value and a null unresolved protected approval reference with a typed pending-link status. Existing HDC ethics remains owner-confirmed.
- Retain the actual rcagent coordinator track ID with a hyphen. The companion's local underscore ID is a different repository-local identifier, not a broken cross-reference.
- Clarify routine and reserved actions without adding a repeated HDC approval checkpoint.

## Agent review

Three roles cross-reviewed the planning changes and closed their bounded findings:

- [Acceptance/evidence review](./reviews/incorporation-acceptance.md).
- [Engineering/evidence-integrity review](./reviews/incorporation-engineering.md).
- [Safety/privacy and source ownership](./reviews/incorporation-source.md).

These are existing-context agent cross-reviews. The receipts identify authorship overlaps, reviewed bytes and excluded scope. They are not fresh/blinded, independent-model, human or clinical validation; exact serving model revisions were not exposed. Later navigation, receipt/metadata updates and explicit training-partition wording receive integrator inspection rather than being falsely attributed to the earlier byte hashes. Track completion and empirical qualification remain pending.

## Local verification and limits

- rcagent repository governance validation passed. Changed JSON/JSONL, relative document links, the 25-task acyclic graph, citation keys and unexecuted/unadmitted state are checked by the delivery validation. The bibliography remains 43 unique structurally checked entries; no full BibTeX parser claim is made.
- The hosted Quality failure at run `42382431050` was ty 0.0.99's deprecated `@contextmanager` Iterator annotation. The repair changes only the import and `_locked` return annotation to `Generator[None, None, None]`; locking behaviour and compiled function bytecode are unchanged.
- An isolated CI-version environment (Python 3.13.15, ty 0.0.99, Ruff 0.16.4, basedpyright 1.39.10, pytest 9.1.1) passed all 108 existing autonomy tests, full Ruff, ty and basedpyright checks. No suppression or gate downgrade was used.
- The broader local rcagent suite produced 1,723 passes, 11 skips and 52 failures among socket-dependent tests in this restricted execution environment. A representative transport fixture fails at socket creation with `PermissionError: [Errno 1] Operation not permitted`; the corresponding session tests cannot establish a captured session. This is not recorded as a full local pass. Exact-head hosted CI remains the integration evidence.
- SourceRight's metadata, paths, added links and whitespace checks passed. Cargo was unavailable locally; no native pass is claimed.
- SearchRight passed 235 Python tests (one skipped) and all 57 static-harness gates on a clean committed candidate, including strict source-package reproducibility and generated binding checks. The full verification entry point then stopped with exit 2 because Cargo was unavailable. Initial duplicate-task/projection drift was removed, source hashes regenerated, and the existing locked binding tools installed without dependency-file changes. Hosted native admission remains separate.
- nlp-policy-nz passed added/new link, JSON, dependency/optional-task and whitespace checks. Its existing HDC YAML is byte-identical; implementation/qualification/publication flags remain pending.

## Delivery evidence

At published head `8ad5d12ce30837f33027fa3f409bdbe2821fadaa`, [hosted Quality run 42423244614](https://github.com/edithatogo/rcagent/actions/runs/42423244614) passed its Ubuntu (1,786 tests; 95.29% total coverage) and macOS jobs. Dependency Review, Vale and the Codecov patch check also passed. Windows stopped at ty before its full suite: the dynamically indexed executable-name list selected a deprecated `shutil.which` overload under the Python 3.11 target. The follow-on repair gives the already-validated list an explicit `list[str]` local binding and retains the existing lookup calls. Windows-target ty, all 37 existing runtime-lab tests, Ruff and basedpyright passed locally; the integrator inspected the validation path and exact diff. Hosted results for the follow-on head remain a separate delivery gate.

The initial incorporation payloads were verified against all 58 published file blobs across the six repositories. Final navigation follow-ups replace temporary coordinated-branch links with immutable reviewed revisions so automatic branch deletion cannot break the references. This mechanical link change does not expand the earlier review receipts' byte scope. Reference pins identify planning evidence, not qualified releases; implementation still selects compatible release revisions.

Use the linked PRs for exact final heads, hosted checks, review-thread dispositions and merge state. Remote file/tree comparisons must match the reviewed local payloads before completion is reported. This receipt records local work and limitations; it does not predict a future CI result or a merge. No default branch is force-updated and no safety, privacy, review or required hosted check is bypassed.

No patient-bearing payload, model weights or research results were uploaded. No dataset release, participant observation, training run or operational capability was created by incorporating these plans.
