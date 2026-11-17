# DM02 contract boundary, receiving allocation and rollback

Date: 17 November 2026, Australia/Brisbane.

## Authority and exact scope

The user authorised DM02 implementation, PR checks and merge. DM01's
[receiving map](../dm01/context-pack.md), [synthetic study](../dm01/study-protocol.md),
[contract proposal](../contracts.md) and current Track 13 interfaces were
reconciled before implementation. DM02 adds an **opt-in research companion**:
one [JSON Schema 2020-12](../../../schemas/decision-models-0.1.schema.json),
a checked [Python boundary](../../../../tools/decision_model_contracts.py)
and synthetic [tests](../../../../tests/test_decision_model_contract_matrix.py).

There is no import into the workbench, clinical application, registry or
routing engine. This is not model admission, a generation API or an approval
record. Source, access, jurisdiction, effective policy and review decisions
continue to originate with existing owners. The trusted source context is
separate from provider wire objects; provider instructions cannot create it.

### Proposed exclusive file allocation

| Owner | Exact path/scope | Disposition |
|---|---|---|
| DM02 isolated source | \`tools/decision_model_contracts.py\` | No upstream port modification |
| DM02 JSON authority | \`conductor/schemas/decision-models-0.1.schema.json\` | Version \`decision-models/0.1\` only |
| DM02 assurance | \`tests/test_decision_model_contracts*.py\` | Synthetic fixtures and Hypothesis |
| DM02 Conductor | \`conductor/tracks/decision-models_20261116/dm02/**\`, this track's local plan/index/metadata | No portfolio number allocation |
| Track 13 coordinator | \`tools/evidence_ports.py\`, \`tools/runtime_lab.py\`, \`conductor/schemas/safety-work.schema.json\`, runtime registry and shared CI | **Unchanged; receiving acknowledgment required** |
| Track 12 | Scientific datasets, references, estimates, groupings | Unchanged |
| Track 14 | Statutory applicability and death-review profile | Unchanged |

The [receiving handoff](https://github.com/edithatogo/rcagent/issues/125#issuecomment-6943868352)
requests the existing sole shared integrator's explicit agreement. The
standalone contract may be code-reviewed and merged as a nonoperational,
unconsumed research artefact; neither a green workflow nor the merge
substitutes for shared receiving acceptance.

## Wire and semantic mapping

- **Canonical schemas:** JSON Schema 2020-12 is normative for three discriminated
  messages (\`request\`, \`result\`, \`capability\`), each closed to unknown fields.
  All have an explicit \`decision-models/0.1\` version. The module uses
  \`Draft202012Validator\` with \`FormatChecker\`; wire parsing rejects oversize
  payloads, duplicate keys, non-finite constants/overflows and scalar roots.
  Strict JSON typing does not coerce booleans or numeric strings into numbers.
- **Identity and source domain:** request/result bind request, task-spec, case,
  view, source-manifest and capability hashes. The view hash is SHA-256 over
  *exact UTF-8 view bytes* provided by the trusted broker, not a stripped or
  re-encoded renderer digest. The capability and ordered candidate-set hashes
  use the existing \`tools.evidence_core.fingerprint\` canonical-JSON domain.
  They are deliberately distinct hash domains. Trusted anchors must remain in
  the same case/view and permitted source window, have matching source-byte
  digests and exclusive UTF-8 byte offsets; extracted strings require exact
  decoded span equality. No original source bytes are included in the wire
  result.
- **Existing ports:** \`Operation\` remains the owner of timeout, idempotency
  and privacy concepts. \`DecisionModelPort\` is a Protocol companion whose
  \`evaluate\` method has no implementation or registration. A future owned
  adapter maps \`result.status\` to existing \`OperationResult\` statuses,
  diagnostics and bounded retry rules; it must not treat a schema-valid answer
  as an accepted safety-work finding or a completed action.
- **States and runtime registry:** \`candidate\` and \`contract_tested\` map
  descriptively to \`interface_contract\`; \`measured_research\` and
  \`task_qualified\` to \`experimental\`; \`unavailable\` and \`withdrawn\` to
  \`unavailable\`. Those are **not writes or promotions**.
  \`runtime_route_eligible\` always returns false in this model-free package.
  Existing \`allow_remote_code=false\`, \`allow_external=false\`, no-model
  registry and prohibited governed-private routing remain unchanged.
- **Primitive semantics:** Noul is a bounded yes-probability; exclusive
  Choice/Score distributions have exact labels and sum to one within 1e-6;
  independent multi-label Choice need not sum to one. Candidate ordering and
  ontology identity remain bound. Ordinal summaries preserve original native
  semantics and direction. \`found<0.5\` forces null/missing, while equality is
  eligible under the frozen task rule; non-null values require source anchors.
  Typed number/date/image results cannot assume units, calendar precision,
  media coordinates or transforms. Box coordinates are normalized [0,1] with
  strict positive width and height; count and duplicate constraints apply.
- **Calibration and policy:** \`calibrated_probabilities=null\` is not zero;
  a populated calibration must name a matching trusted calibrator. An
  unmeasured or changed tuple cannot inherit another result's calibration.
  A deterministic broker policy, not model text, determines
  \`candidate_for_review\`, \`continue_bounded_step\`, \`escalate\`, \`abstain\`.
  Privacy/authority vetoes abstain; applicable hard-review/source-conflict
  signals escalate; invalid, unavailable, uncalibrated or uncertain inputs
  cannot become low-risk passes. No model can set \`approved\`, \`clinically_safe\`,
  \`action_effective\` or a statutory classification.
- **Error precedence:** bound parsing/size/version, schema/type,
  request/capability, identity/privacy/view, primitive semantics, calibration/
  policy, candidate mapping. Model-free validators return safe stable diagnostic
  classes and do not echo private source text. A later transport adapter must
  preserve attempt-level timings, retry budgets and the original deadline.

## Matrix, independent tests and limits

The independent synthetic C01–C42 test cases cover malformed JSON,
probability and label invariants, ontology/category identity, changed source
bytes and Unicode offsets, typed extraction, dates/units/regions, explicit
non-success statuses, capability denial, source and permission vetoes,
idempotency drift, calibration invalidation and forbidden approval/action
transitions. Hypothesis exercises Noul floating point and box geometry.
The [design matrix](../contracts.md#7-concrete-acceptance-fixture-matrix) is
broader than the DM02 software contract: e.g. correlated models, actual
prompt-injection resilience, candidate-retrieval recall, clinical review and
cross-model variation require later DM03–DM09 empirical packages. A model-free
negative test does **not** discharge those scientific controls.

JSON Schema checks shape; Python semantic checks depend on a
broker-provided \`ContractContext\`, not a caller-provided authorisation.
The current controls deliberately cannot show a valid model execution or
operational view: no inference, provenance of real cases, runtime isolation,
terminology rights or calibrated operating point is claimed.

## Backwards compatibility, invalidation and rollback

The new contracts are opt-in and have no production consumers. Existing
safety-work v1.1, record fingerprints, workflow status, runtime registry,
historical receipts and output renders are byte-unchanged. Unknown
\`schema_version\`, unsupported primitives, runtime changes, mismatched
task/rubric/source/capability/ontology/candidate hashes and stale source
anchors fail closed. Reusing an idempotency key with a changed bound view
computes a different identity; future caches must reject the collision
rather than reuse a prior answer. No automatic version migration is provided.

Rollback is **non-activating**: leave the companion unimported, remove any
future adapter registration through its owner, and revert the DM02 companion
files if necessary. No data migration, source rewrite, previous runtime
promotion or irreversible action is required. A future DM03 adapter must
supply its own compatibility tests and expiry/removal test; a model-free
pass cannot enable it.

## Receiving checkpoint

The current shared coordinator remains the sole owner of shared interface
allocation and production mapping. The DM02 proposal asks that owner to
accept or return the isolated paths and mapping before DM03/DM04 consume
them. Without an explicit receiving acknowledgment, **Checkpoint A2 is
engineering-qualified only; shared production integration remains held**.
