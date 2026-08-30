"""Synthetic planning inventory tests; no supplied package is an observation."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from tools.prospective_inventory import inventory, main


def pin(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value: object) -> None:
    path.write_text(json.dumps(value), encoding="utf-8")


def fixture(root: Path) -> tuple[Path, dict]:
    (root / "input.txt").write_text("Synthetic [Case ID]", encoding="utf-8")
    (root / "rubric.txt").write_text("Synthetic research rubric", encoding="utf-8")
    (root / "submissions").mkdir()
    value = {
        "schema_version": "1.0",
        "kind": "prospective-study-plan",
        "study_id": "prospective-test-only",
        "version": "0.1.0",
        "state": "planning",
        "data_class": "synthetic",
        "repeats": 2,
        "cases": [
            {"id": "case-a", "input": {"path": "input.txt", "sha256": pin(root / "input.txt")}}
        ],
        "conditions": [{"id": "condition-a", "execution_status": "unassigned"}],
        "rubric": {"path": "rubric.txt", "sha256": pin(root / "rubric.txt")},
        "expected_slots": ["case-a__condition-a__r1", "case-a__condition-a__r2"],
    }
    manifest = root / "manifest.json"
    write_json(manifest, value)
    return manifest, value


def package(manifest: Path, plan: dict) -> tuple[Path, dict]:
    slot = plan["expected_slots"][0]
    root = manifest.parent / "submissions" / slot
    root.mkdir()
    for name in ("raw.txt", "normalized.txt"):
        (root / name).write_text("Synthetic unverified response", encoding="utf-8")
    value = {
        "schema_version": "1.0",
        "purpose": "primary-observation",
        "study_id": plan["study_id"],
        "manifest_sha256": pin(manifest),
        "slot_id": slot,
        "input_sha256": plan["cases"][0]["input"]["sha256"],
        "raw": {"path": "raw.txt", "sha256": pin(root / "raw.txt")},
        "normalized": {"path": "normalized.txt", "sha256": pin(root / "normalized.txt")},
        "normalization": {
            "source_sha256": pin(root / "raw.txt"),
            "target_sha256": pin(root / "normalized.txt"),
            "method": "identity-utf8-v1",
        },
    }
    receipt = root / "receipt.json"
    write_json(receipt, value)
    return receipt, value


def test_missing_and_structurally_consistent_never_admitted(tmp_path: Path) -> None:
    manifest, plan = fixture(tmp_path)
    result = inventory(manifest, pin(manifest))
    assert result["counts"] == {
        "expected": 2,
        "pending": 2,
        "quarantined": 0,
        "unexpected": 0,
        "admitted": 0,
    }
    package(manifest, plan)
    result = inventory(manifest, pin(manifest))
    assert result["slots"][0]["reason"] == "execution_provenance_unverified"
    assert result["slots"][0]["disposition"] == "quarantined"
    assert result["slots"][1]["reason"] == "submission_missing"
    assert result["study_unlocked"] is False
    assert result["counts"]["admitted"] == 0


@pytest.mark.parametrize(
    "field,value",
    [
        ("study_id", "prospective-other"),
        ("manifest_sha256", "0" * 64),
        ("slot_id", "case-b__condition-a__r1"),
        ("input_sha256", "0" * 64),
    ],
)
def test_cross_identity_quarantined(tmp_path: Path, field: str, value: str) -> None:
    manifest, plan = fixture(tmp_path)
    receipt, payload = package(manifest, plan)
    payload[field] = value
    write_json(receipt, payload)
    assert inventory(manifest, pin(manifest))["slots"][0]["reason"] == "identity_mismatch"


@pytest.mark.parametrize(
    "content,reason",
    [
        (b'{"purpose":"contract-fixture"}', "fixture_not_observation"),
        (b"{}", "invalid_schema"),
        (b'{"x":1,"x":2}', "duplicate_json_key"),
        (b"not json", "invalid_json"),
        (b"\xff", "invalid_json"),
        (b"[" * 2000, "invalid_json"),
        (b"", "artifact_size_out_of_bounds"),
    ],
)
def test_invalid_receipts_are_quarantined(tmp_path: Path, content: bytes, reason: str) -> None:
    manifest, plan = fixture(tmp_path)
    receipt, _ = package(manifest, plan)
    receipt.write_bytes(content)
    assert inventory(manifest, pin(manifest))["slots"][0]["reason"] == reason


@pytest.mark.parametrize(
    "path",
    [
        "../input.txt",
        "/tmp/raw.txt",
        "C:/raw.txt",
        "..\\raw.txt",
        "raw\x00.txt",
        "./raw.txt",
        "dir//raw.txt",
    ],
)
def test_artifact_path_restrictions(tmp_path: Path, path: str) -> None:
    manifest, plan = fixture(tmp_path)
    receipt, payload = package(manifest, plan)
    payload["raw"]["path"] = path
    write_json(receipt, payload)
    assert inventory(manifest, pin(manifest))["slots"][0]["reason"] == "invalid_artifact_path"


@pytest.mark.parametrize(
    "change,reason",
    [
        ("hash", "artifact_hash_mismatch"),
        ("utf8", "invalid_utf8"),
        ("different", "normalization_mismatch"),
        ("source", "normalization_mismatch"),
        ("target", "normalization_mismatch"),
        ("missing", "non_regular_or_symlink_artifact"),
    ],
)
def test_artifact_and_normalization_failures(tmp_path: Path, change: str, reason: str) -> None:
    manifest, plan = fixture(tmp_path)
    receipt, payload = package(manifest, plan)
    raw = receipt.parent / "raw.txt"
    if change == "hash":
        raw.write_bytes(b"changed")
    elif change in {"utf8", "different"}:
        raw.write_bytes(b"\xff" if change == "utf8" else b"different")
        payload["raw"]["sha256"] = pin(raw)
        payload["normalization"]["source_sha256"] = pin(raw)
    elif change in {"source", "target"}:
        payload["normalization"][f"{change}_sha256"] = "0" * 64
    else:
        raw.unlink()
    write_json(receipt, payload)
    assert inventory(manifest, pin(manifest))["slots"][0]["reason"] == reason


@pytest.mark.parametrize(
    "change,reason",
    [
        ("cases", "duplicate_identity"),
        ("conditions", "duplicate_identity"),
        ("denominator", "denominator_mismatch"),
        ("repeats", "invalid_schema"),
        ("extra", "invalid_schema"),
        ("private", "invalid_schema"),
        ("rubric", "artifact_hash_mismatch"),
    ],
)
def test_manifest_rejections(tmp_path: Path, change: str, reason: str) -> None:
    manifest, payload = fixture(tmp_path)
    if change in {"cases", "conditions"}:
        payload[change].append(payload[change][0])
    elif change == "denominator":
        payload["expected_slots"].pop()
    elif change == "repeats":
        payload["repeats"] = 11
    elif change == "private":
        payload["data_class"] = "private"
    elif change == "rubric":
        payload["rubric"]["sha256"] = "0" * 64
    else:
        payload["approved"] = True
    write_json(manifest, payload)
    with pytest.raises(ValueError, match=f"^{reason}$"):
        inventory(manifest, pin(manifest))


@pytest.mark.parametrize("expected_pin", ["", "bad", "0" * 64])
def test_manifest_pin_is_required(tmp_path: Path, expected_pin: str) -> None:
    manifest, _ = fixture(tmp_path)
    with pytest.raises(ValueError, match="manifest_pin_mismatch"):
        inventory(manifest, expected_pin)


def test_unknown_entries_counted_without_disclosure(tmp_path: Path) -> None:
    manifest, _ = fixture(tmp_path)
    (tmp_path / "submissions" / "private-name-must-not-appear").write_bytes(b"private-content")
    result = inventory(manifest, pin(manifest))
    assert result["counts"]["unexpected"] == 1
    assert "private" not in json.dumps(result)


@pytest.mark.parametrize("location", ["root", "slot", "receipt", "artifact"])
def test_symlink_boundaries(tmp_path: Path, location: str) -> None:
    manifest, plan = fixture(tmp_path)
    receipt, _ = package(manifest, plan)
    target = {
        "root": tmp_path / "submissions",
        "slot": receipt.parent,
        "receipt": receipt,
        "artifact": receipt.parent / "raw.txt",
    }[location]
    original = target.with_name(target.name + "-original")
    target.rename(original)
    try:
        target.symlink_to(original, target_is_directory=original.is_dir())
    except OSError:
        pytest.skip("symlinks unavailable")
    if location == "root":
        with pytest.raises(ValueError, match="submissions_root_unavailable"):
            inventory(manifest, pin(manifest))
    else:
        assert (
            inventory(manifest, pin(manifest))["slots"][0]["reason"]
            == "non_regular_or_symlink_artifact"
        )


def test_missing_root_and_entry_limit(tmp_path: Path) -> None:
    manifest, _ = fixture(tmp_path)
    root = tmp_path / "submissions"
    root.rmdir()
    with pytest.raises(ValueError, match="submissions_root_unavailable"):
        inventory(manifest, pin(manifest))
    root.mkdir()
    for index in range(1001):
        (root / f"unknown-{index}").touch()
    with pytest.raises(ValueError, match="too_many_submissions"):
        inventory(manifest, pin(manifest))


def test_cli_success_is_not_admission_and_failure_sanitized(tmp_path: Path, capsys) -> None:
    manifest, _ = fixture(tmp_path)
    assert main(["--manifest", str(manifest), "--expected-sha256", pin(manifest)]) == 0
    result = json.loads(capsys.readouterr().out)
    assert result["status"] == "planning_inventory"
    assert result["study_unlocked"] is False
    assert result["counts"]["admitted"] == 0
    assert main(["--manifest", str(tmp_path / "private-missing"), "--expected-sha256", "bad"]) == 1
    assert json.loads(capsys.readouterr().out) == {
        "status": "inventory_failed",
        "study_unlocked": False,
    }


def test_oversized_receipt_quarantined(tmp_path: Path, monkeypatch) -> None:
    manifest, plan = fixture(tmp_path)
    receipt, _ = package(manifest, plan)
    monkeypatch.setattr("tools.evaluation_preflight.MAX_BYTES", 4096)
    receipt.write_bytes(b"x" * 4097)
    assert inventory(manifest, pin(manifest))["slots"][0]["reason"] == "artifact_size_out_of_bounds"


@pytest.mark.parametrize("value", [1.0, True, False])
def test_repeats_require_actual_integer(tmp_path: Path, value: object) -> None:
    manifest, plan = fixture(tmp_path)
    plan["repeats"] = value
    write_json(manifest, plan)
    with pytest.raises(ValueError):
        inventory(manifest, pin(manifest))


@pytest.mark.parametrize("field", ["study_id", "cases", "conditions"])
def test_identifiers_reject_trailing_newlines(tmp_path: Path, field: str) -> None:
    manifest, plan = fixture(tmp_path)
    if field == "study_id":
        plan[field] += "\n"
    else:
        plan[field][0]["id"] += "\n"
    write_json(manifest, plan)
    with pytest.raises(ValueError):
        inventory(manifest, pin(manifest))


def test_gitkeep_ignored_only_when_empty_regular_file(tmp_path: Path) -> None:
    manifest, _ = fixture(tmp_path)
    marker = tmp_path / "submissions" / ".gitkeep"
    marker.touch()
    assert inventory(manifest, pin(manifest))["counts"]["unexpected"] == 0
    marker.write_bytes(b"not a placeholder")
    assert inventory(manifest, pin(manifest))["counts"]["unexpected"] == 1
    marker.unlink()
    marker.mkdir()
    assert inventory(manifest, pin(manifest))["counts"]["unexpected"] == 1


def test_checked_in_planning_manifest_is_pinned_and_pending() -> None:
    manifest = (
        Path(__file__).parents[1]
        / "evaluation/prospective/prospective-agent-text-20260830/manifest.json"
    )
    result = inventory(manifest, "a21bf8cd1676a20f422b75275307e5be30e203ba7a9755f2ba50d78735e8f2be")
    saved = json.loads((manifest.parent / "inventory-20260830.json").read_text(encoding="utf-8"))
    assert result == saved
    assert result["counts"] == {
        "expected": 2,
        "pending": 2,
        "quarantined": 0,
        "unexpected": 0,
        "admitted": 0,
    }
    assert result["study_unlocked"] is False
