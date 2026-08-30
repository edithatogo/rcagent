# Fixed synthetic output-mode probe

Track `eval-blocker-remediation_20260803`, issue #1; base `f6178dc`.
Branch `codex/synthetic-output-probe`. This is a new output-grammar diagnostic,
not a repeat of the earlier version/help or legacy runtime observations.

## Implementation and rights boundary

`tools/prospective_model.py` keeps the original comparator registry bytes and
its runtime identity intact. An in-memory copy explicitly substitutes the
separately verified 0.3 runtime identity; the existing validator still checks
all three model classes, their licences, file sizes and hashes. The result
records original/effective identities, a digest of each representation and
explicit non-study locks. Selected model and licence bytes are rechecked after
the full validation. This is local artefact eligibility, not study admission.

`tools/local_output_probe.py` has one fixed synthetic READY prompt and one
fixed invocation of the admitted small Qwen model. Documented suppression and
offline flags are taken from the retained 0.3 help receipt, not assumed to
produce response-only output. The CLI exclusively reserves its receipt before
any launch. It retains exact local arguments, complete bounded raw streams,
source/profile/model identities and actual loader evidence; pre/post checks
must agree. Output grammar is not classified as correct by process success.

The existing comparator decision 20260829-002 authorises the bounded local
synthetic scope. No model/runtime installation, global links, new resources,
credentials, private data, paid service or redistribution is introduced.
Clinical, legal, policy, regulatory, employment, cultural-safety, organisational
and deployment authority remains external. Old registry/profile/receipt bytes
and H0–H8/H8P are preserved.

## Panel and fixture evidence

Main agent: acceptance, integration and model helper. Agent
`protocol_contract_review`: probe implementation and fixture-first coverage.
Agent `root_acceptance_map`: read-only evidence-integrity and safety/privacy
review. The panel recommended explicit original-runtime identity and non-study
locks plus a final selected-file recheck; all were implemented. Main requested
exact local argv in addition to the redacted representation; implemented.
No unresolved source-review hard-gate finding remains. Model revisions were
not exposed; this is agent review with correlated-error limits, not independent
human validation or a model-quality assessment.

The helper has 16 synthetic tests; the probe has 20. Both reach 100% statement
and branch coverage. Tests cover other-model/selected-licence drift, original
registry preservation, post-validation changes, source/profile drift, unsafe
destinations, timeout/nonzero/empty/oversized output and loader rejection.
The real read-only cache admission check passed without launching a model.
`uv run python -m tools.full_validation` passed: 776 tests, 93.33% coverage,
scoped lint/types, governance, gremlin scan and seven-case regression. The
implementation was committed as `a82acb1` before live execution.

## Live observation and negative grammar finding

One probe ran from 08:16:22 to 08:16:27 UTC on 2026-08-30, exiting zero in
5.70 seconds. All 16 reported non-system loader images matched the profile;
model, registry, profile and source pins agreed before/after. Complete stdout
was 1,028 bytes and stderr 100,500 bytes. The generated response was READY,
but stdout also contained a startup banner, model metadata, available commands,
the echoed prompt and an exit message. Therefore **response-only stdout was
not established**. Suppression flags did not remove that wrapper.

The complete local-only receipt is
`/Volumes/PortableSSD/rcagent-model-cache/probe-evidence/output-mode-v030-20260830.json`.
Its SHA-256 is `4fdbb667764b48852a3e5e41b7b0685646220bfb136f29bc9f17c3fba085dcd6`.
The raw stdout SHA-256 is
`1d604f100030ccf3d92fa38739e3fe60f8014e75bb393fe5ad1bf7aae67d95a7`;
stderr is `d246be438be1c6bc719814c80ad8266332e210255fed0ddeb470d39c25d40294`.
The admission-envelope digest is
`641c2ab2476e953d0c9eb33faa08ccd04701b1884ee660d38e2045e42b09197d`;
both original and effective runtime identities are retained there. The source
pins bind the committed probe/helper and existing profile/comparator sources.
This public summary deliberately omits raw streams and is not complete raw
evidence. It makes no model-quality, clinical or comparative claim.

Retain the wrapped-output finding rather than generic banner stripping or
searching for READY/JSON. Next normalisation must use a strictly validated
wrapper grammar with pinned implementation evidence, or a separately admitted
response-only entrypoint. One observed output is not proof of general grammar.

## Remaining implementation and rollback

No prospective primary slot is captured or admitted by this slice. Next:
derive deterministic normalisation from actual output evidence, implement the
study runner and full component closure, freeze the protocol, then implement
affirmative stage transitions. A failed probe is retained as a negative result;
unfinished engineering cannot justify readiness-only fallback.

Revert only this helper/probe extension after checking consumers; retain all
raw receipts and historical evidence. Loader diagnostics are not tamper-proof,
OS/driver bytes and network egress are not independently attested, pre/post
hashes do not prevent concurrent replacement, and temporary files are not a
disk quota.
