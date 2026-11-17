# Proposed decision-model interface contracts

This is the original design appendix to [the specification](./spec.md), proposal version `decision-models/0.1`. The fragments below are **historical explanatory examples**, not complete installed schemas. DM02's opt-in canonical [JSON Schema](../../schemas/decision-models-0.1.schema.json), [checked Python companion](../../../tools/decision_model_contracts.py) and [receiving/rollback map](./dm02/contract-mapping.md) implement a bounded model-free subset. JSON Schema remains canonical; Pydantic is optional. No existing public interface or runtime registry has been changed, and shared acceptance remains with the coordinator.

## 1. Port and capability contract

The proposed `DecisionModelPort` exposes capability discovery and a bounded `evaluate(operation, request)` returning a typed result. Reuse `Operation`/`OperationResult` concepts in `tools/evidence_ports.py`; exact symbols and files are allocated by the integrator. Evaluation is side-effect-free with respect to findings, approvals and records-system updates.

A capability receipt is immutable and identifies:

| Field group | Required meaning |
|---|---|
| Identity | Provider, model repository/immutable revision, weight and implementation hashes, tokenizer/processor hashes, runtime/transport versions, precision/quantisation and device profile. Floating aliases are insufficient. |
| Coverage | Supported primitive and modality combinations, multi-label availability, source-offset conventions, number/date/box semantics and provider confidence definition. Absence means unsupported. |
| Limits | Measured context/text/media/candidate/question/batch/output limits, number of image regions, audio duration, concurrency, timeout and memory envelope. No silent truncation. |
| Evidence | Source documentation snapshot, code/licence/model/data admission, contract result, actual execution receipt, calibration binding and last verification date. Documentation is distinct from measurement. |
| Privacy | Mode, data class, network/telemetry/cache/log behaviour, reviewed remote-code policy and actual isolation evidence. A wrapper cannot upgrade these declarations. |
| State | Candidate, contract-tested, measured-research, task-qualified, unavailable or withdrawn, mapped explicitly to existing registry vocabulary. No new status silently enters shared registries. |

DM02 must agree a mapping from these proposed states and records to existing runtime/capability schemas. Keep this companion separate until that mapping passes. Current `allow_remote_code=false`, `allow_external=false` and governed-private restrictions remain in force. A special public/synthetic admission experiment must be explicitly scoped through the existing measurement protocol; it cannot make application routing eligible before measurement exists.

## 2. Canonical request

The request binds questions to one immutable, authorised evidence view. The broker resolves local source handles after access checks and supplies only the permitted projection to the adapter. No request may supply arbitrary URLs, file paths, executable patterns or model-provided tool instructions.

| Field | Type and constraints |
|---|---|
| `schema_version` | Literal `decision-models/0.1`; unknown versions reject. |
| `request_id`, `task_id`, `task_spec_hash` | Nonempty stable IDs and SHA-256 of the task definition. The task defines allowed primitives, labels, semantics and authority boundary. |
| `case_id`, `view_id`, `view_hash` | Exact case/view binding; `view_hash` is over the declared canonical view bytes, not a renderer hash with a prefix removed. |
| `source_manifest_hash` | Fingerprint of immutable permitted source versions, source-family lineage and transformation maps. |
| `privacy_mode` | Existing vocabulary: `public_remote`, `governed_hybrid`, `fully_local`, `air_gapped`; declaration does not itself grant permission. |
| `data_class`, `compartment_id` | Existing runtime data-class mapping and authorised compartment, checked against actual source policy. |
| `capability_receipt_hash` | Exact admitted runtime/model/primitive tuple; no implicit latest-model resolution. |
| `questions` | Nonempty bounded list of discriminated question objects; unique question IDs. |
| `operation` | Existing timeout/idempotency/privacy concepts. Deadline includes queue and retry time. |

Every question has a unique `question_id`, registered `instruction_id` and `instruction_hash`, plus the primitive-specific fields below. Patient/witness text is untrusted data; it cannot replace the instruction/rubric or add options.

| Primitive | Input fields | Input validation |
|---|---|---|
| `noul` | Binary question/rubric identifier | The meaning of “yes”, missing evidence and escalation is explicit. No caller-supplied policy authority. |
| `choice` | `multiple` boolean; candidate objects with stable ID and description; `candidate_set_hash` | Unique IDs; allowed count; fixed NIL/insufficient paths; no unsupported multi-label request. Hash includes labels, descriptions and ordering; evaluation records any deliberate permutation. |
| `score` | `rubric_id`, `rubric_hash`; ordered level IDs/descriptions and severity ordering | At least two levels, within the measured provider limit. Direction, endpoints, severe subset and permitted summaries are explicit. |
| `text` | Field definition and allowed source selection | Exact extraction only; returned text must be source-grounded. |
| `number` | Field definition, permitted units and optional syntactic bounds | Extraction versus estimation is a distinct task. No coercion of a unitless number into an assumed unit. |
| `date` | Field definition and known locale/precision constraints | No assumed year/time zone. Ambiguity remains an interval/unknown in the mapping record. |
| `box`, `boxes` | Admitted image/page handle, dimensions, transformation ID; bounded count | Exact media/region support required; no arbitrary remote image resolution. |

A request schema is compiled from a trusted task definition, not generated by an untrusted model. `additionalProperties: false`, explicit required fields and bounded arrays apply throughout. JSON duplicate keys, non-standard NaN/Infinity, numeric booleans, coercive strings and oversized payloads reject before domain validation. The declared schema alone cannot check hashes, permissions, cross-case references or deadlines; those validators are mandatory.

## 3. Result envelope and provenance

| Field | Required meaning |
|---|---|
| Request binding | Request/task/case/view/source/candidate hashes exactly match the input; provider response IDs alone are insufficient. |
| `status` | `ok`, `abstained`, `unsupported`, `invalid_input`, `invalid_output`, `timeout`, `cancelled`, `unavailable` or `error`. The outer operation contract maps these explicitly. |
| `answers` | Exactly one result or explicit failure per requested question, with the same ID/type. No silent omission, invented question or successful empty response. |
| Native observation | Provider-native semantic fields and bounded raw-response hash. Any retained raw content stays in its original permitted compartment. |
| Canonical prediction | Validated probabilities/value/regions plus source binding. This remains a candidate, not a finding or approval. |
| Calibration | Raw probabilities, separately named calibrated probabilities or null, calibrator identity, calibration-population/split hash and validity scope. Null means not calibrated, not calibrated at zero. |
| Policy | Threshold/routing policy hash, applicable rubric/jurisdiction version and outcome/reasons. The model does not set its own threshold. |
| Cost/timing | Actual input/output usage or explicit unavailable; monotonic stage/end-to-end durations, retries and resource observations. Do not fabricate zero costs for missing counters. |
| Reproducibility | Model/runtime/precision/device/lock identities; seed where meaningful; deterministic configuration and observed repeat variability. A seed does not guarantee bitwise determinism. |

All decision outputs have an authority label of `advisory_candidate`. The downstream disposition is one of `candidate_for_review`, `continue_bounded_step`, `escalate` or `abstain`; it cannot encode `approved`, `clinically_safe`, `no_reporting_duty` or `action_effective`.

## 4. Primitive output shapes

The following valid JSON Schema 2020-12 document describes primitive **payloads**. It is deliberately a design fragment: common envelope, request-derived label enums, actual source binding and the cross-field validators in section 5 are required for a complete implementation. Passing this fragment alone is never admission.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "urn:rcagent:proposal:decision-model-payload:0.1",
  "oneOf": [
    {"$ref": "#/$defs/noul"},
    {"$ref": "#/$defs/choice"},
    {"$ref": "#/$defs/score"},
    {"$ref": "#/$defs/typed"}
  ],
  "$defs": {
    "probability": {"type": "number", "minimum": 0, "maximum": 1},
    "probabilities": {
      "type": "object", "minProperties": 1,
      "additionalProperties": {"$ref": "#/$defs/probability"}
    },
    "noul": {
      "type": "object", "additionalProperties": false,
      "required": ["kind", "p_yes"],
      "properties": {
        "kind": {"const": "noul"},
        "p_yes": {"$ref": "#/$defs/probability"}
      }
    },
    "choice": {
      "type": "object", "additionalProperties": false,
      "required": ["kind", "multiple", "probabilities", "selected_ids"],
      "properties": {
        "kind": {"const": "choice"},
        "multiple": {"type": "boolean"},
        "probabilities": {"$ref": "#/$defs/probabilities"},
        "selected_ids": {
          "type": "array", "uniqueItems": true,
          "items": {"type": "string", "minLength": 1}
        }
      }
    },
    "score": {
      "type": "object", "additionalProperties": false,
      "required": ["kind", "ordered_level_ids", "probabilities", "native_summary", "native_semantics"],
      "properties": {
        "kind": {"const": "score"},
        "ordered_level_ids": {
          "type": "array", "minItems": 2, "uniqueItems": true,
          "items": {"type": "string", "minLength": 1}
        },
        "probabilities": {"$ref": "#/$defs/probabilities"},
        "native_summary": {"type": ["string", "number", "null"]},
        "native_semantics": {
          "enum": ["ordinal_median", "weighted_position", "category", "unavailable"]
        }
      }
    },
    "region": {
      "type": "object", "additionalProperties": false,
      "required": ["top", "bottom", "left", "right"],
      "properties": {
        "top": {"$ref": "#/$defs/probability"},
        "bottom": {"$ref": "#/$defs/probability"},
        "left": {"$ref": "#/$defs/probability"},
        "right": {"$ref": "#/$defs/probability"}
      }
    },
    "typed": {
      "type": "object", "additionalProperties": false,
      "required": ["kind", "found", "value", "unit", "source_anchor_id"],
      "properties": {
        "kind": {"enum": ["text", "number", "date", "box", "boxes"]},
        "found": {"$ref": "#/$defs/probability"},
        "value": {
          "oneOf": [
            {"type": "null"},
            {"type": "string"},
            {"type": "number"},
            {"$ref": "#/$defs/region"},
            {"type": "array", "items": {"$ref": "#/$defs/region"}}
          ]
        },
        "unit": {"type": ["string", "null"]},
        "source_anchor_id": {"type": ["string", "null"]}
      },
      "allOf": [
        {
          "if": {"properties": {"found": {"exclusiveMaximum": 0.5}}},
          "then": {"properties": {"value": {"type": "null"}, "unit": {"type": "null"}, "source_anchor_id": {"type": "null"}}}
        },
        {
          "if": {"properties": {"kind": {"const": "number"}}},
          "then": {"properties": {"value": {"type": ["number", "null"]}}}
        },
        {
          "if": {"properties": {"kind": {"enum": ["text", "date"]}}},
          "then": {"properties": {"value": {"type": ["string", "null"]}, "unit": {"type": "null"}}}
        },
        {
          "if": {"properties": {"kind": {"const": "box"}}},
          "then": {"properties": {"value": {"oneOf": [{"type": "null"}, {"$ref": "#/$defs/region"}]}, "unit": {"type": "null"}}}
        },
        {
          "if": {"properties": {"kind": {"const": "boxes"}}},
          "then": {"properties": {"value": {"oneOf": [{"type": "null"}, {"type": "array", "items": {"$ref": "#/$defs/region"}}]}, "unit": {"type": "null"}}}
        }
      ]
    }
  }
}
```

The canonical `found` field may be populated only when the provider exposes a compatible detection quantity. If a runtime returns regions without an equivalent probability, the adapter must use a separately specified capability/variant or report unsupported; it must not fabricate `found`. Per-region evidence/confidence belongs in the source-anchor records where actually available. Text/date fields require nonempty source-supported values; date/time validation uses an explicitly enabled format checker and stricter domain checks, not a JSON Schema `format` annotation alone.

### Request schema fragment

This design fragment makes the four question families explicit. The full request envelope and task-specific bounds are defined above and are frozen in DM02.

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "urn:rcagent:proposal:decision-model-question:0.1",
  "type": "object",
  "additionalProperties": false,
  "required": ["question_id", "instruction_id", "instruction_hash", "kind"],
  "properties": {
    "question_id": {"type": "string", "minLength": 1},
    "instruction_id": {"type": "string", "minLength": 1},
    "instruction_hash": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
    "kind": {"enum": ["noul", "choice", "score", "text", "number", "date", "box", "boxes"]},
    "multiple": {"type": "boolean"},
    "criteria_id": {"type": "string", "minLength": 1},
    "criteria_hash": {"type": "string", "pattern": "^[a-f0-9]{64}$"},
    "field_spec_id": {"type": "string", "minLength": 1},
    "media_anchor_id": {"type": "string", "minLength": 1}
  },
  "allOf": [
    {
      "if": {"properties": {"kind": {"const": "choice"}}},
      "then": {"required": ["multiple", "criteria_id", "criteria_hash"]}
    },
    {
      "if": {"properties": {"kind": {"const": "score"}}},
      "then": {"required": ["criteria_id", "criteria_hash"]}
    },
    {
      "if": {"properties": {"kind": {"enum": ["text", "number", "date", "box", "boxes"]}}},
      "then": {"required": ["field_spec_id"]}
    },
    {
      "if": {"properties": {"kind": {"enum": ["box", "boxes"]}}},
      "then": {"required": ["media_anchor_id"]}
    }
  ]
}
```

Resolve criteria and field IDs only from the hash-bound trusted task registry. Irrelevant fields are rejected by the discriminated domain validator even where this compact fragment permits them. DM02 must turn these fragments and tables into complete schemas with positive and negative examples; this planning document does not claim complete executable schema coverage.

## 5. Mandatory semantic validators

1. **Probabilities:** finite numeric values in `[0,1]`, never booleans. Exclusive Choice and Score keys match the request exactly and sum to one within a declared canonical tolerance (`1e-6` proposed). Multi-label values are independent and must not be normalised as a simplex. Any documented wire-rounding conversion needs an explicit adapter rule, retained raw values and a bounded delta; no silent repair of arbitrary bad output.
1. **Choices:** all selected IDs belong to the candidate set. Exclusive predictions have at most one selected candidate; an empty prediction is explicitly abstained. Multi-label selections follow the frozen per-label threshold/constraints, with an empty set distinct from unavailable inference. Candidate NIL and epistemic insufficiency remain distinct outcomes.
1. **Ordinal scores:** level ordering and severe subset match the rubric, not lexical/numeric label order. Native median/category/weighted-position semantics are explicit. Preserve the complete distribution; recompute any canonical diagnostic under its named rule. Never average SAC/ISR/P priorities without an approved mathematical interpretation.
1. **Typed values:** below the `found` boundary require null value/unit/anchor; a provider's conflicting non-null answer is invalid output. At/above the boundary, null remains possible but requires an explicit missing/abstained reason. Non-null requires a valid source anchor and any higher task acceptance threshold. No estimated value is reclassified as extraction.
1. **Anchors:** bind source ID, version, case, raw digest, representation/transform and original UTF-8 start/end or image/time region. End is exclusive; start must precede end and exact bytes match. Audio anchors use bounded start/end times with known recording identity; do not claim a text byte span without an admitted transcript.
1. **Numbers/dates/regions:** verify source units, bounds and permitted conversion; explicit calendar/locale/precision; `top < bottom`, `left < right` and original dimensions/transforms. Unknown timezone or missing year stays unknown. Limit region count and reject duplicates where the task requires unique instances.
1. **Authority:** eligible transport and source view first; model scores cannot bypass evidence checks, method ownership, clinical review, disclosure/approval or action state rules.
1. **Calibration:** require exact tuple/task/candidate procedure binding before using calibrated thresholds. Raw confidence without such evidence remains raw. Statistical consistency is not a guarantee for an individual case.

Pydantic integration, if justified, uses strict discriminated models, finite bounded numbers, `extra='forbid'` and explicit model validators, with schema parity tests against the canonical JSON Schema. Keep raw boundary data as `object` until checked; no explicit `Any`, unchecked casts or baseline allowances. Reuse existing canonical hash functions for the correct domain; record any domain distinction rather than stripping digest prefixes.

## 6. Failure, retry and continuation contract

Validate in stable order: transport/size/version → shape/type → request/capability → identity/privacy/view → primitive semantics → calibration/policy → candidate mapping. Record all safe diagnostics without echoing sensitive input; where a single public error is returned, this order defines precedence. Errors never return a successful accepted candidate.

Retry only a declared transient transport/resource error, within the original deadline and a frozen retry budget. Contract, rights, privacy, capability and source-integrity failures are not retryable. Idempotency includes request/task/view/model hashes: reusing a key for different content rejects. A timed-out or cancelled result arriving later cannot be admitted. Retrying may produce a different observation; preserve attempts rather than pretending the model is deterministic.

Fallback is the already authorised rules/manual path or a predeclared same-compartment model. Record fallback identity and attribute its outcome/cost to the cascade. Missing calibration, expired thresholds, out-of-distribution flags or material disagreement never silently become a low-risk pass. Remote fallback and extra context access require their own established authority.

## 7. Concrete acceptance fixture matrix

These are required future tests, not tests executed during this planning change.

| IDs | Independent inputs/negative controls | Required result |
|---|---|---|
| C01–C03 | NaN/Infinity, negative/>1 probability, numeric boolean/string, duplicate JSON keys | Invalid output/input with stable error class; no candidate accepted. |
| C04–C06 | Exclusive mass not one; missing/extra class; two labels each 0.9 in multi-label | First two reject; valid independent multi-label probabilities remain unchanged. |
| C07–C08 | Invented code; correct code outside the supplied candidate set; wrong ontology release | Reject candidate selection, preserving retrieval failure as a separate result. |
| C09–C10 | Same ordinal vector under median and weighted-position providers; reversed SAC label direction | Retain distinct native summaries; canonical severe-tail calculation follows the explicit rubric. |
| C11–C13 | `found=0.499999`, `0.5`, `0.500001`; absent field versus null; non-null below boundary | Null/missing below threshold; equality follows explicit task policy; malformed contradictory output rejects. |
| C14–C16 | Multibyte Unicode, shifted source span, cross-case/stale digest, source outside authorised cutoff | Exact identity/byte/cutoff failures reject even with probability 1. |
| C17–C19 | Ambiguous date/missing year, invalid calendar date, wrong or converted unit without source support | Preserve ambiguity or reject; never invent a timestamp/quantity or recommend treatment. |
| C20–C21 | Inverted/out-of-bounds boxes, wrong page/crop, excess regions, unsupported per-box confidence | Reject or explicit unsupported; no invented confidence/coordinate provenance. |
| C22–C24 | Timeout, cancellation and late response; unavailable runtime; missing calibration | Explicit failure/abstention; bounded local/manual fallback; no hidden remote call. |
| C25–C27 | GGUF typed/multi-label request; absent audio support; remote-code-required model under current policy | Unsupported/no capability before inference; no emulation disguised as native support. |
| C28–C30 | High-risk rule plus low model score; source conflict; same-model critic agreement | Escalate/preserve alternatives; no majority override or independence claim. |
| C31–C33 | Prompt injection, unauthorised tool/recipient, low PII score plus detected identifier | Broker/egress rejects irrespective of model output; safe diagnostics only. |
| C34–C36 | Duplicate-source paraphrases, candidate order/label permutations, genuinely changed evidence | Origin deduplication; mapped invariance where equivalent; sensitivity to relevant changed facts. |
| C37–C39 | Model/rubric/quantisation/ontology change; idempotency replay with changed view; missing run receipt | Invalidate affected calibration/cache or reject; no reuse of stale qualification. |
| C40–C42 | Known good approval replaced by score; schema-valid bad domain record rendered; action marked complete | Existing human/domain/effectiveness boundaries remain intact; no score-created authority. |

Use independently specified synthetic oracles and Hypothesis for boundary combinations; keep meaningful expected errors and do not suppress health checks. Snapshot fixtures and mock transports prove software contracts only. Actual model tests must identify exact input, output, executable tuple, resources, limitations and source rights separately.
