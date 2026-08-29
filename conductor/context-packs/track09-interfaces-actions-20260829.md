# Context Pack: Track 09 Interfaces and Closed-Loop Actions

- **Track:** `interfaces-templates-action-loop_20260731`
- **GitHub issue:** [#14](https://github.com/edithatogo/rcagent/issues/14)
- **Base revision:** `0b267919b5bf33a95a221e9569a261f59ac49f98`
- **Created:** `2026-08-29T09:12:41Z`
- **Fresh until:** dependency, schema, jurisdiction or external-action policy change
- **Privacy mode:** fully local, generated synthetic fixtures only
- **Context budget:** Track 09, direct archived dependency receipts, canonical schemas and bounded interface code
- **Owned files:** `tools/interface_actions.py`, `tests/test_interface_actions.py`, `evaluation/interfaces/`, Track 09 records and directly mapped schemas

## Objective and Acceptance

Create original, client-neutral workflow/template contracts, fail-closed dry-run
interface adapters, participation/support prompts, closed-loop action assurance,
auditable audience views and deterministic synthetic usability evaluation.

## Dependencies and Receipts

- Tracks 02, 03, 04, 06 and 07 are archived with passing completion receipts.
- ims+ or another approved platform remains the incident system of record.

## Decisions, Risks, and Assumptions

- No external send, lodge, approval, disclosure, branded form or system mutation is implemented.
- No clinical, legal, policy, employment, cultural-safety, organisational or deployment approval is inferred.
- Enterprise, FHIR and workflow-engine integrations remain bounded adapter contracts until separately available and authorised.

## Excluded Context

- Private clinical/employee data, credentials, internal endpoints, branded or mandated forms, and external communications.

## Commands and Fixtures

```text
uv run pytest -q tests/test_interface_actions.py
uv run pytest -q --cov=tools --cov-report=term
uv run ruff check tools tests
uv run ty check tools tests
uv run basedpyright
uv run python -m tools.validate_repository
```

## Handoff State

- **Completed:** dependency readiness and boundary declaration.
- **In progress:** deterministic interface and workflow contracts.
- **Blocked:** production integration, identifiable exports and accountable approvals.
- **Next ready step:** implement synthetic contract fixtures and validators.
- **Rollback:** revert Track 09 commits; no external system is mutated.
