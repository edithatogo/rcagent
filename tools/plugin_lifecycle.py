"""Local isolated install, update, and removal helpers for compatibility tests."""

from __future__ import annotations

import ntpath
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
            seen: set[str] = set()
            for member in archive.infolist():
                raw = member.filename
                name = PurePosixPath(member.filename)
                drive, _tail = ntpath.splitdrive(raw)
                canonical = "/".join(name.parts).casefold()
                if (
                    "\x00" in raw
                    or "\\" in raw
                    or drive
                    or raw.startswith(("//", "\\\\"))
                    or name.is_absolute()
                    or ".." in name.parts
                    or not name.parts
                ):
                    raise ValueError("plugin archive contains an unsafe path")
                if canonical in seen:
                    raise ValueError("plugin archive contains duplicate or case-colliding paths")
                seen.add(canonical)
                mode = member.external_attr >> 16
                file_type = stat.S_IFMT(mode)
                if stat.S_ISLNK(mode) or file_type not in {0, stat.S_IFREG, stat.S_IFDIR}:
                    raise ValueError("plugin archive contains a link or special file")
                target = staged.joinpath(*name.parts)
                if not target.resolve().is_relative_to(staged.resolve()):
                    raise ValueError("plugin archive path escapes the staging root")
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
