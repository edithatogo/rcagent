from __future__ import annotations

import json
import shutil
from pathlib import Path

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


def test_completion_gate_passes_when_every_item_passes() -> None:
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


def test_cli_success_and_completion_success(monkeypatch, capsys) -> None:
    monkeypatch.setattr("sys.argv", ["validate_skill_profile", "--root", str(ROOT)])
    assert main() == 0
    assert "validation passed" in capsys.readouterr().out

    monkeypatch.setattr(
        "sys.argv",
        ["validate_skill_profile", "--root", str(ROOT), "--require-complete"],
    )
    assert main() == 0
    assert "validation passed" in capsys.readouterr().out
