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
from typing import TYPE_CHECKING, Literal, TypedDict

if TYPE_CHECKING:
    from _typeshed import ReadableBuffer, WriteableBuffer

MAX_BYTES = 1024 * 1024
MAX_SECONDS = 120


class _ResponseObservation(TypedDict):
    status: Literal["http_response_captured", "transport_failed"]
    error: str
    transport: Literal["unix-domain-socket"]
    method: str
    route: str
    request_body_sha256: str
    http_status: int | None
    headers: list[tuple[str, str]]
    body_complete: bool
    admitted: Literal[False]
    study_unlocked: Literal[False]
    limitations: list[str]


class CaptureResult(_ResponseObservation):
    """A bounded HTTP observation, including retained partial response bytes."""

    body_base64: str
    body_sha256: str
    body_bytes: int


def remaining_seconds(deadline: float) -> float:
    remaining = deadline - time.monotonic()
    if remaining <= 0:
        raise TimeoutError("deadline_exceeded")
    return remaining


class DeadlineSocket(socket.socket):
    def __init__(self, deadline: float):
        family = getattr(socket, "AF_UNIX", None)
        if family is None:
            raise ValueError("unix_socket_unavailable")
        super().__init__(family, socket.SOCK_STREAM)
        self.deadline = deadline

    def recv_into(self, buffer: WriteableBuffer, nbytes: int = 0, flags: int = 0) -> int:
        # socket.makefile()/SocketIO uses this method for every underlying read.
        self.settimeout(remaining_seconds(self.deadline))
        return super().recv_into(buffer, nbytes, flags)

    def sendall(self, data: ReadableBuffer, flags: int = 0) -> None:
        self.settimeout(remaining_seconds(self.deadline))
        super().sendall(data, flags)


class _Connection(http.client.HTTPConnection):
    def __init__(self, path: Path, deadline: float):
        super().__init__("localhost", timeout=remaining_seconds(deadline))
        self.path = path
        self.deadline = deadline

    def connect(self) -> None:
        self.sock = DeadlineSocket(self.deadline)
        self.sock.settimeout(remaining_seconds(self.deadline))
        self.sock.connect(str(self.path))


def socket_identity(path: Path) -> tuple[int, int, int, int]:
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


def capture(
    path: Path, method: object, route: object, body: object, *, deadline: object
) -> CaptureResult:
    """Retain a bounded HTTP body; no JSON semantics or peer identity assertion.

    Invalid caller inputs fail before connecting. Transport failures return an
    unadmitted receipt, including partial body bytes when available. Parsed
    headers are retained, not original HTTP wire header bytes.
    """
    if (
        os.name != "posix"
        or type(body) is not bytes
        or len(body) > MAX_BYTES
        or not isinstance(method, str)
        or not isinstance(route, str)
        or (method, route) not in {("GET", "/health"), ("POST", "/completion")}
        or (method == "GET" and body != b"")
        or (method == "POST" and not body)
    ):
        raise ValueError("unsupported_request")
    now = time.monotonic()
    if (
        type(deadline) is not int and type(deadline) is not float
    ) or not now < deadline <= now + MAX_SECONDS:
        raise ValueError("invalid_deadline")
    identity = socket_identity(path)
    result: _ResponseObservation = {
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
                remaining_seconds(deadline)
                part = response.read1(min(65536, expected - len(data)))
                if not part:
                    raise ValueError("incomplete_body")
                data.extend(part)
            remaining_seconds(deadline)
            result["body_complete"] = True
            if socket_identity(path) != identity:
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
    return {
        **result,
        "body_base64": base64.b64encode(data).decode("ascii"),
        "body_sha256": hashlib.sha256(data).hexdigest(),
        "body_bytes": len(data),
    }
