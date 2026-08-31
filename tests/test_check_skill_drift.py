from __future__ import annotations

import json
from pathlib import Path

import pytest

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

    code, receipt = check_drift(_baseline(tmp_path / "baseline.json"), opener=opener)
    assert code == 0
    assert receipt["status"] == "current"
    assert receipt["current_conformance"] is True


def _changed_opener(paths: list[str]):
    def opener(request, **kwargs):
        if "/commits/main" in request.full_url:
            return _Response({"sha": "changed"})
        return _Response({"status": "ahead", "files": [{"filename": path} for path in paths]})

    return opener


def test_changed_revision_requires_normative_review(tmp_path: Path) -> None:

    code, receipt = check_drift(
        _baseline(tmp_path / "baseline.json"),
        opener=_changed_opener(["docs/specification.mdx"]),
    )
    assert code == 1
    assert receipt["status"] == "normative_review_required"
    assert receipt["current_conformance"] is False


def test_validator_change_requires_normative_review(tmp_path: Path) -> None:
    code, receipt = check_drift(
        _baseline(tmp_path / "baseline.json"),
        opener=_changed_opener(["skills-ref/src/skills_ref/validator.py"]),
    )
    assert code == 1
    assert receipt["status"] == "normative_review_required"


def test_guidance_change_is_advisory(tmp_path: Path) -> None:
    code, receipt = check_drift(
        _baseline(tmp_path / "baseline.json"),
        opener=_changed_opener(["docs/skill-creation/best-practices.mdx"]),
    )
    assert code == 0
    assert receipt["status"] == "guidance_review_advised"
    assert receipt["current_conformance"] is True


def test_unrelated_change_does_not_block_conformance(tmp_path: Path) -> None:
    code, receipt = check_drift(
        _baseline(tmp_path / "baseline.json"),
        opener=_changed_opener(["docs/client-showcase.mdx"]),
    )
    assert code == 0
    assert receipt["status"] == "upstream_change_irrelevant"
    assert receipt["current_conformance"] is True


def test_compare_failure_is_upstream_unavailable(tmp_path: Path) -> None:
    def opener(request, **kwargs):
        if "/commits/main" in request.full_url:
            return _Response({"sha": "changed"})
        raise OSError("comparison unavailable")

    code, receipt = check_drift(_baseline(tmp_path / "baseline.json"), opener=opener)
    assert code == 2
    assert receipt["status"] == "upstream_unavailable"


def test_upstream_failure_is_not_specification_failure(tmp_path: Path) -> None:
    def opener(*args, **kwargs):
        raise OSError("network unavailable")

    code, receipt = check_drift(_baseline(tmp_path / "baseline.json"), opener=opener)
    assert code == 2
    assert receipt["status"] == "upstream_unavailable"
    assert receipt["current_conformance"] is False


def test_cli_writes_honest_offline_receipt(tmp_path: Path, monkeypatch) -> None:
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


@pytest.mark.parametrize(
    "payload",
    [
        {"status": "ahead", "files": [None]},
        {"status": "ahead", "files": [{"filename": ""}]},
        {"status": "ahead", "files": [{"filename": "other", "previous_filename": None}]},
        {"status": "ahead", "files": "not-a-list"},
        {"status": "diverged", "files": []},
        {"files": []},
        {"status": "ahead", "files": [{"filename": "unrelated"}] * 300},
    ],
)
def test_incomplete_or_untrusted_comparison_never_passes(tmp_path, payload):
    def opener(request, **kwargs):
        return _Response({"sha": "changed"} if "/commits/main" in request.full_url else payload)

    code, receipt = check_drift(_baseline(tmp_path / "baseline.json"), opener=opener)
    assert code == 2
    assert receipt["current_conformance"] is False


def test_renaming_normative_file_is_not_irrelevant(tmp_path):
    def opener(request, **kwargs):
        return _Response(
            {"sha": "changed"}
            if "/commits/main" in request.full_url
            else {
                "status": "ahead",
                "files": [
                    {
                        "filename": "elsewhere/spec.mdx",
                        "previous_filename": "docs/specification.mdx",
                    }
                ],
            }
        )

    code, receipt = check_drift(_baseline(tmp_path / "baseline.json"), opener=opener)
    assert code == 1
    assert receipt["status"] == "normative_review_required"


@pytest.mark.parametrize("payload", [None, {}, {"upstream_revision": "x", "sources": []}])
def test_invalid_baseline_has_failed_receipt(tmp_path, payload):
    path = tmp_path / "baseline.json"
    path.write_text(json.dumps(payload))
    code, receipt = check_drift(path, offline=True)
    assert code == 2
    assert receipt["current_conformance"] is False
