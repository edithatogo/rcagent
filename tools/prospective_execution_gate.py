"""Gate a reviewed repository primary session; not observation admission.

The trust root is the owner-controlled reviewed delivery workflow. Committed
evidence integrity is not cryptographic reviewer identity or hostile-owner defence.
"""

from __future__ import annotations

import hashlib
import json
import platform
import re
from dataclasses import dataclass
from pathlib import Path

from tools import prospective_execution_identity as identity
from tools import prospective_freeze as freeze
from tools import prospective_native_protocol as native
from tools import prospective_server_model as model
from tools import prospective_slot_binding as binding
from tools.evaluation_preflight import _digest, _unique

REVIEW_PATH = "conductor/reviews/primary-execution.json"
SOURCES = tuple(
    "tools/" + name + ".py"
    for name in (
        "__init__",
        "prospective_execution_gate",
        "prospective_execution_identity",
        "prospective_primary_session",
        "prospective_study_controller",
        "prospective_observation_admission",
        "prospective_native_prerequisites",
        "prospective_freeze",
        "prospective_slot_binding",
        "prospective_native_protocol",
        "prospective_protocol",
        "prospective_runner_contract",
        "native_completion",
        "prospective_inventory",
        "evaluation_preflight",
        "prospective_server_model",
        "prospective_model",
        "local_model_comparator",
        "prospective_server_session",
        "server_process",
        "unix_http_capture",
        "darwin_server_v030",
        "darwin_runtime_v030",
        "darwin_runtime_profile",
    )
)
REGISTRY = "evaluation/benchmark/comparators.json"
ADAPTER = "tools/prospective_primary_session.py"


@dataclass(frozen=True)
class _Plan:
    payload: bytes

    def value(self) -> dict:
        return json.loads(self.payload)


def _canonical(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode()


def _blob(root: Path, commit: str, path: str) -> bytes:
    if not re.fullmatch(r"[A-Za-z0-9_-]+(?:/[A-Za-z0-9_.-]+)+", path) or any(
        part in {".", ".."} for part in path.split("/")
    ):
        raise ValueError("invalid_review_path")
    entry = freeze._git(root, "ls-tree", "-z", commit, "--", path)
    match = re.fullmatch(rb"100644 blob ([0-9a-f]{40})\t([^\x00]+)\x00", entry)
    if match is None or match[2] != path.encode():
        raise ValueError("review_not_regular_blob")
    raw = freeze._git(root, "cat-file", "blob", match[1].decode())
    if not raw:
        raise ValueError("empty_review_evidence")
    return raw


def _keys(value: object, keys: set[str]) -> None:
    if type(value) is not dict or set(value) != keys:
        raise ValueError("invalid_review_record")


def _record(root: Path, review_commit: str) -> tuple[dict, str]:
    raw = _blob(root, review_commit, REVIEW_PATH)
    try:
        value = json.loads(raw, object_pairs_hook=_unique)
        _keys(
            value,
            {
                "version",
                "source_commit",
                "protocol_sha256",
                "adapter_sha256",
                "closure_sha256",
                "environment_sha256",
                "reviewers",
                "unresolved_findings",
            },
        )
        if value["version"] != "primary-review-v1" or value["unresolved_findings"] != []:
            raise ValueError("invalid_review_record")
        if type(value["unresolved_findings"]) is not list:
            raise ValueError("invalid_review_record")
        if (
            type(value["source_commit"]) is not str
            or re.fullmatch(r"[0-9a-f]{40}", value["source_commit"]) is None
        ):
            raise ValueError("invalid_review_record")
        for key in ("protocol_sha256", "adapter_sha256", "closure_sha256", "environment_sha256"):
            if not _digest(value[key]):
                raise ValueError("invalid_review_record")
        reviewers = value["reviewers"]
        if type(reviewers) is not list or len(reviewers) != 3:
            raise ValueError("invalid_review_record")
        roles, ids, paths = set(), set(), set()
        for reviewer in reviewers:
            _keys(reviewer, {"role", "reviewer_id", "outcome", "evidence_path", "evidence_sha256"})
            if (
                reviewer["role"] not in {"acceptance", "evidence-integrity", "safety-privacy"}
                or reviewer["outcome"] != "pass"
            ):
                raise ValueError("invalid_review_record")
            name = reviewer["reviewer_id"]
            path = reviewer["evidence_path"]
            if (
                type(name) is not str
                or not 1 <= len(name) <= 200
                or type(path) is not str
                or len(path) > 200
                or not path.startswith("conductor/reviews/evidence/")
                or not _digest(reviewer["evidence_sha256"])
            ):
                raise ValueError("invalid_review_record")
            evidence = _blob(root, review_commit, path)
            if hashlib.sha256(evidence).hexdigest() != reviewer["evidence_sha256"]:
                raise ValueError("review_evidence_mismatch")
            envelope = json.loads(evidence, object_pairs_hook=_unique)
            _keys(
                envelope,
                {
                    "role",
                    "reviewer_id",
                    "source_commit",
                    "protocol_sha256",
                    "closure_sha256",
                    "environment_sha256",
                    "outcome",
                    "evidence_locator",
                    "unresolved_findings",
                },
            )
            for key in ("role", "reviewer_id", "outcome"):
                if type(envelope[key]) is not str or envelope[key] != reviewer[key]:
                    raise ValueError("review_evidence_scope_mismatch")
            for key in ("source_commit", "protocol_sha256", "closure_sha256", "environment_sha256"):
                if type(envelope[key]) is not str or envelope[key] != value[key]:
                    raise ValueError("review_evidence_scope_mismatch")
            if (
                type(envelope["unresolved_findings"]) is not list
                or envelope["unresolved_findings"]
                or type(envelope["evidence_locator"]) is not str
                or not 1 <= len(envelope["evidence_locator"]) <= 500
            ):
                raise ValueError("review_evidence_scope_mismatch")
            roles.add(reviewer["role"])
            ids.add(name)
            paths.add(path)
        if len(roles) != 3 or len(ids) != 3 or len(paths) != 3:
            raise ValueError("invalid_review_record")
        _canonical(value)
    except (TypeError, KeyError, UnicodeError, RecursionError):
        raise ValueError("invalid_review_record") from None
    return value, hashlib.sha256(raw).hexdigest()


def _verify(
    protocol_path: Path, pin: str, slot_id: str, review_commit: str, root: Path, model_root: Path
) -> _Plan:
    if (platform.system(), platform.machine()) != ("Darwin", "arm64"):
        raise ValueError("unsupported_primary_platform")
    if type(review_commit) is not str or ".." in protocol_path.parts:
        raise ValueError("invalid_gate_path_or_commit")
    root, protocol_path, relative = freeze._repository(protocol_path, review_commit, root)
    record, review_pin = _record(root, review_commit)
    source = record["source_commit"]
    if source == review_commit:
        raise ValueError("review_must_follow_source")
    freeze._git(root, "merge-base", "--is-ancestor", source, review_commit)
    value, candidate = native._validated_candidate(protocol_path, pin)
    if type(slot_id) is not str or len(slot_id) > 150 or slot_id not in candidate["requests"]:
        raise ValueError("slot_not_in_protocol")
    if record["protocol_sha256"] != pin:
        raise ValueError("review_protocol_mismatch")
    refs = [case["input"] for case in value["cases"]]
    refs.extend(value[key] for key in ("rubric", "scoring_instructions", "prompt_template"))
    expected = {relative: pin, REGISTRY: value["condition"]["registry_sha256"]}
    paths = [relative]
    for ref in refs:
        path = (protocol_path.parent / ref["path"]).relative_to(root).as_posix()
        paths.append(path)
        expected[path] = ref["sha256"]
    paths.extend((*SOURCES, REGISTRY))
    files = freeze._committed_files(root, source, paths, expected)
    if freeze._committed_files(root, review_commit, paths, expected) != files:
        raise ValueError("review_source_parity_mismatch")
    hashes = {item["path"]: item["sha256"] for item in files}
    identity.project_closure(root, SOURCES, hashes)
    if (
        hashes[ADAPTER] != value["condition"]["adapter_sha256"]
        or hashes[ADAPTER] != record["adapter_sha256"]
        or identity.digest(files) != record["closure_sha256"]
    ):
        raise ValueError("review_closure_mismatch")
    environment = identity.environment_identity()
    if identity.digest(environment) != record["environment_sha256"]:
        raise ValueError("environment_identity_mismatch")
    selected = binding.bind_slot(protocol_path, pin, slot_id, model_root)
    admission = model.admit_model(model_root)
    if (
        selected["request"] != candidate["requests"][slot_id]
        or selected["eligibility"]["admission_sha256"] != admission["admission_sha256"]
    ):
        raise ValueError("gate_identity_changed")
    evidence = {
        "review_commit": review_commit,
        "source_commit": source,
        "review_sha256": review_pin,
        "closure_sha256": identity.digest(files),
        "environment_sha256": identity.digest(environment),
        "protocol_sha256": pin,
        "study_id": candidate["study_id"],
        "slot_id": slot_id,
        "adapter_sha256": hashes[ADAPTER],
        "execution_permitted": True,
        "admitted": False,
        "study_unlocked": False,
        "limitations": [
            "trusted-owner-controlled-repository-review",
            "reviewer-cryptographic-identity-not-verified",
            "same-user-races-not-prevented",
            "loaded-code-and-os-not-attested",
            "not-observation-admission",
        ],
    }
    return _Plan(
        _canonical(
            {
                "request": candidate["requests"][slot_id],
                "admission": admission,
                "evidence": evidence,
            }
        )
    )
