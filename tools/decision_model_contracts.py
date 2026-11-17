"""DM02 model-free decision-model companion contracts (not inference or admission).

These opt-in contracts never alter safety-work, the existing runtime registry or
tool/action permissions. JSON Schema is authoritative for wire shapes; the
checked Python boundary enforces relationships that schemas cannot express.
All raw source bytes enter through a trusted broker-owned context, not the wire.
"""

from __future__ import annotations

import json
import math
from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from datetime import date
from hashlib import sha256
from pathlib import Path
from typing import Literal, Protocol, TypeAlias, TypedDict

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

from tools.evidence_core import fingerprint
from tools.evidence_ports import Operation, OperationResult
from tools.json_shapes import JsonObject, is_array, is_object, object_rows, require_object

SCHEMA_PATH = Path(__file__).parents[1] / "conductor/schemas/decision-models-0.1.schema.json"
SCHEMA_VERSION = "decision-models/0.1"
MAX_WIRE_BYTES = 262_144
PROBABILITY_TOLERANCE = 1e-6
DISPOSITIONS = frozenset(
    {"candidate_for_review", "continue_bounded_step", "escalate", "abstain"}
)
RESULT_STATUSES = frozenset(
    {"ok", "abstained", "unsupported", "invalid_input", "invalid_output",
     "timeout", "cancelled", "unavailable", "error"}
)

MessageKind: TypeAlias = Literal["request", "result", "capability"]


class DecisionBinding(TypedDict):
    """Checked wire identity fields, shared by requests and results."""

    request_id: str
    task_id: str
    task_spec_hash: str
    case_id: str
    view_id: str
    view_hash: str
    source_manifest_hash: str
    capability_receipt_hash: str


class DecisionModelPort(Protocol):
    """Proposed opt-in port; no production registration is performed here."""

    def capabilities(self) -> Sequence[JsonObject]: ...

    def evaluate(self, operation: Operation, request: Mapping[str, object]) -> OperationResult: ...


@dataclass(frozen=True, slots=True)
class SourceAnchor:
    """Trusted source attachment. Its bytes must not be sent in wire receipts."""

    anchor_id: str
    source_id: str
    case_id: str
    view_id: str
    source_hash: str
    raw_bytes: bytes
    start_byte: int
    end_byte: int
    permitted: bool = True
    unit: str | None = None
    media_anchor_id: str | None = None
    transform_hash: str | None = None
    page_index: int | None = None


@dataclass(frozen=True, slots=True)
class ContractContext:
    """Broker-validated authority and reference context; never provider-controlled."""

    task_id: str
    task_spec_hash: str
    case_id: str
    view_id: str
    view_hash: str
    view_bytes: bytes
    source_manifest_hash: str
    privacy_mode: str
    data_class: str
    compartment_id: str
    instructions: Mapping[str, str]
    questions: Mapping[str, str]
    anchors: Mapping[str, SourceAnchor]
    policy_hash: str
    ontology_release_hash: str | None = None
    hard_review: bool = False
    source_conflict: bool = False
    privacy_veto: bool = False
    authority_veto: bool = False
    calibration_required: bool = False
    calibrator_hash: str | None = None
    eligible_continue: bool = False
    now_monotonic_ns: int | None = None


def _unique_pairs(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError("duplicate JSON key")
        result[key] = value
    return result


def _reject_constant(value: str) -> object:
    raise ValueError("non-finite JSON constant: " + value)


def _check_finite(value: object) -> None:
    if isinstance(value, float) and not math.isfinite(value):
        raise ValueError("non-finite JSON number")
    if is_object(value):
        for part in value.values():
            _check_finite(part)
    elif is_array(value):
        for part in value:
            _check_finite(part)


def strict_decode(raw: bytes | str, *, max_bytes: int = MAX_WIRE_BYTES) -> JsonObject:
    """Decode one bounded JSON object, rejecting duplicate and non-finite values."""

    payload = raw.encode("utf-8") if isinstance(raw, str) else raw
    if not payload or len(payload) > max_bytes:
        raise ValueError("invalid wire size")
    try:
        decoded: object = json.loads(
            payload, object_pairs_hook=_unique_pairs, parse_constant=_reject_constant
        )
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        raise ValueError("invalid JSON encoding or syntax") from exc
    _check_finite(decoded)
    return require_object(decoded, context="decision-model wire")


def _schema() -> JsonObject:
    parsed: object = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    schema = require_object(parsed, context="decision-model schema")
    Draft202012Validator.check_schema(schema)
    return schema


def schema_for(kind: MessageKind) -> JsonObject:
    """Return a self-contained canonical schema for the selected wire envelope."""

    schema = _schema()
    return {"$schema": schema["$schema"], "$defs": schema["$defs"],
            "$ref": f"#/$defs/{kind}"}


def _schema_errors(value: object, kind: MessageKind) -> list[str]:
    validator = Draft202012Validator(schema_for(kind), format_checker=FormatChecker())
    errors: list[ValidationError] = sorted(
        validator.iter_errors(value), key=lambda error: (tuple(str(p) for p in error.path), error.message)
    )
    return [f"{kind}.schema:{'/'.join(str(p) for p in error.path)}:{error.message}" for error in errors]


def validate_capability(capability: object) -> list[str]:
    """Validate declarative features without inferring measured runtime support."""

    return _schema_errors(capability, "capability")


def registry_compatibility(candidate_state: str) -> str | None:
    """Safe descriptive mapping; never mutate or qualify the shared registry."""

    return {
        "candidate": "interface_contract",
        "contract_tested": "interface_contract",
        "measured_research": "experimental",
        "task_qualified": "experimental",
        "unavailable": "unavailable",
        "withdrawn": "unavailable",
    }.get(candidate_state)


def runtime_route_eligible(capability: object, registry: object) -> bool:
    """A DM02 contract pass is never an executable route or runtime admission."""

    # An actual admission is owned by the runtime/assurance coordinator after
    # independent model measurement. This model-free checkpoint cannot grant it.
    _ = capability, registry
    return False


def _rows(value: object) -> list[JsonObject]:
    return object_rows(value)


def _ids(rows: Sequence[Mapping[str, object]], key: str) -> list[str]:
    return [value for item in rows if isinstance(value := item.get(key), str)]


def _number(value: object) -> float | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    result = float(value)
    return result if math.isfinite(result) else None


def _wire_binding_matches(value: JsonObject, ctx: ContractContext) -> list[str]:
    expected = {
        "task_id": ctx.task_id,
        "task_spec_hash": ctx.task_spec_hash,
        "case_id": ctx.case_id,
        "view_id": ctx.view_id,
        "view_hash": ctx.view_hash,
        "source_manifest_hash": ctx.source_manifest_hash,
    }
    problems = [f"identity.{key}" for key, wanted in expected.items() if value.get(key) != wanted]
    raw_hash = "sha256:" + sha256(ctx.view_bytes).hexdigest()
    if ctx.view_hash != raw_hash:
        problems.append("identity.trusted_view_bytes")
    return problems


def validate_request(
    request: object, context: ContractContext, capability: object
) -> list[str]:
    """Check shape, exact evidence identity, privacy and declared features."""

    errors = _schema_errors(request, "request")
    errors.extend(validate_capability(capability))
    if errors:
        return errors
    req = require_object(request, context="request")
    cap = require_object(capability, context="capability")
    errors.extend(_wire_binding_matches(req, context))
    if req.get("capability_receipt_hash") != fingerprint(cap):
        errors.append("identity.capability_receipt_hash")
    for key, expected in (
        ("privacy_mode", context.privacy_mode),
        ("data_class", context.data_class),
        ("compartment_id", context.compartment_id),
    ):
        if req.get(key) != expected:
            errors.append(f"authority.{key}")
    privacy = require_object(cap["privacy"], context="capability privacy")
    modes = privacy["allowed_modes"]
    classes = privacy["allowed_data_classes"]
    if (not is_array(modes) or context.privacy_mode not in modes
            or not is_array(classes) or context.data_class not in classes):
        errors.append("authority.capability_scope")
    if context.privacy_veto or context.authority_veto:
        errors.append("authority.hard_veto")
    identifiers = req["source_anchor_ids"]
    if is_array(identifiers):
        for anchor_id in identifiers:
            if isinstance(anchor_id, str):
                anchor = context.anchors.get(anchor_id)
                if anchor is None or not anchor.permitted:
                    errors.append("source.unpermitted_anchor")
                elif anchor.case_id != context.case_id or anchor.view_id != context.view_id:
                    errors.append("source.cross_case_or_view")
    questions = _rows(req["questions"])
    ids = _ids(questions, "question_id")
    if len(ids) != len(set(ids)) or set(ids) != set(context.questions):
        errors.append("question.identity_set")
    limits = require_object(cap["limits"], context="limits")
    if len(questions) > int(str(limits["max_questions"])):
        errors.append("capability.question_limit")
    operation = require_object(req["operation"], context="operation")
    timeout = _number(operation["timeout_seconds"])
    maximum_timeout = _number(limits["timeout_seconds"])
    if timeout is None or maximum_timeout is None or timeout > maximum_timeout:
        errors.append("capability.timeout_limit")
    deadline = operation["deadline_monotonic_ns"]
    if (context.now_monotonic_ns is not None and isinstance(deadline, int)
            and deadline <= context.now_monotonic_ns):
        errors.append("operation.deadline_expired")
    combinations = {
        (item["kind"], item["modality"], item["multiple"])
        for item in _rows(cap["supported"])
    }
    for question in questions:
        kind = question["kind"]
        qid = question["question_id"]
        if context.questions.get(str(qid)) != kind:
            errors.append("question.registered_kind")
        iid = question["instruction_id"]
        if context.instructions.get(str(iid)) != question["instruction_hash"]:
            errors.append("question.untrusted_instruction")
        mode = "image" if kind in {"box", "boxes"} else "text"
        mult = question["multiple"] if kind == "choice" else False
        if (kind, mode, mult) not in combinations:
            errors.append("capability.unsupported_primitive")
        if kind == "choice":
            candidates = _rows(question["candidates"])
            ids = _ids(candidates, "candidate_id")
            if len(ids) != len(set(ids)):
                errors.append("choice.duplicate_candidate")
            if len(candidates) > int(str(limits["max_candidates"])):
                errors.append("capability.candidate_limit")
            if question["candidate_set_hash"] != fingerprint(question["candidates"]):
                errors.append("choice.candidate_hash")
            if question.get("ontology_release_hash") != context.ontology_release_hash:
                errors.append("choice.ontology_release")
        if kind == "score":
            levels = _rows(question["ordered_levels"])
            levels_ids = _ids(levels, "level_id")
            order = [int(str(part["severity_order"])) for part in levels]
            if len(set(levels_ids)) != len(levels_ids) or order != sorted(set(order)):
                errors.append("score.level_order")
            severe = question["severe_level_ids"]
            if is_array(severe) and not set(str(x) for x in severe).issubset(levels_ids):
                errors.append("score.severe_membership")
        if kind in {"box", "boxes"} and (
            question["media_anchor_id"] not in context.anchors
            or not context.anchors[str(question["media_anchor_id"])].permitted
        ):
            errors.append("source.unpermitted_media")
    return sorted(set(errors))


def _validate_anchor(
    anchor_id: object, req: JsonObject, ctx: ContractContext, *, expected_text: str | None = None
) -> list[str]:
    if not isinstance(anchor_id, str):
        return ["source.missing_anchor"]
    requested_anchor_ids = req["source_anchor_ids"]
    if not is_array(requested_anchor_ids) or anchor_id not in requested_anchor_ids:
        return ["source.outside_view"]
    anchor = ctx.anchors.get(anchor_id)
    if anchor is None or not anchor.permitted:
        return ["source.unpermitted_anchor"]
    if anchor.case_id != ctx.case_id or anchor.view_id != ctx.view_id:
        return ["source.cross_case_or_view"]
    if anchor.source_hash != "sha256:" + sha256(anchor.raw_bytes).hexdigest():
        return ["source.stale_bytes_hash"]
    if anchor.start_byte < 0 or anchor.start_byte >= anchor.end_byte or anchor.end_byte > len(anchor.raw_bytes):
        return ["source.byte_span_bounds"]
    if expected_text is not None:
        try:
            actual = anchor.raw_bytes[anchor.start_byte:anchor.end_byte].decode("utf-8")
        except UnicodeDecodeError:
            return ["source.partial_utf8"]
        if actual != expected_text:
            return ["source.mismatched_text"]
    return []


def _primitive_errors(
    output: JsonObject, question: JsonObject, req: JsonObject,
    ctx: ContractContext, cap: JsonObject
) -> list[str]:
    kind = question["kind"]
    errors: list[str] = []
    if output["kind"] != kind:
        return ["output.kind"]
    if kind == "choice":
        candidates = _rows(question["candidates"])
        ids = set(_ids(candidates, "candidate_id"))
        values = require_object(output["probabilities"], context="probabilities")
        selected = output["selected_ids"]
        if set(values) != ids or not is_array(selected) or not set(selected).issubset(ids):
            errors.append("choice.candidate_set")
        if output["multiple"] != question["multiple"]:
            errors.append("choice.multiple")
        if question["multiple"] and is_array(selected):
            expected_selected = {key for key, value in values.items() if
                                 _number(value) is not None and float(str(value)) >= 0.5}
            if set(selected) != expected_selected:
                errors.append("choice.multilabel_selection")
        if not question["multiple"]:
            probs = [_number(v) for v in values.values()]
            if any(v is None for v in probs):
                errors.append("probability.invalid")
            elif abs(sum(v for v in probs if v is not None) - 1) > PROBABILITY_TOLERANCE:
                errors.append("choice.exclusive_mass")
            if is_array(selected) and len(selected) > 1:
                errors.append("choice.exclusive_selection")
    if kind == "score":
        levels = _rows(question["ordered_levels"])
        ids = _ids(levels, "level_id")
        values = require_object(output["probabilities"], context="score probabilities")
        if output["ordered_level_ids"] != ids or set(values) != set(ids):
            errors.append("score.level_identity")
        probs = [_number(v) for v in values.values()]
        if any(v is None for v in probs) or abs(sum(v for v in probs if v is not None) - 1) > PROBABILITY_TOLERANCE:
            errors.append("score.probability_mass")
    if kind in {"text", "number", "date", "box", "boxes"}:
        found = _number(output["found"])
        value = output["value"]
        if found is None:
            errors.append("typed.found")
        elif found < 0.5 and (value is not None or output["unit"] is not None
                              or output["source_anchor_id"] is not None):
            errors.append("typed.below_found_boundary")
        if value is not None:
            text = value if kind in {"text", "date"} and isinstance(value, str) else None
            errors.extend(_validate_anchor(output["source_anchor_id"], req, ctx, expected_text=text))
        if kind == "number" and value is not None:
            unit = output["unit"]
            allowed_units = question["allowed_units"]
            if not is_array(allowed_units) or unit not in allowed_units:
                errors.append("number.unit_not_allowed")
            anchor = ctx.anchors.get(str(output["source_anchor_id"]))
            if anchor is None or anchor.unit != unit:
                errors.append("number.unproven_unit")
            v = _number(value)
            for bound in ("minimum", "maximum"):
                b = _number(question.get(bound))
                if v is not None and b is not None and (
                    (bound == "minimum" and v < b) or (bound == "maximum" and v > b)
                ):
                    errors.append("number.bounds")
        if kind == "date" and value is not None and isinstance(value, str):
            if question["precision"] != "day":
                errors.append("date.unadmitted_precision")
            else:
                try:
                    date.fromisoformat(value)
                except ValueError:
                    errors.append("date.invalid_calendar")
        if kind in {"box", "boxes"} and value is not None:
            anchor = ctx.anchors.get(str(output["source_anchor_id"]))
            if (anchor is None or anchor.media_anchor_id != question["media_anchor_id"]
                    or anchor.transform_hash != question["transform_hash"]
                    or anchor.page_index != question["page_index"]):
                errors.append("region.media_transform")
            regions = [value] if kind == "box" else value
            if is_array(regions):
                maximum = question["max_regions"] if kind == "boxes" else 1
                limits = require_object(cap["limits"], context="capability limits")
                if len(regions) > int(str(maximum)) or len(regions) > int(str(limits["max_regions"])):
                    errors.append("region.count_limit")
                seen: set[tuple[float, float, float, float]] = set()
                for region in regions:
                    if not is_object(region):
                        errors.append("region.shape")
                        continue
                    left = _number(region["left"])
                    top = _number(region["top"])
                    right = _number(region["right"])
                    bottom = _number(region["bottom"])
                    if left is None or right is None or top is None or bottom is None:
                        errors.append("region.non_numeric")
                        continue
                    if not left < right or not top < bottom:
                        errors.append("region.inverted")
                    coords = (left, top, right, bottom)
                    if coords in seen:
                        errors.append("region.duplicate")
                    seen.add(coords)
    return errors


def gate_disposition(
    *, hard_review: bool = False, source_conflict: bool = False,
    privacy_veto: bool = False, authority_veto: bool = False,
    all_required_valid: bool = True, calibrated: bool = True,
    uncertain: bool = False, eligible_continue: bool = False
) -> Literal["abstain", "escalate", "candidate_for_review", "continue_bounded_step"]:
    """Deterministic, model-independent recommendation; never an approval."""

    if privacy_veto or authority_veto:
        return "abstain"
    if hard_review or source_conflict:
        return "escalate"
    if not all_required_valid or not calibrated or uncertain:
        return "abstain"
    return "continue_bounded_step" if eligible_continue else "candidate_for_review"


def validate_result(
    result: object, request: object, context: ContractContext, capability: object
) -> list[str]:
    """Validate exact response binding, primitive semantics and fail-closed policy."""

    errors = _schema_errors(result, "result")
    errors.extend(validate_request(request, context, capability))
    if errors:
        return errors
    res = require_object(result, context="result")
    req = require_object(request, context="request")
    cap = require_object(capability, context="capability")
    for key in (
        "request_id", "task_id", "task_spec_hash", "case_id", "view_id",
        "view_hash", "source_manifest_hash", "capability_receipt_hash",
    ):
        if res.get(key) != req.get(key):
            errors.append(f"result.identity.{key}")
    questions = {str(q["question_id"]): q for q in _rows(req["questions"])}
    answers = _rows(res["answers"])
    ids = _ids(answers, "question_id")
    if len(ids) != len(set(ids)) or set(ids) != set(questions):
        errors.append("result.answer_set")
    for answer in answers:
        question = questions.get(str(answer["question_id"]))
        if question is None:
            continue
        if answer["kind"] != question["kind"]:
            errors.append("result.answer_kind")
            continue
        if answer["status"] == "ok":
            output = require_object(answer["output"], context="answer output")
            errors.extend(_primitive_errors(output, question, req, context, cap))
        calibration = require_object(answer["calibration"], context="calibration")
        calibrated = calibration["calibrated_probabilities"]
        calibrator_hash = calibration["calibrator_hash"]
        if (calibrated is None) != (calibrator_hash is None):
            errors.append("calibration.partial_binding")
        if calibrator_hash is not None and calibrator_hash != context.calibrator_hash:
            errors.append("calibration.stale_binding")
        if calibrated is not None:
            values = require_object(calibrated, context="calibrated probabilities")
            if question["kind"] == "noul" and set(values) != {"yes"}:
                errors.append("calibration.noul_keys")
            if question["kind"] in {"choice", "score"}:
                ids_for_prob = (
                    _ids(_rows(question["candidates"]), "candidate_id")
                    if question["kind"] == "choice" else
                    _ids(_rows(question["ordered_levels"]), "level_id")
                )
                if set(values) != set(ids_for_prob):
                    errors.append("calibration.class_keys")
    if res["status"] == "ok" and any(a["status"] != "ok" for a in answers):
        errors.append("result.partial_success")
    if res["status"] != "ok" and all(a["status"] == "ok" for a in answers):
        errors.append("result.false_failure")
    policy = require_object(res["policy"], context="result policy")
    if policy["policy_hash"] != context.policy_hash:
        errors.append("policy.identity")
    calibrated_ok = not context.calibration_required or all(
        is_object(calibration_value := a.get("calibration"))
        and calibration_value.get("calibrator_hash") == context.calibrator_hash
        for a in answers
    )
    expected_disposition = gate_disposition(
        hard_review=context.hard_review,
        source_conflict=context.source_conflict,
        privacy_veto=context.privacy_veto,
        authority_veto=context.authority_veto,
        all_required_valid=not errors and res["status"] == "ok",
        calibrated=calibrated_ok,
        eligible_continue=context.eligible_continue,
    )
    if policy["disposition"] != expected_disposition:
        errors.append("policy.disposition_override")
    return sorted(set(errors))


def idempotency_identity(request: object) -> str:
    """Cache identity includes all immutable request bindings, not only the key."""

    errors = _schema_errors(request, "request")
    if errors:
        raise ValueError("invalid request for idempotency binding")
    value = require_object(request, context="request")
    operation = require_object(value["operation"], context="operation")
    return fingerprint({
        "key": operation["idempotency_key"],
        "request_id": value["request_id"],
        "task": value["task_spec_hash"],
        "case": value["case_id"],
        "view": value["view_hash"],
        "sources": value["source_manifest_hash"],
        "privacy_mode": value["privacy_mode"],
        "data_class": value["data_class"],
        "compartment_id": value["compartment_id"],
        "capability": value["capability_receipt_hash"],
        "questions": value["questions"],
    })


def severe_tail_probability(output: object, question: object) -> float:
    """Calculate a research diagnostic without changing provider-native scores."""

    if not is_object(output) or not is_object(question) or output.get("kind") != "score":
        raise ValueError("score output and question are required")
    values = output.get("probabilities")
    severe = question.get("severe_level_ids")
    if not is_object(values) or not is_array(severe):
        raise ValueError("incomplete score probability binding")
    total = 0.0
    for level in severe:
        if not isinstance(level, str) or level not in values:
            raise ValueError("unknown severe level")
        value = _number(values[level])
        if value is None or not 0 <= value <= 1:
            raise ValueError("invalid severe probability")
        total += value
    return total
