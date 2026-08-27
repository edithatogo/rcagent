from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.install_skill_adapter import install_adapter
from tools.validate_skill import validate_skill

ROOT = Path(__file__).parents[1]


@pytest.mark.parametrize("client", ["codex", "claude-code"])
def test_adapter_installs_unmodified_valid_core(tmp_path: Path, client: str) -> None:
    installed = install_adapter(ROOT, client, tmp_path)
    assert validate_skill(installed) == []
    assert (installed / "SKILL.md").read_bytes() == (
        ROOT / "skills/rca-investigation/SKILL.md"
    ).read_bytes()


def test_adapter_refuses_overwrite_without_explicit_replace(tmp_path: Path) -> None:
    installed = install_adapter(ROOT, "codex", tmp_path)
    with pytest.raises(FileExistsError):
        install_adapter(ROOT, "codex", tmp_path)
    (installed / "stale.txt").write_text("stale", encoding="utf-8")
    replaced = install_adapter(ROOT, "codex", tmp_path, replace=True)
    assert not (replaced / "stale.txt").exists()


def test_adapter_manifests_do_not_preapprove_experimental_tools() -> None:
    for client in ("codex", "claude-code"):
        manifest = json.loads(
            (ROOT / "adapters" / client / "adapter.json").read_text(encoding="utf-8")
        )
        assert manifest["frontmatter"]["experimental"] == []
        assert "allowed-tools" in manifest["frontmatter"]["unsupported"]


def test_adapter_rejects_escaping_target(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    adapter = repository / "adapters/example"
    adapter.mkdir(parents=True)
    skill = repository / "skills/example"
    skill.mkdir(parents=True)
    (skill / "SKILL.md").write_text(
        "---\nname: example\ndescription: Use for an example task.\n---\n# Example\n",
        encoding="utf-8",
    )
    (adapter / "adapter.json").write_text(
        json.dumps(
            {
                "canonical_skill": "../../skills/example",
                "discovery_targets": ["../escape"],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="relative and non-escaping"):
        install_adapter(repository, "example", tmp_path / "destination")


def test_adapter_rejects_canonical_source_outside_repository(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    adapter = repository / "adapters/example"
    adapter.mkdir(parents=True)
    (adapter / "adapter.json").write_text(
        json.dumps(
            {
                "canonical_skill": "../../../../outside",
                "discovery_targets": ["skills/example"],
            }
        ),
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="inside the repository"):
        install_adapter(repository, "example", tmp_path / "destination")
