# Coordinator integration handoff

## Requested disposition

Accept or return this bounded planning track for issue #140, allocate its portfolio number after reconciling AcciMap #139, and register it through the existing shared integration lane. This PR changes only the dedicated HEAPS track. It does not merge itself or claim implementation ownership over any existing lane.

Coordinator: 6af6164f-cf84-8321-9f96-8b7d685aabe5. Observed baseline: c6892497aa0b03555d5145242c04965471eccc1d. The exact published commit and checks are recorded in the PR; planning validation and independent review are in this track.

## Concrete shared registration proposal

[registration-proposal.json](./registration-proposal.json) supplies the stable ID, issue, title, status, dependency semantics, registry text, context entry and field-level shared changes. It is proposed input, not an applied patch or a second active registry.

1. Re-read current master, all active owners, track numbers and this PR before applying anything.
2. Add the assigned-number entry to conductor/tracks.md and roadmap.md/.json using the existing schema; append the stable ID to roadmap.json workstreams[id=product-interfaces-distribution].tracks (parent issue #4); populate this track metadata.json track_number with the same assigned number; add a concise navigation entry to conductor/index.md.
3. Retain hard_dependencies empty. Phase gates are conditional on the capability consumed; avoid cycles through Tracks12/13/14 and do not make AcciMap mandatory.
4. Reference the existing QLD policy records. Add only reviewed missing HEAPS index/local-instrument source records and preserve rights/access status; do not label the internal template public because its index is public.
5. Assign a single owner for shared method-matrix/combination corrections before H2 consumes them; add portable-skill/template navigation only after corresponding assets exist and are admitted.
6. Assign new implementation namespaces and capacity when implementation is authorised. Do not displace the current D0 production/verifier or AcciMap owners.
7. Run normal required checks at the exact integrated head and record explicit acceptance/return. No merge, acceptance or hosted pass is implied by this proposal.

## Merge and work order

This docs-only planning PR can be reviewed independently of D0 or AcciMap implementation. The coordinator may integrate it and shared registration when current checks/ownership allow. Then H1 → H2/H3 → H4 → H5 → H6. H6.1 source acquisition is preparatory parallel work. Exact byte-span claims wait for D0 acceptance; optional graph composition waits for #139 acceptance. Other optional capabilities follow their own receipts.

## Acceptance boundaries and remaining gaps

Planning delivery includes source crosswalk, specification, profile contract, executable-work breakdown, machine-readable dependencies and acceptance design. It includes no implemented HEAPS validator/report generator, executed HEAPS tests, current CHHHS template, local conformity or clinical evidence. Existing rendering/participation remain synthetic-only. Public source snapshots lack fabricated checksums; unavailable sources retain explicit gaps.

Rollback: revert this dedicated planning commit/PR and any separately accepted shared registration together as needed; preserve prior engineering/scientific evidence and unrelated owners' work.
