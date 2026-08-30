"""Bounded synthetic children only; no model runtime or network execution."""

import base64
import os
import subprocess
import sys
import threading
import time
from pathlib import Path
from types import SimpleNamespace

import pytest

from tools import server_process as subject


@pytest.fixture
def child():
    if os.name != "posix":
        pytest.skip("POSIX pipe supervisor")

    def run(code, **kwargs):
        return subject.capture_child(
            [str(Path(sys.executable).resolve()), "-c", code],
            {"PATH": os.defpath, "LANG": "C"},
            **kwargs,
        )

    return run


def test_fast_exit_and_locked_receipt(child):
    receipt = child("pass")
    assert receipt["status"] == "process_captured"
    assert receipt["returncode"] == 0
    assert receipt["reaped"] is True
    assert receipt["stdout_complete"] is receipt["stderr_complete"] is True
    assert receipt["admitted"] is receipt["study_unlocked"] is False


def test_concurrent_streams_do_not_deadlock(child):
    receipt = child(
        "import os\nfor i in range(20):\n os.write(1,b'a'*4096)\n os.write(2,b'b'*4096)"
    )
    assert receipt["status"] == "process_captured"
    assert base64.b64decode(receipt["raw_stdout_base64"]) == b"a" * 81920
    assert base64.b64decode(receipt["raw_stderr_base64"]) == b"b" * 81920


def test_nonzero_exit_is_not_success(child):
    receipt = child("raise SystemExit(7)")
    assert receipt["status"] == "capture_failed"
    assert receipt["error"] == "nonzero_exit"
    assert receipt["returncode"] == 7


def test_timeout_terminates_and_reaps(child):
    start = time.monotonic()
    receipt = child("import time; time.sleep(20)", timeout=0.2, cleanup_grace=0.1)
    assert receipt["error"] == "deadline_exceeded"
    assert receipt["reaped"] is True
    assert time.monotonic() - start < 3


def test_ignored_term_escalates_to_kill(child, tmp_path):
    marker = tmp_path / "ready"
    event = threading.Event()

    def cancel_after_ready():
        deadline = time.monotonic() + 5
        while not marker.exists() and time.monotonic() < deadline:
            time.sleep(0.01)
        event.set()

    watcher = threading.Thread(target=cancel_after_ready)
    watcher.start()
    try:
        receipt = child(
            f"import signal,time,pathlib; signal.signal(signal.SIGTERM, signal.SIG_IGN); pathlib.Path({str(marker)!r}).touch(); time.sleep(20)",
            timeout=10,
            cleanup_grace=0.1,
            cancel=event,
        )
    finally:
        watcher.join(6)
    assert marker.exists()
    assert not watcher.is_alive()
    assert receipt["error"] == "cancelled"
    assert receipt["kill_sent"] is True
    assert receipt["reaped"] is True


def test_cancellation_reaps(child):
    event = threading.Event()
    timer = threading.Timer(0.2, event.set)
    timer.start()
    try:
        receipt = child("import time; time.sleep(20)", cancel=event)
    finally:
        timer.cancel()
        timer.join()
    assert receipt["error"] == "cancelled"
    assert receipt["reaped"] is True


@pytest.mark.parametrize("stream", [1, 2], ids=["stdout", "stderr"])
def test_overflow_retains_only_bounded_prefix(child, stream):
    receipt = child(
        f"import os,time; os.write({stream}, b'x'*4097); time.sleep(20)", output_limit=4096
    )
    name = "stdout" if stream == 1 else "stderr"
    assert receipt["error"] == "output_limit_exceeded"
    assert len(base64.b64decode(receipt[f"raw_{name}_base64"])) == 4096
    assert receipt[f"{name}_complete"] is False
    assert receipt[f"{name}_sha256"] is None
    assert receipt[f"{name}_retained_sha256"]
    assert receipt["reaped"] is True


def test_exact_limit_is_not_overflow(child):
    receipt = child("import os; os.write(1,b'x'*4096)", output_limit=4096)
    assert receipt["status"] == "process_captured"
    assert receipt["stdout_complete"] is True
    assert receipt["stdout_bytes_observed"] == 4096


@pytest.mark.parametrize(
    "kwargs",
    [
        {"timeout": 0},
        {"timeout": float("inf")},
        {"timeout": float("nan")},
        {"timeout": True},
        {"timeout": 121},
        {"timeout": 10**1000},
        {"output_limit": True},
        {"output_limit": 0},
        {"output_limit": 1048577},
        {"cleanup_grace": 0},
        {"cleanup_grace": 6},
        {"cancel": object()},
    ],
    ids=[
        "zero-time",
        "infinite",
        "nan",
        "bool-time",
        "long-time",
        "huge-int",
        "bool-limit",
        "zero-limit",
        "large-limit",
        "zero-grace",
        "large-grace",
        "bad-cancel",
    ],
)
def test_bad_options_never_launch(monkeypatch, kwargs):
    monkeypatch.setattr(
        subject.subprocess, "Popen", lambda *args, **kwargs: pytest.fail("launched")
    )
    with pytest.raises(ValueError):
        subject.capture_child(["/synthetic/python"], {}, **kwargs)


@pytest.mark.parametrize(
    "argv,env",
    [
        ([], {}),
        (["relative"], {}),
        (["/absolute", "bad\x00"], {}),
        (("/absolute",), {}),
        (["/absolute"], {"BAD\x00": "value"}),
        (["/absolute"], {"A": 1}),
        (["/absolute"], {"A=B": "value"}),
        (["/absolute"], []),
    ],
    ids=[
        "empty",
        "relative",
        "nul-arg",
        "tuple-argv",
        "nul-env",
        "nonstring-env",
        "equals-key",
        "list-env",
    ],
)
def test_bad_arguments_never_launch(monkeypatch, argv, env):
    monkeypatch.setattr(
        subject.subprocess, "Popen", lambda *args, **kwargs: pytest.fail("launched")
    )
    with pytest.raises(ValueError):
        subject.capture_child(argv, env)


def test_unsupported_host_rejects(monkeypatch):
    monkeypatch.setattr(subject, "POSIX", False)
    with pytest.raises(ValueError):
        subject.capture_child(["/synthetic/python"], {})


def test_precancel_does_not_launch(child, monkeypatch):
    event = threading.Event()
    event.set()
    monkeypatch.setattr(
        subject.subprocess, "Popen", lambda *args, **kwargs: pytest.fail("launched")
    )
    receipt = child("pass", cancel=event)
    assert receipt["error"] == "cancelled"
    assert receipt["execution_observed"] is False


def test_launch_failure_is_safe(child, monkeypatch):
    def fail(*args, **kwargs):
        raise OSError("private-path")

    monkeypatch.setattr(subject.subprocess, "Popen", fail)
    receipt = child("pass")
    assert receipt["error"] == "launch_failed"
    assert "private-path" not in str(receipt)


def test_explicit_environment_and_invocation(child, monkeypatch):
    original = subject.subprocess.Popen
    calls = []
    monkeypatch.setenv("SECRET_TOKEN", "not-for-child")

    def capture(*args, **kwargs):
        calls.append(kwargs)
        return original(*args, **kwargs)

    monkeypatch.setattr(subject.subprocess, "Popen", capture)
    receipt = child("import os; print(os.environ.get('SECRET_TOKEN','absent'))")
    assert base64.b64decode(receipt["raw_stdout_base64"]) == b"absent\n"
    assert calls[0]["env"] == {"PATH": os.defpath, "LANG": "C"}
    assert calls[0]["stdin"] == subprocess.DEVNULL
    assert calls[0]["start_new_session"] is True
    assert calls[0]["shell"] is False


def test_selector_registration_failure_still_reaps(child, monkeypatch):
    def fail(*args, **kwargs):
        raise OSError("private selector error")

    monkeypatch.setattr(subject.selectors.DefaultSelector, "register", fail)
    receipt = child("import time; time.sleep(20)", cleanup_grace=0.1)
    assert receipt["error"] == "capture_io_failed"
    assert receipt["reaped"] is True


def test_cleanup_escalation_preserves_errors():
    class Fake:
        returncode = None

        def poll(self):
            return None

        def terminate(self):
            raise OSError("private")

        def wait(self, timeout):
            raise subprocess.TimeoutExpired("private", timeout)

        def kill(self):
            raise OSError("private")

    receipt = subject._cleanup(Fake(), 0.1)
    assert receipt["reaped"] is False
    assert receipt["cleanup_errors"] == ["terminate_failed", "kill_failed", "reap_timeout"]


def test_closed_pipes_do_not_complete_a_running_child(child):
    receipt = child("import os,time; os.close(1); os.close(2); time.sleep(20)", timeout=0.2)
    assert receipt["error"] == "deadline_exceeded"
    assert receipt["reaped"] is True


def test_one_closed_pipe_does_not_drop_other_stream(child):
    receipt = child("import os; os.close(1); os.write(2,b'other stream')")
    assert receipt["status"] == "process_captured"
    assert base64.b64decode(receipt["raw_stderr_base64"]) == b"other stream"


def test_timeout_does_not_publish_incomplete_full_hash(child):
    receipt = child("import os,time; os.write(1,b'prefix'); time.sleep(20)", timeout=0.3)
    assert receipt["stdout_sha256"] is None
    assert receipt["stdout_complete"] is False
    assert receipt["stdout_retained_sha256"]


def test_nonzero_exit_can_have_complete_streams(child):
    receipt = child("print('complete'); raise SystemExit(3)")
    assert receipt["error"] == "nonzero_exit"
    assert receipt["stdout_complete"] is True
    assert receipt["stdout_sha256"] == receipt["stdout_retained_sha256"]


@pytest.mark.parametrize("primary", ["none", "deadline_exceeded"])
def test_cleanup_failure_never_masks_primary_error(child, monkeypatch, primary):
    real_cleanup = subject._cleanup

    def cleanup(process, grace):
        result = real_cleanup(process, grace)
        result["cleanup_errors"].append("synthetic_cleanup_error")
        return result

    monkeypatch.setattr(subject, "_cleanup", cleanup)
    receipt = child(
        "pass" if primary == "none" else "import time; time.sleep(20)",
        timeout=5 if primary == "none" else 0.2,
    )
    assert receipt["error"] == ("cleanup_failed" if primary == "none" else primary)
    assert receipt["cleanup_errors"] == ["synthetic_cleanup_error"]
    assert receipt["stdout_complete"] is False
    assert receipt["stdout_sha256"] is None


def test_synthetic_held_pipe_after_child_exit_is_deadline_bounded(child, monkeypatch):
    # An already-exited fake child leaves fixture-owned writers open; no orphan
    # process or scheduler-dependent assumption about Python startup is needed.
    out_read, out_write = os.pipe()
    err_read, err_write = os.pipe()
    try:
        with os.fdopen(out_read, "rb") as stdout, os.fdopen(err_read, "rb") as stderr:
            process = SimpleNamespace(stdout=stdout, stderr=stderr, pid=123, poll=lambda: 0)
            monkeypatch.setattr(subject.subprocess, "Popen", lambda *args, **kwargs: process)
            receipt = child("pass", timeout=0.1)
    finally:
        os.close(out_write)
        os.close(err_write)
    assert receipt["error"] == "deadline_exceeded"
    assert receipt["reaped"] is True
    assert receipt["returncode"] == 0
    assert receipt["terminate_sent"] is receipt["kill_sent"] is False
    assert receipt["stdout_complete"] is False


def test_selector_read_failure_still_reaps(child, monkeypatch):
    def fail(*args, **kwargs):
        raise OSError("private selector error")

    monkeypatch.setattr(subject.selectors.DefaultSelector, "select", fail)
    receipt = child("import time; time.sleep(20)")
    assert receipt["error"] == "capture_io_failed"
    assert receipt["reaped"] is True


@pytest.mark.parametrize("failure", ["poll", "wait", "reap"])
def test_cleanup_system_errors_are_safe(failure):
    class Fake:
        calls = 0

        def poll(self):
            if failure == "poll":
                raise OSError("private")
            return None

        def terminate(self):
            pass

        def wait(self, timeout):
            self.calls += 1
            if self.calls == 1:
                if failure == "wait":
                    raise OSError("private")
                raise subprocess.TimeoutExpired("private", timeout)
            if failure == "reap":
                raise OSError("private")
            return -9

        def kill(self):
            pass

    receipt = subject._cleanup(Fake(), 0.1)
    assert receipt["cleanup_errors"] == [
        {"poll": "poll_failed", "wait": "wait_failed", "reap": "reap_failed"}[failure]
    ]
    assert "private" not in str(receipt)


def test_nonblocking_capability_missing_rejects_before_launch(child, monkeypatch):
    monkeypatch.setattr(subject.os, "set_blocking", None)
    monkeypatch.setattr(
        subject.subprocess, "Popen", lambda *args, **kwargs: pytest.fail("launched")
    )
    with pytest.raises(ValueError, match="unsupported_nonblocking"):
        child("pass")


def test_missing_pipe_is_cleaned_without_capture(child, monkeypatch):
    process = SimpleNamespace(stdout=None, stderr=None, pid=123, poll=lambda: 0)
    monkeypatch.setattr(subject.subprocess, "Popen", lambda *args, **kwargs: process)
    receipt = child("pass")
    assert receipt["error"] == "capture_io_failed"
    assert receipt["reaped"] is True


def test_transient_would_block_is_retried(child, monkeypatch):
    real_select = subject.selectors.DefaultSelector.select
    real_read = subject.os.read
    active = set()
    blocked = []

    def select(selector, timeout):
        events = real_select(selector, timeout)
        active.update(key.fd for key, _ in events)
        return events

    def read(fd, size):
        if fd in active and not blocked:
            blocked.append(True)
            raise BlockingIOError
        return real_read(fd, size)

    monkeypatch.setattr(subject.selectors.DefaultSelector, "select", select)
    monkeypatch.setattr(subject.os, "read", read)
    receipt = child("print('data')")
    assert blocked
    assert receipt["status"] == "process_captured"
    assert base64.b64decode(receipt["raw_stdout_base64"]) == b"data\n"


def test_pipe_close_failure_is_reported(child, monkeypatch):
    real_popen = subject.subprocess.Popen

    class Pipe:
        def __init__(self, wrapped):
            self.wrapped = wrapped

        def fileno(self):
            return self.wrapped.fileno()

        def close(self):
            self.wrapped.close()
            raise OSError("private close error")

    def popen(*args, **kwargs):
        process = real_popen(*args, **kwargs)
        monkeypatch.setattr(process, "stdout", Pipe(process.stdout))
        return process

    monkeypatch.setattr(subject.subprocess, "Popen", popen)
    receipt = child("pass")
    assert receipt["error"] == "cleanup_failed"
    assert receipt["cleanup_errors"] == ["pipe_close_failed"]
    assert receipt["stdout_sha256"] is None
