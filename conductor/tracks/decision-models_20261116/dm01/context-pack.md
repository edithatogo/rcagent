# DM01 bounded context and receiving map

Date: 17 November 2026, Australia/Brisbane. Scope: DM01 only. Working PR:
[#147](https://github.com/edithatogo/rcagent/pull/147).

## Authority, identity and ownership

The current instruction is: “Implement DM01, open a PR, check actions pass,
then merge.” It supersedes the initial planning-only boundary for DM01. This
increment completes context reconciliation, source admission and a frozen
synthetic study definition. It does not start DM02–DM11 or execute a model.

The initial reconciled context input is `master` at `8a564826a3f51765f177f0d9823194718bacb7d9`, tree
`47543fabfbfa8e6682f5b088b56e6982ae5af82d`. It includes D1, D2 and the D2
acceptance record. The published planning head was
`d837836b42cd2dc53a2e3e7188afb6e56b60da0f`; the local merge before DM01 edits was
`3e072299dae8d7277a2d6322beb72de13b2f89b4`, tree
`523db88ff508c973198d222ee176765e9bdf1f09`. These are input identities, not the
eventual tested PR head. [The context snapshot](./context-snapshot.json) binds
the inspected files to their actual bytes at the master revision.

Owned changes are the existing `decision-models_20261116` track and its single
row in `conductor/tracks.md`. Root integrates; two non-overlapping lanes own
source admission and study definition; an additional read-only reviewer audits
receiving interfaces. No production namespace is allocated here. Track 12
retains scientific ownership, Track 13 shared assurance/integration, and Track
14 death-review applicability. Shared coordinator
`6af6164f-cf84-8321-9f96-8b7d685aabe5` retains shared-interface acceptance.

There was no receiving acknowledgement in PR #147's comment or review
collections at preflight. Direct user authority is sufficient for this owned
DM01 increment and its merge; it is not recorded as an acknowledgement from
another owner. DM02 retains the production contract/file-allocation checkpoint.

## Bounded reading set and freshness

Read the root instructions, constraints, Conductor index/product/guidelines/
workflow, this track's specification/plan/contracts, the source register and
the files in the snapshot. Track 12's index and programme decision establish
research ownership and existing HDC authority. Track 13's current plan and
D0–D2 contracts/acceptance records establish receiving limits. Track 14's index
and workflow contract establish the separate application scope.

Budget: load this pack and the DM01 manifests first; inspect at most 12,000
additional tokens of selected source per receiving question. Retrieve exact
functions/contracts on demand instead of loading all fixtures, corpora or
unrelated tracks. Refresh branch heads, owned-file diffs and relevant receipts
before publication/merge; a changed production dependency invalidates only the
consumer relying on it. Historical source observations are not silently
rewritten to match a later head.

The live read confirmed PR #150 merged as `8bf94873af22730e445fcbb1b7fb748cfd16ed25`
and PR #151 merged as the master above. Their D2 acceptance receipt identifies
the tested implementation source `89425a12c15b4d533fb8610baed764fb429c86dc` and
tree `bda7e6384bca761842260a7a5c2dec64812dc2c3`.

| Other active ownership | Observed head | DM01 treatment |
|---|---|---|
| AcciMap, PR #141, draft | `dc42b2e5660c5070db0b1b48b5a83fd17f54425e` | Preserve its owner and planned mappings |
| HEAPS H4, PR #142, ready for review | `c9e7814f13b9036bb7d0a5de5548605f93a81243` | Record progress; do not import or claim its capability |
| Shared recommendations, PR #143, draft | `ff82e1a41283a500e579f5ef83e96b2802dd3e2e` | Preserve shared acceptance/registration scope |

These rows are a timestamped coordination snapshot, not permanent branch
locks. Later changes are reconciled in the verification receipt or PR record.

During DM01, PR #142 merged as `006d98cb60c72143b0517f0e7a446641642ddd5a`,
tree `5c55fde1cbe324973b71413f63367c773391d523`. That master was integrated
before publication. The 23 snapshotted input files and the D0–D3 receiving
observations remain byte-identical; the added H4/HEAPS implementation and its
skill material retain their owner's scope. The original input snapshot and
local failed run are preserved, with integration checks recorded separately.

## Existing-system fit and remaining gap

| Existing boundary | Available evidence | Consequence for this study |
|---|---|---|
| Canonical records | [`evidence_core.py`](../../../../tools/evidence_core.py), `validate_record`, canonical bytes and fingerprints | Reuse schema plus domain validation; do not equate renderer hashes with canonical identity |
| D0 identity | [`faw07_d0_demo.py`](../../../../tools/faw07_d0_demo.py), `inspect_case` | Exact case/source/version/digest and half-open UTF-8 byte spans; identity does not establish truth |
| D1 extraction | [`faw08_d1_extraction.py`](../../../../tools/faw08_d1_extraction.py), `extract_case` and `verify_extraction`; [contract](../../frontier-assurance_20261113/faw08-d1-contract.md) | Available bounded lexical comparator. Requires `synthetic-d1-extraction-only`; dates/times/quantities/assertion mentions retain ambiguity, assertion and provenance. No inferred event linkage, recording/availability clock or clinical truth |
| D2 chronology | [`faw09_d2_timeline.py`](../../../../tools/faw09_d2_timeline.py), `assemble_timeline` and `verify_timeline`; [contract](../../frontier-assurance_20261113/faw09-d2-contract.md) | Available for a later chronology task with caller-declared synthetic event/clock links. It is not an automatic D1-to-event mapper; display order is not temporal evidence |
| D3 decision-time packets | [Track 13 plan](../../frontier-assurance_20261113/plan.md), FAW10 | Pending. No dedicated implementation/contract found. The first study uses full synthetic views and makes no recipient-cutoff, entitlement or hindsight-isolation claim |
| Renderer admission | [`interface_actions.py`](../../../../tools/interface_actions.py), `render_view` | Schema validation plus renderer hash remain narrower than full domain validation. Repair belongs to the shared owner; this study does not use rendering as evidence admission |
| Runtime admission | [`runtime_lab.py`](../../../../tools/runtime_lab.py), `route_request` | Requires local/remote-code restrictions and admitted measured tuples; eligibility still returns `model_executed=false`. No currently supported decision tuple is inferred |
| Retrieval/encoders | [`retrieval_system.py`](../../../../tools/retrieval_system.py); [`encoder_adapter_eval.py`](../../../../tools/encoder_adapter_eval.py) | Reuse SQLite FTS5 for a later task. The deterministic vector oracle is not a measured encoder. Neither ontology retrieval nor a new vector store is needed for the first study |
| Approval/action boundary | [`interface_actions.py`](../../../../tools/interface_actions.py), `validate_approval`, dry-run adapter | Scores cannot grant authority or perform external actions. No connector or Power Automate execution in DM01 |

The remaining DM01 gap is a source-bound question and prospectively fixed
analysis procedure. Versioned Markdown/JSON are sufficient. No new engine,
runtime fork, web service, dependency or compatibility shim is justified.
Later adapters must use the existing ports and receive their path/schema
allocation in DM02. Remove a proposed adapter if its qualification fails;
preserve the negative evidence and the deterministic/manual path.

## Ready and blocked leaves

| Leaf | State at this increment | Evidence or next receiving condition |
|---|---|---|
| Context/ownership reconciliation | Ready within DM01 | This pack, snapshot and current instruction |
| Source/rights disposition | Ready within DM01 | [Admission manifest](./candidate-admission.json); metadata-only pins and explicit exclusions |
| Synthetic first-study procedure | Ready within DM01 | [Frozen protocol](./study-protocol.md); no case or holdout generation/access |
| DM02 schemas/fixtures and production paths | Pending, outside DM01 | Receiving agreement and next named implementation scope |
| DM03 model execution | Blocked for execution | Exact asset bytes, rights disposition, runtime/build/isolation/capability evidence and comparator admission |
| DM04 reference set/harness | Pending, outside DM01 | Independently authored and reviewed synthetic families, locked partitions and executable contracts |
| D0/D1 reuse | Available only in their accepted synthetic contracts | Adapt only after DM02 agreement; preserve exact source/view identities |
| D2 chronology consumption | Available, optional for later study | Caller-declared source-bound links; no inferred temporal correspondence |
| Decision-time/recipient-cutoff conclusions | Blocked on D3 | Accepted receiving contract and actual leakage verification |
| Model/runtime/clinical qualification | Not established | DM03–DM09 observations and their prespecified gates |
| Ontology/media/service/application branches | Excluded from first study | Separate exact rights, modality/runtime and receiving evidence if later selected |

The full-view synthetic task avoids making unsupported D3 claims. It does not
remove D3 from the wider research programme. Existing HDC ethics authority is
preserved within its recorded scope; no HDC case, private data or terminology
release is consumed by DM01.

## Acceptance, commands and handoff

DM01 accepts a reconciled context, an admission disposition that does not
promote missing assets, a fixed and numerically checked study procedure, and
acceptance/evidence-integrity/safety review. See [decisions](./decisions.md) and
[verification](./verification.md) for observed results and limitations.

Use the locked commands in `CONSTRAINTS.md`, the existing repository validator,
JSON/link/hash consistency checks and `git diff --check`. Hosted checks must
refer to the exact final head; local socket restrictions are retained as failed
observations. Before merging, verify current master, the PR head, changed paths,
required rules and check conclusions. Merge with the expected head and no gate
bypass. Rollback reverts only DM01/track documentation; it does not remove other
owners' implementation or erase the initial planning record.

The handoff is DM02 with its receiving agreement still pending. Model runs,
real cases processed and qualified clinical/model capabilities remain zero.
