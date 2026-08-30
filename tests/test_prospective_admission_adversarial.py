"""Synthetic capability and owned-file failures; never launch a primary session."""

import copy
import dataclasses
import json
import os
import pickle

import pytest

from tests.test_prospective_execution_gate import synthetic as synthetic
from tests.test_prospective_study_controller import capture_fixture as capture_fixture
from tools import prospective_observation_admission as admission
from tools import prospective_study_controller as controller


@pytest.fixture
def capability(tmp_path):
    # Deliberately incomplete witness tests ownership without reaching a gate.
    owned = admission._issue(
        (tmp_path / "protocol.json", "a" * 64, "b" * 40, tmp_path, tmp_path),
        (),
        tmp_path,
        (1, 2),
        -1,
        (1, 3),
        b"",
        (),
    )
    yield owned
    admission._LIVE.discard(owned)


@pytest.mark.parametrize("copier", [copy.copy, copy.deepcopy, pickle.dumps])
def test_live_witness_cannot_be_copied_or_serialized(capability, copier):
    with pytest.raises(TypeError):
        copier(capability)


def test_live_witness_cannot_be_json_serialized(capability):
    with pytest.raises(TypeError):
        json.dumps(capability)


def test_dataclass_replacement_does_not_issue_a_second_live_witness(capability):
    replacement = dataclasses.replace(capability)
    try:
        with pytest.raises(ValueError, match="invalid_or_consumed_capture_capability"):
            admission._consume(replacement)
    finally:
        admission._LIVE.discard(replacement)
    assert capability in admission._LIVE


def test_failed_consumption_still_consumes_witness(capability):
    with pytest.raises(ValueError, match="incomplete_capture_denominator"):
        admission._consume(capability)
    with pytest.raises(ValueError, match="invalid_or_consumed_capture_capability"):
        admission._consume(capability)


@pytest.mark.parametrize("value", [{}, {"admitted": True}, {"origin": "controller"}, None, True])
def test_untrusted_json_cannot_rehydrate_capture_authority(value):
    with pytest.raises(ValueError, match="invalid_or_consumed_capture_capability"):
        admission._consume(value)


@pytest.fixture
def owned_file(tmp_path):
    if not callable(getattr(os, "getuid", None)):
        pytest.skip("real owned-file checks require POSIX UID and permission semantics")
    root = tmp_path.resolve()
    path = root / "receipt.json"
    path.write_bytes(b"{}")
    path.chmod(0o600)
    parent = root.stat()
    return path, (parent.st_dev, parent.st_ino)


def test_owned_read_exact_bound_and_identity(owned_file):
    path, parent = owned_file
    data, observed = admission._read(path, parent, 2)
    info = path.stat()
    assert data == b"{}"
    assert observed == (info.st_dev, info.st_ino)


def test_owned_read_rejects_oversize(owned_file):
    path, parent = owned_file
    with pytest.raises(ValueError, match="owned_receipt_byte_limit"):
        admission._read(path, parent, 1)


def test_owned_read_rejects_replaced_identity(owned_file):
    path, parent = owned_file
    with pytest.raises(ValueError, match="owned_receipt_replaced"):
        admission._read(path, parent, 20, (-1, -1))


def test_owned_read_rejects_wrong_parent(owned_file):
    path, _ = owned_file
    with pytest.raises(ValueError):
        admission._read(path, (-1, -1), 20)


def test_owned_read_rejects_hardlink(owned_file):
    path, parent = owned_file
    try:
        os.link(path, path.with_name("alias.json"))
    except OSError:
        pytest.skip("host does not permit synthetic hardlinks")
    with pytest.raises(ValueError):
        admission._read(path, parent, 20)


def test_owned_read_rejects_symlink(owned_file):
    path, parent = owned_file
    alias = path.with_name("alias.json")
    try:
        alias.symlink_to(path)
    except OSError:
        pytest.skip("host does not permit synthetic symlinks")
    with pytest.raises((ValueError, OSError)):
        admission._read(alias, parent, 20)


def test_owned_read_sets_nonblocking_nofollow_before_open(owned_file, monkeypatch):
    path, parent = owned_file
    real_open = admission.os.open
    observed = []

    def checked_open(name, flags, *args, **kwargs):
        assert flags & getattr(os, "O_NONBLOCK", 0)
        if hasattr(os, "O_NOFOLLOW"):
            assert flags & getattr(os, "O_NOFOLLOW", 0)
        observed.append(flags)
        return real_open(name, flags, *args, **kwargs)

    monkeypatch.setattr(admission.os, "open", checked_open)
    assert admission._read(path, parent, 2)[0] == b"{}"
    assert len(observed) == 1


def test_owned_read_fifo_rejected_without_blocking(owned_file, monkeypatch):
    path, parent = owned_file
    mkfifo = getattr(os, "mkfifo", None)
    if not callable(mkfifo):
        pytest.skip("host does not support synthetic FIFOs")
    path.unlink()
    mkfifo(path, 0o600)
    real_open = admission.os.open

    def nonblocking_open(name, flags, *args, **kwargs):
        assert flags & getattr(os, "O_NONBLOCK", 0)  # Fail before opening if the guard regresses.
        return real_open(name, flags, *args, **kwargs)

    monkeypatch.setattr(admission.os, "open", nonblocking_open)
    with pytest.raises((ValueError, OSError)):
        admission._read(path, parent, 20)


def test_owned_read_rejects_hardlink_created_during_read(owned_file, monkeypatch):
    path, parent = owned_file
    alias = path.with_name("late-alias.json")
    try:
        os.link(path, alias)
    except OSError:
        pytest.skip("host does not permit synthetic hardlinks")
    alias.unlink()
    real_fdopen = admission.os.fdopen

    class LinkedDuringRead:
        def __init__(self, descriptor, mode):
            self.stream = real_fdopen(descriptor, mode)

        def __enter__(self):
            return self

        def __exit__(self, *args):
            self.stream.close()

        def fileno(self):
            return self.stream.fileno()

        def read(self, size):
            assert size == 3
            raw = self.stream.read(size)
            os.link(path, alias)
            return raw

    monkeypatch.setattr(admission.os, "fdopen", LinkedDuringRead)
    with pytest.raises(ValueError):
        admission._read(path, parent, 2)


@pytest.mark.parametrize("raw", [b"[]", b"true", b'{"x":1,"x":2}', b'{"x":NaN}', b"\xff"])
def test_receipt_json_rejects_invalid_shapes_and_numbers(raw):
    with pytest.raises(ValueError, match="invalid_owned_receipt"):
        admission._parse(raw)


@pytest.mark.parametrize("value", [None, False, 1, [], "====", "eA==\n"])
def test_capture_body_requires_canonical_base64_string(value):
    with pytest.raises(ValueError):
        admission._body({"body": value}, "body", 2)


def test_capture_body_enforces_decoded_size():
    with pytest.raises(ValueError, match="invalid_capture_bytes"):
        admission._body({"body": "eHl6"}, "body", 2)


def test_journal_binds_event_order_and_previous_hash():
    events = [{"type": "run_started"}, {"type": "slot_started"}]
    raw = admission._journal(events)
    lines = raw.splitlines(keepends=True)
    first, second = [json.loads(line) for line in lines]
    assert first["sequence"] == 0
    assert first["previous_sha256"] == "0" * 64
    assert second["sequence"] == 1
    assert second["previous_sha256"] == admission._sha(lines[0])
    assert raw != admission._journal(list(reversed(events)))


@pytest.mark.parametrize(
    "field,value",
    [
        ("admitted", 0),
        ("admitted", True),
        ("study_unlocked", 0),
        ("worker_joined", 1),
        ("resources_removed", 1),
        ("cleanup_errors", {}),
        ("cleanup_errors", None),
        ("purpose", "contract-fixture"),
        ("fixture", False),
        ("primary_postflight_error", "none"),
    ],
)
def test_malformed_capture_flags_rejected_before_deeper_evidence(field, value):
    raw = {
        "status": "primary_session_captured",
        "error": "none",
        "admitted": False,
        "study_unlocked": False,
        "worker_joined": True,
        "resources_removed": True,
        "cleanup_errors": [],
    }
    raw[field] = value
    plan = admission.gate._Plan(b"{}")
    with pytest.raises(ValueError, match="capture_not_admissible"):
        admission._validate_receipt(admission._canonical(raw), plan)


@pytest.mark.parametrize(
    "field,replacement",
    [
        (("process", "execution_observed"), 1),
        (("process", "reaped"), 1),
        (("process", "pid"), True),
        (("process", "returncode"), 0.0),
        (("process", "stdout_complete"), 1),
        (("process", "stdout_truncated"), 0),
        (("process", "stdout_bytes_observed"), False),
        (("process", "stdout_bytes_retained"), 0.0),
        (("process", "stderr_retained_sha256"), "0" * 64),
        (("process", "cleanup_errors"), None),
        (("completion", "body_complete"), 1),
        (("completion", "http_status"), 200.0),
        (("completion", "body_bytes"), True),
        (("completion", "request_body_sha256"), "0" * 64),
        (("completion", "transport"), "tcp"),
        (("primary_gate", "execution_permitted"), 1),
        (("candidate", "slot_id"), "case-forged__condition-forged__r1"),
        (("decoded", "content_sha256"), "0" * 64),
        (("environment_sha256",), "0" * 64),
        (("loaded_non_system_images",), []),
    ],
)
def test_forged_capture_fields_stop_before_second_slot(
    capture_fixture, monkeypatch, field, replacement
):
    args, calls, capture = capture_fixture

    def mutated(*parameters):
        result = capture(*parameters)
        parent = result
        for component in field[:-1]:
            parent = parent[component]
        parent[field[-1]] = replacement
        parameters[-1].write_bytes(admission._canonical(result) + b"\n")
        return result

    monkeypatch.setattr(controller.primary, "run_primary", mutated)
    result = controller.run_study(*args)
    assert result["admitted"] is False
    assert result["admission_before_blinding"] is False
    assert result["study_unlocked"] is result["scoring_start"] is False
    assert len(calls) == 1
    assert list(result["dispositions"].values())[-1] == "not-attempted"
    with pytest.raises(FileExistsError):
        controller.run_study(*args)
    assert len(calls) == 1


@pytest.mark.parametrize("mutation", ["missing", "same-bytes-new-inode", "broken-chain"])
def test_lost_or_replaced_journal_prevents_second_capture(capture_fixture, monkeypatch, mutation):
    args, calls, capture = capture_fixture

    def damaged(*parameters):
        result = capture(*parameters)
        path = parameters[-1].parent / "journal.jsonl"
        raw = path.read_bytes()
        if mutation in {"missing", "same-bytes-new-inode"}:
            path.rename(path.with_name("preserved-original-journal.jsonl"))
            if mutation == "same-bytes-new-inode":
                path.write_bytes(raw)
                path.chmod(0o600)
        else:
            records = [json.loads(line) for line in raw.splitlines()]
            records[-1]["previous_sha256"] = "f" * 64
            path.write_bytes(b"".join(admission._canonical(row) + b"\n" for row in records))
        return result

    monkeypatch.setattr(controller.primary, "run_primary", damaged)
    result = controller.run_study(*args)
    assert result["admitted"] is False
    assert len(calls) == 1
    assert list(result["dispositions"].values())[-1] == "not-attempted"


def test_raw_receipt_and_returned_capture_must_match(capture_fixture, monkeypatch):
    args, calls, capture = capture_fixture

    def mismatched(*parameters):
        result = capture(*parameters)
        result["unpersisted_extra"] = "synthetic-mismatch"
        return result

    monkeypatch.setattr(controller.primary, "run_primary", mismatched)
    result = controller.run_study(*args)
    assert result["admitted"] is False
    assert result["failure_stage"] == "readback"
    assert len(calls) == 1


def test_persistence_error_after_capture_never_retries(capture_fixture, monkeypatch):
    args, calls, _ = capture_fixture
    real_sync = controller.os.fsync

    def interrupted_sync(descriptor):
        if calls:
            raise OSError("synthetic-persistence-failure")
        return real_sync(descriptor)

    monkeypatch.setattr(controller.os, "fsync", interrupted_sync)
    result = controller.run_study(*args)
    assert result["admitted"] is False
    assert len(calls) == 1
    assert list(result["dispositions"].values()) == [
        "attempted-outcome-unknown",
        "not-attempted",
    ]


def test_existing_future_slot_receipt_never_overwritten(capture_fixture, monkeypatch):
    args, calls, capture = capture_fixture
    preserved = []

    def preexisting(*parameters):
        result = capture(*parameters)
        path = parameters[-1].parent / "slot-2.json"
        path.write_bytes(b"synthetic-existing-evidence")
        path.chmod(0o600)
        preserved.append(path)
        return result

    monkeypatch.setattr(controller.primary, "run_primary", preexisting)
    result = controller.run_study(*args)
    assert result["admitted"] is False
    assert len(calls) == 1
    assert preserved[0].read_bytes() == b"synthetic-existing-evidence"


def test_directory_sync_uses_nonblocking_directory_nofollow_flags(tmp_path, monkeypatch):
    if not callable(getattr(os, "getuid", None)):
        pytest.skip("real owned-directory checks require POSIX UID semantics")
    directory = tmp_path.resolve()
    directory.chmod(0o700)
    info = directory.stat()
    original = controller.os.open
    calls = []

    def checked_open(path, flags, *args, **kwargs):
        assert flags & getattr(os, "O_NONBLOCK", 0)
        if hasattr(os, "O_DIRECTORY"):
            assert flags & getattr(os, "O_DIRECTORY", 0)
        if hasattr(os, "O_NOFOLLOW"):
            assert flags & getattr(os, "O_NOFOLLOW", 0)
        calls.append(flags)
        return original(path, flags, *args, **kwargs)

    monkeypatch.setattr(controller.os, "open", checked_open)
    controller._sync_directory(directory, (info.st_dev, info.st_ino))
    assert len(calls) == 1


def test_postseal_failure_outcome_cannot_overwrite_existing_evidence(capture_fixture, monkeypatch):
    args, calls, _ = capture_fixture
    retained = {}

    def fail_after_seal(owned):
        retained["journal"] = (owned.directory / "journal.jsonl").read_bytes()
        retained["directory"] = owned.directory
        failure = owned.directory / "failure.json"
        failure.write_bytes(b"synthetic-preexisting-failure")
        failure.chmod(0o600)
        raise ValueError("synthetic-admission-failure")

    monkeypatch.setattr(admission, "_consume", fail_after_seal)
    result = controller.run_study(*args)
    assert len(calls) == 2
    assert result["admitted"] is result["scoring_start"] is False
    assert result["outcome_persistence_error"] == "failure_outcome_persistence_failed"
    assert (retained["directory"] / "failure.json").read_bytes() == b"synthetic-preexisting-failure"
    assert (retained["directory"] / "journal.jsonl").read_bytes() == retained["journal"]


def test_admission_write_failure_preserves_sealed_journal_and_locked_failure(
    capture_fixture, monkeypatch
):
    args, calls, _ = capture_fixture
    original = controller._write_result
    retained = {}

    def fail_admission_write(path, parent, result):
        if path.name == "admission.json":
            retained["directory"] = path.parent
            retained["journal"] = (path.parent / "journal.jsonl").read_bytes()
            raise OSError("synthetic-admission-write-failure")
        return original(path, parent, result)

    monkeypatch.setattr(controller, "_write_result", fail_admission_write)
    result = controller.run_study(*args)
    directory = retained["directory"]
    durable_failure = json.loads((directory / "failure.json").read_bytes())
    assert len(calls) == 2
    assert result["admitted"] is False
    assert durable_failure["admitted"] is durable_failure["study_unlocked"] is False
    assert durable_failure["scoring_start"] is False
    assert durable_failure["failure_stage"] == "persistence"
    assert durable_failure["journal_sha256"] == admission._sha(retained["journal"])
    assert (directory / "journal.jsonl").read_bytes() == retained["journal"]
    assert not (directory / "admission.json").exists()
    with pytest.raises(FileExistsError):
        controller.run_study(*args)
    assert len(calls) == 2
