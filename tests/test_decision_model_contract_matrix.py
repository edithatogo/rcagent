"""Independent DM02 model-free envelope and invariant controls.

Each C01–C42 scenario uses newly authored synthetic data. Success demonstrates
software-contract checks only; no model, patient case or clinical authority.
"""

from __future__ import annotations

from copy import deepcopy
from dataclasses import replace
from hashlib import sha256
from typing import Callable

import pytest
from hypothesis import given, strategies as st
from jsonschema import Draft202012Validator

from tools import decision_model_contracts as dm
from tools.evidence_core import fingerprint
from tools.json_shapes import JsonObject, is_array, require_object


def _hash_bytes(value: bytes) -> str:
    return "sha256:" + sha256(value).hexdigest()


def _array(value: object) -> list[object]:
    assert is_array(value)
    return value


def _obj(value: object) -> JsonObject:
    return require_object(value, context="synthetic test fixture")


def _question(request: JsonObject) -> JsonObject:
    return _obj(_array(request["questions"])[0])


def _answer(result: JsonObject) -> JsonObject:
    return _obj(_array(result["answers"])[0])


def _payload(result: JsonObject) -> JsonObject:
    return _obj(_answer(result)["output"])


def _capability() -> JsonObject:
    return {
        "message_type": "capability",
        "schema_version": dm.SCHEMA_VERSION,
        "provider_id": "fixture-provider", "model_id": "fixture-no-model",
        "model_revision": "source-revision", "weight_hash": None,
        "tokenizer_hash": None, "runtime_id": "fixture-not-installed",
        "runtime_revision": "source-build", "precision": "fp32",
        "device_profile_hash": None, "candidate_state": "contract_tested",
        "supported": [
            {"kind": kind, "modality": "image" if kind in {"box", "boxes"} else "text",
             "multiple": multiple}
            for kind in ("noul", "choice", "score", "text", "number", "date", "box", "boxes")
            for multiple in ((False, True) if kind == "choice" else (False,))
        ],
        "limits": {
            "max_questions": 8, "max_candidates": 8, "max_regions": 4,
            "max_payload_bytes": 262144, "timeout_seconds": 120,
        },
        "privacy": {
            "allowed_modes": ["fully_local"], "allowed_data_classes": ["synthetic"],
            "remote_code": False, "external_inference": False, "telemetry": "disabled",
        },
        "measurement_receipt_hash": None,
    }


def _sample() -> tuple[JsonObject, JsonObject, JsonObject, dm.ContractContext]:
    raw = "Report é date 2026-11-17 volume 5 mg".encode()
    start = raw.index("é".encode())
    anchor = dm.SourceAnchor(
        anchor_id="anchor-1", source_id="source-1", case_id="case-1",
        view_id="view-1", source_hash=_hash_bytes(raw), raw_bytes=raw,
        start_byte=start, end_byte=start + len("é".encode()),
    )
    context = dm.ContractContext(
        task_id="synthetic-task", task_spec_hash=_hash_bytes(b"task"),
        case_id="case-1", view_id="view-1", view_hash=_hash_bytes(raw),
        view_bytes=raw, source_manifest_hash=_hash_bytes(b"manifest"),
        privacy_mode="fully_local", data_class="synthetic",
        compartment_id="fixture-only",
        instructions={"noul-rubric": _hash_bytes(b"instruction")},
        questions={"q-severe": "noul"}, anchors={"anchor-1": anchor},
        policy_hash=_hash_bytes(b"policy"),
    )
    capability = _capability()
    request: JsonObject = {
        "message_type": "request", "schema_version": dm.SCHEMA_VERSION,
        "request_id": "request-1", "task_id": context.task_id,
        "task_spec_hash": context.task_spec_hash, "case_id": context.case_id,
        "view_id": context.view_id, "view_hash": context.view_hash,
        "source_manifest_hash": context.source_manifest_hash,
        "capability_receipt_hash": fingerprint(capability),
        "privacy_mode": context.privacy_mode, "data_class": context.data_class,
        "compartment_id": context.compartment_id, "source_anchor_ids": ["anchor-1"],
        "questions": [{
            "kind": "noul", "question_id": "q-severe",
            "instruction_id": "noul-rubric",
            "instruction_hash": context.instructions["noul-rubric"],
        }],
        "operation": {
            "operation_id": "synthetic-evaluate", "idempotency_key": "key-1",
            "timeout_seconds": 30, "deadline_monotonic_ns": 9_999_999_999,
        },
    }
    result: JsonObject = {
        "message_type": "result", "schema_version": dm.SCHEMA_VERSION,
        **{name: request[name] for name in (
            "request_id", "task_id", "task_spec_hash", "case_id", "view_id",
            "view_hash", "source_manifest_hash", "capability_receipt_hash",
        )},
        "status": "ok", "authority_label": "advisory_candidate",
        "answers": [{
            "question_id": "q-severe", "kind": "noul", "status": "ok",
            "output": {"kind": "noul", "p_yes": 0.25},
            "native": {"raw_response_hash": None, "semantics": "mock-binary"},
            "calibration": {"calibrator_hash": None, "calibrated_probabilities": None},
        }],
        "usage": {"elapsed_ms": None, "retries": 0, "input_tokens": None, "output_tokens": None},
        "policy": {"policy_hash": context.policy_hash,
                   "disposition": "candidate_for_review", "reasons": []},
    }
    return request, result, capability, context


def _set_question(
    request: JsonObject, result: JsonObject, context: dm.ContractContext,
    question: JsonObject, output: JsonObject
) -> dm.ContractContext:
    request["questions"] = [question]
    answer = _answer(result)
    answer["question_id"] = question["question_id"]
    answer["kind"] = question["kind"]
    answer["output"] = output
    return replace(context, questions={str(question["question_id"]): str(question["kind"])})


def _common_question(context: dm.ContractContext, kind: str) -> JsonObject:
    return {
        "kind": kind, "question_id": "q-other", "instruction_id": "noul-rubric",
        "instruction_hash": context.instructions["noul-rubric"],
    }


def _choice(request: JsonObject, result: JsonObject, context: dm.ContractContext,
            *, multiple: bool = False) -> dm.ContractContext:
    candidates: list[JsonObject] = [
        {"candidate_id": "alpha", "description": "Synthetic A"},
        {"candidate_id": "beta", "description": "Synthetic B"},
    ]
    question = {
        **_common_question(context, "choice"), "multiple": multiple,
        "candidates": candidates, "candidate_set_hash": fingerprint(candidates),
        "ontology_release_hash": None,
    }
    output: JsonObject = {
        "kind": "choice", "multiple": multiple,
        "probabilities": {"alpha": 0.6, "beta": 0.4},
        "selected_ids": ["alpha"], "nil_reason": None,
    }
    return _set_question(request, result, context, question, output)


def _score(request: JsonObject, result: JsonObject,
           context: dm.ContractContext) -> dm.ContractContext:
    return _set_question(request, result, context, {
        **_common_question(context, "score"), "rubric_id": "synthetic-rubric",
        "rubric_hash": _hash_bytes(b"ordinal-rubric"),
        "ordered_levels": [
            {"level_id": "high", "description": "Synthetic severe", "severity_order": 0},
            {"level_id": "low", "description": "Synthetic non-severe", "severity_order": 1},
        ],
        "severe_level_ids": ["high"],
    }, {
        "kind": "score", "ordered_level_ids": ["high", "low"],
        "probabilities": {"high": 0.3, "low": 0.7},
        "native_summary": "low", "native_semantics": "category",
    })


def _typed(request: JsonObject, result: JsonObject,
           context: dm.ContractContext, kind: str = "text") -> dm.ContractContext:
    question = {**_common_question(context, kind), "field_spec_id": "synthetic-field"}
    output: JsonObject = {
        "kind": kind, "found": 0.5, "value": "é",
        "unit": None, "source_anchor_id": "anchor-1", "missing_reason": None,
    }
    if kind == "number":
        question["allowed_units"] = ["mg"]
        output["value"] = 5
        output["unit"] = "mg"
    if kind == "date":
        question["precision"] = "day"
        output["value"] = "2026-11-17"
    if kind in {"box", "boxes"}:
        question.update({
            "media_anchor_id": "image-1",
            "transform_hash": _hash_bytes(b"transform"), "page_index": 0,
        })
        region = {"left": 0.1, "top": 0.2, "right": 0.8, "bottom": 0.9}
        output.update({
            "media_anchor_id": "image-1",
            "transform_hash": _hash_bytes(b"transform"), "page_index": 0,
            "value": [region] if kind == "boxes" else region,
        })
        if kind == "boxes":
            question["max_regions"] = 2
    return _set_question(request, result, context, question, output)


def _replace_anchor(ctx: dm.ContractContext, *, target: str | None = None,
                    permitted: bool = True, case_id: str = "case-1",
                    unit: str | None = None,
                    media: bool = False) -> dm.ContractContext:
    original = ctx.anchors["anchor-1"]
    start = original.raw_bytes.index(target.encode()) if target is not None else original.start_byte
    end = start + len(target.encode()) if target is not None else original.end_byte
    return replace(ctx, anchors={"anchor-1": replace(
        original, start_byte=start, end_byte=end, permitted=permitted,
        case_id=case_id, unit=unit,
        media_anchor_id="image-1" if media else None,
        transform_hash=_hash_bytes(b"transform") if media else None,
        page_index=0 if media else None,
    )})


def _validate(req: JsonObject, res: JsonObject, cap: JsonObject,
              ctx: dm.ContractContext, *, request_only: bool = False) -> list[str]:
    return (dm.validate_request(req, ctx, cap) if request_only
            else dm.validate_result(res, req, ctx, cap))


def test_canonical_json_schema_has_complete_dialect_and_parses_all_three_envelopes() -> None:
    req, res, cap, ctx = _sample()
    for kind, value in (("request", req), ("result", res), ("capability", cap)):
        schema = dm.schema_for(kind)
        Draft202012Validator.check_schema(schema)
        assert list(Draft202012Validator(schema).iter_errors(value)) == []
    assert dm.validate_request(req, ctx, cap) == []
    assert dm.validate_result(res, req, ctx, cap) == []


@pytest.mark.parametrize("wire", [
    '{"a":1,"a":2}', '{"p":NaN}', '{"p":Infinity}',
    '{"p":-Infinity}', '{"p":1e999}',
])
def test_c01_to_c03_strict_json_rejects_duplicates_and_non_finite(wire: str) -> None:
    with pytest.raises(ValueError, match="duplicate|non-finite"):
        dm.strict_decode(wire)


@pytest.mark.parametrize("invalid", [-0.01, 1.01, True, "0.2", float("inf")])
def test_c01_to_c03_noul_probabilities_are_finite_numeric(invalid: object) -> None:
    req, res, cap, ctx = _sample()
    _payload(res)["p_yes"] = invalid
    assert _validate(req, res, cap, ctx)


@pytest.mark.parametrize(("variant", "expected"), [
    ("mass", "choice.exclusive_mass"),
    ("missing", "choice.candidate_set"),
    ("invented", "choice.candidate_set"),
    ("multi_selected", "choice.exclusive_selection"),
    ("candidate_hash", "choice.candidate_hash"),
    ("ontology", "choice.ontology_release"),
])
def test_c04_to_c08_exclusive_choice_and_candidate_provenance(
    variant: str, expected: str
) -> None:
    req, res, cap, ctx = _sample()
    ctx = _choice(req, res, ctx)
    output = _payload(res)
    question = _question(req)
    probs = _obj(output["probabilities"])
    if variant == "mass":
        probs["alpha"] = 0.7
    elif variant == "missing":
        probs.pop("beta")
    elif variant == "invented":
        _array(output["selected_ids"]).append("outside-supplied-candidates")
    elif variant == "multi_selected":
        _array(output["selected_ids"]).append("beta")
    elif variant == "candidate_hash":
        _obj(_array(question["candidates"])[0])["description"] = "mutated"
    else:
        question["ontology_release_hash"] = _hash_bytes(b"different")
    assert any(expected in x for x in _validate(req, res, cap, ctx))


def test_c06_multilabel_choice_keeps_independent_non_normalized_probabilities() -> None:
    req, res, cap, ctx = _sample()
    ctx = _choice(req, res, ctx, multiple=True)
    output = _payload(res)
    _obj(output["probabilities"]).update({"alpha": 0.9, "beta": 0.9})
    output["selected_ids"] = ["alpha", "beta"]
    assert _validate(req, res, cap, ctx) == []
    assert output["probabilities"] == {"alpha": 0.9, "beta": 0.9}


def test_c09_to_c10_score_preserves_provider_semantics_and_rubric_order() -> None:
    req, res, cap, ctx = _sample()
    ctx = _score(req, res, ctx)
    output = _payload(res)
    assert dm.severe_tail_probability(output, _question(req)) == pytest.approx(0.3)
    assert _validate(req, res, cap, ctx) == []
    output["native_semantics"] = "weighted_position"
    output["native_summary"] = 0.7
    assert _validate(req, res, cap, ctx) == []
    _array(_question(req)["ordered_levels"]).reverse()
    assert any("score.level_order" in e for e in _validate(req, res, cap, ctx))


@pytest.mark.parametrize("found", [0.499999, 0.5, 0.500001])
def test_c11_to_c13_found_boundary_is_inclusive_at_half(found: float) -> None:
    req, res, cap, ctx = _sample()
    ctx = _typed(req, res, ctx)
    payload = _payload(res)
    payload["found"] = found
    if found < 0.5:
        payload.update({"value": None, "unit": None,
                        "source_anchor_id": None, "missing_reason": "not_found"})
    assert _validate(req, res, cap, ctx) == []


def test_c13_conflicting_non_null_below_found_boundary_rejects() -> None:
    req, res, cap, ctx = _sample()
    ctx = _typed(req, res, ctx)
    _payload(res)["found"] = 0.499999
    assert _validate(req, res, cap, ctx)


@pytest.mark.parametrize(("variant", "error"), [
    ("span", "source.mismatched_text"),
    ("cross-case", "source.cross_case_or_view"),
    ("stale", "source.stale_bytes_hash"),
    ("cutoff", "source.unpermitted_anchor"),
])
def test_c14_to_c16_exact_utf8_source_anchors(
    variant: str, error: str
) -> None:
    req, res, cap, ctx = _sample()
    ctx = _typed(req, res, ctx)
    if variant == "span":
        ctx = _replace_anchor(ctx, target="date")
    elif variant == "cross-case":
        ctx = _replace_anchor(ctx, case_id="case-2")
    elif variant == "cutoff":
        ctx = _replace_anchor(ctx, permitted=False)
    else:
        bad = replace(ctx.anchors["anchor-1"], source_hash=_hash_bytes(b"stale"))
        ctx = replace(ctx, anchors={"anchor-1": bad})
    assert any(error in e for e in _validate(req, res, cap, ctx))


def test_c17_to_c19_dates_require_calendar_precision_and_original_source() -> None:
    req, res, cap, ctx = _sample()
    ctx = _typed(req, res, ctx, "date")
    ctx = _replace_anchor(ctx, target="2026-11-17")
    assert _validate(req, res, cap, ctx) == []
    _payload(res)["value"] = "2026-02-30"
    assert _validate(req, res, cap, ctx)
    _payload(res).update({"value": None, "source_anchor_id": None,
                          "missing_reason": "ambiguous_missing_year"})
    assert _validate(req, res, cap, ctx) == []
    _question(req)["precision"] = "unknown"
    _payload(res).update({"value": "2026-11-17", "source_anchor_id": "anchor-1",
                          "missing_reason": None})
    assert any("date.unadmitted_precision" in e for e in _validate(req, res, cap, ctx))


def test_c19_numbers_never_guess_or_convert_units() -> None:
    req, res, cap, ctx = _sample()
    ctx = _typed(req, res, ctx, "number")
    ctx = _replace_anchor(ctx, target="5", unit="mg")
    assert _validate(req, res, cap, ctx) == []
    _payload(res)["unit"] = "mmol"
    assert any("number.unit_not_allowed" in e for e in _validate(req, res, cap, ctx))


@pytest.mark.parametrize(("variant", "error"), [
    ("inverted", "region.inverted"),
    ("page", "region.media_transform"),
    ("transform", "region.media_transform"),
    ("count", "region.count_limit"),
])
def test_c20_to_c21_boxes_reject_bad_geometry_and_provenance(
    variant: str, error: str
) -> None:
    req, res, cap, ctx = _sample()
    ctx = _typed(req, res, ctx, "boxes")
    ctx = _replace_anchor(ctx, media=True)
    payload = _payload(res)
    if variant == "inverted":
        _obj(_array(payload["value"])[0])["right"] = 0.0
    elif variant == "page":
        payload["page_index"] = 1
    elif variant == "transform":
        payload["transform_hash"] = _hash_bytes(b"wrong")
    else:
        payload["value"] = [
            {"left": float(i) / 10, "top": 0.0,
             "right": float(i + 1) / 10, "bottom": 0.5} for i in range(3)
        ]
    assert any(error in e for e in _validate(req, res, cap, ctx))


def test_c22_to_c24_timeout_cancel_unavailable_and_missing_calibration_abstain() -> None:
    for status in ("timeout", "cancelled", "unavailable"):
        req, res, cap, ctx = _sample()
        res["status"] = status
        _answer(res).update({"status": status, "output": None})
        _obj(res["policy"])["disposition"] = "abstain"
        assert _validate(req, res, cap, ctx) == []
    req, res, cap, ctx = _sample()
    ctx = replace(ctx, calibration_required=True,
                  calibrator_hash=_hash_bytes(b"fitted-calibrator"))
    _obj(res["policy"])["disposition"] = "abstain"
    assert _validate(req, res, cap, ctx) == []


def test_c25_to_c27_undeclared_capability_and_remote_code_never_become_supported() -> None:
    req, res, cap, ctx = _sample()
    ctx = _typed(req, res, ctx, "text")
    cap["supported"] = [{"kind": "noul", "modality": "text", "multiple": False}]
    req["capability_receipt_hash"] = fingerprint(cap)
    res["capability_receipt_hash"] = req["capability_receipt_hash"]
    assert any("capability.unsupported_primitive" in e for e in _validate(
        req, res, cap, ctx, request_only=True
    ))
    _obj(cap["privacy"])["remote_code"] = True
    assert dm.validate_capability(cap)
    assert dm.runtime_route_eligible(cap, {"models": []}) is False


@pytest.mark.parametrize(("variant", "disposition"), [
    ("hard-review", "escalate"), ("source-conflict", "escalate"),
    ("privacy", "abstain"), ("authority", "abstain"),
])
def test_c28_to_c33_deterministic_hard_vetoes_ignore_high_model_confidence(
    variant: str, disposition: str
) -> None:
    req, res, cap, ctx = _sample()
    _payload(res)["p_yes"] = 0.0001
    if variant == "hard-review":
        ctx = replace(ctx, hard_review=True)
    elif variant == "source-conflict":
        ctx = replace(ctx, source_conflict=True)
    elif variant == "privacy":
        ctx = replace(ctx, privacy_veto=True)
    else:
        ctx = replace(ctx, authority_veto=True)
    _obj(res["policy"])["disposition"] = disposition
    if variant in {"privacy", "authority"}:
        assert any("authority.hard_veto" in e for e in _validate(req, res, cap, ctx))
    else:
        assert _validate(req, res, cap, ctx) == []
    _obj(res["policy"])["disposition"] = "continue_bounded_step"
    assert any("policy.disposition_override" in e for e in _validate(req, res, cap, ctx))


def test_c31_untrusted_text_cannot_override_instruction_or_add_tools() -> None:
    req, res, cap, ctx = _sample()
    _question(req)["instruction_hash"] = _hash_bytes(b"injected instruction")
    assert any("question.untrusted_instruction" in e for e in _validate(
        req, res, cap, ctx, request_only=True
    ))
    req, res, cap, ctx = _sample()
    req["tool_recipient"] = "external-webhook"
    assert _validate(req, res, cap, ctx, request_only=True)


def test_c34_to_c36_lineage_deduplication_hash_and_view_changes_fail_closed() -> None:
    req, res, cap, ctx = _sample()
    _array(req["source_anchor_ids"]).append("anchor-1")
    assert dm.validate_request(req, ctx, cap)
    req, res, cap, ctx = _sample()
    old = dm.idempotency_identity(req)
    req["view_hash"] = _hash_bytes(b"changed-view")
    assert dm.idempotency_identity(req) != old
    assert any("identity.view_hash" in e for e in dm.validate_request(req, ctx, cap))


def test_c37_to_c39_runtime_and_rubric_drift_invalidates_identity() -> None:
    req, res, cap, ctx = _sample()
    cap["precision"] = "int8"
    assert any("identity.capability_receipt_hash" in e for e in dm.validate_request(
        req, ctx, cap
    ))
    req, res, cap, ctx = _sample()
    ctx = _score(req, res, ctx)
    old = dm.idempotency_identity(req)
    _question(req)["rubric_hash"] = _hash_bytes(b"changed-rubric")
    assert dm.idempotency_identity(req) != old
    assert dm.runtime_route_eligible(cap, {"models": []}) is False


def test_c40_to_c42_score_cannot_sign_approval_render_or_complete_action() -> None:
    req, res, cap, ctx = _sample()
    _obj(res["policy"])["disposition"] = "approved"
    assert _validate(req, res, cap, ctx)
    req, res, cap, ctx = _sample()
    res["action_completed"] = True
    assert _validate(req, res, cap, ctx)
    req, res, cap, ctx = _sample()
    res["domain_validated"] = True
    assert _validate(req, res, cap, ctx)


@pytest.mark.parametrize("state", [
    "candidate", "contract_tested", "measured_research",
    "task_qualified", "unavailable", "withdrawn",
])
def test_registry_mapping_is_descriptive_and_never_promotes(state: str) -> None:
    expected = dm.registry_compatibility(state)
    assert expected in {"interface_contract", "experimental", "unavailable"}
    assert dm.runtime_route_eligible(_capability(), {"models": []}) is False


@given(p=st.floats(allow_nan=False, allow_infinity=False, width=64))
def test_property_noul_probability_is_finite_bounded_without_coercion(p: float) -> None:
    req, res, cap, ctx = _sample()
    _payload(res)["p_yes"] = p
    errors = dm.validate_result(res, req, ctx, cap)
    assert (not errors) == (0 <= p <= 1)


@given(
    left=st.floats(min_value=0, max_value=1, allow_nan=False),
    right=st.floats(min_value=0, max_value=1, allow_nan=False),
)
def test_property_regions_require_strict_nonzero_width(left: float, right: float) -> None:
    req, res, cap, ctx = _sample()
    ctx = _typed(req, res, ctx, "box")
    ctx = _replace_anchor(ctx, media=True)
    box = _obj(_payload(res)["value"])
    box["left"] = left
    box["right"] = right
    errors = dm.validate_result(res, req, ctx, cap)
    assert (not errors) == (left < right)


def test_wire_parser_bounds_and_no_untrusted_scalar() -> None:
    with pytest.raises(ValueError, match="size"):
        dm.strict_decode(b"x" * (dm.MAX_WIRE_BYTES + 1))
    with pytest.raises(ValueError, match="object"):
        dm.strict_decode("[]")
    assert dm.strict_decode('{"safe":"synthetic"}') == {"safe": "synthetic"}
