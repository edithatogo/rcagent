# FAW06 typing repair receipt

Date: 13 November 2026, Australia/Brisbane. The user's current priority is typing
repair. This increment is part of [PR #127](https://github.com/edithatogo/rcagent/pull/127),
with current-head hosted acceptance required before merge. FAW06 remains in progress.

## Measured result

Both measurements use locked basedpyright 1.40.2 with an empty external baseline
and `--baselinemode=discard`. The starting published source is `98ce938`; master
`718b418` is incorporated without altering its separate security workflow. The
[machine-readable receipt](../../../quality/typing-verification-20261113.json)
records exact revisions, source hashes, commands, per-file counts and evidence hashes.

| Scope | Before | After | Removed |
| --- | ---: | ---: | ---: |
| Production | 1,980 | 1,196 | 784 |
| Tests | 7,733 | 4,816 | 2,917 |
| **Total** | **9,713** | **6,012** | **3,701 (38.1%)** |
| Files with retained debt | 117 | 98 | 19 |

No file/rule count increased. Every remaining policy cap now equals the observed
count; zero-count allowances were removed. The original 9,801-diagnostic
measurement and its checker/revision provenance remain historical evidence.
Six new Python files have zero unbaselined diagnostics and no debt allowance.

## Implemented contracts

- Evidence, jurisdiction and release-admission validators now narrow incoming
  containers before access and use explicit schema-validator/result contracts.
- Runtime, adaptation and interface validators retain `object` for unvalidated
  values, bind checked fields before use and reject malformed method-request
  arguments before counting a synthetic abstention as successful.
- Skill drift, conformance, profile, skill and repository validation use explicit
  response/context-manager protocols, nested typed receipts and checked JSON/YAML.
- Five prospective session/controller/admission/identity test modules now have
  typed fixtures, callback signatures, binary-I/O doubles and synthetic environment
  dataclasses. Checked helpers preserve mutable object identity and callable
  parameters; they make no claim of domain validity.
- New negative cases cover malformed arrays, method arguments, non-promotion
  limitations and export values. Existing assertions and adversarial parameter
  matrices remain; 255 original assertions across the two test batches were checked.

Eleven existing production modules and eight existing test modules are now clean
without a baseline. Some explicit legacy `Any` load/export interfaces remain;
this increment does not claim their elimination. Narrow, documented casts adapt
checked containers and an incomplete jsonschema overload. One deliberate
`cast("str", True)` preserves the original invalid-input rejection test. No new
`Any` allowance, ignore directive, disabled diagnostic or skipped test was added.

## Reviewed baseline maintenance

The five prospective test files decreased from 2,608 to 213 diagnostics. Their
refactored expressions surfaced 56 retained diagnostics against the old positional
baseline: 26 had exact prior messages; 30 were relocated or consolidated at checked
boundaries. Read-only review traced the latter to four `mapping_call` registrations,
23 `mapping(...)` checks, one typed monkeypatch receiving an unchanged untyped
callable, and two renamed intermediate variables. No new incompatible type,
missing member or invalid operation was found.

Only those five files' remaining entries were re-anchored to observed ranges,
after proving that no file/rule count grew. Ordinary basedpyright then removed
another 1,306 entries elsewhere and passed with the 6,012-entry retained baseline.
`--writebaseline` was not used. This is explicit maintenance of reviewed remaining
debt, not evidence that the retained APIs are fully typed. Both the previous PR
head comparison and the exact first-rollout master comparison pass.

## Verification

| Check | Observed result |
| --- | --- |
| Ruff, format, ty, retained-baseline basedpyright, baseline/cap ratchet | Passed |
| Hash-bound Bandit, Vulture, Unicode scan | Passed; frozen study source bytes unchanged |
| Repository governance and deterministic benchmark | Passed; 7/7 benchmark cases |
| Live official skill validator, complete project profile, monitored upstream drift | Passed; current conformance true |
| Root boundary/coverage tests | 154 passed |
| Core / conformance and repository focused runs | 112 / 188 passed |
| Two adversarial test files, unchanged and edited | 141 passed in each; same parameter matrix |
| Full integrated pytest with branch coverage | 1,958 passed, 52 failed, 11 skipped; 93.40% coverage |
| Exact 52 failing cases on unchanged source | Same 52 failed; zero status or normalized-message mismatches |
| Release-admission mutation | 24/24 killed; no survivors, timeouts, errors or pardons |
| Actual required-aggregate shell | All-success passed; all 12 failure/cancel/skip variants failed |
| Independent valid method-request combinations | 542 matched the existing guidance result |
| Independent malformed single-field differential checks | 2,425 examined; no changed behaviour or new crashes; 86 pre-existing crashes retained |

The environment denies AF_UNIX socket creation. Twenty-six failing cases directly
raise `PermissionError`; the other 26 reproduce the same downstream effects on
unchanged source. No test was disabled. This establishes failure parity, not
successful execution of these paths; hosted runners must supply that evidence.

The coverage-filtered mutation invocation left 20 of 24 mutants alive after the
guard changes. Running the complete 15-test release suite for every mutant killed
all 24. CI now requires `--gremlin-no-coverage-filter` for this small target while
retaining the 100% real-kill gate.

## Windows coverage correction

At previous published head `98ce938`, [Quality 43305123214](https://github.com/edithatogo/rcagent/actions/runs/43305123214)
passed Linux 3.11/3.15.2, macOS, mutation and profiling. Windows passed all 1,698
applicable tests with 256 skips but measured 85.66% against the global 90% floor;
the required aggregate correctly failed. Dependency review, privacy/secrets and
skill conformance passed on that head. Those results are not acceptance of this
new typing increment.

Windows retains functional testing and branch collection, and defers its percentage
floor to a new required combined gate. Linux/macOS retain their individual 90%
floor. The combined gate requires exactly four separate nonempty branch databases,
rejects missing/corrupt/out-of-scope data, normalizes relative source paths and
enforces 90% on the union of measured branches. No source or test is omitted to
increase the score. Real coverage CLI tests verify both failing and passing unions.

## Next bounded typing work

1. Replace bare result dictionaries in process/HTTP capture and prospective
   session/controller APIs with validated result contracts. These contracts feed
   the 213 remaining diagnostics in the five edited test files; 83 are intentional
   private-use reports and 130 concern unknown contracts or retained boundary parameters.
2. Work through the largest remaining callers: local execution probe, Darwin runtime
   tests, process capture/stop tests and prospective execution gate tests. Frozen
   historical production bytes require a new versioned implementation, not rewriting
   consumed source or retrospective study evidence.
3. Establish string types before hashed enum membership. Read-only differential
   review reproduced these existing list/dict crashes: interface template rights
   and field canonical paths; interface status; runtime dependency/support/network/
   telemetry; adaptation framework status; dataset split name. Add bounded rejection
   tests and return the existing validation errors. Container guards alone do not
   make all domain values safe.
4. Retain the no-growth ratchet and continue deleting debt. Keep FAW07–10 component
   demonstrations queued behind the user's current typing priority.

No new clinical/model capability, Rust migration or death-review implementation
is claimed. Existing research plans, frozen studies and negative findings remain.

## Hosted follow-up after first typing publication

The typing source was published at `ac8ded4469dc0c0e0161b077489b2fd9f9103dcb`
with tree `8294eb64309d41b86d503a22fd415bfaccadca1b`, identical to local `c9656f6`.
Privacy/secrets, dependency review, mutation and Scalene succeeded on that head
while the platform validation jobs were still running.

The advisory Vale reporter failed on GitHub's 20,000-line PR-diff API limit, before
it could report the lint results. The action is updated to the verified immutable
Vale v3.0.0 commit `518a9136acc6e6668ce7c00d367051e0941e87ff`, whose
[release notes](https://github.com/vale-cli/vale-action/releases/tag/v3.0.0)
and maintained implementation address that exact failure. Prose scope and severity
policy are unchanged; the workflow follow-up requires its own hosted observation.

The independently merged offline-security workflow remains queued. Its pinned
central workflow requests `[self-hosted, linux, x64, ai-security-offline]` and a
preloaded isolated security image. Its runner infrastructure was not changed by
the typing increment. No queued execution is presented as a successful security scan.
