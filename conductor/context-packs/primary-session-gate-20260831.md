# Context Pack: Guarded primary session and execution gate

Track `eval-blocker-remediation_20260803`, issue #1. Prepared after the committed
native prerequisite slice; reconcile its delivery receipt and current Git/CI
before activation. This preparation is not a study freeze or execution permit.
PR #99 merged as `acd251d` with reviewed-tree parity; successor branch
`codex/primary-session-gate` starts there. At preparation, main and the
implementation agent had completed design only. Post-merge conformance
`33326897765` and Quality `33326897749`
passed; local master and completed branch cleanup were verified.

Activated on the 2026-08-30T18:46Z heartbeat from clean checkpoint `0c68b95`.
Parent post-merge workflows were rechecked successful; no overlapping writer
or enabled worktree lease was found. Main owns integration, evidence and
safety; `runtime_profile_tests` owns gate/session code and fixtures, with
`root_acceptance_map` providing read-only acceptance review. No actual model
eligibility operation, study freeze or execution is authorised by this fixture
implementation checkpoint. Existing bounded study authority remains unchanged.

Implementation `1d01242` and final agent acceptance now pass, including full
1,407-test validation at 94.29%; see the
[implementation receipt](../tracks/eval-blocker-remediation_20260803/primary-session-gate-20260831.md).
PR #100 merged as `135881d` with exact reviewed-tree parity; all seven PR checks
and both post-merge workflows passed. Completed branch cleanup was verified.
No actual model or study operation occurred. Next,
implement the [controller/admission slice](./controller-admission-20260831.md)
before actual freeze so the reviewed dependency closure includes that path.

## Selected next implementation

The agent panel recommends implementing the guarded single-slot primary adapter
and its prelaunch verifier together, using synthetic fixtures only. Another
candidate-only wrapper does not close the lifecycle gap. Main owns integration,
safety and evidence; assign bounded implementation and acceptance agents after
checking ownership. No human reviewer or repeat routine approval is required.

Proposed modules: `prospective_primary_session.py` and
`prospective_execution_gate.py`, with matching tests. Reuse existing session,
process, transport, decoder, slot binding and committed-file helpers. Preserve
the fixed READY public behavior and historical source-pin receipts. Do not
duplicate the full lifecycle or expose a new unchecked execution entrypoint.

## Read only the needed context

Start at `conductor/index.md`, selected specification/plan/metadata/cursor,
workflow/guidelines and standing decisions 20260830-001/002. Read the preceding
native prerequisite receipt/context, native protocol and runner contract,
slot binder, shared freeze helper, server session and directly imported
runtime/profile/model/process/transport modules and matching tests. Do not
read historical raw outputs or inspect actual model caches for this slice.

## Design checkpoint before code

Agree the primary entry API, complete execution dependency inventory and review
record trust boundary before extracting lifecycle behavior. Gate requirements:

- Exact native protocol pin and declared slot, preserving validated bytes.
- Fresh internally obtained model eligibility bound to the same condition.
- Actual primary adapter identity, not READY or binder identity.
- Explicit complete project-source and dependency identities at one commit,
  including runtime/profile/model/registry/normalizer and package dependencies.
  Distinguish committed sources from separately pinned runtime artefacts and
  loaded interpreter/library identity; a list of nine known files is not closure.
- Hash-bound agent review linked to the exact source commit and protocol,
  from an established trusted record. A caller JSON receipt, boolean or schema
  match alone proves neither review provenance nor execution permission.
- Review record outside the frozen source commit to avoid circular self-hashes.

### Recorded panel recommendation

The implementation agent proposed a signed review policy and new trust key.
Main and acceptance rejected that unnecessary infrastructure/authority expansion
under the standing decisions. No owner decision is outstanding for this design.
Use the existing trusted, owner-controlled repository delivery workflow:

1. Integration records actual panel findings, reviewer task/message evidence
   locators, reviewed scope, dispositions and unresolved findings.
2. Source commit S contains the real adapter and complete declared dependency
   closure. A later review commit R contains the fixed-path review record,
   referring to S and exact protocol, adapter and closure hashes.
3. Select immutable R through the reviewed delivery workflow. The gate reads
   the record from R with sanitized Git, verifies S ancestry, closure-source
   parity between S/R/working bytes, all referenced hashes and resolved hard
   gates, then obtains fresh internal model eligibility.
4. Do not demand whole-tree S/R parity: the review record necessarily differs.
   Do not accept caller receipt dictionaries, booleans or arbitrary review paths.

The trust root is the established repository workflow and actual recorded panel
evidence, not schema conformance. This verifies integrity of a trusted review
record, not cryptographic reviewer identity, agent independence or protection
against a malicious repository owner. Preserve same-user mutation and loaded-code
limitations. Do not invent actual review evidence for synthetic test fixtures.

Proposed sole public entry is `run_primary(protocol_path, pin, slot_id,
review_commit, root, model_root, receipt)`. Resolve S from the committed review
record at R; bind a private immutable gate plan. Do not expose requests, argv,
environment, callbacks, eligibility receipts or bypasses. Recheck identities
immediately before reservation; two checks narrow races but do not prove atomicity.
Extract only shared private lifecycle internals; preserve READY wrapper constants.

Candidate project closure includes gate/primary session, prerequisite/freeze,
binder, native/prospective protocol, runner/decoder, inventory/preflight,
server/model/profile/runtime helpers, comparator, process/transport and package
initialiser, plus exact registry and protocol references. Verify the actual import
closure rather than copying this candidate list blindly. Separately enumerate
supported interpreter, installed validator dependency files and runtime/model/
licence identities; do not claim OS or in-memory-code attestation from file hashes.
Resolve the supported loaded-identity boundary honestly before activation.

Adversarial fixtures must cover review replay/tampering, dependency drift,
gate-to-reservation changes and every failed prerequisite preventing lifecycle,
then exact request selection, synthetic failure cleanup and legacy READY parity.
No always-failing placeholder is an acceptable completed gate.

The existing prerequisite checker deliberately cannot attest loaded code or
complete dependency closure. Resolve those boundaries explicitly; never promote
its positive result to execution permission. A residual same-user mutation race
must remain a stated limitation, not a silent guarantee of atomic attestation.

The sole primary entry verifies every gate before reserving a session receipt,
creating a session directory, worker, socket or model process. Read-only bounded
Git subprocesses are prerequisite checks. No caller bypass or supplied fake
eligibility receipt. Keep execution permission separate from observation
admission, blinding, scoring-start and study completion.

## Validation and completion

Fixture-first tests must prove each missing/mismatched prerequisite prevents all
lifecycle calls. Exercise a permitted synthetic composition through failures,
cleanup and exact request/response binding, without creating a usable production
permit from fixtures. Preserve legacy READY behavior with compatibility tests.
Require meaningful coverage, native/Windows type checks, full repository
validation and agent acceptance review; fix bounded findings automatically.

Do not call this complete if closure or review trust remains unspecified. Keep
actual execution unavailable until genuine identity and review evidence exist.
No actual model run, eligibility operation, study freeze, observation admission,
blinding or scoring in this implementation slice. Preserve all raw evidence,
H0–H8/H8P, Apache-2.0 and per-artefact rights, private-data and credential gates.
Agent engineering agreement is not clinical, legal, policy, regulatory,
employment, cultural-safety, organisational or deployment approval.

Record exact implementation and remaining evidence; verify delivery tree parity.
Next after this slice: implement governed two-slot orchestration and affirmative
admission, then actual complete protocol/closure review and freeze before study
execution. Admission must precede blinding.
