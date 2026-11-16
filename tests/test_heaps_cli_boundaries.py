"""Public HEAPS assembly and CLI failure boundaries beyond the frozen oracle."""

from __future__ import annotations

import hashlib
import json
from dataclasses import replace
from pathlib import Path

import pytest

from tests.prospective_fixture_types import ObjectMap, mapping, sequence
from tests.test_heaps import EVALUATED_AT, FIXTURES, Inputs
from tools import heaps


def _json(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, allow_nan=False, indent=2) + "\n").encode()


def _parsed(raw: bytes) -> ObjectMap:
    value: object = json.loads(raw)
    return mapping(value)


def _sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def _base() -> Inputs:
    return Inputs(
        (FIXTURES / "canonical/base-case.json").read_bytes(),
        (FIXTURES / "packet/base-profile.json").read_bytes(),
        {
            path.relative_to(FIXTURES).as_posix(): path.read_bytes()
            for folder in ("sources", "packet")
            for path in (FIXTURES / folder).rglob("*")
            if path.is_file()
        },
    )


def _rebind(inputs: Inputs, case: ObjectMap, profile: ObjectMap) -> Inputs:
    canonical = json.dumps(
        case, sort_keys=True, separators=(",", ":"), ensure_ascii=False, allow_nan=False
    ).encode()
    mapping(profile["case_binding"])["fingerprint"] = "sha256:" + _sha(canonical)
    return replace(inputs, case=_json(case), profile=_json(profile))


def _arguments(inputs: Inputs, directory: Path, output: Path) -> list[str]:
    directory.mkdir()
    (directory / "case.json").write_bytes(inputs.case)
    (directory / "profile.json").write_bytes(inputs.profile)
    for relative, raw in inputs.artifacts.items():
        path = directory / "artifacts" / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(raw)
    arguments = [
        "--case",
        str(directory / "case.json"),
        "--profile",
        str(directory / "profile.json"),
        "--artifacts",
        str(directory / "artifacts"),
        "--template",
        "packet/template-v1.md",
        "--evaluated-at",
        EVALUATED_AT,
        "--output",
        str(output),
    ]
    for option, raw in (
        ("manifest", inputs.manifest),
        ("decision", inputs.decision),
        ("status", inputs.status),
    ):
        if raw is not None:
            path = directory / f"{option}.json"
            path.write_bytes(raw)
            arguments.extend([f"--{option}", str(path)])
    return arguments


def _assert_rejected(result: heaps.PacketResult, message: str) -> None:
    assert result.preparation_disposition == "reject_input"
    assert result.errors == (message,)
    assert result.files == {}
    assert result.status is None


@pytest.mark.parametrize("template_count", [0, 1, 2])
def test_implicit_template_selection_requires_one_exact_byte_match(template_count: int) -> None:
    inputs = _base()
    artifacts = dict(inputs.artifacts)
    template = artifacts.pop("packet/template-v1.md")
    for index in range(template_count):
        artifacts[f"templates/candidate-{index}.md"] = template
    result = heaps.assemble_packet(
        inputs.case, inputs.profile, artifacts, evaluated_at=EVALUATED_AT
    )
    if template_count == 1:
        assert result.preparation_disposition == "prepare_draft", result.errors
        assert result.files["template.md"] == template
    else:
        _assert_rejected(
            result, "template: a unique explicitly bound template artifact is required"
        )


def test_source_with_matching_hash_still_requires_utf8_text() -> None:
    inputs = _base()
    case, profile = _parsed(inputs.case), _parsed(inputs.profile)
    raw = b"Generated synthetic binary boundary\n\xff"
    mapping(sequence(case["sources"])[0])["fingerprint"] = "sha256:" + _sha(raw)
    mapping(sequence(profile["source_snapshots"])[0])["raw_sha256"] = _sha(raw)
    inputs = _rebind(inputs, case, profile)
    inputs = replace(inputs, artifacts={**inputs.artifacts, "sources/record.txt": raw})
    _assert_rejected(inputs.run(), "artifact: only UTF-8 synthetic text is supported")


@pytest.mark.parametrize("availability", ["available", "unavailable"])
def test_cli_resolves_snapshot_locator_and_preserves_unavailable_source_state(
    tmp_path: Path, capsys: pytest.CaptureFixture[str], availability: str
) -> None:
    inputs = _base()
    case, profile = _parsed(inputs.case), _parsed(inputs.profile)
    mapping(sequence(case["sources"])[0]).pop("citation")
    snapshot = mapping(sequence(profile["source_snapshots"])[0])
    snapshot["state"] = availability
    if availability == "unavailable":
        snapshot["raw_sha256"] = None
        inputs.artifacts.pop("sources/record.txt")
    inputs = _rebind(inputs, case, profile)
    output = tmp_path / "output"
    assert heaps.main(_arguments(inputs, tmp_path / "input", output)) == 0
    assert _parsed(capsys.readouterr().out.encode())["preparation_disposition"] == "prepare_draft"
    status = _parsed((output / "status.json").read_bytes())
    assert status["source_check"] == ("passed" if availability == "available" else "partial")
    assert (output / "sources/record.txt").exists() == (availability == "available")
    emitted_profile = _parsed((output / "profile.json").read_bytes())
    emitted_snapshot = mapping(sequence(emitted_profile["source_snapshots"])[0])
    assert emitted_snapshot["snapshot_id"] == "syn-snapshot-record"
    assert emitted_snapshot["state"] == availability


def test_cli_rejects_casefold_source_collision_before_publication(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    inputs = _base()
    case, profile = _parsed(inputs.case), _parsed(inputs.profile)
    mapping(sequence(case["sources"])[1])["citation"] = "sources/RECORD.txt"
    mapping(sequence(profile["source_snapshots"])[1])["locator"] = None
    inputs = _rebind(inputs, case, profile)
    output = tmp_path / "output"
    assert heaps.main(_arguments(inputs, tmp_path / "input", output)) == 2
    observed = _parsed(capsys.readouterr().out.encode())
    assert observed["errors"] == ["artifacts: case-insensitive path collision"]
    assert not output.exists()


def test_optional_component_cannot_replace_a_generated_report() -> None:
    inputs = _base()
    profile = _parsed(inputs.profile)
    raw = b"Generated synthetic component with no graph qualification.\n"
    profile["optional_components"] = [
        {
            "component": "accimap",
            "contract_version": "synthetic-boundary-1",
            "artifact": {
                "artifact_id": "syn-colliding-component",
                "path": "report.md",
                "sha256": _sha(raw),
                "bytes": len(raw),
            },
            "evidence_refs": [],
            "question": "Which system conditions remain unresolved?",
            "admission": "not_established_by_profile",
        }
    ]
    inputs = replace(
        inputs, profile=_json(profile), artifacts={**inputs.artifacts, "report.md": raw}
    )
    _assert_rejected(inputs.run(), "optional component: duplicate consumed artifact")


@pytest.mark.parametrize("component", ["case", "profile", "template"])
def test_manifest_byte_consistency_does_not_replace_current_semantic_binding(
    component: str,
) -> None:
    inputs = _base()
    first = inputs.run()
    assert first.preparation_disposition == "prepare_draft"
    manifest = _parsed(first.files["manifest.json"])
    descriptor = mapping(mapping(manifest["components"])[component])
    path = descriptor["path"]
    assert isinstance(path, str)
    artifacts = {**inputs.artifacts, **first.files}
    if component == "template":
        raw = b"# Different original synthetic outline\n"
        message = "manifest: template binding is stale"
    else:
        value = _parsed(artifacts[path])
        if component == "case":
            value["version"] = 2
        else:
            value["profile_version"] = 2
        raw = _json(value)
        message = "manifest: case/profile content binding is stale"
    artifacts[path] = raw
    descriptor.update({"sha256": _sha(raw), "bytes": len(raw)})
    result = replace(inputs, artifacts=artifacts, manifest=_json(manifest)).run()
    _assert_rejected(result, message)


@pytest.mark.parametrize("same_bytes", [False, True])
def test_conflicting_historical_output_paths_reject_without_losing_prior_bytes(
    same_bytes: bool,
) -> None:
    inputs = _base()
    first = inputs.run()
    manifest = _parsed(first.files["manifest.json"])
    artifacts = {**inputs.artifacts, **first.files}
    reports: list[ObjectMap] = []
    for index, path in enumerate(("history/report.md", "report.md")):
        raw = b"Original synthetic historical account A.\n"
        if not same_bytes and index:
            raw = b"Conflicting synthetic historical account B.\n"
        artifacts[path] = raw
        reports.append(
            {
                "artifact_id": f"syn-history-{index}",
                "path": path,
                "sha256": _sha(raw),
                "bytes": len(raw),
            }
        )
    mapping(manifest["components"])["reports"] = reports
    result = replace(inputs, artifacts=artifacts, manifest=_json(manifest)).run()
    if same_bytes:
        assert result.preparation_disposition == "prepare_draft", result.errors
        assert result.files["history/report.md"] == artifacts["history/report.md"]
        assert result.files["report.md"] == first.files["report.md"]
    else:
        _assert_rejected(result, "manifest: historical artifact collision")


def test_cli_publish_race_keeps_another_writers_output_intact(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    inputs = _base()
    output = tmp_path / "output"
    arguments = _arguments(inputs, tmp_path / "input", output)

    def competing_publish(_self: Path, target: Path) -> Path:
        target.mkdir(exist_ok=True)
        (target / "other-writer.txt").write_bytes(b"Other synthetic packet writer owns this.")
        raise OSError("Synthetic concurrent publication failure")

    monkeypatch.setattr(Path, "replace", competing_publish)
    monkeypatch.setattr(Path, "rename", competing_publish)
    assert heaps.main(arguments) == 2
    observed = _parsed(capsys.readouterr().out.encode())
    assert observed["errors"] == ["filesystem or input shape boundary failed"]
    assert sorted(path.name for path in output.iterdir()) == ["other-writer.txt"]
    assert (output / "other-writer.txt").read_bytes() == b"Other synthetic packet writer owns this."
    assert sorted(path.name for path in tmp_path.iterdir()) == ["input", "output"]
