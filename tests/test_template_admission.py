from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from collections.abc import Mapping
from pathlib import Path

import pytest

from tests.prospective_fixture_types import mapping, sequence, text_value
from tools import build_client_plugins as plugin_module
from tools import build_distribution as distribution_module
from tools.json_shapes import JsonObject
from tools.template_admission import CONTRACT_PATH, MANIFEST_PATH, validate_template_admission

ROOT = Path(__file__).parents[1]
SKILL = ROOT / "skills/rca-investigation"
TEMPLATE = "assets/templates/markdown/01-investigation-tor.md"


def _files() -> dict[str, bytes]:
    return {
        path.relative_to(SKILL).as_posix(): path.read_bytes()
        for path in SKILL.rglob("*")
        if path.is_file()
    }


def _manifest(files: Mapping[str, bytes]) -> JsonObject:
    return mapping(json.loads(files[MANIFEST_PATH]))


def _write_manifest(files: dict[str, bytes], manifest: JsonObject) -> None:
    files[MANIFEST_PATH] = json.dumps(manifest).encode()


def _repository(destination: Path) -> Path:
    shutil.copytree(SKILL, destination / "skills/rca-investigation")
    for name in ("LICENSE", "DISCLAIMER.md", "PRIVACY.md", "SUPPORT.md", "CHANGELOG.md", "VERSION"):
        shutil.copy2(ROOT / name, destination / name)
    return destination


def _skip_source_verification(*_args: object, **_kwargs: object) -> None:
    return None


def _build(
    repository: Path, destination: Path, builder: str, monkeypatch: pytest.MonkeyPatch
) -> Path:
    if builder == "portable":
        return distribution_module.build_distribution(
            repository, destination, version="0.0.0-test"
        ).archive
    # Release-source checks have dedicated real-Git tests. Here isolate admission.
    monkeypatch.setattr(plugin_module, "verify_release_source", _skip_source_verification)
    monkeypatch.setattr(plugin_module, "verify_release_payloads", _skip_source_verification)
    return plugin_module.build_client_plugin(
        repository,
        destination,
        client=builder,
        version=(repository / "VERSION").read_text().strip(),
        source_revision="1" * 40,
    ).archive


def test_current_rendering_assets_have_exact_draft_admission() -> None:
    files = _files()
    assert validate_template_admission(files) == hashlib.sha256(files[MANIFEST_PATH]).hexdigest()
    manifest = _manifest(files)
    assert (
        mapping(manifest["historical_quarantine"])["status"] == "quarantined_legacy_not_supported"
    )
    assert mapping(manifest["historical_quarantine"])["unchanged"] is True
    assert (
        len(sequence(manifest["files"])) >= 40
    )  # 36 revised templates, two styles, use contract and supporting guide.
    for raw_entry in sequence(manifest["files"]):
        entry = mapping(raw_entry)
        payload = files[text_value(entry["path"])].decode()
        assert "CONFIDENTIAL: QUALITY IMPROVEMENT" not in payload
        assert "protected as Quality Improvement" not in payload
        assert "within 24 hours" not in payload


@pytest.mark.parametrize(
    "path",
    [
        TEMPLATE,
        "assets/styles/docx-style-guide.md",
        CONTRACT_PATH,
        "references/just-culture-guide.md",
    ],
)
def test_modified_template_style_or_contract_is_rejected(path: str) -> None:
    files = _files()
    files[path] += b"\nUnreviewed change\n"
    with pytest.raises(ValueError, match="hash mismatch"):
        validate_template_admission(files)


@pytest.mark.parametrize("path", [MANIFEST_PATH, TEMPLATE, CONTRACT_PATH])
def test_missing_admission_asset_is_rejected(path: str) -> None:
    files = _files()
    del files[path]
    with pytest.raises(ValueError, match="missing"):
        validate_template_admission(files)


def test_unlisted_rendering_asset_is_rejected() -> None:
    files = _files()
    files["assets/templates/markdown/unreviewed.md"] = b"# Not admitted\n"
    with pytest.raises(ValueError, match="unlisted"):
        validate_template_admission(files)


@pytest.mark.parametrize(
    ("field", "value"), [("admission", "quarantined"), ("schema_version", "2.0"), ("scope", "all")]
)
def test_non_admitted_manifest_is_rejected(field: str, value: str) -> None:
    files = _files()
    manifest = _manifest(files)
    manifest[field] = value
    _write_manifest(files, manifest)
    with pytest.raises(ValueError, match="template admission"):
        validate_template_admission(files)


@pytest.mark.parametrize(
    "path",
    [
        "/assets/templates/a.md",
        "assets/templates/../../secret",
        "assets/templates/./a.md",
        "assets\\templates\\a.md",
        "SKILL.md",
    ],
)
def test_manifest_paths_cannot_escape_asset_scope(path: str) -> None:
    files = _files()
    manifest = _manifest(files)
    mapping(sequence(manifest["files"])[0])["path"] = path
    _write_manifest(files, manifest)
    with pytest.raises(ValueError, match="canonical asset scope"):
        validate_template_admission(files)


@pytest.mark.parametrize(
    "mutation",
    [
        "duplicate",
        "quarantined",
        "invalid_hash",
        "missing_contract",
        "missing_revision",
        "empty_files",
        "non_object_entry",
    ],
)
def test_invalid_admission_entries_fail_closed(mutation: str) -> None:
    files = _files()
    manifest = _manifest(files)
    if mutation == "duplicate":
        sequence(manifest["files"]).append(sequence(manifest["files"])[0])
    elif mutation == "quarantined":
        mapping(sequence(manifest["files"])[0])["status"] = "quarantined"
    elif mutation == "invalid_hash":
        mapping(sequence(manifest["files"])[0])["sha256"] = "not-a-digest"
    elif mutation == "missing_contract":
        manifest["files"] = [
            entry
            for entry in sequence(manifest["files"])
            if mapping(entry)["path"] != CONTRACT_PATH
        ]
        del files[CONTRACT_PATH]
    elif mutation == "missing_revision":
        del manifest["revision"]
    elif mutation == "empty_files":
        manifest["files"] = []
    else:
        manifest["files"] = [None]
    _write_manifest(files, manifest)
    with pytest.raises(ValueError, match="template admission"):
        validate_template_admission(files)


@pytest.mark.parametrize(
    "payload",
    [b"[]", b"not-json", b"\xff", b'{"admission":"portable_draft_only","admission":"quarantined"}'],
)
def test_malformed_or_ambiguous_manifest_is_rejected(payload: bytes) -> None:
    files = _files()
    files[MANIFEST_PATH] = payload
    with pytest.raises(ValueError, match="template admission"):
        validate_template_admission(files)


@pytest.mark.parametrize("builder", ["portable", "codex", "claude-code"])
@pytest.mark.parametrize("mutation", ["modified", "missing_manifest", "unlisted"])
def test_all_archive_builders_reject_unadmitted_assets(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, builder: str, mutation: str
) -> None:
    repository = _repository(tmp_path / "repository")
    skill = repository / "skills/rca-investigation"
    if mutation == "modified":
        (skill / TEMPLATE).write_text("# Unreviewed revision\n")
    elif mutation == "missing_manifest":
        (skill / MANIFEST_PATH).unlink()
    else:
        (skill / "assets/templates/markdown/unreviewed.md").write_text("# Unreviewed addition\n")
    destination = tmp_path / "output"
    with pytest.raises(ValueError, match="template admission"):
        _build(repository, destination, builder, monkeypatch)
    assert not list(destination.glob("*.zip"))


@pytest.mark.parametrize("builder", ["portable", "codex", "claude-code"])
def test_builders_package_the_same_bytes_that_admission_validated(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, builder: str
) -> None:
    repository = _repository(tmp_path / "repository")
    target = repository / "skills/rca-investigation" / TEMPLATE
    original = target.read_bytes()

    def validate_then_change_disk(files: Mapping[str, bytes]) -> str:
        digest = validate_template_admission(files)
        target.write_text("# Later unreviewed filesystem change\n")
        return digest

    module = distribution_module if builder == "portable" else plugin_module
    monkeypatch.setattr(module, "validate_template_admission", validate_then_change_disk)
    archive_path = _build(repository, tmp_path / "output", builder, monkeypatch)
    prefix = "rca-investigation/" if builder == "portable" else "skills/rca-investigation/"
    with zipfile.ZipFile(archive_path) as archive:
        assert archive.read(prefix + TEMPLATE) == original
        manifest_payload = archive.read(prefix + MANIFEST_PATH)
        if builder == "portable":
            provenance = json.loads(archive.read(prefix + "distribution-manifest.json"))
        else:
            provenance = json.loads(archive.read("PROVENANCE.json"))
        assert (
            provenance["template_admission_sha256"] == hashlib.sha256(manifest_payload).hexdigest()
        )
        assert provenance["template_admission_scope"] == "portable_draft_only"


@pytest.mark.parametrize(
    "relative",
    [
        "LICENSE",
        "DISCLAIMER.md",
        "PRIVACY.md",
        "SUPPORT.md",
        "CHANGELOG.md",
        "VERSION",
        "distribution-manifest.json",
        "sbom.cdx.json",
        "license",
        "Distribution-Manifest.json",
        "LICENSE/nested.md",
        "distribution-manifest.json/nested.md",
    ],
)
def test_portable_builder_rejects_reserved_names_before_writing_archive(
    tmp_path: Path, relative: str
) -> None:
    repository = _repository(tmp_path / "repository")
    target = repository / "skills/rca-investigation" / relative
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text("Synthetic package-name collision\n")
    destination = tmp_path / "output"
    with pytest.raises(ValueError, match="reserved package path"):
        distribution_module.build_distribution(repository, destination, version="0.0.0-test")
    assert not list(destination.rglob("*"))


@pytest.mark.parametrize("builder", ["portable", "codex", "claude-code"])
def test_builders_reject_output_inside_skill_before_creating_it(
    tmp_path: Path, builder: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    repository = _repository(tmp_path / "repository")
    destination = repository / "skills/rca-investigation/output"
    with pytest.raises(ValueError, match="outside the portable source"):
        _build(repository, destination, builder, monkeypatch)
    assert not destination.exists()


@pytest.mark.parametrize("builder", ["portable", "codex", "claude-code"])
def test_output_guard_uses_resolved_source_when_parent_is_an_internal_symlink(
    tmp_path: Path, builder: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    repository = _repository(tmp_path / "repository")
    actual = repository / "actual-skills"
    (repository / "skills").rename(actual)
    (repository / "skills").symlink_to(actual, target_is_directory=True)
    destination = actual / "rca-investigation/output"
    with pytest.raises(ValueError, match="outside the portable source"):
        _build(repository, destination, builder, monkeypatch)
    assert not destination.exists()
