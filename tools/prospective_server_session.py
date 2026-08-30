"""Fixed synthetic non-study server session; no CLI or study admission.

Only the reviewed model/profile, Unix socket and native completion contracts are
composed. Raw local receipts may contain paths and require publication review.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import platform
import stat
import tempfile
import threading
import time
from pathlib import Path

from tools import darwin_runtime_profile as core
from tools import darwin_runtime_v030 as cli_profile
from tools import darwin_server_v030 as profile
from tools import (
    evaluation_preflight,
    local_model_comparator,
    prospective_inventory,
    prospective_model,
    prospective_protocol,
)
from tools import native_completion as native
from tools import prospective_server_model as model
from tools import server_process as process
from tools import unix_http_capture as transport

PROMPT = "This is a synthetic software capability probe. Reply with the word READY."
TIMEOUT = 120
CLEANUP_GRACE = 1
JOIN_SECONDS = 2 * CLEANUP_GRACE + 1
HEALTH_ATTEMPTS = 60
HEALTH_BYTES = 4096
REQUEST = json.dumps(
    {
        "prompt": PROMPT,
        "n_predict": 512,
        "seed": 42,
        "temperature": 0,
        "stream": False,
        "ignore_eos": False,
        "stop": [],
    },
    sort_keys=True,
    separators=(",", ":"),
).encode()
_LOCK = threading.Lock()
_BLOCKED = False
SAFE_REASONS = frozenset(
    {
        "profile_identity_mismatch",
        "unsafe_session_directory",
        "session_socket_changed",
        "session_directory_changed",
        "receipt_identity_changed",
        "worker_ended_before_completion",
        "session_deadline_exceeded",
        "health_body_too_large",
        "health_transport_failed",
        "health_not_ready",
        "health_attempts_exhausted",
        "completion_transport_failed",
        "completion_request_mismatch",
        "transport_body_mismatch",
        "unsafe_socket_path",
        "unsafe_socket_permissions",
        "socket_unavailable",
        "duplicate_json_key",
        "invalid_completion_json",
        "incomplete_generation",
        "generation_settings_mismatch",
    }
)


def source_pins() -> dict[str, str]:
    paths = [Path(__file__)]
    for module in (
        core,
        cli_profile,
        profile,
        model,
        prospective_model,
        prospective_protocol,
        prospective_inventory,
        evaluation_preflight,
        local_model_comparator,
        process,
        transport,
        native,
    ):
        if not isinstance(module.__file__, str):
            raise ValueError("source_unavailable")
        paths.append(Path(module.__file__))
    return {path.name: hashlib.sha256(path.read_bytes()).hexdigest() for path in paths}


def _directory(path: Path) -> tuple[int, int]:
    getuid = getattr(os, "getuid", None)
    if not callable(getuid) or path.resolve(strict=True) != path or path.is_symlink():
        raise ValueError("unsafe_session_directory")
    value = path.stat()
    if (
        not stat.S_ISDIR(value.st_mode)
        or stat.S_IMODE(value.st_mode) != 0o700
        or value.st_uid != getuid()
    ):
        raise ValueError("unsafe_session_directory")
    return value.st_dev, value.st_ino


def _socket(
    path: Path, directory: tuple[int, int], expected: tuple[int, int, int, int] | None
) -> tuple[int, int, int, int]:
    identity = transport._path_identity(path)
    if identity[:2] != directory or (expected is not None and identity != expected):
        raise ValueError("session_socket_changed")
    return identity


def _remove_owned(
    path: Path, directory: tuple[int, int], expected: tuple[int, int, int, int] | None
) -> None:
    if _directory(path.parent) != directory:
        raise ValueError("session_directory_changed")
    if path.exists() or path.is_symlink():
        if expected is None:
            raise ValueError("unobserved_socket_preserved")
        _socket(path, directory, expected)
        path.unlink()
    path.parent.rmdir()  # Never recursively remove unexpected contents.


def _body(receipt: dict) -> bytes:
    raw = base64.b64decode(receipt["body_base64"], validate=True)
    if (
        len(raw) != receipt["body_bytes"]
        or hashlib.sha256(raw).hexdigest() != receipt["body_sha256"]
    ):
        raise ValueError("transport_body_mismatch")
    return raw


def _healthy(receipt: dict) -> bool:
    if receipt["body_bytes"] > HEALTH_BYTES:
        raise ValueError("health_body_too_large")
    value = json.loads(
        _body(receipt), object_pairs_hook=native._pairs, parse_constant=native._constant
    )
    if receipt["status"] != "http_response_captured":
        if receipt["http_status"] == 503 and receipt["body_complete"]:
            return False
        raise ValueError("health_transport_failed")
    if value != {"status": "ok"}:
        raise ValueError("health_not_ready")
    return True


def _fixed_arguments(admission: dict, path: Path) -> list[str]:
    return [
        profile.EXECUTABLE,
        "-m",
        admission["model_path"],
        "--host",
        str(path),
        "--ctx-size",
        "2048",
        "--parallel",
        "1",
        "--alias",
        model.MODEL_ID,
        "--offline",
        "--no-agent",
        "--no-ui",
        "--no-ui-mcp-proxy",
    ]


def _reserved(destination: Path, descriptor: int, parent: tuple[int, int]) -> None:
    if any(path.is_symlink() for path in (destination, *destination.parents)):
        raise ValueError("receipt_identity_changed")
    current_parent = destination.parent.stat()
    current, reserved = destination.stat(), os.fstat(descriptor)
    if (
        (current_parent.st_dev, current_parent.st_ino) != parent
        or (current.st_dev, current.st_ino) != (reserved.st_dev, reserved.st_ino)
        or not stat.S_ISREG(current.st_mode)
        or stat.S_IMODE(current.st_mode) != 0o600
    ):
        raise ValueError("receipt_identity_changed")


def _run(
    model_root: Path, destination: Path, descriptor: int, parent: tuple[int, int], primary=None
) -> dict:
    global _BLOCKED
    result: dict = {
        "status": "session_failed",
        "error": "none",
        "admitted": False,
        "study_unlocked": False,
        "worker_joined": False,
        "resources_removed": False,
        "health": [],
        "cleanup_errors": [],
        "limitations": [
            "non-study-fixed-synthetic-probe",
            "source-observation-not-freeze",
            "peer-process-not-authenticated",
            "same-user-replacement-races-not-prevented",
            "direct-child-only",
            "os-and-egress-not-attested",
            "join-cannot-force-an-os-blocked-thread",
            "circuit-breaker-is-process-local",
            "raw-receipt-requires-publication-review",
        ],
    }
    if (platform.system(), platform.machine()) != ("Darwin", "arm64"):
        return {**result, "error": "unsupported_platform"}
    request = REQUEST
    if primary is not None:
        request = base64.b64decode(
            primary.plan.value()["request"]["request"]["base64"], validate=True
        )
        result["limitations"][0] = "guarded-primary-observation-not-admitted"
    worker: threading.Thread | None = None
    worker_attempted = False
    path: Path | None = None
    directory: tuple[int, int] | None = None
    identity: tuple[int, int, int, int] | None = None
    stop, cancel, done = threading.Event(), threading.Event(), threading.Event()
    handoff: dict = {}
    pins: dict = {}
    admission: dict = {}
    profile_pin = ""
    stage = "preflight_failed"
    try:
        pins = source_pins()
        admission = (
            model.admit_model(model_root) if primary is None else primary.plan.value()["admission"]
        )
        profile_pin = profile.profile_digest()
        if admission["profile_sha256"] != profile_pin:
            raise ValueError("profile_identity_mismatch")
        result.update(
            admission=admission,
            source_sha256=pins,
            profile_sha256=profile_pin,
            request_base64=base64.b64encode(request).decode(),
            request_sha256=hashlib.sha256(request).hexdigest(),
        )
        path = Path(tempfile.mkdtemp(prefix="rca-session-", dir="/tmp")).resolve() / "server.sock"
        result["socket_path"] = str(path)
        directory = _directory(path.parent)
        deadline = time.monotonic() + TIMEOUT
        result["execution_deadline_monotonic"] = deadline
        argv = _fixed_arguments(admission, path)
        environment = profile.profile_environment()
        result.update(
            arguments=argv,
            environment_sha256=hashlib.sha256(
                json.dumps(environment, sort_keys=True).encode()
            ).hexdigest(),
            environment_keys=sorted(environment),
        )
        _reserved(destination, descriptor, parent)

        def capture() -> None:
            try:
                handoff["process"] = process.capture_child(
                    argv,
                    environment,
                    timeout=TIMEOUT,
                    deadline=deadline,
                    cleanup_grace=CLEANUP_GRACE,
                    stop_event=stop,
                    cancel=cancel,
                )
            except BaseException:
                handoff["error"] = "worker_exception"
            finally:
                done.set()

        worker = threading.Thread(target=capture, name="rcagent-fixed-session", daemon=False)
        stage = "worker_start_failed"
        worker_attempted = True
        worker.start()
        stage = "readiness_failed"
        health_attempts = 0
        while health_attempts < HEALTH_ATTEMPTS:
            if done.is_set():
                raise ValueError("worker_ended_before_completion")
            if time.monotonic() >= deadline:
                raise ValueError("session_deadline_exceeded")
            if _directory(path.parent) != directory:
                raise ValueError("session_directory_changed")
            if not path.exists() and not path.is_symlink():
                done.wait(min(0.1, max(0, deadline - time.monotonic())))
                continue
            identity = _socket(path, directory, identity)
            health_attempts += 1
            health = transport.capture(
                path, "GET", "/health", b"", deadline=min(deadline, time.monotonic() + 2)
            )
            _socket(path, directory, identity)
            result["health"].append(
                {
                    key: health[key]
                    for key in (
                        "status",
                        "error",
                        "http_status",
                        "body_complete",
                        "body_sha256",
                        "body_bytes",
                    )
                }
            )
            if health["body_bytes"] <= HEALTH_BYTES:
                result["health"][-1]["body_base64"] = health["body_base64"]
            if _healthy(health):
                break
            done.wait(min(0.1, max(0, deadline - time.monotonic())))
        else:
            raise ValueError("health_attempts_exhausted")
        stage = "completion_failed"
        if done.is_set():
            raise ValueError("worker_ended_before_completion")
        _socket(path, directory, identity)
        completion = transport.capture(path, "POST", "/completion", request, deadline=deadline)
        result["completion"] = completion
        _socket(path, directory, identity)
        if completion["status"] != "http_response_captured" or not completion["body_complete"]:
            raise ValueError("completion_transport_failed")
        if completion["request_body_sha256"] != hashlib.sha256(request).hexdigest():
            raise ValueError("completion_request_mismatch")
        result["decoded"] = native.decode_completion(
            _body(completion), expected_model=model.MODEL_ID
        )
        stage = "postflight_failed"
    except (ValueError, OSError, RuntimeError, KeyError, TypeError) as exc:
        reason = str(exc)
        result["error"] = reason if reason in SAFE_REASONS else stage
        result["failure_stage"] = stage
        if reason in {
            "unsafe_session_directory",
            "session_socket_changed",
            "session_directory_changed",
            "receipt_identity_changed",
            "unsafe_socket_path",
            "unsafe_socket_permissions",
        }:
            cancel.set()
        else:
            stop.set()
    except (KeyboardInterrupt, SystemExit):
        result["error"] = "session_interrupted"
        result["failure_stage"] = stage
        cancel.set()
    finally:
        stop.set()
        if worker is not None and worker_attempted:
            try:
                worker.join(JOIN_SECONDS)
                result["worker_joined"] = not worker.is_alive()
            except (RuntimeError, OSError, KeyboardInterrupt, SystemExit):
                result["worker_joined"] = False
            if not result["worker_joined"]:
                cancel.set()
                _BLOCKED = True
                result["cleanup_errors"].append("worker_join_failed")
            elif "process" in handoff:
                result["process"] = handoff["process"]
            else:
                _BLOCKED = True
                result["cleanup_errors"].append("worker_receipt_unavailable")
            if "error" in handoff:
                result["worker_error"] = handoff["error"]
        elif worker is None or not worker_attempted:
            result["worker_joined"] = True
        child = result.get("process", {})
        safe = result["worker_joined"] and (
            child.get("reaped") is True
            or child.get("execution_observed") is False
            or not worker_attempted
        )
        if worker_attempted and not safe:
            _BLOCKED = True
            result["cleanup_errors"].append("child_reaping_unverified")
        if path is not None and directory is not None and safe:
            try:
                _remove_owned(path, directory, identity)
                result["resources_removed"] = True
            except (ValueError, OSError):
                result["cleanup_errors"].append("socket_resources_preserved")
    if result["error"] == "none":
        try:
            child = result["process"]
            if (
                result["cleanup_errors"]
                or child["status"] != "process_stopped"
                or not child["reaped"]
                or child["cleanup_errors"]
                or not child["stdout_complete"]
                or not child["stderr_complete"]
            ):
                raise ValueError("process_incomplete")
            raw = base64.b64decode(child["raw_stderr_base64"], validate=True)
            images = profile.verify_loaded_images(raw)
            pids = {
                match[1]
                for line in raw.decode("utf-8").splitlines()
                if (match := core.IMAGE_LINE.fullmatch(line)) is not None
            }
            if pids != {str(child["pid"])}:
                raise ValueError("loader_pid_mismatch")
            if (
                model.admit_model(model_root) != admission
                or profile.profile_digest() != profile_pin
                or source_pins() != pins
            ):
                raise ValueError("postflight_identity_changed")
            result["loaded_non_system_images"] = images
            result["status"] = "session_captured"
        except (ValueError, OSError, KeyError, TypeError):
            result["error"] = "postflight_failed"
    return result


def capture_session(model_root: Path, receipt: Path) -> dict:
    """Reserve a private receipt before the fixed non-study session; never overwrite."""
    return _capture_session(model_root, receipt)


def _capture_session(model_root: Path, receipt: Path, primary=None) -> dict:
    """Private shared lifecycle; primary context is created only by its guarded entry."""
    if not _LOCK.acquire(blocking=False):
        raise ValueError("session_already_running")
    try:
        if _BLOCKED:
            raise ValueError("session_circuit_breaker")
        if primary is not None:
            primary.verify()
        if ".." in receipt.parts:
            raise ValueError("unsafe_receipt_path")
        destination = receipt.absolute()
        if (
            any(path.is_symlink() for path in (destination, *destination.parents))
            or destination.parent.resolve(strict=True) != destination.parent
        ):
            raise ValueError("unsafe_receipt_path")
        parent_info = destination.parent.stat()
        parent = parent_info.st_dev, parent_info.st_ino
        try:
            descriptor = os.open(destination, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        except OSError as exc:
            raise ValueError("receipt_unavailable") from exc
        try:
            with os.fdopen(descriptor, "wb") as stream:
                _reserved(destination, descriptor, parent)
                result = (
                    _run(model_root, destination, descriptor, parent)
                    if primary is None
                    else _run(model_root, destination, descriptor, parent, primary)
                )
                if primary is not None:
                    primary.finish(result)
                try:
                    _reserved(destination, descriptor, parent)
                except (ValueError, OSError):
                    result["error"] = (
                        result["error"] if result["error"] != "none" else "receipt_identity_changed"
                    )
                    result["status"] = "session_failed"
                stream.write((json.dumps(result, indent=2, sort_keys=True) + "\n").encode("utf-8"))
                stream.flush()
                _reserved(destination, descriptor, parent)
        except OSError:
            raise ValueError("receipt_persistence_failed") from None
        return result
    finally:
        _LOCK.release()
