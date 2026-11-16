# H2/H3 integrated implementation review

## Disposition and scope

H2 portable guidance/report mapping and H3 profile/fixture contracts are implemented
and independently reviewed on the HEAPS branch. Their phase checks pass. The full
local repository gate remains **failed**, with 52 environment-related existing
socket/session failures preserved below. This receipt does not claim a green
full local run, H4 assembly, H5 composed-runtime qualification, official-template
conformity, clinical/organisational authority, merge or deployment.

The user explicitly authorised implementing H2 and H3. The branch normally
reconciles prior HEAPS head `58fb0b15171322f70ee070cea6756f32fe792f50` with master
`d11548357baba6a1e20163139a366c6367a05432`; no prior branch history is rewritten.
D0 and the ty update are inherited from accepted master, not reimplemented by HEAPS.
The publication commit binds this receipt and the exact
[input manifest](./h2-h3-input-manifest.json).

## Review panel and independence

| Reviewer | Contribution and independent check | Disposition |
| --- | --- | --- |
| `/root/heaps_guidance` | Authored the two original H2 assets and checked their public-source basis. Independently inspected root-authored shared navigation/method changes. Subsequently reviewed all H3 schemas, contract and corrected independent fixtures, which this reviewer did not author; ran the combined 101-check suite. | No remaining blocking H2 content or H3 contract/fixture defect in reviewed scope. Author source checking is not counted as independent source corroboration. |
| `/root/repo_heaps_mapping` | Compared accepted master/D0 with the H1 baseline, then authored the four H3 schemas, contract and 52 structural tests. Coordinated field shapes without generating the independent oracle. | Producer checks passed; shared runtime gaps remain explicit. Producer self-checks are not independent H3 acceptance. |
| `/root/proposal_review` | Independently authored original synthetic sources/case, literal expected outcomes, raw/canonical identities and 49 fixture-design tests. Did not edit schemas or use producer output helpers to generate expected dispositions. | Frozen 25-case/38-variant design with 22 prepare/14 reject/2 abstain expectations. No H4/H5 execution claim. |
| `/root` | Reconciled master/owners; authored shared content integration and Conductor updates; reviewed H2/H3, checked all 38 canonical input variants against the existing validator, and ran integrated locked gates. | Corrections resolved before freeze; full local failure retained rather than relabelled. Shared registration and merge stay with the coordinator. |

These are agent engineering/content reviews with shared context and possible
correlated errors. They do not provide clinical, cultural, legal, organisational
or independent human authority. The substantive H3 contract reviewed at
`b3ff609d7f28cbfc2bb947bb8027c3a4a9990776e4a8a5af8e25aa03f34e0598`
subsequently received only its checkpoint-status/receipt-link update; the final
publication bytes are in the input manifest.

## Checks actually executed

The locked environment was installed with:

```text
uv sync --locked --extra validate --extra test --extra lint --extra assurance
uv sync --locked --extra validate --extra test --extra lint --extra assurance --group conformance
```

uv 0.13.6 selected CPython 3.15.2. The inherited lock includes jsonschema 4.26.0,
pytest 9.2.0, Ruff 0.17.3, ty 0.0.99 and basedpyright 1.40.2. Installation used a
normal file-copy fallback after a cache hardlink warning. HEAPS changed no
package dependency or lock relative to reconciled master.

| Check | Actual observed result and scope |
| --- | --- |
| `pytest -q tests/test_heaps_profile_contract.py tests/test_heaps_fixture_design.py` | **101 passed**: 52 structural and 49 independent design checks. The independent H3 reviewer reproduced the combined result. These are not HP01–HP25 runtime outcomes. |
| `pytest -q tests/test_template_admission.py tests/test_skill_adapters.py` | **69 passed**. Exact admitted template bytes, archive rejection boundaries and adapter contracts remain enforced. |
| Existing `tools.evidence_core.validate_record` on all 38 oracle case inputs | **38 admitted, zero diagnostics**. This checks canonical compatibility; it does not execute HEAPS profile/packet semantics. |
| `python -m tools.validate_skill_profile --require-complete` and pinned `skills_ref.cli validate` | Passed. |
| `python -m tools.run_skill_conformance` | Exit 0, local/current conformance true, official validator provenance verified at `69ef37e9424c0a7ea9dd2293b559e43ec8176379`. Live upstream changes were outside monitored specification/validator/guidance paths. See [machine receipt](./h2-conformance.json). |
| H2 content/static checks | One H1 per asset; UTF-8, whitespace, portable local links and guide anchors passed. No local link escapes the portable skill. Template inventory contains 41 exact-byte portable-draft assets. |
| `python -m tools.full_validation` | **Exit 1: 2,414 passed, 52 failed, 11 skipped; 93.39% branch coverage**. All preceding strict/static/security/governance/benchmark stages passed. Failure detail below. |
| Final reconciliation | Repository governance/diff checks passed; 38 input-file hashes matched; 23 JSON documents and six ledger events parsed; 113 local link destinations resolved. The final combined H3/template/adaptor rerun passed 170 checks. No shared portfolio registration or merge is inferred. |

The full run included Ruff correctness, formatting (165 files), ty, basedpyright
with 0 errors/warnings/notes, the zero-baseline ratchet, security, Vulture,
invisible-character checks, repository governance, benchmark validation and the
seven-case regression benchmark before pytest. Security returned success with
existing reviewed-source `nosec`-without-finding warnings; HEAPS added no
suppression, allowance, exclusion or changed gate.

## Full local failure retained

| Existing failing module | Failed tests |
| --- | ---: |
| `tests/test_prospective_primary_session.py` | 9 |
| `tests/test_prospective_server_session.py` | 17 |
| `tests/test_prospective_study_controller.py` | 1 |
| `tests/test_unix_http_capture.py` | 25 |
| **Total** | **52** |

Direct `socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)` raised
`PermissionError: [Errno 1] Operation not permitted` in this workspace. This
independently establishes the local socket restriction; it does not substitute
for those tests passing on a supported runner. The formerly missing historical
Git object is present, and the historical-source failure observed in H1 does not
recur. No test was disabled and no full-suite result was upgraded from a focused
rerun.

The full-run log is a transient execution artifact, 126,920 bytes, raw SHA-256
`f3bc73a598501af52112aa66b54fd3b99d542782a8b74088c82159d5cf7e0296`.
The exact command, counts, failing modules and restriction are retained here.
Hosted checks must be observed on the publication head and reported in PR #142;
queued, missing or unavailable checks are not passes. This local receipt does
not pre-claim their result.

## Corrections and preserved limits

Root and peer review repaired the canonical ID grammar, explicit involvement and
participation missingness, snapshot version/applicability, calendar conventions,
supporting-artifact coverage, source-check scope and stale review state. Fixture
review repaired raw-template tamper expectations, status-only abstention, stale
illustrative-status bindings and the method-handover arrangement. The withdrawal
count rule now matches both canonical withdrawal representations. See [H3](./h3.md)
for the precise design corrections.

Early lint/typing findings were repaired with explicit guards, split assertions
and a narrow supported-method Protocol for the upstream jsonschema stub. No
payload uncertainty was hidden with an unchecked schema cast or ignore. A
reviewer run while the corpus was being frozen observed the not-yet-written
fixture lock; the completed lock and 101 checks subsequently passed. The final
oracle did not obtain its semantic expectations from implementation results.

H1's 13-control diagnostic (9 expectations met, 4 unmet) remains historical at `58fb0b1`.
The existing renderer/domain mismatch and absent date-time enforcement are not
repaired by adding schemas. H4 must enforce canonical admission, strict dates,
source/role/hash resolution and receipt provenance. H5 executes the actual
interface/subprocess against the independent oracle. H6 handles the current
local instrument, rights, authority and practice evaluation. No model, real
case, official template, RiskMan write or clinical-effectiveness claim is part
of this delivery.

## Integration and rollback

The skill navigation/method/admission changes are reviewable integration
candidates in this branch. Their paths do not overlap the observed AcciMap
PR #141 or recommendation PR #143 changes. The coordinator retains shared registration,
exact-head acceptance and merge. Existing core schemas/validators, D0/AcciMap,
workbench, CI, lock and historical study files are unchanged relative to master.

Rollback the HEAPS profile/fixtures and the original asset with its associated
navigation/admission changes together through a normal commit. Preserve prior
source/case/decision history, negative evidence and template quarantine. The
next implementation is H4; no H4 runtime work is claimed by this checkpoint.
