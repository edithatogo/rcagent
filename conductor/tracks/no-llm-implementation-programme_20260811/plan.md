# No-LLM Implementation Programme — Plan

## Phase 1: Programme controls and baseline

- [x] Task: Verify `master`, open PRs, remote branches, open issues, and required checks — see `evidence/programme-baseline.md`
- [x] Task: Record the one-branch and one-checkout operating baseline — see `evidence/programme-baseline.md`
- [x] Task: Define the receipt template for commits, checks, merge, cleanup, and blockers — see `evidence/receipt-template.md`
- [x] Task: Confirm no-model-download test doubles and fixture boundaries — see `evidence/no-model-boundary.md`
- [x] Task: Reconcile legacy evaluation records
  - [x] Verify eval-pilot-calibration_20260225 metadata against its recorded H0/H1 evidence and registry status; current evidence is insufficient and the track is blocked fail-closed
  - [x] Archive completed `eval-protocol`; retain incomplete `eval-case-collection` and superseded-but-incomplete `eval-data-collection` in active records without claiming completion
  - [x] Normalize remaining metadata timestamps to UTC ISO-8601
- [x] Task: Record execution-policy precedence — see `evidence/execution-policy-precedence.md`
  - [x] State explicitly that this programme's one-branch baseline preempts autonomy.json lane limits while the programme is active
  - [x] Record single-active-phase-checkpoint WIP discipline for all track plans
- [x] Task: Establish vendored-plugin governance
  - [x] Record the dependency-graph gap: Dependabot and GitHub code scanning cannot see submodule contents, so CVE review and bump cadence are manual owner-checked duties per the `vendored_plugins` update policy in `integration-map.json`
  - [x] Verify each vendored plugin pin against its upstream main and record the receipt (conductor `f06add3`, sourceright `c5fa583`, authentext `ca39b86`) — see `evidence/vendored-plugin-pins.md`
  - [x] Document the consumer fetch step (`git submodule update --init`) on the contributor-facing surface — see `docs/vendored-plugins.md`
  - [x] Evaluate upstream findings (sourceright committed backup artefacts; conductor release-tag pinning) and raise authorised upstream issues or contributions — filed sourceright#100 and gemini-cli-extensions/conductor#180
- [x] Task: Phase verification and checkpoint

## Phase 2: Track 00 reconciliation

- [x] Task: Audit pending Track 00 checklist items against merged evidence — see `../agent-skills-living-conformance_20260731/evidence/checklist-reconciliation-20260827.md`
- [x] Task: Mark only evidenced tasks complete and retain genuine decision gates
- [x] Task: Verify current Agent Skills conformance, adapters, fixtures, and privacy sentinels
- [x] Task: Record the licence gate and release contingency without selecting a licence
- [x] Task: Review, merge, and clean the Track 00 reconciliation PR — PR #31 merged as `3ef006d6e4356f33b24161c5763c1efa8e0c3215`; required checks passed and the branch was deleted
- [x] Task: Phase verification and checkpoint

## Phase 3: Foundation and assurance

- [x] Task: Implement Track 01 safety-systems foundation slice
- [x] Task: Implement Track 02 evidence-workflow slice — `4a976e0`, review `1431674`, receipt `acca833`
- [x] Task: Implement Track 03 privacy/security assurance slice — `3f7aad3`, review `a5ff002`
- [x] Task: Implement Track 04 jurisdiction-pack readiness slice — archived completion `1e32fa4`; bounded active-policy decision retained
- [ ] Task: Apply issues #17 and #18 controls to each slice
- [x] Task: Review, merge, and clean each Phase 3 PR before starting the next — Tracks 01–04 merged and reconciled
- [ ] Task: Phase verification and checkpoint

## Phase 4: Evaluation, multimodal, retrieval, and runtime readiness

- [x] Task: Implement Track 05 deterministic benchmark and admission infrastructure — PR #49 merged as `6578da1`; archived with all comparators unsupported
- [x] Task: Implement Track 06 multimodal contracts, fixtures, mocks, and safety gates — PR #51 merged as `42d64ea`; archive PR #52 merged as `569344b`
- [x] Task: Implement Track 07 deterministic retrieval and citation interfaces — PR #54 merged as `c8d0ea3`; coverage follow-up PR #55 merged as `a7f2787`
- [x] Task: Implement Track 08 runtime discovery, resource limits, and dry-run checks — PR #57 merged as `3689a02`; archived with no supported runtime/model tuple
- [x] Task: Preserve hosted API, human, and local-model execution as explicit gates — Track 08 schema 1.0 cannot promote or execute a model
- [x] Task: Review, merge, and clean each PR before starting the next
  - [x] Tracks 07 and 08 reviewed, merged, remediated and archived with exact hosted evidence
- [x] Task: Phase verification and checkpoint

## Phase 5: Interfaces, distribution, and adaptation readiness

- [x] Task: Implement Track 09 interfaces, templates, and action-loop controls
- [ ] Task: Implement Track 11 packaging, adapters, installation, and release preflights
- [ ] Task: Implement Track 10 dataset governance and dry-run adaptation pipeline only
- [ ] Task: Preserve training and model-artefact production as blocked external work
- [ ] Task: Review, merge, and clean each PR before starting the next
- [ ] Task: Phase verification and checkpoint

## Phase 6: Portfolio reconciliation and closure readiness

- [ ] Task: Re-run repository, security, privacy, provenance, and dependency checks
- [ ] Task: Reconcile child tracks with issues #1-#4 and architecture issue #19
- [ ] Task: Close only issues whose acceptance evidence passes
- [ ] Task: Produce a residual-blocker and restart manifest
- [ ] Task: Verify only `master` and intentionally retained branches remain
- [ ] Task: Verify disposable checkouts and stale lock backups are removed
- [ ] Task: Phase verification and checkpoint

## Planned PR sequence

1. Programme controls and receipt template.
2. Track 00 checklist reconciliation.
3. Track 01 foundation harness.
4. Track 02 evidence workflow.
5. Track 03 privacy and assurance.
6. Track 04 jurisdiction readiness.
7. Track 05 deterministic evaluation infrastructure.
8. Track 06 no-model multimodal contracts.
9. Track 07 deterministic retrieval interfaces.
10. Track 08 runtime discovery and dry-run controls.
11. Track 09 interfaces and action loop.
12. Track 10 adaptation readiness and negative-result closure.
12. Track 11 distribution and release preflights.
13. Track 10 adaptation governance and dry-run pipeline.
14. Cross-cutting quality and portfolio reconciliation.
