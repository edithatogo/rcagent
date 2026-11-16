# Repository-recommendation incorporation receipt

Date: 16 November 2026 (Australia/Brisbane).

## Scope and identity

The owner requested incorporation of the repository review recommendations into
Conductor and an ordered implementation report. This change supplies the
[recommendation map](./recommendations-20261116.md),
[machine-readable order](./execution-order-20261116.json), pending acceptance
criteria in the existing plans, and navigation from the existing tracks and
portfolio. It changes Conductor documentation only.

- Reviewed/base commit: `c6892497aa0b03555d5145242c04965471eccc1d`.
- Isolated branch: `docs/frontier-reuse-execution-plan-20261116`.
- Canonical counts remain 24 FAW and 25 CAW work packages; D0–D8 unchanged.
- Current work remains FAW07 / D0, not accepted. Existing implementation #132,
  verification #133, AcciMap #139 and HEAPS #140 retain their scopes.
- Coordinator `6af6164f-cf84-8321-9f96-8b7d685aabe5` remains the shared integrator
  and merge owner. Track numbers for the parallel method/profile handoffs are
  not allocated here.
- No production code, tests, dependency/profile registry, schema, lock, CI,
  source dataset or historical study result is changed.

## Confirmed renderer gap

The reviewed implementation of `tools/interface_actions.py::render_view`
checks schema shape and source hashing independently of
`tools/evidence_core.py::validate_record`. The latter also enforces domain
references, uniqueness and workflow history. The following synthetic-only
probe was rerun during incorporation on the unchanged source baseline.

```python
from copy import deepcopy
import json
from pathlib import Path

from tools.evidence_core import validate_record
from tools.interface_actions import canonical_hash, render_view

base = json.loads(Path("tests/fixtures/safety-work/valid-case.json").read_text())
context = {
    "citations": [],
    "model_involvement": {"used": False},
    "limitations": ["synthetic review probe"],
    "approval_receipt_ids": [],
    "outstanding_review_ids": [],
}
variants = {name: deepcopy(base) for name in (
    "valid_control", "unknown_source", "duplicate_source", "invalid_transition"
)}
variants["unknown_source"]["evidence"][0]["source_id"] = "missing-synthetic-source"
variants["duplicate_source"]["sources"].append(deepcopy(base["sources"][0]))
variants["invalid_transition"]["events"][0]["from_state"] = "closed"
for name, payload in variants.items():
    errors = validate_record(payload)
    record = {**payload, "source_sha256": canonical_hash(payload)}
    try:
        render_view(record, audience="auditor", data_class="generated_synthetic",
                    view_context=context)
        rendered = True
    except ValueError:
        rendered = False
    print(name, not errors, rendered, errors)
```

Run from the repository root with the locked validation environment using
`uv run --no-sync python`. This diagnostic does not fix the defect or replace
the future regression tests.

| Fixture | Canonical validator | Renderer | Observed canonical error |
|---|---|---|---|
| Unchanged valid control | Accept | Accept | None |
| Unknown evidence source | Reject | Accept | Unknown `source_id` |
| Duplicated source object/ID | Reject | Accept | Duplicate identifier |
| First event changed from `closed` to `investigation` | Reject | Accept | Invalid transition |

The renderer currently admits only generated-synthetic records. This is a
confirmed validation-boundary inconsistency, not evidence of an operational
data leak. R01 schedules a canonical-validator repair with compatibility,
format/reference, property and composition regressions; it remains pending.

## Independent agent review

Three existing review agents cover programme/ownership, code/dependency reuse,
and research/evaluation. They are agent reviewers, not human clinical reviewers;
shared model/context can correlate their errors. No clinical validation is
inferred from their agreement.

Initial review identified an unintended universal D7 acceptance prerequisite for
optional process/Rust work in the planning JSON. This was removed: canonical
per-arm prerequisites now govern independent implementation and acceptance,
while larger empirical extensions remain a later investment priority. Review
also sharpened canonical format/relationship regression coverage and clarified
that outcome invariance applies to prospective decision justifiability, while
relevant harm/consequence and retrospective causal fields may change.

Final review disposition: **all three agents accept the documentation
refinement for coordinator integration; no blocking finding remains**.

| Reviewer | Scope and observed checks | Disposition |
|---|---|---|
| `plan_gap_review` | Full substantive diff; canonical mappings and dependency order; ownership and claims; 192 local links; JSON uniqueness/acyclic references; whitespace; independently reran all four renderer probes | Accept planning scope after removal of the universal D7 gate |
| `dependency_audit` | Full substantive diff; validator/hash contracts, optional dependency admission, package mapping, JSON and whitespace; independently reran all four renderer probes | Accept planning scope with canonical format/relationship coverage clarified |
| `frontier_research` | Full substantive diff against canonical work packages and controlled-experiment design; comparator/rubric/holdout/coverage/workflow and causal-claim boundaries | Accept planning scope with field-specific outcome invariance clarified |

The two principal substantive files reviewed have SHA-256 identifiers:

- `recommendations-20261116.md`:
  `65dac0bbdc52ce4c67eec28b83a474e9968b4f12f100f7d0e5cecca004799e6c`.
- `execution-order-20261116.json`:
  `544a6dcb80e695933a8781b69bf035804bae1a5076726660848e3ba7f13df326`.

Subsequent receipt bookkeeping records observed checks and publication without
changing those substantive plans. Reviewer agreement is bounded by the scope
and shared-model limitations above.

## Verification and delivery

The four synthetic probes above reproduced the reported mismatch. The scoped
documentation gate passed: 15 Conductor paths; 10 unique planning steps with
valid, acyclic dependencies; all R01–R12 mapped; all package references present
in the canonical 24 FAW / 25 CAW / 23 DR sets; 192 local Markdown links present;
JSON/JSONL parsed; prior metadata values and ledger prefix preserved; and
`git diff --check` passed. The repository's required complete local gate is
`uv run --no-sync python -m tools.full_validation`.

The complete local gate **did not pass** in this executor. Ruff checks and
formatting, ty, strict basedpyright, the empty-baseline ratchet, security/dead-code
checks, invisible-character scanning, repository governance and benchmark validation
passed; deterministic regression was 7/7. Pytest reported **2,183 passed,
52 failed and 11 skipped in 71.42 seconds**, with **93.27% coverage** using
branch measurement.
The failures are in the existing Unix-socket/session test groups. Socket
construction raised `PermissionError: [Errno 1] Operation not permitted`; an
independent direct `socket.socket(AF_UNIX, SOCK_STREAM)` probe confirmed that
this executor denies creation. No production/test files were changed or tests
disabled to bypass the restriction. Coverage above the floor does not turn
this failed gate into a pass.

Hosted checks are required on the exact published head. The pull request
records that head and its observed check state; earlier baseline CI is not
transferred to it. This receipt does not change historical queued security
scans to passed. Mutation execution and profiling are separate hosted gates,
not established by the local invisible-character scan or deterministic suite.

A fresh pre-publication reconciliation found unchanged master and D0 heads,
and the separate draft handoffs [AcciMap PR #141](https://github.com/edithatogo/rcagent/pull/141)
at `dc42b2e5660c5070db0b1b48b5a83fd17f54425e` and
[HEAPS PR #142](https://github.com/edithatogo/rcagent/pull/142)
at `1b2a19efa1cbe5260381ca25d1dc624500f6cd5b`. Their published file lists do not
overlap this 15-file Conductor refinement. Their own receipts and coordinator
acceptance remain authoritative; neither draft is accepted by this review.

## Limitations and rollback

Planning incorporation is the only intended completion claim. All pending
fixes, D0 acceptance, model studies, clinical/workflow qualification, local
template conformity, operational deployment and releases retain their own
evidence requirements. The current supported model set is not expanded.

Primary sources are linked in the recommendation map for dependency and study
selection. They are candidate inputs whose exact version, task applicability
and reuse rights must be checked at implementation/study freeze; this change
does not copy third-party instruments or install new dependencies.

Revert this documentation change through a normal commit if the plan changes.
Keep the accepted engineering and historical negative-study records intact.
