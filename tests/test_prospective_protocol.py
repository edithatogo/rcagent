"""Synthetic protocol candidates cannot freeze, execute or admit a study."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from tools.prospective_protocol import main, validate_protocol


def pin(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fixture(root: Path) -> tuple[Path, dict]:
    refs = {}
    for name in ("case-a", "case-b", "rubric", "instructions", "prompt"):
        file = root / f"{name}.txt"
        file.write_text(f"Synthetic {name}", encoding="utf-8")
        refs[name] = {"path": file.name, "sha256": pin(file)}
    value = {
        "schema_version": "1.0",
        "kind": "prospective-study-protocol",
        "protocol_version": "1.0.0",
        "study_id": "prospective-test-only",
        "data_class": "synthetic",
        "case_exposure": "public",
        "held_out": False,
        "claims_boundary": "research-only-public-two-case-one-condition-no-comparative-or-operational-claims",
        "repeats": 1,
        "cases": [{"id": name, "input": refs[name]} for name in ("case-a", "case-b")],
        "condition": {
            "id": "condition-local-text",
            "model_id": "qwen2.5-0.5b-instruct-q4_k_m",
            "model_revision": "a" * 40,
            "model_sha256": "b" * 64,
            "runtime_sha256": "c" * 64,
            "profile_sha256": "d" * 64,
            "adapter_sha256": "e" * 64,
            "registry_sha256": "f" * 64,
        },
        "expected_slots": [f"case-{c}__condition-local-text__r1" for c in ("a", "b")],
        "rubric": refs["rubric"],
        "scoring_instructions": refs["instructions"],
        "prompt_template": refs["prompt"],
        "generation": {
            "seed": 42,
            "temperature": 0,
            "max_tokens": 512,
            "context_tokens": 2048,
            "timeout_seconds": 120,
        },
        "technical_retries": 1,
        "blinding": "metadata-blinding-v1",
        "normalization": "identity-utf8-v1",
        "scoring": {
            "reviewer_class": "agent",
            "roles": ["scorer-1", "scorer-2", "scorer-3"],
            "adjudication": "after-three-sealed-submissions",
            "raw_agreement_minimum": 0.80,
            "ordinal_agreement_minimum": 0.67,
            "hard_gates": ["privacy", "cultural-safety", "clinical-safety", "authority-boundaries"],
            "non_operational": True,
        },
    }
    path = root / "protocol.json"
    path.write_text(json.dumps(value), encoding="utf-8")
    return path, value


def test_valid_candidate_never_unlocks(tmp_path: Path) -> None:
    path, _ = fixture(tmp_path)
    result = validate_protocol(path, pin(path))
    assert result["status"] == "protocol_candidate_valid"
    assert result["admitted"] is result["study_unlocked"] is False
    assert result["expected_slots"] == 2


@pytest.mark.parametrize(
    "field,value",
    [
        ("extra", True),
        ("held_out", True),
        ("held_out", 0),
        ("repeats", True),
        ("repeats", 1.0),
        ("technical_retries", 1.0),
        ("technical_retries", True),
        ("study_id", "prospective-test\n"),
        ("data_class", "private"),
        ("expected_slots", ["invented", "other"]),
        ("normalization", "heuristic"),
    ],
)
def test_bad_top_level(tmp_path: Path, field: str, value: object) -> None:
    path, protocol = fixture(tmp_path)
    protocol[field] = value
    path.write_text(json.dumps(protocol), encoding="utf-8")
    with pytest.raises(ValueError):
        validate_protocol(path, pin(path))


@pytest.mark.parametrize(
    "mutation",
    [
        "duplicate-case",
        "duplicate-slot",
        "case-newline",
        "condition-newline",
        "bad-digest",
        "bool-seed",
        "float-tokens",
        "extra-condition",
        "duplicate-role",
        "early-adjudication",
        "no-hard-gate",
        "lower-threshold",
        "float-timeout",
    ],
)
def test_bad_nested(tmp_path: Path, mutation: str) -> None:
    path, value = fixture(tmp_path)
    if mutation == "duplicate-case":
        value["cases"][1] = value["cases"][0]
    elif mutation == "duplicate-slot":
        value["expected_slots"][1] = value["expected_slots"][0]
    elif mutation == "case-newline":
        value["cases"][0]["id"] += "\n"
    elif mutation == "condition-newline":
        value["condition"]["id"] += "\n"
    elif mutation == "bad-digest":
        value["condition"]["profile_sha256"] += "\n"
    elif mutation == "bool-seed":
        value["generation"]["seed"] = True
    elif mutation == "float-tokens":
        value["generation"]["max_tokens"] = 512.0
    elif mutation == "float-timeout":
        value["generation"]["timeout_seconds"] = 120.0
    elif mutation == "extra-condition":
        value["condition"]["trusted"] = True
    elif mutation == "duplicate-role":
        value["scoring"]["roles"][1] = "scorer-1"
    elif mutation == "early-adjudication":
        value["scoring"]["adjudication"] = "before-submission"
    elif mutation == "no-hard-gate":
        value["scoring"]["hard_gates"].pop()
    else:
        value["scoring"]["raw_agreement_minimum"] = 0.5
    path.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(ValueError):
        validate_protocol(path, pin(path))


@pytest.mark.parametrize("mutation", ["stale", "escape", "symlink", "invalid-utf8"])
def test_bad_artifact(tmp_path: Path, mutation: str) -> None:
    path, value = fixture(tmp_path)
    if mutation == "stale":
        (tmp_path / "rubric.txt").write_text("changed", encoding="utf-8")
    elif mutation == "escape":
        value["rubric"]["path"] = "../rubric.txt"
    elif mutation == "symlink":
        (tmp_path / "link.txt").symlink_to(tmp_path / "rubric.txt")
        value["rubric"]["path"] = "link.txt"
    else:
        (tmp_path / "rubric.txt").write_bytes(b"\xff")
        value["rubric"]["sha256"] = pin(tmp_path / "rubric.txt")
    path.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(ValueError):
        validate_protocol(path, pin(path))


@pytest.mark.parametrize("content", ["{", '{"duplicate":1,"duplicate":2}', "[]"])
def test_bad_json(tmp_path: Path, content: str) -> None:
    path = tmp_path / "protocol.json"
    path.write_text(content, encoding="utf-8")
    with pytest.raises(ValueError):
        validate_protocol(path, pin(path))


def test_wrong_pin_and_cli(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    path, _ = fixture(tmp_path)
    assert main(["--protocol", str(path), "--expected-sha256", "0" * 64]) == 1
    failed = json.loads(capsys.readouterr().out)
    assert failed["status"] == "protocol_candidate_invalid"
    assert str(tmp_path) not in json.dumps(failed)
    assert main(["--protocol", str(path), "--expected-sha256", pin(path)]) == 0
    assert json.loads(capsys.readouterr().out)["study_unlocked"] is False


@pytest.mark.parametrize("mutation", ["model-newline", "revision-newline", "duplicate-path"])
def test_fullmatch_and_distinct_artifacts(tmp_path: Path, mutation: str) -> None:
    path, value = fixture(tmp_path)
    if mutation == "duplicate-path":
        value["prompt_template"] = value["rubric"]
    else:
        field = "model_id" if mutation == "model-newline" else "model_revision"
        value["condition"][field] += "\n"
    path.write_text(json.dumps(value), encoding="utf-8")
    with pytest.raises(ValueError):
        validate_protocol(path, pin(path))
