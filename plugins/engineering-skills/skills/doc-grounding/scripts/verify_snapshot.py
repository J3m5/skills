#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from common import count_files, load_json, manifest_kind, manifest_name


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Verify a docs snapshot directory and its manifest."
    )
    parser.add_argument("--snapshot-dir", required=True)
    parser.add_argument("--min-files", type=int, default=1)
    parser.add_argument("--expect-name")
    parser.add_argument("--expect-kind", choices=["system-tool", "project-dependency"])
    # Backward-compatible alias for older callers.
    parser.add_argument("--expect-dependency")
    parser.add_argument("--expect-installed-version")
    parser.add_argument("--expect-source-type")
    parser.add_argument("--expect-selected-ref")
    parser.add_argument("--expect-selected-subdir")
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    snapshot_dir = Path(args.snapshot_dir)
    manifest_path = snapshot_dir / "manifest.json"
    if not snapshot_dir.exists():
        raise SystemExit(f"Snapshot directory does not exist: {snapshot_dir}")
    if not manifest_path.exists():
        raise SystemExit(f"Missing manifest.json in {snapshot_dir}")

    manifest = load_json(manifest_path)
    name = manifest_name(manifest, snapshot_dir)
    kind = manifest_kind(manifest, snapshot_dir)
    file_count = count_files(snapshot_dir)
    payload = {
        "snapshot_dir": str(snapshot_dir),
        "file_count": file_count,
        "manifest_name": name,
        "manifest_kind": kind,
        "manifest_installed_version": manifest.get("installed_version"),
        "manifest_source_type": manifest.get("source_type"),
        "manifest_selected_ref": manifest.get("selected_ref"),
        "manifest_selected_subdir": manifest.get("selected_subdir"),
    }

    if file_count < args.min_files:
        raise SystemExit(
            f"Snapshot {snapshot_dir} contains only {file_count} files; expected at least {args.min_files}"
        )
    expectations = {
        "name": args.expect_name or args.expect_dependency,
        "kind": args.expect_kind,
        "installed_version": args.expect_installed_version,
        "source_type": args.expect_source_type,
        "selected_ref": args.expect_selected_ref,
        "selected_subdir": args.expect_selected_subdir,
    }
    for key, expected in expectations.items():
        if expected is None:
            continue
        actual = {"name": name, "kind": kind}.get(key, manifest.get(key))
        if actual != expected:
            raise SystemExit(
                f"Manifest mismatch for {key}: expected {expected}, got {actual}"
            )

    json.dump(payload, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
