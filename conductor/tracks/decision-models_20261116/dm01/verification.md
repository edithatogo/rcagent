# DM01 implementation and verification receipt

Date: 17 November 2026, Australia/Brisbane. Status: **DM01 documentation,
source verification, procedural arithmetic and agent review complete**.
Exact-head hosted checks and merge are recorded separately after publication.
[Machine receipt](./verification.json). [PR #147](https://github.com/edithatogo/rcagent/pull/147).

## Delivered scope and identity

DM01 implements the bounded context/receiving map, actual source-admission
dispositions and the frozen first-study procedure. It adds no runtime adapter,
production API, dependency, model qualification or new operational threshold.
Model runs, new study cases, holdout access and real cases processed are zero.
The initial planning receipt remains historical.

The inspected input is master `8a564826a3f51765f177f0d9823194718bacb7d9`, tree
`47543fabfbfa8e6682f5b088b56e6982ae5af82d`. The [context snapshot](./context-snapshot.json)
records 23 actual input blob IDs and SHA-256 digests. The final source commit
and hosted results are recorded in the PR after publication; this document
does not predict its own commit hash or report a future check as passed.

Before publication, master advanced through HEAPS H4 to
`006d98cb60c72143b0517f0e7a446641642ddd5a`, tree
`5c55fde1cbe324973b71413f63367c773391d523`. It was integrated and the full gate
was repeated against that code. All 23 receiving-context files remain
byte-identical; both local observations are retained.

The final publication refresh also includes H4 acceptance PR #152 at master
`5d00ce255cdb5dcabc7d4c749d568c1b9861c47e`, tree
`e6706fc1b2406810c726cbe3cdbd24320d837758`. That intervening change contains
only H4 acceptance documentation. Implementation, tests, lock and workflows
are unchanged from the integrated full-suite input, and all 23 context input
digests were checked again. This freshness observation does not rewrite the
original review or failed-run identities.

## Local engineering observation

`uv sync --locked --extra validate --extra test --extra lint --extra assurance`
passed using the existing lock. Local uv was 0.13.6 and the quality interpreter
was Python 3.15.2. A cache hardlink warning caused a full-copy installation;
the dependency lock was unchanged. No model dependency or weight was installed.

`uv run --no-sync python -m tools.full_validation` exited **1**. Ruff correctness
and formatting, ty, strict basedpyright (zero diagnostics), the zero-debt typing
ratchet, Bandit, Vulture, marker policy, governance and all seven deterministic
benchmark regressions passed. Existing Bandit nosec warnings remain recorded;
no suppressions were changed.

The initial run reported **2,720 passed, 52 failed and 11 skipped**, with
**93.38% branch coverage**. After H4 integration, the repeated run reported
**3,125 passed, 52 failed and 11 skipped**, with **93.54% branch coverage**.
Both sets of 52 failure lines were compared programmatically with the
retained D2 local receipt and matched exactly. A separate direct probe of
`socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)` returned
`PermissionError: [Errno 1] Operation not permitted`. This establishes the
observed local restriction; the full local gate is still a failure. Tests and
gates remain unchanged and enabled on the supported hosted runners.

The machine receipt retains the failed test names, comparison reference, lock
digest and both actual full-log SHA-256 identities. DM01 changes no runtime,
test, dependency or workflow files from the integrated master. Final document
consistency is a separate check after the DM01 records are complete.

## Final document and scientific-design verification

JSON parsing, all local Markdown/JSON references, context/source digests,
protocol count/precision arithmetic, cross-file state, task dependency order,
owned-file diff, the repository validator and `git diff --check` passed. The
machine receipt records the exact counts. Independent review reproduced all
22 retrieved upstream text-file SHA-256/Git-blob/size identities and all 23
repository input identities at both master revisions. Large-asset publisher
metadata remains distinct from local byte verification.

The protocol has seven unique Noul questions, 2,360 independent planned
families and 1,200 holdout families including 300 severe positives. Eight
precision calculations reproduce, including the zero-miss 95% upper bound
of approximately 0.009936 and the one-miss bound of approximately 0.015715.
Thus the proposed 1% safety criterion requires zero unsafe misses at the
specified positive sample size. Secondary variants add no independent n.
These are arithmetic/design checks, not an observed safety rate or a power
guarantee. Zero coverage fails the prespecified floor; missing forecasts cannot
pass the confirmatory probability-metric gate.

The existing local sensitive-text scanner found no findings in the 16 track
files and still detected its synthetic phone positive control. This bounded
scanner result does not replace the actual hosted privacy/secrets workflow.
Protocol and source identities are preserved in the machine receipt. There
are four completed DM01 task/checkpoint markers and 39 pending markers;
all 11 work-package dependencies are acyclic, with DM02–DM11 still pending.

## Review panel

| Role | Observed conclusion and evidence | Independence limits |
|---|---|---|
| Acceptance/architecture | Passed bounded context, ownership, receiving contracts, source identities and procedure; independently verified 22 upstream files, 23 repository inputs and numerical totals | Read-only reviewer, no DM01 file authorship; no runtime/clinical assessment |
| Evidence integrity | Passed after closing comparator-selection timing and provisional-decision mapping findings; independently checked protocol arithmetic and both context revisions | Authored the source pair; independent of protocol/context authorship, not independent verification of its own sources |
| Safety/privacy | Passed admission/authority limits, synthetic references, missingness, escalation, no-abstain loophole and no unsupported clinical claim | Authored the protocol and made assigned clarifications; no blinded or human validation |
| Integrator verification | Reproduced structure, links, input identities, eight precision calculations, task state, privacy positive control and owned-file boundary | Consolidates the evidence; does not convert correlated agent reviews into clinical or empirical proof |

The draft review closed three concrete procedural ambiguities before the
first published freeze: H uses each component's tuned severe threshold for
agreement; training-only configuration ranking uses raw probabilities and
explicit 0.5 cutoffs; one deterministic postprocessor owns all dispositions.
The source pair now expressly permits bounded training-only selection while
forbidding calibration/threshold/holdout-based substitution. A date mismatch
was also corrected. No case, reference label, model outcome or holdout was
created/accessed during these changes.

The machine receipt binds the final seven context/source/protocol artefacts.
The acceptance reviewer inspected the preceding draft; the later small
procedure/timing deltas were checked by the evidence reviewer, safety reviewer
and integrator. All roles are agents with potential correlated errors. This
is engineering/research-design review, not clinical or human reference validation.

## Publication and merge conditions

The current user explicitly authorised DM01, PR checks and merge. PR #147
already holds the planning increment and is extended with this package.
Before merge, read the actual final head, current master, changed paths,
active rules and latest checks. Required contexts are `dependency-review`,
`validate (ubuntu-latest)`, `validate (macos-latest)` and
`validate (windows-latest)`. The Ubuntu aggregate requires the full validation
matrix, mutation, profiling and combined coverage. Also inspect privacy/secrets
and all runnable Quality jobs. Use an expected-head merge after their success;
do not change protection or bypass checks.

The inherited Offline AI security workflow is distinct from these required
contexts. Its actual queued/running/completed state is retained separately.
A queued run is not a completed scan. Hosted evidence for the old planning
head does not qualify the new DM01 head. Exact-head and post-merge observations
belong in the PR acceptance record after they occur.

## Handoff and rollback

DM02 remains pending. No shared production path/schema agreement or supported
runtime is claimed. Later execution requires its named scope, actual asset
and licence admission, independently authored references and sealed manifests.
The seven-Noul study does not qualify other primitives or data populations.
Reverting the bounded documentation changes withdraws this package while
preserving other owners' code, original planning history and negative evidence.
