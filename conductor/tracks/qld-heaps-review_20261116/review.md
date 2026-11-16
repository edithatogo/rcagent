# Independent planning review

Reviewed on 16 November 2026. Two read-only agent reviewers inspected the actual planning files and the relevant existing contracts. They shared conversation context; this is an agent engineering panel, not an independent human clinical review, organisational approval or empirical qualification.

## Reviewer scopes and disposition

| Reviewer | Scope | Initial finding | Remediation and final disposition |
| --- | --- | --- | --- |
| /root/proposal_review | Specification, profile/packet contract, sequence/DAG, acceptance design, metadata and source boundaries | P2: HP21 conflated semantic equivalence with unchanged identity under array permutation. P3: packet/profile hashing could be read as circular. | Split HP21 replay/object-key invariance from HP25 changed array bytes; preserve new hash and stale bindings. Specify detached acyclic construction and separate approval. Narrow re-review found both resolved and no remaining blocking finding in scope. |
| /root/repo_heaps_mapping | Ownership, existing component/AcciMap boundaries, registration proposal, context, metadata, fit-gap and implementation order | Low: proposal should name workstream membership and eventual metadata track_number update explicitly. | Added roadmap workstream append target, parent issue #4 and consistent number allocation. Narrow re-review found resolved and no remaining blocking ownership/integration finding. |

## Exact amended bytes re-reviewed

| File | SHA-256 at remediation review |
| --- | --- |
| contract.md | 90907174f5a2d4df8dcc9b49a017faaa0f94160ab4a15b7efc5e59b527dbab63 |
| acceptance-catalogue.json | c6881b817a94a3017306ab5bdc2d042b3d366d6236e090c59c762b7a5b8773a5 |
| plan.md | cd7828f502fdb2b377e4a3c45dfd166f8e1730241b7f6a09cb3f188cef829a8e |
| registration-proposal.json | dac951039cf8fa5b023a1a0a57875ca5821ea044d8716a5b61066663cb8044fe |
| integration-handoff.md | baf270ea6398d7be2215a13ea08b12762d196bb67bcf3f1822872eb45d45005e |

The earlier plan/metadata versions reviewed were planning-pending. After remediation review, root changed only the P0 checkpoint to reflect executed checks and the administrative verification fields in metadata, then recorded this receipt. Those final administrative file identities are listed in planning-evidence.md separately; the hashes above are not relabelled as the later bytes.

## Preserved initial findings

The original HP21 expected stable identity for repeat/round-trip/permuted inputs. Existing canonical serialization preserves array order, so changed array bytes must change identity even if a permitted unordered semantic comparison is equivalent. The original contract excluded each object's own digest field but did not fully exclude a cross-object manifest/profile cycle. Both were corrected before publication rather than accepting an ambiguous implementation target.

The original registration proposal omitted explicit workstream membership and metadata numbering follow-through. The shared coordinator must substitute an actual unallocated number before applying the proposed record. Neither a placeholder nor a pending proposal is registered execution state.

## Limits

Reviewers did not run HEAPS tests, verify a live clinical workflow, inspect the internal QHEPS/CHHHS instrument, or establish legal/clinical/operational authority. Source-author work was not counted as independent source corroboration. Root's separate structural checks validate planning artefacts; the repository validator alone does not fully validate an as-yet-unregistered track. Coordinator acceptance, shared registration, required hosted checks and any later implementation remain distinct.

## Hosted-check metadata remediation review

After the first draft's privacy check flagged the public timezone metadata as a generic API-key candidate, /root/proposal_review independently inspected the three-file correction. The reviewer confirmed the source inventory is semantically identical after renaming the timezone field, all 14 input hashes and the documented current manifest match, the evidence ledger preserves historical identities, and no scanner rule or shared/runtime file changed. No blocking finding remained in this narrow review. The reviewer did not run Gitleaks or inspect hosted logs; hosted results on the replacement commit remain separate.

| File | SHA-256 at remediation review |
| --- | --- |
| sources.json | 5cb5411dd121a80359491b21c632a7c8204ebd06509bb924d53bf23543aa43fa |
| planning-evidence.md | 34778c74edd4d6756cf5042179d3f0d4b7a8230af3084a081e0f10f0cbd8d264 |
| evidence.jsonl | 21abb9cbc076c3d213823071c170d36b27ac2fb21f069eb45c9f4b4ee216c4c9 |
