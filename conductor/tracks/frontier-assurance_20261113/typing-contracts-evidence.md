# FAW06 process and session typing receipt

Date: 13 November 2026, Australia/Brisbane. This is the next bounded typing
increment in [PR #128](https://github.com/edithatogo/rcagent/pull/128), following
merged PR #127. FAW06 remains in progress; this receipt does not declare the
repository fully typed. The machine-readable [measurement](../../../quality/typing-contracts-verification-20261113.json)
records source identities, commands, per-file changes, review and evidence hashes.

## Measured reduction

Both measurements use locked basedpyright 1.40.2, an empty external baseline and
`--baselinemode=discard`. The before revision is master `a38dd9c`; the published
source/baseline revision is `b83b461d6c12c5e6ae6aa535b87c2fb0715593d6`, whose tree
exactly matches the measured local integration. Documentation follows separately.

| Scope | Before | After | Removed |
| --- | ---: | ---: | ---: |
| Production | 1,196 | 1,008 | 188 |
| Tests | 4,816 | 4,015 | 801 |
| **Total** | **6,012** | **5,023** | **989 (16.5%)** |
| Files with retained diagnostics | 98 | 96 | 2 |

No file/rule count increased. Every cap equals the current observed count;
zero-count allowances were deleted. No new Python module or debt allowance was
introduced. Explicit `Any` name references across this increment's edited Python
files decreased from five to zero. This does not describe unedited modules.

## Contracts and concrete defects

`server_process` and `unix_http_capture` now have complete typed result receipts.
Process control, stream observations, cleanup outcomes, buffers, fixture callbacks
and lifecycle doubles have explicit contracts. Both production modules have zero
baseline-free diagnostics. Their three test modules fell from 706 diagnostics to
nine retained private-helper access reports, preserving existing tests and assertions.

The session and primary adapter now distinguish required initial receipt fields
from fields available after later stages. The controller has explicit dispositions,
failure stages and durable outcomes. Primary plan/context and journal stream
protocols describe their consumed interfaces. Existing dictionaries remain the
runtime representation; mapping guards check incoming values before access. A
shape check is not a statement that a receipt is admissible scientific evidence.

These changes preserve the process deadline, cancellation, stop escalation,
reaping, worker joining, resource ownership, journal ordering, readback and
admission boundaries. An optional failure-stage access in an adversarial test now
asserts the key is present before checking its exact value.

Four new list/dictionary method/route cases reproduce the previous unhashable
`TypeError` and now require `ValueError("unsupported_request")` before any HTTP
connection is constructed. No successful request behaviour was intentionally changed.

The corrupt-coverage reader had a separate concrete resource defect: coverage
7.15.2 could open SQLite and fail during setup before its internal context manager
closed the connection. The validator now owns the complete lifetime with the
public `CoverageData.close()` method. A Python 3.13.5 comparison preserves the
unreadable-database rejection while changing the observed unclosed-connection
warning count from one to zero. The regression captures warnings during garbage
collection; warnings are not suppressed.

## Historical source integrity

The newly imported `json_shapes.py` is included in both the current session source
inventory and the current execution gate closure. The historical study-input test
checks the adapter blob at the source revision recorded in the retained execution
review, and binds that review to the exact protocol and adapter hashes. Both
workflows that run this test fetch the required Git history.

The historical protocol, review records, source receipts and failed study results
remain unchanged. Current engineering changes do not requalify the consumed study
or authorise a rerun. All four pinned production files remain byte-identical:
`darwin_runtime_profile.py`, `local_model_comparator.py`, `darwin_server_v030.py`
and `darwin_runtime_v030.py`.

## Reviewed baseline maintenance

Ordinary basedpyright initially surfaced 31 reports whose positions no longer
matched the retained baseline. A read-only reviewer traced all 31 to the old
source: 11 unknown-member, 12 unknown-argument, one unknown-variable and seven
private-use reports. Existing upstream producers still return unknown dictionaries;
the new checked guards expose that uncertainty at their arguments. The private
reports concern the same existing APIs, including `_Receipt` at its direct import.
There was no new incompatible type, missing member or invalid operation.

Only the six reviewed files were re-anchored to their exact 155 remaining reports,
down from 337 in those files. The selected maintenance changed the stored total
from 6,012 to 5,830; ordinary basedpyright then removed another 807 entries and
passed with 5,023. The retained baseline exactly matches the independent empty
baseline measurement by file/rule. Every policy cap was ratcheted to that count.
`--writebaseline`, enlarged caps, new rules, ignores and blanket casts were not used.
Unresolved upstream and intentional private-access debt remains visible.

## Verification at publication

| Check | Observed result |
| --- | --- |
| Ruff, formatting, ty and retained-baseline basedpyright | Passed |
| Exact baseline/cap comparison against master `a38dd9c` | Passed; 5,023 retained diagnostics |
| Hash-bound Bandit, Vulture and Unicode scan | Passed |
| Repository governance and deterministic benchmark | Passed; 7/7 cases |
| Live official skill validator, complete profile and monitored upstream drift | Passed; current conformance true |
| Coverage reader, historical inputs and execution gate focused tests | 57 passed |
| Process/HTTP/deadline suite | 111 passed, 25 unchanged socket-environment failures |
| Session/controller focused suite | 69 passed, 27 unchanged socket-environment failures |
| Full integrated pytest | 1,963 passed, 52 failed, 11 skipped; 93.30% branch-enabled coverage |
| Exact 52 failed IDs on unchanged source | Same 52 failures; zero normalized-message mismatches |
| Python 3.13.5 corrupt database comparison | Same rejection; one resource warning before, zero after |

The unchanged comparison checkout has exactly master's tree. Fifty failure
messages match verbatim; the other two differ only in generated session-directory
names. Normalisation is restricted to that random directory component. This proves
failure parity, not successful execution of the socket-dependent paths. No test
was disabled. The new head still needs hosted Linux/Python 3.11 and 3.15.2, macOS,
Windows, complete-matrix coverage, mutation, profiling, dependency, privacy and
conformance observations. Hosted status is recorded against the exact PR head,
separately from this local publication snapshot.

The prior increment's accepted head `ce35323999b87ee208c280a6b5ff5c0ff498dfc4`
passed [Quality 43400688051](https://github.com/edithatogo/rcagent/actions/runs/43400688051),
dependency review, privacy/secrets and official conformance before PR #127 merged
as `a38dd9c`. Its separately incorporated offline-security job was queued for its
dedicated self-hosted runner, not a completed security scan. That result is not
used as acceptance of this increment; no security workflow or bypass was changed.

## Review and next work

Two implementation lanes owned the process/HTTP and session/controller changes.
A read-only agent reviewed their source and test diffs, root's coverage/history
changes, and every surfaced baseline report. Root integrated the contracts,
checked global counts and gates, and retained the failure-parity evidence. These
reviews share project context and are not independent human or model observations.

Continue FAW06 with the native protocol, request/completion and observation-admission
contracts that still propagate unknown values into these callers. Migrate the
execution gate together with those consumers; annotating its plan dictionary alone
exposed unsupported operations in untouched callers and was therefore reverted.
Then address the largest remaining test fixtures and the separately recorded
enum/hashability defects. Preserve frozen production bytes when selecting that work.

The component demonstrations, hallucination-reduction comparisons, death-review
profiles and selective Rust experiment remain in their existing tracks. This
increment adds no clinical qualification, model observation or Rust migration.
