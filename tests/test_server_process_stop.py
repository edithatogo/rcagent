"""Graceful-stop fixtures use only synthetic children and owned local pipes."""

import base64
import os
import selectors
import signal
import subprocess
import sys
import threading
import time
from collections.abc import Callable
from pathlib import Path
from typing import IO, Never, Protocol, TypedDict, Unpack

import pytest

from tools import server_process as subject


class ReadyChildOptions(TypedDict, total=False):
    output_limit: int
    cleanup_grace: float
    cancel: threading.Event | None
    deadline: float | None


class WaitForProcess(Protocol):
    def __call__(self, timeout: float | None = None) -> int: ...


class ReadyChildRunner(Protocol):
    def __call__(
        self,
        handler: str,
        *,
        action: Callable[[threading.Event], None] | None = None,
        timeout: float = 10,
        **kwargs: Unpack[ReadyChildOptions],
    ) -> subject.CaptureResult: ...


class PopenOptions(TypedDict):
    stdin: int
    stdout: int
    stderr: int
    env: dict[str, str]
    shell: bool
    start_new_session: bool


class PipeProcess:
    def __init__(
        self,
        stdout: IO[bytes],
        stderr: IO[bytes],
        returncode: int | None = None,
        *,
        exit_on_terminate: bool = False,
    ) -> None:
        self.stdout = stdout
        self.stderr = stderr
        self.pid = 123
        self.returncode = returncode
        self.exit_on_terminate = exit_on_terminate

    def poll(self) -> int | None:
        return self.returncode

    def terminate(self) -> None:
        if self.exit_on_terminate:
            self.returncode = 0


def _unexpected_launch(*_args: object, **_kwargs: object) -> Never:
    pytest.fail("launched")


@pytest.fixture
def ready_child(tmp_path: Path) -> ReadyChildRunner:
    if os.name != "posix":
        pytest.skip("POSIX child supervisor")

    def run(
        handler: str,
        *,
        action: Callable[[threading.Event], None] | None = None,
        timeout: float = 10,
        **kwargs: Unpack[ReadyChildOptions],
    ) -> subject.CaptureResult:
        marker = tmp_path / "ready"
        stop = threading.Event()
        done = threading.Event()

        def request_stop() -> None:
            deadline = time.monotonic() + 8
            while not marker.exists() and not done.is_set() and time.monotonic() < deadline:
                time.sleep(0.01)
            if marker.exists():
                if action is not None:
                    action(stop)
                else:
                    stop.set()

        watcher = threading.Thread(target=request_stop)
        watcher.start()
        script = (
            "import os,signal,time,pathlib\n"
            + handler
            + f"\npathlib.Path({str(marker)!r}).touch()\nwhile True: time.sleep(0.1)\n"
        )
        try:
            result = subject.capture_child(
                [str(Path(sys.executable).resolve()), "-c", script],
                {"PATH": os.defpath, "LANG": "C"},
                stop_event=stop,
                timeout=timeout,
                **kwargs,
            )
        finally:
            done.set()
            watcher.join(9)
        assert marker.exists(), "synthetic child never became ready"
        assert not watcher.is_alive()
        return result

    return run


def test_prestop_does_not_launch(monkeypatch: pytest.MonkeyPatch) -> None:
    if os.name != "posix":
        pytest.skip("POSIX child supervisor")
    event = threading.Event()
    event.set()
    monkeypatch.setattr(subject.subprocess, "Popen", _unexpected_launch)
    result = subject.capture_child(["/synthetic/child"], {}, stop_event=event)
    assert result["error"] == "stop_before_launch"
    assert result["execution_observed"] is False
    assert result["stop_requested"] is True
    assert result["stop_started"] is False


def test_cancel_wins_over_prestop(monkeypatch: pytest.MonkeyPatch) -> None:
    if os.name != "posix":
        pytest.skip("POSIX child supervisor")
    event = threading.Event()
    event.set()
    monkeypatch.setattr(subject.subprocess, "Popen", _unexpected_launch)
    result = subject.capture_child(["/synthetic/child"], {}, stop_event=event, cancel=event)
    assert result["error"] == "cancelled"
    assert result["stop_started"] is False


@pytest.mark.parametrize(
    "invalid", [True, 1, "stop", object()], ids=["bool", "int", "str", "object"]
)
def test_stop_event_requires_event(monkeypatch: pytest.MonkeyPatch, invalid: object) -> None:
    monkeypatch.setattr(subject.subprocess, "Popen", _unexpected_launch)
    with pytest.raises(ValueError):
        subject.capture_child(["/synthetic/child"], {}, stop_event=invalid)


def test_handler_final_streams_are_drained(ready_child: ReadyChildRunner) -> None:
    result = ready_child(
        "def stop(signum, frame):\n os.write(1,b'final-out')\n os.write(2,b'final-err')\n raise SystemExit(0)\nsignal.signal(signal.SIGTERM,stop)",
        cleanup_grace=1,
    )
    assert result["status"] == "process_stopped"
    assert result["error"] == "none"
    assert result["returncode"] == 0
    assert result["stop_requested"] is result["stop_started"] is True
    assert result["reaped"] is True
    assert result["stdout_complete"] is result["stderr_complete"] is True
    assert base64.b64decode(result["raw_stdout_base64"]) == b"final-out"
    assert base64.b64decode(result["raw_stderr_base64"]) == b"final-err"
    assert result["admitted"] is result["study_unlocked"] is False


def test_default_sigterm_is_stopped_not_natural_exit(ready_child: ReadyChildRunner) -> None:
    result = ready_child("pass")
    assert result["status"] == "process_stopped"
    assert result["returncode"] == -signal.SIGTERM
    assert result["stop_started"] is True


def test_ignored_term_fails_and_is_sent_once(
    ready_child: ReadyChildRunner, monkeypatch: pytest.MonkeyPatch
) -> None:
    original = subject.subprocess.Popen
    terms: list[bool] = []

    def popen(*args: *tuple[list[str]], **kwargs: Unpack[PopenOptions]) -> subprocess.Popen[bytes]:
        process = original(*args, **kwargs)
        terminate = process.terminate

        def term() -> None:
            terms.append(True)
            terminate()

        monkeypatch.setattr(process, "terminate", term)
        return process

    monkeypatch.setattr(subject.subprocess, "Popen", popen)
    result = ready_child("signal.signal(signal.SIGTERM,signal.SIG_IGN)", cleanup_grace=0.1)
    assert result["status"] == "capture_failed"
    assert result["error"] == "stop_grace_exceeded"
    assert result["kill_sent"] is result["reaped"] is True
    assert terms == [True]


@pytest.mark.parametrize("stream", [1, 2], ids=["stdout", "stderr"])
def test_stopping_output_overflow_remains_failure(
    ready_child: ReadyChildRunner, stream: int
) -> None:
    handler = f"def stop(signum,frame):\n os.write({stream},b'x'*4097)\n raise SystemExit(0)\nsignal.signal(signal.SIGTERM,stop)"
    result = ready_child(handler, output_limit=4096)
    assert result["error"] == "output_limit_exceeded"
    assert result["status"] == "capture_failed"
    digest = result["stdout_sha256"] if stream == 1 else result["stderr_sha256"]
    raw = result["raw_stdout_base64"] if stream == 1 else result["raw_stderr_base64"]
    assert digest is None
    assert len(base64.b64decode(raw)) == 4096


def test_handler_nonzero_is_not_laundered(ready_child: ReadyChildRunner) -> None:
    result = ready_child(
        "def stop(signum,frame):\n raise SystemExit(7)\nsignal.signal(signal.SIGTERM,stop)"
    )
    assert result["returncode"] == 7
    assert result["status"] == "capture_failed"
    assert result["error"] == "nonzero_exit"


def test_active_cancel_and_stop_remain_cancellation(ready_child: ReadyChildRunner) -> None:
    cancel = threading.Event()

    def both(stop: threading.Event) -> None:
        cancel.set()
        stop.set()

    result = ready_child("pass", action=both, cancel=cancel)
    assert result["error"] == "cancelled"
    assert result["status"] == "capture_failed"


@pytest.mark.parametrize("code", [0, 7], ids=["zero", "nonzero"])
def test_observed_exit_is_not_relabelled_by_stop(
    monkeypatch: pytest.MonkeyPatch, code: int
) -> None:
    if os.name != "posix":
        pytest.skip("POSIX child supervisor")
    stop = threading.Event()
    out_r, out_w = os.pipe()
    err_r, err_w = os.pipe()
    os.close(out_w)
    os.close(err_w)
    with os.fdopen(out_r, "rb") as stdout, os.fdopen(err_r, "rb") as stderr:
        process = PipeProcess(stdout, stderr, returncode=code)

        def popen(*args: object, **kwargs: object) -> PipeProcess:
            stop.set()
            return process

        monkeypatch.setattr(subject.subprocess, "Popen", popen)
        result = subject.capture_child(["/synthetic/child"], {}, stop_event=stop)
    assert result["stop_requested"] is True
    assert result["stop_started"] is False
    assert result["terminate_sent"] is False
    assert result["status"] == ("process_captured" if code == 0 else "capture_failed")
    assert result["error"] == ("none" if code == 0 else "nonzero_exit")


@pytest.mark.parametrize(
    ("timeout", "error"),
    [(5, "stop_grace_exceeded"), (0.05, "deadline_exceeded")],
    ids=["stop-budget", "execution-deadline"],
)
def test_held_pipe_after_stopped_child_is_bounded(
    monkeypatch: pytest.MonkeyPatch, timeout: float, error: str
) -> None:
    if os.name != "posix":
        pytest.skip("POSIX child supervisor")
    stop = threading.Event()
    out_r, out_w = os.pipe()
    err_r, err_w = os.pipe()
    try:
        with os.fdopen(out_r, "rb") as stdout, os.fdopen(err_r, "rb") as stderr:
            process = PipeProcess(stdout, stderr, exit_on_terminate=True)

            def popen(*args: object, **kwargs: object) -> PipeProcess:
                stop.set()
                return process

            monkeypatch.setattr(subject.subprocess, "Popen", popen)
            started = time.monotonic()
            result = subject.capture_child(
                ["/synthetic/child"], {}, stop_event=stop, cleanup_grace=0.05, timeout=timeout
            )
    finally:
        os.close(out_w)
        os.close(err_w)
    assert time.monotonic() - started < 2
    assert result["status"] == "capture_failed"
    assert result["error"] == error
    assert result["reaped"] is True
    assert result["stdout_complete"] is False
    assert result["stdout_sha256"] is None


def test_read_failure_after_stop_still_reaps(
    ready_child: ReadyChildRunner, monkeypatch: pytest.MonkeyPatch
) -> None:
    original = subject.subprocess.Popen
    real_select = subject.selectors.DefaultSelector.select
    stopping: list[bool] = []

    def popen(*args: *tuple[list[str]], **kwargs: Unpack[PopenOptions]) -> subprocess.Popen[bytes]:
        process = original(*args, **kwargs)
        terminate = process.terminate

        def term() -> None:
            stopping.append(True)
            terminate()

        monkeypatch.setattr(process, "terminate", term)
        return process

    def select(
        selector: selectors.DefaultSelector, timeout: float | None
    ) -> list[tuple[selectors.SelectorKey, int]]:
        if stopping:
            raise OSError("private failure")
        return real_select(selector, timeout)

    monkeypatch.setattr(subject.subprocess, "Popen", popen)
    monkeypatch.setattr(subject.selectors.DefaultSelector, "select", select)
    result = ready_child("pass")
    assert result["error"] == "capture_io_failed"
    assert result["stop_started"] is True
    assert result["reaped"] is True
    assert "private failure" not in str(result)


@pytest.mark.parametrize("signal_name", ["terminate", "kill"])
def test_signal_error_is_preserved_without_leaking_child(
    ready_child: ReadyChildRunner, monkeypatch: pytest.MonkeyPatch, signal_name: str
) -> None:
    original = subject.subprocess.Popen
    calls: list[bool] = []
    children: list[tuple[subprocess.Popen[bytes], Callable[[], None], WaitForProcess]] = []

    def popen(*args: *tuple[list[str]], **kwargs: Unpack[PopenOptions]) -> subprocess.Popen[bytes]:
        process = original(*args, **kwargs)
        send = process.terminate if signal_name == "terminate" else process.kill
        kill, wait = process.kill, process.wait
        children.append((process, kill, wait))

        def fail() -> Never:
            calls.append(True)
            send()
            # Test error preservation, not scheduler latency within the stop budget.
            wait(timeout=5)
            raise OSError("private failure")

        monkeypatch.setattr(process, signal_name, fail)
        return process

    monkeypatch.setattr(subject.subprocess, "Popen", popen)
    try:
        result = ready_child(
            "signal.signal(signal.SIGTERM,signal.SIG_IGN)" if signal_name == "kill" else "pass",
            cleanup_grace=0.1,
        )
        assert result["error"] == (
            "stop_signal_failed" if signal_name == "terminate" else "stop_grace_exceeded"
        )
        assert f"{signal_name}_failed" in result["cleanup_errors"]
        assert result["reaped"] is True
        assert calls == [True]
    finally:
        # Original methods bypass injected failures; cleanup errors must stay visible.
        for process, kill, wait in children:
            try:
                if process.poll() is None:
                    kill()
            finally:
                wait(timeout=5)


def test_cleanup_error_cannot_become_successful_stop(
    ready_child: ReadyChildRunner, monkeypatch: pytest.MonkeyPatch
) -> None:
    original = subject.finish_child_stop

    def finish(
        process: subject.ReapableProcess,
        deadline: float,
        terminate_sent: bool,
        kill_attempted: bool,
        kill_sent: bool,
        errors: list[str],
    ) -> subject.CleanupResult:
        result = original(process, deadline, terminate_sent, kill_attempted, kill_sent, errors)
        result["cleanup_errors"].append("synthetic_reap_error")
        return result

    monkeypatch.setattr(subject, "finish_child_stop", finish)
    result = ready_child("pass")
    assert result["error"] == "cleanup_failed"
    assert result["status"] == "capture_failed"
    assert result["stdout_complete"] is False


@pytest.mark.parametrize(
    "failure",
    ["poll", "kill", "wait", "timeout", "already-attempted"],
    ids=["poll-error", "kill-error", "wait-error", "reap-timeout", "no-repeated-kill"],
)
def test_finish_stop_errors_and_budget_are_bounded(failure: str) -> None:
    kills: list[bool] = []
    waits: list[float] = []

    class Fake:
        def poll(self) -> int | None:
            if failure == "poll":
                raise OSError("private")
            return

        def kill(self) -> None:
            kills.append(True)
            if failure == "kill":
                raise OSError("private")

        def wait(self, timeout: float) -> int:
            waits.append(timeout)
            if failure == "wait":
                raise OSError("private")
            if failure == "timeout":
                raise subprocess.TimeoutExpired("private", timeout)
            return -9

    result = subject.finish_child_stop(
        Fake(), time.monotonic() + 0.1, True, failure == "already-attempted", False, ["original"]
    )
    assert result["cleanup_errors"][0] == "original"
    expected = {
        "poll": "poll_failed",
        "kill": "kill_failed",
        "wait": "reap_failed",
        "timeout": "reap_timeout",
    }
    if failure in expected:
        assert expected[failure] in result["cleanup_errors"]
    assert kills == ([] if failure == "already-attempted" else [True])
    assert len(waits) == 1
    assert 0 <= waits[0] <= 0.1
    assert "private" not in str(result)


def test_late_observed_clean_exit_is_not_successful_stop(monkeypatch: pytest.MonkeyPatch) -> None:
    if os.name != "posix":
        pytest.skip("POSIX child supervisor")
    stop = threading.Event()
    clock = [time.monotonic()]
    real_select = subject.selectors.DefaultSelector.select
    out_r, out_w = os.pipe()
    err_r, err_w = os.pipe()
    os.close(out_w)
    os.close(err_w)
    with os.fdopen(out_r, "rb") as stdout, os.fdopen(err_r, "rb") as stderr:
        process = PipeProcess(stdout, stderr)

        def popen(*args: object, **kwargs: object) -> PipeProcess:
            stop.set()
            return process

        def select(
            selector: selectors.DefaultSelector, timeout: float | None
        ) -> list[tuple[selectors.SelectorKey, int]]:
            events = real_select(selector, timeout)
            clock[0] += 0.15  # Both EOF and clean exit are observed after the 0.1s grace.
            process.returncode = 0
            return events

        monkeypatch.setattr(subject.subprocess, "Popen", popen)
        monkeypatch.setattr(subject.time, "monotonic", lambda: clock[0])
        monkeypatch.setattr(subject.selectors.DefaultSelector, "select", select)
        result = subject.capture_child(
            ["/synthetic/child"], {}, stop_event=stop, cleanup_grace=0.1, timeout=5
        )
    assert result["error"] == "stop_grace_exceeded"
    assert result["returncode"] == 0
    assert result["kill_sent"] is False
    assert result["status"] == "capture_failed"


def test_sigterm_without_stop_request_is_not_graceful_stop() -> None:
    if os.name != "posix":
        pytest.skip("POSIX child supervisor")
    result = subject.capture_child(
        [
            str(Path(sys.executable).resolve()),
            "-c",
            "import os,signal; os.kill(os.getpid(),signal.SIGTERM)",
        ],
        {"PATH": os.defpath, "LANG": "C"},
        stop_event=threading.Event(),
        timeout=5,
    )
    assert result["returncode"] == -signal.SIGTERM
    assert result["error"] == "nonzero_exit"
    assert result["stop_started"] is result["stop_requested"] is False
