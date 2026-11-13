"""Primary gate composition uses synthetic sockets, never real model eligibility."""

import json
import os
import sys
from pathlib import Path
from typing import Unpack

import pytest

from tests.prospective_fixture_types import (
    GateFixture,
    HttpArgs,
    HttpCapture,
    HttpOptions,
    ObjectMap,
    Plan,
    PrimaryFixture,
    SessionFixture,
    VerifyArgs,
    mapping,
    sequence,
    text_value,
)
from tests.test_native_completion import response
from tests.test_prospective_execution_gate import REAL_FILES, REAL_GIT, commit_review
from tests.test_prospective_execution_gate import synthetic as _gate_fixture
from tests.test_prospective_protocol import pin
from tests.test_prospective_server_session import synthetic as _session_fixture
from tools import prospective_primary_session as primary

session_fixture = _session_fixture
gate_fixture = _gate_fixture


@pytest.fixture
def synthetic(session_fixture: SessionFixture, monkeypatch: pytest.MonkeyPatch) -> PrimaryFixture:
    root, receipt, calls, processes, session_admission = session_fixture
    request = mapping(primary.runner.build_request(b"Synthetic primary {{INPUT}}", b"case input"))
    admission: primary.gate.model.ModelAdmission = {
        "purpose": "local-artefact-eligibility-only",
        "local_artifact_eligible": True,
        "admitted": False,
        "study_unlocked": False,
        "registry_sha256": "c" * 64,
        "effective_manifest_sha256": "d" * 64,
        "original_runtime": {"name": "synthetic-historical-cli"},
        "runtime_overlay": {
            "name": "synthetic-server",
            "version": "synthetic",
            "executable": "/synthetic/server",
            "executable_sha256": "e" * 64,
            "license": "MIT",
            "profile_id": "synthetic-profile",
            "profile_sha256": session_admission["profile_sha256"],
            "distribution": "synthetic",
            "runtime_dependencies": [],
        },
        "profile_id": "synthetic-profile",
        "profile_sha256": session_admission["profile_sha256"],
        "model_id": session_admission["model_id"],
        "model_revision": "synthetic-revision",
        "model_sha256": "f" * 64,
        "model_license_sha256": "a" * 64,
        "model_path": session_admission["model_path"],
        "model_license_path": str(root / "LICENSE"),
        "limitations": ["synthetic-fixture-not-actual-eligibility"],
        "admission_sha256": session_admission["admission_sha256"],
    }

    def admit_fixture(_root: Path) -> primary.gate.model.ModelAdmission:
        return admission.copy()

    monkeypatch.setattr(primary.session.model, "admit_model", admit_fixture)
    evidence: primary.gate.ExecutionEvidence = {
        "review_commit": "b" * 40,
        "source_commit": "c" * 40,
        "review_sha256": "d" * 64,
        "closure_sha256": "e" * 64,
        "environment_sha256": "f" * 64,
        "protocol_sha256": "a" * 64,
        "study_id": "synthetic-primary-study",
        "slot_id": "case-a__condition-local__r1",
        "adapter_sha256": "a" * 64,
        "admitted": False,
        "study_unlocked": False,
        "execution_permitted": True,
        "limitations": ["synthetic-fixture-not-actual-eligibility"],
    }
    plan: Plan = primary.gate._Plan(
        primary.gate._canonical({"request": request, "admission": admission, "evidence": evidence})
    )
    checks: list[VerifyArgs] = []

    def verify(*args: *VerifyArgs) -> Plan:
        checks.append(args)
        return plan

    monkeypatch.setattr(primary.gate, "_verify", verify)
    return root, receipt, calls, processes, plan, checks


def run(fixture: PrimaryFixture) -> ObjectMap:
    root, receipt, *_ = fixture
    return mapping(
        primary.run_primary(
            root / "protocol.json",
            "a" * 64,
            "case-a__condition-local__r1",
            "b" * 40,
            root,
            root,
            receipt,
        )
    )


def test_primary_uses_exact_selected_request_and_persists_candidate(
    synthetic: PrimaryFixture,
) -> None:
    _root, receipt, calls, processes, plan, checks = synthetic
    result = run(synthetic)
    assert result["status"] == "primary_session_captured"
    assert len(checks) == 3
    assert len(processes) == 1
    request = mapping(mapping(plan.value())["request"])
    assert calls[-1][3] != primary.session.REQUEST
    assert result["request_sha256"] == mapping(request["request"])["sha256"]
    assert mapping(result["candidate"])["request"] == request
    assert result["admitted"] is result["study_unlocked"] is False
    assert result["worker_joined"]
    assert result["resources_removed"]
    assert json.loads(receipt.read_bytes()) == result


@pytest.mark.parametrize("stage", [1, 2])
def test_gate_failure_prevents_all_session_resources(
    synthetic: PrimaryFixture, monkeypatch: pytest.MonkeyPatch, stage: int
) -> None:
    _root, receipt, _, processes, plan, _ = synthetic
    count = 0

    def verify(*args: *VerifyArgs) -> Plan:
        nonlocal count
        count += 1
        if count == stage:
            raise ValueError("synthetic_gate_failure")
        return plan

    monkeypatch.setattr(primary.gate, "_verify", verify)

    def forbidden(*args: object, **kwargs: object) -> None:
        raise AssertionError("No session resources before both gates pass")

    monkeypatch.setattr(primary.session.tempfile, "mkdtemp", forbidden)
    monkeypatch.setattr(primary.session.os, "open", forbidden)
    monkeypatch.setattr(primary.session.threading, "Thread", forbidden)
    with pytest.raises(ValueError, match="synthetic_gate_failure"):
        run(synthetic)
    assert not receipt.exists()
    assert not processes


def test_changed_plan_prevents_reservation(
    synthetic: PrimaryFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    _, receipt, _, processes, plan, _ = synthetic
    changed = mapping(plan.value())
    mapping(changed["evidence"])["review_commit"] = "different"
    results = iter([plan, primary.gate._Plan(primary.gate._canonical(changed))])

    def next_plan(*args: *VerifyArgs) -> Plan:
        return next(results)

    monkeypatch.setattr(primary.gate, "_verify", next_plan)
    with pytest.raises(ValueError, match="primary_gate_changed"):
        run(synthetic)
    assert not receipt.exists()
    assert not processes


@pytest.mark.parametrize(
    "failure",
    [ValueError("drift"), ImportError("missing dependency"), KeyboardInterrupt(), SystemExit()],
    ids=["identity-drift", "missing-package", "interrupt", "exit"],
)
def test_postflight_failure_retains_raw_capture(
    synthetic: PrimaryFixture, monkeypatch: pytest.MonkeyPatch, failure: BaseException
) -> None:
    _, receipt, _, _, plan, _ = synthetic
    count = 0

    def verify(*args: *VerifyArgs) -> Plan:
        nonlocal count
        count += 1
        if count == 3:
            raise failure
        return plan

    monkeypatch.setattr(primary.gate, "_verify", verify)
    result = run(synthetic)
    assert result["error"] == "primary_postflight_failed"
    assert result["status"] == "session_failed"
    assert mapping(result["process"])["reaped"]
    assert result["worker_joined"]
    assert mapping(result["completion"])["body_base64"]
    assert json.loads(receipt.read_bytes()) == result


def test_primary_failure_never_masks_http_or_cleanup_failure(
    synthetic: PrimaryFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    _, receipt, _, _, plan, _ = synthetic
    capture: HttpCapture = primary.session.transport.capture

    def failed_http(*args: *HttpArgs, **kwargs: Unpack[HttpOptions]) -> ObjectMap:
        value = mapping(capture(*args, **kwargs))
        if args[2] == "/completion":
            value["status"] = "transport_failed"
        return value

    monkeypatch.setattr(primary.session.transport, "capture", failed_http)
    count = 0

    def verify(*args: *VerifyArgs) -> Plan:
        nonlocal count
        count += 1
        if count == 3:
            raise ValueError("postflight")
        return plan

    monkeypatch.setattr(primary.gate, "_verify", verify)
    result = run(synthetic)
    assert result["error"] == "completion_transport_failed"
    assert result["primary_postflight_error"] == "primary_postflight_failed"
    assert mapping(result["process"])["reaped"]
    assert json.loads(receipt.read_bytes()) == result


def test_primary_and_ready_share_lock(synthetic: PrimaryFixture) -> None:
    _, receipt, _, processes, _, _ = synthetic
    assert primary.session._LOCK.acquire(blocking=False)
    try:
        with pytest.raises(ValueError, match="session_already_running"):
            run(synthetic)
    finally:
        primary.session._LOCK.release()
    assert not receipt.exists()
    assert not processes


def test_http_failure_with_successful_gate_stays_failed(
    synthetic: PrimaryFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    capture: HttpCapture = primary.session.transport.capture

    def failed(*args: *HttpArgs, **kwargs: Unpack[HttpOptions]) -> ObjectMap:
        result = mapping(capture(*args, **kwargs))
        if args[2] == "/completion":
            result["status"] = "transport_failed"
        return result

    monkeypatch.setattr(primary.session.transport, "capture", failed)
    result = run(synthetic)
    assert result["error"] == "completion_transport_failed"
    assert "candidate" not in result
    assert "primary_postflight_error" not in result
    assert mapping(result["process"])["reaped"]


def test_cleanup_failure_and_postflight_failure_both_retained(
    synthetic: PrimaryFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    _, receipt, _, _, plan, _ = synthetic

    def fail_cleanup(*args: object) -> None:
        raise OSError("synthetic cleanup failure")

    monkeypatch.setattr(primary.session, "_remove_owned", fail_cleanup)
    count = 0

    def verify(*args: *VerifyArgs) -> Plan:
        nonlocal count
        count += 1
        if count == 3:
            raise ValueError("synthetic postflight failure")
        return plan

    monkeypatch.setattr(primary.gate, "_verify", verify)
    result = run(synthetic)
    try:
        assert result["error"] == "postflight_failed"
        assert result["primary_postflight_error"] == "primary_postflight_failed"
        assert "socket_resources_preserved" in sequence(result["cleanup_errors"])
        assert result["worker_joined"]
        assert mapping(result["process"])["reaped"]
        assert json.loads(receipt.read_bytes()) == result
    finally:
        socket_path = Path(text_value(result["socket_path"]))
        socket_path.unlink()
        socket_path.parent.rmdir()


def test_primary_circuit_breaker_blocks_before_reservation(
    synthetic: PrimaryFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    _, receipt, _, processes, _, _ = synthetic
    monkeypatch.setattr(primary.session, "_BLOCKED", True)
    with pytest.raises(ValueError, match="session_circuit_breaker"):
        run(synthetic)
    assert not receipt.exists()
    assert not processes


def test_real_guarded_git_child_http_and_decoder_composition(
    gate_fixture: GateFixture, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Only eligibility/profile/environment/import-origin are synthetic boundaries."""
    if os.name != "posix":
        pytest.skip("Real synthetic Unix child composition")
    root, path, value, _, _, _, _, admission = gate_fixture
    source, review = commit_review(gate_fixture)
    monkeypatch.setattr(primary.gate.freeze, "_git", REAL_GIT)
    monkeypatch.setattr(primary.gate.freeze, "_committed_files", REAL_FILES)
    admission["profile_sha256"] = mapping(value["condition"])["profile_sha256"]
    monkeypatch.setattr(primary.session, "_BLOCKED", False)
    monkeypatch.setattr(primary.session, "source_pins", lambda: {"synthetic": "a" * 64})
    monkeypatch.setattr(
        primary.session.profile, "profile_digest", lambda: admission["profile_sha256"]
    )
    monkeypatch.setattr(
        primary.session.profile,
        "profile_environment",
        lambda: {"PATH": "/usr/bin:/bin", "LANG": "C"},
    )

    def loaded_images(raw: bytes) -> list[str]:
        return ["/synthetic/server"]

    monkeypatch.setattr(primary.session.profile, "verify_loaded_images", loaded_images)
    body = mapping(response())
    body["model"] = admission["model_id"]
    body["content"] = "Synthetic exact content\r\n"
    raw_body = json.dumps(body).encode()
    script = """
import os, signal, socket, sys
def stop(signum, frame):
    raise SystemExit(0)
signal.signal(signal.SIGTERM, stop)
sys.stderr.write('dyld[%d]: <12345678-1234-1234-1234-123456789ABC> /synthetic/server\\n' % os.getpid())
sys.stderr.flush()
listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
listener.bind(sys.argv[1])
listener.listen(2)
while True:
    connection, _ = listener.accept()
    with connection:
        data = b''
        while b'\\r\\n\\r\\n' not in data:
            data += connection.recv(4096)
        header, received = data.split(b'\\r\\n\\r\\n', 1)
        length = 0
        for line in header.split(b'\\r\\n')[1:]:
            if line.lower().startswith(b'content-length:'):
                length = int(line.split(b':', 1)[1])
        while len(received) < length:
            received += connection.recv(4096)
        payload = b'{"status":"ok"}' if header.startswith(b'GET /health ') else bytes.fromhex(sys.argv[2])
        connection.sendall(b'HTTP/1.1 200 OK\\r\\nContent-Type: application/json\\r\\nContent-Length: ' + str(len(payload)).encode() + b'\\r\\nConnection: close\\r\\n\\r\\n' + payload)
"""

    def arguments(admission: object, socket_path: Path) -> list[str]:
        return [sys.executable, "-c", script, str(socket_path), raw_body.hex()]

    monkeypatch.setattr(primary.session, "_fixed_arguments", arguments)
    receipt = root / "synthetic-primary-receipt.json"
    result = mapping(
        primary.run_primary(
            path,
            pin(path),
            text_value(sequence(value["expected_slots"])[0]),
            review,
            root,
            root / "synthetic-cache",
            receipt,
        )
    )
    assert result["status"] == "primary_session_captured"
    assert mapping(result["primary_gate"])["source_commit"] == source
    assert mapping(mapping(result["candidate"])["decoded"])["content"] == body["content"]
    assert mapping(result["process"])["reaped"]
    assert result["worker_joined"]
    assert result["resources_removed"]
    assert result["admitted"] is result["study_unlocked"] is False
    # HTTP headers are tuples in memory and JSON arrays in retained receipts.
    assert json.loads(receipt.read_bytes()) == json.loads(json.dumps(result))
