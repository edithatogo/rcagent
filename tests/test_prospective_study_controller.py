"""Synthetic controller mechanics do not produce actual study observations."""

import base64
import json
import os
import sys

import pytest

from tests.test_native_completion import response
from tests.test_prospective_execution_gate import R
from tests.test_prospective_execution_gate import synthetic as synthetic
from tests.test_prospective_protocol import pin
from tools import prospective_execution_gate as gate
from tools import prospective_observation_admission as admission
from tools import prospective_runner_contract as runner
from tools import prospective_server_session as session
from tools import prospective_study_controller as controller

REAL_PRIMARY = controller.primary.run_primary


def receipt_for(plan, socket_path):
    """Fabricated fixture bytes, never a production capture or study observation."""
    expected = plan.value()
    native = response()
    native["model"] = expected["admission"]["model_id"]
    body = json.dumps(native).encode()
    request = base64.b64decode(expected["request"]["request"]["base64"])
    candidate = runner.normalize_candidate(
        expected["request"],
        body,
        slot_id=expected["evidence"]["slot_id"],
        expected_slot_id=expected["evidence"]["slot_id"],
        expected_model=native["model"],
    )
    child = dict(
        status="process_stopped",
        error="none",
        execution_observed=True,
        reaped=True,
        cleanup_errors=[],
        pid=123,
        returncode=0,
    )
    for name, data in [
        ("stdout", b""),
        ("stderr", b"dyld[123]: <AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE> /synthetic/server\n"),
    ]:
        child.update(
            {
                f"raw_{name}_base64": base64.b64encode(data).decode(),
                f"{name}_complete": True,
                f"{name}_truncated": False,
                f"{name}_bytes_observed": len(data),
                f"{name}_bytes_retained": len(data),
                f"{name}_sha256": admission._sha(data),
                f"{name}_retained_sha256": admission._sha(data),
            }
        )
    environment = session.profile.profile_environment()
    health_body = b'{"status":"ok"}'
    return dict(
        status="primary_session_captured",
        error="none",
        admitted=False,
        study_unlocked=False,
        worker_joined=True,
        resources_removed=True,
        cleanup_errors=[],
        health=[
            dict(
                status="http_response_captured",
                error="none",
                http_status=200,
                body_complete=True,
                body_bytes=len(health_body),
                body_sha256=admission._sha(health_body),
                body_base64=base64.b64encode(health_body).decode(),
            )
        ],
        primary_gate=expected["evidence"],
        admission=expected["admission"],
        request_base64=base64.b64encode(request).decode(),
        request_sha256=admission._sha(request),
        completion=dict(
            status="http_response_captured",
            error="none",
            body_complete=True,
            http_status=200,
            method="POST",
            route="/completion",
            transport="unix-domain-socket",
            request_body_sha256=admission._sha(request),
            body_base64=base64.b64encode(body).decode(),
            body_bytes=len(body),
            body_sha256=admission._sha(body),
        ),
        candidate=candidate,
        decoded=candidate["decoded"],
        process=child,
        loaded_non_system_images=["/synthetic/server"],
        source_sha256=session.source_pins(),
        profile_sha256=session.profile.profile_digest(),
        socket_path=str(socket_path),
        arguments=session._fixed_arguments(expected["admission"], socket_path),
        environment_sha256=admission._sha(json.dumps(environment, sort_keys=True).encode()),
        environment_keys=sorted(environment),
    )


@pytest.fixture
def capture_fixture(synthetic, monkeypatch):
    if os.name != "posix":
        pytest.skip("owned POSIX mode/uid/directory fsync contract")
    root, path, value, *_ = synthetic
    synthetic[-1].update(model_path="/synthetic/model", profile_sha256="e" * 64)
    monkeypatch.setattr(session.profile, "profile_environment", lambda: {"PATH": "/usr/bin:/bin"})
    monkeypatch.setattr(session.profile, "profile_digest", lambda: "e" * 64)
    monkeypatch.setattr(session.profile, "verify_loaded_images", lambda _: ["/synthetic/server"])
    monkeypatch.setattr(session, "source_pins", lambda: {"synthetic": "f" * 64})
    evidence = root / "evidence"
    evidence.mkdir(mode=0o700)
    calls = []

    def capture(protocol, pinned, slot, review, repo, model_root, receipt):
        calls.append(slot)
        plan = gate._verify(protocol, pinned, slot, review, repo, model_root)
        result = receipt_for(plan, receipt.parent / "server.sock")
        fd = os.open(receipt, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, "wb") as stream:
            stream.write(admission._canonical(result) + b"\n")
        return result

    monkeypatch.setattr(controller.primary, "run_primary", capture)
    args = (path, pin(path), R, root, root / "synthetic-cache", evidence)
    return args, calls, capture


def test_two_slot_immediate_admission_and_no_resume(capture_fixture):
    args, calls, _ = capture_fixture
    result = controller.run_study(*args)
    assert result["status"] == "controller_admitted_before_blinding", result
    assert len(calls) == 2
    assert result["admitted"] is True
    assert result["study_unlocked"] is result["scoring_start"] is False
    with pytest.raises(FileExistsError):
        controller.run_study(*args)
    assert len(calls) == 2


@pytest.mark.parametrize("failure", [ValueError, KeyboardInterrupt, SystemExit])
def test_primary_exception_consumes_attempt_never_retries(capture_fixture, monkeypatch, failure):
    args, calls, _ = capture_fixture

    def fail(*parameters):
        calls.append(parameters[2])
        raise failure()

    monkeypatch.setattr(controller.primary, "run_primary", fail)
    result = controller.run_study(*args)
    assert result["admitted"] is False
    assert list(result["dispositions"].values()) == ["attempted-outcome-unknown", "not-attempted"]
    assert len(calls) == 1
    assert result["failure_stage"] == "capture"


@pytest.mark.parametrize("mutation", ["cleanup", "journal", "directory"])
def test_first_capture_damage_prevents_second(capture_fixture, monkeypatch, mutation):
    args, calls, capture = capture_fixture

    def damaged(*parameters):
        result = capture(*parameters)
        path = parameters[-1]
        if mutation == "cleanup":
            result["resources_removed"] = False
            path.write_bytes(admission._canonical(result))
        elif mutation == "journal":
            (path.parent / "journal.jsonl").write_bytes(b"corrupt")
        else:
            path.parent.chmod(0o755)
        return result

    monkeypatch.setattr(controller.primary, "run_primary", damaged)
    result = controller.run_study(*args)
    assert result["admitted"] is False
    assert len(calls) == 1


def test_two_real_synthetic_children_transport_and_admission(capture_fixture, monkeypatch):
    """Real process/HTTP/decoder/controller; Git/profile/model/origins/environment mocked."""
    args, _, _ = capture_fixture
    monkeypatch.setattr(controller.primary, "run_primary", REAL_PRIMARY)
    monkeypatch.setattr(session, "_BLOCKED", False)
    body = response()
    body["model"] = gate.model.MODEL_ID
    encoded = json.dumps(body).encode().hex()
    script = r"""
import os,signal,socket,sys
signal.signal(signal.SIGTERM,lambda *args: sys.exit(0))
print('dyld[%d]: <AAAAAAAA-BBBB-CCCC-DDDD-EEEEEEEEEEEE> /synthetic/server'%os.getpid(),file=sys.stderr,flush=True)
s=socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
s.bind(sys.argv[1]);s.listen(2)
while True:
 c,_=s.accept()
 with c:
  data=b''
  while b'\r\n\r\n' not in data: data+=c.recv(4096)
  header,content=data.split(b'\r\n\r\n',1)
  length=0
  for row in header.split(b'\r\n')[1:]:
   if row.lower().startswith(b'content-length:'): length=int(row.split(b':',1)[1])
  while len(content)<length: content+=c.recv(4096)
  body=b'{"status":"ok"}' if header.startswith(b'GET ') else bytes.fromhex(sys.argv[2])
  c.sendall(b'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: '+str(len(body)).encode()+b'\r\nConnection: close\r\n\r\n'+body)
"""
    monkeypatch.setattr(
        session,
        "_fixed_arguments",
        lambda _, path: [sys.executable, "-c", script, str(path), encoded],
    )
    result = controller.run_study(*args)
    assert result["status"] == "controller_admitted_before_blinding", result
    directory = next(args[-1].iterdir())
    for path in directory.glob("slot-*.json"):
        raw = json.loads(path.read_bytes())
        assert raw["process"]["reaped"] is raw["worker_joined"] is raw["resources_removed"] is True


def test_postseal_admission_failure_has_durable_locked_outcome(capture_fixture, monkeypatch):
    args, _, _ = capture_fixture
    monkeypatch.setattr(
        admission, "_consume", lambda _: (_ for _ in ()).throw(ValueError("failure"))
    )
    result = controller.run_study(*args)
    assert result["admitted"] is False
    directory = next(args[-1].iterdir())
    failed = json.loads((directory / "failure.json").read_bytes())
    assert failed["failure_stage"] == "admission"
    assert failed["admitted"] is False


@pytest.mark.parametrize(
    "boundary",
    ["protocol-traversal", "review-type", "evidence-traversal", "gate-drift", "gate-disagree"],
)
def test_preflight_refusals_create_no_resources(capture_fixture, monkeypatch, boundary):
    args, calls, _ = capture_fixture
    changed = list(args)
    if boundary == "protocol-traversal":
        changed[0] = args[0].parent / ".." / args[0].name
    elif boundary == "review-type":
        changed[2] = True
    elif boundary == "evidence-traversal":
        changed[-1] = args[-1] / ".." / "evidence"
    else:
        original = gate._verify
        count = 0

        def drift(*params):
            nonlocal count
            count += 1
            plan = original(*params)
            if count == (2 if boundary == "gate-disagree" else 3):
                value = plan.value()
                value["admission"]["admission_sha256"] = "0" * 64
                return gate._Plan(gate._canonical(value))
            return plan

        monkeypatch.setattr(gate, "_verify", drift)
    with pytest.raises(ValueError):
        controller.run_study(*changed)
    assert not calls
    assert not list(args[-1].iterdir())


def test_failed_primary_receipt_hash_retained(capture_fixture, monkeypatch):
    args, calls, capture = capture_fixture

    def failure(*params):
        raw = capture(*params)
        raw["status"] = "session_failed"
        raw["error"] = "synthetic-failure"
        params[-1].write_bytes(admission._canonical(raw))
        return raw

    monkeypatch.setattr(controller.primary, "run_primary", failure)
    result = controller.run_study(*args)
    assert len(calls) == 1
    directory = next(args[-1].iterdir())
    events = [
        json.loads(row)["event"] for row in (directory / "journal.jsonl").read_bytes().splitlines()
    ]
    failed = next(row for row in events if row["type"] == "slot_failed")
    assert failed["receipt_sha256"] == admission._sha((directory / "slot-1.json").read_bytes())
    assert list(result["dispositions"].values()) == ["failed-receipt-retained", "not-attempted"]


@pytest.mark.parametrize("damage", ["final-sync", "result-change", "failure-persistence"])
def test_final_persistence_never_returns_positive_on_failure(capture_fixture, monkeypatch, damage):
    args, _, _ = capture_fixture
    original = controller._write_result

    def write(path, parent, result):
        if damage == "failure-persistence":
            raise OSError("fixture")
        original(path, parent, result)
        if damage == "result-change":
            path.write_bytes(b"{}")

    monkeypatch.setattr(controller, "_write_result", write)
    if damage == "final-sync":
        sync = controller._sync_directory

        def fail_after_result(path, parent):
            if (path / "admission.json").exists():
                raise OSError("fixture")
            sync(path, parent)

        monkeypatch.setattr(controller, "_sync_directory", fail_after_result)
    result = controller.run_study(*args)
    assert result["admitted"] is False
    assert result["failure_stage"] == "persistence"
    if damage in ("final-sync", "failure-persistence"):
        assert result["outcome_persistence_error"] == "failure_outcome_persistence_failed"


@pytest.mark.parametrize("point", [1, 2, 3])
def test_directory_identity_checks_reject_changes(capture_fixture, monkeypatch, point):
    args, _, _ = capture_fixture
    directory = args[-1]
    expected = session._directory(directory)
    if point in (1, 3):
        calls = 0

        def identity(_):
            nonlocal calls
            calls += 1
            return (0, 0) if calls == (1 if point == 1 else 2) else expected

        monkeypatch.setattr(session, "_directory", identity)
    else:
        original = os.fstat
        from types import SimpleNamespace

        monkeypatch.setattr(
            os,
            "fstat",
            lambda fd: (
                SimpleNamespace(st_dev=0, st_ino=0)
                if original(fd).st_ino == expected[1]
                else original(fd)
            ),
        )
    with pytest.raises(ValueError, match="owned_directory_changed"):
        controller._sync_directory(directory, expected)


def test_journal_size_bound_prevents_launch(capture_fixture, monkeypatch):
    args, calls, _ = capture_fixture
    monkeypatch.setattr(admission, "MAX_JOURNAL", 1)
    result = controller.run_study(*args)
    assert result["admitted"] is False
    assert not calls


@pytest.mark.parametrize("mutation", ["absent", "bad-hash", "bad-json", "too-many"])
def test_health_evidence_required_before_second_slot(capture_fixture, monkeypatch, mutation):
    args, calls, capture = capture_fixture

    def damaged(*params):
        result = capture(*params)
        if mutation == "absent":
            result["health"] = []
        elif mutation == "bad-hash":
            result["health"][-1]["body_sha256"] = "0" * 64
        elif mutation == "bad-json":
            result["health"][-1]["body_base64"] = "e30="
        else:
            result["health"] *= session.HEALTH_ATTEMPTS + 1
        params[-1].write_bytes(admission._canonical(result))
        return result

    monkeypatch.setattr(controller.primary, "run_primary", damaged)
    result = controller.run_study(*args)
    assert result["admitted"] is False
    assert len(calls) == 1


def test_start_fsync_failure_prevents_any_primary_call(capture_fixture, monkeypatch):
    args, calls, _ = capture_fixture
    fsync = os.fsync
    failed = False

    def fail_start(descriptor):
        nonlocal failed
        journals = list(args[-1].glob("*/journal.jsonl"))
        if journals and b'"slot_started"' in journals[0].read_bytes() and not failed:
            failed = True
            raise OSError("synthetic_start_sync_failure")
        fsync(descriptor)

    monkeypatch.setattr(os, "fsync", fail_start)
    result = controller.run_study(*args)
    assert failed
    assert not calls
    assert result["admitted"] is False
    assert set(result["dispositions"].values()) == {"not-attempted"}
    with pytest.raises(FileExistsError):
        controller.run_study(*args)


def test_fresh_gate_drift_during_consume_persists_locked_failure(capture_fixture, monkeypatch):
    args, calls, _ = capture_fixture
    verify = gate._verify

    def drift_after_both_captures(*parameters):
        plan = verify(*parameters)
        journals = list(args[-1].glob("*/journal.jsonl"))
        if journals and b'"capture_complete"' in journals[0].read_bytes():
            value = plan.value()
            value["admission"]["admission_sha256"] = "0" * 64
            return gate._Plan(gate._canonical(value))
        return plan

    monkeypatch.setattr(gate, "_verify", drift_after_both_captures)
    result = controller.run_study(*args)
    assert len(calls) == 2
    assert result["admitted"] is False
    assert result["failure_stage"] == "admission"
    directory = next(args[-1].iterdir())
    persisted = json.loads((directory / "failure.json").read_bytes())
    assert persisted["admitted"] is False
    assert persisted["failure_stage"] == "admission"
    assert not (directory / "admission.json").exists()


@pytest.mark.parametrize("stage", ["before-mkdir", "after-mkdir"])
def test_changed_evidence_root_prevents_journal_and_primary(capture_fixture, monkeypatch, stage):
    args, calls, _ = capture_fixture
    original = session._directory
    checks = 0

    def changed(path):
        nonlocal checks
        identity = original(path)
        if path == args[-1]:
            checks += 1
            if checks == (2 if stage == "before-mkdir" else 3):
                return (0, 0)
        return identity

    monkeypatch.setattr(session, "_directory", changed)
    with pytest.raises(ValueError, match="evidence_root_changed"):
        controller.run_study(*args)
    assert not calls
    assert not list(args[-1].glob("*/journal.jsonl"))


@pytest.mark.parametrize("stage", ["append", "before-primary"])
def test_owned_directory_identity_drift_blocks_launch(capture_fixture, monkeypatch, stage):
    args, calls, _ = capture_fixture
    original = session._directory
    appended = False
    append = controller._append

    def record(*parameters):
        nonlocal appended
        append(*parameters)
        if parameters[-1]["type"] == "slot_started":
            appended = True

    def changed(path):
        identity = original(path)
        if path.name.startswith("run-") and (
            appended if stage == "before-primary" else (path / "journal.jsonl").exists()
        ):
            return (0, 0)
        return identity

    monkeypatch.setattr(controller, "_append", record)
    monkeypatch.setattr(session, "_directory", changed)
    result = controller.run_study(*args)
    assert result["admitted"] is False
    assert not calls


@pytest.mark.parametrize("target", ["journal", "admission"])
def test_short_write_is_never_success(capture_fixture, monkeypatch, target):
    args, calls, _ = capture_fixture
    fdopen = os.fdopen

    class ShortWriter:
        def __init__(self, stream):
            self.stream = stream

        def __enter__(self):
            return self

        def __exit__(self, *exc):
            self.stream.close()

        def fileno(self):
            return self.stream.fileno()

        def write(self, raw):
            return self.stream.write(raw[:-1])

    def opened(descriptor, mode, *positional, **keywords):
        stream = fdopen(descriptor, mode, *positional, **keywords)
        if mode == ("w+b" if target == "journal" else "wb"):
            return ShortWriter(stream)
        return stream

    if target == "journal":
        monkeypatch.setattr(os, "fdopen", opened)
        result = controller.run_study(*args)
        assert result["admitted"] is False
        assert not calls
    else:
        parent = session._directory(args[-1])
        monkeypatch.setattr(os, "fdopen", opened)
        with pytest.raises(OSError, match="short_admission_write"):
            controller._write_result(args[-1] / "result.json", parent, {"admitted": False})


@pytest.mark.parametrize("point", ["append-readback", "sealed-readback"])
def test_journal_readback_corruption_fails_closed(capture_fixture, monkeypatch, point):
    args, calls, _ = capture_fixture
    read = admission._read
    complete_reads = 0

    def changed(path, *parameters, **keywords):
        nonlocal complete_reads
        raw, identity = read(path, *parameters, **keywords)
        if path.name == "journal.jsonl":
            if point == "append-readback" and b'"run_started"' in raw:
                return b"corrupt", identity
            if point == "sealed-readback" and b'"capture_complete"' in raw:
                complete_reads += 1
                if complete_reads == 2:
                    return b"corrupt", identity
        return raw, identity

    monkeypatch.setattr(admission, "_read", changed)
    result = controller.run_study(*args)
    assert result["admitted"] is False
    assert len(calls) == (0 if point == "append-readback" else 2)


def test_controller_defensive_denominator_guard(capture_fixture, monkeypatch):
    args, calls, _ = capture_fixture
    validate = controller.native._validated_candidate

    def one_slot(*parameters):
        value, candidate = validate(*parameters)
        value["expected_slots"] = value["expected_slots"][:1]
        return value, candidate

    # Isolate the controller guard: the actual native validator already rejects this.
    plans = controller._plans(args[0], args[1], args[2], args[3], args[4])[2]
    monkeypatch.setattr(controller.native, "_validated_candidate", one_slot)
    monkeypatch.setattr(gate, "_verify", lambda *parameters: plans[0])
    with pytest.raises(ValueError, match="invalid_controller_denominator"):
        controller.run_study(*args)
    assert not calls
    assert not list(args[-1].iterdir())


@pytest.mark.parametrize("failed_receipt", [False, True])
def test_each_raw_directory_sync_precedes_completion_and_next_slot(
    capture_fixture, monkeypatch, failed_receipt
):
    args, calls, capture = capture_fixture
    sync = controller._sync_directory
    reached = False

    def returned(*parameters):
        result = capture(*parameters)
        if failed_receipt:
            result["status"] = "session_failed"
            result["error"] = "synthetic_failure"
            parameters[-1].write_bytes(admission._canonical(result))
        return result

    def fail_first_receipt_sync(path, expected):
        nonlocal reached
        if (path / "slot-1.json").exists():
            reached = True
            events = [
                json.loads(row)["event"]["type"]
                for row in (path / "journal.jsonl").read_bytes().splitlines()
            ]
            assert events == ["run_started", "slot_started"]
            assert len(calls) == 1
            raise OSError("synthetic_raw_directory_sync_failure")
        sync(path, expected)

    monkeypatch.setattr(controller.primary, "run_primary", returned)
    monkeypatch.setattr(controller, "_sync_directory", fail_first_receipt_sync)
    result = controller.run_study(*args)
    assert reached
    assert len(calls) == 1
    assert result["admitted"] is False
    assert list(result["dispositions"].values()) == ["attempted-outcome-unknown", "not-attempted"]
    assert result["failure_stage"] == "readback"
