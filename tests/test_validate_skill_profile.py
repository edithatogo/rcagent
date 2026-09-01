from __future__ import annotations

import json
import shutil
from pathlib import Path

import pytest

from tools.validate_skill_profile import TRACK, main, validate_profile

ROOT = Path(__file__).parents[1]


def _profile(tmp_path: Path) -> Path:
    (tmp_path / "skills").mkdir(parents=True)
    (tmp_path / TRACK).parent.mkdir(parents=True)
    (tmp_path / "evaluations/skills").mkdir(parents=True)
    shutil.copytree(
        ROOT / "skills/rca-investigation",
        tmp_path / "skills/rca-investigation",
    )
    shutil.copytree(
        ROOT / TRACK,
        tmp_path / TRACK,
    )
    shutil.copytree(
        ROOT / "evaluations/skills/rca-investigation",
        tmp_path / "evaluations/skills/rca-investigation",
    )
    return tmp_path


def test_current_profile_is_structurally_valid() -> None:
    assert validate_profile(ROOT) == []


def test_completion_gate_passes_with_current_actual_client_evidence() -> None:
    assert validate_profile(ROOT, require_complete=True) == []


def test_missing_evidence_is_reported(tmp_path: Path) -> None:
    root = _profile(tmp_path)
    matrix_path = root / TRACK / "evidence/compliance-matrix.json"
    matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
    matrix["items"][0]["evidence"] = "missing.md"
    matrix_path.write_text(json.dumps(matrix), encoding="utf-8")
    assert any("RCA-PROFILE-003" in error for error in validate_profile(root))


def test_evaluation_contract_is_fail_closed(tmp_path: Path) -> None:
    root = _profile(tmp_path)
    output_path = root / "evaluations/skills/rca-investigation/output-cases.json"
    output = json.loads(output_path.read_text(encoding="utf-8"))
    output["aggregation"]["unavailable_is_pass"] = True
    output_path.write_text(json.dumps(output), encoding="utf-8")
    assert any("RCA-EVAL-002" in error for error in validate_profile(root))


def test_cli_structural_and_completion_success(monkeypatch, capsys) -> None:
    monkeypatch.setattr("sys.argv", ["validate_skill_profile", "--root", str(ROOT)])
    assert main() == 0
    assert "validation passed" in capsys.readouterr().out

    monkeypatch.setattr(
        "sys.argv",
        ["validate_skill_profile", "--root", str(ROOT), "--require-complete"],
    )
    assert main() == 0
    assert "validation passed" in capsys.readouterr().out


@pytest.fixture
def matrix_profile(tmp_path: Path, monkeypatch) -> Path:
    """Isolate matrix mutations from unrelated skill and model-run fixtures."""
    monkeypatch.setattr("tools.validate_skill_profile.validate_skill", lambda _path: [])
    track = tmp_path / TRACK
    (track / "evidence").mkdir(parents=True)
    matrix = json.loads((ROOT / TRACK / "evidence/compliance-matrix.json").read_text())
    for item in matrix["items"]:
        item["evidence"] = "evidence.md"
        item["result"] = "pass"
        item["source"] = "https://agentskills.io/specification"
    (tmp_path / "evidence.md").write_text("Synthetic evidence for structural tests.\n")
    (track / "evidence/compliance-matrix.json").write_text(json.dumps(matrix))
    (track / "upstream-baseline.json").write_text(
        json.dumps(
            {
                "upstream_revision": matrix["baseline_revision"],
                "sources": ["https://agentskills.io/specification"],
            }
        )
    )
    extension_data = json.loads((ROOT / TRACK / "extensions.json").read_text())
    for item in extension_data["extensions"]:
        item["evidence"] = "evidence/fixture.md"
    (track / "evidence/fixture.md").write_text("Synthetic extension receipt.\n")
    (track / "extensions.json").write_text(json.dumps(extension_data))
    evaluations = tmp_path / "evaluations/skills/rca-investigation"
    evaluations.mkdir(parents=True)
    (evaluations / "trigger-cases.json").write_text(
        json.dumps({"cases": [{"partition": "train"}, {"partition": "held_out"}]})
    )
    (evaluations / "output-cases.json").write_text(
        json.dumps({"aggregation": {"unavailable_is_pass": False}})
    )
    return tmp_path


def _change_matrix(root: Path, change) -> None:
    path = root / TRACK / "evidence/compliance-matrix.json"
    matrix = json.loads(path.read_text())
    change(matrix)
    path.write_text(json.dumps(matrix))


def test_synthetic_complete_matrix_passes(matrix_profile: Path) -> None:
    assert validate_profile(matrix_profile, require_complete=True) == []


@pytest.mark.parametrize("remaining", [0, 1, 13])
def test_matrix_cannot_omit_required_coverage(matrix_profile: Path, remaining: int) -> None:
    _change_matrix(matrix_profile, lambda matrix: matrix.update(items=matrix["items"][:remaining]))
    assert any(
        "missing required ids" in error
        for error in validate_profile(matrix_profile, require_complete=True)
    )


@pytest.mark.parametrize("evidence", [None, "", " ", [], "missing.md", "../evidence.md"])
def test_pass_requires_bounded_nonempty_evidence(matrix_profile: Path, evidence) -> None:
    _change_matrix(matrix_profile, lambda matrix: matrix["items"][0].update(evidence=evidence))
    assert any("RCA-PROFILE-003" in error for error in validate_profile(matrix_profile))


def test_empty_evidence_file_cannot_pass(matrix_profile: Path) -> None:
    (matrix_profile / "evidence.md").write_text("")
    assert any("RCA-PROFILE-003" in error for error in validate_profile(matrix_profile))


def test_absolute_evidence_path_cannot_pass(matrix_profile: Path) -> None:
    _change_matrix(
        matrix_profile,
        lambda matrix: matrix["items"][0].update(evidence=str(matrix_profile / "evidence.md")),
    )
    assert any("RCA-PROFILE-003" in error for error in validate_profile(matrix_profile))


def test_symlink_evidence_cannot_escape_repository(matrix_profile: Path) -> None:
    outside = matrix_profile.parent / f"{matrix_profile.name}-outside.md"
    outside.write_text("Synthetic external evidence.\n")
    link = matrix_profile / "external.md"
    try:
        link.symlink_to(outside)
    except OSError:
        pytest.skip("Symlinks unavailable on this platform")
    _change_matrix(matrix_profile, lambda matrix: matrix["items"][0].update(evidence="external.md"))
    assert any("RCA-PROFILE-003" in error for error in validate_profile(matrix_profile))


@pytest.mark.parametrize("field", ["id", "source", "requirement", "applicability", "result"])
@pytest.mark.parametrize("value", [None, [], {}, " "])
def test_malformed_matrix_fields_fail_without_crashing(matrix_profile: Path, field, value) -> None:
    _change_matrix(matrix_profile, lambda matrix: matrix["items"][0].update({field: value}))
    assert any("non-empty strings required" in error for error in validate_profile(matrix_profile))


def test_duplicate_matrix_id_rejected(matrix_profile: Path) -> None:
    _change_matrix(matrix_profile, lambda matrix: matrix["items"].append(matrix["items"][0].copy()))
    assert any("duplicate id" in error for error in validate_profile(matrix_profile))


def test_pending_evidence_not_complete(matrix_profile: Path) -> None:
    _change_matrix(
        matrix_profile, lambda matrix: matrix["items"][0].update(result="pending", evidence=None)
    )
    assert validate_profile(matrix_profile) == []
    assert any(
        "RCA-PROFILE-004" in error
        for error in validate_profile(matrix_profile, require_complete=True)
    )


@pytest.mark.parametrize("document", ["trigger-cases.json", "output-cases.json"])
@pytest.mark.parametrize("value", [None, [], {"cases": None, "aggregation": []}])
def test_malformed_evaluation_documents_fail_closed(matrix_profile: Path, document, value) -> None:
    path = matrix_profile / "evaluations/skills/rca-investigation" / document
    path.write_text(json.dumps(value))
    assert any("RCA-EVAL-00" in error for error in validate_profile(matrix_profile))


@pytest.mark.parametrize("revision", [None, [], "", "f" * 40])
def test_matrix_revision_must_match_baseline(matrix_profile: Path, revision) -> None:
    _change_matrix(matrix_profile, lambda matrix: matrix.update(baseline_revision=revision))
    assert any("matrix revision" in error for error in validate_profile(matrix_profile))


def test_matrix_source_must_be_recorded(matrix_profile: Path) -> None:
    _change_matrix(
        matrix_profile,
        lambda matrix: matrix["items"][0].update(source="https://example.invalid/unknown"),
    )
    assert any("source is outside" in error for error in validate_profile(matrix_profile))


@pytest.mark.parametrize("value", [None, [], {}, {"extensions": []}])
def test_extension_document_requires_known_coverage(matrix_profile: Path, value) -> None:
    (matrix_profile / TRACK / "extensions.json").write_text(json.dumps(value))
    assert any("RCA-PROFILE-005" in error for error in validate_profile(matrix_profile))


@pytest.mark.parametrize(
    "field,value",
    [
        ("field", []),
        ("fallback", ""),
        ("scope", None),
        ("state", "unknown"),
        ("evidence", None),
        ("evidence", "../evidence.md"),
        ("evidence", "missing.md"),
    ],
)
def test_extension_entries_are_validated(matrix_profile: Path, field, value) -> None:
    path = matrix_profile / TRACK / "extensions.json"
    extensions = json.loads(path.read_text())
    extensions["extensions"][0][field] = value
    path.write_text(json.dumps(extensions))
    assert any("RCA-PROFILE-005" in error for error in validate_profile(matrix_profile))


@pytest.mark.parametrize(
    "document", ["evidence/compliance-matrix.json", "extensions.json", "upstream-baseline.json"]
)
def test_unreadable_profile_document_fails_closed(matrix_profile, document):
    (matrix_profile / TRACK / document).write_text("{")
    assert any("RCA-PROFILE-001" in error for error in validate_profile(matrix_profile))


@pytest.mark.parametrize("value", [None, [], {"items": None}])
def test_invalid_matrix_shape_fails_closed(matrix_profile, value):
    (matrix_profile / TRACK / "evidence/compliance-matrix.json").write_text(json.dumps(value))
    assert any("items array" in error for error in validate_profile(matrix_profile))


@pytest.mark.parametrize(
    "item,expected", [(None, "item must be an object"), ({}, "missing fields")]
)
def test_invalid_matrix_item_fails_closed(matrix_profile, item, expected):
    _change_matrix(matrix_profile, lambda matrix: matrix["items"].append(item))
    assert any(expected in error for error in validate_profile(matrix_profile))


@pytest.mark.parametrize("sources", [None, [], [None], [" "]])
def test_invalid_baseline_sources_rejected(matrix_profile, sources):
    path = matrix_profile / TRACK / "upstream-baseline.json"
    baseline = json.loads(path.read_text())
    baseline["sources"] = sources
    path.write_text(json.dumps(baseline))
    assert any("non-empty source URLs" in error for error in validate_profile(matrix_profile))


@pytest.mark.parametrize(
    "changes,expected",
    [
        ({"result": "success"}, "invalid result"),
        ({"applicability": "adapter_only", "omission_rationale": " "}, "omission rationale"),
    ],
)
def test_invalid_claims_require_correction(matrix_profile, changes, expected):
    _change_matrix(matrix_profile, lambda matrix: matrix["items"][0].update(changes))
    assert any(expected in error for error in validate_profile(matrix_profile))


def test_evidence_resolution_error_is_reported(matrix_profile, monkeypatch):
    original = Path.resolve

    def resolve(path, *args, **kwargs):
        if path.name == "evidence.md":
            raise OSError("Cannot resolve evidence")
        return original(path, *args, **kwargs)

    monkeypatch.setattr(Path, "resolve", resolve)
    assert any("RCA-PROFILE-003" in error for error in validate_profile(matrix_profile))
