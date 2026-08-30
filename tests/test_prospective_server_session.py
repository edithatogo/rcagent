"""Fixed-session integration fixtures never execute a model runtime."""

import base64
import hashlib
import json
import os
import socket
import sys
import threading
from pathlib import Path

import pytest

from tools import prospective_server_session as session

REAL_CAPTURE_CHILD = session.process.capture_child
REAL_HTTP_CAPTURE = session.transport.capture


def test_missing_imported_source_cannot_produce_pin_inventory(monkeypatch):
    monkeypatch.setattr(session.core, "__file__", None)
    with pytest.raises(ValueError, match="source_unavailable"):
        session.source_pins()


@pytest.mark.parametrize("field", ["body_bytes", "body_sha256"])
def test_transport_body_integrity_mismatch_rejected(field):
    raw = b"synthetic"
    receipt = {
        "body_base64": base64.b64encode(raw).decode(),
        "body_bytes": len(raw),
        "body_sha256": hashlib.sha256(raw).hexdigest(),
    }
    receipt[field] = 0 if field == "body_bytes" else "0" * 64
    with pytest.raises(ValueError, match="transport_body_mismatch"):
        session._body(receipt)


def test_concurrent_session_rejected_before_receipt_creation(tmp_path):
    receipt = tmp_path / "receipt.json"
    assert session._LOCK.acquire(blocking=False)
    try:
        with pytest.raises(ValueError, match="session_already_running"):
            session.capture_session(tmp_path, receipt)
    finally:
        session._LOCK.release()
    assert not receipt.exists()


def test_private_directory_and_cleanup_identity_guards(tmp_path):
    if os.name != "posix":
        pytest.skip("POSIX ownership and mode guards")
    directory = tmp_path.resolve() / "private"
    directory.mkdir(mode=0o700)
    identity = session._directory(directory)
    alias = tmp_path / "alias"
    alias.symlink_to(directory, target_is_directory=True)
    with pytest.raises(ValueError, match="unsafe_session_directory"):
        session._directory(alias)
    directory.chmod(0o755)
    with pytest.raises(ValueError, match="unsafe_session_directory"):
        session._directory(directory)
    directory.chmod(0o700)
    with pytest.raises(ValueError, match="session_directory_changed"):
        session._remove_owned(directory / "server.sock", (identity[0], identity[1] + 1), None)
    assert directory.is_dir()
    assert alias.is_symlink()


def unix_socket():
    family = getattr(socket, "AF_UNIX", None)
    if family is None:
        raise RuntimeError("Unix sockets unavailable in this fixture")
    return socket.socket(family, socket.SOCK_STREAM)


def test_source_pin_inventory_matches_repository_bytes():
    pins = session.source_pins()
    assert set(pins) == {
        "prospective_server_session.py",
        "darwin_runtime_profile.py",
        "darwin_runtime_v030.py",
        "darwin_server_v030.py",
        "prospective_server_model.py",
        "prospective_model.py",
        "prospective_protocol.py",
        "prospective_inventory.py",
        "evaluation_preflight.py",
        "local_model_comparator.py",
        "server_process.py",
        "unix_http_capture.py",
        "native_completion.py",
    }
    for digest in pins.values():
        assert len(digest) == 64
        int(digest, 16)
    assert (
        pins["server_process.py"]
        == hashlib.sha256(Path(session.process.__file__).read_bytes()).hexdigest()
    )
    assert (
        pins["prospective_server_session.py"]
        == hashlib.sha256(Path(session.__file__).read_bytes()).hexdigest()
    )


@pytest.fixture
def synthetic(tmp_path, monkeypatch):
    if os.name != "posix":
        pytest.skip("Unix session composition")
    monkeypatch.setattr(session, "_BLOCKED", False)
    monkeypatch.setattr(session.platform, "system", lambda: "Darwin")
    monkeypatch.setattr(session.platform, "machine", lambda: "arm64")
    root = tmp_path.resolve()
    admission = {
        "admission_sha256": "a" * 64,
        "model_path": str(root / "synthetic-model.gguf"),
        "model_id": "synthetic-model",
        "profile_sha256": "b" * 64,
    }
    monkeypatch.setattr(session.model, "admit_model", lambda root: dict(admission))
    monkeypatch.setattr(session, "source_pins", lambda: {"fixture.py": "c" * 64})
    monkeypatch.setattr(session.profile, "profile_digest", lambda: "b" * 64)
    monkeypatch.setattr(session.profile, "verify_loaded_images", lambda raw: ["/synthetic/server"])
    monkeypatch.setattr(
        session.profile, "profile_environment", lambda: {"PATH": "/usr/bin:/bin", "LANG": "C"}
    )
    monkeypatch.setattr(session.profile, "EXECUTABLE", "/synthetic/server")
    monkeypatch.setattr(
        session.native,
        "decode_completion",
        lambda raw, expected_model: {
            "status": "native_completion_consistent",
            "admitted": False,
            "study_unlocked": False,
        },
    )
    calls = []
    processes = []

    def capture_child(argv, environment, *, deadline, stop_event, cancel, **kwargs):
        processes.append((argv, environment, deadline))
        path = Path(argv[argv.index("--host") + 1])
        with unix_socket() as listener:
            listener.bind(str(path))
            while not stop_event.wait(0.01) and not cancel.is_set():
                pass
        raw = b"dyld[123]: <12345678-1234-1234-1234-123456789ABC> /synthetic/server\n"
        return {
            "status": "process_stopped",
            "error": "none",
            "pid": 123,
            "reaped": True,
            "cleanup_errors": [],
            "stdout_complete": True,
            "stderr_complete": True,
            "raw_stderr_base64": base64.b64encode(raw).decode(),
            "admitted": False,
            "study_unlocked": False,
        }

    def capture(path, method, route, body, *, deadline):
        calls.append((path, method, route, body, deadline))
        raw = b'{"status":"ok"}' if route == "/health" else b'{"synthetic":"completion"}'
        return {
            "status": "http_response_captured",
            "error": "none",
            "http_status": 200,
            "body_complete": True,
            "body_base64": base64.b64encode(raw).decode(),
            "body_sha256": hashlib.sha256(raw).hexdigest(),
            "body_bytes": len(raw),
            "request_body_sha256": hashlib.sha256(body).hexdigest(),
            "headers": [],
            "admitted": False,
            "study_unlocked": False,
        }

    monkeypatch.setattr(session.process, "capture_child", capture_child)
    monkeypatch.setattr(session.transport, "capture", capture)
    return root, root / "receipt.json", calls, processes, admission


def test_fixed_session_reserved_and_locked(synthetic):
    root, receipt, calls, processes, _ = synthetic
    result = session.capture_session(root, receipt)
    assert result["status"] == "session_captured"
    assert result["admitted"] is result["study_unlocked"] is False
    assert result["worker_joined"] is True
    assert result["resources_removed"] is True
    assert json.loads(receipt.read_bytes()) == result
    assert receipt.stat().st_mode & 0o777 == 0o600
    assert [call[2] for call in calls] == ["/health", "/completion"]
    argv, env, deadline = processes[0]
    assert "--offline" in argv and "--no-agent" in argv and "--no-ui-mcp-proxy" in argv
    assert argv[argv.index("--ctx-size") + 1] == "2048"
    assert argv[argv.index("--parallel") + 1] == "1"
    assert calls[-1][-1] == deadline
    assert json.loads(calls[-1][3])["prompt"] == session.PROMPT
    assert env == {"PATH": "/usr/bin:/bin", "LANG": "C"}


def test_receipt_exists_never_launches(synthetic):
    root, receipt, _, processes, _ = synthetic
    receipt.write_bytes(b"preserve")
    with pytest.raises(ValueError):
        session.capture_session(root, receipt)
    assert receipt.read_bytes() == b"preserve"
    assert not processes


def test_unsupported_platform_does_not_launch(synthetic, monkeypatch):
    root, receipt, _, processes, _ = synthetic
    monkeypatch.setattr(session.platform, "system", lambda: "Linux")
    assert session.capture_session(root, receipt)["error"] == "unsupported_platform"
    assert not processes


def test_preflight_profile_disagreement_never_launches(synthetic):
    root, receipt, calls, processes, admission = synthetic
    admission["profile_sha256"] = "d" * 64
    result = session.capture_session(root, receipt)
    assert result["error"] == "profile_identity_mismatch"
    assert result["status"] == "session_failed"
    assert result["admitted"] is result["study_unlocked"] is False
    assert not calls and not processes


def test_health_attempt_budget_stops_without_completion(synthetic, monkeypatch):
    root, receipt, calls, _, _ = synthetic
    original = session.transport.capture

    def loading(*args, **kwargs):
        value = original(*args, **kwargs)
        value.update(status="transport_failed", http_status=503)
        return value

    monkeypatch.setattr(session, "HEALTH_ATTEMPTS", 1)
    monkeypatch.setattr(session.transport, "capture", loading)
    result = session.capture_session(root, receipt)
    assert result["error"] == "health_attempts_exhausted"
    assert result["status"] == "session_failed"
    assert [call[2] for call in calls] == ["/health"]
    assert result["worker_joined"] and result["process"]["reaped"]
    assert result["resources_removed"]


def test_interrupted_health_keeps_failure_after_worker_cleanup(synthetic, monkeypatch):
    root, receipt, _, _, _ = synthetic

    def interrupted(*args, **kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr(session.transport, "capture", interrupted)
    result = session.capture_session(root, receipt)
    assert result["error"] == "session_interrupted"
    assert result["failure_stage"] == "readiness_failed"
    assert result["status"] == "session_failed"
    assert result["worker_joined"] and result["process"]["reaped"]
    assert result["resources_removed"]
    assert result["admitted"] is result["study_unlocked"] is False


@pytest.mark.parametrize("damage", ["duplicate", "malformed", "status", "oversize", "http"])
def test_bad_health_cannot_be_replaced_by_later_success(synthetic, monkeypatch, damage):
    root, receipt, calls, _, _ = synthetic
    original = session.transport.capture

    def capture(*args, **kwargs):
        value = original(*args, **kwargs)
        raw = {
            "duplicate": b'{"status":"bad","status":"ok"}',
            "malformed": b"{",
            "status": b'{"status":"wrong"}',
            "oversize": b" " * 4097,
            "http": b'{"error":"bad"}',
        }[damage]
        value.update(
            body_base64=base64.b64encode(raw).decode(),
            body_bytes=len(raw),
            body_sha256=hashlib.sha256(raw).hexdigest(),
        )
        if damage == "http":
            value.update(status="transport_failed", http_status=500)
        return value

    monkeypatch.setattr(session.transport, "capture", capture)
    result = session.capture_session(root, receipt)
    assert result["status"] == "session_failed"
    assert len(calls) == 1
    assert result["process"]["status"] == "process_stopped"


def test_loading_health_retries_on_same_socket(synthetic, monkeypatch):
    root, receipt, calls, _, _ = synthetic
    original = session.transport.capture

    def capture(*args, **kwargs):
        value = original(*args, **kwargs)
        if len(calls) == 1:
            value.update(status="transport_failed", http_status=503)
        return value

    monkeypatch.setattr(session.transport, "capture", capture)
    assert session.capture_session(root, receipt)["status"] == "session_captured"
    assert [call[2] for call in calls] == ["/health", "/health", "/completion"]


def test_completion_failure_is_not_erased_by_successful_stop(synthetic, monkeypatch):
    root, receipt, _, _, _ = synthetic
    original = session.transport.capture

    def capture(path, method, route, body, **kwargs):
        value = original(path, method, route, body, **kwargs)
        if route == "/completion":
            value.update(status="transport_failed", http_status=500)
        return value

    monkeypatch.setattr(session.transport, "capture", capture)
    result = session.capture_session(root, receipt)
    assert result["error"] == "completion_transport_failed"
    assert result["process"]["status"] == "process_stopped"


@pytest.mark.parametrize("damage", ["pid", "logs", "admission", "source", "profile", "decode"])
def test_final_evidence_gaps_fail_closed(synthetic, monkeypatch, damage):
    root, receipt, _, _, admission = synthetic
    original = session.process.capture_child
    original_transport = session.transport.capture

    def capture_child(*args, **kwargs):
        value = original(*args, **kwargs)
        if damage == "pid":
            value["pid"] = 999
        elif damage == "logs":
            value["stderr_complete"] = False
        return value

    def capture(*args, **kwargs):
        value = original_transport(*args, **kwargs)
        if args[2] == "/completion":
            if damage == "admission":
                admission["admission_sha256"] = "changed"
            elif damage == "source":
                monkeypatch.setattr(session, "source_pins", lambda: {"changed": "d" * 64})
            elif damage == "profile":
                monkeypatch.setattr(session.profile, "profile_digest", lambda: "changed")
        return value

    monkeypatch.setattr(session.process, "capture_child", capture_child)
    monkeypatch.setattr(session.transport, "capture", capture)
    if damage == "decode":

        def reject(*args, **kwargs):
            raise ValueError("incomplete_generation")

        monkeypatch.setattr(session.native, "decode_completion", reject)
    result = session.capture_session(root, receipt)
    assert result["status"] == "session_failed"
    assert result["admitted"] is result["study_unlocked"] is False


def test_worker_exception_preserves_resources_and_blocks_replacement(synthetic, monkeypatch):
    root, receipt, _, _, _ = synthetic

    def fail(*args, **kwargs):
        raise RuntimeError("private-exception")

    monkeypatch.setattr(session.process, "capture_child", fail)
    result = session.capture_session(root, receipt)
    assert result["worker_error"] == "worker_exception"
    assert result["resources_removed"] is False
    assert "private-exception" not in json.dumps(result)
    with pytest.raises(ValueError, match="circuit_breaker"):
        session.capture_session(root, root / "second.json")
    Path(result["socket_path"]).parent.rmdir()  # Empty fixture directory; no child existed.


def test_start_that_launches_then_raises_is_joined_before_cleanup(synthetic, monkeypatch):
    root, receipt, _, _, _ = synthetic
    original = threading.Thread.start

    def start(worker):
        original(worker)
        raise RuntimeError("synthetic start error")

    monkeypatch.setattr(session.threading.Thread, "start", start)
    result = session.capture_session(root, receipt)
    assert result["error"] == "worker_start_failed"
    assert result["worker_joined"] is True
    # A socket created after start failed was never observed/identified: preserve it.
    path = Path(result["socket_path"])
    if path.exists():
        path.unlink()
    if path.parent.exists():
        path.parent.rmdir()


def test_receipt_replacement_during_preflight_never_launches(synthetic, monkeypatch):
    root, receipt, _, processes, admission = synthetic

    def admit(root):
        receipt.rename(receipt.with_name("reserved.json"))
        receipt.write_bytes(b"replacement")
        return dict(admission)

    monkeypatch.setattr(session.model, "admit_model", admit)
    with pytest.raises(ValueError, match="receipt_identity_changed"):
        session.capture_session(root, receipt)
    reserved = json.loads(receipt.with_name("reserved.json").read_bytes())
    assert reserved["error"] == "receipt_identity_changed"
    assert not processes
    assert receipt.read_bytes() == b"replacement"


def test_socket_replacement_between_health_and_completion_is_rejected(synthetic, monkeypatch):
    root, receipt, calls, _, _ = synthetic
    original = session.transport.capture
    replacement = unix_socket()

    def capture(path, *args, **kwargs):
        value = original(path, *args, **kwargs)
        if args[1] == "/health":
            path.unlink()
            replacement.bind(str(path))
        return value

    monkeypatch.setattr(session.transport, "capture", capture)
    try:
        result = session.capture_session(root, receipt)
    finally:
        replacement.close()
    assert result["error"] == "session_socket_changed"
    assert len(calls) == 1
    assert result["resources_removed"] is False
    path = Path(result["socket_path"])
    path.unlink()
    path.parent.rmdir()


def test_real_synthetic_child_http_and_graceful_stop(synthetic, monkeypatch):
    # Profile/eligibility and decoder remain labelled fixtures, while process,
    # worker, HTTP framing, Unix socket and TERM-drain composition execute for real.
    root, receipt, _, _, _ = synthetic
    # The fixture patched module globals; restore functions from explicitly saved
    # unpatched references below rather than importing those patched attributes.
    monkeypatch.setattr(session.process, "capture_child", REAL_CAPTURE_CHILD)
    monkeypatch.setattr(session.transport, "capture", REAL_HTTP_CAPTURE)
    script = """import os,signal,socket,sys
path=sys.argv[1]
print('dyld[%s]: <12345678-1234-1234-1234-123456789ABC> /synthetic/server'%os.getpid(),file=sys.stderr,flush=True)
def stop(*args): raise SystemExit(0)
signal.signal(signal.SIGTERM,stop)
with socket.socket(socket.AF_UNIX,socket.SOCK_STREAM) as listener:
 listener.bind(path); listener.listen(2)
 while True:
  conn,_=listener.accept()
  with conn:
   request=b''
   while b'\\r\\n\\r\\n' not in request: request+=conn.recv(4096)
   headers,payload=request.split(b'\\r\\n\\r\\n',1)
   length=next((int(line.split(b':',1)[1]) for line in headers.split(b'\\r\\n') if line.lower().startswith(b'content-length:')),0)
   while len(payload)<length: payload+=conn.recv(length-len(payload))
   body=b'{"status":"ok"}' if request.startswith(b'GET ') else b'{"synthetic":"completion"}'
   conn.sendall(b'HTTP/1.1 200 OK\\r\\nContent-Type: application/json\\r\\nContent-Length: '+str(len(body)).encode()+b'\\r\\n\\r\\n'+body)
"""
    monkeypatch.setattr(
        session,
        "_fixed_arguments",
        lambda admission, path: [str(Path(sys.executable).resolve()), "-c", script, str(path)],
    )
    result = session.capture_session(root, receipt)
    assert result["status"] == "session_captured"
    assert result["process"]["reaped"] is True
    assert result["process"]["stop_started"] is True
    assert result["resources_removed"] is True


def test_delayed_socket_creation_does_not_consume_health_attempts(synthetic, monkeypatch):
    root, receipt, calls, _, _ = synthetic
    original = session.process.capture_child

    def delayed(*args, **kwargs):
        threading.Event().wait(0.25)
        return original(*args, **kwargs)

    monkeypatch.setattr(session.process, "capture_child", delayed)
    monkeypatch.setattr(session, "HEALTH_ATTEMPTS", 1)
    assert session.capture_session(root, receipt)["status"] == "session_captured"
    assert len(calls) == 2


def test_completion_request_hash_mismatch_rejected(synthetic, monkeypatch):
    root, receipt, _, _, _ = synthetic
    original = session.transport.capture

    def capture(*args, **kwargs):
        value = original(*args, **kwargs)
        if args[2] == "/completion":
            value["request_body_sha256"] = "changed"
        return value

    monkeypatch.setattr(session.transport, "capture", capture)
    assert session.capture_session(root, receipt)["error"] == "completion_request_mismatch"


def test_worker_join_failure_preserves_paths_and_blocks_next_run(synthetic, monkeypatch):
    root, receipt, _, _, _ = synthetic
    original = session.process.capture_child
    release = threading.Event()
    workers = []

    def capture(*args, **kwargs):
        workers.append(threading.current_thread())
        value = original(*args, **kwargs)
        release.wait(5)
        return value

    monkeypatch.setattr(session.process, "capture_child", capture)
    monkeypatch.setattr(session, "JOIN_SECONDS", 0.01)
    try:
        result = session.capture_session(root, receipt)
        assert result["worker_joined"] is False
        assert result["resources_removed"] is False
        assert "worker_join_failed" in result["cleanup_errors"]
        with pytest.raises(ValueError, match="circuit_breaker"):
            session.capture_session(root, root / "second.json")
    finally:
        release.set()
        for worker in workers:
            worker.join(5)
            assert not worker.is_alive()
    path = Path(result["socket_path"])
    path.unlink()
    path.parent.rmdir()


def test_unexpected_directory_content_is_not_recursively_removed(synthetic, monkeypatch):
    root, receipt, _, _, _ = synthetic
    original = session.transport.capture

    def capture(path, *args, **kwargs):
        value = original(path, *args, **kwargs)
        (path.parent / "unexpected.txt").write_bytes(b"preserve")
        return value

    monkeypatch.setattr(session.transport, "capture", capture)
    result = session.capture_session(root, receipt)
    assert result["status"] == "session_failed"
    assert result["resources_removed"] is False
    directory = Path(result["socket_path"]).parent
    assert (directory / "unexpected.txt").read_bytes() == b"preserve"
    (directory / "unexpected.txt").unlink()
    directory.rmdir()


@pytest.mark.parametrize("failure", ["write", "flush", "close"])
def test_receipt_persistence_failure_never_returns_success(synthetic, monkeypatch, failure):
    root, receipt, _, _, _ = synthetic
    original = os.fdopen

    class Stream:
        def __init__(self, value):
            self.value = value

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.value.close()
            if failure == "close":
                raise OSError("private storage failure")

        def write(self, value):
            if failure == "write":
                raise OSError("private storage failure")
            return self.value.write(value)

        def flush(self):
            if failure == "flush":
                raise OSError("private storage failure")
            self.value.flush()

    monkeypatch.setattr(
        session.os, "fdopen", lambda *args, **kwargs: Stream(original(*args, **kwargs))
    )
    with pytest.raises(ValueError, match="^receipt_persistence_failed$"):
        session.capture_session(root, receipt)


@pytest.mark.parametrize("kind", ["symlink", "traversal", "missing-parent"])
def test_unsafe_receipt_rejected_before_any_launch(synthetic, kind):
    root, receipt, _, processes, _ = synthetic
    if kind == "symlink":
        receipt.symlink_to(root / "absent")
    elif kind == "traversal":
        (root / "nested").mkdir()
        receipt = root / "nested" / ".." / "receipt.json"
    else:
        receipt = root / "absent" / "receipt.json"
    with pytest.raises((ValueError, OSError)):
        session.capture_session(root, receipt)
    assert not processes


def test_shared_deadline_expiry_stops_readiness_without_completion(synthetic, monkeypatch):
    root, receipt, calls, _, _ = synthetic
    original = session.transport.capture

    def capture(*args, **kwargs):
        value = original(*args, **kwargs)
        value.update(status="transport_failed", http_status=503)
        return value

    monkeypatch.setattr(session.transport, "capture", capture)
    monkeypatch.setattr(session, "TIMEOUT", 0.2)
    result = session.capture_session(root, receipt)
    assert result["status"] == "session_failed"
    assert result["error"] == "session_deadline_exceeded"
    assert all(call[2] == "/health" for call in calls)


def test_receipt_parent_replacement_during_open_never_launches(synthetic, monkeypatch):
    root, _, _, processes, _ = synthetic
    parent = root / "receipt-parent"
    parent.mkdir()
    destination = parent / "receipt.json"
    original = os.open
    preserved = root / "preserved-parent"

    def open_file(path, *args, **kwargs):
        descriptor = original(path, *args, **kwargs)
        if Path(path) == destination:
            parent.rename(preserved)
            parent.mkdir()
        return descriptor

    monkeypatch.setattr(session.os, "open", open_file)
    with pytest.raises(ValueError, match="receipt_persistence_failed"):
        session.capture_session(root, destination)
    assert not processes
    assert (preserved / "receipt.json").read_bytes() == b""
    assert not destination.exists()


def test_receipt_replacement_during_flush_prevents_positive_return(synthetic, monkeypatch):
    root, receipt, _, _, _ = synthetic
    original = os.fdopen
    preserved = root / "reserved-old.json"

    class Stream:
        def __init__(self, value):
            self.value = value

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.value.close()

        def write(self, data):
            return self.value.write(data)

        def flush(self):
            self.value.flush()
            receipt.rename(preserved)
            receipt.write_bytes(b"replacement")

    monkeypatch.setattr(
        session.os, "fdopen", lambda *args, **kwargs: Stream(original(*args, **kwargs))
    )
    with pytest.raises(ValueError, match="receipt_identity_changed"):
        session.capture_session(root, receipt)
    assert receipt.read_bytes() == b"replacement"
    assert json.loads(preserved.read_bytes())["admitted"] is False
