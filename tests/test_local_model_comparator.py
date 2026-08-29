from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path
from types import SimpleNamespace

import pytest

from tools import local_model_comparator
from tools.local_model_comparator import (
    _extract_object,
    _prompt,
    _read_object,
    _score,
    run,
    validate_admission,
)


def _file_record(path: Path) -> dict[str, object]:
    return {
        "path": path.name,
        "bytes": path.stat().st_size,
        "sha256": local_model_comparator._sha256(path),
    }


def _admitted_manifest(tmp_path: Path) -> tuple[dict, Path]:
    executable = tmp_path / "llama-cli"
    executable.write_bytes(b"runtime")
    model_root = tmp_path / "models"
    models = []
    for size_class in ("small", "medium", "larger"):
        directory = model_root / size_class
        directory.mkdir(parents=True)
        licence = directory / "LICENSE"
        licence.write_bytes(b"Apache-2.0")
        weights = directory / "model.gguf"
        weights.write_bytes(size_class.encode())
        models.append(
            {
                "id": f"model-{size_class}",
                "size_class": size_class,
                "license": "Apache-2.0",
                "admission_status": "admitted_local_research_only",
                "cache_subdirectory": size_class,
                "license_sha256": local_model_comparator._sha256(licence),
                "files": [_file_record(weights)],
            }
        )
    return (
        {
            "admission_policy": {
                "data_class": "synthetic_only",
                "network": "disabled",
                "external_inference": False,
                "remote_code": False,
                "telemetry": False,
                "redistribution": False,
                "publication": False,
                "promotion_eligible": False,
            },
            "runtime": {
                "executable": str(executable),
                "executable_sha256": local_model_comparator._sha256(executable),
                "license": "MIT",
            },
            "models": models,
        },
        model_root,
    )


def test_extract_and_score_valid_response() -> None:
    response = _extract_object(
        '```json\n{"evidence_ids":["e1"],"claim_types":["unknown"],"abstained":true,"rationale":"Missing."}\n```'
    )
    score = _score(
        {"evidence_ids": ["e1"], "claim_types": ["unknown"], "must_abstain": True}, response
    )
    assert score["passed"] is True


def test_read_object_accepts_object_and_rejects_other_json(tmp_path: Path) -> None:
    path = tmp_path / "value.json"
    path.write_text('{"status":"ok"}')
    assert _read_object(path) == {"status": "ok"}
    path.write_text("[]")
    with pytest.raises(ValueError, match="expected a JSON object"):
        _read_object(path)


def test_score_rejects_non_boolean_abstention() -> None:
    response = {
        "evidence_ids": ["e1"],
        "claim_types": ["unknown"],
        "abstained": ["person"],
        "rationale": "No.",
    }
    score = _score(
        {"evidence_ids": ["e1"], "claim_types": ["unknown"], "must_abstain": True}, response
    )
    assert score["schema_valid"] is False
    assert score["passed"] is False


def test_extract_object_skips_invalid_candidates_and_rejects_non_objects() -> None:
    assert _extract_object('prefix {bad} then {"ok": true}') == {"ok": True}
    assert _extract_object('```json\n["not", "an", "object"]\n```') is None
    assert _extract_object("no structured response") is None


def test_score_handles_missing_response() -> None:
    assert _score({"evidence_ids": [], "claim_types": [], "must_abstain": True}, None) == {
        "schema_valid": False,
        "evidence_exact": False,
        "claim_types_exact": False,
        "abstention_correct": False,
        "passed": False,
    }


def test_prompt_contains_case_contract_and_evidence() -> None:
    prompt = _prompt(
        {
            "summary": "Synthetic accounts disagree.",
            "expected": {"evidence_ids": ["account-a", "account-b"]},
        }
    )
    assert "Return only one compact JSON object" in prompt
    assert "authority_boundary" in prompt
    assert "Synthetic accounts disagree." in prompt
    assert "account-a, account-b" in prompt


def test_admission_fails_closed_without_all_size_classes(tmp_path: Path) -> None:
    manifest = json.loads(
        (Path(__file__).parents[1] / "evaluation/benchmark/comparators.json").read_text()
    )
    manifest["models"] = []
    errors = validate_admission(manifest, tmp_path)
    assert "models: exactly small, medium, and larger classes must be admitted" in errors


def test_admission_accepts_exact_local_files(tmp_path: Path) -> None:
    manifest, model_root = _admitted_manifest(tmp_path)
    assert validate_admission(manifest, model_root) == []


def test_admission_reports_policy_runtime_and_model_metadata_errors(tmp_path: Path) -> None:
    manifest, model_root = _admitted_manifest(tmp_path)
    manifest["admission_policy"]["network"] = "enabled"
    manifest["runtime"]["license"] = "GPL"
    manifest["runtime"]["executable_sha256"] = "0" * 64
    manifest["models"][0]["license"] = "research-only"
    manifest["models"][0]["admission_status"] = "pending"

    errors = validate_admission(manifest, model_root)

    assert "admission_policy.network: must be 'disabled'" in errors
    assert "runtime: licence is not MIT" in errors
    assert "runtime: executable is missing or hash mismatched" in errors
    assert "model-small: licence is not Apache-2.0" in errors
    assert "model-small: model is not locally admitted" in errors


def test_admission_reports_escape_missing_licence_and_bad_model_files(tmp_path: Path) -> None:
    manifest, model_root = _admitted_manifest(tmp_path)
    manifest["models"][0]["cache_subdirectory"] = "../escape"
    (model_root / "medium" / "LICENSE").unlink()
    (model_root / "larger" / "model.gguf").write_bytes(b"changed")
    missing = model_root / "medium" / "model.gguf"
    missing.unlink()

    errors = validate_admission(manifest, model_root)

    assert "model-small: cache path escapes model root" in errors
    assert "model-medium: licence file is missing or mismatched" in errors
    assert "model-medium: missing model.gguf" in errors
    assert "model-larger: size or hash mismatch for model.gguf" in errors


def test_run_rejects_invalid_admission(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(local_model_comparator, "validate_admission", lambda *_: ["bad"])
    with pytest.raises(ValueError, match="invalid comparator admission: bad"):
        run({}, tmp_path, repeats=1, timeout=1)


def test_run_records_successful_observation_and_summary(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    manifest, model_root = _admitted_manifest(tmp_path)
    manifest["models"] = manifest["models"][:1]
    case = {
        "id": "case-1",
        "summary": "Evidence is missing.",
        "expected": {
            "evidence_ids": ["e1"],
            "claim_types": ["unknown"],
            "must_abstain": True,
        },
    }
    output = json.dumps(
        {
            "evidence_ids": ["e1"],
            "claim_types": ["unknown"],
            "abstained": True,
            "rationale": "Missing.",
        }
    )
    monkeypatch.setattr(local_model_comparator, "validate_admission", lambda *_: [])
    monkeypatch.setattr(local_model_comparator, "_read_object", lambda _: {"cases": [case]})
    monkeypatch.setattr(
        local_model_comparator.subprocess,
        "run",
        lambda *args, **kwargs: SimpleNamespace(stdout=output, returncode=0),
    )
    ticks = iter((10.0, 10.025))
    monkeypatch.setattr(local_model_comparator.time, "perf_counter", lambda: next(ticks))

    receipt = run(manifest, model_root, repeats=1, timeout=9)

    observation = receipt["observations"][0]
    assert observation["exit_code"] == 0
    assert observation["latency_ms"] == 25.0
    assert observation["score"]["passed"] is True
    assert receipt["summary"]["model-small"] == {
        "observations": 1,
        "passed": 1,
        "schema_valid": 1,
        "latency_ms_min": 25.0,
        "latency_ms_max": 25.0,
        "latency_ms_mean": 25.0,
    }
    assert len(receipt["receipt_sha256"]) == 64


@pytest.mark.parametrize("partial_stdout", [b"partial bytes", "partial text", None])
def test_run_records_timeout_output(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    partial_stdout: bytes | str | None,
) -> None:
    manifest, model_root = _admitted_manifest(tmp_path)
    manifest["models"] = manifest["models"][:1]
    case = {
        "id": "case-1",
        "summary": "Timeout case.",
        "expected": {"evidence_ids": [], "claim_types": [], "must_abstain": True},
    }
    monkeypatch.setattr(local_model_comparator, "validate_admission", lambda *_: [])
    monkeypatch.setattr(local_model_comparator, "_read_object", lambda _: {"cases": [case]})

    def timeout(*args: object, **kwargs: object) -> None:
        raise subprocess.TimeoutExpired("llama-cli", 1, output=partial_stdout)

    monkeypatch.setattr(local_model_comparator.subprocess, "run", timeout)
    receipt = run(manifest, model_root, repeats=1, timeout=1)
    observation = receipt["observations"][0]
    expected_output = (
        partial_stdout.decode(errors="replace")
        if isinstance(partial_stdout, bytes)
        else (partial_stdout or "")
    )
    assert observation["exit_code"] == "timeout"
    assert observation["response"] is None
    assert observation["raw_output_sha256"] == local_model_comparator.hashlib.sha256(
        expected_output.encode()
    ).hexdigest()


def test_comparator_cli_validate_and_run_paths(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(local_model_comparator, "validate_admission", lambda manifest, root: [])
    monkeypatch.setattr(local_model_comparator, "_read_object", lambda path: {"models": []})
    monkeypatch.setattr(
        sys, "argv", ["comparator", "--model-root", str(tmp_path), "--validate-only"]
    )
    assert local_model_comparator.main() == 0
    assert "validation passed" in capsys.readouterr().out

    output = tmp_path / "result.json"
    monkeypatch.setattr(
        local_model_comparator,
        "run",
        lambda manifest, root, repeats, timeout: {"receipt_sha256": "a" * 64},
    )
    monkeypatch.setattr(
        sys,
        "argv",
        ["comparator", "--model-root", str(tmp_path), "--output", str(output)],
    )
    assert local_model_comparator.main() == 0
    assert json.loads(output.read_text())["receipt_sha256"] == "a" * 64


def test_comparator_cli_prints_result_without_output_file(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(local_model_comparator, "validate_admission", lambda *_: [])
    monkeypatch.setattr(local_model_comparator, "_read_object", lambda _: {"models": []})
    monkeypatch.setattr(
        local_model_comparator,
        "run",
        lambda *_: {"receipt_sha256": "b" * 64, "status": "unsupported"},
    )
    monkeypatch.setattr(sys, "argv", ["comparator", "--model-root", str(tmp_path)])

    assert local_model_comparator.main() == 0
    assert json.loads(capsys.readouterr().out)["status"] == "unsupported"


def test_comparator_cli_reports_admission_errors(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.setattr(local_model_comparator, "_read_object", lambda path: {})
    monkeypatch.setattr(
        local_model_comparator, "validate_admission", lambda manifest, root: ["missing model"]
    )
    monkeypatch.setattr(sys, "argv", ["comparator", "--model-root", str(tmp_path)])
    assert local_model_comparator.main() == 1
    assert "ERROR: missing model" in capsys.readouterr().out
