# Context Pack: Track 08 Local Runtime and Model Lab

- **Track:** `local-runtime-model-lab_20260731`
- **GitHub issue:** [#13](https://github.com/edithatogo/rcagent/issues/13)
- **Base revision:** `20e38e36008c42104d7ee750e691d05870392443`
- **Created:** `2026-08-29T08:33:37Z`
- **Fresh until:** any dependency, runtime registry, model admission, or execution-policy change
- **Privacy mode:** fully local, generated synthetic/public metadata only
- **Context budget:** Track 08 plus the three archived dependency receipts and directly reused contracts
- **Owned files:** `tools/runtime_lab.py`, `tests/test_runtime_lab.py`, `evaluation/runtime-lab/`, Track 08 Conductor records, and bounded comparator hardening

## Objective and Acceptance

Provide model-free device discovery, strict runtime/model admission, fail-closed
routing, operator-owned offline-bundle verification and a dated negative
recommendation matrix. No new runtime or model is downloaded or executed.

## Authoritative Inputs

| Input | Revision or date | Why needed | Authority | Freshness |
|---|---|---|---|---|
| Track 08 specification | 2026-07-31 | scope and acceptance | repository contract | current |
| Product guidelines | 2026-08-29 checkout | privacy and authority boundaries | repository policy | source change |
| Decisions 20260829-002 and 004 | 2026-08-29 | bounded comparator and agent-panel rules | owner decisions | decision change |
| Runtime registry schema 1.0 | 2026-08-29 | admission and negative support states | Track 08 contract | schema change |

## Dependencies and Receipts

- Track 05: `conductor/archive/benchmark-evaluation-harness_20260731/evidence/completion-receipt-20260829.md`.
- Track 06: `conductor/archive/multimodal-capability-fabric_20260731/evidence/completion-receipt-20260829.md`.
- Track 07: `conductor/archive/retrieval-knowledge-system_20260731/evidence/completion-20260829.md`.

## Decisions, Risks, and Assumptions

- Existing local comparators may be reused only after their exact admission checks; their negative result is not support or promotion evidence.
- New downloads, external inference, paid compute, remote code and promotion remain pending gates.
- Missing heterogeneous hardware is a negative evidence result, not permission to infer performance.

## Excluded Context

- Model weights, private clinical or employee data, credentials, host identifiers, vendor claims, and external inference.

## Commands and Fixtures

```text
uv run pytest -q tests/test_runtime_lab.py tests/test_local_model_comparator.py
uv run pytest --cov=tools --cov-report=term-missing
uv run ruff check tools tests
uv run ty check tools tests
uv run basedpyright
uv run python -m tools.validate_repository
```

## Handoff State

- **Completed:** dependency and boundary reconciliation.
- **In progress:** model-free runtime lab contracts and evidence.
- **Blocked:** positive runtime/model support and heterogeneous device performance claims.
- **Next ready step:** validate contracts and publish the internal unsupported matrix.
- **Rollback:** revert Track 08 commits; optional external artefacts are untouched.
