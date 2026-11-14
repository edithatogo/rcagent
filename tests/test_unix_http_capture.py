"""Synthetic local sockets only, never an inference server."""

import base64
import hashlib
import http.client
import os
import socket
import tempfile
import threading
import time
from collections.abc import Iterator
from pathlib import Path
from typing import Never

import pytest

from tools import unix_http_capture as subject

pytestmark = pytest.mark.skipif(os.name != "posix", reason="Unix-only transport")


class Server:
    def __init__(self, directory: Path) -> None:
        self.directory = directory
        self.listeners: list[socket.socket] = []
        self.threads: list[threading.Thread] = []
        self.requests: list[tuple[bytes, bytes]] = []

    def __call__(self, response: bytes | list[bytes], delay: float = 0) -> Path:
        path = self.directory / f"{len(self.listeners)}.sock"
        family = getattr(socket, "AF_UNIX", None)
        assert family is not None
        listener = socket.socket(family, socket.SOCK_STREAM)
        listener.bind(str(path))
        listener.listen(1)
        listener.settimeout(2)
        self.listeners.append(listener)

        def serve() -> None:
            try:
                conn, _ = listener.accept()
                with conn:
                    conn.settimeout(2)
                    request = b""
                    while b"\r\n\r\n" not in request:
                        data = conn.recv(4096)
                        if not data:
                            return
                        request += data
                    header, payload = request.split(b"\r\n\r\n", 1)
                    length = next(
                        int(line.split(b":", 1)[1])
                        for line in header.split(b"\r\n")
                        if line.lower().startswith(b"content-length:")
                    )
                    while len(payload) < length:
                        data = conn.recv(length - len(payload))
                        if not data:
                            return
                        payload += data
                    self.requests.append((header, payload))
                    chunks = [response] if isinstance(response, bytes) else response
                    for chunk in chunks:
                        if delay:
                            time.sleep(delay)
                        conn.sendall(chunk)
            except OSError:
                pass

        thread = threading.Thread(target=serve, daemon=True)
        thread.start()
        self.threads.append(thread)
        return path


@pytest.fixture
def server() -> Iterator[Server]:
    with tempfile.TemporaryDirectory(prefix="rca-", dir="/tmp") as name:
        instance = Server(Path(name).resolve())
        yield instance
        for listener in instance.listeners:
            listener.close()
        for thread in instance.threads:
            thread.join(3)
            assert not thread.is_alive()


def wire(body: bytes = b'{"synthetic": true}\n', status: int = 200, extra: bytes = b"") -> bytes:
    return (
        f"HTTP/1.1 {status} Synthetic\r\nContent-Type: application/json\r\nContent-Length: {len(body)}\r\n".encode()
        + extra
        + b"\r\n"
        + body
    )


def capture(path: Path) -> subject.CaptureResult:
    return subject.capture(path, "GET", "/health", b"", deadline=time.monotonic() + 2)


def test_exact_body_and_locked_receipt(server: Server, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("HTTP_PROXY", "http://invalid.example:1")
    raw = b' {"synthetic": "a\\n"} \r\n'
    result = capture(server(wire(raw)))
    assert result["status"] == "http_response_captured"
    assert result["body_complete"] is True
    assert base64.b64decode(result["body_base64"]) == raw
    assert result["body_sha256"] == hashlib.sha256(raw).hexdigest()
    assert result["admitted"] is result["study_unlocked"] is False
    assert result["transport"] == "unix-domain-socket"


def test_post_request_bound_by_digest(server: Server) -> None:
    body = b'{"prompt":"synthetic"}'
    result = subject.capture(
        server(wire()), "POST", "/completion", body, deadline=time.monotonic() + 2
    )
    assert result["request_body_sha256"] == hashlib.sha256(body).hexdigest()
    assert result["status"] == "http_response_captured"
    header, received = server.requests[0]
    assert header.startswith(b"POST /completion HTTP/1.1\r\n")
    assert b"Host: localhost" in header
    assert received == body


@pytest.mark.parametrize("status", [301, 400, 500])
def test_http_error_preserves_body_without_following_redirect(server: Server, status: int) -> None:
    result = capture(server(wire(status=status, extra=b"Location: http://invalid.example\r\n")))
    assert result["status"] == "transport_failed"
    assert result["error"] == "http_status_rejected"
    assert result["body_complete"] is True
    assert result["http_status"] == status


@pytest.mark.parametrize(
    "headers",
    [
        b"Content-Type: application/json\r\n",
        b"Content-Length: 2\r\n",
        b"Content-Type: text/plain\r\nContent-Length: 2\r\n",
        b"Content-Type: application/json\r\nContent-Length: -1\r\n",
        b"Content-Type: application/json\r\nContent-Length: 9999999\r\n",
        b"Content-Type: application/json\r\nContent-Length: 2\r\nContent-Length: 2\r\n",
        b"Content-Type: application/json\r\nContent-Type: application/json\r\nContent-Length: 2\r\n",
        b"Content-Type: application/json\r\nContent-Length: 2\r\nTransfer-Encoding: chunked\r\n",
        b"Content-Type: application/json\r\nContent-Length: 2\r\nContent-Encoding: gzip\r\n",
    ],
)
def test_ambiguous_framing_rejected(server: Server, headers: bytes) -> None:
    result = capture(server(b"HTTP/1.1 200 OK\r\n" + headers + b"\r\n{}"))
    assert result["status"] == "transport_failed"
    assert result["body_complete"] is False


def test_short_body_retained(server: Server) -> None:
    result = capture(
        server(b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: 10\r\n\r\n{}")
    )
    assert result["error"] == "incomplete_body"
    assert base64.b64decode(result["body_base64"]) == b"{}"


def test_bad_http(server: Server) -> None:
    assert capture(server(b"not HTTP\r\n"))["error"] == "http_protocol_error"


def test_absolute_deadline_stops_trickling_headers(server: Server) -> None:
    path = server([b"HTTP/1.1 200 OK\r\n", b"X-A: a\r\n"] * 8, delay=0.025)
    start = time.monotonic()
    result = subject.capture(path, "GET", "/health", b"", deadline=start + 0.12)
    assert result["error"] == "deadline_exceeded"
    assert time.monotonic() - start < 1


def test_body_deadline_retains_partial_bytes(
    server: Server, monkeypatch: pytest.MonkeyPatch
) -> None:
    headers = b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: 100\r\n\r\n"
    path = server(headers + b"abc")
    original = subject.http.client.HTTPResponse.read1
    calls: list[bool] = []

    def read1(response: http.client.HTTPResponse, amount: int) -> bytes:
        if calls:
            raise TimeoutError
        calls.append(True)
        return original(response, amount)

    monkeypatch.setattr(subject.http.client.HTTPResponse, "read1", read1)
    result = capture(path)
    assert result["error"] == "deadline_exceeded"
    assert base64.b64decode(result["body_base64"]) == b"abc"


@pytest.mark.parametrize(
    ("method", "route", "body"),
    [
        ("GET", "/completion", b""),
        ("POST", "/health", b"{}"),
        ("GET", "http://example.invalid", b""),
        ("GET", "/health", b"{}"),
        ("POST", "/completion", b""),
        ("POST", "/completion", "{}"),
        ("POST", "/completion", b"x" * (subject.MAX_BYTES + 1)),
    ],
    ids=[
        "get-completion",
        "post-health",
        "remote-route",
        "health-body",
        "empty-completion",
        "text-not-bytes",
        "oversized-body",
    ],
)
def test_bad_request_fails_before_connection(
    tmp_path: Path, method: object, route: object, body: object
) -> None:
    with pytest.raises(ValueError):
        subject.capture(
            tmp_path / "missing.sock", method, route, body, deadline=time.monotonic() + 1
        )


@pytest.mark.parametrize(
    ("method", "route"),
    [([], "/health"), ({}, "/health"), ("GET", []), ("GET", {})],
    ids=["list-method", "dict-method", "list-route", "dict-route"],
)
def test_unhashable_request_fields_reject_before_connection(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path, method: object, route: object
) -> None:
    def unexpected_connection(*_args: object) -> Never:
        pytest.fail("connected")

    monkeypatch.setattr(subject, "_Connection", unexpected_connection)
    with pytest.raises(ValueError, match=r"^unsupported_request$"):
        subject.capture(
            tmp_path / "missing.sock", method, route, b"", deadline=time.monotonic() + 1
        )


@pytest.mark.parametrize(
    "deadline",
    [0, float("inf"), float("nan"), True, "1", 10**1000],
    ids=["expired", "infinite", "nan", "boolean", "string", "oversized-integer"],
)
def test_invalid_deadline(deadline: object, tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        subject.capture(tmp_path / "missing.sock", "GET", "/health", b"", deadline=deadline)


def test_unsafe_paths(tmp_path: Path) -> None:
    regular = tmp_path / "file.sock"
    regular.write_bytes(b"synthetic")
    for path in (Path("relative.sock"), regular, tmp_path / "missing.sock"):
        with pytest.raises(ValueError):
            capture(path)


def test_shared_directory_rejected(server: Server) -> None:
    path = server(wire())
    path.parent.chmod(0o755)
    try:
        with pytest.raises(ValueError):
            capture(path)
    finally:
        path.parent.chmod(0o700)


def test_expired_remaining_time() -> None:
    with pytest.raises(TimeoutError):
        subject.remaining_seconds(time.monotonic() - 1)


def test_connection_setup_expiry_returns_receipt(
    server: Server, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = server(wire())

    def fail(*args: object) -> Never:
        raise TimeoutError

    monkeypatch.setattr(subject, "_Connection", fail)
    result = capture(path)
    assert result["error"] == "deadline_exceeded"
    assert result["body_complete"] is False


def test_connect_failure_returns_receipt() -> None:
    with tempfile.TemporaryDirectory(prefix="rca-", dir="/tmp") as name:
        path = Path(name).resolve() / "closed.sock"
        family = getattr(socket, "AF_UNIX", None)
        assert family is not None
        with socket.socket(family, socket.SOCK_STREAM) as listener:
            listener.bind(str(path))
        assert capture(path)["error"] == "socket_io_failed"


def test_socket_replacement_rejected(server: Server, monkeypatch: pytest.MonkeyPatch) -> None:
    path = server(wire())
    real = subject.socket_identity
    calls: list[tuple[int, int, int, int]] = []

    def identity(path: Path) -> tuple[int, int, int, int]:
        value = real(path)
        calls.append(value)
        return value if len(calls) == 1 else (0, 0, 0, 0)

    monkeypatch.setattr(subject, "socket_identity", identity)
    result = capture(path)
    assert result["error"] == "socket_changed"
    assert result["body_complete"] is True


def test_socket_symlink_and_foreign_owner_rejected(
    server: Server, monkeypatch: pytest.MonkeyPatch
) -> None:
    path = server(wire())
    link = path.with_name("link.sock")
    link.symlink_to(path)
    with pytest.raises(ValueError):
        capture(link)
    monkeypatch.setattr(subject.os, "getuid", lambda: -1)
    with pytest.raises(ValueError):
        capture(path)


def test_http_header_line_bound(server: Server) -> None:
    raw = b"HTTP/1.1 200 OK\r\nX-Large: " + b"x" * 65536 + b"\r\n\r\n"
    assert capture(server(raw))["error"] == "http_protocol_error"


def test_malformed_header_not_silently_ignored(server: Server) -> None:
    result = capture(server(wire(extra=b"not-a-header\r\n")))
    assert result["error"] == "unsupported_http_framing"


def test_absent_unix_capabilities_never_fall_back(
    monkeypatch: pytest.MonkeyPatch, tmp_path: Path
) -> None:
    monkeypatch.setattr(socket, "AF_UNIX", None)
    with pytest.raises(ValueError, match="unix_socket_unavailable"):
        subject.DeadlineSocket(time.monotonic() + 1)
    monkeypatch.setattr(os, "getuid", None)
    with pytest.raises(ValueError, match="unix_identity_unavailable"):
        subject.socket_identity(tmp_path / "missing.sock")
