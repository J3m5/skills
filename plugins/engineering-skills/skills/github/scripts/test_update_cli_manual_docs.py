#!/usr/bin/env python3
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import update_cli_manual_docs as updater


class UpdateCliManualDocsTests(unittest.TestCase):
    def make_config(
        self, output_root: Path, *, full_refresh: bool = False
    ) -> updater.Config:
        return updater.Config(
            start_url=updater.DEFAULT_START_URL,
            output_root=output_root,
            max_pages=None,
            delay_seconds=0,
            timeout_seconds=1,
            full_refresh=full_refresh,
            no_clean=False,
        )

    def test_incremental_error_does_not_prune_existing_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = Path(temp_dir) / "github"
            manual_file = output_root / "manual" / "existing.md"
            manual_file.parent.mkdir(parents=True)
            manual_file.write_text("existing\n", encoding="utf-8")
            state = {
                "version": updater.STATE_VERSION,
                "pages": {
                    "https://cli.github.com/manual/existing": {
                        "links": [],
                        "output_path": str(manual_file),
                    }
                },
            }
            (output_root / updater.STATE_FILENAME).write_text(
                json.dumps(state),
                encoding="utf-8",
            )

            with (
                patch.object(
                    updater,
                    "fetch_latest_release_version",
                    return_value=("v2.96.0", None),
                ),
                patch.object(updater, "fetch_page", side_effect=OSError("offline")),
            ):
                status = updater.refresh_docs(self.make_config(output_root))

            manifest = json.loads(
                (output_root / "manifest.json").read_text(encoding="utf-8")
            )
            saved_state = json.loads(
                (output_root / updater.STATE_FILENAME).read_text(encoding="utf-8")
            )
            self.assertEqual(status, 1)
            self.assertTrue(manual_file.exists())
            self.assertFalse(manifest["prune_enabled"])
            self.assertEqual(len(manifest["errors"]), 1)
            self.assertIn(
                "https://cli.github.com/manual/existing",
                saved_state["pages"],
            )

    def test_failed_full_refresh_preserves_existing_output(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            output_root = Path(temp_dir) / "github"
            output_root.mkdir()
            sentinel = output_root / "sentinel.txt"
            sentinel.write_text("keep\n", encoding="utf-8")

            with (
                patch.object(
                    updater,
                    "parse_args",
                    return_value=self.make_config(output_root, full_refresh=True),
                ),
                patch.object(updater, "refresh_docs", return_value=1),
            ):
                status = updater.main()

            self.assertEqual(status, 1)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep\n")

    def test_staged_output_replaces_existing_tree(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            output_root = root / "github"
            staged_root = root / "staged"
            output_root.mkdir()
            staged_root.mkdir()
            (output_root / "old.txt").write_text("old\n", encoding="utf-8")
            (staged_root / "new.txt").write_text("new\n", encoding="utf-8")

            updater.install_staged_output(staged_root, output_root)

            self.assertFalse(staged_root.exists())
            self.assertFalse((output_root / "old.txt").exists())
            self.assertEqual(
                (output_root / "new.txt").read_text(encoding="utf-8"),
                "new\n",
            )


if __name__ == "__main__":
    unittest.main()
