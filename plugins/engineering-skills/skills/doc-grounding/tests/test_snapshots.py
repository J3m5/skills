import argparse
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

import import_git_snapshot as importer
import refresh_snapshot as refresher


class SnapshotTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="doc-source-mirror-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.dest = self.root / "current"
        self.dest.mkdir()
        self.source = "gh:fixture/docs/guide#v1"
        self.manifest = {
            "name": "fixture",
            "kind": "project-dependency",
            "installed_version": "1",
            "source_type": "github",
            "chosen_docs_source": self.source,
            "selected_ref": "v1",
        }
        self.write_manifest()
        (self.dest / "guide.md").write_text("old docs")

    def write_manifest(self):
        (self.dest / "manifest.json").write_text(json.dumps(self.manifest))

    def args(self, **overrides):
        values = {
            "snapshot_dir": str(self.dest),
            "source": None,
            "installed_version": None,
            "selected_ref": None,
            "fetch_date": "2026-10-16",
            "min_files": 1,
            "keep_temp": False,
            "dry_run": False,
        }
        values.update(overrides)
        return argparse.Namespace(**values)

    def add_history(self):
        history = self.dest / "history" / "v0" / "guide.md"
        history.parent.mkdir(parents=True)
        history.write_text("retained docs")
        return history

    def export(self, command):
        # Simulate only the mdzilla process; keep all snapshot handling real.
        self.assertEqual(command[0], "mdzilla")
        staged = Path(command[-1])
        staged.mkdir()
        (staged / "guide.md").write_text(f"docs from {command[1]}")

    def tree(self):
        return {
            str(p.relative_to(self.dest)): p.read_bytes()
            for p in self.dest.rglob("*")
            if p.is_file()
        }

    def test_refresh_preserves_retained_history_and_updates_current_docs(self):
        history = self.add_history()
        with patch.object(refresher, "run", side_effect=self.export):
            refresher.refresh(self.args())
        self.assertEqual(history.read_text(), "retained docs")
        self.assertEqual(
            (self.dest / "guide.md").read_text(), f"docs from {self.source}"
        )
        manifest = json.loads((self.dest / "manifest.json").read_text())
        self.assertEqual(manifest["file_count"], len(self.tree()))

    def test_selected_ref_changes_the_source_actually_exported(self):
        with patch.object(refresher, "run", side_effect=self.export):
            refresher.refresh(self.args(selected_ref="v2", installed_version="2"))
        expected = "gh:fixture/docs/guide#v2"
        self.assertEqual((self.dest / "guide.md").read_text(), f"docs from {expected}")
        manifest = json.loads((self.dest / "manifest.json").read_text())
        self.assertEqual(manifest["chosen_docs_source"], expected)
        self.assertEqual(manifest["selected_ref"], "v2")
        self.assertEqual(manifest["installed_version"], "2")

    def test_refresh_supports_export_sources_and_existing_mdzilla_manifests(self):
        for source_type, source in [
            ("http", "https://example.test/v1/"),
            ("npm", "npm:fixture@1.0.0"),
            ("local", str(self.root / "source")),
            ("mdzilla", self.source),
            ("mdzilla-github", self.source),
        ]:
            with self.subTest(source_type=source_type):
                self.manifest.update(source_type=source_type, chosen_docs_source=source)
                self.write_manifest()
                with patch.object(refresher, "run", side_effect=self.export):
                    refresher.refresh(self.args())
                self.assertEqual(
                    (self.dest / "guide.md").read_text(), f"docs from {source}"
                )

    def test_ref_override_for_unpinnable_source_does_not_relabel_old_docs(self):
        self.manifest.update(
            source_type="http", chosen_docs_source="https://example.test/v1/"
        )
        self.write_manifest()
        before = self.tree()
        with (
            patch.object(refresher, "run") as exporter,
            self.assertRaisesRegex(SystemExit, "--selected-ref"),
        ):
            refresher.refresh(self.args(selected_ref="v2"))
        exporter.assert_not_called()
        self.assertEqual(self.tree(), before)

    def test_http_fragment_is_not_recorded_as_a_git_ref(self):
        self.manifest.update(
            source_type="http", chosen_docs_source="https://example.test/v1/"
        )
        self.manifest.pop("selected_ref")
        self.write_manifest()
        with patch.object(refresher, "run", side_effect=self.export):
            refresher.refresh(self.args(source="https://example.test/v2/#guide"))
        manifest = json.loads((self.dest / "manifest.json").read_text())
        self.assertNotIn("selected_ref", manifest)

    def test_existing_github_ref_is_used_when_source_has_no_pin(self):
        self.manifest["chosen_docs_source"] = "gh:fixture/docs/guide"
        self.write_manifest()
        with patch.object(refresher, "run", side_effect=self.export):
            refresher.refresh(self.args())
        self.assertEqual(
            (self.dest / "guide.md").read_text(), f"docs from {self.source}"
        )

    def test_dry_run_preserves_the_entire_destination(self):
        self.add_history()
        before = self.tree()
        with patch.object(refresher, "run", side_effect=self.export):
            result = refresher.refresh(self.args(dry_run=True))
        self.assertEqual(self.tree(), before)
        self.addCleanup(shutil.rmtree, result["temp_dir"])

    def test_failed_or_empty_export_does_not_replace_current_docs(self):
        self.add_history()
        before = self.tree()
        with (
            patch.object(
                refresher,
                "run",
                side_effect=subprocess.CalledProcessError(1, "mdzilla"),
            ),
            self.assertRaises(subprocess.CalledProcessError),
        ):
            refresher.refresh(self.args())
        with (
            patch.object(
                refresher, "run", side_effect=lambda cmd: Path(cmd[-1]).mkdir()
            ),
            self.assertRaises(SystemExit),
        ):
            refresher.refresh(self.args())
        self.assertEqual(self.tree(), before)

    def test_exported_history_collision_leaves_existing_history_untouched(self):
        self.add_history()
        before = self.tree()

        def conflicting_export(command):
            self.export(command)
            history = Path(command[-1]) / "history" / "v0" / "guide.md"
            history.parent.mkdir(parents=True)
            history.write_text("upstream history")

        with (
            patch.object(refresher, "run", side_effect=conflicting_export),
            self.assertRaises((SystemExit, FileExistsError)),
        ):
            refresher.refresh(self.args())
        self.assertEqual(self.tree(), before)

    def test_failed_install_restores_current_docs_and_history(self):
        self.add_history()
        before = self.tree()
        rename = Path.rename

        def failing_install(path, target):
            if path.name == "snapshot" and Path(target) == self.dest:
                raise OSError("simulated install failure")
            return rename(path, target)

        with (
            patch.object(refresher, "run", side_effect=self.export),
            patch.object(Path, "rename", failing_install),
            self.assertRaises(OSError),
        ):
            refresher.refresh(self.args())
        self.assertEqual(self.tree(), before)

    def test_git_reimport_preserves_history(self):
        history = self.add_history()
        repo = self.root / "upstream"
        repo.mkdir()
        subprocess.run(["git", "init", "-q", str(repo)], check=True)
        (repo / "guide.md").write_text("git docs")
        subprocess.run(["git", "-C", str(repo), "add", "guide.md"], check=True)
        subprocess.run(
            [
                "git",
                "-C",
                str(repo),
                "-c",
                "user.name=Fixture",
                "-c",
                "user.email=fixture@example.test",
                "-c",
                "core.hooksPath=/dev/null",
                "commit",
                "-qm",
                "Fixture",
            ],
            check=True,
        )
        args = argparse.Namespace(
            repo=str(repo),
            ref="HEAD",
            dest=str(self.dest),
            name="fixture",
            dependency=None,
            kind="project-dependency",
            installed_version="2",
            logical_project_name=None,
            docs_directory_name=None,
            subdir=None,
            notes="",
            fetch_date="2026-10-16",
            replace=True,
            min_files=1,
        )
        importer.import_snapshot(args)
        self.assertEqual(history.read_text(), "retained docs")
        self.assertEqual((self.dest / "guide.md").read_text(), "git docs")


if __name__ == "__main__":
    unittest.main()
