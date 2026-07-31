from __future__ import annotations

import json
from pathlib import Path

from tools.check_skill_drift import check_drift, main


def _baseline(path: Path) -> Path:
    path.write_text(
        json.dumps(
            {
                "upstream_revision": "expected",
                "sources": ["https://agentskills.io/specification"],
            }
        ),
        encoding="utf-8",
    )
    return path


class _Response:
    def __init__(self, payload: object) -> None:
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return None

    def read(self) -> bytes:
        return json.dumps(self.payload).encode()


def test_offline_mode_cannot_claim_current(tmp_path: Path) -> None:
    code, receipt = check_drift(_baseline(tmp_path / "baseline.json"), offline=True)
    assert code == 0
    assert receipt["status"] == "offline_not_current"
    assert receipt["current_conformance"] is False


def test_matching_live_revision_is_current(tmp_path: Path) -> None:
    def opener(*args, **kwargs):
        return _Response({"sha": "expected"})

    code, receipt = check_drift(
        _baseline(tmp_path / "baseline.json"), opener=opener
    )
    assert code == 0
    assert receipt["status"] == "current"
    assert receipt["current_conformance"] is True


def test_changed_revision_requires_normative_review(tmp_path: Path) -> None:
    def opener(*args, **kwargs):
        return _Response({"sha": "changed"})

    code, receipt = check_drift(
        _baseline(tmp_path / "baseline.json"), opener=opener
    )
    assert code == 1
    assert receipt["status"] == "normative_review_required"
    assert receipt["current_conformance"] is False


def test_upstream_failure_is_not_specification_failure(tmp_path: Path) -> None:
    def opener(*args, **kwargs):
        raise OSError("network unavailable")

    code, receipt = check_drift(
        _baseline(tmp_path / "baseline.json"), opener=opener
    )
    assert code == 2
    assert receipt["status"] == "upstream_unavailable"
    assert receipt["current_conformance"] is False


def test_cli_writes_honest_offline_receipt(
    tmp_path: Path, monkeypatch
) -> None:
    baseline = _baseline(tmp_path / "baseline.json")
    output = tmp_path / "receipt.json"
    monkeypatch.setattr(
        "sys.argv",
        [
            "check_skill_drift",
            "--baseline",
            str(baseline),
            "--offline",
            "--output",
            str(output),
        ],
    )
    assert main() == 0
    receipt = json.loads(output.read_text(encoding="utf-8"))
    assert receipt["status"] == "offline_not_current"
    assert receipt["current_conformance"] is False
