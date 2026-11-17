"""Synthetic, actor-scoped D5 representation lineage and disagreement contract."""

from __future__ import annotations

from copy import deepcopy

import pytest

from tools.evidence_core import canonical_bytes, fingerprint
from tools.faw10_d3_decision_view import generate_receipt as d3_generate_receipt
from tools.faw12_d5_representations import compare_representations
from tools.json_shapes import JsonObject, is_array, require_object


def _case(*, late: bool = True) -> JsonObject:
    receipt = d3_generate_receipt()
    inputs = receipt["inputs"]
    assert is_array(inputs)
    return deepcopy(require_object(inputs[1 if late else 0], context="D3 input"))


def _row(
    identity: str,
    event: str,
    kind: str,
    origin: str,
    value: str | None,
    *,
    status: str = "simulated_annotation",
    key: str = "dose",
) -> JsonObject:
    return {
        "id": identity,
        "event_id": event,
        "comparison_key": key,
        "origin_family_id": origin,
        "representation_kind": kind,
        "status": status,
        "value": value,
    }


def test_native_and_ocr_of_one_source_are_not_independent_witnesses() -> None:
    rows = [
        _row("native", "concern", "native_text", "pdf-source", "3 mg"),
        _row("ocr", "concern", "layout_ocr", "pdf-source", "3 mg"),
    ]
    result = compare_representations(_case(), rows)
    assert result["status"] == "synthetic_contract_only"
    assert result["ocr_executed"] is False
    assert result["model_executed"] is False
    assert result["independence_qualified"] is False
    assert result["clinical_qualification"] == "none"
    assert result["d3_packet_fingerprint"].startswith("sha256:")
    summary = result["comparisons"][0]
    assert summary["comparison_key"] == "dose"
    assert summary["origin_count"] == 1
    assert summary["simulated_representations"] == 2
    assert summary["values"] == ["3 mg"]
    assert summary["representation_disagreement"] is False
    assert summary["declared_agreement_without_qualification"] is False
    assert all(row["evidence"]["verified"] for row in result["representations"])


def test_disagreeing_ocr_and_native_transcriptions_preserve_alternatives() -> None:
    result = compare_representations(
        _case(),
        [
            _row("native", "concern", "native_text", "pdf-source", "3 mg"),
            _row("ocr", "concern", "layout_ocr", "pdf-source", "8 mg"),
        ],
    )
    summary = result["comparisons"][0]
    assert summary["origin_count"] == 1
    assert summary["representation_disagreement"] is True
    assert summary["cross_origin_disagreement"] is False
    assert summary["values"] == ["3 mg", "8 mg"]


def test_distinct_visible_structured_log_is_an_unqualified_declared_second_origin() -> None:
    rows = [
        _row("native", "concern", "native_text", "pdf-original", "3 mg"),
        _row("log", "result", "structured_log", "ehr-original", "3 mg"),
    ]
    outcome = compare_representations(_case(), rows)
    group = outcome["comparisons"][0]
    assert group["origin_count"] == 2
    assert group["representation_disagreement"] is False
    assert group["declared_agreement_without_qualification"] is True
    assert outcome["independence_qualified"] is False
    assert {item["event_id"] for item in outcome["representations"]} == {"concern", "result"}


def test_distinct_origin_conflict_is_not_collapsed_to_consensus() -> None:
    outcome = compare_representations(
        _case(),
        [
            _row("native", "concern", "native_text", "pdf-original", "3 mg"),
            _row("log", "result", "structured_log", "ehr-original", "5 mg"),
        ],
    )
    group = outcome["comparisons"][0]
    assert group["origin_count"] == 2
    assert group["cross_origin_disagreement"] is True
    assert group["declared_agreement_without_qualification"] is False
    assert group["values"] == ["3 mg", "5 mg"]


def test_explicitly_unsupported_ocr_is_not_an_executed_observation() -> None:
    outcome = compare_representations(
        _case(),
        [
            _row("native", "concern", "native_text", "pdf-original", "3 mg"),
            _row(
                "unsupported", "concern", "layout_ocr", "pdf-original", None, status="unsupported"
            ),
        ],
    )
    group = outcome["comparisons"][0]
    assert group["origin_count"] == 1
    assert group["unsupported_representations"] == 1
    assert group["simulated_representations"] == 1
    assert outcome["ocr_executed"] is False


def test_future_event_is_not_admitted_at_earlier_recipient_cutoff() -> None:
    with pytest.raises(ValueError, match="invalid or unauthorized D5 representations") as caught:
        compare_representations(
            _case(late=False),
            [_row("SECRET-FUTURE-EVENT", "result", "structured_log", "ehr", "harm")],
        )
    assert "SECRET-FUTURE-EVENT" not in str(caught.value)


def test_identical_source_hash_cannot_be_declared_two_origin_families() -> None:
    with pytest.raises(ValueError, match="invalid or unauthorized D5 representations"):
        compare_representations(
            _case(),
            [
                _row("native", "concern", "native_text", "real-pdf-family", "3 mg"),
                _row("ocr", "concern", "layout_ocr", "different-fake-origin", "3 mg"),
            ],
        )


@pytest.mark.parametrize(
    "bad",
    [
        _row("native", "concern", "unknown_method", "origin", "3 mg"),
        _row("native", "concern", "layout_ocr", "origin", "3 mg", status="unsupported"),
        _row("native", "concern", "layout_ocr", "origin", None),
        _row("native", "concern", "layout_ocr", "origin", "3 mg", status="claimed_executed"),
        _row("native", "other-case", "native_text", "origin", "3 mg"),
        _row("", "concern", "native_text", "origin", "3 mg"),
    ],
)
def test_invalid_or_unsupported_representation_is_fail_closed(bad: JsonObject) -> None:
    with pytest.raises(ValueError, match="invalid or unauthorized D5 representations"):
        compare_representations(_case(), [bad])


def test_duplicates_and_extra_fields_are_rejected() -> None:
    row = _row("native", "concern", "native_text", "origin", "3 mg")
    with pytest.raises(ValueError, match="invalid or unauthorized D5 representations"):
        compare_representations(_case(), [row, deepcopy(row)])
    extra = deepcopy(row)
    extra["fabricated_source_authority"] = "approved"
    with pytest.raises(ValueError, match="invalid or unauthorized D5 representations"):
        compare_representations(_case(), [extra])


def test_forged_source_fingerprint_rejected_without_echoing_source_material() -> None:
    raw = _case()
    timeline = require_object(raw["timeline"], context="D3 timeline")
    sources = timeline["sources"]
    assert is_array(sources)
    require_object(sources[0], context="source")["fingerprint"] = "sha256:" + "0" * 64
    with pytest.raises(ValueError, match="invalid or unauthorized D5 representations") as caught:
        compare_representations(raw, [_row("native", "concern", "native_text", "source", "3 mg")])
    assert "Family reported" not in str(caught.value)


def test_representation_order_permutation_is_canonical() -> None:
    rows = [
        _row("native", "concern", "native_text", "pdf", "3 mg"),
        _row("ocr", "concern", "layout_ocr", "pdf", "3 mg"),
        _row("log", "result", "structured_log", "ehr", "3 mg"),
    ]
    forward = compare_representations(_case(), rows)
    reverse = compare_representations(_case(), list(reversed(rows)))
    assert canonical_bytes(forward) == canonical_bytes(reverse)
    assert forward["result_fingerprint"] == fingerprint(
        {key: value for key, value in forward.items() if key != "result_fingerprint"}
    )
