"""Assemble deterministic synthetic HEAPS drafts without operational authority.

The public seam consumes exact ingress bytes. Optional earlier packet manifests,
decisions and status claims are verification inputs, never authority to bypass
admission. Source-span extraction and AcciMap qualification are not implemented.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
import tempfile
from collections.abc import Mapping, Sequence
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path

from tools.evidence_core import fingerprint
from tools.heaps_validation import (
    MAX_INPUT_BYTES,
    MAX_TOTAL_BYTES,
    admit_case_profile,
    artifact_descriptor,
    check_references,
    ensure_bytes,
    json_bytes,
    manifest_inventory,
    obj,
    parse_json,
    raw_hash,
    read_artifact,
    rows,
    safe_path,
    schema_errors,
    strict_fields,
    text,
    text_list,
    utc_time,
    validate_profile_semantics,
)
from tools.interface_actions import canonical_hash, render_view, sanitize_export
from tools.json_shapes import JsonObject, is_array, is_object

LIMITATIONS = [
    "Generated synthetic preparation only; labels and input checks do not establish actual synthetic origin.",
    "This bounded consumer admits UTF-8 synthetic text and the shared safe-export subset; active links/HTTPS locators and unsafe values are rejected, not silently removed.",
    "Clinical review, substantive findings/actions approval, legal protection and actual organisational authority are not established.",
    "Record/reference integrity and raw artifact hashes do not prove source truth, causal support, independent corroboration or exact source spans.",
    "Current local HEAPS instrument conformity is not established; no system-of-record submission or case closure is performed.",
    "D0 byte-span and AcciMap composition are omitted and unqualified in this consumer.",
    "Chronology preserves supplied order and time precision; missing times remain unknown. Deadline assertions remain unverified and are not calculated.",
    "Action implementation and effectiveness are separate; completed actions do not prove outcomes.",
]
FALLBACK_TEMPLATE = b"# Original HEAPS synthetic outline\n\nNo local instrument has been supplied; conformity is not established.\n"


@dataclass(frozen=True)
class PacketResult:
    preparation_disposition: str
    review_disposition: str
    errors: tuple[str, ...]
    files: dict[str, bytes]
    status: JsonObject | None


def _markdown(value: object) -> str:
    value_text = (
        value if isinstance(value, str) else json.dumps(value, ensure_ascii=False, sort_keys=True)
    )
    # Escape user-controlled formatting after shared active-content admission.
    value_text = value_text.replace("\r\n", "\n").replace("\r", "\n").replace("\n", " / ")
    return re.sub(r"([\\`*{}<>|\[\]()!#])", r"\\\1", value_text)


def _md_bytes(lines: list[str]) -> bytes:
    return ("\n".join(lines).replace("\r\n", "\n").replace("\r", "\n").rstrip("\n") + "\n").encode(
        "utf-8"
    )


def _table(headers: list[str], values: list[list[object]]) -> list[str]:
    return [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
        *["| " + " | ".join(_markdown(value) for value in row) + " |" for row in values],
        "",
    ]


def _context(lines: list[str], title: str, value: object) -> None:
    lines.extend([f"## {title}", ""])
    items = value if is_array(value) else [value]
    if not items:
        lines.extend(["None supplied; no completion is inferred.", ""])
    for index, item in enumerate(items, 1):
        lines.extend([f"### Item {index}", ""])
        if is_object(item):
            lines.extend(
                _table(
                    ["Field", "Recorded value"],
                    [[key, field] for key, field in sorted(item.items())],
                )
            )
        else:
            lines.extend([_markdown(item), ""])


def _statement_usable(statement: JsonObject) -> bool:
    return statement.get("withdrawn") is not True and obj(statement["provenance"])[
        "review_state"
    ] not in {"withdrawn", "rejected"}


def _reports(case: JsonObject, profile: JsonObject) -> dict[str, bytes]:
    # Reuse the existing canonical interface only after the full domain guard.
    render_view(
        {**case, "source_sha256": canonical_hash(case)},
        audience="auditor",
        data_class="generated_synthetic",
        view_context={
            "citations": [row["source_id"] for row in rows(case.get("sources"))],
            "model_involvement": {"used": False},
            "limitations": list(LIMITATIONS),
            "approval_receipt_ids": [],
            "outstanding_review_ids": [row["review_id"] for row in rows(case.get("reviews"))],
        },
    )
    report = [
        "# HEAPS synthetic draft",
        "",
        "This is a preparation draft. Clinical review and substantive approval are not established.",
        "",
        f"Case: {_markdown(case['case_id'])}; version: {case['version']}.",
        "",
        f"Canonical fingerprint: {fingerprint(case)}.",
        "",
        "## Scope and limitations",
        "",
        *[f"- {value}" for value in LIMITATIONS],
        "",
    ]
    statements = rows(case.get("statements"))
    usable_count = sum(_statement_usable(row) for row in statements)
    preparation = "prepared" if usable_count else ("all_abstain" if statements else "empty")
    report.extend(
        [
            f"Preparation: {preparation}; input statements: {len(statements)}; usable draft items: {usable_count}; abstained items: {len(statements) - usable_count}.",
            "",
        ]
    )
    headings = {
        "observed_fact": "Recorded observations",
        "reported_account": "Reported accounts",
        "inference": "Inferences",
        "hypothesis": "Hypotheses and alternatives",
        "finding": "Proposed findings",
        "recommendation": "Draft recommendations",
        "decision": "Recorded decisions",
        "problem": "Recorded problems",
        "strength": "Recorded strengths",
        "weakness": "Recorded weaknesses",
    }
    for kind, heading in headings.items():
        report.extend([f"## {heading}", ""])
        group = [row for row in statements if row["kind"] == kind]
        report.extend(
            _table(
                [
                    "Statement",
                    "Kind",
                    "Text",
                    "Source",
                    "Review state",
                    "Draft eligibility",
                    "Uncertainty",
                ],
                [
                    [
                        row["statement_id"],
                        row["kind"],
                        row["text"],
                        obj(row["provenance"])["source_id"],
                        obj(row["provenance"])["review_state"],
                        "usable in recorded epistemic kind"
                        if _statement_usable(row)
                        else "abstained: withdrawn or rejected; retained for history",
                        row.get("uncertainty", "Not supplied"),
                    ]
                    for row in group
                ],
            )
        )
    _context(report, "Relationships and contrary evidence", case.get("relationships", []))
    _context(
        report, "Finding support, contrary evidence and alternatives", profile["finding_context"]
    )
    _context(report, "Factors: function and current status", case.get("factors", []))
    _context(report, "Factor taxonomy mapping", profile["factor_assignments"])
    _context(report, "Participation and unresolved agreement", profile["participation"])
    report.extend(
        [
            "Participation state and recorded accounts do not establish consultation completion or agreement.",
            "",
        ]
    )
    _context(report, "Review responsibilities and incident involvement", profile["roles"])
    _context(report, "Review-process selection", profile["selection"])
    _context(report, "Applicability and protection", profile["applicability"])
    _context(report, "Source snapshots and versions", profile["source_snapshots"])
    _context(report, "Source-family lineage", profile["source_families"])
    incident = [
        row
        for row in rows(profile["source_snapshots"])
        if "incident_evidence" in text_list(row["purposes"])
    ]
    report.extend(
        [
            f"Incident source count: {len(incident)}; incident source-family count: {len({text(row['source_family_id']) for row in incident})}.",
            "",
            "Independent corroboration is not established. Derivative records remain in their originating source family. Missing documentation does not establish omitted care.",
            "",
        ]
    )
    _context(report, "Separate clocks", profile["clocks"])
    _context(report, "Unverified deadlines and unresolved bases", profile["deadlines"])
    _context(report, "Template mapping and gaps", profile["template_mapping"])
    _context(report, "Concurrent route questions", profile["open_route_questions"])
    _context(report, "Optional components: omitted and unqualified", profile["optional_components"])
    report.extend(
        [
            "No qualified graph or source-span view is emitted. Accepted recommendations: 0; all recommendations remain drafts requiring substantive review.",
            "",
        ]
    )
    contexts = rows(profile["action_context"])
    unsupported = [row for row in contexts if not row["finding_refs"] and not row["condition_refs"]]
    if unsupported:
        report.extend(
            [
                "Recommendation support incomplete for: "
                + ", ".join(text(obj(row["recommendation_ref"])["id"]) for row in unsupported)
                + ".",
                "",
            ]
        )
    chronology = [
        "# HEAPS supplied chronology",
        "",
        "Supplied order is retained. Event time, document time and information availability are distinct. Unknown times and precision are not filled or sorted into an inferred order.",
        "",
    ]
    _context(chronology, "Chronology entries", profile["chronology"])
    actions = [
        "# HEAPS draft action register",
        "",
        "Recorded implementation is distinct from effectiveness. Outcome evidence and substantive approval are not established by an action-status label.",
        "",
    ]
    actions.extend(["Accepted recommendations: 0; recommendations remain drafts.", ""])
    if unsupported:
        actions.extend(
            [
                "Recommendation support incomplete for: "
                + ", ".join(text(obj(row["recommendation_ref"])["id"]) for row in unsupported)
                + ".",
                "",
            ]
        )
    _context(actions, "Canonical actions", case.get("actions", []))
    _context(actions, "Action mechanisms, measures and residual risk", profile["action_context"])
    _context(actions, "Outcome observations", case.get("outcomes", []))
    _context(actions, "Review records", case.get("reviews", []))
    _context(actions, "Referrals", case.get("referrals", []))
    report.extend(chronology[2:])
    report.extend(actions[2:])
    return {
        "report.md": _md_bytes(report),
        "chronology.md": _md_bytes(chronology),
        "actions.md": _md_bytes(actions),
    }


def _read_source_assets(
    case: JsonObject, profile: JsonObject, artifacts: Mapping[str, bytes]
) -> dict[str, bytes]:
    sources = {text(row["source_id"]): row for row in rows(case.get("sources"))}
    consumed: dict[str, bytes] = {}
    seen_paths: set[str] = set()
    for snapshot in rows(profile["source_snapshots"]):
        if snapshot["state"] != "available":
            continue
        source = sources[text(snapshot["source_id"])]
        citation = source.get("citation")
        locator = snapshot["locator"]
        path_value = (
            citation
            if isinstance(citation, str)
            else (
                locator.removeprefix("synthetic:")
                if isinstance(locator, str) and locator.startswith("synthetic:")
                else None
            )
        )
        path = safe_path(path_value)
        if (
            isinstance(citation, str)
            and isinstance(locator, str)
            and locator.startswith("synthetic:")
            and safe_path(locator.removeprefix("synthetic:")) != path
        ):
            raise ValueError("source snapshot: local locator and canonical citation disagree")
        if path.casefold() in seen_paths:
            raise ValueError("source artifact: duplicate/colliding source path")
        seen_paths.add(path.casefold())
        payload = artifacts.get(path)
        if payload is None or not payload or len(payload) > MAX_INPUT_BYTES:
            raise ValueError("artifact.raw_byte_identity: source bytes missing, empty or oversized")
        if raw_hash(payload) != snapshot["raw_sha256"] or source[
            "fingerprint"
        ] != "sha256:" + raw_hash(payload):
            raise ValueError("artifact.raw_byte_identity: stale source bytes or fingerprint")
        _safe_asset(payload)
        consumed[path] = payload
    return consumed


def _safe_asset(payload: bytes) -> None:
    try:
        content = payload.decode("utf-8")
    except UnicodeError:
        raise ValueError("artifact: only UTF-8 synthetic text is supported") from None
    sanitize_export(content)


def _template(
    profile: JsonObject, artifacts: Mapping[str, bytes], template_path: str | None
) -> tuple[str, bytes]:
    mapping = obj(profile["template_mapping"])
    expected = mapping["template_raw_sha256"]
    if expected is None:
        if template_path is not None:
            # An unavailable local instrument does not consume a supplied template.
            safe_path(template_path)
        return "template.md", FALLBACK_TEMPLATE
    if template_path is None:
        matches = [path for path, payload in artifacts.items() if raw_hash(payload) == expected]
        if len(matches) != 1:
            raise ValueError("template: a unique explicitly bound template artifact is required")
        template_path = matches[0]
    path = safe_path(template_path)
    payload = artifacts.get(path)
    if (
        payload is None
        or not payload
        or len(payload) > MAX_INPUT_BYTES
        or raw_hash(payload) != expected
    ):
        raise ValueError("artifact.raw_byte_identity: stale template bytes or missing template")
    _safe_asset(payload)
    return path, payload


def _decision(
    decision: JsonObject | None,
    manifest: JsonObject,
    manifest_bytes: bytes,
    index: Mapping[str, tuple[str, JsonObject]],
    evaluated_at: str,
    prepared: bool,
) -> tuple[str, str]:
    if decision is None:
        return "not_requested", "not_established" if prepared else "withheld"
    errors = schema_errors("review-decision", decision)
    if errors:
        raise ValueError("; ".join(errors[:16]))
    strict_fields(decision)
    sanitize_export(decision)
    check_references(decision, index)
    decision_state = decision["decision"]
    if decision_state == "approved_synthetic_draft":
        if obj(decision["author_role_ref"])["id"] == obj(decision["reviewer_role_ref"])["id"]:
            raise ValueError("decision: same author and reviewer role cannot approve")
        issued = utc_time(decision["issued_at"], "decision issued_at")
        expires = utc_time(decision["expires_at"], "decision expires_at")
        now = utc_time(evaluated_at, "evaluated_at")
        declared = utc_time(decision["evaluated_at"], "decision evaluated_at")
        if not issued <= declared <= now < expires:
            raise ValueError("decision: outside issued/evaluated/expiry validity interval")
    binding = obj(decision["manifest_binding"])
    if binding["manifest_id"] != manifest["manifest_id"] or binding["raw_sha256"] != raw_hash(
        manifest_bytes
    ):
        return "stale", "stale"
    if not prepared:
        return "not_requested", "withheld"
    return {
        "approved_synthetic_draft": "synthetic_draft_reviewed",
        "pending": "pending",
        "returned": "returned",
        "rejected": "rejected",
    }[text(decision_state)], "not_established"


def _verify_status(claim: JsonObject, actual: JsonObject) -> None:
    sanitize_export(claim)
    errors = schema_errors("status-receipt", claim)
    if errors:
        raise ValueError("; ".join(errors[:16]))
    strict_fields(claim)
    for key in (
        "profile_binding",
        "manifest_binding",
        "decision_binding",
        "preparation",
        "structural_check",
        "source_check",
        "source_check_scope",
        "template_mapping",
        "review",
        "submission",
        "clinical_review",
        "actual_authority",
        "counts",
        "evaluated_at",
    ):
        if claim[key] != actual[key]:
            raise ValueError(f"status claim: {key} differs from executed observation")


def assemble_packet(
    case_bytes: bytes,
    profile_bytes: bytes,
    artifacts: Mapping[str, bytes],
    *,
    evaluated_at: str,
    template_path: str | None = None,
    manifest_bytes: bytes | None = None,
    decision_bytes: bytes | None = None,
    status_bytes: bytes | None = None,
) -> PacketResult:
    """Admit exact synthetic bytes and return an entirely detached draft packet.

    Rejection returns no accepted files and never reflects source text in errors.
    The fixed evaluation timestamp is supplied by the caller; host time is unused.
    """
    try:
        utc_time(evaluated_at, "evaluated_at")
        case = parse_json(case_bytes, "case")
        profile = parse_json(profile_bytes, "profile")
        index = admit_case_profile(case, profile)
        validate_profile_semantics(profile, index)
        folded_paths: set[str] = set()
        for path, payload in artifacts.items():
            safe_path(path)
            if path.casefold() in folded_paths:
                raise ValueError("artifact: case-insensitive path collision")
            folded_paths.add(path.casefold())
            ensure_bytes(payload)
        source_assets = _read_source_assets(case, profile, artifacts)
        selected_template_path, template_payload = _template(profile, artifacts, template_path)
        prior = parse_json(manifest_bytes, "manifest") if manifest_bytes is not None else None
        prior_assets: dict[str, bytes] = {}
        if prior is not None:
            prior_assets = manifest_inventory(prior, artifacts)
            components = obj(prior["components"])
            old_case = obj(components["case"])
            old_profile = obj(components["profile"])
            if (
                prior["case_id"] != case["case_id"]
                or prior["profile_id"] != profile["profile_id"]
                or prior["profile_version"] != profile["profile_version"]
            ):
                raise ValueError("manifest: stale case/profile binding")
            bound_case = parse_json(prior_assets[text(old_case["path"])], "manifest case")
            bound_profile = parse_json(prior_assets[text(old_profile["path"])], "manifest profile")
            if bound_case != case or bound_profile != profile:
                raise ValueError("manifest: case/profile content binding is stale")
            inventoried = {text(row["path"]) for row in rows(components["sources"])}
            if set(source_assets) != inventoried:
                raise ValueError("manifest: source inventory is incomplete")
            if obj(components["template"])["sha256"] != raw_hash(template_payload):
                raise ValueError("manifest: template binding is stale")
        decision = parse_json(decision_bytes, "decision") if decision_bytes is not None else None
        status_claim = parse_json(status_bytes, "status") if status_bytes is not None else None
        files = {
            "case.json": json_bytes(case),
            "profile.json": json_bytes(profile),
            "mapping.json": json_bytes(profile["template_mapping"]),
            "template.md": template_payload,
            "ingress/case.json": case_bytes,
            "ingress/profile.json": profile_bytes,
            **_reports(case, profile),
        }
        support_descriptors: list[JsonObject] = [
            artifact_descriptor("heaps-ingress-case", "ingress/case.json", case_bytes),
            artifact_descriptor("heaps-ingress-profile", "ingress/profile.json", profile_bytes),
        ]
        source_descriptors: list[JsonObject] = []
        for path, payload in sorted(source_assets.items()):
            output = path
            if output.casefold() in {name.casefold() for name in files}:
                raise ValueError("source artifact: output path collision")
            files[output] = payload
            source_descriptors.append(
                artifact_descriptor("heaps-source-" + raw_hash(path.encode())[:24], output, payload)
            )
        for component in rows(profile["optional_components"]):
            descriptor = obj(component["artifact"])
            path, payload = read_artifact(descriptor, artifacts)
            _safe_asset(payload)
            output = path
            if output in files:
                raise ValueError("optional component: duplicate consumed artifact")
            files[output] = payload
            support_descriptors.append(
                artifact_descriptor(
                    "heaps-component-" + raw_hash(path.encode())[:24], output, payload
                )
            )
        # Earlier reports/mappings are verified historical inputs, never substituted
        # for generated reports. Capture them once without putting a later manifest
        # or decision inside the new manifest.
        if prior is not None:
            components = obj(prior["components"])
            extras = [
                obj(components["case"]),
                obj(components["profile"]),
                obj(components["mapping"]),
                obj(components["template"]),
                *rows(components["sources"]),
                *rows(components["reports"]),
                *rows(components["supporting_artifacts"]),
            ]
            for descriptor in extras:
                path = text(descriptor["path"])
                payload = prior_assets[path]
                _safe_asset(payload)
                if files.get(path) == payload:
                    continue
                output = path if path.startswith("history/") else "history/" + path
                if output in files:
                    if files[output] != payload:
                        raise ValueError("manifest: historical artifact collision")
                    continue
                files[output] = payload
                support_descriptors.append(
                    artifact_descriptor(
                        "heaps-history-" + raw_hash(output.encode())[:24], output, payload
                    )
                )
        source_descriptors.sort(key=lambda row: text(row["path"]))
        support_descriptors.sort(key=lambda row: text(row["path"]))
        manifest: JsonObject = {
            "schema_version": "heaps-packet-manifest-1.0",
            "manifest_id": "heaps-manifest-" + raw_hash(files["profile.json"])[:24],
            "data_class": "generated_synthetic",
            "privacy_mode": "fully_local",
            "case_id": case["case_id"],
            "profile_id": profile["profile_id"],
            "profile_version": profile["profile_version"],
            "hash_domain": "sha256-raw-bytes-v1",
            "ordering": "fixed-groups-path-ascending-v1",
            "components": {
                "case": artifact_descriptor("heaps-case", "case.json", files["case.json"]),
                "profile": artifact_descriptor(
                    "heaps-profile", "profile.json", files["profile.json"]
                ),
                "sources": source_descriptors,
                "supporting_artifacts": support_descriptors,
                "mapping": artifact_descriptor(
                    "heaps-mapping", "mapping.json", files["mapping.json"]
                ),
                "template": artifact_descriptor(
                    "heaps-template", "template.md", files["template.md"]
                ),
                "reports": [
                    artifact_descriptor("heaps-" + path.split(".")[0], path, files[path])
                    for path in ("actions.md", "chronology.md", "report.md")
                ],
            },
        }
        del selected_template_path  # The exact template bytes, not its local filename, are emitted.
        manifest_inventory(manifest, files)
        if sum(map(len, files.values())) > MAX_TOTAL_BYTES:
            raise ValueError("packet: total consumed/generated bytes exceeds 32 MiB")
        generated_manifest = json_bytes(manifest)
        statements = rows(case.get("statements"))
        usable = sum(_statement_usable(row) for row in statements)
        preparation = "prepared" if usable else ("all_abstain" if statements else "empty")
        review, review_disposition = _decision(
            decision, manifest, generated_manifest, index, evaluated_at, preparation == "prepared"
        )
        status: JsonObject = {
            "schema_version": "heaps-status-receipt-1.0",
            "receipt_id": "heaps-status-" + raw_hash(generated_manifest)[:24],
            "data_class": "generated_synthetic",
            "privacy_mode": "fully_local",
            "profile_binding": {
                "profile_id": profile["profile_id"],
                "profile_version": profile["profile_version"],
                "raw_sha256": raw_hash(files["profile.json"]),
                "hash_domain": "sha256-raw-bytes-v1",
            },
            "manifest_binding": {
                "manifest_id": manifest["manifest_id"],
                "raw_sha256": raw_hash(generated_manifest),
                "hash_domain": "sha256-raw-bytes-v1",
            },
            "decision_binding": None
            if decision is None or decision_bytes is None
            else {
                "decision_id": decision["decision_id"],
                "raw_sha256": raw_hash(decision_bytes),
                "hash_domain": "sha256-raw-bytes-v1",
            },
            "preparation": preparation,
            "structural_check": "passed",
            "source_check": "passed"
            if all(row["state"] == "available" for row in rows(profile["source_snapshots"]))
            else "partial",
            "source_check_scope": "record_reference_integrity",
            "template_mapping": obj(profile["template_mapping"])["state"],
            "review": review,
            "submission": "not_submitted",
            "clinical_review": "not_established",
            "actual_authority": "unverified",
            "counts": {
                "input_items": len(statements),
                "usable_items": usable,
                "abstained_items": len(statements) - usable,
            },
            "errors": [],
            "limitations": list(LIMITATIONS),
            "evaluated_at": evaluated_at,
        }
        if status_claim is not None:
            _verify_status(status_claim, status)
        generated_errors = schema_errors("status-receipt", status)
        if generated_errors:
            raise ValueError("generated status failed structural admission")
        files["manifest.json"] = generated_manifest
        files["status.json"] = json_bytes(status)
        if decision_bytes is not None:
            files["decision.json"] = decision_bytes
        if manifest_bytes is not None:
            files["verification-input-manifest.json"] = manifest_bytes
        if status_bytes is not None:
            files["verification-input-status.json"] = status_bytes
        files["verification.json"] = json_bytes(
            {
                "schema_version": "heaps-verification-1.0",
                "scope": "synthetic_packet_verification",
                "data_class": "generated_synthetic",
                "privacy_mode": "fully_local",
                "input_manifest_sha256": raw_hash(manifest_bytes)
                if manifest_bytes is not None
                else None,
                "input_status_sha256": raw_hash(status_bytes) if status_bytes is not None else None,
                "generated_manifest_sha256": raw_hash(generated_manifest),
                "status_sha256": raw_hash(files["status.json"]),
                "evaluated_at": evaluated_at,
                "actual_authority": "unverified",
                "clinical_review": "not_established",
                "submission": "not_submitted",
            }
        )
        if sum(map(len, files.values())) > MAX_TOTAL_BYTES:
            raise ValueError(
                "packet: total output bytes including detached receipts exceeds 32 MiB"
            )
        return PacketResult(
            "prepare_draft" if usable else "abstain", review_disposition, (), files, status
        )
    except (ValueError, KeyError, TypeError, RecursionError) as exc:
        # Guarded helpers give content-free messages; unexpected shape errors
        # never expose the source object or masquerade as a successful packet.
        message = (
            str(exc) if isinstance(exc, ValueError) else "input: invalid object shape or nesting"
        )
        return PacketResult(
            "reject_input",
            "stale"
            if decision_bytes is not None and ("stale" in message or "raw_byte_identity" in message)
            else "not_established",
            (message,),
            {},
            None,
        )


def _read_file(path: Path, label: str) -> bytes:
    if (
        path.is_symlink()
        or any(parent.is_symlink() for parent in path.parents)
        or not path.is_file()
    ):
        raise ValueError(f"{label}: must be a regular file, not a symlink")
    if path.stat().st_size > MAX_INPUT_BYTES:
        raise ValueError(f"{label}: exceeds 4 MiB input bound")
    return path.read_bytes()


def _asset_paths(
    case_bytes: bytes, profile_bytes: bytes, template_path: str | None, manifest_bytes: bytes | None
) -> set[str]:
    case = parse_json(case_bytes, "case")
    profile = parse_json(profile_bytes, "profile")
    paths: set[str] = set()
    sources = {text(row["source_id"]): row for row in rows(case.get("sources"))}
    for snapshot in rows(profile.get("source_snapshots")):
        if snapshot.get("state") != "available":
            continue
        source = sources.get(text(snapshot.get("source_id")))
        citation = source.get("citation") if source is not None else None
        locator = snapshot.get("locator")
        if isinstance(citation, str):
            paths.add(safe_path(citation))
        elif isinstance(locator, str) and locator.startswith("synthetic:"):
            paths.add(safe_path(locator.removeprefix("synthetic:")))
    for row in rows(profile.get("optional_components")):
        paths.add(safe_path(obj(row.get("artifact"))["path"]))
    if (
        template_path is not None
        and obj(profile.get("template_mapping")).get("template_raw_sha256") is not None
    ):
        paths.add(safe_path(template_path))
    if manifest_bytes is not None:
        manifest = parse_json(manifest_bytes, "manifest")
        components = obj(manifest.get("components"))
        for group in components.values():
            entries = rows(group) if is_array(group) else [obj(group)]
            paths.update(safe_path(row["path"]) for row in entries)
    return paths


def _read_assets(root: Path, paths: set[str]) -> dict[str, bytes]:
    if (
        root.is_symlink()
        or any(parent.is_symlink() for parent in root.parents)
        or not root.is_dir()
    ):
        raise ValueError("artifacts: requires a regular directory")
    assets: dict[str, bytes] = {}
    folded: set[str] = set()
    total = 0
    for relative in sorted(paths):
        if relative.casefold() in folded:
            raise ValueError("artifacts: case-insensitive path collision")
        folded.add(relative.casefold())
        path = root
        for component in relative.split("/"):
            path = path / component
            if path.is_symlink():
                raise ValueError("artifacts: symlink path component is forbidden")
        if not path.exists():
            continue  # The semantic consumer reports missing required inputs.
        payload = _read_file(path, "artifact")
        total += len(payload)
        if total > MAX_TOTAL_BYTES:
            raise ValueError("artifacts: total bytes exceeds 32 MiB")
        assets[relative] = payload
    return assets


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", required=True, type=Path)
    parser.add_argument("--profile", required=True, type=Path)
    parser.add_argument("--artifacts", required=True, type=Path)
    parser.add_argument("--template")
    parser.add_argument("--evaluated-at", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--manifest", type=Path)
    parser.add_argument("--decision", type=Path)
    parser.add_argument("--status", type=Path)
    args = parser.parse_args(argv)
    try:
        case_path: Path = args.case
        profile_path: Path = args.profile
        artifact_root: Path = args.artifacts
        output: Path = args.output
        template_path: str | None = args.template
        evaluated_at: str = args.evaluated_at
        manifest_path: Path | None = args.manifest
        decision_path: Path | None = args.decision
        status_path: Path | None = args.status
        if output.exists() or output.is_symlink():
            raise ValueError("output: must be a new directory; existing paths are not overwritten")
        if not output.parent.is_dir() or any(
            parent.is_symlink() for parent in [output.parent, *output.parents]
        ):
            raise ValueError("output: parent must exist and contain no symlinks")
        case_bytes = _read_file(case_path, "case")
        profile_bytes = _read_file(profile_path, "profile")
        manifest_bytes = _read_file(manifest_path, "manifest") if manifest_path else None
        decision_bytes = _read_file(decision_path, "decision") if decision_path else None
        status_bytes = _read_file(status_path, "status") if status_path else None
        artifacts = _read_assets(
            artifact_root, _asset_paths(case_bytes, profile_bytes, template_path, manifest_bytes)
        )
        result = assemble_packet(
            case_bytes,
            profile_bytes,
            artifacts,
            evaluated_at=evaluated_at,
            template_path=template_path,
            manifest_bytes=manifest_bytes,
            decision_bytes=decision_bytes,
            status_bytes=status_bytes,
        )
        if result.files:
            with tempfile.TemporaryDirectory(prefix=".heaps-packet-", dir=output.parent) as staging:
                staged = Path(staging) / "packet"
                staged.mkdir()
                for relative, payload in sorted(result.files.items()):
                    destination = staged / safe_path(relative)
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    with destination.open("xb") as handle:
                        handle.write(payload)
                # Reserve the destination without overwriting a concurrent writer.
                output.mkdir()
                reserved = True
                try:
                    if sys.platform == "win32":
                        output.rmdir()
                        reserved = False
                        staged.rename(output)
                    else:
                        staged.replace(output)
                except OSError:
                    # Only our empty reservation can be removed; unrelated
                    # content causes rmdir to fail and is never deleted.
                    if reserved and output.is_dir() and not output.is_symlink():
                        with suppress(OSError):
                            output.rmdir()
                    raise
        print(
            json.dumps(
                {
                    "preparation_disposition": result.preparation_disposition,
                    "review_disposition": result.review_disposition,
                    "errors": result.errors,
                    "output_files": sorted(result.files),
                },
                sort_keys=True,
            )
        )
        return {"prepare_draft": 0, "reject_input": 2, "abstain": 3}[result.preparation_disposition]
    except (ValueError, OSError, KeyError, TypeError) as exc:
        error = (
            str(exc) if isinstance(exc, ValueError) else "filesystem or input shape boundary failed"
        )
        print(
            json.dumps(
                {
                    "preparation_disposition": "reject_input",
                    "review_disposition": "not_established",
                    "errors": [error],
                    "output_files": [],
                },
                sort_keys=True,
            )
        )
        return 2


if __name__ == "__main__":
    sys.exit(main())
