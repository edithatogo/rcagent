# Context Pack: Track 01 review

- Track: safety-systems-foundation_20260731; GitHub issue #6
- Base revision: `02e7245dcccfad3d9e44fa5c2af340373ae1941a`
- Branch: `codex/review-track01`; separate temporary worktree
- Created: 2026-08-31; fresh until relevant source or branch changes
- Privacy mode: synthetic-only local engineering; GitHub delivery metadata only
- Context budget: selected track, delivery contracts and directly relevant code/tests
- Owned files: autonomy harness/state, workbench, their tests, Track 01 records
  and current archive/dependency links; integration lane owns shared records

## Objective and acceptance

Review all eleven specification criteria, fix concrete safety and continuity
gaps, and archive only after evidence and required validation pass. The three
agent lanes cover acceptance, safety/privacy, and evidence/archive integrity.
Exact model revisions are unavailable; shared context limits independence.

## Authority and dependencies

Use Track 01 specification/plan, product guidelines, workflow, autonomy
contracts, integration map and standing agent-review decision 20260830-001.
Track 00 gates only its declared licence/release/clinical-claim consumption,
not unrelated reversible foundation work. Its pending Claude trials are not
executed or declared complete here. Apache-2.0 remains unchanged.

## Exclusions and risks

No private clinical/employee data, model execution, credential changes,
historical study retry, external system writes, release or professional
validation. Durable local coordination does not confer authority to execute
commands or take over another writer's lock. Preserve hash-bound historical
receipts; document supersession separately.

## Commands and handoff

Use focused pytest, Ruff, ty and basedpyright, followed by
`python -m tools.full_validation`. Reconcile exact GitHub issue/dependency and
check state before claiming delivery. Track 00's separate branch is untouched.
Rollback consists of reverting focused review commits; never discard unrelated
work or rewrite retained evidence. Next step: integrate panel fixes and validate.
