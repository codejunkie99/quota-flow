#!/usr/bin/env python3
"""Install Quota Flow into a Codex home without changing global config."""

from __future__ import annotations

import argparse
import os
import shutil
import stat
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, Sequence


Mode = Literal["install", "check", "uninstall"]


class InstallError(RuntimeError):
    """Raised when an operation cannot be completed safely."""


@dataclass(frozen=True)
class ManifestEntry:
    source: Path
    relative: Path


def _is_regular_file(path: Path) -> bool:
    try:
        return stat.S_ISREG(path.lstat().st_mode)
    except FileNotFoundError:
        return False


def _same_bytes(left: Path, right: Path) -> bool:
    if left.stat().st_size != right.stat().st_size:
        return False
    with left.open("rb") as left_file, right.open("rb") as right_file:
        while True:
            left_chunk = left_file.read(1024 * 1024)
            right_chunk = right_file.read(1024 * 1024)
            if left_chunk != right_chunk:
                return False
            if not left_chunk:
                return True


def _manifest(source_root: Path) -> list[ManifestEntry]:
    source_root = source_root.expanduser().absolute()
    entries: list[ManifestEntry] = []

    skill_root = source_root / "skills" / "quota-flow"
    if not skill_root.is_dir() or skill_root.is_symlink():
        raise InstallError(f"missing or invalid source directory: {skill_root}")
    for source in sorted(skill_root.rglob("*")):
        if source.is_symlink():
            raise InstallError(f"source symlinks are not supported: {source}")
        if source.is_file():
            entries.append(ManifestEntry(source, source.relative_to(source_root)))
        elif not source.is_dir():
            raise InstallError(f"unsupported source path: {source}")

    agents_root = source_root / "agents"
    if not agents_root.is_dir() or agents_root.is_symlink():
        raise InstallError(f"missing or invalid source directory: {agents_root}")
    for source in sorted(agents_root.glob("*.toml")):
        if not _is_regular_file(source):
            raise InstallError(f"source is not a regular file: {source}")
        entries.append(ManifestEntry(source, source.relative_to(source_root)))

    for relative in (Path("prompts/quota-flow.md"), Path("bin/quota-flow")):
        source = source_root / relative
        if not _is_regular_file(source):
            raise InstallError(f"missing or invalid source file: {source}")
        entries.append(ManifestEntry(source, relative))

    if not any(entry.relative.parts[:2] == ("skills", "quota-flow") for entry in entries):
        raise InstallError(f"source directory contains no files: {skill_root}")
    if not any(entry.relative.parts[0] == "agents" for entry in entries):
        raise InstallError(f"source directory contains no agent TOML files: {agents_root}")
    return entries


def _inside_home_ancestors(home: Path, destination: Path) -> list[Path]:
    relative = destination.relative_to(home)
    return [home.joinpath(*relative.parts[:index]) for index in range(1, len(relative.parts))]


def _validate_home(home: Path) -> None:
    if home.is_symlink():
        raise InstallError(f"Codex home must not be a symlink: {home}")
    if home.exists() and not home.is_dir():
        raise InstallError(f"Codex home is not a directory: {home}")


def _preflight_paths(home: Path, entries: Sequence[ManifestEntry]) -> None:
    _validate_home(home)
    checked: set[Path] = set()
    for entry in entries:
        destination = home / entry.relative
        for ancestor in _inside_home_ancestors(home, destination):
            if ancestor in checked:
                continue
            checked.add(ancestor)
            if ancestor.is_symlink():
                raise InstallError(f"destination ancestor is a symlink: {ancestor}")
            if ancestor.exists() and not ancestor.is_dir():
                raise InstallError(f"destination ancestor is not a directory: {ancestor}")


def _preflight_install(home: Path, entries: Sequence[ManifestEntry]) -> None:
    _preflight_paths(home, entries)
    for entry in entries:
        destination = home / entry.relative
        if destination.is_symlink():
            raise InstallError(f"destination is a symlink: {destination}")
        if destination.exists():
            if not _is_regular_file(destination):
                raise InstallError(f"destination is not a regular file: {destination}")
            if not _same_bytes(entry.source, destination):
                raise InstallError(f"destination differs from source: {destination}")


def _install(home: Path, entries: Sequence[ManifestEntry]) -> None:
    _preflight_install(home, entries)
    for entry in entries:
        destination = home / entry.relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        if not destination.exists():
            shutil.copy2(entry.source, destination)
        elif entry.relative == Path("bin/quota-flow"):
            shutil.copymode(entry.source, destination)


def _check(home: Path, entries: Sequence[ManifestEntry]) -> None:
    _preflight_paths(home, entries)
    problems: list[str] = []
    for entry in entries:
        destination = home / entry.relative
        if destination.is_symlink() or not _is_regular_file(destination):
            problems.append(f"missing or invalid: {destination}")
            continue
        if not _same_bytes(entry.source, destination):
            problems.append(f"contents differ: {destination}")
        source_exec = stat.S_IMODE(entry.source.stat().st_mode) & 0o111
        destination_exec = stat.S_IMODE(destination.stat().st_mode) & 0o111
        if destination_exec != source_exec:
            problems.append(f"executable mode differs: {destination}")
    if problems:
        raise InstallError("check failed:\n" + "\n".join(problems))


def _uninstall(home: Path, entries: Sequence[ManifestEntry]) -> None:
    _preflight_paths(home, entries)
    removable: list[Path] = []
    problems: list[str] = []
    for entry in entries:
        destination = home / entry.relative
        if not destination.exists() and not destination.is_symlink():
            continue
        if destination.is_symlink() or not _is_regular_file(destination):
            problems.append(f"modified or invalid: {destination}")
        elif not _same_bytes(entry.source, destination):
            problems.append(f"modified: {destination}")
        else:
            removable.append(destination)
    if problems:
        raise InstallError("uninstall refused:\n" + "\n".join(problems))
    for destination in removable:
        destination.unlink()


def install(source_root: Path | str, codex_home: Path | str, mode: Mode = "install") -> None:
    """Install, verify, or uninstall Quota Flow files."""
    source = Path(source_root)
    home = Path(codex_home).expanduser().absolute()
    entries = _manifest(source)
    if mode == "install":
        _install(home, entries)
    elif mode == "check":
        _check(home, entries)
    elif mode == "uninstall":
        _uninstall(home, entries)
    else:
        raise ValueError(f"unknown mode: {mode}")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--codex-home",
        type=Path,
        default=Path(os.environ.get("CODEX_HOME", "~/.codex")).expanduser(),
        help="destination Codex home (default: CODEX_HOME or ~/.codex)",
    )
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument("--check", action="store_true", help="verify installed files")
    modes.add_argument("--uninstall", action="store_true", help="remove unchanged installed files")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    mode: Mode = "check" if args.check else "uninstall" if args.uninstall else "install"
    source_root = Path(__file__).resolve().parents[1]
    try:
        install(source_root, args.codex_home, mode)
    except (InstallError, OSError) as error:
        print(f"quota-flow: {error}", file=sys.stderr)
        return 1
    print(f"quota-flow: {mode} complete")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
