from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest

from tools import build_client_plugins as plugin_module
from tools.build_client_plugins import build_client_plugin

ROOT = Path(__file__).parents[1]
REVISION = "1" * 40


@pytest.fixture(autouse=True)
def _unit_release_source(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(plugin_module, "verify_release_source", lambda *_args, **_kwargs: None)
    monkeypatch.setattr(plugin_module, "verify_release_payloads", lambda *_args, **_kwargs: None)


@pytest.mark.parametrize(
    ("client", "manifest_path"),
    [("codex", ".codex-plugin/plugin.json"), ("claude-code", ".claude-plugin/plugin.json")],
)
def test_client_plugin_is_deterministic_thin_and_offline(
    tmp_path: Path, client: str, manifest_path: str
) -> None:
    first = build_client_plugin(ROOT, tmp_path / "first", client=client, version="0.1.1", source_revision=REVISION)
    second = build_client_plugin(ROOT, tmp_path / "second", client=client, version="0.1.1", source_revision=REVISION)
    assert first.archive.read_bytes() == second.archive.read_bytes()
    with zipfile.ZipFile(first.archive) as archive:
        names = set(archive.namelist())
        manifest = json.loads(archive.read(manifest_path))
        assert manifest["skills"] == "./skills/"
        assert manifest["license"] == "Apache-2.0"
        if client == "codex":
            assert isinstance(manifest["interface"]["defaultPrompt"], list)
        provenance = json.loads(archive.read("PROVENANCE.json"))
        inventory = json.loads(archive.read("INVENTORY.json"))
        assert provenance["source_revision"] == REVISION
        assert provenance["network"] == "none"
        assert provenance["private_data"] is False
        for record in inventory["files"]:
            import hashlib

            assert hashlib.sha256(archive.read(record["path"])).hexdigest() == record["sha256"]
        assert {record["path"] for record in inventory["files"]} == names - {"INVENTORY.json"}
        assert "skills/rca-investigation/SKILL.md" in names
        assert {"LICENSE", "DISCLAIMER.md", "PRIVACY.md", "SUPPORT.md"} <= names
        assert not any(name.endswith((".mcp.json", ".app.json", "hooks.json")) for name in names)
        assert not any(name.startswith(("scripts/", "hooks/")) for name in names)


@pytest.mark.parametrize("client", ["unknown", "openai-mcp"])
def test_client_plugin_rejects_unsupported_surface(tmp_path: Path, client: str) -> None:
    with pytest.raises(ValueError, match="unsupported"):
        build_client_plugin(ROOT, tmp_path, client=client, version="0.1.0", source_revision=REVISION)


@pytest.mark.parametrize("version", ["1", "1.0", "v1.0.0", "1.0.0-beta"])
def test_client_plugin_rejects_non_release_version(tmp_path: Path, version: str) -> None:
    with pytest.raises(ValueError, match="semantic"):
        build_client_plugin(ROOT, tmp_path, client="codex", version=version, source_revision=REVISION)


def test_client_plugin_rejects_bad_revision_and_nonempty_destination(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="full Git commit"):
        build_client_plugin(ROOT, tmp_path / "bad", client="codex", version="0.1.0", source_revision="main")
    destination = tmp_path / "occupied"
    destination.mkdir()
    (destination / "keep").write_text("keep")
    with pytest.raises(FileExistsError, match="empty"):
        build_client_plugin(ROOT, destination, client="codex", version="0.1.0", source_revision=REVISION)
