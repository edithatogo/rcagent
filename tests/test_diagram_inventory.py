from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import cast

import pytest

from tools.diagram_inventory import (
    METHODS,
    TEMPLATE_SYNTAX,
    InventoryError,
    build_inventory,
    main,
)

SKILL = Path("skills/rca-investigation")


def _repository(root: Path) -> Path:
    manifest_files: list[dict[str, str]] = []
    for method in METHODS:
        path = root / SKILL / "references/methods" / method.guide
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(f"# Synthetic guide {method.slug}\n", encoding="utf-8")
    for name, keyword in TEMPLATE_SYNTAX.items():
        path = root / SKILL / "assets/templates/mermaid" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        content = f"%% Synthetic diagram\n{keyword} LR\n    A --> B\n"
        if keyword in {"mindmap", "timeline", "quadrantChart"}:
            content = f"%% Synthetic diagram\n{keyword}\n"
        path.write_bytes(content.encode("utf-8"))
        manifest_files.append(
            {
                "path": f"assets/templates/mermaid/{name}",
                "sha256": hashlib.sha256(content.encode()).hexdigest(),
                "status": "admitted_portable_draft",
            }
        )
    manifest = {
        "schema_version": "1.0",
        "admission": "portable_draft_only",
        "revision": "synthetic-test",
        "files": manifest_files,
    }
    path = root / SKILL / "assets/template-admission.json"
    path.write_text(json.dumps(manifest), encoding="utf-8")
    return root


def _mutate_manifest(root: Path, change: str) -> None:
    path = root / SKILL / "assets/template-admission.json"
    data = cast(dict[str, object], json.loads(path.read_text(encoding="utf-8")))
    if change == "status":
        data["admission"] = "unverified"
    elif change == "duplicate":
        files = cast(list[dict[str, object]], data["files"])
        files.append(dict(files[0]))
    elif change == "missing":
        files = cast(list[dict[str, object]], data["files"])
        files.pop()
    elif change == "duplicate-key":
        path.write_text('{"schema_version":"1.0","schema_version":"1.0"}', encoding="utf-8")
        return
    path.write_text(json.dumps(data), encoding="utf-8")


def test_inventory_reports_current_methods_templates_and_status(tmp_path: Path) -> None:
    report = build_inventory(_repository(tmp_path))
    assert report["schema_version"] == "diagram-inventory-1.0"
    assert report["admission_revision"] == "synthetic-test"
    assert len(report["methods"]) == 14
    assert len(report["templates"]) == 12
    assert report["native_diagram_claim"] == "not-established"
    assert any(t["role"] == "workflow" for t in report["templates"])
    assert all(t["status"] == "admitted_portable_draft" for t in report["templates"])
    assert all(t["syntax_checked"] for t in report["templates"])


def test_inventory_is_stably_sorted(tmp_path: Path) -> None:
    root = _repository(tmp_path)
    a = build_inventory(root)
    b = build_inventory(root)
    assert json.dumps(a, sort_keys=True) == json.dumps(b, sort_keys=True)
    assert [t["name"] for t in a["templates"]] == sorted(TEMPLATE_SYNTAX)


@pytest.mark.parametrize(
    ("fault", "message"),
    [
        ("status", "not admitted"),
        ("duplicate", "duplicate admitted template"),
        ("missing", "missing admitted template"),
        ("duplicate-key", "duplicate JSON key"),
    ],
)
def test_rejects_invalid_admission_manifest(tmp_path: Path, fault: str, message: str) -> None:
    root = _repository(tmp_path)
    _mutate_manifest(root, fault)
    with pytest.raises(InventoryError, match=message):
        build_inventory(root)


def test_rejects_modified_rendering_bytes(tmp_path: Path) -> None:
    root = _repository(tmp_path)
    path = root / SKILL / "assets/templates/mermaid/accimap-levels.mmd"
    path.write_text("flowchart LR\n    A-->C\n", encoding="utf-8")
    with pytest.raises(InventoryError, match="digest mismatch"):
        build_inventory(root)


def test_rejects_wrong_mermaid_keyword_even_with_valid_digest(tmp_path: Path) -> None:
    root = _repository(tmp_path)
    path = root / SKILL / "assets/templates/mermaid/accimap-levels.mmd"
    content = "timeline\n    title Not an AcciMap fallback\n"
    path.write_bytes(content.encode("utf-8"))
    manifest = root / SKILL / "assets/template-admission.json"
    data = cast(dict[str, object], json.loads(manifest.read_text(encoding="utf-8")))
    files = cast(list[dict[str, object]], data["files"])
    for item in files:
        item_path = item.get("path")
        if isinstance(item_path, str) and item_path.endswith("accimap-levels.mmd"):
            item["sha256"] = hashlib.sha256(content.encode()).hexdigest()
    manifest.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(InventoryError, match="Mermaid keyword drift"):
        build_inventory(root)


def test_rejects_unregistered_template(tmp_path: Path) -> None:
    root = _repository(tmp_path)
    (root / SKILL / "assets/templates/mermaid/new-diagram.mmd").write_text(
        "flowchart LR\n", encoding="utf-8"
    )
    with pytest.raises(InventoryError, match="unregistered Mermaid file"):
        build_inventory(root)


def test_rejects_missing_method_guide(tmp_path: Path) -> None:
    root = _repository(tmp_path)
    (root / SKILL / "references/methods/accimap.md").unlink()
    with pytest.raises(InventoryError, match="missing method guide"):
        build_inventory(root)


def test_cli_returns_json_and_zero_exit(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = _repository(tmp_path)
    assert main([str(root)]) == 0
    decoded = cast(dict[str, object], json.loads(capsys.readouterr().out))
    assert decoded["schema_version"] == "diagram-inventory-1.0"


def test_cli_fails_closed(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert main([str(tmp_path)]) == 1
    assert "missing" in capsys.readouterr().err


def test_actual_admitted_method_and_template_inventory() -> None:
    from tools.diagram_inventory import ROOT

    report = build_inventory(ROOT)
    assert len(report["methods"]) == 14
    assert len(report["templates"]) == 12
    assert report["admission_revision"] != "synthetic-test"


def test_synthetic_manifest_hashes_are_byte_stable(tmp_path: Path) -> None:
    root = _repository(tmp_path)
    manifest_path = root / SKILL / "assets/template-admission.json"
    decoded = cast(dict[str, object], json.loads(manifest_path.read_text(encoding="utf-8")))
    entries = cast(list[dict[str, object]], decoded["files"])
    for entry in entries:
        path_value = entry.get("path")
        digest = entry.get("sha256")
        assert isinstance(path_value, str)
        assert isinstance(digest, str)
        data = (root / SKILL / path_value).read_bytes()
        assert hashlib.sha256(data).hexdigest() == digest
