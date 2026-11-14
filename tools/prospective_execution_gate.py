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
from typing import Literal, TypeAlias, TypedDict, TypeGuard

from tools import json_shapes
from tools import prospective_execution_identity as identity
from tools import prospective_freeze as freeze
from tools import prospective_native_protocol as native
from tools import prospective_runner_contract as runner
from tools import prospective_server_model as model
from tools import prospective_slot_binding as binding
from tools.evaluation_preflight import is_sha256, unique_object_pairs

REVIEW_PATH = "conductor/reviews/primary-execution.json"
SOURCES = tuple(
    "tools/" + name + ".py"
    for name in (
        "__init__",
        "json_shapes",
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


ReviewRole: TypeAlias = Literal["acceptance", "evidence-integrity", "safety-privacy"]


class ReviewerRecord(TypedDict):
    role: ReviewRole
    reviewer_id: str
    outcome: Literal["pass"]
    evidence_path: str
    evidence_sha256: str


class ReviewRecord(TypedDict):
    version: Literal["primary-review-v1"]
    source_commit: str
    protocol_sha256: str
    adapter_sha256: str
    closure_sha256: str
    environment_sha256: str
    reviewers: list[ReviewerRecord]
    unresolved_findings: list[object]


class ReviewEnvelope(TypedDict):
    role: ReviewRole
    reviewer_id: str
    source_commit: str
    protocol_sha256: str
    closure_sha256: str
    environment_sha256: str
    outcome: Literal["pass"]
    evidence_locator: str
    unresolved_findings: list[object]


class ExecutionEvidence(TypedDict):
    review_commit: str
    source_commit: str
    review_sha256: str
    closure_sha256: str
    environment_sha256: str
    protocol_sha256: str
    study_id: str
    slot_id: str
    adapter_sha256: str
    execution_permitted: Literal[True]
    admitted: Literal[False]
    study_unlocked: Literal[False]
    limitations: list[str]


class ExecutionPlanValue(TypedDict):
    request: runner.RequestPackage
    admission: model.ModelAdmission
    evidence: ExecutionEvidence


def _strings(value: object) -> TypeGuard[list[str]]:
    return json_shapes.is_array(value) and all(isinstance(item, str) for item in value)


def _role(value: object) -> TypeGuard[ReviewRole]:
    return isinstance(value, str) and value in {
        "acceptance",
        "evidence-integrity",
        "safety-privacy",
    }


def _is_reviewer(value: object) -> TypeGuard[ReviewerRecord]:
    return (
        json_shapes.is_object(value)
        and _role(value.get("role"))
        and isinstance(value.get("outcome"), str)
        and value.get("outcome") == "pass"
        and all(
            isinstance(value.get(key), str)
            for key in ("reviewer_id", "evidence_path", "evidence_sha256")
        )
    )


def _is_review_record(value: object) -> TypeGuard[ReviewRecord]:
    if (
        not json_shapes.is_object(value)
        or not isinstance(value.get("version"), str)
        or value.get("version") != "primary-review-v1"
        or not all(
            isinstance(value.get(key), str)
            for key in (
                "source_commit",
                "protocol_sha256",
                "adapter_sha256",
                "closure_sha256",
                "environment_sha256",
            )
        )
        or not json_shapes.is_array(value.get("unresolved_findings"))
    ):
        return False
    reviewers = value.get("reviewers")
    return json_shapes.is_array(reviewers) and all(_is_reviewer(item) for item in reviewers)


def _is_review_envelope(value: object) -> TypeGuard[ReviewEnvelope]:
    return (
        json_shapes.is_object(value)
        and _role(value.get("role"))
        and isinstance(value.get("outcome"), str)
        and value.get("outcome") == "pass"
        and all(
            isinstance(value.get(key), str)
            for key in (
                "reviewer_id",
                "source_commit",
                "protocol_sha256",
                "closure_sha256",
                "environment_sha256",
                "evidence_locator",
            )
        )
        and json_shapes.is_array(value.get("unresolved_findings"))
    )


def _is_artifact(value: object) -> TypeGuard[runner.Artifact]:
    return (
        json_shapes.is_object(value)
        and isinstance(value.get("base64"), str)
        and isinstance(value.get("sha256"), str)
        and type(value.get("bytes")) is int
    )


def _is_request(value: object) -> TypeGuard[runner.RequestPackage]:
    if not json_shapes.is_object(value):
        return False
    generation, limits = value.get("generation"), value.get("limits")
    return (
        isinstance(value.get("version"), str)
        and all(_is_artifact(value.get(key)) for key in ("template", "input", "prompt", "request"))
        and json_shapes.is_object(generation)
        and all(type(item) is int for item in generation.values())
        and json_shapes.is_object(limits)
        and type(limits.get("max_bytes_per_artifact")) is int
        and limits.get("context_tokens_validated") is False
        and _strings(value.get("limitations"))
        and value.get("execution_observed") is False
        and value.get("admitted") is False
        and value.get("study_unlocked") is False
    )


def _is_execution_evidence(value: object) -> TypeGuard[ExecutionEvidence]:
    return (
        json_shapes.is_object(value)
        and all(
            isinstance(value.get(key), str)
            for key in (
                "review_commit",
                "source_commit",
                "review_sha256",
                "closure_sha256",
                "environment_sha256",
                "protocol_sha256",
                "study_id",
                "slot_id",
                "adapter_sha256",
            )
        )
        and value.get("execution_permitted") is True
        and value.get("admitted") is False
        and value.get("study_unlocked") is False
        and _strings(value.get("limitations"))
    )


def _is_execution_plan(value: object) -> TypeGuard[ExecutionPlanValue]:
    return (
        json_shapes.is_object(value)
        and _is_request(value.get("request"))
        and model.is_model_admission(value.get("admission"))
        and _is_execution_evidence(value.get("evidence"))
    )


@dataclass(frozen=True)
class ExecutionPlan:
    payload: bytes

    def value(self) -> ExecutionPlanValue:
        value: object = json.loads(self.payload)
        if not _is_execution_plan(value):
            raise ValueError("invalid_execution_plan")
        return value


def canonical_bytes(value: object) -> bytes:
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode()


def committed_blob(root: Path, commit: str, path: str) -> bytes:
    if not re.fullmatch(r"[A-Za-z0-9_-]+(?:/[A-Za-z0-9_.-]+)+", path) or any(
        part in {".", ".."} for part in path.split("/")
    ):
        raise ValueError("invalid_review_path")
    entry = freeze.git_bytes(root, "ls-tree", "-z", commit, "--", path)
    match = re.fullmatch(rb"100644 blob ([0-9a-f]{40})\t([^\x00]+)\x00", entry)
    if match is None or match[2] != path.encode():
        raise ValueError("review_not_regular_blob")
    raw = freeze.git_bytes(root, "cat-file", "blob", match[1].decode())
    if not raw:
        raise ValueError("empty_review_evidence")
    return raw


def _keys(value: object, keys: set[str]) -> json_shapes.JsonObject:
    if not json_shapes.is_object(value) or type(value) is not dict or set(value) != keys:
        raise ValueError("invalid_review_record")
    return value


def _record(root: Path, review_commit: str) -> tuple[ReviewRecord, str]:
    raw = committed_blob(root, review_commit, REVIEW_PATH)
    try:
        value = _keys(
            json.loads(raw, object_pairs_hook=unique_object_pairs),
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
        source = value["source_commit"]
        if type(source) is not str or re.fullmatch(r"[0-9a-f]{40}", source) is None:
            raise ValueError("invalid_review_record")
        for key in ("protocol_sha256", "adapter_sha256", "closure_sha256", "environment_sha256"):
            if not is_sha256(value[key]):
                raise ValueError("invalid_review_record")
        reviewers = value["reviewers"]
        if not json_shapes.is_array(reviewers) or len(reviewers) != 3:
            raise ValueError("invalid_review_record")
        roles: set[ReviewRole] = set()
        ids: set[str] = set()
        paths: set[str] = set()
        for item in reviewers:
            reviewer = _keys(
                item, {"role", "reviewer_id", "outcome", "evidence_path", "evidence_sha256"}
            )
            if not _is_reviewer(reviewer):
                raise ValueError("invalid_review_record")
            name = reviewer["reviewer_id"]
            path = reviewer["evidence_path"]
            if (
                not 1 <= len(name) <= 200
                or len(path) > 200
                or not path.startswith("conductor/reviews/evidence/")
                or not is_sha256(reviewer["evidence_sha256"])
            ):
                raise ValueError("invalid_review_record")
            evidence = committed_blob(root, review_commit, path)
            if hashlib.sha256(evidence).hexdigest() != reviewer["evidence_sha256"]:
                raise ValueError("review_evidence_mismatch")
            envelope = _keys(
                json.loads(evidence, object_pairs_hook=unique_object_pairs),
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
            if not _is_review_envelope(envelope):
                raise ValueError("review_evidence_scope_mismatch")
            for key in ("role", "reviewer_id", "outcome"):
                if envelope[key] != reviewer[key]:
                    raise ValueError("review_evidence_scope_mismatch")
            for key in ("source_commit", "protocol_sha256", "closure_sha256", "environment_sha256"):
                if envelope[key] != value[key]:
                    raise ValueError("review_evidence_scope_mismatch")
            if envelope["unresolved_findings"] or not 1 <= len(envelope["evidence_locator"]) <= 500:
                raise ValueError("review_evidence_scope_mismatch")
            roles.add(reviewer["role"])
            ids.add(name)
            paths.add(path)
        if len(roles) != 3 or len(ids) != 3 or len(paths) != 3:
            raise ValueError("invalid_review_record")
        canonical_bytes(value)
        if not _is_review_record(value):
            raise ValueError("invalid_review_record")
    except (TypeError, KeyError, UnicodeError, RecursionError):
        raise ValueError("invalid_review_record") from None
    return value, hashlib.sha256(raw).hexdigest()


def verify_execution_plan(
    protocol_path: Path,
    pin: str,
    slot_id: object,
    review_commit: object,
    root: Path,
    model_root: Path,
) -> ExecutionPlan:
    if (platform.system(), platform.machine()) != ("Darwin", "arm64"):
        raise ValueError("unsupported_primary_platform")
    if type(review_commit) is not str or ".." in protocol_path.parts:
        raise ValueError("invalid_gate_path_or_commit")
    root, protocol_path, relative = freeze.resolve_repository(protocol_path, review_commit, root)
    record, review_pin = _record(root, review_commit)
    source = record["source_commit"]
    if source == review_commit:
        raise ValueError("review_must_follow_source")
    freeze.git_bytes(root, "merge-base", "--is-ancestor", source, review_commit)
    value, candidate = native.validated_candidate(protocol_path, pin)
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
    files = freeze.committed_files(root, source, paths, expected)
    if freeze.committed_files(root, review_commit, paths, expected) != files:
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
    evidence: ExecutionEvidence = {
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
    result: ExecutionPlanValue = {
        "request": candidate["requests"][slot_id],
        "admission": admission,
        "evidence": evidence,
    }
    return ExecutionPlan(canonical_bytes(result))
