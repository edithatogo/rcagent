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
from typing import Any

POSIX = os.name == "posix"


def _cleanup(process: Any, grace: float) -> dict:
    result: dict = {
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
    argv: list[str],
    environment: dict[str, str],
    timeout: float,
    output_limit: int,
    cleanup_grace: float,
    cancel: threading.Event | None,
    stop_event: threading.Event | None,
) -> None:
    if not POSIX:
        raise ValueError("unsupported_platform")
    if (
        type(argv) is not list
        or not argv
        or any(type(value) is not str or "\x00" in value for value in argv)
        or not Path(argv[0]).is_absolute()
        or type(environment) is not dict
        or any(
            type(key) is not str
            or not key
            or "=" in key
            or "\x00" in key
            or type(value) is not str
            or "\x00" in value
            for key, value in environment.items()
        )
    ):
        raise ValueError("invalid_invocation")
    if (
        type(timeout) not in (int, float)
        or not 0 < timeout <= 120
        or type(cleanup_grace) not in (int, float)
        or not 0 < cleanup_grace <= 5
        or type(output_limit) is not int
        or not 0 < output_limit <= 1048576
        or (cancel is not None and not isinstance(cancel, threading.Event))
        or (stop_event is not None and not isinstance(stop_event, threading.Event))
    ):
        raise ValueError("invalid_capture_limits")


def _finish_stop(
    process: Any,
    deadline: float,
    terminate_sent: bool,
    kill_attempted: bool,
    kill_sent: bool,
    errors: list[str],
) -> dict:
    """Finish within the stop budget, never resending an attempted signal."""
    result: dict = {
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
    argv: list[str],
    environment: dict[str, str],
    *,
    timeout: float = 60,
    output_limit: int = 1048576,
    cleanup_grace: float = 1,
    cancel: threading.Event | None = None,
    stop_event: threading.Event | None = None,
) -> dict:
    """Capture authorised caller-selected bytes with bounded direct-child cleanup.

    Invalid inputs raise before launch. Operational failures retain the original
    reason and separate cleanup errors. A full-stream digest requires observed
    EOF without truncation; retained-prefix digests never assert completeness.
    A stop requests TERM while draining; cancellation aborts capture. Stopped
    means observed cleanup, not proof that our signal caused the process exit.
    """
    _validate(argv, environment, timeout, output_limit, cleanup_grace, cancel, stop_event)
    set_blocking = getattr(os, "set_blocking", None)
    if not callable(set_blocking):
        raise ValueError("unsupported_nonblocking_pipes")
    buffers = {"stdout": bytearray(), "stderr": bytearray()}
    observed = {name: 0 for name in buffers}
    eof = {name: False for name in buffers}
    truncated = {name: False for name in buffers}
    started = time.monotonic()
    deadline = started + timeout
    error = "none"
    stop_requested = stop_event is not None and stop_event.is_set()
    stop_started = False
    stop_term_deadline = stop_final_deadline = deadline
    stop_term_sent = stop_kill_attempted = stop_kill_sent = False
    stop_errors: list[str] = []
    process: subprocess.Popen[bytes] | None = None
    cleanup: dict = {
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
        else:
            try:
                process = subprocess.Popen(
                    list(argv),
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    env=dict(environment),
                    shell=False,
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
                            name = key.data
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
                cleanup = _finish_stop(
                    process,
                    stop_final_deadline,
                    stop_term_sent,
                    stop_kill_attempted,
                    stop_kill_sent,
                    stop_errors,
                )
            else:
                cleanup = _cleanup(process, cleanup_grace)
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
    result = {
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
    for name, data in buffers.items():
        complete = (
            eof[name]
            and not truncated[name]
            and cleanup["reaped"]
            and not cleanup["cleanup_errors"]
        )
        digest = hashlib.sha256(data).hexdigest()
        result.update(
            {
                f"raw_{name}_base64": base64.b64encode(data).decode("ascii"),
                f"{name}_bytes_observed": observed[name],
                f"{name}_bytes_retained": len(data),
                f"{name}_complete": complete,
                f"{name}_truncated": truncated[name],
                f"{name}_retained_sha256": digest,
                f"{name}_sha256": digest if complete else None,
            }
        )
    return result
