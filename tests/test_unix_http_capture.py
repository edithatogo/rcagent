"""Synthetic local sockets only, never an inference server."""

import base64
import hashlib
import os
import socket
import tempfile
import threading
import time
from pathlib import Path

import pytest

from tools import unix_http_capture as subject

pytestmark = pytest.mark.skipif(os.name != "posix", reason="Unix-only transport")


@pytest.fixture
def server():
    listeners = []
    threads = []
    with tempfile.TemporaryDirectory(prefix="rca-", dir="/tmp") as name:
        directory = Path(name).resolve()

        def start(response, delay=0):
            path = directory / f"{len(listeners)}.sock"
            listener = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            listener.bind(str(path))
            listener.listen(1)
            listener.settimeout(2)
            listeners.append(listener)

            def serve():
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
                        chunks = [response] if isinstance(response, bytes) else response
                        for chunk in chunks:
                            if delay:
                                time.sleep(delay)
                            conn.sendall(chunk)
                except OSError:
                    pass

            thread = threading.Thread(target=serve, daemon=True)
            thread.start()
            threads.append(thread)
            return path

        yield start
        for listener in listeners:
            listener.close()
        for thread in threads:
            thread.join(3)
            assert not thread.is_alive()


def wire(body=b'{"synthetic": true}\n', status=200, extra=b""):
    return (
        f"HTTP/1.1 {status} Synthetic\r\nContent-Type: application/json\r\nContent-Length: {len(body)}\r\n".encode()
        + extra
        + b"\r\n"
        + body
    )


def capture(path, **kwargs):
    return subject.capture(path, "GET", "/health", b"", deadline=time.monotonic() + 2, **kwargs)


def test_exact_body_and_locked_receipt(server, monkeypatch):
    monkeypatch.setenv("HTTP_PROXY", "http://invalid.example:1")
    raw = b' {"synthetic": "a\\n"} \r\n'
    result = capture(server(wire(raw)))
    assert result["status"] == "http_response_captured"
    assert result["body_complete"] is True
    assert base64.b64decode(result["body_base64"]) == raw
    assert result["body_sha256"] == hashlib.sha256(raw).hexdigest()
    assert result["admitted"] is result["study_unlocked"] is False
    assert result["transport"] == "unix-domain-socket"


def test_post_request_bound_by_digest(server):
    body = b'{"prompt":"synthetic"}'
    result = subject.capture(
        server(wire()), "POST", "/completion", body, deadline=time.monotonic() + 2
    )
    assert result["request_body_sha256"] == hashlib.sha256(body).hexdigest()
    assert result["status"] == "http_response_captured"


@pytest.mark.parametrize("status", [301, 400, 500])
def test_http_error_preserves_body_without_following_redirect(server, status):
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
def test_ambiguous_framing_rejected(server, headers):
    result = capture(server(b"HTTP/1.1 200 OK\r\n" + headers + b"\r\n{}"))
    assert result["status"] == "transport_failed"
    assert result["body_complete"] is False


def test_short_body_retained(server):
    result = capture(
        server(b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: 10\r\n\r\n{}")
    )
    assert result["error"] == "incomplete_body"
    assert base64.b64decode(result["body_base64"]) == b"{}"


def test_bad_http(server):
    assert capture(server(b"not HTTP\r\n"))["error"] == "http_protocol_error"


def test_absolute_deadline_stops_trickling_headers(server):
    path = server([b"HTTP/1.1 200 OK\r\n", b"X-A: a\r\n"] * 8, delay=0.025)
    start = time.monotonic()
    result = subject.capture(path, "GET", "/health", b"", deadline=start + 0.12)
    assert result["error"] == "deadline_exceeded"
    assert time.monotonic() - start < 1


def test_body_deadline_retains_partial_bytes(server):
    headers = b"HTTP/1.1 200 OK\r\nContent-Type: application/json\r\nContent-Length: 100\r\n\r\n"
    path = server([headers, b"abc"] * 8, delay=0.04)
    result = subject.capture(path, "GET", "/health", b"", deadline=time.monotonic() + 0.13)
    assert result["error"] == "deadline_exceeded"
    assert base64.b64decode(result["body_base64"]).startswith(b"abc")


@pytest.mark.parametrize(
    "method,route,body",
    [
        ("GET", "/completion", b""),
        ("POST", "/health", b"{}"),
        ("GET", "http://example.invalid", b""),
        ("GET", "/health", b"{}"),
        ("POST", "/completion", b""),
        ("POST", "/completion", "{}"),
        ("POST", "/completion", b"x" * (subject.MAX_BYTES + 1)),
    ],
)
def test_bad_request_fails_before_connection(tmp_path, method, route, body):
    with pytest.raises(ValueError):
        subject.capture(
            tmp_path / "missing.sock", method, route, body, deadline=time.monotonic() + 1
        )


@pytest.mark.parametrize("deadline", [0, float("inf"), float("nan"), True, "1", 10**1000])
def test_invalid_deadline(deadline, tmp_path):
    with pytest.raises(ValueError):
        subject.capture(tmp_path / "missing.sock", "GET", "/health", b"", deadline=deadline)


def test_unsafe_paths(tmp_path):
    regular = tmp_path / "file.sock"
    regular.write_bytes(b"synthetic")
    for path in (Path("relative.sock"), regular, tmp_path / "missing.sock"):
        with pytest.raises(ValueError):
            capture(path)


def test_shared_directory_rejected(server):
    path = server(wire())
    path.parent.chmod(0o755)
    try:
        with pytest.raises(ValueError):
            capture(path)
    finally:
        path.parent.chmod(0o700)


def test_expired_remaining_time():
    with pytest.raises(TimeoutError):
        subject._remaining(time.monotonic() - 1)


def test_connection_setup_expiry_returns_receipt(server, monkeypatch):
    path = server(wire())

    def fail(*args):
        raise TimeoutError

    monkeypatch.setattr(subject, "_Connection", fail)
    result = capture(path)
    assert result["error"] == "deadline_exceeded"
    assert result["body_complete"] is False


def test_connect_failure_returns_receipt():
    with tempfile.TemporaryDirectory(prefix="rca-", dir="/tmp") as name:
        path = Path(name).resolve() / "closed.sock"
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as listener:
            listener.bind(str(path))
        assert capture(path)["error"] == "socket_io_failed"


def test_socket_replacement_rejected(server, monkeypatch):
    path = server(wire())
    real = subject._path_identity
    calls = []

    def identity(path):
        value = real(path)
        calls.append(value)
        return value if len(calls) == 1 else (0, 0, 0, 0)

    monkeypatch.setattr(subject, "_path_identity", identity)
    result = capture(path)
    assert result["error"] == "socket_changed"
    assert result["body_complete"] is True


def test_socket_symlink_and_foreign_owner_rejected(server, monkeypatch):
    path = server(wire())
    link = path.with_name("link.sock")
    link.symlink_to(path)
    with pytest.raises(ValueError):
        capture(link)
    monkeypatch.setattr(subject.os, "getuid", lambda: -1)
    with pytest.raises(ValueError):
        capture(path)


def test_http_header_line_bound(server):
    raw = b"HTTP/1.1 200 OK\r\nX-Large: " + b"x" * 65536 + b"\r\n\r\n"
    assert capture(server(raw))["error"] == "http_protocol_error"


def test_malformed_header_not_silently_ignored(server):
    result = capture(server(wire(extra=b"not-a-header\r\n")))
    assert result["error"] == "unsupported_http_framing"
