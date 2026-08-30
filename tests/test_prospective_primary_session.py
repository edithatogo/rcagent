"""Primary gate composition uses synthetic sockets, never real model eligibility."""

import json
import os
import sys

import pytest

from tests.test_native_completion import response
from tests.test_prospective_execution_gate import REAL_FILES, REAL_GIT, commit_review
from tests.test_prospective_execution_gate import synthetic as _gate_fixture
from tests.test_prospective_protocol import pin
from tests.test_prospective_server_session import synthetic as _session_fixture
from tools import prospective_primary_session as primary

session_fixture = _session_fixture
gate_fixture = _gate_fixture


@pytest.fixture
def synthetic(session_fixture, monkeypatch):
    root, receipt, calls, processes, admission = session_fixture
    request = primary.runner.build_request(b"Synthetic primary {{INPUT}}", b"case input")
    evidence = {
        "slot_id": "case-a__condition-local__r1",
        "admitted": False,
        "study_unlocked": False,
        "execution_permitted": True,
    }
    plan = primary.gate._Plan(
        primary.gate._canonical({"request": request, "admission": admission, "evidence": evidence})
    )
    checks = []

    def verify(*args):
        checks.append(args)
        return plan

    monkeypatch.setattr(primary.gate, "_verify", verify)
    return root, receipt, calls, processes, plan, checks


def run(fixture):
    root, receipt, *_ = fixture
    return primary.run_primary(
        root / "protocol.json",
        "a" * 64,
        "case-a__condition-local__r1",
        "b" * 40,
        root,
        root,
        receipt,
    )


def test_primary_uses_exact_selected_request_and_persists_candidate(synthetic):
    root, receipt, calls, processes, plan, checks = synthetic
    result = run(synthetic)
    assert result["status"] == "primary_session_captured"
    assert len(checks) == 3
    assert len(processes) == 1
    request = plan.value()["request"]
    assert calls[-1][3] != primary.session.REQUEST
    assert result["request_sha256"] == request["request"]["sha256"]
    assert result["candidate"]["request"] == request
    assert result["admitted"] is result["study_unlocked"] is False
    assert result["worker_joined"] and result["resources_removed"]
    assert json.loads(receipt.read_bytes()) == result


@pytest.mark.parametrize("stage", [1, 2])
def test_gate_failure_prevents_all_session_resources(synthetic, monkeypatch, stage):
    root, receipt, _, processes, plan, _ = synthetic
    count = 0

    def verify(*args):
        nonlocal count
        count += 1
        if count == stage:
            raise ValueError("synthetic_gate_failure")
        return plan

    monkeypatch.setattr(primary.gate, "_verify", verify)

    def forbidden(*args, **kwargs):
        raise AssertionError("No session resources before both gates pass")

    monkeypatch.setattr(primary.session.tempfile, "mkdtemp", forbidden)
    monkeypatch.setattr(primary.session.os, "open", forbidden)
    monkeypatch.setattr(primary.session.threading, "Thread", forbidden)
    with pytest.raises(ValueError, match="synthetic_gate_failure"):
        run(synthetic)
    assert not receipt.exists() and not processes


def test_changed_plan_prevents_reservation(synthetic, monkeypatch):
    _, receipt, _, processes, plan, _ = synthetic
    changed = plan.value()
    changed["evidence"]["review_commit"] = "different"
    results = iter([plan, primary.gate._Plan(primary.gate._canonical(changed))])
    monkeypatch.setattr(primary.gate, "_verify", lambda *args: next(results))
    with pytest.raises(ValueError, match="primary_gate_changed"):
        run(synthetic)
    assert not receipt.exists() and not processes


@pytest.mark.parametrize(
    "failure",
    [ValueError("drift"), ImportError("missing dependency"), KeyboardInterrupt(), SystemExit()],
    ids=["identity-drift", "missing-package", "interrupt", "exit"],
)
def test_postflight_failure_retains_raw_capture(synthetic, monkeypatch, failure):
    _, receipt, _, _, plan, _ = synthetic
    count = 0

    def verify(*args):
        nonlocal count
        count += 1
        if count == 3:
            raise failure
        return plan

    monkeypatch.setattr(primary.gate, "_verify", verify)
    result = run(synthetic)
    assert result["error"] == "primary_postflight_failed"
    assert result["status"] == "session_failed"
    assert result["process"]["reaped"] and result["worker_joined"]
    assert result["completion"]["body_base64"]
    assert json.loads(receipt.read_bytes()) == result


def test_primary_failure_never_masks_http_or_cleanup_failure(synthetic, monkeypatch):
    _, receipt, _, _, plan, _ = synthetic
    capture = primary.session.transport.capture

    def failed_http(*args, **kwargs):
        value = capture(*args, **kwargs)
        if args[2] == "/completion":
            value["status"] = "transport_failed"
        return value

    monkeypatch.setattr(primary.session.transport, "capture", failed_http)
    count = 0

    def verify(*args):
        nonlocal count
        count += 1
        if count == 3:
            raise ValueError("postflight")
        return plan

    monkeypatch.setattr(primary.gate, "_verify", verify)
    result = run(synthetic)
    assert result["error"] == "completion_transport_failed"
    assert result["primary_postflight_error"] == "primary_postflight_failed"
    assert result["process"]["reaped"]
    assert json.loads(receipt.read_bytes()) == result


def test_primary_and_ready_share_lock(synthetic):
    _, receipt, _, processes, _, _ = synthetic
    assert primary.session._LOCK.acquire(blocking=False)
    try:
        with pytest.raises(ValueError, match="session_already_running"):
            run(synthetic)
    finally:
        primary.session._LOCK.release()
    assert not receipt.exists() and not processes


def test_http_failure_with_successful_gate_stays_failed(synthetic, monkeypatch):
    capture = primary.session.transport.capture

    def failed(*args, **kwargs):
        result = capture(*args, **kwargs)
        if args[2] == "/completion":
            result["status"] = "transport_failed"
        return result

    monkeypatch.setattr(primary.session.transport, "capture", failed)
    result = run(synthetic)
    assert result["error"] == "completion_transport_failed"
    assert "candidate" not in result and "primary_postflight_error" not in result
    assert result["process"]["reaped"]


def test_cleanup_failure_and_postflight_failure_both_retained(synthetic, monkeypatch):
    _, receipt, _, _, plan, _ = synthetic

    def fail_cleanup(*args):
        raise OSError("synthetic cleanup failure")

    monkeypatch.setattr(primary.session, "_remove_owned", fail_cleanup)
    count = 0

    def verify(*args):
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
        assert "socket_resources_preserved" in result["cleanup_errors"]
        assert result["worker_joined"] and result["process"]["reaped"]
        assert json.loads(receipt.read_bytes()) == result
    finally:
        from pathlib import Path

        socket_path = Path(result["socket_path"])
        socket_path.unlink()
        socket_path.parent.rmdir()


def test_primary_circuit_breaker_blocks_before_reservation(synthetic, monkeypatch):
    _, receipt, _, processes, _, _ = synthetic
    monkeypatch.setattr(primary.session, "_BLOCKED", True)
    with pytest.raises(ValueError, match="session_circuit_breaker"):
        run(synthetic)
    assert not receipt.exists() and not processes


def test_real_guarded_git_child_http_and_decoder_composition(gate_fixture, monkeypatch):
    """Only eligibility/profile/environment/import-origin are synthetic boundaries."""
    if os.name != "posix":
        pytest.skip("Real synthetic Unix child composition")
    root, path, value, _, _, _, _, admission = gate_fixture
    source, review = commit_review(gate_fixture)
    monkeypatch.setattr(primary.gate.freeze, "_git", REAL_GIT)
    monkeypatch.setattr(primary.gate.freeze, "_committed_files", REAL_FILES)
    admission["profile_sha256"] = value["condition"]["profile_sha256"]
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
    monkeypatch.setattr(
        primary.session.profile, "verify_loaded_images", lambda raw: ["/synthetic/server"]
    )
    body = response()
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
    monkeypatch.setattr(
        primary.session,
        "_fixed_arguments",
        lambda admission, socket_path: [
            sys.executable,
            "-c",
            script,
            str(socket_path),
            raw_body.hex(),
        ],
    )
    receipt = root / "synthetic-primary-receipt.json"
    result = primary.run_primary(
        path, pin(path), value["expected_slots"][0], review, root, root / "synthetic-cache", receipt
    )
    assert result["status"] == "primary_session_captured"
    assert result["primary_gate"]["source_commit"] == source
    assert result["candidate"]["decoded"]["content"] == body["content"]
    assert result["process"]["reaped"] and result["worker_joined"] and result["resources_removed"]
    assert result["admitted"] is result["study_unlocked"] is False
    # HTTP headers are tuples in memory and JSON arrays in retained receipts.
    assert json.loads(receipt.read_bytes()) == json.loads(json.dumps(result))
