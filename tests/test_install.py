from __future__ import annotations

import importlib.util
import os
import stat
import sys
import tempfile
import unittest
from pathlib import Path


INSTALL_PATH = Path(__file__).resolve().parents[1] / "scripts" / "install.py"
SPEC = importlib.util.spec_from_file_location("quota_flow_install", INSTALL_PATH)
assert SPEC is not None and SPEC.loader is not None
installer = importlib.util.module_from_spec(SPEC)
sys.modules[SPEC.name] = installer
SPEC.loader.exec_module(installer)


class InstallerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        root = Path(self.temporary.name)
        self.source = root / "source"
        self.home = root / "home"
        files = {
            "skills/quota-flow/SKILL.md": b"skill\n",
            "skills/quota-flow/nested/reference.txt": b"reference\n",
            "agents/quota-flow.toml": b'name = "quota-flow"\n',
            "agents/helper.toml": b'name = "helper"\n',
            "prompts/quota-flow.md": b"prompt\n",
            "bin/quota-flow": b"#!/bin/sh\nexit 0\n",
        }
        for relative, contents in files.items():
            path = self.source / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(contents)
        (self.source / "bin/quota-flow").chmod(0o755)

    def installed(self, relative: str) -> Path:
        return self.home / relative

    def test_install_check_and_idempotence(self) -> None:
        installer.install(self.source, self.home, "install")
        installer.install(self.source, self.home, "check")
        first_stat = self.installed("prompts/quota-flow.md").stat()
        installer.install(self.source, self.home, "install")
        second_stat = self.installed("prompts/quota-flow.md").stat()
        self.assertEqual(first_stat.st_ino, second_stat.st_ino)

    def test_collision_preflight_makes_no_partial_writes(self) -> None:
        collision = self.installed("prompts/quota-flow.md")
        collision.parent.mkdir(parents=True)
        collision.write_text("user data\n")
        with self.assertRaises(installer.InstallError):
            installer.install(self.source, self.home, "install")
        self.assertEqual(collision.read_text(), "user data\n")
        self.assertFalse(self.installed("skills/quota-flow/SKILL.md").exists())
        self.assertFalse(self.installed("bin/quota-flow").exists())

    def test_symlink_destination_is_rejected(self) -> None:
        external = Path(self.temporary.name) / "external"
        external.write_text("skill\n")
        destination = self.installed("skills/quota-flow/SKILL.md")
        destination.parent.mkdir(parents=True)
        destination.symlink_to(external)
        with self.assertRaises(installer.InstallError):
            installer.install(self.source, self.home, "install")
        self.assertEqual(external.read_text(), "skill\n")
        self.assertFalse(self.installed("bin/quota-flow").exists())

    def test_symlink_ancestor_is_rejected(self) -> None:
        external = Path(self.temporary.name) / "external-directory"
        external.mkdir()
        self.home.mkdir()
        (self.home / "skills").symlink_to(external, target_is_directory=True)
        with self.assertRaises(installer.InstallError):
            installer.install(self.source, self.home, "install")
        self.assertEqual(list(external.iterdir()), [])
        self.assertFalse(self.installed("bin/quota-flow").exists())

    def test_modified_file_refuses_uninstall_without_partial_deletion(self) -> None:
        installer.install(self.source, self.home, "install")
        modified = self.installed("prompts/quota-flow.md")
        modified.write_text("modified\n")
        unchanged = self.installed("skills/quota-flow/SKILL.md")
        with self.assertRaises(installer.InstallError):
            installer.install(self.source, self.home, "uninstall")
        self.assertTrue(unchanged.exists())
        self.assertEqual(modified.read_text(), "modified\n")

    def test_missing_file_fails_check(self) -> None:
        installer.install(self.source, self.home, "install")
        self.installed("agents/helper.toml").unlink()
        with self.assertRaises(installer.InstallError):
            installer.install(self.source, self.home, "check")

    def test_uninstall_allows_missing_and_preserves_unrelated_data(self) -> None:
        installer.install(self.source, self.home, "install")
        self.installed("agents/helper.toml").unlink()
        unrelated = self.installed("skills/quota-flow/user-note.txt")
        unrelated.write_text("keep me\n")
        installer.install(self.source, self.home, "uninstall")
        self.assertTrue(unrelated.exists())
        self.assertEqual(unrelated.read_text(), "keep me\n")
        self.assertTrue(self.installed("skills/quota-flow").is_dir())
        self.assertFalse(self.installed("prompts/quota-flow.md").exists())

    def test_launcher_executable_mode_is_preserved_and_checked(self) -> None:
        installer.install(self.source, self.home, "install")
        launcher = self.installed("bin/quota-flow")
        self.assertEqual(stat.S_IMODE(launcher.stat().st_mode) & 0o111, 0o111)
        launcher.chmod(stat.S_IMODE(launcher.stat().st_mode) & ~0o111)
        with self.assertRaises(installer.InstallError):
            installer.install(self.source, self.home, "check")
        installer.install(self.source, self.home, "install")
        self.assertEqual(stat.S_IMODE(launcher.stat().st_mode) & 0o111, 0o111)
        installer.install(self.source, self.home, "check")

    @unittest.skipUnless(hasattr(os, "symlink"), "symlinks unavailable")
    def test_wrong_path_type_is_rejected_before_writes(self) -> None:
        wrong_type = self.installed("agents/quota-flow.toml")
        wrong_type.mkdir(parents=True)
        with self.assertRaises(installer.InstallError):
            installer.install(self.source, self.home, "install")
        self.assertTrue(wrong_type.is_dir())
        self.assertFalse(self.installed("prompts/quota-flow.md").exists())


if __name__ == "__main__":
    unittest.main()
