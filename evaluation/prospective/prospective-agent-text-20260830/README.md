# Prospective agent-text planning inventory

This separate, repository-authored synthetic planning study implements the
manifest and inventory part of [decision 20260830-002](../../../conductor/decisions/20260830-002-prospective-agent-study.md).
It does not replace historical H0–H8/H8P or their denominator. The new two-case,
one-condition, one-repeat denominator is a planning scaffold, not a frozen or
powered research design. `condition-local-text` names an unassigned candidate,
not a selected model, executable adapter, observation or recommendation.

## Reproduce the scoped inventory

From the repository root:

```sh
uv run python -m tools.prospective_inventory --manifest evaluation/prospective/prospective-agent-text-20260830/manifest.json --expected-sha256 a21bf8cd1676a20f422b75275307e5be30e203ba7a9755f2ba50d78735e8f2be
```

The pin must come from the reviewed manifest revision, not be silently
recomputed to accept changed input. Version changes require a new pin and
review. SHA-256 establishes byte identity, not authenticity or synthetic
provenance. Cases here are original generated examples with synthetic
placeholders; tests cannot prove arbitrary caller-supplied text is synthetic.

The command validates schema, identities, exact Cartesian expected slots and
case/rubric pins. It inspects only the adjacent `submissions/` directory, one
level deep, with at most 1,000 entries. The empty tracked `.gitkeep` is ignored
only if it remains an empty regular nonsymlink file. A missing or unreadable
root fails; it is not reported as an empty successfully audited cohort.

Exit 0 means the inventory command completed, never admission. Its output is
`planning_inventory` with `study_unlocked: false` and zero admitted slots.
Missing expected slots are pending; supplied expected slots are quarantined.
Unexpected entries are counted without exposing their filenames or contents.
All expected slots remain in the denominator regardless of disposition.

## Candidate package checks

Expected packages live at `submissions/<slot-id>/receipt.json`; paths within
the receipt resolve only under that slot directory. The strict receipt schema
is `SUBMISSION` in `tools/prospective_inventory.py`. It binds the study ID,
manifest hash, slot ID and input hash, plus raw and normalized byte references.
This version supports only an identity UTF-8 normalization join: raw and
normalized bytes must be identical, and source/target hashes must agree.
Other normalization methods remain unsupported rather than inferred.

Fixture-marked receipts, identity mismatches, malformed JSON, invalid paths,
missing files, stale hashes and broken joins are quarantined with reasons.
Even a structurally consistent package is quarantined as
`execution_provenance_unverified`: there is no attestation-equivalent execution
adapter, model identity verification, timestamp validation or affirmative
admission yet. Relabelling a fixture cannot bypass this lock.

Files are bounded to 4 MiB each and existing symlinks are rejected. Checks
assume a stable, trusted local checkout; they are not an atomic snapshot or a
sandbox against concurrent filesystem replacement or hardlinks. Inventory
completion does not freeze inputs. Rerun after any submission or input change.

## Current evidence and next work

The scoped run on 2026-08-30 found two expected slots, both pending due to
missing submissions; no quarantined or unexpected entries and zero admitted.
This says nothing about current historical eligibility, uninspected locations,
all available executable conditions, or a completed Option C fallback.

Next, assign and verify an executable condition and provenance-capture adapter,
finalise and freeze the input/rubric/blinding/scoring protocol, then implement
affirmative admission separately from scoring and analysis gates. Existing
standing approval covers bounded implementation and agent review; no repeat
approval is required. No provider execution, acquisition or scoring occurred.

Agent review is repository review, not independent human agreement or clinical,
legal, policy, regulatory, employment, cultural-safety, organisational or
deployment validation. These boundaries remain external. The parent track and
root issue #1 remain incomplete.
