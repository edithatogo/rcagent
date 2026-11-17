# FAW10 / D3: recipient- and cutoff-scoped synthetic decision packets

## Authority and scope

D3 follows the accepted D0, D1 and D2 sequence on Track 13, contributing a bounded
synthetic example to CAW10/20. The direct instruction is to implement D3, submit a
pull request, check hosted Actions and merge only when the normal gates pass.
The implementation branch started at master \`96c6fe25ecdaf07875ae205ba74d6404314085f2\`.
No open PR held D3 ownership. DM02, AcciMap, repository planning, security and
dependency branches retain their existing owners and are not implementation inputs.

D3 **does not claim** retrospective clinical truth, delivery receipt, comprehension,
authority to see real records, privacy isolation of a deployment, or automatic
semantic recognition. It uses only synthetic source and entitlement declarations.
Source/content hashes bind bytes but do not prove that an assertion is true.
The *only* supported downstream interfaces are scoped retrieval, exact-text
verification and rendering, each verifying the full packet against the same
source input, actor and cutoff. No unscoped corpus search or general model call
is introduced.

## Input and admission

\`assemble_decision_packet(case: object)\` takes an object with exactly:

- \`permitted_view=synthetic-d3-decision-only\`;
- \`recipient_id\`: a D2-enumerated actor (up to 128 UTF-8 characters);
- \`cutoff_utc\`: a valid full \`YYYY-MM-DDTHH:MM:SSZ\` second, with no implicit
  timezone or clock source;
- \`timeline\`: one complete D2 input object with all eight required keys;
- \`entitlements\`: up to 512 explicit declarations, one per source ID,
  source version and recipient, each with \`first_available_utc\` equal to a
  valid explicit UTC second or \`null\` for unknown; and
- \`labels\`: one per D2 event, with \`event_id\`, \`kind\` and
  \`speaker_role\`. Kinds are \`observation\`, \`outcome\`, \`appraisal\` and
  \`patient_family_concern\`. Concerns require a declared \`patient\` or
  \`family\` speaker; other kinds require a null speaker.

Entitlement and label associations are **caller-declared synthetic metadata**.
They must reference admitted IDs and are not independent observation or semantic
evidence. Every source is checked against D0's full SHA-256 and byte-span
witnesses through D2. Unknown or duplicate entitlements or labels, wrong
recipients/views, malformed calendar values, unsupported fields and tampered
provenance fail closed. There is no permissive timezone interpretation or
default first-available date. A same-source revised document is a distinct,
immutable source version.

## Cutoff projection

All D2 input sources and spans are admitted for integrity in the internal
validation compartment. They are **not returned**. For the requested actor,
admit only source versions with an explicit, known first-available UTC second
at or before the cutoff. Remove all remaining versions *before* the first
D2 chronology construction. Remove event, clock, amendment and relation
references to excluded sources, and clock assertions for other recipients.
A post-cutoff source amendment therefore cannot retroactively replace a
pre-cutoff clock assertion.

An event enters the candidate packet only if its source version was admitted,
the target actor's event-availability summary has known UTC windows wholly
at/before the cutoff, and any active recording-time assertion has known windows
wholly at/before the cutoff. If an event-time summary has windows, all possible
event times must be at/before cutoff. Outcome and appraisal entries additionally
require a wholly pre-cutoff known event time. Unknown or conflicting windows that
could cross the cutoff produce abstention; no best-case timestamp is chosen.
Missing recording clocks are not substituted for availability clocks; a present
but unresolved recording assertion is withheld.

Reconstruct chronology *again* on entitled events only. Excluded nodes and
their relations cannot influence pair order, cycles, feasibility or display
order. The resulting packet contains only the entitled actor's event spans,
their D2 summaries and support IDs, visible pairs/edges, a deterministic
display order when consistent and a source/view-derived fingerprint. It omits
all raw source contents, all other-recipient clocks, all excluded event IDs,
their counts and any future outcome/appraisal text. The packet may report
\`not_documented_at_cutoff\` for family concerns; **this does not mean**
the family had no concerns.

## Downstream and replay

- \`retrieve_decision_evidence(case, packet, query)\` does literal substring
  matching over **only the revalidated, scoped packet**. There is no full
  source-index, search fallback or external retrieval interface.
- \`verify_decision_claim(case, packet, event_id, statement)\` confirms only
  exact source-span text equality to a visible event; it never verifies
  semantic entailment, factual correctness or a causal conclusion.
- \`render_decision_packet(case, packet)\` renders only the freshly replayed
  canonical packet bytes, not a raw D2 case.
- Each downstream call recomputes the actor/cutoff projection and compares
  canonical bytes. Forged, stale or other-recipient packets are refused.
  The fingerprint is deterministic integrity/replay metadata, **not**
  a secret-key signature or an access-control credential.

## Finite tests and qualification

The test suite must include late results, delayed notes, same-event different
recipient availability, explicit unknown availability, changed late outcome
with unchanged earlier packet, late source revisions and amendments, absent
and present family concerns, inconsistent chronology isolation, invalid
spans/digests, invalid cutoffs, mutated packet rejection and all three
downstream interfaces. The D3 demonstration emits an auditable synthetic
research receipt; the receipt's unrestricted *synthetic fixture inputs* must
never be mistaken for an actor-facing decision packet.

No model evaluation, held-out clinical set, person-level rights check,
independent observed delivery, legal privilege or prospective clinical
validation is inferred from passing software checks. Checkpoint B, D4 and
wider CAW10/20 qualification remain open. Restore the previous source commit
if the D3 adapter fails; do not weaken strict typing, privacy or claim gates.
