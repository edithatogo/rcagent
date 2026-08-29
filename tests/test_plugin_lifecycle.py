from __future__ import annotations

import json
import zipfile
from pathlib import Path

import pytest

from tools import build_client_plugins as plugin_module
from tools.build_client_plugins import build_client_plugin
from tools.plugin_lifecycle import install_plugin_archive, remove_plugin

ROOT = Path(__file__).parents[1]


@pytest.fixture(autouse=True)
def _unit_release_source(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(plugin_module, "verify_release_source", lambda *_args, **_kwargs: None)


@pytest.mark.parametrize(
    ("client", "manifest"),
    [("codex", ".codex-plugin/plugin.json"), ("claude-code", ".claude-plugin/plugin.json")],
)
def test_isolated_install_update_discovery_reference_parity_and_remove(
    tmp_path: Path, client: str, manifest: str
) -> None:
    built = build_client_plugin(
        ROOT, tmp_path / "build", client=client, version="0.1.0", source_revision="1" * 40
    )
    install = install_plugin_archive(built.archive, tmp_path / "installed")
    assert json.loads((install / manifest).read_text())["version"] == "0.1.0"
    for source in (ROOT / "skills/rca-investigation").rglob("*"):
        if source.is_file():
            target = install / "skills/rca-investigation" / source.relative_to(
                ROOT / "skills/rca-investigation"
            )
            assert target.read_bytes() == source.read_bytes()
    (install / "stale.txt").write_text("must disappear")
    install_plugin_archive(built.archive, install)
    assert not (install / "stale.txt").exists()
    remove_plugin(install)
    assert not install.exists()


def test_isolated_installer_rejects_archive_traversal(tmp_path: Path) -> None:
    archive = tmp_path / "unsafe.zip"
    with zipfile.ZipFile(archive, "w") as output:
        output.writestr("../escape", b"no")
    with pytest.raises(ValueError, match="unsafe"):
        install_plugin_archive(archive, tmp_path / "installed")
    assert not (tmp_path / "escape").exists()
