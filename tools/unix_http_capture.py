"""Bounded Unix-socket HTTP observations, not runtime or study admission.

No TCP, proxies, redirects, process launch or disk writes. The caller owns server
lifecycle, request provenance and persistent receipt custody. Same-user socket
replacement and process-wide egress are not prevented by directory checks.
"""

from __future__ import annotations

import base64
import hashlib
import http.client
import os
import socket
import stat
import time
from pathlib import Path
from typing import Any

MAX_BYTES = 1024 * 1024
MAX_SECONDS = 120


def _remaining(deadline: float) -> float:
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise TimeoutError("deadline_exceeded")
    return remaining


class _DeadlineSocket(socket.socket):
    def __init__(self, deadline: float):
        family = getattr(socket, "AF_UNIX", None)
        if family is None:
            raise ValueError("unix_socket_unavailable")
        super().__init__(family, socket.SOCK_STREAM)
        self.deadline = deadline

    def recv_into(self, buffer: Any, nbytes: int = 0, flags: int = 0) -> int:
        # socket.makefile()/SocketIO uses this method for every underlying read.
        self.settimeout(_remaining(self.deadline))
        return super().recv_into(buffer, nbytes, flags)

    def sendall(self, data: Any, flags: int = 0) -> None:
        self.settimeout(_remaining(self.deadline))
        super().sendall(data, flags)


class _Connection(http.client.HTTPConnection):
    def __init__(self, path: Path, deadline: float):
        super().__init__("localhost", timeout=_remaining(deadline))
        self.path = path
        self.deadline = deadline

    def connect(self) -> None:
        self.sock = _DeadlineSocket(self.deadline)
        self.sock.settimeout(_remaining(self.deadline))
        self.sock.connect(str(self.path))


def _path_identity(path: Path) -> tuple[int, int, int, int]:
    getuid = getattr(os, "getuid", None)
    if getuid is None:
        raise ValueError("unix_identity_unavailable")
    try:
        if (
            not path.is_absolute()
            or path.resolve(strict=True) != path
            or len(os.fsencode(path)) > 100
            or path.suffix != ".sock"
        ):
            raise ValueError("unsafe_socket_path")
        parent = path.parent.stat()
        target = path.lstat()
        if (
            stat.S_IMODE(parent.st_mode) != 0o700
            or parent.st_uid != getuid()
            or not stat.S_ISSOCK(target.st_mode)
            or target.st_uid != getuid()
        ):
            raise ValueError("unsafe_socket_permissions")
        return parent.st_dev, parent.st_ino, target.st_dev, target.st_ino
    except OSError as exc:
        raise ValueError("socket_unavailable") from exc


def capture(path: Path, method: str, route: str, body: bytes, *, deadline: float) -> dict:
    """Retain a bounded HTTP body; no JSON semantics or peer identity assertion.

    Invalid caller inputs fail before connecting. Transport failures return an
    unadmitted receipt, including partial body bytes when available. Parsed
    headers are retained, not original HTTP wire header bytes.
    """
    if (
        os.name != "posix"
        or type(body) is not bytes
        or len(body) > MAX_BYTES
        or (method, route) not in {("GET", "/health"), ("POST", "/completion")}
        or (method == "GET" and body != b"")
        or (method == "POST" and not body)
    ):
        raise ValueError("unsupported_request")
    now = time.monotonic()
    if (
        type(deadline) not in (int, float)
        or not now < deadline <= now + MAX_SECONDS
    ):
        raise ValueError("invalid_deadline")
    identity = _path_identity(path)
    result: dict = {
        "status": "transport_failed",
        "error": "none",
        "transport": "unix-domain-socket",
        "method": method,
        "route": route,
        "request_body_sha256": hashlib.sha256(body).hexdigest(),
        "http_status": None,
        "headers": [],
        "body_complete": False,
        "admitted": False,
        "study_unlocked": False,
        "limitations": [
            "peer-process-not-attested",
            "same-user-replacement-not-prevented",
            "request-origin-and-runtime-not-verified",
            "parsed-not-wire-headers",
            "process-lifecycle-and-egress-not-controlled",
            "not-study-admission",
        ],
    }
    data = bytearray()
    connection: _Connection | None = None
    try:
        connection = _Connection(path, deadline)
        connection.request(
            method,
            route,
            body=body,
            headers={
                "Content-Type": "application/json",
                "Accept": "application/json",
                "Connection": "close",
            },
        )
        with connection.getresponse() as response:
            result["http_status"] = response.status
            result["headers"] = response.getheaders()
            lengths = response.headers.get_all("Content-Length", [])
            types = response.headers.get_all("Content-Type", [])
            if (
                response.headers.defects
                or len(lengths) != 1
                or not lengths[0].isascii()
                or not lengths[0].isdigit()
                or len(lengths[0]) > 8
                or int(lengths[0]) > MAX_BYTES
                or len(types) != 1
                or types[0].split(";")[0].strip().lower() != "application/json"
                or "Transfer-Encoding" in response.headers
                or "Content-Encoding" in response.headers
            ):
                raise ValueError("unsupported_http_framing")
            expected = int(lengths[0])
            while len(data) < expected:
                _remaining(deadline)
                part = response.read1(min(65536, expected - len(data)))
                if not part:
                    raise ValueError("incomplete_body")
                data.extend(part)
            _remaining(deadline)
            result["body_complete"] = True
            if _path_identity(path) != identity:
                raise ValueError("socket_changed")
            if response.status != 200:
                raise ValueError("http_status_rejected")
            result["status"] = "http_response_captured"
    except TimeoutError:
        result["error"] = "deadline_exceeded"
    except http.client.HTTPException:
        result["error"] = "http_protocol_error"
    except OSError:
        result["error"] = "socket_io_failed"
    except ValueError as exc:
        result["error"] = str(exc)
    finally:
        if connection is not None:
            connection.close()
    result.update(
        {
            "body_base64": base64.b64encode(data).decode("ascii"),
            "body_sha256": hashlib.sha256(data).hexdigest(),
            "body_bytes": len(data),
        }
    )
    return result
