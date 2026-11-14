"""Bounded POSIX child capture, not model/server eligibility or study admission.

The caller must authorise the executable, arguments and explicit environment.
Only the direct child is supervised; no socket, server readiness, process-wide
egress or descendant lifecycle is verified by this primitive.
"""

from __future__ import annotations

import base64
import hashlib
import os
import selectors
import signal
import subprocess
import threading
import time
from pathlib import Path
from typing import Literal, NamedTuple, Protocol, TypedDict, cast

POSIX = os.name == "posix"


class ReapableProcess(Protocol):
    """The process operations needed to finish a bounded stop."""

    def poll(self) -> int | None: ...

    def kill(self) -> None: ...

    def wait(self, timeout: float) -> int: ...


class ProcessControl(ReapableProcess, Protocol):
    """Direct-child control, independent of a concrete subprocess implementation."""

    def terminate(self) -> None: ...


class CleanupResult(TypedDict):
    reaped: bool
    terminate_sent: bool
    kill_sent: bool
    cleanup_errors: list[str]
    returncode: int | None


class _CaptureObservation(CleanupResult):
    status: Literal["process_stopped", "process_captured", "capture_failed"]
    error: str
    execution_observed: bool
    pid: int | None
    admitted: Literal[False]
    study_unlocked: Literal[False]
    runtime_verified: Literal[False]
    stop_requested: bool
    stop_started: bool
    elapsed_seconds: float
    execution_deadline_monotonic: float
    limitations: list[str]


class CaptureResult(_CaptureObservation):
    """The complete receipt shape, including incomplete or failed captures."""

    raw_stdout_base64: str
    stdout_bytes_observed: int
    stdout_bytes_retained: int
    stdout_complete: bool
    stdout_truncated: bool
    stdout_retained_sha256: str
    stdout_sha256: str | None
    raw_stderr_base64: str
    stderr_bytes_observed: int
    stderr_bytes_retained: int
    stderr_complete: bool
    stderr_truncated: bool
    stderr_retained_sha256: str
    stderr_sha256: str | None


class _CaptureInputs(NamedTuple):
    argv: list[str]
    environment: dict[str, str]
    timeout: float
    output_limit: int
    cleanup_grace: float
    cancel: threading.Event | None
    stop_event: threading.Event | None


class _StreamResult(TypedDict):
    raw_base64: str
    bytes_observed: int
    bytes_retained: int
    complete: bool
    truncated: bool
    retained_sha256: str
    sha256: str | None


def cleanup_child(process: ProcessControl, grace: float) -> CleanupResult:
    result: CleanupResult = {
        "reaped": False,
        "terminate_sent": False,
        "kill_sent": False,
        "cleanup_errors": [],
        "returncode": None,
    }
    try:
        code = process.poll()
        if code is not None:
            return {**result, "reaped": True, "returncode": code}
    except OSError:
        result["cleanup_errors"].append("poll_failed")
    try:
        process.terminate()
        result["terminate_sent"] = True
    except OSError:
        result["cleanup_errors"].append("terminate_failed")
    try:
        code = process.wait(timeout=grace)
        return {**result, "reaped": True, "returncode": code}
    except subprocess.TimeoutExpired:
        pass
    except OSError:
        result["cleanup_errors"].append("wait_failed")
    try:
        process.kill()
        result["kill_sent"] = True
    except OSError:
        result["cleanup_errors"].append("kill_failed")
    try:
        code = process.wait(timeout=grace)
        result.update(reaped=True, returncode=code)
    except subprocess.TimeoutExpired:
        result["cleanup_errors"].append("reap_timeout")
    except OSError:
        result["cleanup_errors"].append("reap_failed")
    return result


def _validate(
    argv: object,
    environment: object,
    timeout: object,
    output_limit: object,
    cleanup_grace: object,
    cancel: object,
    stop_event: object,
) -> _CaptureInputs:
    if not POSIX:
        raise ValueError("unsupported_platform")
    if type(argv) is not list or type(environment) is not dict:
        raise ValueError("invalid_invocation")
    # Only the concrete containers are established here; inspect their elements
    # before claiming the caller's argv/environment contract.
    raw_argv = cast("list[object]", argv)
    raw_environment = cast("dict[object, object]", environment)
    if (
        not raw_argv
        or any(type(value) is not str or "\x00" in value for value in raw_argv)
        or any(
            type(key) is not str
            or not key
            or "=" in key
            or "\x00" in key
            or type(value) is not str
            or "\x00" in value
            for key, value in raw_environment.items()
        )
    ):
        raise ValueError("invalid_invocation")
    # Every element/key/value has just passed the exact string checks above.
    checked_argv = cast("list[str]", raw_argv)
    checked_environment = cast("dict[str, str]", raw_environment)
    if not Path(checked_argv[0]).is_absolute():
        raise ValueError("invalid_invocation")
    if (
        (type(timeout) is not int and type(timeout) is not float)
        or not 0 < timeout <= 120
        or (type(cleanup_grace) is not int and type(cleanup_grace) is not float)
        or not 0 < cleanup_grace <= 5
        or type(output_limit) is not int
        or not 0 < output_limit <= 1048576
        or (cancel is not None and not isinstance(cancel, threading.Event))
        or (stop_event is not None and not isinstance(stop_event, threading.Event))
    ):
        raise ValueError("invalid_capture_limits")
    return _CaptureInputs(
        checked_argv,
        checked_environment,
        timeout,
        output_limit,
        cleanup_grace,
        cancel,
        stop_event,
    )


def finish_child_stop(
    process: ReapableProcess,
    deadline: float,
    terminate_sent: bool,
    kill_attempted: bool,
    kill_sent: bool,
    errors: list[str],
) -> CleanupResult:
    """Finish within the stop budget, never resending an attempted signal."""
    result: CleanupResult = {
        "reaped": False,
        "terminate_sent": terminate_sent,
        "kill_sent": kill_sent,
        "cleanup_errors": list(errors),
        "returncode": None,
    }
    try:
        code = process.poll()
        if code is not None:
            return {**result, "reaped": True, "returncode": code}
    except OSError:
        result["cleanup_errors"].append("poll_failed")
    if not kill_attempted:
        try:
            process.kill()
            result["kill_sent"] = True
        except OSError:
            result["cleanup_errors"].append("kill_failed")
    try:
        code = process.wait(timeout=max(0, deadline - time.monotonic()))
        result.update(reaped=True, returncode=code)
    except subprocess.TimeoutExpired:
        result["cleanup_errors"].append("reap_timeout")
    except OSError:
        result["cleanup_errors"].append("reap_failed")
    return result


def capture_child(
    argv: object,
    environment: object,
    *,
    timeout: object = 60,
    output_limit: object = 1048576,
    cleanup_grace: object = 1,
    cancel: object = None,
    stop_event: object = None,
    deadline: object = None,
) -> CaptureResult:
    """Capture authorised caller-selected bytes with bounded direct-child cleanup.

    Invalid inputs raise before launch. Operational failures retain the original
    reason and separate cleanup errors. A full-stream digest requires observed
    EOF without truncation; retained-prefix digests never assert completeness.
    A stop requests TERM while draining; cancellation aborts capture. Stopped
    means observed cleanup, not proof that our signal caused the process exit.
    An absolute monotonic deadline can only shorten the relative timeout. An
    already-expired valid deadline refuses launch, including delayed workers.
    """
    argv, environment, timeout, output_limit, cleanup_grace, cancel, stop_event = _validate(
        argv, environment, timeout, output_limit, cleanup_grace, cancel, stop_event
    )
    set_blocking = getattr(os, "set_blocking", None)
    if not callable(set_blocking):
        raise ValueError("unsupported_nonblocking_pipes")
    buffers = {"stdout": bytearray(), "stderr": bytearray()}
    observed = dict.fromkeys(buffers, 0)
    eof = dict.fromkeys(buffers, False)
    truncated = dict.fromkeys(buffers, False)
    started = time.monotonic()
    if deadline is not None and (
        (type(deadline) is not int and type(deadline) is not float)
        or not 0 < deadline <= started + 120
    ):
        raise ValueError("invalid_deadline")
    deadline = min(started + timeout, deadline) if deadline is not None else started + timeout
    error = "none"
    stop_requested = stop_event is not None and stop_event.is_set()
    stop_started = False
    stop_term_deadline = stop_final_deadline = deadline
    stop_term_sent = stop_kill_attempted = stop_kill_sent = False
    stop_errors: list[str] = []
    process: subprocess.Popen[bytes] | None = None
    cleanup: CleanupResult = {
        "reaped": False,
        "terminate_sent": False,
        "kill_sent": False,
        "cleanup_errors": [],
        "returncode": None,
    }
    try:
        if cancel is not None and cancel.is_set():
            error = "cancelled"
        elif stop_requested:
            error = "stop_before_launch"
        elif time.monotonic() >= deadline:
            error = "deadline_exceeded"
        else:
            try:
                process = subprocess.Popen(
                    list(argv),
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env=dict(environment),
                    shell=False,  # nosec B603 # explicit argv capability, shell=False, bounded process lifetime
                    start_new_session=True,
                )
            except OSError:
                error = "launch_failed"
            if process is not None:
                with selectors.DefaultSelector() as selector:
                    for name, stream in (("stdout", process.stdout), ("stderr", process.stderr)):
                        if stream is None:
                            raise OSError("missing_pipe")
                        set_blocking(stream.fileno(), False)
                        selector.register(stream, selectors.EVENT_READ, name)
                    while True:
                        if cancel is not None and cancel.is_set():
                            error = error if error != "none" else "cancelled"
                            break
                        now = time.monotonic()
                        remaining = deadline - now
                        if remaining <= 0:
                            error = error if error != "none" else "deadline_exceeded"
                            break
                        code = process.poll()
                        if stop_event is not None and stop_event.is_set():
                            stop_requested = True
                            if not stop_started and code is None:
                                stop_started = True
                                stop_term_deadline = min(deadline, now + cleanup_grace)
                                stop_final_deadline = now + 2 * cleanup_grace
                                try:
                                    process.terminate()
                                    stop_term_sent = True
                                except OSError:
                                    stop_errors.append("terminate_failed")
                                    error = "stop_signal_failed"
                                    break
                        if stop_started:
                            if now >= stop_term_deadline and error == "none":
                                error = "stop_grace_exceeded"
                                if code is None:
                                    stop_kill_attempted = True
                                    try:
                                        process.kill()
                                        stop_kill_sent = True
                                    except OSError:
                                        stop_errors.append("kill_failed")
                            drain_deadline = (
                                stop_term_deadline if error == "none" else stop_final_deadline
                            )
                            remaining = min(remaining, drain_deadline - now)
                            if remaining <= 0:
                                error = error if error != "none" else "stop_grace_exceeded"
                                break
                        if all(eof.values()) and code is not None:
                            break
                        events = selector.select(min(remaining, 0.05))
                        overflow = False
                        for key, _ in events:
                            name: object = key.data
                            if not isinstance(name, str):
                                raise ValueError("invalid_pipe_name")
                            available = output_limit - len(buffers[name])
                            try:
                                chunk = os.read(key.fd, min(65536, available + 1))
                            except BlockingIOError:
                                continue
                            if not chunk:
                                eof[name] = True
                                selector.unregister(key.fileobj)
                                continue
                            observed[name] += len(chunk)
                            buffers[name].extend(chunk[:available])
                            if len(chunk) > available:
                                truncated[name] = True
                                error = error if error != "none" else "output_limit_exceeded"
                                overflow = True
                                break
                        if overflow:
                            break
    except (OSError, ValueError):
        error = "capture_io_failed" if error == "none" else error
    finally:
        if process is not None:
            if stop_started:
                cleanup = finish_child_stop(
                    process,
                    stop_final_deadline,
                    stop_term_sent,
                    stop_kill_attempted,
                    stop_kill_sent,
                    stop_errors,
                )
            else:
                cleanup = cleanup_child(process, cleanup_grace)
            for stream in (process.stdout, process.stderr):
                if stream is not None:
                    try:
                        stream.close()
                    except OSError:
                        cleanup["cleanup_errors"].append("pipe_close_failed")
    if error == "none":
        if cleanup["cleanup_errors"] or not cleanup["reaped"]:
            error = "cleanup_failed"
        elif cleanup["returncode"] not in ((0, -signal.SIGTERM) if stop_started else (0,)):
            error = "nonzero_exit"
        elif not all(eof.values()):
            error = "incomplete_output"
    result: _CaptureObservation = {
        "status": (
            ("process_stopped" if stop_started else "process_captured")
            if error == "none"
            else "capture_failed"
        ),
        "error": error,
        "execution_observed": process is not None,
        "pid": process.pid if process is not None else None,
        "admitted": False,
        "study_unlocked": False,
        "runtime_verified": False,
        "stop_requested": stop_requested,
        "stop_started": stop_started,
        "elapsed_seconds": time.monotonic() - started,
        "execution_deadline_monotonic": deadline,
        **cleanup,
        "limitations": [
            "caller-authorises-argv-and-environment",
            "direct-child-only-descendants-not-attested",
            "no-socket-readiness-or-runtime-verification",
            "os-and-egress-not-attested",
            "process-creation-and-scheduling-not-hard-real-time-bounded",
            "raw-streams-require-inspection-before-publication",
            "capture-stops-on-failure-shutdown-bytes-may-be-unretained",
            "signal-requests-not-proven-delivery-or-exit-causality",
            "not-study-admission",
        ],
    }
    streams: dict[str, _StreamResult] = {}
    for name, data in buffers.items():
        complete = (
            eof[name]
            and not truncated[name]
            and cleanup["reaped"]
            and not cleanup["cleanup_errors"]
        )
        digest = hashlib.sha256(data).hexdigest()
        streams[name] = {
            "raw_base64": base64.b64encode(data).decode("ascii"),
            "bytes_observed": observed[name],
            "bytes_retained": len(data),
            "complete": complete,
            "truncated": truncated[name],
            "retained_sha256": digest,
            "sha256": digest if complete else None,
        }
    stdout, stderr = streams["stdout"], streams["stderr"]
    return {
        **result,
        "raw_stdout_base64": stdout["raw_base64"],
        "stdout_bytes_observed": stdout["bytes_observed"],
        "stdout_bytes_retained": stdout["bytes_retained"],
        "stdout_complete": stdout["complete"],
        "stdout_truncated": stdout["truncated"],
        "stdout_retained_sha256": stdout["retained_sha256"],
        "stdout_sha256": stdout["sha256"],
        "raw_stderr_base64": stderr["raw_base64"],
        "stderr_bytes_observed": stderr["bytes_observed"],
        "stderr_bytes_retained": stderr["bytes_retained"],
        "stderr_complete": stderr["complete"],
        "stderr_truncated": stderr["truncated"],
        "stderr_retained_sha256": stderr["retained_sha256"],
        "stderr_sha256": stderr["sha256"],
    }
