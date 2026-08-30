"""Absolute deadlines may shorten capture but never restart a session budget."""

import os
import sys
import time
from pathlib import Path

import pytest

from tools import server_process as subject

pytestmark = pytest.mark.skipif(os.name != "posix", reason="POSIX child capture")


@pytest.mark.parametrize(
    "deadline",
    [True, "later", float("nan"), float("inf"), 0, -1, 10**1000],
    ids=["bool", "string", "nan", "infinity", "zero", "negative", "huge"],
)
def test_invalid_absolute_deadline_never_launches(monkeypatch, deadline):
    monkeypatch.setattr(subject.subprocess, "Popen", lambda *a, **kw: pytest.fail("launched"))
    with pytest.raises(ValueError, match="invalid_deadline"):
        subject.capture_child(["/synthetic/python"], {}, deadline=deadline)


def test_expired_worker_deadline_does_not_launch(monkeypatch):
    monkeypatch.setattr(subject.subprocess, "Popen", lambda *a, **kw: pytest.fail("launched"))
    result = subject.capture_child(["/synthetic/python"], {}, deadline=time.monotonic() - 1)
    assert result["error"] == "deadline_exceeded"
    assert result["execution_observed"] is False


def test_deadline_crossed_during_setup_does_not_launch(monkeypatch):
    clock = iter([100.0, 101.0, 102.0])
    monkeypatch.setattr(subject.time, "monotonic", lambda: next(clock))
    monkeypatch.setattr(subject.subprocess, "Popen", lambda *a, **kw: pytest.fail("launched"))
    result = subject.capture_child(["/synthetic/python"], {}, deadline=100.5)
    assert result["error"] == "deadline_exceeded"
    assert result["execution_observed"] is False


@pytest.mark.parametrize("timeout,absolute,expected", [(2, 110, 102), (20, 105, 105)])
def test_earlier_deadline_wins(monkeypatch, timeout, absolute, expected):
    monkeypatch.setattr(subject.time, "monotonic", lambda: 100.0)
    monkeypatch.setattr(
        subject.subprocess, "Popen", lambda *a, **kw: (_ for _ in ()).throw(OSError())
    )
    result = subject.capture_child(["/synthetic/python"], {}, timeout=timeout, deadline=absolute)
    assert result["execution_deadline_monotonic"] == expected


def test_future_deadline_is_bounded(monkeypatch):
    monkeypatch.setattr(subject.time, "monotonic", lambda: 100.0)
    with pytest.raises(ValueError, match="invalid_deadline"):
        subject.capture_child(["/synthetic/python"], {}, deadline=221)


def test_absolute_deadline_stops_running_synthetic_child():
    deadline = time.monotonic() + 0.2
    result = subject.capture_child(
        [str(Path(sys.executable).resolve()), "-c", "import time; time.sleep(20)"],
        {"PATH": os.defpath, "LANG": "C"},
        timeout=5,
        deadline=deadline,
        cleanup_grace=0.1,
    )
    assert result["error"] == "deadline_exceeded"
    assert result["reaped"] is True
    assert result["execution_deadline_monotonic"] == deadline
