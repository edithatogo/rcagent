# Read-only investigation and Mermaid diagram inventory

This index is the engineering companion to [rcagent #162](https://github.com/edithatogo/rcagent/issues/162) and [native-diagram compatibility proposal #183](https://github.com/edithatogo/rcagent/issues/183).

The inventory uses the **existing** `skills/rca-investigation/assets/template-admission.json` manifest and files. It does not create a second source of truth for template admission, a new case record schema, or a Mermaid rendering engine. Its contract is deliberately bounded to repository inventory verification.

## Current classification

- **14 documented method guides**, including independently named Bow-Tie and generic barrier analysis, linked to existing rcagent proposal issues.
- **12 admitted portable-draft Mermaid templates**. Their source hashes, actual declared Mermaid keywords and method ownership are checked. `investigation-workflow.mmd` is a workflow view, not a fifteenth investigation method.
- **Nine proposed specialist diagram keywords** mapped to planning issues. They are explicitly `proposed-not-implemented`, not proof that Mermaid or rcagent supports them.
- Review processes such as HEAPS and death reviews retain separate Conductor ownership and are not confused with investigation methods.

Run the machine-readable inventory (no source changes):

```sh
uv run --no-sync python -m tools.diagram_inventory > diagram-inventory.json
uv run --no-sync python -m pytest -q tests/test_diagram_inventory.py
```

The JSON output contains `schema_version`, `source`, `admission_revision`, `native_diagram_claim`, `methods`, `templates` and `proposed_diagrams`. The report is a **diagnostic snapshot**; do not check it into the packaged skill, use it as an admission decision or infer clinical validity from it.

## Fail-closed checks

- Missing, unregistered, renamed or altered Mermaid template files.
- Source content digest mismatch against existing admission manifest.
- Unexpected or changed first Mermaid syntax keyword, even if the manifest digest was updated.
- Duplicate manifest keys/entries, unadmitted file status and malformed source inventory.
- Missing guide files or incorrect method-template relationships.

All test inputs are generated-synthetic. The CLI is read-only, returns a stable sorted report on success, and a nonzero exit with a source-specific error on failure.

## Boundaries

This validator does **not** parse or render Mermaid syntax, test method-specific analytical correctness, assert that a diagram type exists upstream, verify institutional sources, or authorise clinical use. The canonical template-admission machinery and source-revision validation remain authoritative for distribution, and clinical/policy/human review remains governed by existing Conductor tracks. The proposal figures in [PR #191](https://github.com/edithatogo/rcagent/pull/191) are separate, optional design mock-ups with their own assurance checks.

Implementation is reversible by reverting this read-only module, tests and documentation. No migration or release action is required.
