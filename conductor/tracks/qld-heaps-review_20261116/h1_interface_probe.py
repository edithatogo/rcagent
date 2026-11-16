"""Observe existing HEAPS consumer boundaries with public synthetic controls.

This is an H1 diagnostic, not a HEAPS implementation or an acceptance oracle for
H3-H5. Exit 2 reports unmet safety expectations; it does not turn known unsafe
acceptance into a passing test. Run from the locked repository environment.
"""

from __future__ import annotations

import hashlib
import importlib.metadata
import json
import platform
from copy import deepcopy
from pathlib import Path

from jsonschema import FormatChecker

from tools.evidence_core import canonical_round_trip, fingerprint, validate_record
from tools.interface_actions import canonical_hash, render_view, validate_approval
from tools.json_shapes import JsonObject, object_rows, require_object

ROOT = Path(__file__).resolve().parents[3]
FIXTURE = "tests/fixtures/safety-work/valid-case.json"
COMPONENTS = (
    "tools/evidence_core.py",
    "tools/interface_actions.py",
    "tools/json_shapes.py",
    "tools/jurisdiction_pack.py",
    "tools/template_admission.py",
    "conductor/schemas/safety-work.schema.json",
    "conductor/jurisdictions/registry.json",
    "pyproject.toml",
    "uv.lock",
    FIXTURE,
)


def first_row(record: JsonObject, collection: str) -> JsonObject:
    """Resolve the known synthetic fixture row without inventing a replacement."""
    rows = object_rows(record.get(collection))
    if not rows:
        raise ValueError(f"synthetic fixture has no {collection} row")
    return rows[0]


def observe(
    identifier: str,
    record: JsonObject,
    *,
    should_validate: bool,
    should_render: bool,
    supplied_hash: str | None = None,
    data_class: str = "generated_synthetic",
) -> JsonObject:
    """Compare actual admission against explicit safety expectations."""
    errors = validate_record(record)
    core_admitted = not errors
    context: JsonObject = {
        "citations": [],
        "model_involvement": {"used": False},
        "limitations": ["synthetic H1 interface diagnostic only"],
        "approval_receipt_ids": [],
        "outstanding_review_ids": [],
    }
    render_record: JsonObject = {
        **record,
        "source_sha256": canonical_hash(record) if supplied_hash is None else supplied_hash,
    }
    render_error: str | None = None
    rendered: JsonObject | None = None
    try:
        rendered = render_view(
            render_record,
            audience="auditor",
            data_class=data_class,
            view_context=context,
        )
    except ValueError as exc:
        render_error = str(exc)
    render_admitted = rendered is not None
    return {
        "case_id": identifier,
        "expected_core_admission": should_validate,
        "observed_core_admission": core_admitted,
        "core_errors": errors,
        "expected_render_admission": should_render,
        "observed_render_admission": render_admitted,
        "render_error": render_error,
        "expectations_met": core_admitted == should_validate and render_admitted == should_render,
    }


def run() -> JsonObject:
    """Collect record and approval controls with actual component identities."""
    loaded: object = json.loads((ROOT / FIXTURE).read_text(encoding="utf-8"))
    original = require_object(loaded, context="synthetic fixture")
    valid = canonical_round_trip(original)
    cases = [observe("valid_ascii", valid, should_validate=True, should_render=True)]

    unicode_record = deepcopy(valid)
    first_row(unicode_record, "statements")["text"] = "[Synthetic note: µ / café]"
    unicode_record = canonical_round_trip(unicode_record)
    core_digest = fingerprint(unicode_record)
    interface_digest = canonical_hash(unicode_record)
    independent_utf8 = hashlib.sha256(
        json.dumps(
            unicode_record, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode("utf-8")
    ).hexdigest()
    independent_escaped = hashlib.sha256(
        json.dumps(unicode_record, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode(
            "utf-8"
        )
    ).hexdigest()
    hash_controls_match = (
        core_digest == f"sha256:{independent_utf8}"
        and interface_digest == independent_escaped
        and independent_utf8 != independent_escaped
    )
    cases.append(observe("valid_unicode", unicode_record, should_validate=True, should_render=True))

    unknown_source = deepcopy(valid)
    first_row(unknown_source, "evidence")["source_id"] = "source-missing-synthetic"
    cases.append(
        observe("unknown_source", unknown_source, should_validate=False, should_render=False)
    )

    duplicate = deepcopy(valid)
    sources = object_rows(duplicate.get("sources"))
    if not sources:
        raise ValueError("synthetic fixture requires a source row")
    duplicate["sources"] = [*sources, deepcopy(sources[0])]
    cases.append(
        observe("duplicate_identifier", duplicate, should_validate=False, should_render=False)
    )

    transition = deepcopy(valid)
    first_row(transition, "events")["from_state"] = "intake"
    cases.append(
        observe("invalid_transition", transition, should_validate=False, should_render=False)
    )

    timestamp = deepcopy(valid)
    first_row(timestamp, "sources")["acquired_at"] = "not-a-time"
    cases.append(
        observe("invalid_timestamp", timestamp, should_validate=False, should_render=False)
    )

    cases.append(
        observe(
            "unicode_wrong_hash_domain",
            unicode_record,
            should_validate=True,
            should_render=False,
            supplied_hash=core_digest.removeprefix("sha256:"),
        )
    )
    cases.append(
        observe(
            "non_synthetic_render",
            valid,
            should_validate=True,
            should_render=False,
            data_class="real_clinical",
        )
    )

    profile_in_core = deepcopy(valid)
    profile_in_core["heaps_profile"] = "synthetic-profile"
    cases.append(
        observe(
            "unknown_profile_field", profile_in_core, should_validate=False, should_render=False
        )
    )

    stale_hash = canonical_hash(valid)
    changed = deepcopy(valid)
    first_row(changed, "statements")["text"] = "[Changed synthetic note]"
    cases.append(
        observe(
            "stale_render_hash",
            changed,
            should_validate=True,
            should_render=False,
            supplied_hash=stale_hash,
        )
    )

    approval: JsonObject = {
        "artefact_sha256": "a" * 64,
        "scope": "communication",
        "authority_class": "human_organisational",
        "decision": "approved",
        "actor_class": "accountable_human",
        "actor_role_id": "syn-reviewer",
        "author_role_id": "syn-author",
        "conflict_declared": True,
        "issued_at": "2026-11-16T00:00:00Z",
        "expires_at": "2026-11-17T00:00:00Z",
    }
    unknown_scope: JsonObject = {**approval, "scope": "heaps_packet"}
    approval_variants: tuple[tuple[str, JsonObject, str, list[str]], ...] = (
        ("communication_declaration", approval, "a" * 64, []),
        (
            "wrong_approval_artefact",
            approval,
            "b" * 64,
            ["approval is not bound to the exact artefact"],
        ),
        ("unsupported_packet_scope", unknown_scope, "a" * 64, ["scope is invalid"]),
    )
    approval_cases: list[JsonObject] = []
    for identifier, declaration, expected_hash, expected_errors in approval_variants:
        errors = validate_approval(
            declaration,
            artefact_sha256=expected_hash,
            evaluated_at="2026-11-16T12:00:00Z",
        )
        approval_cases.append(
            {
                "case_id": identifier,
                "expected_errors": expected_errors,
                "observed_errors": errors,
                "expectations_met": errors == expected_errors,
                "real_authority_established": False,
            }
        )

    total = len(cases) + len(approval_cases)
    unmet = sum(case["expectations_met"] is not True for case in [*cases, *approval_cases])
    return {
        "schema_version": "heaps-h1-interface-observation-1.0",
        "scope": "existing_interfaces_generated_synthetic_only",
        "qualification": "not_a_heaps_runtime_or_clinical_acceptance",
        "environment": {
            "python": platform.python_version(),
            "platform": platform.system(),
            "jsonschema": importlib.metadata.version("jsonschema"),
            "date_time_checker_registered": "date-time" in FormatChecker().checkers,
        },
        "component_sha256": {
            name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in COMPONENTS
        },
        "hash_domains": {
            "core_fingerprint_utf8": core_digest,
            "renderer_hash_ascii_escaped": interface_digest,
            "independent_hash_controls_match": hash_controls_match,
            "interchangeable_by_prefix_removal": False,
        },
        "case_count": total,
        "record_case_count": len(cases),
        "approval_case_count": len(approval_cases),
        "cases_meeting_safety_expectations": total - unmet,
        "cases_with_unmet_safety_expectations": unmet,
        "cases": cases,
        "approval_cases": approval_cases,
        "diagnostic_exit_code": 2 if unmet or not hash_controls_match else 0,
    }


def main() -> int:
    """Print the complete observation; retain nonzero unsafe-boundary evidence."""
    result = run()
    print(json.dumps(result, indent=2, ensure_ascii=False, sort_keys=True))
    return 2 if result["diagnostic_exit_code"] == 2 else 0


if __name__ == "__main__":
    raise SystemExit(main())
