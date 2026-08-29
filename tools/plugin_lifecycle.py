"""Local isolated install, update, and removal helpers for compatibility tests."""

from __future__ import annotations

import shutil
import stat
import tempfile
import zipfile
from pathlib import Path, PurePosixPath


def install_plugin_archive(archive_path: Path, install_root: Path) -> Path:
    """Safely replace one isolated plugin install from an archive."""
    install_root.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="rcagent-plugin-", dir=install_root.parent) as temporary:
        staged = Path(temporary) / "plugin"
        staged.mkdir()
        with zipfile.ZipFile(archive_path) as archive:
            for member in archive.infolist():
                name = PurePosixPath(member.filename)
                if name.is_absolute() or ".." in name.parts or not name.parts:
                    raise ValueError("plugin archive contains an unsafe path")
                mode = member.external_attr >> 16
                if stat.S_ISLNK(mode) or (mode and not (stat.S_ISREG(mode) or stat.S_ISDIR(mode))):
                    raise ValueError("plugin archive contains a link or special file")
                target = staged.joinpath(*name.parts)
                target.parent.mkdir(parents=True, exist_ok=True)
                if not member.is_dir():
                    target.write_bytes(archive.read(member))
        old = install_root.with_name(install_root.name + ".old")
        if old.exists():
            shutil.rmtree(old)
        if install_root.exists():
            install_root.rename(old)
        staged.rename(install_root)
        if old.exists():
            shutil.rmtree(old)
    return install_root


def remove_plugin(install_root: Path) -> None:
    if install_root.exists():
        shutil.rmtree(install_root)
